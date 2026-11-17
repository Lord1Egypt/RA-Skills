// lianjia.mjs — 链家（lianjia.com）。与贝壳同集团、URL 语法一致，走共用工厂。

import { makeKeGroup } from './_ke-group.mjs';

export default makeKeGroup({
  id: 'lianjia',
  name: '链家',
  domain: 'lianjia.com',
  groupNote: '链家直营口径，房源核验码与真实度在主流平台中最规范；成交明细 /chengjiao/ 是同小区成交锚点的首选来源之一。',
});
