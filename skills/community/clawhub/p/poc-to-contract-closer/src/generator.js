#!/usr/bin/env node

const readline = require('readline');

function parseNumber(value) {
  const n = Number.parseFloat(value);
  return Number.isFinite(n) ? n : null;
}

function normalize(value) {
  return (value || '').trim();
}

function assessClosing(config) {
  const passRate = Number.isFinite(config.passRate) ? config.passRate : null;
  const p0 = Number.isFinite(config.p0) ? config.p0 : 0;
  const p1 = Number.isFinite(config.p1) ? config.p1 : 0;
  const silenceDays = Number.isFinite(config.silenceDays) ? config.silenceDays : null;
  const decisionMaker = normalize(config.decisionMaker);
  const procurementPath = normalize(config.procurementPath);
  const launchWindow = normalize(config.launchWindow);
  const acceptedValue = normalize(config.acceptedValue);
  const cooling = assessCooling(silenceDays);

  const gaps = [];
  const actions = [];
  let score = 0;

  if (passRate !== null && passRate >= 90) score += 2;
  else gaps.push('POC 通过率未达到 >=90% 或缺少可量化验收结果');

  if (p0 === 0) score += 2;
  else gaps.push(`仍有 ${p0} 个 P0，必须关闭或取得客户书面接受 workaround`);

  if (acceptedValue) score += 1;
  else gaps.push('客户已接受的业务价值未写成可转发证据');

  if (decisionMaker) score += 1;
  else gaps.push('决策人未触达，champion 认可不能等同于可签约');

  if (procurementPath) score += 2;
  else gaps.push('采购路径缺失：需确认招投标/单一来源/框架协议/续约/比价路径');

  if (launchWindow) score += 1;
  else gaps.push('缺少上线窗口期，合同没有时间紧迫性');

  if (cooling.status !== 'Normal') {
    gaps.push(cooling.gap);
  }

  actions.push({
    step: 'Data Passed',
    status: passRate !== null && passRate >= 90 ? 'Ready' : 'Gap',
    evidence: passRate !== null ? `${passRate}% pass rate` : 'missing measurable result',
    gap: passRate !== null && passRate >= 90 ? '-' : '补齐验收口径或一页纸 POC 结果',
    owner: 'Tech owner',
    next: '把 POC 结果写成一句话：测了什么、通过什么、证明什么价值',
  });

  actions.push({
    step: 'Issues Cleared',
    status: p0 === 0 ? (p1 > 0 ? 'Nearly ready' : 'Ready') : 'Blocked',
    evidence: `P0=${p0}, P1=${p1}`,
    gap: p0 === 0 ? (p1 > 0 ? 'P1 需 owner + post-contract plan' : '-') : 'P0 未清零',
    owner: 'Tech owner',
    next: p0 === 0 ? 'P1 转为合同后处理计划，P2 入 backlog' : '先回 war-room 清 P0',
  });

  actions.push({
    step: 'Decision Maker Reached',
    status: decisionMaker ? 'Ready' : 'Gap',
    evidence: decisionMaker || 'unknown',
    gap: decisionMaker ? '-' : '经济买方/业务 owner/技术门禁/采购法务 owner 未确认',
    owner: 'Sales owner',
    next: decisionMaker ? '安排决策人复盘或确认签约路径' : '约 champion 安排 executive recap',
  });

  actions.push({
    step: 'Procurement Path',
    status: procurementPath ? 'Ready' : 'Gap',
    evidence: procurementPath || 'unknown',
    gap: procurementPath ? '-' : '未确认是否招投标、比价、单一来源、框架协议或续约采购',
    owner: 'Sales owner',
    next: procurementPath ? '把路径转为倒排节点' : '当天向采购/客户 champion 确认采购方式和最早可启动日期',
  });

  actions.push({
    step: 'Closing Window',
    status: launchWindow ? 'Ready' : 'Gap',
    evidence: launchWindow || 'unknown',
    gap: launchWindow ? '-' : '缺少必须签约/上线的时间窗口',
    owner: 'Sales owner',
    next: launchWindow ? '围绕窗口期倒排合同、采购、上线节点' : '确认业务上线窗口、预算周期或会议节点',
  });

  actions.push({
    step: 'Cooling Threshold',
    status: cooling.status === 'Normal' ? 'Ready' : cooling.status,
    evidence: silenceDays !== null ? `${silenceDays} days silence` : 'unknown',
    gap: cooling.status === 'Normal' ? '-' : cooling.gap,
    owner: 'Sales owner',
    next: cooling.next,
  });

  const hasHardCoolingGap = cooling.status === 'Gap' || cooling.status === 'Blocked';
  let status = score >= 8 && p0 === 0 && !hasHardCoolingGap ? 'Ready' : score >= 5 && p0 === 0 ? 'Nearly ready' : 'Not ready';
  if (cooling.status === 'Blocked') status = 'Blocked';
  const mainBlocker = p0 > 0 ? 'P0 issue not cleared' : gaps[0] || 'none';
  const returnToWarRoom = p0 > 0 || (passRate !== null && passRate < 90) || cooling.status === 'Blocked';

  return { status, gaps, actions, mainBlocker, returnToWarRoom, cooling };
}

