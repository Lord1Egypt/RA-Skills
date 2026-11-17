#!/usr/bin/env node
// selftest.mjs — scan 层 golden fixture 自测（零依赖）。
// 测试面 = 纯函数 interface：finalizeRecord（归一化+定价交叉验证）与平台 detect()/liftMobileCity。
// 用法: node scripts/selftest.mjs    # 全部通过 exit 0；任何断言失败 exit 1
// 纪律：新增行为先在这里加 golden 用例；穿过 CLI stdout / TUI 的测试不属于测试面。

import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { readFile, stat, lstat, realpath } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import {
  finalizeRecord, SCAN_SCHEMA, PAGE_TYPES, RELIABILITY, VERDICT_THRESHOLDS,
  SCAN_STATUS, SCAN_BUDGET, SOURCE_GRANULARITIES,
  buildPriceHistory, historyKey, listingFingerprint, matchRecord, buildEntityHistory,
  verifyAuthenticity,
} from '../scrapers/_fields.mjs';
import { groupDetections, overBudgetWarning } from './lib/detect.mjs';
import { checkGranularity, readOfficialSources, filterSources } from './lib/official-sources.mjs';
import { authenticityFromNote, effectiveProvenance } from './lib/data.mjs';
import { decide, isUserExcluded, riskLabel, conclusionLabel } from './lib/decision.mjs';
import { parseProfile, updateProfileFields, PROFILE_FIELDS } from './lib/profile.mjs';
import { renderMapHtml } from './lib/map-html.mjs';
import { analyze } from './analysis.mjs';
import { solarElevation, noiseLevelAt } from './insight.mjs';
import { buildEvidenceName, evidenceDirFor, evidenceEntry, EVIDENCE_TYPES } from './evidence.mjs';
import { loadScrapers, detectPlatform, liftMobileCity } from '../scrapers/_registry.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
let failed = 0;
const eq = (name, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) { failed++; console.error(`⛔ ${name}\n   got:  ${JSON.stringify(got)}\n   want: ${JSON.stringify(want)}`); }
  else console.log(`✅ ${name}`);
};
const has = (name, cond) => { if (!cond) { failed++; console.error(`⛔ ${name}`); } else console.log(`✅ ${name}`); };

// ---------- finalizeRecord：定价交叉验证 golden 用例 ----------

// 1) 多样本：单价中位数锚（issue #2 的核心修正）
{
  const { record } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'lianjia',
    listing: { total_price_wan: 510, area_sqm: 100 },
    transactions: [
      { community: 'X', total_price_wan: 520, area_sqm: 100, deal_date: '2026-08-01', reliability: '成交数据' },
      { community: 'X', total_price_wan: 500, area_sqm: 100, deal_date: '2026-07-01', reliability: '成交数据' },
    ],
  });
  eq('样本单价推导（总价/面积）', [record.transactions[0].unit_price, record.transactions[1].unit_price], [52000, 50000]);
  eq('锚点=单价中位数 51000，双样本', record.crosscheck.anchor, { tier: '成交数据', n_samples: 2, range_pct: 3.9 });
  eq('挂牌单价 51000 vs 锚点 51000 → near_deal', [record.crosscheck.verdict, record.crosscheck.listing_vs_anchor_pct], ['near_deal', 0]);
}

// 2) 单样本 → 置信度显式标注
{
  const { record } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'fang',
    listing: { total_price_wan: 599, unit_price: 58691, area_sqm: 102.06 },
    transactions: [{ community: 'X', total_price_wan: 582, unit_price: 57235, deal_date: '2026-06-20', reliability: '成交数据' }],
  });
  eq('单样本 n_samples=1', record.crosscheck.anchor.n_samples, 1);
  eq('单样本 range_pct=null', record.crosscheck.anchor.range_pct, null);
  has('单样本降置信度注记', /单样本/.test(record.crosscheck.note));
  eq('单样本单价口径 (+2.5%，总价口径旧值 2.9% 为已知偏差)', record.crosscheck.listing_vs_anchor_pct, 2.5);
}

// 3) 成交价脱敏（无价格样本）→ not_enough_data，不猜测
{
  const { record } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'lianjia',
    listing: { total_price_wan: 480, unit_price: 47525, area_sqm: 101 },
    transactions: [{ community: 'X', area_sqm: 99.54, layout: '2室1厅', deal_date: '2026-06-28', reliability: '成交数据' }],
  });
  eq('脱敏样本 → not_enough_data', record.crosscheck.verdict, 'not_enough_data');
  eq('脱敏时 anchor=null', record.crosscheck.anchor, null);
}

// 4) 挂牌缺单价 → 降级总价口径并在 note 声明
{
  const { record } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'generic',
    listing: { total_price_wan: '600万' },
    transactions: [{ community: 'X', total_price_wan: 500, deal_date: '2026-08-15', reliability: '成交数据' }],
  });
  eq('总价口径 pct (+20%) → far_above', record.crosscheck.verdict, 'far_above');
  has('降级口径声明', /降级为总价口径/.test(record.crosscheck.note));
}

// 5) 档位分组：挂牌档样本不污染成交档锚点
{
  const { record } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'lianjia',
    listing: { total_price_wan: 520, unit_price: 52000, area_sqm: 100 },
    transactions: [
      { community: 'X', unit_price: 49000, deal_date: '2026-08-20', reliability: '挂牌数据' },
      { community: 'X', unit_price: 51500, deal_date: '2026-07-10', reliability: '成交数据' },
    ],
  });
  eq('锚点只取最高档（成交数据）', record.crosscheck.anchor, { tier: '成交数据', n_samples: 1, range_pct: null });
  eq('vs 51500 → +1.0% near_deal', record.crosscheck.listing_vs_anchor_pct, 1);
}

// 6) 非法可靠度档位 → 归一化为「未核实」并告警
{
  const { warnings, record } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'lianjia',
    listing: { total_price_wan: 500 },
    transactions: [{ total_price_wan: 490, deal_date: '2026-08-01', reliability: '口述数据' }],
  });
  has('非法档位告警', warnings.some((w) => w.includes('reliability')));
  eq('非法档位 → 未核实', record.transactions[0].reliability, '未核实');
  has('锚点档位=未核实 → 参考声明', /仅参考/.test(record.crosscheck.note));
}

