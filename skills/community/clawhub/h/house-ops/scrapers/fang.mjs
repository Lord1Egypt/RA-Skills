// fang.mjs — 房天下（fang.com）。二手房在 esf.{city}.fang.com，新房在 newhouse.{city}.fang.com。

import { COMMON_LISTING_FIELDS } from './_fields.mjs';

export default {
  id: 'fang',
  name: '房天下',
  domains: ['fang.com'],
  fields: [...COMMON_LISTING_FIELDS, '小区均价（估算口径）'],
  transaction: {
    pattern: null,
    reliability: '挂牌数据',
    coverage: '无公开成交明细；「查房价」频道为估算口径，最高按「挂牌数据」档',
  },
  notes: [
    '假房源/低价引流盘比例较高——价格必须与链家/贝壳成交页或政务源交叉验证后才可进报告',
    '仅限个人购房研究用途：遵守平台条款，不批量抓取、不公开再分发页面内容',
  ],
  detect(url) {
    let u;
    try {
      u = new URL(url.trim());
    } catch {
      return null;
    }
    if (!/(^|\.)fang\.com$/i.test(u.hostname)) return null;
    const labels = u.hostname.replace(/\.fang\.com$/i, '').split('.');
    // 城市子域顺序不定：esf.sh.fang.com 与 sh.esf.fang.com（证书匹配 *.esf.fang.com，2026-09 实测）都存在
    const section = labels.find((l) => l === 'esf' || l === 'newhouse') ?? '';
    const cityCode = labels.find((l) => l !== 'esf' && l !== 'newhouse') ?? labels[labels.length - 1];
    const path = u.pathname;
    let pageType = 'unknown';
    let listingId = null;
    if (section === 'esf') {
      // 详情语法多变：/house/xxx.htm、/house-a015/f_047_1.htm、/chushou/3_511432907.htm（2026-09 实测）
      const seg = /\/(?:house[^/]*|chushou)\/([^/]+?\.htm)$/i.exec(path) || /\/house\/([^/]+?)\.htm/i.exec(path);
      if (seg) {
        pageType = 'listing';
        listingId = seg[1].replace(/\.htm$/i, '');
      } else {
        pageType = 'search';
      }
    } else if (section === 'newhouse') {
      const lp = /\/loupan\/([^/]+)/i.exec(path);
      if (lp) {
        pageType = 'new_home';
        listingId = lp[1];
      } else {
        pageType = 'search';
      }
    }
    return { page_type: pageType, city_code: cityCode, listing_id: listingId };
  },
};