function assessCooling(silenceDays) {
  if (!Number.isFinite(silenceDays)) {
    return {
      status: 'Gap',
      gap: '客户沉默天数未知，无法判断 closing 是否进入冷却',
      next: '补齐上次客户有效互动日期，并设置 3/7/14 天跟进阈值',
    };
  }
  if (silenceDays >= 14) {
    return {
      status: 'Blocked',
      gap: '客户沉默达到 14 天，视为 closing 冷却/失速',
      next: '停止常规报价推进，回到 champion + 决策人路径重启，必要时回 war-room 重建价值证据',
    };
  }
  if (silenceDays >= 7) {
    return {
      status: 'Gap',
      gap: '客户沉默达到 7 天，closing 动能正在丢失',
      next: '当天触达 champion，要求确认决策人、采购路径和下一次会议节点',
    };
  }
  if (silenceDays >= 3) {
    return {
      status: 'Nearly ready',
      gap: '客户沉默达到 3 天，需要主动保持签约动能',
      next: '发送 POC 一页纸 recap，并请求确认下一步 buying-process 节点',
    };
  }
  return {
    status: 'Normal',
    gap: '-',
    next: '按既定 closing 节奏推进，并维护下一节点日期',
  };
}

function generateReport(config) {
  const result = assessClosing(config);
  const lines = [];

  lines.push('## POC-to-Contract Closing Plan', '');
  lines.push('### 1. Closing Readiness');
  lines.push(`- Status: ${result.status}`);
  lines.push(`- Reason: ${result.gaps.length ? result.gaps.join('; ') : 'POC evidence, buyer path, procurement path, and closing window are present.'}`);
  lines.push(`- Main blocker: ${result.mainBlocker}`);
  lines.push(`- Return to \`tob-poc-war-room\`? ${result.returnToWarRoom ? 'yes' : 'no'}`, '');

  lines.push('### 2. Six-Step Checklist');
  lines.push('| Step | Status | Evidence | Gap | Owner | Next action |');
  lines.push('|------|--------|----------|-----|-------|-------------|');
  result.actions.forEach((a) => {
    lines.push(`| ${a.step} | ${a.status} | ${a.evidence} | ${a.gap} | ${a.owner} | ${a.next} |`);
  });
  lines.push('');

  lines.push('### 3. One-Page Recap Draft');
  lines.push(`- Original pain: ${config.originalPain || 'missing'}`);
  lines.push(`- POC scope: ${config.scope || 'missing'}`);
  lines.push(`- Result: ${Number.isFinite(config.passRate) ? `${config.passRate}% pass rate` : 'missing measurable result'}`);
  lines.push(`- Business value: ${config.acceptedValue || 'missing'}`);
  lines.push(`- Remaining risks: P0=${Number.isFinite(config.p0) ? config.p0 : 0}, P1=${Number.isFinite(config.p1) ? config.p1 : 0}, P2=${Number.isFinite(config.p2) ? config.p2 : 0}`);
  lines.push(`- Procurement path: ${config.procurementPath || 'missing'}`);
  lines.push(`- Closing window: ${config.launchWindow || 'missing'}`);
  lines.push(`- Cooling threshold: ${Number.isFinite(config.silenceDays) ? `${config.silenceDays} days silence; ${result.cooling.status}` : 'missing silence-days'}`);
  lines.push(`- Rollout proposal: ${config.launchWindow || 'missing launch window'}`);
  lines.push('- Decision requested: confirm buyer/procurement path and next contract node', '');

  lines.push('### 4. Customer Message');
  lines.push('- Recipient: champion + decision maker/procurement owner if known');
  lines.push('- Objective: convert accepted POC result into a dated buying-process node');
  lines.push('- Draft:');
  lines.push(`  ${buildCustomerMessage(config, result)}`, '');

  lines.push('### 5. Quote / Commercial Action');
  lines.push(`- Quote now? ${result.status === 'Ready' ? 'yes' : 'no'}`);
  lines.push(`- Scope: ${config.scope || 'confirm from POC recap first'}`);
  lines.push('- Assumptions: P0 cleared, P1 has owner, procurement path confirmed');
  lines.push('- Owner: Sales owner');
  lines.push(`- Deadline: ${config.deadline || (config.launchWindow ? 'before launch-window procurement cutoff' : 'after procurement path confirmation')}`, '');

  lines.push('### 6. Launch Node');
  lines.push(`- Proposed kickoff: ${config.launchWindow || 'missing'}`);
  lines.push(`- First milestone: ${config.firstMilestone || 'confirm production milestone'}`);
  lines.push('- Customer dependency: procurement/legal/resource owner confirmation');
  lines.push('- Success metric: reuse accepted POC metric as first production metric', '');

  lines.push('### 7. Risks');
  lines.push(`- Buying-process risk: ${config.procurementPath ? 'path known; track dates and owner' : 'procurement path unknown; do not send detailed quote before confirmation'}`);
  lines.push(`- Technical residual risk: P0=${Number.isFinite(config.p0) ? config.p0 : 0}, P1=${Number.isFinite(config.p1) ? config.p1 : 0}`);
  lines.push(`- Silence / momentum risk: ${Number.isFinite(config.silenceDays) ? `${config.silenceDays} days silence` : 'unknown'}`);
  lines.push(`- Cooling threshold: ${result.cooling.next}`);
  lines.push('');

  return lines.join('\n');
}

