// evaluate.ts — /pvp 评估我的：评估已有宝可梦
// 规则：显示 PvPokeTW 物种排名 + 推荐配招 + 我的配招 + IV 差别

import * as fs from 'fs';
import * as path from 'path';
import { MyPokemon } from './add';
import { getSpeciesCn, getMoveCn } from './mapper';
import { loadGamemaster, getPokemonBase, computeBestIV, parseUserIV, findUserIVInResults, computeIVDiff, getRankings } from './fetcher';

const DATA_DIR = path.resolve(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'my_pokemon.json');

function loadMyPokemon(): MyPokemon[] {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf-8');
      return JSON.parse(raw) as MyPokemon[];
    }
  } catch { /* 忽略 */ }
  return [];
}

interface EvaluateEntry {
  name: string;
  speciesId: string;
  iv: [number, number, number];
  cp: number;
  level: number;
  built: boolean;
  note: string;
  moves: string[];
  bestIV: string;
  ivDiff: string;
  suggestion: string;
  pvpRank: number | string;
  recommendedFast: string;
  recommendedCharged: string[];
}

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  'master': '大师联盟',
  '484': '小小杯',
};

function resolveLeague(input: string): string | null {
  const map: Record<string, string> = {
    '1500': '1500', '超级': '1500', '超级联盟': '1500',
    '2500': '2500', '高级': '2500', '高级联盟': '2500',
    'master': 'master', '大师': 'master', '大师联盟': 'master', '无限制': 'master',
    '484': '484', '小小': '484', '小小杯': '484', '幼童': '484',
  };
  return map[input.trim()] || null;
}

function formatIVDiff(diff: { atk: number; def: number; hp: number }): string {
  const parts: string[] = [];
  if (diff.atk !== 0) parts.push(`攻${diff.atk > 0 ? '+' : ''}${diff.atk}`);
  if (diff.def !== 0) parts.push(`防${diff.def > 0 ? '+' : ''}${diff.def}`);
  if (diff.hp !== 0) parts.push(`血${diff.hp > 0 ? '+' : ''}${diff.hp}`);
  if (parts.length === 0) return '相同';
  return parts.join(' ');
}

/**
 * 从 rankings entry 读取推荐配招（使用率最高的 1 小招 + 2 充能招）
 */
function getRecommendedMoves(entry: any): { fast: string; charged: string[] } {
  // 优先使用 PvPoke 官方推荐组合（moveset 字段）
  if (entry.moveset && Array.isArray(entry.moveset) && entry.moveset.length >= 1) {
    return {
      fast: entry.moveset[0],
      charged: entry.moveset.slice(1, 3),
    };
  }
  // 回退：用使用率最高的小招 + 2 个充能招
  const fastMoves: any[] = (entry.moves?.fastMoves || []).sort((a: any, b: any) => b.uses - a.uses);
  const chargedMoves: any[] = (entry.moves?.chargedMoves || []).sort((a: any, b: any) => b.uses - a.uses);
  return {
    fast: fastMoves.length > 0 ? fastMoves[0].moveId : '',
    charged: chargedMoves.slice(0, 2).map((c: any) => c.moveId),
  };
}

/**
 * 判断某个招式是否为精英/限定招式
 */
export function isEliteMove(speciesId: string, moveId: string): boolean {
  try {
    const elitePath = path.join(DATA_DIR, 'elite_moves.json');
    if (fs.existsSync(elitePath)) {
      const elite = JSON.parse(fs.readFileSync(elitePath, 'utf-8'));
      // 先尝试原生 speciesId，再尝试去掉 _shadow 后查询
      const lookups = [speciesId];
      if (speciesId.endsWith('_shadow')) {
        lookups.push(speciesId.slice(0, -7));
      }
      for (const sid of lookups) {
        const moves = elite[sid];
        if (Array.isArray(moves)) {
          for (const eliteMove of moves) {
            if (eliteMove === moveId) return true;
            const cn = getMoveCn(eliteMove);
            if (cn === moveId) return true;
          }
        }
      }
    }
  } catch { /* 忽略 */ }
  return false;
}