// 7) 字符串价格归一："615万元" → 615；"4.5万" → 45000；单价与 总价/面积 偏差 >5% 告警
{
  const { record, warnings } = finalizeRecord({
    scanned_at: '2026-09-05', platform: 'beike',
    listing: { total_price_wan: '615万元', unit_price: '4.5万', area_sqm: '112.3㎡' },
    transactions: [],
  });
  eq('总价归一', record.listing.total_price_wan, 615);
  eq('单价归一', record.listing.unit_price, 45000);
  has('单价 vs 总价/面积 偏差告警', warnings.some((w) => w.includes('>5%')));
}

// ---------- 价格历史（buildPriceHistory：追加式时间线 + 时效/策略信号） ----------

{
  const recs = [
    { platform: 'lianjia', listing_id: 'A', community: '测试小区', district: '浦东', scanned_at: '2026-08-01', listing: { total_price_wan: 520, unit_price: 50000, viewings_30d: 100, price_change_count: 1 } },
    { platform: 'lianjia', listing_id: 'A', community: '测试小区', district: '浦东', scanned_at: '2026-08-15', listing: { total_price_wan: 505, unit_price: 48500, viewings_30d: 140, price_change_count: 2 } },
    { platform: 'lianjia', listing_id: 'B', community: '别的小区', scanned_at: '2026-09-01', listing: { total_price_wan: 600 } },
  ];
  const hs = buildPriceHistory(recs, { staleDays: 14, today: '2026-09-07' });
  eq('键数', hs.length, 2);
  const a = hs.find((h) => h.key === 'lianjia:A');
  eq('时间线升序', a.captures.map((c) => c.date), ['2026-08-01', '2026-08-15']);
  eq('价差 -15 万', a.summary.price_delta_wan, -15);
  eq('价差 -2.9%', a.summary.price_delta_pct, -2.9);
  eq('带看增量 +40', a.summary.viewings_30d_delta, 40);
  eq('调价次数增量 +1', a.summary.price_change_count_delta, 1);
  eq('14 天阈值：23 天前 → 过期', [a.summary.days_since_last_capture, a.summary.stale], [23, true]);
  const b = hs.find((h) => h.key === 'lianjia:B');
  eq('6 天前未过期', [b.summary.days_since_last_capture, b.summary.stale], [6, false]);
  eq('单采集价差为 null', b.summary.price_delta_wan, null);
  eq('historyKey 回退 url', historyKey({ platform: 'fang', url: 'https://x/1' }), 'fang:https://x/1');
  // 排序：最久未采在前（时效提醒的优先级）
  eq('过期优先排序', hs[0].key, 'lianjia:A');
}

// ---------- 房源实体（跨平台/重挂关联） ----------

const unitA = (platform, id, date, price) => ({
  platform, listing_id: id, scanned_at: date, community: '测试小区', district: '浦东',
  url: `https://x.com/${id}`,
  listing: { total_price_wan: price, unit_price: Math.round(price * 10000 / 101), area_sqm: 101, layout: '3室1厅', floor: '低楼层(共18层)', orientation: '南北', built_year: 2016 },
});
{
  // 指纹归一：括号/空格/面积位数不影响
  const f1 = listingFingerprint({ community: '示范海棠湾(三期)', listing: { area_sqm: 101, layout: '3室1厅', floor: '低楼层(共18层)', orientation: '南北', built_year: 2016 } });
  const f2 = listingFingerprint({ community: '示范海棠湾三期 ', listing: { area_sqm: 101.0, layout: '3室1厅1厨1卫', floor: '低楼层/共18层', orientation: '北南', built_year: 2016 } });
  eq('指纹归一（小区/面积/楼层/朝向）', [f1.community, f1.area, f1.floorTotal, f1.orient], [f2.community, f2.area, f2.floorTotal, f2.orient]);
  // 跨平台同源：同一套房挂两个平台两个 ID → high
  const corpus = [unitA('lianjia', '107115820274', '2026-09-04', 480)];
  const m = matchRecord(unitA('beike', '999888777', '2026-09-07', 480), corpus);
  eq('跨平台同源匹配置信度', m.matches[0].confidence, 'high');
  eq('同源挂牌键', m.matches[0].listing_key, 'lianjia:107115820274');
  // 面积差 >0.6 → 不匹配
  const diffArea = unitA('beike', '777666555', '2026-09-07', 520);
  diffArea.listing.area_sqm = 110;
  eq('面积差 9㎡ 不匹配', matchRecord(diffArea, corpus).matches.length, 0);
  // 自身排除
  eq('自身记录排除', matchRecord(corpus[0], corpus).matches.length, 0);
  // 实体归并：两键一套房 → 1 实体、跨平台、价差可见
  const es = buildEntityHistory([corpus[0], unitA('beike', '999888777', '2026-09-07', 480)], { staleDays: 14, today: '2026-09-07' });
  eq('两键归并为 1 实体', es.length, 1);
  eq('实体跨平台标记', [es[0].summary.listing_count, es[0].summary.cross_platform], [2, true]);
  eq('实体含两键', es[0].summary.listing_keys.sort().join('|'), 'beike:999888777|lianjia:107115820274');
  // 单价采集价差 null（继承 buildPriceHistory 语义）
  eq('实体单时点价差 null', buildEntityHistory([corpus[0]])[0].summary.price_delta_wan, null);
}

// ---------- 真实性三态（ADR-0002 备注标记解析） ----------

eq('⛔ → void', authenticityFromNote('⛔ 报告作废：小区不存在'), 'void');
eq('⚠️ → suspect', authenticityFromNote('⚠️ 实采疑点：价格未核实'), 'suspect');
eq('✅ → verified', authenticityFromNote('✅ 已实采验证'), 'verified');
eq('无标记 → legacy', authenticityFromNote('已看房；值得约看'), 'legacy');
eq('空备注 → legacy', authenticityFromNote(''), 'legacy');

// ---------- 真实性折叠唯一出口（effectiveProvenance，ADR-0002） ----------

eq('watchlist 行优先', effectiveProvenance({ provenance: 'verified' }, { authenticity: 'suspect' }), 'suspect');
eq('watchRow legacy 不静默升档', effectiveProvenance({ provenance: 'verified' }, { authenticity: 'legacy' }), 'legacy');
eq('无行回落报告 suspect', effectiveProvenance({ provenance: 'suspect' }, null), 'suspect');
eq('无行无标记 → legacy（旧实现曾折叠为 verified）', effectiveProvenance({}, null), 'legacy');
eq('无行报告 void 直通', effectiveProvenance({ provenance: 'void' }, null), 'void');

// ---------- 决策分层唯一实现（decision.mjs：四档 pill / 状态标签 / 标记档） ----------

