// fetcher.ts — PvPoke 数据拉取、gamemaster 加载、IV 计算

import * as fs from 'fs';
import * as path from 'path';
import { PvPokePokemon, LeagueInfo, PokemonBase, IVRecord, IVResult } from './types';

export const LEAGUES: Record<string, LeagueInfo> = {
  '1500': { key: 1500, label: '超级联盟', cpLimit: 1500, fileName: 'rankings-1500.json' },
  '2500': { key: 2500, label: '高级联盟', cpLimit: 2500, fileName: 'rankings-2500.json' },
  master: { key: 'master', label: '大师联盟', cpLimit: 10000, fileName: 'rankings-master.json' },
};

const CACHE_DIR = path.resolve(__dirname, '..', 'cache');
const CACHE_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 天

const PVPOKE_RAW_BASE = 'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall';
const PVPOKE_GM_URL = 'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster.json';

// CP 乘数表 (Level 1~51, 半级步进, 索引 0=Lv1)
// 来源: PvPoke GitHub src/js/pokemon/Pokemon.js (2026-05-15)
const CP_M = [
  0.0939999967813491, 0.135137430784308, 0.166397869586944, 0.192650914456886,
  0.215732470154762, 0.236572655026622, 0.255720049142837, 0.273530381100769,
  0.290249884128570, 0.306057381335773, 0.321087598800659, 0.335445032295077,
  0.349212676286697, 0.362457748778790, 0.375235587358474, 0.387592411085168,
  0.399567276239395, 0.411193549517250, 0.422500014305114, 0.432926413410414,
  0.443107545375824, 0.453059953871985, 0.462798386812210, 0.472336077786704,
  0.481684952974319, 0.490855810259008, 0.499858438968658, 0.508701756943992,
  0.517393946647644, 0.525942508771329, 0.534354329109191, 0.542635762230353,
  0.550792694091796, 0.558830599438087, 0.566754519939422, 0.574569148039264,
  0.582278907299041, 0.589887911977272, 0.597400009632110, 0.604823657502073,
  0.612157285213470, 0.619404110566050, 0.626567125320434, 0.633649181622743,
  0.640652954578399, 0.647580963301656, 0.654435634613037, 0.661219263506722,
  0.667934000492096, 0.674581899290818, 0.681164920330047, 0.687684905887771,
  0.694143652915954, 0.700542893277978, 0.706884205341339, 0.713169102333341,
  0.719399094581604, 0.725575616972598, 0.731700003147125, 0.734741011137376,
  0.737769484519958, 0.740785574597326, 0.743789434432983, 0.746781208702482,
  0.749761044979095, 0.752729105305821, 0.755685508251190, 0.758630366519684,
  0.761563837528228, 0.764486065255226, 0.767397165298461, 0.770297273971590,
  0.773186504840850, 0.776064945942412, 0.778932750225067, 0.781790064808426,
  0.784636974334716, 0.787473583646825, 0.790300011634826, 0.792803950958807,
  0.795300006866455, 0.797803921486970, 0.800300002098083, 0.802803892322847,
  0.805299997329711, 0.807803863460723, 0.810299992561340, 0.812803834895026,
  0.815299987792968, 0.817803806620319, 0.820299983024597, 0.822803778631297,
  0.825299978256225, 0.827803750922782, 0.830299973487854, 0.832803753381377,
  0.835300028324127, 0.837803755931569, 0.840300023555755, 0.842803729034748,
  0.845300018787384, 0.847803702398935, 0.850300014019012, 0.852803676019539,
  0.855300009250640, 0.857803649892077, 0.860300004482269, 0.862803624012168,
  0.865299999713897,
];

function cpMultiplier(level: number): number {
  const idx = Math.floor((level - 1.0) * 2);
  return CP_M[Math.max(0, Math.min(idx, CP_M.length - 1))];
}

// CP 公式：完全对齐 PvPoke 官方实现
// 注意：不要在 CP 计算中对 HP stat 做 floor 操作
// PvPoke calculateCP: floor( (atk+ivA) * sqrt(def+ivD) * sqrt(hp+ivH) * cpm^2 / 10 )
function calcCP(baseAtk: number, baseDef: number, baseSta: number,
                ivAtk: number, ivDef: number, ivSta: number,
                level: number): number {
  const m = cpMultiplier(level);
  // PvPoke 不对 hp stat 做 floor——直接使用原始基础值
  return Math.floor(
    (baseAtk + ivAtk) * Math.pow(baseDef + ivDef, 0.5) * Math.pow(baseSta + ivSta, 0.5) * Math.pow(m, 2) / 10
  );
}



