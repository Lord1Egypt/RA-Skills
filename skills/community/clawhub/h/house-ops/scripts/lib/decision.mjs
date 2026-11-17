// decision.mjs — 决策分层唯一实现（四档 pill / 状态标签 / 地图标记档 / 结论中文标签）。
// 语义 SoT：本文件。此前同语义散落 map.mjs（排除正则）、map-html.mjs 页面 JS（decisionInfo）、
// dashboard.mjs（CONCLUSION_LABEL，曾漏 strong_recommend 造成漂移）；消费方一律经本 interface。
//
// 分层规则（watchlist 与 evaluate 口径）：
//   pass（高代价/硬伤档）：hard_dq_hit ‖ score_global < 3.5 ‖ conclusion = pass ‖ 备注含 排除/弃购
//   rec （第一梯队）     ：非 pass ∧ (score_global ≥ 4.0 ‖ conclusion ∈ REC_CONCLUSIONS)
//   cond（备选对照）     ：其余
// 真实性（ADR-0002）不改变分层，只在展示标签上合成（suspect/legacy → 「待验真」）。

export const REC_CONCLUSIONS = ['worth_viewing', 'strong_buy', 'strong_recommend'];
export const EXCLUDE_LINE = 3.5;
export const REC_LINE = 4.0;

// watchlist 备注语义：用户亲手写的「排除/弃购」是人做的决定，等效一票否决
export function isUserExcluded(note = '') {
  return /排除|弃购/.test(String(note));
}

// 风险档展示标签：接受英文枚举（Machine Summary）与中文（watchlist 列）两种输入
export function riskLabel(risk) {
  const r = String(risk ?? '').trim();
  if ({ low: 1, 低: 1 }[r]) return '低';
  if ({ caution: 1, 注意: 1 }[r]) return '注意';
  if ({ high: 1, 高: 1, 高风险: 1 }[r]) return '高';
  return null;
}

// conclusion 枚举中文 SoT（dashboard 曾漏 strong_recommend —— 回归用例见 selftest）
export function conclusionLabel(conclusion) {
  const labels = {
    strong_recommend: '强烈推荐',
    strong_buy: '强推',
    worth_viewing: '值得看',
    conditional: '看情况',
    pass: '放弃',
  };
  return labels[conclusion] ?? conclusion ?? '';
}

// 分层唯一入口。输入：Machine Summary ∪ watchlist 合并后的房源字段。
// 输出：{ tier: 'rec'|'cond'|'pass', markerCls, tag, tagCls, risk }
export function decide(listing = {}) {
  const score = listing.score_global;
  const excluded = Boolean(listing.hard_dq_hit)
    || (score != null && score < EXCLUDE_LINE)
    || listing.conclusion === 'pass'
    || Boolean(listing.user_excluded);
  const rec = !excluded && (
    (score != null && score >= REC_LINE)
    || REC_CONCLUSIONS.includes(listing.conclusion)
  );
  const tier = excluded ? 'pass' : rec ? 'rec' : 'cond';
  const unverified = listing.authenticity === 'suspect' || listing.authenticity === 'legacy';

  const markerCls = tier === 'pass' ? 'low' : tier === 'rec' ? 'high' : 'mid';
  let tag;
  if (tier === 'pass') tag = '高代价/已排除';
  else if (unverified) tag = '待验真';
  else tag = tier === 'rec' ? '可约看' : '备选对照';
  const tagCls = tier === 'pass' ? 'status-red' : unverified ? 'status-amber' : tier === 'rec' ? 'status-green' : 'status-blue';

  return { tier, markerCls, tag, tagCls, risk: riskLabel(listing.risk_tier) };
}
