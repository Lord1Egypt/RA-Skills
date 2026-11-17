// 5i5j.mjs — 我爱我家（5i5j.com）。城市子域名：bj/sh/nj/tj 等。

import { COMMON_LISTING_FIELDS } from './_fields.mjs';
import { liftMobileCity } from './_registry.mjs';

const RE = /^https?:\/\/([a-z0-9]+)\.5i5j\.com\/?(.*)$/i;

export default {
  id: '5i5j',
  name: '我爱我家',
  domains: ['5i5j.com'],
  fields: [...COMMON_LISTING_FIELDS, '经纪人/门店信息'],
  transaction: {
    pattern: null,
    reliability: '挂牌数据',
    coverage: '无公开成交明细（部分城市有成交参考页，可得性与口径需核实）；估算行情最高按「挂牌数据」档',
  },
  notes: [
    '直营门店口径为主，部分城市覆盖有限——价格建议与链家/贝壳成交页或政务源交叉验证',
    '仅限个人购房研究用途：遵守平台条款，不批量抓取、不公开再分发页面内容',
  ],
  detect(url) {
    const m = RE.exec(url.trim());
    if (!m) return null;
    let [cityCode, path = ''] = [m[1], m[2] ?? ''];
    path = path.replace(/^\/+/, '');
    [cityCode, path] = liftMobileCity(cityCode, path);
    let pageType = 'unknown';
    let listingId = null;
    let im;
    if ((im = /^ershoufang\/(\w+)\.html?/i.exec(path))) {
      pageType = 'listing';
      listingId = im[1];
    } else if (/^ershoufang/i.test(path)) {
      pageType = 'search';
    } else if (/^(community|xiaoqu)/i.test(path)) {
      pageType = 'community';
    }
    return { page_type: pageType, city_code: cityCode, listing_id: listingId };
  },
};
