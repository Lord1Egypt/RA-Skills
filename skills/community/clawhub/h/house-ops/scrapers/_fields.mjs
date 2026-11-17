// _fields.mjs — 扫描记录的字段契约与数值归一化（scripts/scan.mjs 与各平台模块共享）。
// schema SoT：modes/scan.md 的「扫描记录 schema」节，键名变更需同步该文件。
// 依赖：零依赖（Node ≥18）。

export const SCAN_SCHEMA = 'house-ops.scan/1';

// page_type 枚举以本文件为 SoT；modes/scan.md 的 schema 节与之一致（doctor 断言）
export const PAGE_TYPES = ['listing', 'transaction', 'transaction_list', 'community', 'new_home', 'market', 'search', 'unknown'];

// crosscheck verdict 阈值（实现源）；scan.md Step 4 的解读表与这里保持一致
export const VERDICT_THRESHOLDS = [
  { verdict: 'below_deal', max: -10, note: '挂牌低于可比成交锚点 ≥10%——先核实硬伤（采光遮挡/凶宅/税费转嫁/急售原因）再谈捡漏' },
  { verdict: 'near_deal', max: 5, note: '挂牌价贴近可比成交锚点——定价贴合市场' },
  { verdict: 'above_deal', max: 15, note: '挂牌高于可比成交锚点——议价空间参考此偏差与挂牌时长' },
  { verdict: 'far_above', max: Infinity, note: '挂牌明显高于可比成交锚点（>15%）——虚高挂牌或成交样本过旧，需核实' },
];

// 可靠度四档（SoT：modes/_shared.md「数据可靠度四档」节），index 越小越可信
export const RELIABILITY = ['成交数据', '挂牌数据', '中介口述', '未核实'];

// 扫描记录完成度：complete = 预算内查完；partial = 联网预算中断留的残缺记录（引用前先续扫）
// SoT：modes/scan.md「联网预算与中断」节；doctor 断言 scan.md 含这两个 token。
export const SCAN_STATUS = ['complete', 'partial'];

// 联网预算（AI 侧执行，脚本只做入口提醒）：每条链接 ≤6 次、单次调用合计 ≤12 次、单次 ≤3 条链接
export const SCAN_BUDGET = { max_urls_per_call: 3, fetches_per_listing: 6, fetches_per_call: 12 };

// 政务源数据粒度原子档（SoT 本文件；templates/official-sources.*.yml 的 granularity 只能取这些值，
// 多粒度用内联数组）。doctor 断言登记表不漂移。
export const SOURCE_GRANULARITIES = ['单套级', '地块级', '楼盘级', '小区级', '街区级', '片区级', '区级', '全市级', '全国级'];

// 各平台通用的挂牌页提取清单（AI 按 scan 模式逐项抓取）
export const COMMON_LISTING_FIELDS = [
  '挂牌标题（话术反查用）', '小区名（含所在区/板块）', '总价（万元）', '单价（元/㎡）', '建筑面积（㎡）',
  '户型（几室几厅）', '楼层/总楼层', '电梯（有无）', '建成年代', '朝向', '装修程度',
  '挂牌时间与调价记录（次数/方向/幅度）', '交易权属（商品房/经适/回迁等）',
];

function firstNumber(raw) {
  const m = /-?\d[\d,]*(?:\.\d+)?/.exec(String(raw).replace(/，/g, ','));
  return m ? Number(m[0].replace(/,/g, '')) : NaN;
}

// "480万" → 480；"4800000" / "4,800,000元" → 480（页面给"元"时自动折万）
export function parsePriceWan(v, warnings = [], label = '') {
  const raw = String(v ?? '').trim();
  if (!raw) return null;
  let n = firstNumber(raw);
  if (!Number.isFinite(n)) {
    warnings.push(`${label}: 无法解析 "${raw}" → null`);
    return null;
  }
  if (!/万/.test(raw) && n >= 10000) n = n / 10000;
  return Math.round(n * 100) / 100;
}

// "95000元/㎡" → 95000；"9.5万" → 95000
export function parseUnitPrice(v, warnings = [], label = '') {
  const raw = String(v ?? '').trim();
  if (!raw) return null;
  const n = firstNumber(raw);
  if (!Number.isFinite(n)) {
    warnings.push(`${label}: 无法解析 "${raw}" → null`);
    return null;
  }
  return Math.round(/万/.test(raw) ? n * 10000 : n);
}

