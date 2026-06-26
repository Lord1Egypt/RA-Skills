/**
 * presales-win-blueprint
 *
 * 行业 + 经验方法论规则引擎。
 * 规则表达保留政府、零售、制造、金融等行业打法差异，但不包含个人履历、
 * 真实客户、真实厂商、真实项目数据或可追溯案例。
 */

const STAGE_RULES = {
  '线索期': {
    summary: '先判断这是不是一条值得投入的线索。不要急着讲产品，先确认预算意愿、决策路径和业务痛点是否真实。',
    focus: [
      '确认客户是主动建设、上级要求、业务倒逼，还是只在做供应商摸底',
      '识别三类人：需求发起人、评估影响人、最终拍板人',
      '只做轻量诊断，不在需求未澄清时提交完整方案',
      '把下一步锁定为诊断会、业务访谈或场景演示，而不是无边界写材料'
    ],
    actionPlan: '安排一次短诊断，输出问题假设和待验证清单；只有客户愿意补充业务信息，才进入方案投入。',
    winCondition: '客户愿意开放业务背景，并接受你定义下一步议程。',
    riskSignals: ['预算口径模糊', '只要求发资料', '对接人无法解释业务目标']
  },
  '需求期': {
    summary: '需求期的核心不是收集功能，而是把功能诉求翻译成业务问题，再把业务问题落到可交付范围。',
    focus: [
      '用“现状-影响-目标-约束”拆需求，避免直接进入功能清单',
      '政府客户重点看合规、协同、留痕、验收；零售客户重点看周转、转化、履约、门店执行',
      '每轮沟通后形成确认纪要，把未决问题和假设写清楚',
      '提前识别客户内部是否存在多部门目标不一致'
    ],
    actionPlan: '组织业务、技术、采购或合规相关方参与的需求澄清会，形成可签收的需求边界。',
    winCondition: '客户认可你对业务问题的重构，而不只是认可功能列表。',
    riskSignals: ['只谈功能不谈指标', '业务方缺席', '需求口径反复变化']
  },
  'POC阶段': {
    summary: 'POC不是免费开发，而是用最小验证闭环证明方案价值。先定义评估标准，再安排演示和测试。',
    focus: [
      'POC开始前确认场景、数据、通过标准、时间边界和客户配合人',
      '验证业务闭环，不追求覆盖所有边缘功能',
      '过程要同步业务负责人，不能只让技术评估人掌握结论',
      '输出对比型结论：解决了什么问题、还有什么前提、下一步怎么采购'
    ],
    actionPlan: '制定POC计划和验收口径，控制在有限场景内完成价值证明，并保留书面结论。',
    winCondition: 'POC结论能被业务负责人复述，并自然导向采购或招采流程。',
    riskSignals: ['多家同时无标准测试', 'POC范围持续扩大', '客户不承诺后续流程']
  },
  '招投标': {
    summary: '招投标阶段要把前期行业理解转成评分语言。每一项响应都要对应客户的行业约束和验收逻辑。',
    focus: [
      '政府项目重点处理政策符合、数据安全、国产化适配、验收材料和运维边界',
      '零售项目重点处理多渠道数据、门店/仓配协同、促销高峰、培训推广和持续运营',
      '技术方案要逐条贴合评分点，避免只写产品能力',
      '商务承诺必须与交付能力一致，不能为了中标把风险后置'
    ],
    actionPlan: '建立评分点-响应内容-证明材料-风险承诺四列表，逐项检查缺口。',
    winCondition: '客户评审能清楚看到“懂行业、能落地、风险可控”。',
    riskSignals: ['评分规则过度价格导向', '关键参数与自身能力偏离', '交付条款模糊']
  },
  '商务谈判': {
    summary: '商务谈判不是单纯降价，而是把范围、价值、风险和付款节点重新对齐。',
    focus: [
      '先确认客户还在比较什么：价格、风险、内部意见，还是流程卡点',
      '降价必须绑定范围、付款、交付节奏或服务边界',
      '避免用口头承诺换签约，所有额外承诺都要进入清单',
      '把高层关心的结果、业务方关心的体验、技术方关心的稳定性分开回应'
    ],
    actionPlan: '输出最终商务包：范围边界、里程碑、付款节点、服务边界和未纳入项。',
    winCondition: '客户把讨论从“多少钱”转向“怎么签、怎么启动、怎么验收”。',
    riskSignals: ['突然要求重新比价', '付款节点后置', '额外承诺不进合同']
  }
};

