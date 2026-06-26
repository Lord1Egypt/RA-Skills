// team.ts — /pvp 配队：配队推荐 v1.2（含评分 + 关键威胁）
// 评分维度：
//   ① 元覆盖范围（80%）：队伍对当前环境前50的压制能力（属性克制）
//   ② 翻盘能力（10%）：安全换 / 高压充能 / 收割潜力
//   ③ 稳定性（10%）：共同弱点 / 抗性分散
//   ④ 关键威胁：热门环境中压制队伍的 top 5

import * as fs from 'fs';
import * as path from 'path';
import { getSpeciesCn, getMoveCn } from './mapper';
import { getRankings, resolveLeague, loadGamemaster, getPokemonBase } from './fetcher';
import { loadMyPokemon } from './list';
import type { PvPokePokemon, PokemonBase } from './types';

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  'master': '大师联盟',
};

// ===== 类型效果表 =====
// attacker → defender: 效果倍数
// 只包含 PvP 中常见属性
const TYPE_EFFECT: Record<string, Record<string, number>> = {
  normal:   { rock: 0.5, ghost: 0, steel: 0.5 },
  fire:     { fire: 0.5, water: 0.5, grass: 2, ice: 2, bug: 2, rock: 0.5, dragon: 0.5, steel: 2 },
  water:    { fire: 2, water: 0.5, grass: 0.5, ground: 2, rock: 2, dragon: 0.5 },
  electric: { water: 2, electric: 0.5, grass: 0.5, ground: 0, flying: 2, dragon: 0.5 },
  grass:    { fire: 0.5, water: 2, grass: 0.5, poison: 0.5, ground: 2, flying: 0.5, bug: 0.5, rock: 2, dragon: 0.5, steel: 0.5 },
  ice:      { fire: 0.5, water: 0.5, grass: 2, ice: 0.5, ground: 2, flying: 2, dragon: 2, steel: 0.5 },
  fighting: { normal: 2, ice: 2, poison: 0.5, flying: 0.5, psychic: 0.5, bug: 0.5, rock: 2, ghost: 0, dark: 2, steel: 2, fairy: 0.5 },
  poison:   { grass: 2, poison: 0.5, ground: 0.5, rock: 0.5, ghost: 0.5, steel: 0, fairy: 2 },
  ground:   { fire: 2, grass: 0.5, electric: 2, poison: 2, flying: 0, bug: 0.5, rock: 2, steel: 2 },
  flying:   { grass: 2, electric: 0.5, fighting: 2, bug: 2, rock: 0.5, steel: 0.5 },
  psychic:  { fighting: 2, poison: 2, psychic: 0.5, dark: 0, steel: 0.5 },
  bug:      { fire: 0.5, grass: 2, fighting: 0.5, poison: 0.5, flying: 0.5, psychic: 2, ghost: 0.5, dark: 2, steel: 0.5, fairy: 0.5 },
  rock:     { fire: 2, ice: 2, fighting: 0.5, ground: 0.5, flying: 2, bug: 2, steel: 0.5 },
  ghost:    { normal: 0, psychic: 2, ghost: 2, dark: 0.5 },
  dragon:   { dragon: 2, steel: 0.5, fairy: 0 },
  dark:     { fighting: 0.5, psychic: 2, ghost: 2, dark: 0.5, fairy: 0.5 },
  steel:    { fire: 0.5, water: 0.5, electric: 0.5, ice: 2, rock: 2, steel: 0.5, fairy: 2 },
  fairy:    { fire: 0.5, fighting: 2, poison: 0.5, dragon: 2, dark: 2, steel: 0.5 },
};

function getTypeEffectiveness(attackType: string, defenderTypes: string[]): number {
  let best = 0;
  for (const dt of defenderTypes) {
    if (dt === 'none') continue; // normal-only treated as normal
    const eff = TYPE_EFFECT[attackType]?.[dt] ?? 1;
    if (eff > best) best = eff;
  }
  return best;
}

// ===== 数据加载 =====

function loadEliteMoves(): Record<string, string[]> {
  try {
    const elitePath = path.resolve(__dirname, '..', 'data', 'elite_moves.json');
    if (fs.existsSync(elitePath)) {
      return JSON.parse(fs.readFileSync(elitePath, 'utf-8'));
    }
  } catch { /* ignore */ }
  return {};
}