// "89.5㎡" / "89.5平米" → 89.5
export function parseAreaSqm(v, warnings = [], label = '') {
  const raw = String(v ?? '').trim();
  if (!raw) return null;
  const n = firstNumber(raw);
  if (!Number.isFinite(n)) {
    warnings.push(`${label}: 无法解析 "${raw}" → null`);
    return null;
  }
  return Math.round(n * 100) / 100;
}

function normField(obj, key, fn, warnings, label) {
  if (obj && obj[key] != null && obj[key] !== '') obj[key] = fn(obj[key], warnings, label);
}

// 归一化整条记录：价格单位、单价一致性（±5%）、可靠度档位合法性。
// 只修正可机械判定的部分，不虚构任何字段。返回 { record, warnings }。
export function normalizeRecord(raw) {
  const rec = structuredClone(raw ?? {});
  const warnings = [];
  rec.schema = SCAN_SCHEMA;
  if (!rec.scanned_at) warnings.push('scanned_at 缺失——应为扫描日期 YYYY-MM-DD');
  // 完成度：缺失按 complete 处理（兼容旧记录）但提醒显式声明；非法值按 partial（宁存疑）
  if (!SCAN_STATUS.includes(rec.status)) {
    if (rec.status == null || rec.status === '') {
      rec.status = 'complete';
      warnings.push('status 缺失——按 complete 处理（旧记录兼容）；联网预算中断时务必显式写 "partial"');
    } else {
      rec.status = 'partial';
      warnings.push(`status "${rec.status}" 非法（∈ ${SCAN_STATUS.join('|')}）→ 按 partial 处理`);
    }
  }
  if (rec.status === 'partial') {
    warnings.push('本记录 status=partial（预算中断的残缺记录）——未查项写入 unverified_items，落盘后先续扫再交给 evaluate 引用');
  }

  const L = (rec.listing ??= {});
  normField(L, 'total_price_wan', parsePriceWan, warnings, 'listing.total_price_wan');
  normField(L, 'unit_price', parseUnitPrice, warnings, 'listing.unit_price');
  normField(L, 'area_sqm', parseAreaSqm, warnings, 'listing.area_sqm');
  if (Number.isFinite(L.total_price_wan) && Number.isFinite(L.area_sqm) && L.area_sqm > 0) {
    const implied = Math.round((L.total_price_wan * 10000) / L.area_sqm);
    if (Number.isFinite(L.unit_price) && L.unit_price > 0) {
      if (Math.abs(implied - L.unit_price) / L.unit_price > 0.05) {
        warnings.push(`listing.unit_price（${L.unit_price}）与 总价/面积 推导值（${implied}）偏差 >5%——以页面为准，差异原因进 unverified_items`);
      }
    } else {
      L.unit_price = implied;
      warnings.push(`listing.unit_price 缺失，已按 总价/面积 推导为 ${implied} 元/㎡`);
    }
  }
  if (!RELIABILITY.includes(L.source_reliability)) L.source_reliability = '挂牌数据';

  (rec.transactions ??= []).forEach((t, i) => {
    normField(t, 'total_price_wan', parsePriceWan, warnings, `transactions[${i}].total_price_wan`);
    normField(t, 'unit_price', parseUnitPrice, warnings, `transactions[${i}].unit_price`);
    normField(t, 'area_sqm', parseAreaSqm, warnings, `transactions[${i}].area_sqm`);
    // 成交样本与挂牌同规则：缺单价时由 总价/面积 推导补齐（静默，不告警）
    if (!Number.isFinite(t.unit_price) && Number.isFinite(t.total_price_wan) && Number.isFinite(t.area_sqm) && t.area_sqm > 0) {
      t.unit_price = Math.round((t.total_price_wan * 10000) / t.area_sqm);
    }
    if (!RELIABILITY.includes(t.reliability)) {
      warnings.push(`transactions[${i}].reliability "${t.reliability}" 非法 → "未核实"`);
      t.reliability = '未核实';
    }
  });

  return { record: rec, warnings };
}

// ---------- 房源实体（跨平台/重挂关联）：指纹匹配 + 实体级历史 ----------