function buildCustomerMessage(config, result) {
  if (result.returnToWarRoom) {
    return 'POC 结果还需要补齐验收/阻塞清单。我们先在 48 小时内关闭 P0 或确认 workaround，再同步签约节点。';
  }
  if (!config.procurementPath) {
    return 'POC 核心结果已经具备收口基础。为了避免报价和合同节点空转，想先和您确认采购路径：招投标、比价、单一来源、框架协议还是续约采购？确认后我们当天给出倒排计划。';
  }
  if (!config.launchWindow) {
    return 'POC 核心价值已经确认，采购路径也清楚。下一步建议确认上线窗口或业务节点，我们据此倒排合同、采购和上线准备。';
  }
  return `POC 核心价值已经确认，采购路径为「${config.procurementPath}」。建议围绕「${config.launchWindow}」倒排合同和上线节点，本周先确认下一次决策/采购会议。`;
}

function parseArgs(argv) {
  const args = { passRate: null, p0: 0, p1: 0, p2: 0 };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--pass-rate': args.passRate = parseNumber(argv[++i]); break;
      case '--p0': args.p0 = parseNumber(argv[++i]); break;
      case '--p1': args.p1 = parseNumber(argv[++i]); break;
      case '--p2': args.p2 = parseNumber(argv[++i]); break;
      case '--silence-days': args.silenceDays = parseNumber(argv[++i]); break;
      case '--decision-maker': args.decisionMaker = argv[++i]; break;
      case '--procurement-path': args.procurementPath = argv[++i]; break;
      case '--launch-window': args.launchWindow = argv[++i]; break;
      case '--accepted-value': args.acceptedValue = argv[++i]; break;
      case '--original-pain': args.originalPain = argv[++i]; break;
      case '--scope': args.scope = argv[++i]; break;
      case '--deadline': args.deadline = argv[++i]; break;
      case '--first-milestone': args.firstMilestone = argv[++i]; break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(`
poc-to-contract-closer — POC 转签约收口助手

用法:
  poc-to-contract-closer
  poc-to-contract-closer --pass-rate 93 --p0 0 --p1 1 \\
    --decision-maker "业务负责人已确认" \\
    --procurement-path "比价采购" \\
    --launch-window "6月试点上线"

关键参数:
  --pass-rate          POC 通过率
  --p0 / --p1 / --p2   未关闭问题数量
  --decision-maker     决策人触达状态
  --procurement-path   招投标/比价/单一来源/框架协议/续约等采购路径
  --launch-window      上线窗口期、预算周期或必须签约节点
  --silence-days       POC 后客户沉默天数
                     冷却阈值：3天主动触达，7天动能丢失，14天视为失速/冷却
`);
}

function interactiveMode() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (question) => new Promise((resolve) => rl.question(question, resolve));

  (async () => {
    console.log('\nPOC 转签约收口助手 — 输入 POC 收口信息\n');
    const passRate = parseNumber(await ask('POC 通过率（如 93）：'));
    const p0 = parseNumber(await ask('P0 数量：'));
    const p1 = parseNumber(await ask('P1 数量：'));
    const decisionMaker = await ask('决策人触达状态：');
    const procurementPath = await ask('采购路径（招投标/比价/单一来源/框架协议/未知）：');
    const launchWindow = await ask('上线窗口期/预算节点：');
    const silenceDays = parseNumber(await ask('客户沉默天数（如 7）：'));
    const acceptedValue = await ask('客户接受的业务价值：');
    console.log('\n' + generateReport({ passRate, p0, p1, decisionMaker, procurementPath, launchWindow, silenceDays, acceptedValue }));
    rl.close();
  })();
}

if (require.main === module) {
  const args = parseArgs(process.argv);
  if (!args.passRate && !args.decisionMaker && !args.procurementPath && !args.launchWindow) {
    interactiveMode();
  } else {
    console.log(generateReport(args));
  }
}

module.exports = { assessClosing, assessCooling, buildCustomerMessage, generateReport, parseArgs };
