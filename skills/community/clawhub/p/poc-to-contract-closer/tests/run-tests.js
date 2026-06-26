const assert = require('assert');
const { assessClosing, assessCooling, generateReport, parseArgs } = require('../src/generator');

function includesAll(text, fragments) {
  for (const fragment of fragments) {
    assert(text.includes(fragment), `expected output to include: ${fragment}\n\n${text}`);
  }
}

const missingProcurement = generateReport({
  passRate: 93,
  p0: 0,
  p1: 2,
  acceptedValue: '客服解决率提升已被 champion 认可',
  decisionMaker: '业务负责人已看过 recap',
  silenceDays: 3,
});
includesAll(missingProcurement, [
  '采购路径缺失',
  '招投标/单一来源/框架协议/续约/比价路径',
  'Cooling Threshold',
  '客户沉默达到 3 天',
  'procurement path unknown',
  'Quote now? no',
]);

const ready = generateReport({
  passRate: 94,
  p0: 0,
  p1: 1,
  p2: 3,
  acceptedValue: '核心问答准确率达标',
  decisionMaker: '经济买方已确认',
  procurementPath: '比价采购',
  launchWindow: '6月试点上线',
  silenceDays: 1,
});
includesAll(ready, [
  'Status: Ready',
  'Procurement Path',
  'Closing Window',
  'Cooling Threshold',
  'Procurement path: 比价采购',
  'Closing window: 6月试点上线',
  'Quote now? yes',
  '比价采购',
]);

const blocked = assessClosing({ passRate: 88, p0: 1, procurementPath: '招投标' });
assert.strictEqual(blocked.returnToWarRoom, true);
assert.strictEqual(blocked.status, 'Not ready');
const cooled = assessClosing({
  passRate: 94,
  p0: 0,
  acceptedValue: '核心价值已确认',
  decisionMaker: '经济买方已确认',
  procurementPath: '比价采购',
  launchWindow: '6月试点上线',
  silenceDays: 7,
});
assert.strictEqual(cooled.status, 'Nearly ready');
assert.strictEqual(assessCooling(14).status, 'Blocked');
assert(assessCooling(7).gap.includes('closing 动能正在丢失'));

const stalled = generateReport({
  passRate: 94,
  p0: 0,
  acceptedValue: '核心价值已确认',
  decisionMaker: '经济买方已确认',
  procurementPath: '框架协议',
  launchWindow: 'Q3上线',
  silenceDays: 14,
});
includesAll(stalled, [
  'Status: Blocked',
  'Return to `tob-poc-war-room`? yes',
  '客户沉默达到 14 天',
  'Quote now? no',
]);

const args = parseArgs([
  'node',
  'generator.js',
  '--pass-rate',
  '93',
  '--p0',
  '0',
  '--procurement-path',
  '框架协议',
  '--launch-window',
  'Q3上线',
  '--silence-days',
  '7',
]);
assert.strictEqual(args.passRate, 93);
assert.strictEqual(args.p0, 0);
assert.strictEqual(args.procurementPath, '框架协议');
assert.strictEqual(args.launchWindow, 'Q3上线');
assert.strictEqual(args.silenceDays, 7);

console.log('poc-to-contract-closer tests passed');
