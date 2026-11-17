// beike.mjs — 贝壳找房（ke.com）。与链家同集团、URL 语法一致，走共用工厂；
// 拆成独立文件便于单独禁用/修补单个平台（career-ops providers 约定）。

import { makeKeGroup } from './_ke-group.mjs';

export default makeKeGroup({
  id: 'beike',
  name: '贝壳找房',
  domain: 'ke.com',
  groupNote: '贝壳/链家同集团：同一房源常双平台同价挂牌；贝壳覆盖加盟门店房源，面通常比链家直营更广。',
});