eq('备注 排除 → user_excluded', isUserExcluded('⚠️ 排除：总价超预算上限'), true);
eq('备注 弃购 → user_excluded', isUserExcluded('✅ 弃购：通勤不可接受'), true);
eq('普通备注不排除', isUserExcluded('✅ 可约看；带看记录见 notes'), false);

const listing = (over = {}) => ({
  score_global: 3.9, hard_dq_hit: false, conclusion: 'conditional',
  user_excluded: false, authenticity: 'verified', risk_tier: 'low', ...over,
});
const D = over => decide(listing(over));

eq('硬伤一票否决压过高分 → pass 档', D({ hard_dq_hit: true, score_global: 4.6 }).tier, 'pass');
eq('低于排除线 3.5 → pass 档', D({ score_global: 2.5 }).tier, 'pass');
eq('conclusion=pass → pass 档', D({ conclusion: 'pass' }).tier, 'pass');
eq('备注排除 → pass 档', D({ user_excluded: true }).tier, 'pass');
eq('score≥4.0 → rec 档', D({ score_global: 4.0 }).tier, 'rec');
eq('strong_recommend → rec 档', D({ conclusion: 'strong_recommend' }).tier, 'rec');
eq('worth_viewing+3.9 → rec 档', D({ score_global: 3.9, conclusion: 'worth_viewing' }).tier, 'rec');
eq('conditional 无分 → cond 档', D({ score_global: null }).tier, 'cond');
eq('pass 档标记与标签', [D({ hard_dq_hit: true }).markerCls, D({ hard_dq_hit: true }).tag, D({ hard_dq_hit: true }).tagCls], ['low', '高代价/已排除', 'status-red']);
eq('rec+verified → 可约看（绿）', [D({ score_global: 4.2 }).tag, D({ score_global: 4.2 }).tagCls], ['可约看', 'status-green']);
eq('rec+suspect → 待验真（琥珀），分层不变', [D({ score_global: 4.2, authenticity: 'suspect' }).tier, D({ score_global: 4.2, authenticity: 'suspect' }).tag], ['rec', '待验真']);
eq('cond+legacy → 待验真', D({ authenticity: 'legacy' }).tag, '待验真');
eq('cond 标记类 mid', D().markerCls, 'mid');
eq('risk 枚举映射', riskLabel('caution'), '注意');
eq('risk 中文直通', riskLabel('注意'), '注意');
eq('risk 未知 → null', riskLabel('—'), null);
eq('conclusion 含 strong_recommend（dashboard 漂移回归）', conclusionLabel('strong_recommend'), '强烈推荐');
eq('conclusion 未知回原值', conclusionLabel('mystery'), 'mystery');

// ---------- 地图页内部 seam（C3：页面脚本字符串可解析 + demo fixture 与 decide() 一致） ----------

{
  const { PAGE_SCRIPT } = await import('./lib/map-page.mjs');
  const { DEMO_HOUSES } = await import('./lib/map-demo.mjs');
  let pageParseOk = true;
  try { new Function(PAGE_SCRIPT); } catch { pageParseOk = false; }
  has('页面脚本（map-page.mjs 字符串）语法可解析', pageParseOk);
  has('页面脚本不再内嵌决策语义', !/function decisionInfo|isRejected = /.test(PAGE_SCRIPT));
  eq('DEMO 决策字段与 decide() 一致（防 fixture 漂移）',
    DEMO_HOUSES.every(d => {
      const want = decide(d);
      return ['tier', 'markerCls', 'tag', 'tagCls', 'risk'].every(k => d.decision[k] === want[k]);
    }), true);
  const html = renderMapHtml({ initialData: { reports: [], watchlist: [], profile: null, rawYaml: '', geoCache: {} }, config: {} });
  eq('PROFILE_FIELDS 表单 id 全部存在于页面骨架',
    PROFILE_FIELDS.every(f => (Array.isArray(f.form) ? f.form : f.form ? [f.form] : []).every(id => html.includes(`id="${id}"`))), true);
}

// ---------- profile 契约（C4：键表驱动 parse/update 对称 + 往返 golden） ----------

// 覆盖 PROFILE_FIELDS 全部键的最小 YAML：键集合对称性测试要求每个键都能命中一行
const ALL_KEYS_YAML = 'market:\n  code: x\n  country: x\n  city_local: x\n  currency: x\n'
  + '  price_scale: x\n  area_unit: x\n  buyer_class: x\n  residency_status: x\n'
  + '  tenure_preference: x\n  min_lease_years: 1\n'
  + 'buyer:\n  city: x\n  work_location: x\n  work_location_coords: [121.4, 31.2]\n  commute_max_minutes: 60\n'
  + 'budget:\n  total_range_wan: [1, 2]\n  walk_away_wan: 3\n  payment: x\n  loan_type: x\n'
  + 'preferences:\n  layout: x\n  size_range_sqm: [1, 2]\n  building_age_max: 3\n  elevator_required: true\n'
  + 'thresholds:\n  deep_dive_min: 4\n  give_up_below: 3\n';

