/**
 * window-attribution-receipt.js — 跨窗口归因收据（Window Attribution Receipt）
 *
 * 对齐 microsoft/autogen#7888 kawacukennedy 固定的 straddling fixture schema：
 *   { turn_id, window_start, window_end, outcome, effective, is_straddling, straddle, commitment }
 *
 * 核心语义（与 #7888 讨论一致）：
 *   - effective = 回合「开始所在」的窗口（start window），不做事后归因
 *   - straddle.overlap_exposure = 重叠窗口被显式暴露，但不 claim attribution
 *   - 每个收据自带完整性字段，防「读取时偏好毒化快照」
 *
 * 使用：const { WindowAttributionReceipt } = require('./src/core/window-attribution-receipt.js')
 */
'use strict';

class WindowAttributionReceipt {
  constructor(projectRoot) {
    this.projectRoot = projectRoot || process.cwd();
    this._receipts = new Map(); // turn_id -> receipt
    this.VERSION = '0.1.0';
  }

  /**
   * 创建收据
   * @param {Object} opts { turn_id, window_start, window_end, outcome, effective, is_straddling, straddle, commitment }
   */
  create(opts = {}) {
    const { turn_id, window_start, window_end, outcome = 'completed', effective, is_straddling = false, straddle = null, commitment = null } = opts;
    if (!turn_id) return { ok: false, error: 'turn_id required' };
    if (window_start == null || window_end == null) return { ok: false, error: 'window_start/window_end required' };

    const receipt = {
      schema: 'window-attribution-receipt@0.1.0',
      turn_id,
      window_start,
      window_end,
      outcome,
      effective: effective != null ? effective : window_start, // 默认归因到开始窗口
      is_straddling,
      straddle: straddle || null,
      commitment: commitment || null,
      created_at: Date.now(),
      digest: null,
    };
    receipt.digest = this._digest(receipt);
    this._receipts.set(turn_id, receipt);
    return { ok: true, receipt };
  }

  _digest(r) {
    const crypto = require('crypto');
    const payload = JSON.stringify({
      turn_id: r.turn_id,
      window_start: r.window_start,
      window_end: r.window_end,
      outcome: r.outcome,
      effective: r.effective,
      is_straddling: r.is_straddling,
      straddle: r.straddle,
      commitment: r.commitment,
    });
    return crypto.createHash('sha256').update(payload).digest('hex');
  }

  /**
   * 验证外部收据（如 kawacukennedy 的 fixture JSON）
   * 返回 { ok, valid, findings[] }
   */
  verifyReceipt(receipt) {
    const findings = [];
    if (!receipt || typeof receipt !== 'object') {
      return { ok: false, valid: false, findings: [{ level: 'error', msg: 'receipt not an object' }] };
    }
    // 1. 必填字段
    for (const f of ['turn_id', 'window_start', 'window_end', 'outcome', 'effective']) {
      if (receipt[f] == null) findings.push({ level: 'error', msg: `missing ${f}` });
    }
    // 2. effective 必须是开始窗口（跨窗口归因核心语义）
    if (receipt.effective != null && receipt.effective !== receipt.window_start && !receipt.is_straddling) {
      findings.push({ level: 'error', msg: 'effective != window_start on non-straddling receipt — mis-attribution' });
    }
    // 3. outcome 合法值
    if (receipt.outcome != null && !['completed', 'failed', 'partial', 'revoked'].includes(receipt.outcome)) {
      findings.push({ level: 'error', msg: `invalid outcome: ${receipt.outcome}` });
    }
    // 4. straddle 结构（若声明）
    if (receipt.is_straddling) {
      if (!receipt.straddle || !receipt.straddle.second_window_start || !receipt.straddle.second_window_end) {
        findings.push({ level: 'error', msg: 'is_straddling=true but straddle.second_window missing' });
      }
      if (receipt.straddle && receipt.straddle.overlap_exposure == null) {
        findings.push({ level: 'warn', msg: 'straddle.overlap_exposure not set' });
      }
    }
    // 5. 完整性校验（digest 若存在）
    if (receipt.digest) {
      const recomputed = this._digest(receipt);
      if (recomputed !== receipt.digest) {
        findings.push({ level: 'error', msg: 'digest mismatch — receipt tampered or re-attributed' });
      }
    }
    return {
      ok: findings.filter(f => f.level === 'error').length === 0,
      valid: findings.filter(f => f.level === 'error').length === 0,
      findings,
    };
  }

  /** 取回收据 */
  get(turn_id) {
    return this._receipts.get(turn_id) || null;
  }

  /** 统计 */
  getStats() {
    const all = [...this._receipts.values()];
    return {
      total: all.length,
      completed: all.filter(r => r.outcome === 'completed').length,
      partial: all.filter(r => r.outcome === 'partial').length,
      failed: all.filter(r => r.outcome === 'failed').length,
      revoked: all.filter(r => r.outcome === 'revoked').length,
      straddling: all.filter(r => r.is_straddling).length,
    };
  }
}

module.exports = { WindowAttributionReceipt };