const INDUSTRY_PLAYBOOKS = {
  government: {
    label: '政府/公共服务',
    angles: [
      '强调政策符合、跨部门协同、数据安全、审计留痕和验收闭环',
      '方案语言要从“功能先进”转为“治理能力提升、流程规范、风险可控”',
      '售前节奏要预留招采、评审、等保、信创或内控制度带来的周期不确定性'
    ],
    mustAsk: [
      '是否存在上级考核、专项建设或年度验收要求？',
      '数据归属、部署形态、审计留痕和权限边界由谁确认？',
      '最终验收材料需要覆盖哪些制度口径？'
    ],
    proof: ['政策映射表', '安全与权限方案', '验收材料清单', '运维响应边界']
  },
  retail: {
    label: '零售/消费品',
    angles: [
      '强调效率、转化、履约、会员运营、门店执行和活动高峰承载',
      '方案要能解释总部、区域、门店、电商和客服等角色如何协同',
      '客户通常更关注上线速度和业务效果，演示必须贴近真实运营流程'
    ],
    mustAsk: [
      '核心指标是增长、降本、提效、控损，还是体验改善？',
      '线上、线下、仓配、客服和财务数据是否需要打通？',
      '培训推广由总部统一推进，还是门店分批落地？'
    ],
    proof: ['业务指标拆解', '运营流程演示', '培训推广计划', '高峰容量假设']
  },
  manufacturing: {
    label: '制造/供应链',
    angles: [
      '强调计划协同、库存周转、质量追溯、供应商协同和系统集成',
      '不能只讲单点系统，要解释与ERP、MES、WMS、SRM等系统的边界',
      '客户通常重视稳定性和变更成本，方案要给出分阶段替换或并行策略'
    ],
    mustAsk: [
      '当前瓶颈在计划、采购、生产、仓储、质量还是交付？',
      '哪些主数据和接口是上线前必须打通的？',
      '是否允许分阶段上线，还是必须一次性切换？'
    ],
    proof: ['系统边界图', '主数据治理方案', '接口清单', '分阶段上线计划']
  },
  finance: {
    label: '金融/强监管',
    angles: [
      '强调合规、风控、审计、权限、数据隔离和稳定性',
      '方案表达要减少概念化创新，增加可审计、可追溯、可回滚的控制点',
      '采购周期和安全评审较重，售前要提前准备合规证据和风险说明'
    ],
    mustAsk: [
      '安全、合规、审计和业务连续性分别由谁把关？',
      '是否涉及敏感数据、跨域流转或模型使用限制？',
      '上线前需要完成哪些内审、压测或备案动作？'
    ],
    proof: ['合规映射表', '权限模型', '审计日志设计', '回滚与容灾方案']
  },
  generic: {
    label: '通用企业服务',
    angles: [
      '先抓业务目标，再落到范围、集成、数据、组织和验收',
      '避免把方案写成产品说明书，要让客户看到组织如何使用',
      '把不可控风险前置说明，减少签约后交付争议'
    ],
    mustAsk: [
      '客户当前最想解决的业务问题是什么？',
      '谁使用、谁维护、谁验收、谁承担推广责任？',
      '上线后如何判断项目成功？'
    ],
    proof: ['业务蓝图', '角色权限表', '里程碑计划', '验收标准']
  }
};