// 物理房屋身份 = 小区 + 面积 + 户型 + 总楼层 + 朝向 + 年代。
// 挂牌 ID/平台/价格/核验码不是身份——房东下架重挂（换 ID/换平台）后它们全变。
export function listingFingerprint(rec) {
  const L = rec?.listing ?? {};
  const normCommunity = String(rec?.community ?? '').replace(/[\s（）()·、]/g, '').toLowerCase();
  const area = Number.isFinite(L.area_sqm) ? Math.round(L.area_sqm * 10) / 10 : null;
  const lm = String(L.layout ?? '').match(/(\d+)室(\d+)?厅?/);
  const fm = String(L.floor ?? '').match(/共(\d+)层/);
  const orient = [...new Set(String(L.orientation ?? '').split('').filter((c) => /[东西南北]/.test(c)))]
    .sort((a, b) => '东南西北'.indexOf(a) - '东南西北'.indexOf(b))
    .join('');
  return {
    community: normCommunity || null,
    area,
    rooms: lm ? Number(lm[1]) : null,
    halls: lm && lm[2] != null ? Number(lm[2]) : null,
    floorTotal: fm ? Number(fm[1]) : null,
    orient: orient || null,
    year: Number.isFinite(L.built_year) ? L.built_year : null,
  };
}

// 新记录 vs 既有记录集合：找出同一物理房源的挂牌记录（跨平台/跨挂牌键）。
// 硬条件：小区（归一后）相同 且 |面积差|≤0.6㎡；软信号（室/厅/总楼层/朝向/年代）逐项计分。
// 自身（同 historyKey 且同 scanned_at）排除。返回按置信度排序的匹配列表。
export function matchRecord(record, existing) {
  const fp = listingFingerprint(record);
  const matches = [];
  for (const rec of existing ?? []) {
    if (historyKey(rec) === historyKey(record) && String(rec?.scanned_at ?? '') === String(record?.scanned_at ?? '')) continue;
    const fp2 = listingFingerprint(rec);
    if (!fp.community || !fp2.community || fp.community !== fp2.community) continue;
    if (fp.area == null || fp2.area == null || Math.abs(fp.area - fp2.area) > 0.6) continue;
    let score = 0;
    const reasons = [];
    const conflicts = [];
    if (fp.rooms != null && fp2.rooms != null) {
      if (fp.rooms === fp2.rooms) { score += 2; reasons.push(`同为${fp.rooms}室`); }
      else conflicts.push(`室数不同(${fp2.rooms}室 vs ${fp.rooms}室)`);
    }
    if (fp.halls != null && fp2.halls != null) {
      if (fp.halls === fp2.halls) { score += 1; reasons.push(`同${fp.halls}厅`); }
      else conflicts.push(`厅数不同(${fp2.halls}厅 vs ${fp.halls}厅)`);
    }
    if (fp.floorTotal != null && fp2.floorTotal != null) {
      if (fp.floorTotal === fp2.floorTotal) { score += 1; reasons.push(`同总楼层${fp.floorTotal}F`); }
      else conflicts.push(`总楼层不同(${fp2.floorTotal}F vs ${fp.floorTotal}F)`);
    }
    if (fp.orient && fp2.orient) {
      if (fp.orient === fp2.orient) { score += 1; reasons.push('同朝向'); }
      else conflicts.push(`朝向不同(${fp2.orient} vs ${fp.orient})`);
    }
    if (fp.year != null && fp2.year != null) {
      if (fp.year === fp2.year) { score += 1; reasons.push(`同年代${fp.year}`); }
      else conflicts.push(`年代不同(${fp2.year} vs ${fp.year})`);
    }
    matches.push({
      listing_key: historyKey(rec),
      platform: rec.platform ?? null,
      listing_id: rec.listing_id ?? null,
      url: rec.url ?? null,
      scanned_at: rec.scanned_at ?? null,
      total_price_wan: rec.listing?.total_price_wan ?? null,
      score,
      confidence: score >= 5 ? 'high' : score >= 3 ? 'medium' : 'low',
      reasons,
      conflicts,
    });
  }
  matches.sort((a, b) => b.score - a.score);
  return { fingerprint: fp, matches };
}