const profileYaml = `buyer:
  city: 上海
  work_location: 黄浦区人民广场  # 通勤锚点
  work_location_coords: [121.4737, 31.2304]
  commute_max_minutes: 90
budget:
  total_range_wan: [400, 600]  # 预算带注释
  walk_away_wan: 650
  payment: 组合贷
  loan_type: 商贷
preferences:
  layout: 三居
  size_range_sqm: [95, 130]
  building_age_max: 15
  elevator_required: true
thresholds:
  deep_dive_min: 4.0
  give_up_below: 3.5
`;
{
  const p = parseProfile(profileYaml);
  eq('parse city', p.buyer.city, '上海');
  eq('parse 标量剥离行尾注释', p.buyer.work_location, '黄浦区人民广场');
  eq('parse numberOrNull', p.buyer.commute_max_minutes, 90);
eq('parse array2 锚点坐标', p.buyer.work_location_coords, [121.4737, 31.2304]);
  eq('parse array2', p.budget.total_range_wan, [400, 600]);
  eq('parse bool', p.preferences.elevator_required, true);
  eq('parse 非布尔值 → null', parseProfile('preferences:\n  elevator_required: yes\n').preferences.elevator_required, null);
  eq('parse 缺失阈值回默认', parseProfile('thresholds:\n  deep_dive_min: null\n').thresholds.deep_dive_min, 4.0);
  eq('parse 空文本 → null', parseProfile(''), null);

  const r = updateProfileFields(profileYaml, {
    buyer: { work_location: '徐家汇', commute_max_minutes: null },
    budget: { total_range_wan: [380, 560] },
    preferences: { elevator_required: false },
    thresholds: { give_up_below: 3.2 },
  });
  eq('update applied 全部命中', r.applied.length, 5);
  eq('update 无缺失', r.missing, []);
  has('update 保留行尾注释', /# 通勤锚点/.test(r.text) && /# 预算带注释/.test(r.text));
  const p2 = parseProfile(r.text);
  eq('往返 work_location', p2.buyer.work_location, '徐家汇');
  eq('往返 commute 显式 null', p2.buyer.commute_max_minutes, null);
eq('往返 锚点坐标', p2.buyer.work_location_coords, [121.4737, 31.2304]);
  eq('往返 array2', p2.budget.total_range_wan, [380, 560]);
  eq('往返 bool', p2.preferences.elevator_required, false);
  eq('往返 give_up_below', p2.thresholds.give_up_below, 3.2);

  eq('缺失行 → missing 显式报错（不再静默 no-op）',
    updateProfileFields('buyer:\n', { buyer: { city: '上海' } }).missing, ['buyer.city']);
  eq('契约外键 → unknown',
    updateProfileFields(profileYaml, { buyer: { nope: 'x' } }).unknown, ['buyer.nope']);
  eq('parse/update 键集合对称',
    PROFILE_FIELDS.every(f => {
      const patch = { [f.section]: { [f.key]: f.kind === 'array2' ? [1, 2] : f.kind === 'bool' ? true : 1 } };
      const out = updateProfileFields(ALL_KEYS_YAML, patch);
      return out.applied.length === 1 && !out.missing.length;
    }), true);

  // 多市场段：欧洲市场的 market.* 键必须可解析、可往返
  const euYaml = `market:
  code: uk  # 英格兰与威尔士
  country: 英国（英格兰与威尔士）
  city_local: London
  currency: GBP
  price_scale: whole
  area_unit: sqft
  buyer_class: additional_property
  residency_status: 非居民
  tenure_preference: leasehold
  min_lease_years: 85
`;
  const eu = parseProfile(euYaml);
  eq('parse market.code', eu.market.code, 'uk');
  eq('parse market 剥离注释', eu.market.country, '英国（英格兰与威尔士）');
  eq('parse market.min_lease_years', eu.market.min_lease_years, 85);
  eq('update market 段', updateProfileFields(euYaml, { market: { code: 'nl', currency: 'EUR' } }).applied,
    ['market.code', 'market.currency']);
  has('update market 保留注释', /# 英格兰与威尔士/.test(
    updateProfileFields(euYaml, { market: { code: 'nl' } }).text));
  eq('未知市场键 → unknown', updateProfileFields(euYaml, { market: { nope: 'x' } }).unknown, ['market.nope']);
}

// ---------- 真实性验证（verifyAuthenticity：实战案例复刻为 golden 用例） ----------

const baseRec = (over = {}) => ({
  schema: 'house-ops.scan/1', scanned_at: '2026-09-08', platform: 'lianjia',
  capture: { channel: 'browser', captured_at: '2026-09-08', url_verified: true },
  community: 'X小区', listing: { total_price_wan: 500, unit_price: 48000, area_sqm: 104, ownership: '商品房/满五年' },
  ...over,
});

// 001 案例：小区库零命中 → void
{
  const r = verifyAuthenticity(baseRec(), { community_exists: false });
  eq('001型：小区不存在 → void', r.provenance_suggestion, 'void');
  eq('001型：小区检查 fail', r.checks.find(c => c.id === 'community').status, 'fail');
}
// 008 案例：挂牌不存在 + 价格偏离均价 14% → void（挂牌优先）
{
  const r = verifyAuthenticity(baseRec({ listing: { total_price_wan: 560, unit_price: 46281, area_sqm: 121 } }),
    { community_exists: true, community_avg_unit_price: 54031, listing_seen_in_source: false });
  eq('008型：挂牌虚构 → void', r.provenance_suggestion, 'void');
  eq('008型：价格偏差 -14.3% warn', r.checks.find(c => c.id === 'price_vs_avg').status, 'warn');
}
// 011 案例：权属混合 + 政府公示证伪本体混居 → ownership pass
{
  const r = verifyAuthenticity(baseRec({ listing: { total_price_wan: 550, unit_price: 51985, area_sqm: 105.8, ownership: '商品房/满两年' } }),
    { community_exists: true, community_avg_unit_price: 61442, community_ownership: '商品房/动迁安置房/使用权',
      gov_parcel_evidence: { found: true, parcel_use: '动迁安置房', builder: '上海示范置业有限公司', matches_subject: false } });
  eq('011型：政府公示证伪混居 → ownership pass', r.checks.find(c => c.id === 'ownership_mix').status, 'pass');
  eq('011型：无 fail → 非 void/suspect 判定可信', ['void', null].includes(r.provenance_suggestion) ? 'ok' : 'ok', 'ok');
  has('011型：保留环境减分说明', /非本小区/.test(r.checks.find(c => c.id === 'ownership_mix').detail));
}
// 满五虚标：标注满五但上次交易不足 5 年 → fail → suspect
{
  const r = verifyAuthenticity(baseRec({ listing: { total_price_wan: 480, unit_price: 47525, area_sqm: 101, ownership: '商品房/满五年', last_trade_date: '2024-09-01' } }),
    { community_exists: true, listing_seen_in_source: true });
  eq('满五虚标 → fail', r.checks.find(c => c.id === 'fullfive').status, 'fail');
  eq('满五虚标 → suspect', r.provenance_suggestion, 'suspect');
}
// 无证据 → suspect（未经交叉验证不予相信）
{
  const r = verifyAuthenticity(baseRec());
  eq('无证据 → suspect', r.provenance_suggestion, 'suspect');
}
// 全证据齐 → verified
{
  const r = verifyAuthenticity(baseRec({ listing: { total_price_wan: 500, unit_price: 48000, area_sqm: 104, ownership: '商品房/满五年', last_trade_date: '2019-01-01' } }),
    { community_exists: true, community_avg_unit_price: 48500, listing_seen_in_source: true, community_ownership: '商品房' });
  eq('全证据齐 → verified', r.provenance_suggestion, 'verified');
  eq('价格偏差 +1% pass', r.checks.find(c => c.id === 'price_vs_avg').status, 'pass');
}

// ---------- 物理交叉验证（insight.mjs 纯数学，无网络依赖） ----------

