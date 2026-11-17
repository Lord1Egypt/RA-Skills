#!/usr/bin/env node
// analysis.mjs — 分类分析引擎：户型/价格/流动性/日照采光/噪音/真实性 六类结论 + 观点提炼
// 纯函数、零依赖（Node ≥18）。AI 负责采集证据，判定与观点结构由本模块产出。
// 设计：findings 按 severity 分级（good/ok/warn/bad），distillViewpoint 从全部 findings
//      提炼「事实 / 代价 / 结论」三句话——数字优先，与地图详情卡三句话卡同构。
// 输入：record = house-ops.scan/1 扫描记录（schema SoT：modes/scan.md）
//       evidence = 实采证据（小区均价/户型房间明细/噪音源/政府公示等，由 AI 采集）
//       profile = { population } 画像数字（人口驱动卫生间/面积类结论）

import { verifyAuthenticity, finalizeRecord } from '../scrapers/_fields.mjs';
import { solarElevation } from './insight.mjs';

const SEV_ORDER = { bad: 0, warn: 1, ok: 2, good: 3 };
const f = (v) => Number.isFinite(v);

function finding(level, title, detail) {
  return { level, title, detail };
}

// ---------- 户型布局（012 案例固化：伪三房/单卫/刀把形判别） ----------
export function analyzeLayout(record, evidence = {}, profile = {}) {
  const out = [];
  const pop = profile.population ?? 4;
  const rooms = evidence.layout_rooms ?? [];          // [{name:'卧室A', area:13.5}, ...]
  const beds = rooms.filter((r) => /卧室/.test(r.name));
  const baths = evidence.bathrooms ?? (rooms.filter((r) => /卫/.test(r.name)).length || null);
  const halls = rooms.filter((r) => /客厅/.test(r.name));
  const L = record.listing ?? {};

  if (beds.length) {
    const minBed = Math.min(...beds.map((b) => b.area)).toFixed(1);
    if (Number(minBed) < 7) {
      out.push(finding('bad', '伪多房：最小卧室不达标', `最小卧室仅 ${minBed}㎡（放 1.2m 床后无活动空间）——实际为 ${beds.length - 0.5} 房，非真 ${beds.length} 房`));
    } else if (Number(minBed) < 9) {
      out.push(finding('warn', '最小卧室偏紧凑', `最小卧室 ${minBed}㎡，学龄儿童长期居住局促`));
    } else {
      out.push(finding('good', '卧室尺度合格', `最小卧室 ${minBed}㎡，可正常布局`));
    }
  }
  if (baths != null) {
    if (baths >= 2 && pop >= 3) out.push(finding('good', '双卫及以上', `${baths} 个卫生间，${pop} 口之家晨间无冲突`));
    else if (baths === 1 && pop >= 3) out.push(finding('warn', '全屋单卫', `${pop} 口之家共用 1 个卫生间（${(rooms.find((r) => /卫/.test(r.name))?.area ?? '?')}㎡）——晨间冲突是每日现实`));
  }
  if (evidence.layout_shape && /刀把|异形|手枪/.test(evidence.layout_shape)) {
    out.push(finding('warn', '户型形状不规则', `${evidence.layout_shape}——家具摆放受限，拐角空间利用率打折`));
  }
  if (halls.length && pop >= 3) {
    const hall = halls[0].area;
    if (hall >= 25) out.push(finding('good', '客厅宽敞', `客厅 ${hall}㎡`));
    else if (hall < 18) out.push(finding('warn', '客厅偏小', `客厅 ${hall}㎡，${pop} 口之家活动空间集中于此`));
  }
  // 人均居住面积（套内口径优先，缺省用建面×0.8 估）
  const area = L.area_sqm;
  if (f(area) && pop) {
    const per = Math.round(((area * 0.8) / pop) * 10) / 10;
    if (per < 18) out.push(finding('warn', '人均居住面积偏低', `人均约 ${per}㎡（${area}㎡ ÷ ${pop} 人）`));
    else if (per >= 25) out.push(finding('good', '人均居住面积宽裕', `人均约 ${per}㎡`));
  }
  if (!out.length) out.push(finding('ok', '户型数据不足', '提供户型房间明细（evidence.layout_rooms）后可出布局结论'));
  return out;
}

