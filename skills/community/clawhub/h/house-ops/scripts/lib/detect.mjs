// detect.mjs — `scan.mjs detect` 的输出整形（纯函数，可 golden 测试）。
// 设计要点：平台负载（fields / transaction / notes）每平台只输出一次，URL 清单挂在平台下——
// 5 条贝壳链接不再灌 5 份相同的提取清单（issue #3：token 经济）。

import { SCAN_BUDGET } from '../../scrapers/_fields.mjs';

/**
 * @param {Array<object>} items — 每条 URL 的识别结果，形状：
 *   { url, platform, name, page_type, city_code, listing_id, fields, transaction, notes, hint }
 * @returns {{ url_count: number, over_budget: boolean, max_urls_per_call: number, platforms: Array<object> }}
 */
export function groupDetections(items, { maxUrls = SCAN_BUDGET.max_urls_per_call } = {}) {
  const list = items ?? [];
  const order = [];
  const byPlatform = new Map();
  for (const it of list) {
    const key = it?.platform ?? 'generic';
    if (!byPlatform.has(key)) {
      byPlatform.set(key, {
        platform: key,
        name: it?.name ?? key,
        fields: it?.fields ?? [],
        transaction: it?.transaction ?? null,
        notes: it?.notes ?? [],
        ...(it?.hint ? { hint: it.hint } : {}),
        url_count: 0,
        urls: [],
      });
      order.push(key);
    }
    const g = byPlatform.get(key);
    const { url, page_type, city_code, listing_id } = it ?? {};
    g.urls.push({ url, page_type: page_type ?? 'unknown', city_code: city_code ?? null, listing_id: listing_id ?? null });
    g.url_count = g.urls.length;
  }
  return {
    url_count: list.length,
    max_urls_per_call: maxUrls,
    over_budget: list.length > maxUrls,
    platforms: order.map((k) => byPlatform.get(k)),
  };
}

// 超批量的 stderr 提醒文本（单次调用链接数上限由 SCAN_BUDGET 定义）
export function overBudgetWarning(count, maxUrls = SCAN_BUDGET.max_urls_per_call) {
  return `⚠️  本次 ${count} 条链接 > 单次调用上限 ${maxUrls} 条——超出部分请分批再跑（联网预算：每条 ≤${SCAN_BUDGET.fetches_per_listing} 次、单次调用合计 ≤${SCAN_BUDGET.fetches_per_call} 次）`;
}