const COMPETITOR_STRATEGIES = {
  platform: {
    label: '平台型厂商',
    tactics: [
      '不正面对比全栈能力，聚焦行业场景深度、交付响应和定制边界',
      '指出平台方案常见风险：标准能力强，但行业流程需要二次设计',
      '用客户组织角色和落地计划证明你更贴近业务现场'
    ]
  },
  legacy: {
    label: '传统套件厂商',
    tactics: [
      '强调迭代速度、用户体验、轻量集成和新技术适配',
      '避免攻击历史系统，表达为“保留稳定底座，补齐新业务能力”',
      '用分阶段替换方案降低客户的迁移焦虑'
    ]
  },
  lowPrice: {
    label: '低价竞争者',
    tactics: [
      '把对比从采购价拉回总成本：实施、培训、集成、运维和返工',
      '要求客户确认同等范围、同等服务、同等验收标准后再比价',
      '用风险清单解释为什么低价不等于低成本'
    ]
  },
  niche: {
    label: '垂直小厂商',
    tactics: [
      '承认其单点能力可能灵活，但强调组织级交付、持续服务和系统扩展',
      '突出项目治理、文档、验收和长期运维能力',
      '用路线图说明客户未来扩展时不会被单点方案锁死'
    ]
  },
  peer: {
    label: '同类竞品',
    tactics: [
      '减少功能表格拉踩，转向行业理解、实施路径和风险控制',
      '准备三类差异：业务场景差异、交付方法差异、长期运营差异',
      '把客户内部决策语言统一成“价值、风险、周期、成本”四项'
    ]
  }
};

const SELF_CHECKLIST = [
  { id: 'C01', category: '行业洞察', question: '方案是否说明该行业的核心业务约束，而不只是列产品功能？', weight: 12, failWarning: '客户会认为你不了解行业，只是在套模板。' },
  { id: 'C02', category: '客户理解', question: '是否识别了需求发起人、评估影响人、最终拍板人和反对者？', weight: 14, failWarning: '决策链不清，方案可能传不到真正拍板人。' },
  { id: 'C03', category: '业务价值', question: '是否把客户的小需求翻译成业务问题和可衡量目标？', weight: 15, failWarning: '停留在功能层，容易被拉入低价比较。' },
  { id: 'C04', category: '竞争策略', question: '是否准备了竞品差异，但没有使用攻击性表达？', weight: 10, failWarning: '没有差异就只能比价格，攻击竞品会降低专业感。' },
  { id: 'C05', category: '交付边界', question: '是否明确范围、数据、集成、培训、验收和运维边界？', weight: 13, failWarning: '售前承诺不清会在交付阶段变成争议。' },
  { id: 'C06', category: '行业证据', question: '是否准备了行业化证明材料，而不是泛泛成功案例？', weight: 10, failWarning: '缺少证明材料会让方案停留在观点层。' },
  { id: 'C07', category: '现场控制', question: '是否设计了提问顺序，让客户从现状、影响、目标逐步展开？', weight: 9, failWarning: '现场容易被客户带着跳功能细节。' },
  { id: 'C08', category: '商务风险', question: '是否明确哪些优惠、免费服务或额外承诺需要交换条件？', weight: 11, failWarning: '没有交换条件的让步会降低成交质量。' },
  { id: 'C09', category: '下一步', question: '方案汇报后是否有明确推进动作和责任人？', weight: 10, failWarning: '没有下一步，客户会把方案放进待比较清单。' }
];

const RISK_RULES = [
  { match: ['预算模糊', '没有预算', '预算未知'], score: 18, warning: '预算口径不清：先确认资金来源、审批路径和采购时间。' },
  { match: ['对接人非决策层', '拍板人不露面', '决策人不露面'], score: 16, warning: '决策链不透明：需要设计触达拍板人的汇报材料或会议。' },
  { match: ['多家POC', '多家竞品', '同时测试'], score: 14, warning: '多方并行评估：必须争取统一评估标准，避免变成无边界比价。' },
  { match: ['需求反复', '方案多次修改', '范围扩大'], score: 12, warning: '需求边界漂移：需要用纪要和版本边界控制投入。' },
  { match: ['只要报价', '重新比价', '压价'], score: 12, warning: '价格导向增强：把对话拉回同等范围和总成本。' },
  { match: ['业务方缺席', '只有IT'], score: 10, warning: '业务方缺席：方案价值可能无法被内部传播。' }
];

