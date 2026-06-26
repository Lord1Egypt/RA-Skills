const assert = require('assert');
const fs = require('fs');
const path = require('path');
const {
  generateBlueprint,
  detectIndustry,
  classifyCompetitor
} = require('../src/rules');

const result = generateBlueprint({
  client: '某连锁企业',
  industry: '零售/消费品',
  stage: 'POC',
  competitors: ['平台型厂商', '低价竞争者'],
  budget: '已立项',
  signals: ['多家竞品', '预算模糊']
});

assert.strictEqual(result.stage, 'POC阶段');
assert.strictEqual(result.industryPlaybook.label, '零售/消费品');
assert.strictEqual(result.competitorStrategy.length, 2);
assert.ok(result.riskAssessment.score < 100);
assert.ok(result.selfChecklist.mustFix.length > 0);
assert.ok(result.nextMoves.length > 0);

assert.strictEqual(detectIndustry('政府公共服务'), 'government');
assert.strictEqual(detectIndustry('制造供应链'), 'manufacturing');
assert.strictEqual(classifyCompetitor('传统套件厂商'), 'legacy');
assert.strictEqual(classifyCompetitor('报价低'), 'lowPrice');

const root = path.resolve(__dirname, '..');
const files = [
  'SKILL.md',
  'README.md',
  'package.json',
  'src/index.js',
  'src/rules.js',
  'tests/test.js'
];

const forbidden = [
  ['17', '年'].join(''),
  ['18', '年'].join(''),
  ['资深', '从业者'].join(''),
  ['测试', '点'].join(''),
  ['问题', '关闭率'].join(''),
  ['P', '0'].join(''),
  ['P', '1'].join(''),
  ['P', '2'].join(''),
  ['P', '3'].join('')
];

for (const file of files) {
  const content = fs.readFileSync(path.join(root, file), 'utf8');
  for (const word of forbidden) {
    assert.ok(!content.includes(word), `${file} contains forbidden text: ${word}`);
  }
}

console.log('presales-win-blueprint tests passed');