// ---------- 流动性（带看/成交/挂牌时长 → 房东策略与议价空间） ----------
export function analyzeLiquidity(record, evidence = {}) {
  const out = [];
  const L = record.listing ?? {};
  const viewings = L.viewings_30d;
  const txs = record.transactions ?? [];
  const pricedDeals = txs.filter((t) => t.total_price_wan != null).length;
  // 有"无价成交记录"（脱敏）≠ 没有成交——不能当作 0 套参与判定
  const dealsKnown = evidence.deals_90d != null || pricedDeals > 0 || txs.some((t) => f(t.total_price_wan));
  const unpricedDeals = txs.filter((t) => !f(t.total_price_wan)).length;
  const deals90 = evidence.deals_90d ?? pricedDeals;
  const days = L.listed_at ? Math.max(0, Math.round((Date.now() - new Date(L.listed_at)) / 86400000)) : null;
  if (!dealsKnown) {
    // 成交价脱敏/缺失：绝不当作 0 套成交参与判定
    const v = f(viewings) ? `30 天带看 ${viewings} 次` : '';
    const u = unpricedDeals > 0 ? `近 90 天 ${unpricedDeals} 套成交（价格脱敏）` : '暂无成交明细';
    out.push(finding('warn', '高关注·真实成交待核', `${v}${v && unpricedDeals ? '，' : ''}${u}——议价前先通过产调/政务渠道核实真实成交`));
  } else if (f(viewings) && f(deals90)) {
    if (viewings >= 100 && deals90 <= 2) out.push(finding('warn', '有价无市', `30 天带看 ${viewings} 次 vs 90 天成交 ${deals90} 套——关注度高但转化低，要价高于市场出清价，议价空间大`));
    else if (viewings >= 100 && deals90 >= 5) out.push(finding('good', '热销盘', `带看 ${viewings} 次/90 天成交 ${deals90} 套——定价贴合市场，好房不等人`));
    else if (viewings < 30) out.push(finding('warn', '关注冷淡', `30 天带看仅 ${viewings} 次——板块或本套缺乏吸引力`));
    else out.push(finding('ok', '流动性正常', `30 天带看 ${viewings} 次 / 90 天成交 ${deals90} 套`));
  }
  if (dealsKnown && deals90 === 0) out.push(finding('good', '近 90 天零成交（真实口径）', '可作为压价依据'));
  if (f(days) && days >= 120) out.push(finding('warn', `挂牌 ${days} 天未去化`, `长挂牌=议价筹码（房东或已多轮调价，查调价记录）`));
  if (!out.length) out.push(finding('ok', '流动性数据不足', '采集带看/成交数据后可出流动性结论'));
  return out;
}

// ---------- 日照采光（太阳几何 + 楼间距输入，[推算] 档） ----------
export function analyzeSunlight(record, evidence = {}, profile = {}) {
  const out = [];
  const lat = evidence.lat ?? 31.23;
  const spacing = evidence.sun_spacing;           // 楼间距 m（卫星测距/OSM）
  const southFloors = evidence.south_floors;      // 南侧遮挡楼栋层数
  const floorMatch = String(record.listing?.floor ?? '').match(/(低|中|高)楼层|(\d+)F/);
  const myFloorNum = (() => {
    const m = String(record.listing?.floor ?? '').match(/共(\d+)层/);
    const low = /低楼层/.test(record.listing?.floor ?? '');
    const high = /高楼层/.test(record.listing?.floor ?? '');
    const mid = /中楼层/.test(record.listing?.floor ?? '');
    if (!(m)) return null;
    const total = Number(m[1]);
    if (low) return Math.max(1, Math.round(total * 0.2));
    if (mid) return Math.round(total * 0.5);
    if (high) return Math.round(total * 0.8);
    return null;
  })();
  if (f(spacing) && f(southFloors) && f(myFloorNum)) {
    const dahan = solarElevation(lat, '2027-01-20', 12);
    const Hs = southFloors * 3;
    const shadeTopAtNoon = Hs - spacing * Math.tan(dahan * D2R);
    const sill = (myFloorNum - 1) * 3 + 0.9;
    if (shadeTopAtNoon > sill) out.push(finding('bad', '大寒日正午被南侧楼栋遮挡', `遮挡线 ${shadeTopAtNoon.toFixed(1)}m > 本套窗台 ${sill.toFixed(1)}m——日照可能低于 GB 50180 大寒日 2h 法定标准`));
    else out.push(finding('good', '大寒日正午日照无遮挡', `遮挡线 ${shadeTopAtNoon.toFixed(1)}m ≤ 窗台 ${sill.toFixed(1)}m`));
  }
  if (!out.length) out.push(finding('ok', '日照输入不足', '补齐楼间距与南侧楼层数（evidence.sun_spacing / south_floors）后可出日照结论'));
  return out;
}

// ---------- 噪音（evidence.noise_rows：insight noise 的输出行） ----------
export function analyzeNoise(record, evidence = {}) {
  const out = [];
  const rows = evidence.noise_rows ?? [];
  if (rows.length) {
    const worst = rows.reduce((a, b) => (b.db > a.db ? b : a), rows[0]);
    const gb = worst.db <= 60 ? ['pass', '2 类区限值 60dB'] : worst.db <= 70 ? ['warn', '介于 2-4a 类之间'] : ['bad', '超 4a 类限值 70dB'];
    out.push(finding(gb[0] === 'pass' ? 'good' : gb[0], `主导噪音源 ${worst.db}dB（${gb[1]}）`, `${worst.kind ?? '噪音源'}「${worst.name ?? ''}」距离 ${worst.dist}m`));
    if (record.listing?.orientation && /航线|机场/.test(evidence.airport_note ?? '')) out.push(finding('bad', '机场航线覆盖', evidence.airport_note));
  } else {
    out.push(finding('ok', '噪音数据未采集', '运行 insight noise（坐标）后填入 evidence.noise_rows'));
  }
  return out;
}

