import assert from 'node:assert/strict';
import test from 'node:test';

import {
  coerceDateRangeValue,
  coerceNodeValue,
  coerceNumberUnitValue,
  formatDateForDisplay,
  parseDateParts
} from '../scripts/answer-coercion.mjs';
import {
  areaLevelOf,
  buildAreaIndex,
  resolveAreaPath,
  splitRegionText
} from '../scripts/area-resolver.mjs';
import { applyAnswersToNodes } from '../scripts/interaction-normalizer.mjs';

const AREAS = [
  { id: 'yn', name: '云南省', parentId: null },
  { id: 'km', name: '昆明市', parentId: 'yn' },
  { id: 'wh', name: '五华区', parentId: 'km' },
  { id: 'qj', name: '曲靖市', parentId: 'yn' },
  { id: 'sc', name: '四川省', parentId: null },
  { id: 'cd', name: '成都市', parentId: 'sc' }
];

function dateNode(overrides = {}) {
  return {
    id: 'birth',
    component: '10',
    title: '出生年月',
    config: { dateFormat: 'yyyy-MM', required: true },
    ...overrides
  };
}

function unixOf(year, month, day, hour = 0, minute = 0) {
  return String(Math.floor(new Date(year, month - 1, day, hour, minute, 0, 0).getTime() / 1000));
}

test('日期题提交 unix 秒而不是日期字符串', () => {
  const node = dateNode();
  // 前端 QDate 的 value 是 dayjs(...).unix()，提交 "1969-05-20" 会让后端得到 Invalid Date。
  assert.equal(coerceNodeValue(node, 'date', '1969-05-20'), unixOf(1969, 5, 1));
  assert.equal(coerceNodeValue(node, 'date', '1969年5月'), unixOf(1969, 5, 1));
  assert.equal(coerceNodeValue(node, 'date', '196905'), unixOf(1969, 5, 1));
});

test('yyyy-MM 的日期题把日固定为 1', () => {
  assert.equal(coerceNodeValue(dateNode(), 'date', '1991-11-08'), unixOf(1991, 11, 1));
});

test('完整年月日的日期题保留日', () => {
  const node = dateNode({ config: { required: true } });
  assert.equal(coerceNodeValue(node, 'date', '1991-11-08'), unixOf(1991, 11, 8));
});

test('component 11 的日期题保留时分', () => {
  const node = dateNode({ component: '11', config: { required: true } });
  assert.equal(coerceNodeValue(node, 'date', '2024-03-05 14:30'), unixOf(2024, 3, 5, 14, 30));
});

test('已经是 unix 秒的日期不被二次转换', () => {
  const node = dateNode({ config: { required: true } });
  const seconds = unixOf(1991, 11, 8);
  assert.equal(coerceNodeValue(node, 'date', seconds), seconds);
});

test('无法解析的日期原样返回，交给后端报错', () => {
  assert.equal(coerceNodeValue(dateNode(), 'date', '去年冬天'), '去年冬天');
  assert.equal(parseDateParts(''), null);
});

test('超出 1900 到 2200 的日期不提交', () => {
  const node = dateNode({ config: { required: true } });
  assert.equal(coerceNodeValue(node, 'date', '1800-01-01'), '1800-01-01');
});

test('日期区间题提交带 start 和 end 的对象', () => {
  const node = { id: 'range', component: '8', config: {} };
  const value = coerceDateRangeValue(node, ['2024-01-01', '2024-03-31']);
  assert.equal(value.start, Number(unixOf(2024, 1, 1)));
  assert.equal(value.end, Number(unixOf(2024, 3, 31)));
  assert.equal(value.allday, 91);
  assert.equal(value.month, 3);
  assert.equal(value.year, 0);
});

test('日期区间题接受“至”分隔的写法', () => {
  const node = { id: 'range', component: '8', config: {} };
  const value = coerceDateRangeValue(node, '2024-01-01 至 2024-03-31');
  assert.equal(value.start, Number(unixOf(2024, 1, 1)));
});

test('数值加单位题提交 value 和 unit 对象', () => {
  const node = { id: 'unit', component: '25', config: { nameUnit: '年,月,天' } };
  assert.deepEqual(coerceNumberUnitValue(node, '15年'), { value: 15, unit: '年' });
  assert.deepEqual(coerceNumberUnitValue(node, 20), { value: 20, unit: '年' });
});

test('金额题仍然提交纯数字', () => {
  const node = { id: 'money', component: '9', config: {} };
  assert.equal(coerceNodeValue(node, 'money', '4,300元'), 4300);
});

test('日期回显为人类可读文本', () => {
  const node = dateNode();
  assert.equal(formatDateForDisplay(node, unixOf(1969, 5, 1)), '1969-05');
});

test('地区文本按层级拆分', () => {
  assert.deepEqual(splitRegionText('云南省昆明市五华区'), ['云南省', '昆明市', '五华区']);
  assert.deepEqual(splitRegionText('云南省昆明市'), ['云南省', '昆明市']);
});

test('地区题解析成对应层级的地区 id', () => {
  const index = buildAreaIndex(AREAS);
  assert.equal(resolveAreaPath(index, '云南省昆明市', 2).id, 'km');
  assert.equal(resolveAreaPath(index, '云南省', 1).id, 'yn');
  assert.equal(resolveAreaPath(index, '云南省昆明市五华区', 3).id, 'wh');
});

test('地区名称缺少后缀也能匹配', () => {
  const index = buildAreaIndex(AREAS);
  assert.equal(resolveAreaPath(index, '云南昆明', 2).id, 'km');
});

test('地区层级不足时返回该层级的真实候选', () => {
  const index = buildAreaIndex(AREAS);
  const outcome = resolveAreaPath(index, '云南省', 2);
  assert.equal(outcome.ok, false);
  assert.equal(outcome.reason, 'INCOMPLETE');
  assert.equal(outcome.level, 2);
  assert.deepEqual(outcome.candidates.map(area => area.name), ['昆明市', '曲靖市']);
});

test('地区匹配不到时不把原文当作答案', () => {
  const index = buildAreaIndex(AREAS);
  const outcome = resolveAreaPath(index, '不存在省', 1);
  assert.equal(outcome.ok, false);
  assert.equal(outcome.reason, 'NOT_MATCHED');
});

test('areaLevel 缺省按省市两级处理', () => {
  assert.equal(areaLevelOf({ config: {} }), 2);
  assert.equal(areaLevelOf({ config: { areaLevel: 1 } }), 1);
  assert.equal(areaLevelOf({ config: { areaLevel: 3 } }), 3);
});

test('applyAnswersToNodes 按组件配置写入取值', () => {
  const nodes = [dateNode()];
  const [applied] = applyAnswersToNodes(nodes, { birth: '1969-05-20' });
  assert.equal(applied.value, unixOf(1969, 5, 1));
  assert.equal(applied.edit, true);
});
