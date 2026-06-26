// buildOrder.ts — /pvp 培养顺序：资源投入顺序排序
// 复用 train.ts 的筛选和评分逻辑，输出格式偏"资源投入顺序"

import { loadMyPokemon } from './list';
import { getRankings, loadGamemaster } from './fetcher';
import { getSpeciesCn, getMoveCn } from './mapper';
import type { MyPokemon } from './add';
import type { PvPokePokemon } from './types';

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  'master': '大师联盟',
};

const LEAGUE_ORDER = ['1500', '2500', 'master'];

function loadEliteMoves(): Record<string, string[]> {
  try {
    const path = require('path');
    const fs = require('fs');
    const elitePath = path.resolve(__dirname, '..', 'data', 'elite_moves.json');
    if (fs.existsSync(elitePath)) {
      return JSON.parse(fs.readFileSync(elitePath, 'utf-8'));
    }
  } catch { /* ignore */ }
  return {};
}

function isEliteByMoveId(speciesId: string, moveId: string): boolean {
  const elite = loadEliteMoves();
  const moves = elite[speciesId];
  if (Array.isArray(moves)) {
    for (const em of moves) {
      if (em === moveId) return true;
      const cn = getMoveCn(em);
      if (cn === moveId) return true;
    }
  }
  return false;
}

