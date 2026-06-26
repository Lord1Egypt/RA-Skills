import type { Priority, ServiceLine } from '../shared.js';
import { clamp, priorityFromScore } from '../shared.js';
import { pickPersona } from './personas.js';

/**
 * 财税获客线索打分。
 * 维度（满分 100）：规模 25 + 行业 15 + 区域 10 + 痛点信号 25 + 决策人级别 15 + 时机信号 10。
 */

export interface LeadInput {
  name: string;
  industry?: string;
  region?: string;
  employees?: number;
  revenue_wan?: number;
  decision_maker_role?: string;
  notes?: string;
  /** 上次接触日期 yyyy-mm-dd（用于 followup 决策，打分阶段不使用）。 */
  last_contact?: string;
  stage?: string;
}

export interface ScoredLead {
  name: string;
  score: number;
  priority: Priority;
  reasons: string[];
  recommended_services: ServiceLine[];
  hook: string;
  persona: string;
}

const PAINPOINT_KEYWORDS: Array<{ kw: string; weight: number; tag: string }> = [
  { kw: '汇算清缴', weight: 18, tag: '汇算清缴时点' },
  { kw: '高新', weight: 15, tag: '高新认定窗口' },
  { kw: '研发加计', weight: 14, tag: '研发加计扣除' },
  { kw: '股改', weight: 20, tag: '股改/拟上市' },
  { kw: '上市', weight: 22, tag: '拟上市' },
  { kw: 'IPO', weight: 22, tag: '拟上市' },
  { kw: '稽查', weight: 18, tag: '稽查风险' },
  { kw: '补税', weight: 15, tag: '补税整改' },
  { kw: '出口退税', weight: 16, tag: '出口退税' },
  { kw: '跨境', weight: 12, tag: '跨境业务' },
  { kw: '关联交易', weight: 14, tag: '关联交易合规' },
  { kw: '税务筹划', weight: 12, tag: '税务筹划意向' },
  { kw: '代账', weight: 10, tag: '代账需求' },
  { kw: '社保', weight: 8, tag: '社保合规' },
  { kw: '发票', weight: 8, tag: '发票合规' },
  { kw: '审计', weight: 12, tag: '审计需求' },
];

const TIMING_KEYWORDS: Array<{ kw: string; weight: number; tag: string }> = [
  { kw: '年报', weight: 10, tag: '年报临近' },
  { kw: '季度', weight: 6, tag: '季度申报' },
  { kw: '马上', weight: 8, tag: '紧迫诉求' },
  { kw: '近期', weight: 5, tag: '中期窗口' },
  { kw: '明年', weight: 7, tag: '中长期规划' },
];

const HIGH_VALUE_INDUSTRY = [
  '医疗', '生物', '半导体', '新能源', '芯片', '智能制造', '高端装备',
  '电子信息', '航空', '航天', '人工智能', '互联网', '软件', 'SaaS',
];

function scoreSize(input: LeadInput): { score: number; reason: string } {
  const e = input.employees ?? 0;
  const r = input.revenue_wan ?? 0;
  if (r >= 50000 || e >= 1000) return { score: 25, reason: '集团规模 → 高客单财税顾问场景' };
  if (r >= 5000 || e >= 200) return { score: 22, reason: '中大型企业 → 适合审计+筹划' };
  if (r >= 500 || e >= 20) return { score: 18, reason: '成长企业 → 代账升级 + 汇算清缴' };
  if (r > 0 || e > 0) return { score: 12, reason: '小微 → 代账刚需' };
  return { score: 6, reason: '规模未知，先视为基础代账线索' };
}

function scoreIndustry(input: LeadInput): { score: number; reason: string } {
  const ind = (input.industry ?? '').toLowerCase();
  if (!ind) return { score: 4, reason: '行业未知' };
  if (HIGH_VALUE_INDUSTRY.some((k) => ind.includes(k.toLowerCase()))) {
    return { score: 15, reason: `高价值行业（${input.industry}）→ 大概率有研发加计 / 高新` };
  }
  if (/外贸|出口|跨境|外资/.test(ind)) {
    return { score: 13, reason: '外贸/外资 → 出口退税与跨境财税场景' };
  }
  if (/制造|化工|建筑|物流/.test(ind)) {
    return { score: 10, reason: '传统行业 → 增值税链条复杂，合规体检价值高' };
  }
  return { score: 7, reason: '一般行业，按通用方向跟进' };
}

function scoreRegion(input: LeadInput, defaultRegion: string): { score: number; reason: string } {
  const r = input.region ?? '';
  if (!r) return { score: 3, reason: '区域未知' };
  if (r.includes(defaultRegion)) return { score: 10, reason: `本地客户（${r}）→ 现场服务便利` };
  if (/山东|济南|烟台|威海|潍坊|青岛/.test(r)) return { score: 8, reason: `省内（${r}）→ 服务半径合理` };
  return { score: 5, reason: `异地（${r}）→ 远程服务可行但优先级降一档` };
}