// 实体级历史：把跨平台/跨挂牌键的同源记录归并到一套房子下。
// 无法指纹化（缺小区或面积）的记录按 listing 键单独成实体，不丢弃。
export function buildEntityHistory(records, { staleDays = 14, today = null } = {}) {
  const now = today ?? new Date().toISOString().slice(0, 10);
  const groups = [];
  const recs = [...(records ?? [])].sort((a, b) => String(a.scanned_at ?? '').localeCompare(String(b.scanned_at ?? '')));
  for (const rec of recs) {
    const fp = listingFingerprint(rec);
    const ok = fp.community != null && fp.area != null;
    const target = ok
      ? groups.find((g) => g._fp.community === fp.community && Math.abs(g._fp.area - fp.area) <= 0.6)
      : null;
    if (target) target.records.push(rec);
    else groups.push({ _fp: ok ? fp : null, records: [rec] });
  }
  const out = [];
  for (const g of groups) {
    const byKey = new Map();
    for (const rec of g.records) {
      const key = historyKey(rec);
      if (!byKey.has(key)) byKey.set(key, { key, platform: rec.platform ?? null, listing_id: rec.listing_id ?? null, url: rec.url ?? null, captures: [] });
      byKey.get(key).captures.push({
        date: String(rec.scanned_at ?? ''),
        total_price_wan: rec.listing?.total_price_wan ?? null,
        unit_price: rec.listing?.unit_price ?? null,
        viewings_30d: rec.listing?.viewings_30d ?? null,
        price_change_count: rec.listing?.price_change_count ?? null,
      });
    }
    const listings = [...byKey.values()].map((l) => ({
      ...l,
      captures: l.captures.sort((a, b) => a.date.localeCompare(b.date)),
      first_date: l.captures[0]?.date ?? '',
      last_date: l.captures[l.captures.length - 1]?.date ?? '',
    }));
    const pricePoints = g.records
      .filter((r) => r.listing?.total_price_wan != null)
      .map((r) => ({ date: String(r.scanned_at ?? ''), listing_key: historyKey(r), total_price_wan: r.listing.total_price_wan, unit_price: r.listing?.unit_price ?? null }))
      .sort((a, b) => a.date.localeCompare(b.date));
    const allDates = g.records.map((r) => String(r.scanned_at ?? '')).sort();
    const lastDate = allDates[allDates.length - 1] ?? '';
    const daysSince = lastDate ? Math.max(0, Math.round((new Date(now) - new Date(lastDate)) / 86400000)) : null;
    const platforms = new Set(listings.map((l) => l.platform).filter(Boolean));
    const firstPrice = pricePoints[0]?.total_price_wan ?? null;
    const lastPrice = pricePoints[pricePoints.length - 1]?.total_price_wan ?? null;
    const priceDelta = pricePoints.length >= 2 && firstPrice != null && lastPrice != null
      ? Math.round((lastPrice - firstPrice) * 100) / 100
      : null;
    const last = g.records[g.records.length - 1];
    out.push({
      entity_id: g._fp
        ? `${g._fp.community}~${g._fp.area}㎡~${g._fp.rooms ?? '?'}室~${g._fp.floorTotal ?? '?'}F~${g._fp.year ?? '?'}`
        : `unmatched~${listings[0]?.key ?? 'unknown'}`,
      fingerprint: g._fp,
      community: last?.community ?? '',
      district: last?.district ?? '',
      listings,
      price_points: pricePoints,
      summary: {
        capture_count: g.records.length,
        listing_count: listings.length,
        cross_platform: platforms.size > 1,
        listing_keys: listings.map((l) => l.key),
        first_date: allDates[0] ?? '',
        last_date: lastDate,
        days_since_last_capture: daysSince,
        stale: daysSince == null ? true : daysSince > staleDays,
        price_delta_wan: priceDelta,
        price_delta_pct: (priceDelta != null && firstPrice) ? Math.round((priceDelta / firstPrice) * 1000) / 10 : null,
      },
    });
  }
  out.sort((a, b) => (b.summary.days_since_last_capture ?? 9999) - (a.summary.days_since_last_capture ?? 9999));
  return out;
}

// ---------- 价格历史与房东策略信号（跨时点扫描记录聚合，追加式） ----------

// 追踪键：platform:listing_id（缺 listing_id 时退回 platform:url）
export function historyKey(rec) {
  if (rec?.platform && rec?.listing_id) return `${rec.platform}:${rec.listing_id}`;
  if (rec?.platform && rec?.url) return `${rec.platform}:${rec.url}`;
  return rec?.community || 'unknown';
}

