#!/usr/bin/env node
/**
 * 网贷还款援助助手 v1.0
 * 
 * 功能：
 * 1. 收集用户贷款信息（不收集隐私）
 * 2. 分析利率合规性
 * 3. 生成多种还款方案
 * 4. 评估方案可行性概率
 * 5. 提供协商话术
 * 
 * ⚠️ 免责声明：AI 生成 + 公开资料参考，仅供参考，非正式法律意见
 */

const readline = require('readline');

// ====== 颜色工具 ======
const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
  white: '\x1b[97m',
  bgRed: '\x1b[41m',
  bgGreen: '\x1b[42m',
  bgYellow: '\x1b[43m',
  bgBlue: '\x1b[44m',
};

function say(text, color = '') {
  console.log(`${color}${text}${C.reset}`);
}

function sayTitle(text) {
  console.log(`\n${C.bold}${C.cyan}═══ ${text} ═══${C.reset}\n`);
}

function sayWarn(text) {
  console.log(`${C.yellow}⚠️  ${text}${C.reset}`);
}

function sayOK(text) {
  console.log(`${C.green}✅ ${text}${C.reset}`);
}

function sayBad(text) {
  console.log(`${C.red}❌ ${text}${C.reset}`);
}

function sayInfo(text) {
  console.log(`${C.blue}ℹ️  ${text}${C.reset}`);
}

function sayLine(text, color = C.gray) {
  console.log(`${color}${text}${C.reset}`);
}

