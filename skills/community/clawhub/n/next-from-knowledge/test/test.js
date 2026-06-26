const assert = require('assert');
const NextFromKnowledge = require('../src/index.js');

function run() {
  const engine = new NextFromKnowledge();
  let passed = 0;
  let failed = 0;

  function test(name, fn) {
    try {
      fn();
      console.log(`PASS ${name}`);
      passed += 1;
    } catch (error) {
      console.log(`FAIL ${name}: ${error.message}`);
      failed += 1;
    }
  }

  const actionText = `
用户访谈里 5 次提到 onboarding 不清楚。
现在只有 2 周窗口，工程资源有限。
先安排 3 个新用户访谈验证首页文案。
之后再决定是否重写整个流程。
`;

  const decideText = `
方案A 重写整个 onboarding，成本高，依赖设计和前端排期。
方案B 先修首页文案和引导问题，最快本周验证，风险更低。
用户反馈主要集中在文案理解，不在功能缺失。
`;

  const gapText = `
已经知道用户抱怨设置复杂，团队本周能改文案。
还不清楚是注册步骤太多，还是价值表达不清楚？
是否需要法务审批也待确认。
`;

  test('distill finds actions and constraints', () => {
    const distilled = engine.distill(actionText);
    assert(distilled.actions.some((item) => item.includes('先安排 3 个新用户访谈验证首页文案')));
    assert(distilled.constraints.some((item) => item.includes('工程资源有限')));
  });

  test('nextStep prefers the explicit first action', () => {
    const result = engine.nextStep({ text: actionText });
    assert(result.recommendedMove.includes('先安排 3 个新用户访谈验证首页文案'));
  });

  test('plan builds a now bucket', () => {
    const result = engine.plan({ text: actionText }, { horizon: '7d' });
    assert(result.now.length >= 1);
    assert(result.horizon === '7d');
  });

  test('decide chooses the lower-risk option', () => {
    const result = engine.decide({ text: decideText }, { options: ['方案A', '方案B'] });
    assert.strictEqual(result.decision, '方案B');
  });

  test('experiment produces a hypothesis and test', () => {
    const result = engine.experiment({ text: actionText });
    assert(result.hypothesis.length > 0);
    assert(result.smallestUsefulTest.length > 0);
  });

  test('gaps surfaces explicit unknowns', () => {
    const result = engine.gaps({ text: gapText });
    assert(result.missingFacts.length >= 2);
  });

  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

run();