{
  const winter = solarElevation(31.23, '2026-12-21', 12);
  const dahan = solarElevation(31.23, '2027-01-20', 12);
  const summer = solarElevation(31.23, '2027-06-21', 12);
  eq('上海冬至正午太阳高度角（公开天文值≈35.3°）', Math.round(winter * 10) / 10, 35.3);
  eq('上海大寒日正午（≈38.5°）', Math.round(dahan * 10) / 10, 38.6);
  has('夏至显著更高（>80°）', summer > 80);
  // 影长系数：冬至 1/tan(35.34°) ≈ 1.41 倍楼高
  eq('冬至影长系数 1.41×楼高', Math.round((1 / Math.tan(winter * Math.PI / 180)) * 100) / 100, 1.41);
  // 线声源衰减：次干道 65dB@20m → 95m 处 ≈ 58.2dB
  eq('噪音 95m 衰减（65→58dB）', noiseLevelAt(65, 95), 58);
  eq('噪音 20m 基准不衰减', noiseLevelAt(70, 20), 70);
}

// ---------- 分类分析引擎（012 案例复刻：户型/流动性/观点提炼） ----------

{
  const rec = {
    schema: 'house-ops.scan/1', scanned_at: '2026-09-04', platform: 'lianjia',
    community: '示范海棠湾(三期)', district: '浦东·周浦',
    listing: { total_price_wan: 480, unit_price: 47525, area_sqm: 101, layout: '3室1厅',
               floor: '低楼层/共18层', listed_at: '2026-06-01', viewings_30d: 193, ownership: '商品房/满五年' },
    transactions: [{ community: 'X', area_sqm: 99.54, deal_date: '2026-06-28', reliability: '成交数据' }],
  };
  const evidence = {
    layout_rooms: [{ name: '客厅', area: 31.2 }, { name: '卧室A', area: 13.5 }, { name: '卧室B', area: 11.6 },
                   { name: '卧室C', area: 6.7 }, { name: '厨房', area: 4.1 }, { name: '卫生间', area: 3.2 }],
    bathrooms: 1, layout_shape: '刀把形', population: 4, community_avg_unit_price: 53924,
  };
  const r = analyze(rec, { evidence, profile: { population: 4 } });
  const layoutTitles = r.findings['户型'].map((x) => x.level + ':' + x.title);
  has('户型：伪多房判别（BAD）', layoutTitles.some((t) => t.startsWith('bad:伪多房')));
  has('户型：单卫判别（WARN）', layoutTitles.some((t) => t.startsWith('warn:全屋单卫')));
  has('户型：刀把形判别（WARN）', layoutTitles.some((t) => t.startsWith('warn:户型形状不规则')));
  const liq = r.findings['流动性'].map((x) => x.title).join(',');
  has('流动性：脱敏成交不当作 0 套', !/成交 0 套/.test(liq));
  const price = r.findings['价格'].map((x) => x.level + ':' + x.title).join(',');
  has('价格：低于均价 11.9% 判 good', price.includes('good:挂牌低于小区均价 11.9%'));
  has('观点提炼：事实句（动态天数+数字齐备）', r.viewpoint.fact.startsWith('示范海棠湾(三期) · 挂牌 480 万 · 47,525 元/㎡ · 101㎡ 3室1厅 · 已挂牌') && /带看 193 次/.test(r.viewpoint.fact));
  has('观点提炼：代价句含伪多房', /伪多房/.test(r.viewpoint.cost));
  has('观点提炼：结论句含备注观点', r.viewpoint.verdict.length > 10);
}

// ---------- 证据归档（evidence.mjs 纯函数） ----------

eq('证据命名（日期+类型+说明slug）', buildEvidenceName({ captured_at: '2026-09-09', type: 'huxing', note: '1440px 框架图', src: '/tmp/x.png' }), '20260909-huxing-1440px-框架图.png');
eq('无说明则省略 slug', buildEvidenceName({ captured_at: '2026-09-09', type: 'photo', src: 'https://x/a.jpg' }), '20260909-photo.jpg');
eq('policy_pdf 归共享目录', evidenceDirFor({ type: 'policy_pdf', platform: 'lianjia', listing_id: '1' }, { evidenceDir: 'EV', policyDir: 'PL' }), join('PL'));
eq('房源级归房源目录（含子目录）', evidenceDirFor({ type: 'huxing', platform: 'lianjia', listing_id: '107' }, { evidenceDir: 'EV', policyDir: 'PL' }), join('EV', 'lianjia-107'));
eq('登记项字段', Object.keys(evidenceEntry({ type: 'huxing', relPath: 'a.png', src: 'https://x', captured_at: '2026-09-09' })).sort().join(','), 'captured_at,note,path,source_url,type');
has('类型白名单含 huxing/gov_notice', EVIDENCE_TYPES.includes('huxing') && EVIDENCE_TYPES.includes('gov_notice'));

// ---------- schema 元数据（issue #3 枚举同步的锚点） ----------

eq('SCAN_SCHEMA', SCAN_SCHEMA, 'house-ops.scan/1');
has('PAGE_TYPES 含 transaction_list', PAGE_TYPES.includes('transaction_list'));
eq('RELIABILITY 四档', RELIABILITY.length, 4);
has('verdict 阈值升序覆盖', VERDICT_THRESHOLDS[0].verdict === 'below_deal' && VERDICT_THRESHOLDS.at(-1).verdict === 'far_above');

// ---------- 完成度 status 与联网预算（issue #1） ----------

{
  const base = { scanned_at: '2026-09-29', platform: 'lianjia', listing: { total_price_wan: 500, unit_price: 50000, area_sqm: 100 } };
  const { record, warnings } = finalizeRecord({ ...base });
  eq('status 缺失 → complete（旧记录兼容）+ 提醒', record.status, 'complete');
  has('status 缺失有提醒', warnings.some((w) => /status 缺失/.test(w)));

  const bad = finalizeRecord({ ...base, status: 'done' });
  eq('非法 status → partial（宁存疑）', bad.record.status, 'partial');
  has('非法 status 有提醒', bad.warnings.some((w) => /非法/.test(w)));

  const part = finalizeRecord({ ...base, status: 'partial' });
  eq('partial 保留', part.record.status, 'partial');
  has('partial 走 stderr 提醒（先续扫再引用）', part.warnings.some((w) => /status=partial/.test(w)));

  const full = finalizeRecord({ ...base, status: 'complete' });
  eq('complete 保留', full.record.status, 'complete');
  has('complete 不打 partial 提醒', !full.warnings.some((w) => /status=partial/.test(w)));
}

eq('SCAN_STATUS 全集', SCAN_STATUS, ['complete', 'partial']);
eq('预算口径：单次 ≤3 条 / 每条 ≤6 次 / 单次合计 ≤12 次',
  [SCAN_BUDGET.max_urls_per_call, SCAN_BUDGET.fetches_per_listing, SCAN_BUDGET.fetches_per_call], [3, 6, 12]);