const EXPERIENCE_TIPS = [
  '行业普遍教训：客户说“先给个完整方案看看”时，先确认用途。未确认决策路径前，不要投入重方案。',
  '实战经验总结：政府类客户更怕风险失控，零售类客户更怕上线慢和业务不中用，方案语言要分别调整。',
  '行业普遍教训：POC前没有通过标准，POC后就很难形成采购结论。',
  '实战经验总结：商务让步必须绑定范围、付款或周期，否则交付阶段会变成隐性成本。',
  '行业普遍教训：方案赢在客户能复述你的价值，而不是你讲完了多少页材料。'
];

function normalizeStage(stage) {
  if (!stage) return '需求期';
  if (stage === 'POC') return 'POC阶段';
  return STAGE_RULES[stage] ? stage : '需求期';
}

function detectIndustry(industry = '') {
  const text = String(industry).toLowerCase();
  if (/政府|政务|公共|应急|监管/.test(text)) return 'government';
  if (/零售|快消|消费|连锁|门店|电商|餐饮/.test(text)) return 'retail';
  if (/制造|供应链|工厂|生产|仓储|物流/.test(text)) return 'manufacturing';
  if (/金融|银行|保险|证券|支付|风控/.test(text)) return 'finance';
  return 'generic';
}

function classifyCompetitor(name = '') {
  const text = String(name).toLowerCase();
  if (/云|平台|大厂|全栈|生态/.test(text)) return 'platform';
  if (/erp|传统|套件|老牌/.test(text)) return 'legacy';
  if (/低价|便宜|报价低|免费/.test(text)) return 'lowPrice';
  if (/垂直|小厂|创业|单点|轻量/.test(text)) return 'niche';
  return 'peer';
}

function calculateRiskScore(signals = []) {
  let score = 100;
  const warnings = [];
  const joined = signals.filter(Boolean).join(' ');

  for (const rule of RISK_RULES) {
    if (rule.match.some(keyword => joined.includes(keyword))) {
      score -= rule.score;
      warnings.push(rule.warning);
    }
  }

  score = Math.max(0, score);
  return {
    score,
    level: score >= 85 ? '健康' : score >= 70 ? '可控' : score >= 55 ? '需关注' : '高风险',
    warnings
  };
}

function generateBlueprint(input = {}) {
  const client = input.client || '未命名客户';
  const industry = input.industry || '通用行业';
  const stage = normalizeStage(input.stage);
  const budget = input.budget || '未明确';
  const competitors = Array.isArray(input.competitors) ? input.competitors.filter(Boolean) : [];
  const signals = Array.isArray(input.signals) ? input.signals.filter(Boolean) : [];
  const industryKey = detectIndustry(industry);
  const industryPlaybook = INDUSTRY_PLAYBOOKS[industryKey];
  const stageRule = STAGE_RULES[stage];
  const riskAssessment = calculateRiskScore([...signals, ...stageRule.riskSignals.filter(s => signals.includes(s))]);

  return {
    client,
    industry,
    stage,
    budget,
    decisionRole: input.decisionRole || '未明确',
    stageAnalysis: {
      label: stage,
      summary: stageRule.summary,
      focusItems: stageRule.focus,
      actionPlan: stageRule.actionPlan,
      winCondition: stageRule.winCondition,
      riskSignals: stageRule.riskSignals
    },
    industryPlaybook,
    competitorStrategy: competitors.map(competitor => {
      const type = classifyCompetitor(competitor);
      return {
        competitor,
        type: COMPETITOR_STRATEGIES[type].label,
        tactics: COMPETITOR_STRATEGIES[type].tactics
      };
    }),
    riskAssessment,
    selfChecklist: {
      mustFix: SELF_CHECKLIST.filter(item => item.weight >= 10),
      niceToHave: SELF_CHECKLIST.filter(item => item.weight < 10)
    },
    nextMoves: [
      '用行业问题清单补一次客户访谈',
      '把方案改成“业务目标-场景路径-交付边界-验收证据”结构',
      '确认下一次会议的参会角色和推进动作'
    ],
    tip: EXPERIENCE_TIPS[Math.floor(Math.random() * EXPERIENCE_TIPS.length)]
  };
}

module.exports = {
  generateBlueprint,
  STAGE_RULES,
  INDUSTRY_PLAYBOOKS,
  COMPETITOR_STRATEGIES,
  SELF_CHECKLIST,
  calculateRiskScore,
  detectIndustry,
  classifyCompetitor
};