function isEliteMove(speciesId: string, moveId: string): boolean {
  const elite = loadEliteMoves();
  const lookups = [speciesId];
  if (speciesId.endsWith('_shadow')) {
    lookups.push(speciesId.slice(0, -7));
  }
  for (const sid of lookups) {
    const moves = elite[sid];
    if (Array.isArray(moves)) {
      for (const em of moves) {
        if (em === moveId) return true;
        const cn = getMoveCn(em);
        if (cn === moveId) return true;
      }
    }
  }
  return false;
}

function hasMyPokemon(speciesId: string, league: string): boolean {
  const myPokes = loadMyPokemon();
  return myPokes.some(p => p.speciesId === speciesId && p.league === league);
}

function getRecommendedMoves(entry: PvPokePokemon): { fast: string; charged: string[] } {
  if (entry.moveset && entry.moveset.length >= 3) {
    return {
      fast: entry.moveset[0],
      charged: entry.moveset.slice(1, 3),
    };
  }
  const fastSorted = [...(entry.moves?.fastMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  const chargedSorted = [...(entry.moves?.chargedMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  return {
    fast: fastSorted[0]?.moveId || '',
    charged: chargedSorted.slice(0, 2).map((c: any) => c.moveId),
  };
}

function formatMoves(speciesId: string, fast: string, charged: string[]): string {
  const fastCn = getMoveCn(fast) + (isEliteMove(speciesId, fast) ? '（厉害特殊招式学习器）' : '');
  const chargedCn = charged.map(m => getMoveCn(m) + (isEliteMove(speciesId, m) ? '（厉害特殊招式学习器）' : ''));
  return `小招：${fastCn}\n充能招1：${chargedCn[0] || '-'}\n充能招2：${chargedCn[1] || '-'}`;
}

// ===== 组队逻辑 =====

function getMySpeciesForLeague(league: string): string[] {
  const myPokes = loadMyPokemon();
  const seen = new Set<string>();
  const result: string[] = [];
  for (const p of myPokes) {
    if (p.league === league && !seen.has(p.speciesId)) {
      seen.add(p.speciesId);
      result.push(p.speciesId);
    }
  }
  return result;
}

function pickFromRankings(rankings: PvPokePokemon[], speciesIds: string[]): { entry: PvPokePokemon; rank: number }[] {
  const result: { entry: PvPokePokemon; rank: number }[] = [];
  const targets = new Set(speciesIds.map(s => s.toLowerCase()));
  for (let i = 0; i < rankings.length; i++) {
    if (targets.has(rankings[i].speciesId.toLowerCase())) {
      result.push({ entry: rankings[i], rank: i + 1 });
    }
  }
  return result;
}

function findEntryInRankings(rankings: PvPokePokemon[], input: string): { entry: PvPokePokemon; rank: number } | null {
  const lower = input.trim().toLowerCase();
  const idx = rankings.findIndex(e => e.speciesId.toLowerCase() === lower);
  if (idx >= 0) return { entry: rankings[idx], rank: idx + 1 };

  for (let i = 0; i < rankings.length; i++) {
    const cn = getSpeciesCn(rankings[i].speciesId);
    if (cn === input.trim()) return { entry: rankings[i], rank: i + 1 };
    if (cn.includes(input.trim()) || input.trim().includes(cn)) {
      return { entry: rankings[i], rank: i + 1 };
    }
  }

  for (let i = 0; i < rankings.length; i++) {
    if (rankings[i].speciesName.toLowerCase() === lower) {
      return { entry: rankings[i], rank: i + 1 };
    }
  }

  for (let i = 0; i < rankings.length; i++) {
    if (rankings[i].speciesId.toLowerCase().startsWith(lower) || lower.startsWith(rankings[i].speciesId.toLowerCase())) {
      return { entry: rankings[i], rank: i + 1 };
    }
  }

  return null;
}

// ===== 评分逻辑 =====

interface TeamMemberInfo {
  speciesId: string;
  types: string[];         // 宝可梦自身属性
  moves: { fast: string; charged: string[] };
}

/**
 * 获取 gamemaster 中宝可梦的类型和招式类型
 */
function getMoveType(gm: any, moveId: string): string {
  if (!gm?.moves) return 'normal';
  const move = gm.moves.find((m: any) => m.moveId === moveId);
  return move?.type || 'normal';
}

function getPokemonTypes(gm: any, speciesId: string): string[] {
  const base = getPokemonBase(gm, speciesId);
  if (!base || !base.types || base.types.length === 0) return ['normal'];
  return base.types.filter((t: string) => t !== 'none');
}

/**
 * ① 元覆盖范围（80%）
 * 对前50 meta 中每只，检查队伍3只是否至少有一只能打出优势
 * 优势 = fast 或 charged 能克制 opponent（效果≥2）
 * 均势 = 有一招效果1（STAB 加成时同等对待）
 */
function calcMetaCoverage(
  team: TeamMemberInfo[],
  rankings: PvPokePokemon[],
  gm: any,
): { score: number; advantages: number; neutral: number; total: number } {
  const top50 = rankings.slice(0, 50);
  let advantages = 0;
  let neutral = 0;

  for (const opp of top50) {
    const oppTypes = getPokemonTypes(gm, opp.speciesId);
    let bestEff = 0;

    for (const member of team) {
      const moves = [member.moves.fast, ...member.moves.charged];
      for (const moveId of moves) {
        if (!moveId) continue;
        const atkType = getMoveType(gm, moveId);
        const eff = getTypeEffectiveness(atkType, oppTypes);
        if (eff > bestEff) bestEff = eff;
      }
    }

    if (bestEff >= 2) advantages++;
    else if (bestEff >= 0.5) neutral++;
  }

  // 换算 0~100：优势 = 1分，均势 = 0.5分
  const raw = (advantages + neutral * 0.5) / top50.length;
  const score = Math.round(raw * 100);

  return { score: Math.min(100, score), advantages, neutral, total: top50.length };
}

/**
 * ② 翻盘能力（10%）
 * 评估团队翻盘要素：
 * - 安全换存在（第二只有防御/耐久向属性）
 * - 高压充能招（大威力高能耗招式，如过热、近身战、疯狂伏特等）
 * - 后期收割（第三只有高速高攻属性特征）
 */
const HIGH_POWER_MOVES = new Set([
  'FOCUS_BLAST', 'CLOSE_COMBAT', 'SUPER_POWER', 'OVERHEAT',
  'WILD_CHARGE', 'FLARE_BLITZ', 'BRAVE_BIRD', 'HYDRO_PUMP',
  'SOLAR_BEAM', 'GUNK_SHOT', 'MEGAHORN', 'OUTRAGE',
  'FIRE_BLAST', 'BLIZZARD', 'THUNDER', 'HYPER_BEAM',
  'DRACO_METEOR', 'PRECIPICE_BLADES', 'ORIGIN_PULSE', 'ROAR_OF_TIME',
  'SPACIAL_REND', 'AEROBLAST', 'SACRED_FIRE', 'V_CREATE',
  'DOOM_DESIRE', 'EARTHQUAKE', 'STONE_EDGE',
  'FRENZY_PLANT', 'BLAST_BURN', 'HYDRO_CANNON',
]);

// 中高压招式（能造成可靠伤害但不是最顶级的）
const MID_POWER_MOVES = new Set([
  'BODY_SLAM', 'SHADOW_BALL', 'EARTH_POWER', 'ROCK_SLIDE',
  'ICE_BEAM', 'AVALANCHE', 'PSYCHIC', 'FOUL_PLAY',
  'CRUNCH', 'NIGHT_SLASH', 'PLAY_ROUGH', 'DAZZLING_GLEAM',
  'MOONBLAST', 'SLUDGE_BOMB', 'BUG_BUZZ', 'X_SCISSOR',
  'IRON_HEAD', 'FLASH_CANNON', 'ENERGY_BALL', 'LEAF_BLADE',
  'THUNDERBOLT', 'DISCHARGE', 'SCALD', 'AQUA_TAIL',
  'DARK_PULSE', 'DRAGON_CLAW', 'DRAIN_PUNCH', 'POWER_UP_PUNCH',
  'BREAKING_SWIPE', 'SCORCHING_SANDS', 'BONE_CLUB', 'DRILL_RUN',
]);

function calcComebackScore(team: TeamMemberInfo[], gm: any): number {
  let score = 0;

  // 安全换：第二只是否适合做安全换
  const slot2 = team[1];
  if (slot2) {
    // 防御向属性组合加分
    const hasDefensiveTypes = slot2.types.some(t =>
      ['steel', 'fairy', 'water', 'ghost', 'poison', 'rock'].includes(t)
    );
    // 双重属性提供更多抗性
    const hasDualTypes = slot2.types.length >= 2 && !slot2.types.includes('normal');
    
    if (hasDefensiveTypes && hasDualTypes) score += 40;
    else if (hasDefensiveTypes) score += 30;
    else if (hasDualTypes) score += 20;
    else score += 10; // 单属性也有基本切换价值
  }

  // 高压/中压充能招
  for (const member of team) {
    for (const cm of member.moves.charged) {
      if (HIGH_POWER_MOVES.has(cm)) {
        score += 30;
        break;
      }
    }
    // 再检查中压招
    for (const cm of member.moves.charged) {
      if (MID_POWER_MOVES.has(cm)) {
        score += 10;
        break;
      }
    }
  }
  // cap high power bonus
  score = Math.min(score, 50);

  // 后期收割（第三只）
  const slot3 = team[2];
  if (slot3) {
    const fast = slot3.moves.fast;
    if (fast) {
      const fastType = getMoveType(gm, fast);
      // 攻击型小招：格斗/龙/暗影/幽灵/飞行/超能/火/地面
      const aggressiveTypes = ['fighting', 'dragon', 'ghost', 'flying', 'psychic', 'fire', 'ground', 'rock', 'dark', 'steel'];
      if (aggressiveTypes.includes(fastType)) score += 25;
    }
    // 有收割倾向的属性
    if (slot3.types.some(t => ['fighting', 'ghost', 'dark', 'fairy', 'fire', 'rock'].includes(t))) score += 15;
  }

  return Math.min(100, score);
}

/**
 * ③ 稳定性（10%）
 * 共同弱点和抗性分散
 */
function calcStabilityScore(team: TeamMemberInfo[], gm: any): number {
  const allAttackTypes = Object.keys(TYPE_EFFECT);
  let weakCount = 0;
  let multipleWeak = 0;
  let tripleWeak = 0;

  // 弱点分析
  for (const atkType of allAttackTypes) {
    let weakMembers = 0;
    for (const member of team) {
      const eff = getTypeEffectiveness(atkType, member.types);
      if (eff >= 2) weakMembers++;
    }
    if (weakMembers >= 3) tripleWeak++;
    else if (weakMembers >= 2) multipleWeak++;
    if (weakMembers > 0) weakCount += weakMembers;
  }

  let score = 100;
  score -= tripleWeak * 20;    // 三只都怕同属性 — 严重
  score -= multipleWeak * 12;  // 两只都怕 — 明显漏洞
  score -= Math.min(20, (weakCount - multipleWeak * 2 - tripleWeak * 3) * 2); // 单个弱点轻微扣分

  // 抗性加分：队伍对攻击属性的整体抵抗能力
  let resistPoints = 0;
  for (const atkType of allAttackTypes) {
    let resistMembers = 0;
    for (const member of team) {
      const eff = getTypeEffectiveness(atkType, member.types);
      if (eff < 1 && eff > 0) resistMembers++;
      if (eff === 0) resistMembers += 2;
    }
    if (resistMembers >= 2) resistPoints += 8;
  }
  score += Math.min(24, Math.floor(resistPoints));

  return Math.max(0, Math.min(100, Math.round(score)));
}

/**
 * ④ 关键威胁
 * 找出 meta 前55名中克制队伍最多成员的宝可梦（top 5）
 */
function calcThreats(
  team: TeamMemberInfo[],
  rankings: PvPokePokemon[],
  gm: any,
): { speciesId: string; rank: number; threatScore: number }[] {
  const top55 = rankings.slice(0, 55);
  const threats: { speciesId: string; rank: number; threatScore: number; idx: number }[] = [];

  for (let i = 0; i < top55.length; i++) {
    const opp = top55[i];
    const oppTypes = getPokemonTypes(gm, opp.speciesId);
    let threatScore = 0;

    for (const member of team) {
      // opponent's moves vs our team
      const oppMoves = getRecommendedMoves(opp);
      const allOppMoves = [oppMoves.fast, ...oppMoves.charged];
      let bestEff = 0;
      for (const moveId of allOppMoves) {
        if (!moveId) continue;
        const atkType = getMoveType(gm, moveId);
        const eff = getTypeEffectiveness(atkType, member.types);
        if (eff > bestEff) bestEff = eff;
      }
      if (bestEff >= 2) threatScore += 2;
      else if (bestEff >= 0.5) threatScore += 1;
    }

    // 另外加上属性压制：opponent 的抵抗属性对队伍的压制
    for (const member of team) {
      const memberMoves = [member.moves.fast, ...member.moves.charged];
      let bestMemberEff = 0;
      for (const moveId of memberMoves) {
        if (!moveId) continue;
        const atkType = getMoveType(gm, moveId);
        const eff = getTypeEffectiveness(atkType, oppTypes);
        if (eff > bestMemberEff) bestMemberEff = eff;
      }
      if (bestMemberEff < 0.5) threatScore += 1; // 我方打不动他
    }

    threats.push({ speciesId: opp.speciesId, rank: i + 1, threatScore, idx: i });
  }

  threats.sort((a, b) => b.threatScore - a.threatScore || a.rank - b.rank);
  return threats.slice(0, 5).map(t => ({ speciesId: t.speciesId, rank: t.rank, threatScore: t.threatScore }));
}

// ===== 主函数 =====

interface TeamSlot {
  speciesId: string;
  name: string;
  rank: number;
  fastMove: string;
  chargedMoves: string[];
  role: string;
  owned: boolean;
}

export async function buildTeam(leagueKey: string, coreInput?: string): Promise<string> {
  const leagueLabel = LEAGUE_LABELS[leagueKey] || leagueKey;

  // 加载 rankings
  const rankings = await getRankings(leagueKey);
  if (!rankings || rankings.length === 0) {
    return `无法加载 ${leagueLabel} 数据，暂无本地缓存。请稍后重试。`;
  }

  // 加载 gamemaster
  const gm = await loadGamemaster();
  if (!gm) {
    return `无法加载 gamemaster 数据，请稍后重试。`;
  }

  interface Pick {
    entry: PvPokePokemon;
    rank: number;
    owned: boolean;
  }

  const selected: Pick[] = [];

  if (coreInput) {
    const coreEntry = findEntryInRankings(rankings, coreInput);
    if (!coreEntry) {
      return `在 ${leagueLabel} 中未找到 ${coreInput}，请确认名字是否正确。`;
    }

    selected.push({ entry: coreEntry.entry, rank: coreEntry.rank, owned: hasMyPokemon(coreEntry.entry.speciesId, leagueKey) });

    const myPicks = pickFromRankings(rankings, getMySpeciesForLeague(leagueKey))
      .filter(p => p.entry.speciesId !== coreEntry.entry.speciesId)
      .slice(0, 2);

    for (const pick of myPicks) {
      selected.push({ entry: pick.entry, rank: pick.rank, owned: true });
    }

    if (selected.length < 3) {
      for (const entry of rankings) {
        if (selected.length >= 3) break;
        if (selected.some(s => s.entry.speciesId === entry.speciesId)) continue;
        selected.push({ entry, rank: selected.length + 1, owned: false });
      }
    }
  } else {
    const myPicks = pickFromRankings(rankings, getMySpeciesForLeague(leagueKey)).slice(0, 3);

    for (const pick of myPicks) {
      selected.push({ entry: pick.entry, rank: pick.rank, owned: true });
    }

    if (selected.length < 3) {
      for (const entry of rankings) {
        if (selected.length >= 3) break;
        if (selected.some(s => s.entry.speciesId === entry.speciesId)) continue;
        selected.push({ entry, rank: selected.length + 1, owned: false });
      }
    }
  }

  const final = selected.slice(0, 3);
  const roles = ['核心', '安全换', '收割'];

  // 构建 team info 用于评分
  const teamInfo: TeamMemberInfo[] = final.map(slot => {
    const moves = getRecommendedMoves(slot.entry);
    return {
      speciesId: slot.entry.speciesId,
      types: getPokemonTypes(gm, slot.entry.speciesId),
      moves,
    };
  });

  // ===== 评分 =====
  const metaScore = calcMetaCoverage(teamInfo, rankings, gm);
  const comebackScore = calcComebackScore(teamInfo, gm);
  const stabilityScore = calcStabilityScore(teamInfo, gm);

  const finalScore = Math.round(
    metaScore.score * 0.60 + comebackScore * 0.20 + stabilityScore * 0.20
  );

  // 评级
  let rating = '';
  if (finalScore >= 90) rating = '顶级';
  else if (finalScore >= 80) rating = '强力';
  else if (finalScore >= 70) rating = '良好';
  else if (finalScore >= 60) rating = '一般';
  else rating = '较弱';

  // ===== 关键威胁 =====
  const threats = calcThreats(teamInfo, rankings, gm);

  // ===== 输出 =====
  const lines: string[] = [];
  const neededSpecies: string[] = [];
  const ownedSpecies: string[] = [];

  // 标题
  lines.push(`📦 ${leagueLabel} 配队推荐`);
  lines.push('');

  // 每只宝可梦
  for (let i = 0; i < final.length; i++) {
    const slot = final[i];
    const role = roles[i] || `角色${i + 1}`;
    const moves = getRecommendedMoves(slot.entry);
    const name = getSpeciesCn(slot.entry.speciesId);

    lines.push(`${role}：${name}（PvPokeTW #${slot.rank}）`);
    lines.push(formatMoves(slot.entry.speciesId, moves.fast, moves.charged));
    lines.push('');

    if (slot.owned) {
      ownedSpecies.push(name);
    } else {
      neededSpecies.push(name);
    }
  }

  // 评分
  lines.push(`队伍评分：${finalScore} /100`);
  lines.push(`评级：${rating}`);
  lines.push('');
  lines.push('评分构成：');
  lines.push(`环境覆盖：${metaScore.score}（权重60%）`);
  lines.push(`战术弹性：${comebackScore}（权重20%）`);
  lines.push(`队伍容错：${stabilityScore}（权重20%）`);

  // 关键威胁
  lines.push('');
  lines.push('关键威胁：');
  for (const threat of threats) {
    const name = getSpeciesCn(threat.speciesId);
    lines.push(`#${threat.rank} ${name}`);
  }

  // 已有/缺少
  lines.push('');
  const ownedStr = ownedSpecies.length > 0
    ? ownedSpecies.map(n => `✅ ${n}`).join('、')
    : '无';

  const neededStr = neededSpecies.length > 0
    ? neededSpecies.map(n => `❌ ${n}`).join('、')
    : '无';

  lines.push(`我已有：${ownedStr}`);
  lines.push(`我缺少：${neededStr}`);

  if (neededSpecies.length > 0) {
    lines.push(`下一步培养：${neededSpecies[0]}`);
  }

  return lines.join('\n');
}

// ===== 命令行测试入口 =====
if (require.main === module) {
  (async () => {
    const args = process.argv.slice(2);

    if (args.length >= 1 && args[0] === '--test') {
      const testCases: [string, string?][] = [
        ['1500'],
        ['1500', '胖嘟嘟'],
        ['master', '固拉多'],
      ];

      for (const [league, core] of testCases) {
        console.log(`\n>>> /pvp 配队 ${league}${core ? ' ' + core : ''}`);
        console.log('---');
        const result = await buildTeam(league, core);
        console.log(result);
        console.log('---');
      }
    } else if (args.length >= 1) {
      const leagueKey = resolveLeague(args[0]);
      if (!leagueKey) {
        console.log(`未知联盟: ${args[0]}，支持 1500 / 2500 / master`);
        process.exit(1);
      }
      const coreInput = args.length >= 2 ? args.slice(1).join(' ') : undefined;
      const result = await buildTeam(leagueKey, coreInput);
      console.log(result);
    } else {
      console.log('用法: node dist/team.js <联盟> [核心宝可梦]');
      console.log('       node dist/team.js --test');
    }
  })();
}