function scorePainpoints(input: LeadInput): { score: number; reasons: string[]; tags: string[] } {
  const text = `${input.notes ?? ''} ${input.stage ?? ''}`.toLowerCase();
  let total = 0;
  const reasons: string[] = [];
  const tags: string[] = [];
  for (const { kw, weight, tag } of PAINPOINT_KEYWORDS) {
    if (text.includes(kw.toLowerCase())) {
      total += weight;
      reasons.push(`命中"${kw}" → ${tag}`);
      tags.push(tag);
    }
  }
  return { score: clamp(total, 0, 25), reasons, tags };
}

function scoreDecisionMaker(input: LeadInput): { score: number; reason: string } {
  const role = (input.decision_maker_role ?? '').toLowerCase();
  if (!role) return { score: 3, reason: '决策人未知' };
  if (/老板|创始人|董事长|ceo|cfo/.test(role)) return { score: 15, reason: '一把手/CFO → 决策周期短' };
  if (/总监|总经理|vp/.test(role)) return { score: 12, reason: '总监级 → 推动力强' };
  if (/经理|主管/.test(role)) return { score: 8, reason: '中层 → 需要向上推动' };
  if (/会计|出纳|文员/.test(role)) return { score: 4, reason: '执行层 → 决策链路长' };
  return { score: 5, reason: '决策人级别一般' };
}

function scoreTiming(input: LeadInput): { score: number; reasons: string[] } {
  const text = `${input.notes ?? ''} ${input.stage ?? ''}`.toLowerCase();
  let total = 0;
  const reasons: string[] = [];
  for (const { kw, weight, tag } of TIMING_KEYWORDS) {
    if (text.includes(kw.toLowerCase())) {
      total += weight;
      reasons.push(`时机"${kw}" → ${tag}`);
    }
  }
  return { score: clamp(total, 0, 10), reasons };
}

function recommendServices(
  input: LeadInput,
  painTags: string[],
  available: ServiceLine[],
): ServiceLine[] {
  const candidates = new Set<ServiceLine>();
  if (painTags.includes('汇算清缴时点')) candidates.add('汇算清缴');
  if (painTags.includes('高新认定窗口')) candidates.add('高新申报');
  if (painTags.includes('研发加计扣除')) candidates.add('税务筹划');
  if (painTags.includes('股改/拟上市') || painTags.includes('拟上市')) {
    candidates.add('IPO辅导');
    candidates.add('股权架构');
    candidates.add('审计');
  }
  if (painTags.includes('稽查风险') || painTags.includes('补税整改')) {
    candidates.add('财税顾问');
    candidates.add('审计');
  }
  if (painTags.includes('出口退税')) candidates.add('财税顾问');
  if ((input.employees ?? 0) <= 20 && candidates.size === 0) candidates.add('代账');
  if (candidates.size === 0) candidates.add('代账');

  const filtered = Array.from(candidates).filter((s) => available.includes(s));
  return filtered.length > 0 ? filtered : [available[0]];
}

export function scoreLead(
  input: LeadInput,
  config: { region: string; services: ServiceLine[] },
): ScoredLead {
  const size = scoreSize(input);
  const ind = scoreIndustry(input);
  const reg = scoreRegion(input, config.region);
  const pain = scorePainpoints(input);
  const dm = scoreDecisionMaker(input);
  const tim = scoreTiming(input);

  const total = clamp(size.score + ind.score + reg.score + pain.score + dm.score + tim.score, 0, 100);
  const reasons = [
    `规模 ${size.score} —— ${size.reason}`,
    `行业 ${ind.score} —— ${ind.reason}`,
    `区域 ${reg.score} —— ${reg.reason}`,
    ...(pain.reasons.length > 0 ? [`痛点信号 ${pain.score} —— ${pain.reasons.join('；')}`] : [`痛点信号 0 —— 未在备注中识别到关键词`]),
    `决策人 ${dm.score} —— ${dm.reason}`,
    ...(tim.reasons.length > 0 ? [`时机 ${tim.score} —— ${tim.reasons.join('；')}`] : []),
  ];

  const persona = pickPersona({
    employees: input.employees,
    revenue_wan: input.revenue_wan,
    industry: input.industry,
    stage: input.stage,
    notes: input.notes,
  });
  const recommended = recommendServices(input, pain.tags, config.services);
  const hook = persona.hooks[0];

  return {
    name: input.name,
    score: total,
    priority: priorityFromScore(total),
    reasons,
    recommended_services: recommended,
    hook,
    persona: persona.display,
  };
}