// ---------- 价格（复用 finalizeRecord/crosscheck 判定） ----------
export function analyzePrice(record, evidence = {}) {
  const out = [];
  const rec = structuredClone(record);
  rec.transactions = rec.transactions ?? [];
  const L = rec.listing ?? {};
  const avg = evidence.community_avg_unit_price;
  if (f(L.unit_price) && f(avg) && avg > 0) {
    const pct = Math.round(((L.unit_price - avg) / avg) * 1000) / 10;
    if (pct <= -15) out.push(finding('bad', `挂牌低于小区均价 ${Math.abs(pct)}%`, '先查结构性原因（混居折价/户型缺陷/急售），确认前不视为捡漏'));
    else if (pct <= -5) out.push(finding('good', `挂牌低于小区均价 ${Math.abs(pct)}%`, '有议价与价值空间'));
    else if (pct <= 5) out.push(finding('ok', `挂牌贴近小区均价（+${pct}%）`));
    else if (pct <= 15) out.push(finding('warn', `挂牌高于小区均价 ${pct}%`, '议价以均价为锚'));
    else out.push(finding('bad', `挂牌高于小区均价 ${pct}%`, '明显虚高，需核实'));
  }
  return out;
}

// ---------- 真实性（包装 verifyAuthenticity 判定表） ----------
export function analyzeAuthenticity(record, evidence = {}) {
  const v = verifyAuthenticity(record, evidence);
  return v.checks
    .filter((c) => c.status !== 'unknown')
    .map((c) => finding(c.status === 'pass' ? 'good' : c.status === 'warn' ? 'warn' : 'bad', c.name, c.detail));
}

// ---------- 观点提炼（三句话：事实 / 代价 / 结论） ----------
export function distillViewpoint(record, findings, profile = {}) {
  const L = record.listing ?? {};
  const days = L.listed_at ? Math.max(0, Math.round((Date.now() - new Date(L.listed_at)) / 86400000)) : null;
  const factBits = [];
  if (record.community) factBits.push(record.community);
  if (f(L.total_price_wan)) factBits.push(`挂牌 ${L.total_price_wan} 万`);
  if (f(L.unit_price)) factBits.push(`${L.unit_price.toLocaleString()} 元/㎡`);
  if (f(L.area_sqm)) factBits.push(`${L.area_sqm}㎡ ${L.layout ?? ''}`);
  if (days != null) factBits.push(`已挂牌 ${days} 天`);
  if (f(L.viewings_30d)) factBits.push(`30 天带看 ${L.viewings_30d} 次`);
  const fact = factBits.join(' · ') || '--';

  const bads = findings.filter((x) => x.level === 'bad').map((x) => x.title + (x.detail ? `（${x.detail.slice(0, 40)}）` : ''));
  const warns = findings.filter((x) => x.level === 'warn').map((x) => x.title);
  const costBits = [];
  if (bads.length) costBits.push(...bads.slice(0, 2));
  if (warns.length) costBits.push(...warns.slice(0, 2));
  const cost = costBits.length ? costBits.join('；') : '无已知代价';

  const verdictBits = [];
  if (findings.some((x) => x.level === 'bad')) verdictBits.push('存在硬伤项，优先排除或验证');
  if (record.listing?.ownership && /满五/.test(record.listing.ownership)) verdictBits.push('满五税费优');
  verdictBits.push(record.watchlist_note || record.next_action || '建议先补齐待核实项');
  const verdict = verdictBits.join('；');

  return { fact, cost: cost || '无', verdict };
}

// ---------- 总入口：分类聚合 ----------
export function analyze(record, { evidence = {}, profile = {} } = {}) {
  const { record: rec } = finalizeRecord(structuredClone(record ?? {}));
  const findings = {
    户型: analyzeLayout(rec, evidence, profile),
    流动性: analyzeLiquidity(rec, evidence),
    日照采光: analyzeSunlight(rec, evidence, profile),
    噪音: analyzeNoise(rec, evidence),
    价格: analyzePrice(rec, evidence),
    真实性: analyzeAuthenticity(rec, evidence),
  };
  const all = Object.entries(findings).flatMap(([type, list]) => list.map((x) => ({ type, ...x })));
  all.sort((a, b) => SEV_ORDER[a.level] - SEV_ORDER[b.level]);
  return { findings, all, viewpoint: distillViewpoint(rec, all, profile), record: rec };
}