/** 计算最佳 IV 及前 50 名（按 PvPoke 排序：SP 降序，同 SP 时 CP 降序） */
export function computeBestIV(base: PokemonBase, cpLimit: number, levelCap = 51.0): IVResult {
  interface InternalEntry {
    iv: [number, number, number];
    cp: number;
    level: number;
    product: number;
  }
  const entries: InternalEntry[] = [];

  for (let a = 0; a <= 15; a++) {
    for (let d = 0; d <= 15; d++) {
      for (let s = 0; s <= 15; s++) {
        let maxLevel = 1.0;
        const maxSteps = Math.floor((levelCap - 1.0) * 2);
        for (let step = 0; step <= maxSteps; step++) {
          const level = 1.0 + step * 0.5;
          const cp = calcCP(base.atk, base.def, base.sta, a, d, s, level);
          if (cp <= cpLimit) {
            maxLevel = level;
          } else {
            break;
          }
        }

        if (maxLevel < 1.5) continue;

        const cp = calcCP(base.atk, base.def, base.sta, a, d, s, maxLevel);
        const m = cpMultiplier(maxLevel);
        // HP 取整：Math.floor((sta + iv) * CPM) — 与 PvPoke 完全一致
        const hp = Math.floor((base.sta + s) * m);
        const atk = (base.atk + a) * m;
        const def = (base.def + d) * m;
        const product = atk * def * hp;

        entries.push({ iv: [a, d, s], cp, level: maxLevel, product });
      }
    }
  }

  // 排序策略：对齐 PvPokeTW 网站结果
  // 主键：stat product（atk * def * hp），同 product 组内按实战倾向排序
  entries.sort((a, b) => {
    // 1) stat product 降序（主要排序依据）
    if (b.product !== a.product) return b.product - a.product;
    // 2) ATK IV 越小越优先（实战低攻高防高血倾向）
    if (a.iv[0] !== b.iv[0]) return a.iv[0] - b.iv[0];
    // 3) DEF IV 越大越优先
    if (b.iv[1] !== a.iv[1]) return b.iv[1] - a.iv[1];
    // 4) STA IV 越大越优先
    if (b.iv[2] !== a.iv[2]) return b.iv[2] - a.iv[2];
    // 5) CP 越接近上限越优先
    return b.cp - a.cp;
  });

  const top50: IVRecord[] = [];
  for (let i = 0; i < entries.length; i++) {
    const e = entries[i];
    const record: IVRecord = { iv: e.iv, cp: e.cp, level: e.level, rank: i + 1 };
    if (i < 50) top50.push(record);
  }

  return {
    best: entries.length > 0 ? top50[0] : null!,
    top50,
    total: entries.length,
  };
}

/** 解析用户 IV 字符串（如 "1/15/10"） */
export function parseUserIV(input: string): [number, number, number] | null {
  const parts = input.trim().split('/');
  if (parts.length !== 3) return null;
  const a = parseInt(parts[0], 10);
  const d = parseInt(parts[1], 10);
  const s = parseInt(parts[2], 10);
  if (isNaN(a) || isNaN(d) || isNaN(s)) return null;
  if (a < 0 || a > 15 || d < 0 || d > 15 || s < 0 || s > 15) return null;
  return [a, d, s];
}

/** 查找用户 IV 在排名表中的位置 */
export function findUserIVInResults(userIV: [number, number, number], ivResult: IVResult): {
  record: IVRecord | null;
  inTop50: boolean;
} {
  for (const r of ivResult.top50) {
    if (r.iv[0] === userIV[0] && r.iv[1] === userIV[1] && r.iv[2] === userIV[2]) {
      return { record: r, inTop50: true };
    }
  }
  return { record: null, inTop50: false };
}

/** 计算用户 IV 对应的 CP / 等级（不输出 product） */
export function computeUserIV(base: PokemonBase, userIV: [number, number, number],
                               cpLimit: number, levelCap = 51.0): IVRecord {
  const maxSteps = Math.floor((levelCap - 1.0) * 2);
  let maxLevel = 1.0;
  for (let step = 0; step <= maxSteps; step++) {
    const level = 1.0 + step * 0.5;
    const cp = calcCP(base.atk, base.def, base.sta, userIV[0], userIV[1], userIV[2], level);
    if (cp <= cpLimit) {
      maxLevel = level;
    } else break;
  }
  const cp = calcCP(base.atk, base.def, base.sta, userIV[0], userIV[1], userIV[2], maxLevel);
  return { iv: userIV, cp, level: maxLevel, rank: 9999 };
}