// records: 扫描记录数组（同键多条 = 追加式历史）。staleDays: 实采时效阈值（天）。
// 只读聚合，不修改输入。输出每键时间线 + 摘要（价差/调价增量/带看增量/过期标记）——
// 数值由脚本计算，"房东策略"的解读由 AI 基于这些数值输出并区分事实与推断。
export function buildPriceHistory(records, { staleDays = 14, today = null } = {}) {
  const byKey = new Map();
  for (const rec of records ?? []) {
    const key = historyKey(rec);
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key).push(rec);
  }
  const now = today ?? new Date().toISOString().slice(0, 10);
  const out = [];
  for (const [key, recs] of byKey) {
    const caps = recs
      .map((r) => ({
        date: String(r.scanned_at ?? ''),
        total_price_wan: r.listing?.total_price_wan ?? null,
        unit_price: r.listing?.unit_price ?? null,
        viewings_30d: r.listing?.viewings_30d ?? null,
        price_change_count: r.listing?.price_change_count ?? null,
        community: r.community ?? '',
        district: r.district ?? '',
      }))
      .sort((a, b) => a.date.localeCompare(b.date));
    if (!caps.length) continue;
    const first = caps[0];
    const last = caps[caps.length - 1];
    const multi = caps.length >= 2; // 单次采集无从比较变化，增量一律 null
    const daysSince = last.date
      ? Math.max(0, Math.round((new Date(now) - new Date(last.date)) / 86400000))
      : null;
    const priceDelta = (multi && first.total_price_wan != null && last.total_price_wan != null)
      ? Math.round((last.total_price_wan - first.total_price_wan) * 100) / 100
      : null;
    out.push({
      key,
      community: last.community,
      district: last.district,
      captures: caps,
      summary: {
        capture_count: caps.length,
        first_date: first.date,
        last_date: last.date,
        days_since_last_capture: daysSince,
        stale: daysSince == null ? true : daysSince > staleDays,
        price_delta_wan: priceDelta,
        price_delta_pct: (priceDelta != null && first.total_price_wan)
          ? Math.round((priceDelta / first.total_price_wan) * 1000) / 10
          : null,
        viewings_30d_delta: (multi && first.viewings_30d != null && last.viewings_30d != null)
          ? last.viewings_30d - first.viewings_30d
          : null,
        price_change_count_delta: (multi && first.price_change_count != null && last.price_change_count != null)
          ? last.price_change_count - first.price_change_count
          : null,
      },
    });
  }
  out.sort((a, b) => (b.summary.days_since_last_capture ?? 9999) - (a.summary.days_since_last_capture ?? 9999));
  return out;
}

// ---------- 真实性验证（verifyAuthenticity：把本会话实战验真方法固化为判定表） ----------
//
// 方法论来源（2026-09 实战事故 001/008/009 与解例 011）：
//   C1 URL 实访          capture.url_verified === false → void（重定向占位符）
//   C2 小区存在性        evidence.community_exists === false → void（小区库零命中）
//   C3 挂牌存在性        evidence.listing_seen_in_source === false → void（参数组合在源站不存在）
//   C4 价格 vs 小区均价  |偏差|>20% → suspect；>10% → warn（below/above 纪律）
//   C5 单价一致性        normalize 已查（此处只引用 warnings 外的 listing 自洽）
//   C6 满五 vs 上次交易  房屋年限含「满五」且上次交易距今 <5 年 → conflict（虚标）
//   C7 权属/混居         社区权属含动迁+无政府反证 → warn（带看/产调必核）；
//                        政府公示证伪（matches_subject=false）→ pass；证实 → fail
// provenance 建议：C2/C3 fail → void；C1 fail 或 C6 conflict → suspect；
//            其余全 pass 且核心证据齐 → verified；证据缺失 → suspect（未经交叉验证不予相信）。

const finite_ = (v) => Number.isFinite(v);

