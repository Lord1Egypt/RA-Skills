import type { ServiceLine } from '../shared.js';

/**
 * 5 类财税客户画像。
 * 用于 sales_lead_brief 工具：把已知的 lead 字段（员工数/年营收/行业/阶段）映射到画像，
 * 再据此推断痛点、推荐服务、决策人优先级、切入话术 hook。
 */

export interface Persona {
  id: 'startup' | 'growth' | 'pre_ipo' | 'group' | 'foreign_trade';
  display: string;
  /** 用于自动匹配的判定条件（任一命中即归到此画像；多个画像命中时按数组顺序优先）。 */
  match: {
    employees_max?: number;
    employees_min?: number;
    revenue_max_wan?: number;
    revenue_min_wan?: number;
    industry_keywords?: string[];
    stage_keywords?: string[];
  };
  pain_points: string[];
  recommended_services: ServiceLine[];
  /** 决策人按优先级排序，第一个最重要。 */
  decision_makers: string[];
  /** 切入话术的开场 hook（具体写法在 pitch_templates 里）。 */
  hooks: string[];
}

export const PERSONAS: Persona[] = [
  {
    id: 'startup',
    display: '初创小微',
    match: { employees_max: 20, revenue_max_wan: 500 },
    pain_points: [
      '没有专职财务，老板自己记账或亲戚兼职',
      '工商税务流程不熟，被税务通知后才补',
      '发票开具、社保公积金缴纳容易踩坑',
      '想做高新认定/研发加计但不知从何下手',
    ],
    recommended_services: ['代账', '高新申报', '税务筹划'],
    decision_makers: ['老板/创始人', '联合创始人', '行政'],
    hooks: [
      '同行业很多老板都是被税务通知过一次，才意识到代账不只是"做账"，是"挡子弹"',
      '高新认定省的所得税，能直接抵掉两三年的代账费',
      '老板自己记账踩过的坑，我们三句话就能列清楚',
    ],
  },
  {
    id: 'growth',
    display: '成长成熟',
    match: { employees_min: 20, employees_max: 200, revenue_min_wan: 500, revenue_max_wan: 5000 },
    pain_points: [
      '账越做越复杂，财务团队人手不够',
      '想做税务筹划但担心被认定为偷漏税',
      '汇算清缴每年都赶在截止日前焦头烂额',
      '税务稽查风险逐年加大，需要合规体检',
      '研发费加计扣除做了但不规范，怕被翻账',
    ],
    recommended_services: ['代账', '审计', '汇算清缴', '税务筹划', '财税顾问'],
    decision_makers: ['财务总监', '财务经理', '老板', 'CFO'],
    hooks: [
      '汇算清缴前 30 天我们做合规体检，只查 7 个高风险点，比稽查抢先一步',
      '研发加计扣除做规范了，每 100 万研发费多省 25 万所得税',
      '账上看起来漂亮但增值税链条断了 —— 这是稽查重点',
    ],
  },
  {
    id: 'pre_ipo',
    display: '上市辅导',
    match: {
      employees_min: 200,
      revenue_min_wan: 5000,
      stage_keywords: ['股改', 'pre-IPO', '拟上市', '辅导期', '挂牌'],
    },
    pain_points: [
      '股改前历史账务混乱，需要追溯调整',
      '关联交易未规范，证监会问询会要',
      '股权激励落地难，税务成本高',
      '审计师对内控提的建议落不下去',
      '合并报表口径不统一，子公司账质量参差',
    ],
    recommended_services: ['IPO辅导', '审计', '股权架构', '税务筹划', '财税顾问'],
    decision_makers: ['CFO', '董秘', '财务总监', '老板'],
    hooks: [
      '股改前先做"历史合规体检"，比辅导期被问询时再补便宜十倍',
      '股权激励的税务方案能省 30%+ 个税，但必须在授予前设计',
      '关联交易"实质性披露"是问询函的高频点，提前准备好基础资料',
    ],
  },
  {
    id: 'group',
    display: '集团 / 大型企业',
    match: { employees_min: 1000, revenue_min_wan: 50000 },
    pain_points: [
      '多公司合并报表口径不统一',
      '跨境业务转移定价被税务关注',
      '历史税务争议悬而未决',
      '税务数字化体系待建设',
      '集团内重组、分立、合并的税务影响复杂',
    ],
    recommended_services: ['财税顾问', '审计', '股权架构', '税务筹划'],
    decision_makers: ['CFO', '集团财务总监', '税务总监'],
    hooks: [
      '集团 BU 结算价的税务定性，决定了未来三年的所得税地图',
      '跨境转移定价文档能从被动应对变主动防御',
      '集团重组的税务方案做一个特殊性税务处理备案，能省一笔大的',
    ],
  },
  {
    id: 'foreign_trade',
    display: '外贸 / 外资',
    match: {
      industry_keywords: ['外贸', '出口', '进口', '跨境', '外资', '中外合资', 'WFOE'],
    },
    pain_points: [
      '出口退税流程慢，资金占用大',
      '汇兑损益处理不规范',
      '跨境劳务/特许权使用费税务认定不清',
      '关联企业转让定价文档缺失',
      '外汇核销与海关申报数据对不上',
    ],
    recommended_services: ['财税顾问', '税务筹划', '代账', '审计'],
    decision_makers: ['财务总监', 'CFO', '老板', '外贸经理'],
    hooks: [
      '出口退税平均提速 14 天，对外贸现金流就是真金白银',
      '汇兑损益每年都算错的口径，我们一次性给你定一个三年内不用改的',
      '跨境特许权使用费的扣缴，操作不当多缴 10% 增值税',
    ],
  },
];

export function pickPersona(input: {
  employees?: number;
  revenue_wan?: number;
  industry?: string;
  stage?: string;
  notes?: string;
}): Persona {
  const text = `${input.industry ?? ''} ${input.stage ?? ''} ${input.notes ?? ''}`.toLowerCase();
  for (const p of PERSONAS) {
    const m = p.match;
    if (m.employees_min !== undefined && (input.employees ?? 0) < m.employees_min) continue;
    if (m.employees_max !== undefined && (input.employees ?? Number.MAX_SAFE_INTEGER) > m.employees_max) continue;
    if (m.revenue_min_wan !== undefined && (input.revenue_wan ?? 0) < m.revenue_min_wan) continue;
    if (m.revenue_max_wan !== undefined && (input.revenue_wan ?? Number.MAX_SAFE_INTEGER) > m.revenue_max_wan) continue;
    if (m.industry_keywords && !m.industry_keywords.some((kw) => text.includes(kw.toLowerCase()))) continue;
    if (m.stage_keywords && !m.stage_keywords.some((kw) => text.includes(kw.toLowerCase()))) continue;
    return p;
  }
  return PERSONAS[1];
}