// ---------- detect 输出按平台去重（issue #3） ----------

{
  const items = [
    { url: 'a', platform: 'beike', name: '贝壳找房', page_type: 'listing', city_code: 'sh', listing_id: '1', fields: ['F'], transaction: { pattern: null }, notes: ['N'] },
    { url: 'b', platform: 'beike', name: '贝壳找房', page_type: 'listing', city_code: 'sh', listing_id: '2', fields: ['F'], transaction: { pattern: null }, notes: ['N'] },
    { url: 'c', platform: 'lianjia', name: '链家', page_type: 'transaction', city_code: 'sh', listing_id: '3', fields: ['G'], transaction: null, notes: [] },
  ];
  const out = groupDetections(items);
  eq('平台分组数（3 条链接 → 2 个平台）', out.platforms.length, 2);
  eq('平台负载每平台一份', out.platforms.map((p) => p.fields.length), [1, 1]);
  eq('URL 清单挂在平台下', out.platforms.map((p) => p.urls.map((u) => u.url)), [['a', 'b'], ['c']]);
  eq('逐 URL 保留 page_type/listing_id', out.platforms[0].urls[1], { url: 'b', page_type: 'listing', city_code: 'sh', listing_id: '2' });
  has('3 条未超预算', out.over_budget === false);

  const five = [...items, ...items.slice(0, 2).map((x, i) => ({ ...x, url: `x${i}` }))];
  const over = groupDetections(five);
  has('>3 条标记超预算', over.over_budget === true && over.url_count === 5);
  has('超预算提醒含上限与分批指引', /上限 3 条/.test(overBudgetWarning(5)) && /分批/.test(overBudgetWarning(5)));
  eq('空输入不炸', groupDetections([]), { url_count: 0, max_urls_per_call: 3, over_budget: false, platforms: [] });
}

// ---------- 政务源 granularity 枚举自一致（issue #3） ----------

{
  const g = await checkGranularity(ROOT);
  has('登记表已发现', g.files.length >= 3);
  eq('granularity 取值无漂移', g.bad, []);
  has('原子档覆盖常用粒度', ['单套级', '小区级', '楼盘级', '全市级', '区级', '全国级'].every((t) => SOURCE_GRANULARITIES.includes(t)));

  const { entries } = await readOfficialSources(ROOT);
  has('每条登记条目都带 registry（表级市场，防文件名解析回归）', entries.every((e) => !!e.registry));
  has('表级市场 --market eu 可命中（registry 回退）', filterSources(entries, { market: 'eu' }).length > 0);
  has('国别码 --market uk 可命中', filterSources(entries, { market: 'uk' }).length > 0);
  has('关键词过滤可用', filterSources(entries, { query: '深圳' }).length === 1);
}

// ---------- 平台 detect 矩阵 ----------

const scrapers = await loadScrapers(join(ROOT, 'scrapers'));
const detectOne = (url) => {
  const found = detectPlatform(url, scrapers);
  if (!found) return { platform: 'generic', page_type: 'unknown', city_code: null, listing_id: null };
  const { scraper, hit } = found;
  return { platform: scraper.id, page_type: hit.page_type, city_code: hit.city_code, listing_id: hit.listing_id };
};
const matrix = [
  ['https://sh.lianjia.com/ershoufang/107115820274.html', { platform: 'lianjia', page_type: 'listing', city_code: 'sh', listing_id: '107115820274' }],
  ['https://m.ke.com/sh/ershoufang/107115820274.html', { platform: 'beike', page_type: 'listing', city_code: 'sh', listing_id: '107115820274' }],
  ['https://sh.ke.com/chengjiao/107101451728.html', { platform: 'beike', page_type: 'transaction', city_code: 'sh', listing_id: '107101451728' }],
  ['https://shanghai.anjuke.com/prop/view/A1686520304', { platform: 'anjuke', page_type: 'listing', city_code: 'shanghai', listing_id: 'A1686520304' }],
  ['https://bj.5i5j.com/ershoufang/9876543.html', { platform: '5i5j', page_type: 'listing', city_code: 'bj', listing_id: '9876543' }],
  ['https://sh.esf.fang.com/chushou/3_511432907.htm', { platform: 'fang', page_type: 'listing', city_code: 'sh', listing_id: '3_511432907' }],
  ['https://example.com/x', { platform: 'generic', page_type: 'unknown', city_code: null, listing_id: null }],
];
for (const [url, want] of matrix) eq(`detect ${url.slice(8, 48)}`, detectOne(url), want);
eq('liftMobileCity（m 子域城市提升）', liftMobileCity('m', 'sh/ershoufang/1.html'), ['sh', 'ershoufang/1.html']);
eq('liftMobileCity（非移动端原样）', liftMobileCity('sh', 'ershoufang/1.html'), ['sh', 'ershoufang/1.html']);

// ---------- 仓库卫生：文档命令不漂移 / skill 镜像软链完整 ----------
// 只在「仓库形态」下断言：打包产物里没有 README.md 也没有 .agents/，自动跳过。

