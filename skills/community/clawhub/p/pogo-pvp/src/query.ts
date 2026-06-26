// query.ts — 宝可梦查询逻辑（含 IV 查询）

import * as fs from 'fs';
import * as path from 'path';
import { PvPokePokemon, QueryResult, CommandParse } from './types';
import { getSpeciesCn, getMoveCn } from './mapper';
import { isEliteMove } from './evaluate';
import {
  resolveLeague, getRankings, loadGamemaster, getPokemonBase,
  computeBestIV, parseUserIV, computeUserIV, findUserIVInResults,
  computeIVDiff,
} from './fetcher';
import { findSpeciesId as findSpeciesIdIv } from './iv';

const ALIAS_PATH = path.resolve(__dirname, '..', 'data', 'pokemon_alias.json');

export function parseCommand(args: string[]): CommandParse {
  if (args.length < 2) {
    return { pokemon: '', league: '', userIV: null, valid: false, error: '用法：/pvp 培养 <宝可梦> <联盟> [攻击/防御/生命]', suggestions: ['1500', '2500', 'master'] };
  }

  const pokemon = args[0].trim();
  let leagueInput = args[1].trim();
  let userIV: string | null = null;

  if (args.length >= 3) {
    const ivCandidate = args[2].trim();
    if (/^\d{1,2}\/\d{1,2}\/\d{1,2}$/.test(ivCandidate)) {
      userIV = ivCandidate;
    }
  }

  const leagueKey = resolveLeague(leagueInput);
  if (!leagueKey) {
    return {
      pokemon,
      league: leagueInput,
      userIV,
      valid: false,
      error: `未知联盟: ${leagueInput}`,
      suggestions: ['1500 / 超级联盟', '2500 / 高级联盟', 'master / 大师联盟'],
    };
  }

  return { pokemon, league: leagueKey, userIV, valid: true };
}

/** 查找宝可梦 speciesId */
function findSpeciesId(userInput: string): string[] {
  return findSpeciesIdIv(userInput);
}


/** 格式化六维评分（仅备用，不输出到用户） */
function formatSixScores(scores: number[]): string {
  const labels = ['综合', '攻击', '防御', '体', '灵活性', '压制'];
  if (!scores || scores.length === 0) return '';
  return scores.map((s, i) => `${labels[i] || `维${i + 1}`}: ${s}`).join(' | ');
}

/** 格式化类型数组 */
function formatTypes(types: string[]): string {
  const typeCnMap: Record<string, string> = {
    Normal: '一般', Fire: '火', Water: '水', Electric: '电', Grass: '草',
    Ice: '冰', Fighting: '格斗', Poison: '毒', Ground: '地面', Flying: '飞行',
    Psychic: '超能力', Bug: '虫', Rock: '岩石', Ghost: '幽灵', Dragon: '龙',
    Dark: '恶', Steel: '钢', Fairy: '妖精',
  };
  return types.map(t => typeCnMap[t] || t).join('');
}

/** 主查询 */
export async function queryPokemon(pokemonInput: string, leagueKey: string, userIVStr?: string | null): Promise<QueryResult | { error: string }> {
  const speciesIds = findSpeciesId(pokemonInput);
  if (speciesIds.length === 0) {
    return { error: `未找到宝可梦: ${pokemonInput}，请确认名字是否正确` };
  }

  const data = await getRankings(leagueKey);
  if (!data) {
    return { error: `无法读取 ${leagueKey} 数据，暂无本地缓存。请稍后重试或运行 fetch 拉取。` };
  }

  const leagueLabels: Record<string, string> = { '1500': '超级联盟', '2500': '高级联盟', master: '大师联盟' };

  // 搜索匹配
  let found: PvPokePokemon | null = null;
  let rank = 0;
  const targetSet = new Set(speciesIds.map(s => s.toLowerCase()));
  const hit = data.find((item) => targetSet.has(item.speciesId.toLowerCase()));
  if (hit) {
    found = hit;
    rank = data.indexOf(hit) + 1;
  }

  if (!found) {
    return { error: `在 ${leagueLabels[leagueKey] || leagueKey} 中未找到 ${pokemonInput}` };
  }

  let gm: any = null;
  let base = null;
  let ivResult = null;
  let userIVInfo = null;

  try {
    gm = await loadGamemaster();
    if (gm) {
      base = getPokemonBase(gm, found.speciesId);
    }
  } catch { /* gm 加载失败不影响主查询 */ }

  if (base) {
    const cpLimit = { '1500': 1500, '2500': 2500, 'master': 10000 }[leagueKey] || 1500;
    ivResult = computeBestIV(base, cpLimit);

    if (userIVStr) {
      const parsed = parseUserIV(userIVStr);
      if (parsed) {
        const foundRecord = findUserIVInResults(parsed, ivResult);
        const ivDiff = computeIVDiff(ivResult.best.iv, parsed);

        if (foundRecord.record) {
          userIVInfo = {
            iv: `${parsed[0]}/${parsed[1]}/${parsed[2]}`,
            record: foundRecord.record,
            inTop50: true,
            ivDiff,
          };
        } else {
          const computed = computeUserIV(base, parsed, cpLimit);
          userIVInfo = {
            iv: `${parsed[0]}/${parsed[1]}/${parsed[2]}`,
            record: computed,
            inTop50: false,
            ivDiff,
          };
        }
      }
    }
  }

  const types = found.types || base?.types || [];
  const cp = found.cp || 0;
  const level = found.level || 0;
  const now = new Date();

  const result: QueryResult = {
    pokemon: getSpeciesCn(found.speciesId),
    speciesName: found.speciesName,
    league: leagueLabels[leagueKey] || leagueKey,
    rank,
    score: found.score,
    rating: found.rating,
    editorScore: found.editorScore,
    recommendedMoves: found.moveset.map((m: string) => getMoveCn(m) + (isEliteMove(found.speciesId, m) ? '（厉害特殊招式学习器）' : '')),
    fastMoves: found.moves.fastMoves.map((m) => getMoveCn(m.moveId)),
    chargeMoves: found.moves.chargedMoves.map((m) => getMoveCn(m.moveId)),
    stats: found.stats,
    matchups: found.matchups || [],
    counters: found.counters || [],
    sixScores: formatSixScores(found.scores),
    cp,
    level,
    types,
    bestIV: ivResult?.best || null,
    ivTop50: ivResult?.top50 || [],
    userIV: userIVInfo,
    source: 'PvPokeTW',
    fetchedAt: now.toISOString().replace('T', ' ').slice(0, 19),
  };

  return result;
}