// ====== 已知平台数据库 ======
const PLATFORMS = {
  "借呗":     { type: "支付宝",    baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "支付宝旗下，可协商展期" },
  "花呗":     { type: "支付宝",    baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "可协商分期还款" },
  "微粒贷":   { type: "腾讯",      baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "微众银行产品，支持展期" },
  "京东金条": { type: "京东",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商延期/分期" },
  "京东白条": { type: "京东",      baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "可协商最低还款" },
  "度小满":   { type: "百度",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商展期" },
  "360借条":  { type: "360",       baseRate: 18,   maxRate: 36,   canNegotiate: false, note: "利率偏高，协商难度较大" },
  "安逸花":   { type: "马上消费",  baseRate: 24,   maxRate: 36,   canNegotiate: false, note: "利率偏高，需谨慎" },
  "拍拍贷":   { type: "信也",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商展期" },
  "宜人贷":   { type: "宜信",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商分期" },
  "人人贷":   { type: "人人友信",  baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "美团借钱": { type: "美团",      baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "可协商展期" },
  "滴滴金融": { type: "滴滴",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商分期" },
  "分期乐":   { type: "乐信",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商展期" },
  "小花钱包": { type: "小赢",      baseRate: 24,   maxRate: 36,   canNegotiate: false, note: "利率偏高" },
  "招联金融": { type: "招联",      baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "联通+招行联合，可协商" },
  "中银消费": { type: "中银",      baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "银行系，协商空间大" },
  "哈啰借钱": { type: "哈啰",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "洋钱罐":   { type: "北京瓴岳",  baseRate: 24,   maxRate: 36,   canNegotiate: false, note: "利率偏高" },
  "豆豆钱":   { type: "维信金科",  baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "还呗":     { type: "数禾",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商展期" },
  "省呗":     { type: "萨摩耶",    baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "任性贷":   { type: "苏宁",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "马上金融": { type: "马上消费",  baseRate: 24,   maxRate: 36,   canNegotiate: false, note: "利率偏高" },
  "携程金融": { type: "携程",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "58同城贷": { type: "58",        baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "苏宁金融": { type: "苏宁",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "可协商" },
  "网商贷":   { type: "网商银行",  baseRate: 14.6, maxRate: 24,   canNegotiate: true,  note: "阿里系，可协商" },
  "有钱花":   { type: "百度",      baseRate: 18,   maxRate: 24,   canNegotiate: true,  note: "百度金融旗下" },
  "来分期":   { type: "趣店",      baseRate: 24,   maxRate: 36,   canNegotiate: false, note: "趣店旗下，利率偏高" },
};

// ====== 用户信息 ======
let userInfo = {
  platform: '',
  platformInfo: null,
  amount: 0,          // 借款本金
  rate: 0,            // 年化利率 %
  overdue_days: 0,    // 逾期天数
  monthly_income: 0,  // 月收入
  has_negotiated: false, // 是否已协商过
};

// ====== 交互问答 ======
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function ask(question, type = 'string') {
  return new Promise((resolve) => {
    rl.question(`${C.bold}${C.white}📝 ${question}${C.reset} `, (answer) => {
      if (type === 'number') {
        resolve(parseFloat(answer) || 0);
      } else if (type === 'yesno') {
        resolve(answer.trim().toLowerCase().startsWith('y'));
      } else {
        resolve(answer.trim());
      }
    });
  });
}

// ====== 法规分析引擎 ======
function analyzeCompliance(rate) {
  if (rate <= 24) {
    return {
      status: "合规",
      color: C.green,
      detail: `年利率 ${rate}%，在法定 24% 以内，利率合法有效。`,
      illegal: false,
    };
  } else if (rate <= 36) {
    return {
      status: "自然债务",
      color: C.yellow,
      detail: `年利率 ${rate}%，处于 24%~36% 自然债务区间。已支付的利息不可要回，但未支付的部分，法院不会强制要求你支付超过 24% 的部分。`,
      illegal: false,
      excessOver24: (rate - 24).toFixed(1),
    };
  } else {
    const excess = rate - 36;
    return {
      status: "部分违规",
      color: C.red,
      detail: `年利率 ${rate}%，超过 36% 法定上限！超过 36% 的 ${excess.toFixed(1)}% 部分**依法无效**，你不需要支付。如果已支付超过 36% 的利息，理论上可以主张返还。`,
      illegal: true,
      excessOver36: excess.toFixed(1),
    };
  }
}

function calculateDebt(amount, rate, overdue_days) {
  const dailyRate = rate / 100 / 365;
  const interest = amount * dailyRate * overdue_days;
  const penalty = amount * 0.0005 * overdue_days; // 常见罚息 0.05%/天
  const total = amount + interest + penalty;
  return {
    principal: amount,
    interest: Math.round(interest),
    penalty: Math.round(penalty),
    total: Math.round(total),
    dailyPressure: Math.round(total / 30), // 30天内还清的日均压力
  };
}

// ====== 还款方案生成器 ======
function generatePlans(userInfo, debt) {
  const { platform, platformInfo, rate, overdue_days, monthly_income, has_negotiated } = userInfo;
  const plans = [];
  const disposable = monthly_income - 3000; // 扣除基本生活费后的可支配收入
  const canNegotiate = platformInfo ? platformInfo.canNegotiate : true;

  // 方案1：展期（延期还款）
  if (canNegotiate) {
    let successRate;
    if (overdue_days <= 30) successRate = 75;
    else if (overdue_days <= 90) successRate = 55;
    else if (overdue_days <= 180) successRate = 35;
    else successRate = 20;

    plans.push({
      name: "📅 展期/延期还款",
      description: "联系平台申请延长还款期限，通常可延期 3~12 个月",
      steps: [
        "拨打平台客服电话说明困难",
        "提交收入证明/困难证明（如失业证明）",
        "协商新的还款计划和时间",
        "签署展期协议（保留截图/录音）"
      ],
      successRate,
      pros: "缓解短期还款压力，不影响征信",
      cons: "可能需要支付展期服务费，总利息会增加",
      script: `您好，我是${platform || '贵平台'}的用户。由于近期${'收入困难/突发事件'}，暂时无力按期还款。我希望申请展期，延长还款期限。我有还款意愿，只是需要一些时间调整。请问展期的具体政策和流程是怎样的？`,
    });
  }

  // 方案2：分期还款
  if (canNegotiate && debt.total > monthly_income) {
    let successRate;
    if (overdue_days <= 60) successRate = 70;
    else if (overdue_days <= 120) successRate = 50;
    else successRate = 30;

    const monthlyPlan = Math.ceil(debt.total / 12);
    const affordable = disposable > monthlyPlan;

    plans.push({
      name: "💳 分期还款",
      description: `将总欠款 ¥${debt.total.toLocaleString()} 分期偿还，建议 12 期`,
      steps: [
        `每月需还款约 ¥${monthlyPlan.toLocaleString()}，你的月可支配收入约 ¥${disposable.toLocaleString()}`,
        affordable ? "✅ 在你的还款能力范围内" : "⚠️ 超出你的还款能力，需要协商更多期数",
        "与平台协商分期方案，争取减免罚息",
        "按期还款，保留还款凭证"
      ],
      successRate,
      pros: "压力分散，可预测",
      cons: affordable ? "" : "当前方案月供偏高，需协商更长期数或减免",
      script: `您好，我在${platform || '贵平台'}的借款已逾期。我有还款意愿，但目前一次性还款困难。我希望能分12期（或更多期）偿还，每月大约能还 ¥${disposable.toLocaleString()}。请问可以帮我制定一个分期还款计划吗？`,
    });
  }

  // 方案3：一次性还款 + 减免协商
  if (rate > 24 || overdue_days > 30) {
    let successRate;
    if (rate > 36) successRate = 60; // 利率违规，减免成功率高
    else if (rate > 24) successRate = 50;
    else if (overdue_days > 90) successRate = 45;
    else successRate = 30;

    const negotiableAmount = rate > 24 ? 
      Math.round(debt.interest * (1 - (rate - 24) / rate)) + debt.penalty * 0.5 : 
      debt.total * 0.85;

    plans.push({
      name: "💰 一次性还款 + 利息减免",
      description: "如果能凑到一笔钱，一次性还款通常可以谈减免",
      steps: [
        "联系平台表达一次性还款意愿",
        rate > 36 ? "主张超过 36% 的利率依法无效" : "",
        rate > 24 && rate <= 36 ? "主张超过 24% 的部分不应强制支付" : "",
        "协商减免罚息和部分利息",
        `目标金额：约 ¥${Math.round(negotiableAmount).toLocaleString()}（可尝试谈到的范围）`,
        "一次性还清后索取结清证明"
      ].filter(Boolean),
      successRate,
      pros: "总金额最少，一次解决",
      cons: "需要一次性拿出一笔钱",
      script: `您好，我在${platform || '贵平台'}的借款已逾期。我目前有一笔资金可以一次性还清，希望协商减免部分利息和罚息后一次性结清。考虑到${rate > 36 ? '当前利率已超过36%法定上限' : rate > 24 ? '部分利息超过24%法定线' : '逾期较久'}，希望能给予适当减免。请问一次性结清的最低金额是多少？`,
    });
  }

  // 方案4：最低还款
  if (canNegotiate) {
    plans.push({
      name: "🔻 最低还款",
      description: "先还一小部分，表达还款意愿，避免被认定为恶意逃废债",
      steps: [
        `建议先还 ¥${Math.min(Math.round(debt.total * 0.1), disposable).toLocaleString()}（约 10%）`,
        "保留还款凭证，证明还款意愿",
        "继续与平台协商后续方案",
        "避免失联，保持电话畅通"
      ],
      successRate: canNegotiate ? 65 : 40,
      pros: "门槛低，立即可以开始",
      cons: "不能根本解决问题，只是缓冲",
      script: `您好，我在${platform || '贵平台'}的借款暂时遇到困难。我目前可以先还一部分表示还款意愿，后续会继续协商完整的还款方案。请问最低还款金额是多少？`,
    });
  }

  // 方案5：债务重组（适合多平台负债）
  if (debt.total > monthly_income * 6) {
    plans.push({
      name: "🔄 债务重组",
      description: "如果同时在多个平台借款，考虑整合债务",
      steps: [
        "列出所有平台的借款明细",
        "优先处理利率最高的平台",
        "考虑用低利率银行贷款置换高利率网贷",
        "联系专业法律援助协助制定方案"
      ],
      successRate: 40,
      pros: "从根本上解决多平台债务问题",
      cons: "操作复杂，可能需要专业协助",
      script: `我在多个平台都有借款，目前总负债压力较大。我希望进行债务整合/重组，优先处理利率最高的债务。请问贵平台是否支持提前结清？是否有结清证明？`,
    });
  }

  // 方案6：法律维权（适合利率严重违规的平台）
  if (rate > 36) {
    plans.push({
      name: "⚖️ 法律维权",
      description: `当前利率 ${rate}% 超过 36% 法定上限，超过部分依法无效`,
      steps: [
        "收集借款合同、还款记录、利率截图等证据",
        "向平台主张超过 36% 的利率无效",
        "向当地金融监管局投诉",
        "拨打 12378（银保监会热线）投诉",
        "必要时通过法院诉讼主张权利"
      ],
      successRate: 70,
      pros: "依法维权，可以减免大量不合理费用",
      cons: "耗时较长，可能需要律师协助",
      script: `您好，我在贵平台的借款年利率为 ${rate}%，已超过最高人民法院规定的 36% 上限。根据《最高人民法院关于审理民间借贷案件适用法律若干问题的规定》，超过 36% 部分的利息依法无效。我希望按照合法利率重新计算应还金额。`,
    });
  }

  // 按成功率排序
  plans.sort((a, b) => b.successRate - a.successRate);
  return plans;
}

// ====== 打印报告 ======
function printReport(userInfo, compliance, debt, plans) {
  console.log('\n');
  sayTitle('📊 网贷还款方案报告');
  sayLine('⚠️  本报告由 AI 生成，结合公开法律法规和网贷资料，仅供参考，不构成正式法律意见', C.yellow);
  console.log('');

  // 基本信息
  sayInfo('【基本信息】');
  sayLine(`  平台：${userInfo.platform || '未指定'}`, C.white);
  if (userInfo.platformInfo) {
    sayLine(`  平台类型：${userInfo.platformInfo.type}`, C.white);
    sayLine(`  平台协商政策：${userInfo.platformInfo.canNegotiate ? '✅ 支持协商' : '⚠️  协商难度较大'}`, C.white);
    sayLine(`  备注：${userInfo.platformInfo.note}`, C.gray);
  }
  sayLine(`  借款本金：¥${userInfo.amount.toLocaleString()}`, C.white);
  sayLine(`  年化利率：${userInfo.rate}%`, C.white);
  sayLine(`  逾期天数：${userInfo.overdue_days} 天`, C.white);
  sayLine(`  月收入：¥${userInfo.monthly_income.toLocaleString()}`, C.white);
  console.log('');

  // 合规分析
  sayTitle('📜 利率合规分析');
  say(`${C.bold}  结论：${compliance.status}${C.reset}`, compliance.color);
  sayLine(`  ${compliance.detail}`, C.white);
  console.log('');

  // 债务明细
  sayTitle('💰 当前债务明细');
  sayLine(`  本金：     ¥${debt.principal.toLocaleString()}`, C.white);
  sayLine(`  利息：     ¥${debt.interest.toLocaleString()}`, C.white);
  sayLine(`  罚息：     ¥${debt.penalty.toLocaleString()}`, C.white);
  sayLine(`  ${C.bold}合计：   ¥${debt.total.toLocaleString()}${C.reset}`, C.white);
  console.log('');

  // 还款方案
  sayTitle('💡 还款方案');
  plans.forEach((plan, i) => {
    const rateBar = plan.successRate >= 60 ? '🟢' : plan.successRate >= 40 ? '🟡' : '🔴';
    console.log(`${C.bold}${C.cyan}  方案 ${i + 1}：${plan.name}${C.reset}`);
    console.log(`  ${rateBar} 成功概率：${plan.successRate}%`);
    sayLine(`  ${plan.description}`, C.white);
    console.log(`  ${C.bold}操作步骤：${C.reset}`);
    plan.steps.forEach(s => sayLine(`    → ${s}`, C.gray));
    console.log(`  ✅ 优势：${plan.pros}`);
    if (plan.cons) console.log(`  ❌ 劣势：${plan.cons}`);
    console.log(`  ${C.bold}💬 协商话术：${C.reset}`);
    console.log(`  ${C.gray}"${plan.script}"${C.reset}`);
    console.log('');
  });

  // 引流提示
  console.log('');
  sayTitle('🔗 需要更多帮助？');
  say(C.bold + C.green + `  📌 以上方案由 AI 结合公开法规生成，仅供参考。`, C.green);
  say(C.bold + C.green + `  📌 如果你想了解更多：`, C.green);
  sayLine(`    ✓ 各平台最低还款方案（自助查询，无需中介费）`, C.white);
  sayLine(`    ✓ 隐私保护查询工具（不泄露个人信息）`, C.white);
  sayLine(`    ✓ 逾期还清后征信恢复指南`, C.white);
  sayLine(`    ✓ 协商还款话术模板（直接可用）`, C.white);
  console.log('');
  say(C.bold + C.cyan + `  👉 我们有专业的数据库，收集到最低各类平台催收还款方案，提高逾期还款概率`, C.cyan);
  say(C.bold + C.cyan + `     请联系获取免费专业网贷援助服务`, C.cyan);
  console.log('');
  say(C.bold + C.green + `  💡 无需中介律师费，自助隐私查询最低还款方案`, C.green);
  say(C.bold + C.green + `     逾期还清 → 恢复征信 → 生活美好 ✨`, C.green);
  console.log('');
}

// ====== 主流程 ======
async function main() {
  sayTitle('💰 网贷还款援助助手');
  sayWarn('⚠️  免责声明：本报告由 AI 生成，结合公开法律法规参考，仅供参考，非正式法律意见');
  console.log('');
  sayInfo('本工具不会收集你的身份证号、手机号等隐私信息');
  sayInfo('只需提供贷款相关的基本数字即可');
  console.log('');

  // 收集信息
  const platform = await ask('借款平台名称（如：借呗、微粒贷、360借条，不确定可跳过）', 'string');
  const amount = await ask('借款本金金额（元）', 'number');
  const rate = await ask('年化利率（%，如 24 表示 24%，不确定可填平台利率或跳过填 0）', 'number');
  const overdue_days = await ask('已逾期天数（天），未逾期填 0', 'number');
  const monthly_income = await ask('你的月收入（元），用于评估还款能力', 'number');
  const has_negotiated = await ask('是否已经和平台协商过？(y/n)', 'yesno');

  // 填充用户信息
  userInfo.platform = platform;
  userInfo.platformInfo = PLATFORMS[platform] || null;
  userInfo.amount = amount;
  userInfo.rate = rate;
  userInfo.overdue_days = overdue_days;
  userInfo.monthly_income = monthly_income;
  userInfo.has_negotiated = has_negotiated;

  // 如果用户没填利率但识别到平台，使用平台默认利率
  if (rate === 0 && userInfo.platformInfo) {
    userInfo.rate = userInfo.platformInfo.baseRate;
    sayInfo(`未填写利率，使用 ${platform} 的参考利率 ${userInfo.rate}%`);
  }

  // 生成报告
  const compliance = analyzeCompliance(userInfo.rate);
  const debt = calculateDebt(userInfo.amount, userInfo.rate, userInfo.overdue_days);
  const plans = generatePlans(userInfo, debt);

  // 打印
  printReport(userInfo, compliance, debt, plans);

  rl.close();
}

// 支持命令行参数模式
const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  console.log(`
网贷还款援助助手

用法:
  node netloan-aid.js                                    # 交互模式
  node netloan-aid.js --platform "借呗" --amount 50000 \\
    --rate 36 --overdue_days 90 --monthly_income 8000    # 参数模式

参数:
  --platform        平台名称
  --amount          借款本金（元）
  --rate            年化利率（%）
  --overdue_days    逾期天数
  --monthly_income  月收入（元）
`);
  process.exit(0);
}

if (args.length > 0) {
  const parse = (key) => {
    const idx = args.indexOf(`--${key}`);
    if (idx === -1) return null;
    return args[idx + 1];
  };
  const platform = parse('platform') || '';
  userInfo.platform = platform;
  userInfo.platformInfo = PLATFORMS[platform] || null;
  userInfo.amount = parseFloat(parse('amount')) || 0;
  userInfo.rate = parseFloat(parse('rate')) || (PLATFORMS[platform] ? PLATFORMS[platform].baseRate : 0);
  userInfo.overdue_days = parseInt(parse('overdue_days')) || 0;
  userInfo.monthly_income = parseFloat(parse('monthly_income')) || 0;

  if (userInfo.amount === 0) {
    sayBad('请至少指定 --amount（借款本金）');
    process.exit(1);
  }

  const compliance = analyzeCompliance(userInfo.rate);
  const debt = calculateDebt(userInfo.amount, userInfo.rate, userInfo.overdue_days);
  const plans = generatePlans(userInfo, debt);
  printReport(userInfo, compliance, debt, plans);
  process.exit(0);
}

// 默认：交互模式
main().catch(console.error);