function getRankingMoves(entry: PvPokePokemon): { fast: string; charged: string[] } {
  if (entry.moveset && entry.moveset.length >= 3) {
    return { fast: entry.moveset[0], charged: entry.moveset.slice(1, 3) };
  }
  const fastSorted = [...(entry.moves?.fastMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  const chargedSorted = [...(entry.moves?.chargedMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  return {
    fast: fastSorted[0]?.moveId || '',
    charged: chargedSorted.slice(0, 2).map((c: any) => c.moveId),
  };
}

function findRankingEntry(rankings: PvPokePokemon[], speciesId: string): { entry: PvPokePokemon; rank: number } | null {
  const idx = rankings.findIndex(e => e.speciesId === speciesId);
  if (idx < 0) return null;
  return { entry: rankings[idx], rank: idx + 1 };
}

interface BuildOrderItem {
  speciesId: string;
  name: string;
  league: string;
  pvpokeRank: number;
  pvpokeScore: number;
  ivRank: number;
  built: boolean;
  missingMoves: string[];
  hasEliteMissing: boolean;
  score: number;
  suggestion: string;
  reasons: string[];
  needsResource: string[];
}

/**
 * /pvp 培养顺序
 */
export async function buildOrderList(leagueKey?: string): Promise<string> {
  const myPokes = loadMyPokemon();
  if (myPokes.length === 0) {
    return '暂无已记录宝可梦\n先去添加吧：/pvp 添加 <宝可梦> <联盟> <IV> <CP> <等级>';
  }

  // 过滤联盟
  let filtered: MyPokemon[];
  let leagueKeys: string[];
  if (leagueKey) {
    filtered = myPokes.filter(p => p.league === leagueKey);
    leagueKeys = [leagueKey];
  } else {
    filtered = myPokes;
    leagueKeys = LEAGUE_ORDER.filter(lk => myPokes.some(p => p.league === lk));
  }

  if (filtered.length === 0) {
    const label = leagueKey ? (LEAGUE_LABELS[leagueKey] || leagueKey) : '';
    return `${label ? label + ' ' : ''}暂无已记录宝可梦`;
  }

  // 加载 rankings
  const rankingsMap: Record<string, PvPokePokemon[]> = {};
  for (const lk of leagueKeys) {
    try {
      const ranks = await getRankings(lk);
      if (ranks && ranks.length > 0) rankingsMap[lk] = ranks;
    } catch { /* ignore */ }
  }

  const gm = await loadGamemaster();

  const items: BuildOrderItem[] = [];

  for (const poke of filtered) {
    const lk = poke.league;
    const rankings = rankingsMap[lk];
    if (!rankings || rankings.length === 0) continue;

    const rankingInfo = findRankingEntry(rankings, poke.speciesId);
    if (!rankingInfo) continue;

    const entry = rankingInfo.entry;
    const pvpokeRank = rankingInfo.rank;
    const moves = getRankingMoves(entry);

    // IV 排名
    let ivRank = 999;
    try {
      if (lk !== 'master' && gm) {
        const { getPokemonBase, computeBestIV } = require('./fetcher');
        const base = getPokemonBase(gm, poke.speciesId);
        if (base) {
          const cpLimit = lk === '1500' ? 1500 : 2500;
          const ivResult = computeBestIV(base, cpLimit);
          const top50 = ivResult.top50 || [];
          for (let i = 0; i < top50.length; i++) {
            if (top50[i].iv[0] === poke.iv[0] && top50[i].iv[1] === poke.iv[1] && top50[i].iv[2] === poke.iv[2]) {
              ivRank = i + 1;
              break;
            }
          }
        }
      }
    } catch { /* ignore */ }

    // 配招缺口
    const userMoves = new Set(poke.moves.map(m => m.toUpperCase()));
    const missingMoves: string[] = [];
    const allRecMoves = [moves.fast, ...moves.charged];
    let hasEliteMissing = false;
    for (const recMove of allRecMoves) {
      if (!recMove) continue;
      const recUpper = recMove.toUpperCase();
      const recCn = getMoveCn(recUpper);
      const found =
        userMoves.has(recUpper) ||
        userMoves.has(recCn) ||
        (recCn && userMoves.has(recCn));
      if (!found) {
        missingMoves.push(recCn || recUpper);
        if (!hasEliteMissing && isEliteByMoveId(poke.speciesId, recUpper)) {
          hasEliteMissing = true;
        }
      }
    }

    // ⭐ 评分（同 train.ts 逻辑）
    let score = 0;
    const rankScore = Math.max(0, 40 - (pvpokeRank - 1) * 0.4);
    score += rankScore;
    if (ivRank <= 50) {
      const ivScore = Math.max(0, 25 - (ivRank - 1) * 0.5);
      score += ivScore;
    }
    if (!poke.built) {
      score += 15;
    } else {
      score -= 10;
    }
    score += Math.min(10, missingMoves.length * 3);
    if (hasEliteMissing) score += 5;
    if (pvpokeRank <= 10) score += 10;
    else if (pvpokeRank <= 30) score += 5;

    // 建议文案
    let suggestion = '';
    if (!poke.built && pvpokeRank <= 10 && ivRank <= 10) suggestion = '⭐ 优先培养';
    else if (!poke.built && (pvpokeRank <= 30 || ivRank <= 30)) suggestion = '推荐培养';
    else if (!poke.built) suggestion = '值得培养';
    else if (missingMoves.length > 0) suggestion = '更新配招';
    else suggestion = '可用 ✓';

    // 原因列表
    const reasons: string[] = [];
    reasons.push(`PvPokeTW 排名 #${pvpokeRank}`);
    if (lk !== 'master' && ivRank <= 50) {
      reasons.push(`IV 排名 #${ivRank}`);
    } else if (lk === 'master') {
      reasons.push(`大师联盟（IV 15/15/15 默认）`);
    }
    if (!poke.built) {
      reasons.push('未培养');
    } else {
      reasons.push('已培养');
    }
    if (missingMoves.length > 0) {
      reasons.push(`推荐配招不完整（缺少 ${missingMoves.join('、')}）`);
    } else {
      reasons.push('推荐配招完整');
    }
    if (hasEliteMissing) {
      reasons.push('需要精英招式');
    }

    // 资源提醒
    const needsResource: string[] = [];
    if (!poke.built) {
      needsResource.push('星尘');
      needsResource.push('糖果');
    }
    if (hasEliteMissing) {
      needsResource.push('精英学习器');
    }

    items.push({
      speciesId: poke.speciesId,
      name: getSpeciesCn(poke.speciesId) || poke.speciesId,
      league: lk,
      pvpokeRank,
      pvpokeScore: entry.score,
      ivRank,
      built: poke.built,
      missingMoves,
      hasEliteMissing,
      score: Math.round(score),
      suggestion,
      reasons,
      needsResource,
    });
  }

  // 排序（降序）
  items.sort((a, b) => b.score - a.score);

  // ===== 输出 =====
  const lines: string[] = [];

  if (leagueKey) {
    const label = LEAGUE_LABELS[leagueKey] || leagueKey;
    lines.push(`📌 ${label} 培养顺序`);
  } else {
    lines.push('📌 当前培养顺序');
  }
  lines.push('');

  let rank = 1;
  for (const item of items) {
    const label = LEAGUE_LABELS[item.league] || item.league;
    lines.push(`${rank}. ${item.name}｜${label}`);
    lines.push(`  建议：${item.suggestion}`);
    lines.push('  原因：');
    for (const r of item.reasons) {
      lines.push(`  * ${r}`);
    }

    if (item.needsResource.length > 0) {
      lines.push(`  需要：${item.needsResource.join('、')}`);
    }
    lines.push('');
    rank++;
  }

  // 全局资源提醒
  lines.push('资源提醒：');
  lines.push('* 需要检查星尘/糖果/精英学习器余量');
  if (items.some(i => !i.built)) {
    lines.push(`* ${items.filter(i => !i.built).length} 只未培养，建议优先投入星尘`);
  }
  if (items.some(i => i.hasEliteMissing)) {
    lines.push(`* ${items.filter(i => i.hasEliteMissing).length} 只需要精英学习器`);
  }

  return lines.join('\n');
}