/**
 * 格式化招式行：标识"推荐配招"或"我的配招"
 * 用 getMoveCn 转中文，精英招式加 *
 */
function formatMoveLine(fast: string, charged: string[], speciesId: string, label: string): string {
  const fastCn = getMoveCn(fast) + (isEliteMove(speciesId, fast) ? '（厉害特殊招式学习器）' : '');
  const chargedCn = charged.map(m => getMoveCn(m) + (isEliteMove(speciesId, m) ? '（厉害特殊招式学习器）' : ''));
  const lines = [
    `   ${label}：`,
    `     小招：${fastCn}`,
  ];
  chargedCn.forEach((m, i) => {
    lines.push(`     充能招${i + 1}：${m}`);
  });
  return lines.join('\n');
}

/**
 * /pvp 评估我的 <联盟>
 */
export async function handleEvaluate(args: string[]): Promise<string> {
  if (args.length === 0) {
    return '用法：/pvp 评估我的 <联盟>\n示例：/pvp 评估我的 1500\n      /pvp 评估我的 2500';
  }

  const league = resolveLeague(args[0]);
  if (!league) return `未知联盟: ${args[0]}，支持 1500 / 2500 / master / 484`;

  const cpLimit = league === '1500' ? 1500 : league === '2500' ? 2500 : league === 'master' ? 10000 : 484;
  const leagueLabel = LEAGUE_LABELS[league] || league;

  const all = loadMyPokemon();
  const filtered = all.filter(p => p.league === league);
  if (filtered.length === 0) return `暂无 ${leagueLabel} 的已记录宝可梦`;

  const gm = await loadGamemaster();
  if (!gm) return '无法加载 gamemaster 数据，请稍后重试';

  const rankings = await getRankings(league);

  // 构建 rankings 查找索引
  const rankingMap = new Map<string, { rank: number; entry: any }>();
  if (rankings && Array.isArray(rankings)) {
    rankings.forEach((entry: any, i: number) => {
      rankingMap.set(entry.speciesId, { rank: i + 1, entry });
    });
  }

  const entries: EvaluateEntry[] = [];

  for (const p of filtered) {
    // 物种排名
    const rankInfo = rankingMap.get(p.speciesId);
    const pvpRank = rankInfo ? rankInfo.rank : '—';

    // 推荐配招
    let recFast = '';
    let recCharged: string[] = [];
    if (rankInfo) {
      const rec = getRecommendedMoves(rankInfo.entry);
      recFast = rec.fast;
      recCharged = rec.charged;
    }

    // 计算 IV
    const base = getPokemonBase(gm, p.speciesId);
    if (!base) {
      entries.push({
        name: p.name,
        speciesId: p.speciesId,
        iv: p.iv,
        cp: p.cp,
        level: p.level,
        built: p.built,
        note: p.note,
        moves: p.moves || [],
        bestIV: '—',
        ivDiff: '—',
        suggestion: '待确认（无基础数据）',
        pvpRank,
        recommendedFast: recFast,
        recommendedCharged: recCharged,
      });
      continue;
    }

    const ivResult = computeBestIV(base, cpLimit);
    const best = ivResult.best;
    const bestIVStr = best ? `${best.iv[0]}/${best.iv[1]}/${best.iv[2]}` : '—';

    const found = findUserIVInResults(p.iv, ivResult);
    let ivDiff: string;
    let suggestion: string;

    if (found.record) {
      const d = computeIVDiff(best!.iv, p.iv);
      ivDiff = formatIVDiff(d);
      suggestion = found.record.rank <= 50 ? '优先培养' : '暂缓培养';
    } else {
      ivDiff = '—';
      suggestion = '暂缓培养';
    }

    if (p.built) suggestion = '已培养，跳过';

    entries.push({
      name: p.name,
      speciesId: p.speciesId,
      iv: p.iv,
      cp: p.cp,
      level: p.level,
      built: p.built,
      note: p.note,
      moves: p.moves || [],
      bestIV: bestIVStr,
      ivDiff,
      suggestion,
      pvpRank,
      recommendedFast: recFast,
      recommendedCharged: recCharged,
    });

    // 如果用户没手动录入配招，自动填充推荐配招到文件
    if (recFast && p.moves.length === 0) {
      const movesToSave = [recFast, ...recCharged];
      p.moves = movesToSave;
      const allP = loadMyPokemon();
      const idx = allP.findIndex(
        (x) => x.speciesId === p.speciesId && x.league === p.league &&
          x.iv[0] === p.iv[0] && x.iv[1] === p.iv[1] && x.iv[2] === p.iv[2]
      );
      if (idx >= 0) {
        allP[idx].moves = movesToSave;
        allP[idx].updatedAt = new Date().toISOString();
        fs.writeFileSync(DATA_FILE, JSON.stringify(allP, null, 2), 'utf-8');
      }
    }
  }

  // 排序
  const order: Record<string, number> = {
    '优先培养': 0, '暂缓培养': 1, '已培养，跳过': 2, '待确认（无基础数据）': 3,
  };
  entries.sort((a, b) => (order[a.suggestion] ?? 99) - (order[b.suggestion] ?? 99));

  // 统计
  const total = entries.length;
  const priorityCount = entries.filter(e => e.suggestion === '优先培养').length;
  const deferCount = entries.filter(e => e.suggestion === '暂缓培养').length;
  const doneCount = entries.filter(e => e.suggestion === '已培养，跳过').length;
  const unknownCount = entries.filter(e => e.suggestion === '待确认（无基础数据）').length;

  // 输出
  const lines: string[] = [];
  lines.push(`📦 ${leagueLabel} 库存`);
  lines.push(`共 ${total} 只`);
  if (priorityCount > 0) lines.push(`🟢 优先培养：${priorityCount}`);
  if (deferCount > 0) lines.push(`🔴 暂缓培养：${deferCount}`);
  if (doneCount > 0) lines.push(`✅ 已培养：${doneCount}`);
  if (unknownCount > 0) lines.push(`❓ 待确认：${unknownCount}`);
  lines.push('');

  for (const e of entries) {
    const ivStr = `${e.iv[0]}/${e.iv[1]}/${e.iv[2]}`;
    const rankStr = typeof e.pvpRank === 'number' ? `#${e.pvpRank}` : e.pvpRank;
    const suggestionIcon = e.suggestion === '优先培养' ? '🟢' : e.suggestion === '暂缓培养' ? '🔴' : e.suggestion === '已培养，跳过' ? '✅' : '❓';

    lines.push(`📘 ${e.name}`);
    lines.push(`   PvPokeTW 排名：${rankStr}`);
    lines.push(`   IV：${ivStr} ｜ 最佳IV：${e.bestIV} ｜ 差别：${e.ivDiff}`);

    // 推荐配招
    if (e.recommendedFast) {
      lines.push(formatMoveLine(e.recommendedFast, e.recommendedCharged, e.speciesId, '推荐配招'));
    }

    // 我的配招（如果用户有手动录入且与推荐不同）
    if (e.moves.length > 0) {
      const userFast = e.moves[0];
      const userCharged = e.moves.slice(1);
      if (userFast !== e.recommendedFast ||
          userCharged[0] !== e.recommendedCharged[0] ||
          userCharged[1] !== e.recommendedCharged[1]) {
        lines.push(formatMoveLine(userFast, userCharged, e.speciesId, '我的配招'));
      }
    }

    lines.push(`   状态：${e.built ? '✅ 已培养' : '⏳ 未培养'} ｜ 建议：${suggestionIcon} ${e.suggestion}`);
    if (e.note) lines.push(`   📝 ${e.note}`);
    lines.push('');
  }

  return lines.join('\n');
}
