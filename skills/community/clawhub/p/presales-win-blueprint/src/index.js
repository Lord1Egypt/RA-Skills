#!/usr/bin/env node

const readline = require('readline');
const { generateBlueprint } = require('./rules');

function splitList(value) {
  return (value || '').split(',').map(item => item.trim()).filter(Boolean);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const input = {};

  for (let i = 0; i < args.length; i += 1) {
    const key = args[i];
    const value = args[i + 1];
    switch (key) {
      case '--client':
        input.client = value;
        i += 1;
        break;
      case '--industry':
        input.industry = value;
        i += 1;
        break;
      case '--stage':
        input.stage = value;
        i += 1;
        break;
      case '--competitors':
        input.competitors = splitList(value);
        i += 1;
        break;
      case '--budget':
        input.budget = value;
        i += 1;
        break;
      case '--decision-role':
        input.decisionRole = value;
        i += 1;
        break;
      case '--signals':
        input.signals = splitList(value);
        i += 1;
        break;
      default:
        break;
    }
  }

  return input;
}

function printList(items, prefix = '  - ') {
  items.forEach(item => console.log(`${prefix}${item}`));
}

function printOutput(result) {
  console.log('');
  console.log('='.repeat(64));
  console.log('presales-win-blueprint | 售前方案通关秘籍');
  console.log('='.repeat(64));
  console.log(`客户: ${result.client}`);
  console.log(`行业: ${result.industry} (${result.industryPlaybook.label})`);
  console.log(`阶段: ${result.stage}`);
  console.log(`预算: ${result.budget}`);
  console.log('');

  console.log('1. 阶段打法');
  console.log(result.stageAnalysis.summary);
  printList(result.stageAnalysis.focusItems);
  console.log(`行动建议: ${result.stageAnalysis.actionPlan}`);
  console.log(`赢单条件: ${result.stageAnalysis.winCondition}`);
  console.log('');

  console.log('2. 行业打法');
  printList(result.industryPlaybook.angles);
  console.log('关键追问:');
  printList(result.industryPlaybook.mustAsk);
  console.log('建议证明材料:');
  printList(result.industryPlaybook.proof);
  console.log('');

  console.log('3. 竞品攻防');
  if (result.competitorStrategy.length === 0) {
    console.log('  - 未输入竞品。建议仍准备平台型、低价型、同类竞品三套话术。');
  } else {
    result.competitorStrategy.forEach(item => {
      console.log(`  ${item.competitor} | ${item.type}`);
      printList(item.tactics, '    - ');
    });
  }
  console.log('');

  console.log('4. 风险预警');
  console.log(`评分: ${result.riskAssessment.score}/100 (${result.riskAssessment.level})`);
  if (result.riskAssessment.warnings.length === 0) {
    console.log('  - 暂未识别明显风险信号。');
  } else {
    printList(result.riskAssessment.warnings);
  }
  console.log('');

  console.log('5. 方案自检');
  result.selfChecklist.mustFix.forEach(item => {
    console.log(`  [${item.category}] ${item.question}`);
    console.log(`    风险: ${item.failWarning}`);
  });
  console.log('');

  console.log('6. 下一步');
  printList(result.nextMoves);
  console.log('');

  console.log(`经验提示: ${result.tip}`);
  console.log('='.repeat(64));
}

async function interactive() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = question => new Promise(resolve => rl.question(question, resolve));

  console.log('');
  console.log('presales-win-blueprint | 售前方案通关秘籍');
  const client = await ask('客户名称: ');
  const industry = await ask('所属行业: ');
  const stage = (await ask('当前阶段 (线索期/需求期/POC阶段/招投标/商务谈判) [需求期]: ')) || '需求期';
  const competitors = splitList(await ask('已知竞品 (逗号分隔，可选): '));
  const budget = await ask('预估预算 (可选): ');
  const decisionRole = await ask('主要决策角色 (可选): ');
  const signals = splitList(await ask('风险信号 (逗号分隔，可选): '));
  rl.close();

  printOutput(generateBlueprint({ client, industry, stage, competitors, budget, decisionRole, signals }));
}

if (process.argv.includes('--quick')) {
  const input = parseArgs();
  if (!input.client || !input.industry) {
    console.error('快速模式需要至少指定 --client 和 --industry');
    console.error('示例: presales-win-blueprint --quick --client "某连锁企业" --industry "零售" --stage "需求期"');
    process.exit(1);
  }
  printOutput(generateBlueprint(input));
} else {
  interactive().catch(error => {
    console.error(error);
    process.exit(1);
  });
}
