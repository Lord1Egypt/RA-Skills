// anjuke.mjs — 安居客（anjuke.com）。城市子域名为全拼（shanghai/beijing/suzhou…）。

import { COMMON_LISTING_FIELDS } from './_fields.mjs';
import { liftMobileCity } from './_registry.mjs';

const RE = /^https?:\/\/([a-z]+)\.anjuke\.com\/?(.*)$/i;

export default {
  id: 'anjuke',
  name: '安居客',
  domains: ['anjuke.com'],
  fields: [...COMMON_LISTING_FIELDS, '小区均价与同小区在售量', '经纪人/门店信息'],
  transaction: {
    pattern: null,
    reliability: '挂牌数据',
    coverage: '无公开成交明细；「查房价」(/market/) 频道是板块/小区估算均价，档位最高按「挂牌数据」，不得当成交价引用',
  },
  notes: [
    '反爬明显（验证码/跳转）——失败按 modes/scan.md 降级链路处理，不绕验证码',
    '经纪人自主发布，低价引流盘比例高——价格异常一律与链家/贝壳成交页或政务源交叉验证后再进报告',
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
    if ((im = /^prop\/view\/(A?\w+)/i.exec(path))) {
      pageType = 'listing';
      listingId = im[1];
    } else if (/^community/i.test(path)) {
      pageType = 'community';
    } else if (/^market/i.test(path)) {
      pageType = 'market';
    } else if (/^(ershoufang|sale)/i.test(path)) {
      pageType = 'search';
    }
    return { page_type: pageType, city_code: cityCode, listing_id: listingId };
  },
};
