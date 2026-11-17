/**
 * engine/light/ledger.mjs — 轻量后端的审核台账
 *
 * 语义与 evolver `review` 对齐：approve / quarantine / list。
 * fail-closed 不变量：只有台账中 state **等于** "approved" 的 asset 才可被注入
 * （读取侧见 store.approvedAssetIds；判定统一走 store.isApprovedState，禁止子串匹配）。
 */
import { appendReview, readGenes, readReview, assetIdOf, isApprovedState } from './store.mjs';

/** 审核通过（接受 gene_id 或 asset_id） */
export function approve(idOrAssetId) {
  const assetId = String(idOrAssetId).startsWith('sha256:') ? String(idOrAssetId) : assetIdOf(String(idOrAssetId));
  if (!assetId) return { ok: false, reason: `找不到 gene: ${idOrAssetId}` };
  // 0.18.1：幂等判定改 **LWW**（最后一条状态）——旧 `.some()` 只要历史上有 approved 就跳过，
  // 会让「曾被批准→后被隔离」的基因永远无法重新批准（0.14.4 LWW 修复清单遗漏的第 4 处，
  // 2026-10-11 实测：5 条 approve 静默无效假 ✓）。
  let lastState = null;
  for (const r of readReview()) { if (r.assetId === assetId) lastState = r.state; }
  // 0.31 安全修复：精确比对。旧写法 `includes('approv')` 遇到 'unapproved'/'disapproved'
  // 会判为 alreadyApproved ⇒ **真正的 approve 被静默跳过**（写入侧假 ✓）。
  if (isApprovedState(lastState)) return { ok: true, assetId, alreadyApproved: true };
  appendReview({ assetId, state: 'approved', reason: 'approved via light ledger' });
  return { ok: true, assetId, alreadyApproved: false };
}

/** 隔离（起草态，等价 evolver 的 quarantined） */
export function quarantine(idOrAssetId, reason = 'drafted — review before use') {
  const assetId = String(idOrAssetId).startsWith('sha256:') ? String(idOrAssetId) : assetIdOf(String(idOrAssetId));
  if (!assetId) return { ok: false, reason: `找不到 gene: ${idOrAssetId}` };
  appendReview({ assetId, state: 'quarantined', reason });
  return { ok: true, assetId };
}

/** 台账列表（附带基因摘要，便于人工审阅） */
export function list() {
  const genes = new Map(readGenes().map((g) => [g.asset_id, g]));
  const latest = new Map();
  for (const r of readReview()) latest.set(r.assetId, r); // 后写覆盖前写 = 最新态
  return [...latest.values()].map((r) => {
    const g = genes.get(r.assetId);
    return {
      assetId: r.assetId,
      state: r.state,
      at: r.at,
      id: g?.id ?? null,
      category: g?.category ?? null,
      strategy: (g?.strategy?.[0] ?? '').slice(0, 120),
    };
  });
}