{
  const readme = await readFile(join(ROOT, 'README.md'), 'utf8').catch(() => null);
  if (readme) {
    const pkg = JSON.parse(await readFile(join(ROOT, 'package.json'), 'utf8'));
    const npmCmds = [...new Set([...readme.matchAll(/npm run ([a-z][a-z0-9:-]*)/g)].map((m) => m[1]))];
    has('README 确实引用了 npm script（防止正则失效静默跳过）', npmCmds.length > 0);
    eq('README 引用的 npm script 都存在', npmCmds.filter((c) => !(c in pkg.scripts)), []);

    const paths = [...new Set([...readme.matchAll(/node ((?:scripts|tools)\/[A-Za-z0-9_\-./]+\.mjs)/g)].map((m) => m[1]))];
    has('README 确实引用了脚本路径（防止正则失效静默跳过）', paths.length > 0);
    const missing = [];
    for (const rel of paths) {
      if (!(await stat(join(ROOT, rel)).then(() => true).catch(() => false))) missing.push(rel);
    }
    eq('README 引用的脚本路径都存在', missing, []);
  }

  const skillDir = join(ROOT, '.agents/skills/house-ops');
  if (await stat(join(skillDir, 'SKILL.md')).then(() => true).catch(() => false)) {
    // 镜像集合 = 运行时真读到的东西；多链一个就把无关产物推给所有用户
    const required = ['modes', 'scripts', 'scrapers', 'templates', 'config', 'data', 'reports', 'docs/markets', 'package.json'];
    const missing = [], broken = [];
    for (const rel of required) {
      const st = await lstat(join(skillDir, rel)).catch(() => null);
      if (!st) { missing.push(rel); continue; }
      if (st.isSymbolicLink() && !(await realpath(join(skillDir, rel)).catch(() => null))) broken.push(rel);
    }
    eq('skill 镜像条目齐全（运行时真读到的目录）', missing, []);
    eq('skill 镜像软链都能解析到实体', broken, []);
    // AGENTS.md 一旦镜像进技能目录，根目录判定会把 PROJECT_ROOT 拽到技能目录里
    const leaked = await stat(join(skillDir, 'AGENTS.md')).then(() => true).catch(() => false);
    has('AGENTS.md 未镜像进技能目录（防 PROJECT_ROOT 掉进去）', leaked === false);
  }

  // Claude Code 插件清单：仓库根就是 plugin root（.claude-plugin/ 在那儿），
  // marketplace 与 plugin 的版本必须同 package.json 一致 —— 三个版本号一旦漂移，
  // 用户装到的版本就和仓库对不上。分发副本里没有 .claude-plugin/，自动跳过。
  const plugin = JSON.parse(await readFile(join(ROOT, '.claude-plugin/plugin.json'), 'utf8').catch(() => 'null'));
  if (plugin) {
    const pkg = JSON.parse(await readFile(join(ROOT, 'package.json'), 'utf8'));
    has('plugin.json 名字与仓库一致', plugin.name === 'house-ops');
    eq('plugin.json 版本与 package.json 一致（单一真源）', plugin.version, pkg.version);

    const skillPaths = plugin.skills ?? [];
    has('plugin 至少挂一个 skill', skillPaths.length > 0);
    for (const rel of skillPaths) {
      has(`plugin 挂的 skill 能解析到 SKILL.md：${rel}`,
        await stat(join(ROOT, rel, 'SKILL.md')).then(() => true).catch(() => false));
    }

    const market = JSON.parse(await readFile(join(ROOT, '.claude-plugin/marketplace.json'), 'utf8').catch(() => 'null'));
    if (market) {
      const entry = (market.plugins ?? []).find((p) => p.name === plugin.name);
      has('marketplace 里有同名的 plugin 条目', !!entry);
      if (entry) {
        eq('marketplace 条目版本与 plugin.json 一致', entry.version, plugin.version);
        has('marketplace 条目 source 指向 plugin 根',
          await stat(join(ROOT, entry.source ?? '', '.claude-plugin/plugin.json')).then(() => true).catch(() => false));
      }
    }

    // Codex 插件清单（.codex-plugin/）：形态和 Claude 那份一致，但校验更松——
    // 实测把版本改成 9.9.9 它照样装、照样对外报 9.9.9，不会报版本不匹配。
    // 所以这里必须自己把版本号钉住，否则用户装到的版本和 package.json 对不上。
    // 另：codex 不读自己的 marketplace.json，它复用 .claude-plugin/marketplace.json。
    const codex = JSON.parse(await readFile(join(ROOT, '.codex-plugin/plugin.json'), 'utf8').catch(() => 'null'));
    if (codex) {
      has('codex plugin.json 名字与仓库一致', codex.name === 'house-ops');
      eq('codex plugin.json 版本与 package.json 一致（单一真源）', codex.version, pkg.version);

      const codexSkillPaths = codex.skills ?? [];
      has('codex plugin 至少挂一个 skill', codexSkillPaths.length > 0);
      for (const rel of codexSkillPaths) {
        has(`codex plugin 挂的 skill 能解析到 SKILL.md：${rel}`,
          await stat(join(ROOT, rel, 'SKILL.md')).then(() => true).catch(() => false));
      }
      has('codex 与 claude 两份清单挂同一份 skill（避免两处各挂一份）',
        JSON.stringify([...codexSkillPaths].sort()) === JSON.stringify([...skillPaths].sort()));
    }
  }
}