export function verifyAuthenticity(record, evidence = {}) {
  const checks = [];
  const add = (id, name, status, detail = '') => checks.push({ id, name, status, detail });
  const L = record?.listing ?? {};
  const cap = record?.capture ?? {};

  // C1 URL 实访
  if (cap.url_verified === false) add('url', 'URL 实访', 'fail', '访问被重定向或拦截——占位符/失效链接');
  else if (cap.url_verified === true) add('url', 'URL 实访', 'pass', '已实际访问并核对内容');
  else add('url', 'URL 实访', 'unknown', '无采集留痕（capture 字段缺失）');

  // C2 小区存在性
  const ce = evidence.community_exists;
  if (ce === false) add('community', '小区存在性', 'fail', '小区库检索零命中——小区实体不存在');
  else if (ce === true) add('community', '小区存在性', 'pass', evidence.community_source || '小区库可检索');
  else add('community', '小区存在性', 'unknown', '未做小区库检索');

  // C3 挂牌存在性
  const ls = evidence.listing_seen_in_source;
  if (ls === false) add('listing', '挂牌存在性', 'fail', '该面积/总价组合在源站真实在售中不存在——挂牌虚构');
  else if (ls === true) add('listing', '挂牌存在性', 'pass', '在真实在售列表中核对到本标的');
  else add('listing', '挂牌存在性', 'unknown', '未对照真实在售列表');

  // C4 价格 vs 小区均价
  const avg = evidence.community_avg_unit_price;
  if (finite_(avg) && avg > 0 && finite_(L.unit_price)) {
    const dev = Math.round(((L.unit_price - avg) / avg) * 1000) / 10;
    if (Math.abs(dev) > 20) add('price_vs_avg', '价格 vs 小区均价', 'fail', `偏差 ${dev}%——远超市场带，真实性高度存疑`);
    else if (Math.abs(dev) > 10) add('price_vs_avg', '价格 vs 小区均价', 'warn', `偏差 ${dev}%——按 below/above 纪律先查原因`);
    else add('price_vs_avg', '价格 vs 小区均价', 'pass', `偏差 ${dev}%，贴近小区均价`);
  } else add('price_vs_avg', '价格 vs 小区均价', 'unknown', '缺小区均价或本套单价');

  // C5 单价一致性
  const implied = finite_(L.total_price_wan) && finite_(L.area_sqm) && L.area_sqm > 0
    ? Math.round((L.total_price_wan * 10000) / L.area_sqm) : null;
  if (implied != null && finite_(L.unit_price)) {
    const dev = Math.abs(implied - L.unit_price) / L.unit_price;
    add('unit_consistency', '单价一致性（总价/面积）', dev > 0.05 ? 'fail' : 'pass',
      dev > 0.05 ? `页面 ${L.unit_price} vs 推导 ${implied}，偏差 ${(dev * 100).toFixed(1)}%` : `${L.unit_price} 元/㎡ 自洽`);
  } else add('unit_consistency', '单价一致性（总价/面积）', 'unknown', '缺少单价或面积');

  // C6 满五 vs 上次交易
  const own = String(L.ownership ?? '');
  const lt = evidence.last_trade_date || L.last_trade_date || '';
  if (/满五/.test(own) && /^\d{4}-\d{2}-\d{2}/.test(lt)) {
    const years = (Date.now() - new Date(lt).getTime()) / (365.25 * 86400000);
    add('fullfive', '满五与上次交易交叉', years >= 5 ? 'pass' : 'fail',
      years >= 5 ? `上次交易 ${lt.slice(0, 10)}，满五成立` : `上次交易 ${lt.slice(0, 10)} 距今不足 5 年——「满五」虚标`);
  } else add('fullfive', '满五与上次交易交叉', 'unknown', '缺少满五标注或上次交易日期');

  // C7 权属/混居（政府公示判别法）
  const co = String(evidence.community_ownership ?? '');
  const gov = evidence.gov_parcel_evidence ?? null;
  if (co && /动迁|安置/.test(co)) {
    if (gov && gov.found) {
      if (gov.matches_subject === false) add('ownership_mix', '回迁混居', 'pass', `政府公示证实周边安置房属「${gov.builder || '第三方'}」项目，非本小区——本体证伪，保留环境减分`);
      else if (gov.matches_subject === true) add('ownership_mix', '回迁混居', 'fail', `政府公示证实本小区含安置房（${gov.parcel_use || ''}）`);
      else add('ownership_mix', '回迁混居', 'warn', '政府公示已找到但对应关系未确认');
    } else add('ownership_mix', '回迁混居', 'warn', `小区权属含动迁/安置成分（${co}）——需政府公示或产调判别本体构成`);
  } else if (co) add('ownership_mix', '回迁混居', 'pass', `小区权属「${co}」，无动迁成分`);
  else add('ownership_mix', '回迁混居', 'unknown', '未采集小区权属口径');

  // ── provenance 建议判定 ──
  const byId = Object.fromEntries(checks.map((c) => [c.id, c]));
  const coreFail = ['community', 'listing'].some((k) => byId[k].status === 'fail');
  const anyFail = checks.some((c) => c.status === 'fail');
  const evidenceUsed = [ce, ls, avg, co].some((v) => v != null && v !== '') || gov != null;
  let provenance;
  if (byId.community.status === 'fail' || byId.listing.status === 'fail') provenance = 'void';
  else if (byId.url.status === 'fail' || byId.fullfive.status === 'fail' || byId.price_vs_avg.status === 'fail') provenance = 'suspect';
  else if (!evidenceUsed) provenance = 'suspect'; // 未经交叉验证不予相信
  else if (anyFail) provenance = 'suspect';
  else if (checks.every((c) => c.status === 'pass')) provenance = 'verified';
  else provenance = 'suspect'; // 有 unknown 项：宁存疑不乐观

  return { checks, provenance_suggestion: provenance };
}