/** 计算 IV 差值（最佳 IV vs 用户 IV） */
export function computeIVDiff(bestIV: [number, number, number],
                              userIV: [number, number, number]):
  { atk: number; def: number; hp: number } {
  return {
    atk: bestIV[0] - userIV[0],
    def: bestIV[1] - userIV[1],
    hp: bestIV[2] - userIV[2],
  };
}

// ===== Gamemaster 加载 =====

let _gmCache: { data: any; fetchedAt: number } | null = null;

/** 从缓存或网络加载 gamemaster.json */
export async function loadGamemaster(): Promise<any> {
  const cachePath = path.join(CACHE_DIR, 'gamemaster.json');
  const ageOk = (age: number) => age < CACHE_TTL_MS * 2;

  if (_gmCache && ageOk(Date.now() - _gmCache.fetchedAt)) {
    return _gmCache.data;
  }

  if (fs.existsSync(cachePath)) {
    const stat = fs.statSync(cachePath);
    if (ageOk(Date.now() - stat.mtimeMs)) {
      const data = JSON.parse(fs.readFileSync(cachePath, 'utf-8'));
      _gmCache = { data, fetchedAt: Date.now() };
      return data;
    }
  }

  try {
    const resp = await fetch(PVPOKE_GM_URL, { headers: { 'User-Agent': 'OpenClaw-PvPoke/1.1' } });
    if (!resp.ok) return null;
    const data = await resp.json();
    if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
    fs.writeFileSync(cachePath, JSON.stringify(data), 'utf-8');
    _gmCache = { data, fetchedAt: Date.now() };
    return data;
  } catch {
    return null;
  }
}

/** 从 gamemaster 中查询宝可梦基础数据 */
export function getPokemonBase(gm: any, speciesId: string): PokemonBase | null {
  if (!gm || !gm.pokemon) return null;
  const list = gm.pokemon as any[];
  const lower = speciesId.toLowerCase();
  for (const p of list) {
    if (p.speciesId?.toLowerCase() === lower) {
      return {
        speciesId: p.speciesId,
        speciesName: p.speciesName || '',
        atk: p.baseStats.atk,
        def: p.baseStats.def,
        sta: p.baseStats.hp,
        types: p.types || [],
      };
    }
  }
  return null;
}

// ===== Rankings 缓存 =====

/** 自动选择联盟 key */
export function resolveLeague(input: string): string | null {
  const map: Record<string, string> = {
    '1500': '1500', '超级': '1500', '超级联盟': '1500',
    '2500': '2500', '高级': '2500', '高级联盟': '2500',
    'master': 'master', '大师': 'master', '大师联盟': 'master', '无限制': 'master',
  };
  return map[input.trim()] || null;
}

/** 加载缓存数据 */
export function loadCache(leagueKey: string): PvPokePokemon[] | null {
  const info = LEAGUES[leagueKey];
  if (!info) return null;
  const filePath = path.join(CACHE_DIR, info.fileName);
  if (!fs.existsSync(filePath)) return null;
  const stat = fs.statSync(filePath);
  const age = Date.now() - stat.mtimeMs;
  if (age > CACHE_TTL_MS * 2) return null;
  const raw = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(raw) as PvPokePokemon[];
}

/** 从网络拉取并保存 */
export async function fetchRankings(leagueKey: string): Promise<PvPokePokemon[] | null> {
  const info = LEAGUES[leagueKey];
  if (!info) return null;
  const urlMap: Record<string, string> = {
    '1500': `${PVPOKE_RAW_BASE}/rankings-1500.json`,
    '2500': `${PVPOKE_RAW_BASE}/rankings-2500.json`,
    master: `${PVPOKE_RAW_BASE}/rankings-10000.json`,
  };
  const url = urlMap[leagueKey];
  if (!url) return null;

  try {
    const resp = await fetch(url, { headers: { 'User-Agent': 'OpenClaw-PvPoke/1.0' } });
    if (!resp.ok) return null;
    const data = (await resp.json()) as PvPokePokemon[];
    if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
    const filePath = path.join(CACHE_DIR, info.fileName);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
    return data;
  } catch {
    return null;
  }
}

/** 获取数据（先缓存、再网络） */
export async function getRankings(leagueKey: string): Promise<PvPokePokemon[] | null> {
  const cached = loadCache(leagueKey);
  if (cached) return cached;
  return await fetchRankings(leagueKey);
}