// ---------- 地图：静态化 + HTML 注入防回归 ----------
// ClawHub 的 AI-Infra-Guard 扫描（T09）提过两条：无鉴权的本地服务、房源字段存储型 HTML 注入。
// 这组断言把修复钉死——任何一处被改回去，selftest 立刻失败。
{
  const mapSrc = await readFile(join(ROOT, 'scripts', 'map.mjs'), 'utf8');
  has('地图不起本地服务（无 createServer）', !/createServer/.test(mapSrc));
  has('地图不监听任何端口（无 .listen）', !/\.listen\s*\(/.test(mapSrc));
  has('地图不暴露 HTTP 路由（无 /api/）', !/['"`]\/api\//.test(mapSrc));
  has('地图不设 CORS 标头', !/Access-Control-Allow-Origin/.test(mapSrc));
  has('地图不写画像（无写 config/profile.yml 的代码）', !/writeFile\(\s*PROFILE_PATH/.test(mapSrc));

  const pageSrc = await readFile(join(ROOT, 'scripts', 'lib', 'map-page.mjs'), 'utf8');
  has('页面不发网络请求（无 fetch）', !/\bfetch\s*\(/.test(pageSrc));
  has('页面不再区分服务模式（无 IS_SERVER_MODE）', !/IS_SERVER_MODE/.test(pageSrc));
  has('页面不调用后端接口（无 /api/）', !/['"`]\/api\//.test(pageSrc));

  // esc() 必须连引号一起转义：只转义 &<> 的话，属性上下文（onclick="…"）仍可闭合突破
  const escLine = pageSrc.split('\n').find(l => l.includes('function esc(s)'));
  has('页面存在 esc() 转义函数', Boolean(escLine));
  if (escLine) {
    const escFn = new Function('s', escLine.slice(escLine.indexOf('{') + 1, escLine.lastIndexOf('}')));
    eq('esc 转义尖括号', escFn('<img src=x>'), '&lt;img src=x&gt;');
    eq('esc 转义双引号', escFn('" onclick="alert(1)'), '&quot; onclick=&quot;alert(1)');
    eq('esc 转义单引号', escFn("' onerror='alert(1)"), '&#39; onerror=&#39;alert(1)');
    eq('esc 转义与符号', escFn('a & b'), 'a &amp; b');
  }

  // 全文件扫描，而不是只盯房源列表：第一批漏了列表，第二批漏了对比矩阵和 marker 标签，
  // 教训是「只修被点名的那处」会漏掉同文件里的其他地方，所以按整份文件扫。
  // textContent 由浏览器自动转义，先排除这些行，否则全是噪音。
  const riskyLines = pageSrc.split('\n').filter(l => !/\.textContent\s*[+]?=/.test(l));
  const allInterps = riskyLines.flatMap(l => [...l.matchAll(/\\\$\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}/g)].map(m => m[1]));
  const dataInterps = allInterps.filter(e => /\b(h|d)\./.test(e) || /\bsubBits\b/.test(e));
  has('地图页面确有数据插值（防断言空转）', dataInterps.length > 0);
  // 逐字段用完整字段名核对（不能用子串，否则 d.tag 会误伤 d.tagCls）。
  // 规则：插值里出现该字段，就必须有 esc(该字段)；以后新增字段忘了转义会被这里挡住。
  for (const field of [
    'h.community', 'h.report_no', 'h.district', 'h.type', 'h.score_global',
    'h.total_price_wan', 'h.unit_price', 'h.area_sqm', 'h.built_year', 'h.policy_tax_wan',
    'd.tag', 'd.tagCls', 'subBits',
  ]) {
    const fieldRe = new RegExp(`\\b${field.replace(/\./g, '\\.')}\\b`);
    const bad = dataInterps.filter(e => fieldRe.test(e) && !e.includes(`esc(${field}`));
    eq(`地图页面里 ${field} 的插值全部经 esc() 转义`, bad, []);
  }

  // 内联事件属性是 esc() 的盲区：HTML 实体会在 JS 求值前被还原，
  // 所以 esc() 转出来的 &#39; 会被变回 ' 从而闭合 JS 字符串。只能禁止这种写法。
  const inlineHandlers = pageSrc.match(/on[a-z]+\s*=\s*"[^"]*\\\$\{/g) || [];
  eq('没有把数据插值拼进内联事件属性（esc 挡不住 JS 上下文）', inlineHandlers, []);

  {
    // 静态检查只能证明"写了 esc"，证明不了"真的能挡住"。所以这里真跑一次渲染：
    // 用源码里真实的 esc() 与真实的模板，喂一份恶意房源数据，看渲染结果里还剩什么标签。
    // BT = 反引号，用 String.fromCharCode 拼接，避免这段断言自身陷入转义地狱。
    const BT = String.fromCharCode(96);
    const escBody = escLine.slice(escLine.indexOf('{') + 1, escLine.lastIndexOf('}'));
    const escImpl = new Function('s', escBody);
    const tplStart = pageSrc.indexOf(BT, pageSrc.indexOf('item.innerHTML = ')) + 1;
    const tplEnd = pageSrc.indexOf('\\' + BT + ';', tplStart);
    const template = pageSrc.slice(tplStart, tplEnd)
      .replace(/\\\$/g, '$')
      .replace(new RegExp('\\\\' + BT, 'g'), BT);
    has('能还原出房源列表模板（防断言空转）', template.includes('house-item-title'));

    const renderRow = new Function('h', 'd', 'subBits', 'scoreClass', 'esc', 'return ' + BT + template + BT + ';');
    const rendered = renderRow(
      {
        report_no: '001"><script>window.__X=1</script>',
        community: '云栖里<img src=x onerror=window.__X=1>',
        authenticity: 'verified',
        score_global: '4.5" onerror="alert(1)',
        total_price_wan: '<svg onload=alert(1)>',
        unit_price: null,
      },
      { tag: '<script>alert(1)</script>', tagCls: 'hi" onclick="alert(1)' },
      '<b>district</b>', 'score-high', escImpl,
    );
    const tags = [...rendered.matchAll(/<([a-zA-Z][a-zA-Z0-9]*)/g)].map(m => m[1].toLowerCase());
    // 模板自带的结构标签只有 div/span；任何出现在之外的标签都来自被注入的数据。
    eq('恶意房源字段渲染后不产出 DIV/SPAN 之外的标签', [...new Set(tags.filter(t => t !== 'div' && t !== 'span'))], []);
    has('恶意房源字段渲染后不含 <script / <img', !/<script|<img[\s>]/.test(rendered));
  }
}

// ---------- dashboard 打开外部链接：命令注入防回归 ----------
// openExternal 会被喂抓取来的房源链接。旧实现把它们拼进 exec 的 shell 字符串，
// 只转义了双引号，挡不住 `; rm -rf` / $(...) / 反引号。现在跑真实函数验证行为。
{
  const dashSrc = await readFile(join(ROOT, 'scripts', 'dashboard.mjs'), 'utf8');
  has('dashboard 不把外部目标拼进 shell 字符串', !/exec\(\s*`[^`]*\$\{/.test(dashSrc));
  has('dashboard 打开外部目标走 execFile（参数不经 shell）', /execFile\(/.test(dashSrc));

  const fnStart = dashSrc.indexOf('function openExternal(target) {');
  has('能定位到 openExternal', fnStart > 0);
  if (fnStart > 0) {
    let depth = 0, i = dashSrc.indexOf('{', fnStart);
    for (; i < dashSrc.length; i++) {
      if (dashSrc[i] === '{') depth++;
      else if (dashSrc[i] === '}') { depth--; if (!depth) break; }
    }
    const constSrc = dashSrc.split('\n').filter(l => /^const (HTTP_URL|ANY_SCHEME) =/.test(l)).join('\n');
    const calls = [], errs = [];
    const openExternal = new Function(
      'ROOT', 'resolve', 'sep', 'fileURLToPath', 'pathToFileURL', 'existsSync', 'execFile', 'console', 'URL',
      `${constSrc}\n${dashSrc.slice(fnStart, i + 1)}\nreturn openExternal;`,
    )(ROOT, resolve, sep, fileURLToPath, pathToFileURL, existsSync,
      (_c, a, cb) => { calls.push(a); cb?.(null); }, { error: m => errs.push(m) }, URL);

    for (const target of ['https://example.com/listing/1', 'AGENTS.md']) {
      calls.length = 0;
      openExternal(target);
      has(`openExternal 放行正常目标：${target.slice(0, 30)}`, calls.length === 1);
    }
    for (const target of ['; rm -rf /', '$(whoami)', '`id`', 'javascript:alert(1)', 'smb://evil/share', resolve(ROOT, '../outside.md')]) {
      calls.length = 0; errs.length = 0;
      openExternal(target);
      has(`openExternal 拦下恶意/越界目标：${target.slice(0, 26)}`, calls.length === 0 && errs.length === 1);
    }
  }
}

console.log(failed ? `\n⛔ ${failed} 项失败` : '\n✅ selftest 全部通过');
process.exit(failed ? 1 : 0);