// ---------- 定价交叉验证（deep module：调用者只学 finalizeRecord） ----------

const finite = (v) => Number.isFinite(v);

// 单价优先，缺单价时由 总价/面积 推导；反之亦然
const unitOf = (t) => (finite(t?.unit_price) ? t.unit_price
  : finite(t?.total_price_wan) && finite(t?.area_sqm) && t.area_sqm > 0
    ? Math.round((t.total_price_wan * 10000) / t.area_sqm) : null);
const totalOf = (t) => (finite(t?.total_price_wan) ? t.total_price_wan
  : finite(t?.unit_price) && finite(t?.area_sqm) && t.area_sqm > 0
    ? Math.round(t.unit_price * t.area_sqm) / 100 : null);

function median(nums) {
  const s = [...nums].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : Math.round((s[mid - 1] + s[mid]) / 2);
}

// 扫描记录定稿唯一入口：归一化 → 定价交叉验证，一次完成。
// （旧"先 normalize 才能 crosscheck"的顺序约定由本 interface 吸收，调用者无需知道。）
export function finalizeRecord(raw) {
  const { record, warnings } = normalizeRecord(raw);
  crosscheckRecord(record);
  return { record, warnings };
}

// 定价锚点方法论：
//   口径优先单价（元/㎡），挂牌无单价时降级总价口径并在 note 声明；
//   锚点 = 最高可靠度档内、deal_date 最近的 ≤5 条的口径中位数（同口径两侧对比）；
//   单样本显式降置信度；锚点档位与样本数写进 anchor，不再藏在 note 措辞里。
export function crosscheckRecord(rec) {
  const L = rec?.listing ?? {};
  rec.crosscheck = { anchor: null, listing_vs_anchor_pct: null, verdict: 'not_enough_data', note: '' };
  const listingUnit = unitOf(L);
  const useUnit = listingUnit != null;
  const listingVal = useUnit ? listingUnit : totalOf(L);
  if (listingVal == null) {
    rec.crosscheck.note = '挂牌价缺失（单价与总价均不可得）——不猜测';
    return rec;
  }
  const tierOf = (t) => Math.max(0, RELIABILITY.indexOf(t.reliability ?? '未核实'));
  const samples = (rec.transactions ?? [])
    .map((t) => ({ tier: tierOf(t), date: String(t.deal_date ?? ''), val: useUnit ? unitOf(t) : totalOf(t) }))
    .filter((s) => s.val != null);
  if (!samples.length) {
    rec.crosscheck.note = '无价格可取的可比成交——成交价进待核实清单，不猜测';
    return rec;
  }
  const best = Math.min(...samples.map((s) => s.tier));
  const anchorSet = samples.filter((s) => s.tier === best)
    .sort((a, b) => b.date.localeCompare(a.date)).slice(0, 5);
  const vals = anchorSet.map((s) => s.val);
  const anchorVal = median(vals);
  const tier = RELIABILITY[best];
  const pct = Math.round(((listingVal - anchorVal) / anchorVal) * 1000) / 10;
  const rule = VERDICT_THRESHOLDS.find((r) => pct <= r.max);
  const notes = [];
  if (!useUnit) notes.push('挂牌缺单价，降级为总价口径');
  if (anchorSet.length === 1) notes.push('单样本锚点，置信度低');
  if (tier !== '成交数据') notes.push(`锚点档位为「${tier}」，结论仅参考`);
  rec.crosscheck = {
    anchor: {
      tier,
      n_samples: anchorSet.length,
      range_pct: anchorSet.length > 1 ? Math.round(((Math.max(...vals) - Math.min(...vals)) / anchorVal) * 1000) / 10 : null,
    },
    listing_vs_anchor_pct: pct,
    verdict: rule.verdict,
    note: [rule.note, ...notes].join('；'),
  };
  return rec;
}
