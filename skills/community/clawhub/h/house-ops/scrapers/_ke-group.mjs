// _ke-group.mjs — 链家/贝壳共用模块工厂：两者同集团，Web 端 URL 语法一致
//（{城市}.lianjia.com / {城市}.ke.com，城市子域名如 sh/bj/gz），字段清单与成交页同源。
// `_` 前缀 = 共享工具，不会被注册表当作平台模块加载。

import { COMMON_LISTING_FIELDS } from './_fields.mjs';
import { liftMobileCity } from './_registry.mjs';

export function makeKeGroup({ id, name, domain, groupNote }) {
  const escaped = domain.replace(/\./g, '\\.');
  const RE = new RegExp(`^https?://([a-z0-9-]+)\\.${escaped}/?(.*)$`, 'i');
  return {
    id,
    name,
    domains: [domain],
    fields: [
      ...COMMON_LISTING_FIELDS,
      '房源核验码', '近 30 日带看次数与关注人数', '满五唯一/房本年限', '上次交易日期',
      '抵押/租约/户口披露', '小区均价与流动性（在售套数/近 90 天成交/近 30 天带看）',
    ],
    transaction: {
      pattern: `https://{城市}.${domain}/chengjiao/`,
      reliability: '成交数据',
      coverage: '已成交明细（成交价/成交日期/挂牌周期/调价次数），覆盖该集团经手的成交，非全市全量；取同小区最近 3-5 条可作成交锚点',
    },
    notes: [
      '反爬较强：无 cookie 的抓取可能被拦——按 modes/scan.md 降级链路处理（快照/搜索/用户粘贴），不绕验证码',
      groupNote,
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
      if ((im = /^ershoufang\/(\d+)\.html?/i.exec(path))) {
        pageType = 'listing';
        listingId = im[1];
      } else if (/^ershoufang/i.test(path)) {
        pageType = 'search';
      } else if ((im = /^chengjiao\/(\d+)\.html?/i.exec(path))) {
        pageType = 'transaction';
        listingId = im[1];
      } else if (/^chengjiao/i.test(path)) {
        pageType = 'transaction_list';
      } else if ((im = /^xiaoqu\/([^/]+)/i.test(path))) {
        pageType = 'community';
        listingId = im[1];
      } else if (/^loupan/i.test(path)) {
        pageType = 'new_home';
      }
      return { page_type: pageType, city_code: cityCode, listing_id: listingId };
    },
  };
}
