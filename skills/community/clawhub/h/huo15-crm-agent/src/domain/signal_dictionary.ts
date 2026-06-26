/**
 * 财税行业意向信号词典（finance_tax 领域包 v0.2）
 *
 * 5 大类信号（招标 / 招聘 / 融资 / 经营变更 / 风险），每条命中加权到 lead score。
 *
 * 设计：
 * - 词条用关键词字面匹配（substring，不 regex），简单稳定。
 * - 单条 weight 0-25；total_weight cap 100。
 * - 高权重 = 强意向（直接采购财税服务）；低权重 = 弱信号（潜在）。
 * - hint 字段是"财税解读" —— 销售看到 hint 知道为什么这条信号有效。
 *
 * 这是绿火相对通用拓客 SaaS 的核心护城河：行业 know-how 编码到词典里。
 * 通用拓客平台只能识别"招聘会计"，绿火能识别"招聘会计 → 内部财务升级
 * → 可能外包代账"。
 */

export type SignalCategory = 'tender' | 'recruit' | 'finance' | 'change' | 'risk';

export interface SignalEntry {
  /** 关键词字面（substring 匹配），中文为主。 */
  term: string;
  category: SignalCategory;
  /** 0-25。25 = 直接采购财税服务，最高优先级。 */
  weight: number;
  /** 财税解读：销售看到这条信号知道下一步切入什么。 */
  hint: string;
}

export const FINANCE_TAX_SIGNALS: SignalEntry[] = [
  // ── 招标信号（最强意向 —— 客户主动公告要采购财税服务）──
  { term: '代理记账服务', category: 'tender', weight: 25, hint: '直接采购代账，最高优先级' },
  { term: '税务咨询服务', category: 'tender', weight: 23, hint: '直接采购财税顾问' },
  { term: '审计服务采购', category: 'tender', weight: 24, hint: '需要审计师，可推 IPO 辅导切入' },
  { term: 'IPO辅导', category: 'tender', weight: 25, hint: '股改 / 上市辅导客户' },
  { term: 'IPO 辅导', category: 'tender', weight: 25, hint: '股改 / 上市辅导客户' },
  { term: '股改', category: 'tender', weight: 22, hint: '股份制改造，IPO / 股权架构需求' },
  { term: '高新认定', category: 'tender', weight: 20, hint: '高新技术企业认定，可推税务筹划' },
  { term: '研发加计扣除', category: 'tender', weight: 20, hint: '研发费加计扣除合规辅导' },
  { term: '汇算清缴', category: 'tender', weight: 18, hint: '汇算清缴期合规体检' },
  { term: '中标公告', category: 'tender', weight: 12, hint: '中标方需要做账，潜在代账机会' },
  { term: '采购公告', category: 'tender', weight: 8, hint: '采购方需要做账' },

  // ── 招聘信号（中强意向 —— 内部财税体系变动）──
  { term: '招聘 IPO', category: 'recruit', weight: 22, hint: '拟上市企业，IPO 辅导黄金客户' },
  { term: '招聘CFO', category: 'recruit', weight: 18, hint: 'CFO 招聘，财税体系重组窗口' },
  { term: '招聘 CFO', category: 'recruit', weight: 18, hint: 'CFO 招聘，财税体系重组窗口' },
  { term: '招聘财务总监', category: 'recruit', weight: 15, hint: '财务领导层升级，外包筹划机会' },
  { term: '招聘财务负责人', category: 'recruit', weight: 14, hint: '财务领导层换人，可能外包代账' },
  { term: '招聘审计', category: 'recruit', weight: 13, hint: '内审升级，可推审计 / 筹划' },
  { term: '招聘税务', category: 'recruit', weight: 14, hint: '税务专员需求，可能外包筹划' },
  { term: '招聘会计', category: 'recruit', weight: 12, hint: '内部会计需求，可能外包代账或工具升级' },
  { term: '招聘出纳', category: 'recruit', weight: 8, hint: '基础财务岗，外包代账可能性中等' },

  // ── 融资信号（中强意向 —— 资本动作驱动财税升级）──
  { term: 'Pre-IPO', category: 'finance', weight: 25, hint: '上市前夕，IPO 辅导 + 审计高需求' },
  { term: '战略投资', category: 'finance', weight: 16, hint: '股权变动，需要重组方案' },
  { term: 'B 轮', category: 'finance', weight: 18, hint: 'B 轮成长期，财税筹划高需求' },
  { term: 'B轮', category: 'finance', weight: 18, hint: 'B 轮成长期，财税筹划高需求' },
  { term: 'C 轮', category: 'finance', weight: 20, hint: 'C 轮规模化，IPO 准备窗口' },
  { term: 'C轮', category: 'finance', weight: 20, hint: 'C 轮规模化，IPO 准备窗口' },
  { term: 'A 轮', category: 'finance', weight: 15, hint: 'A 轮，需要规范财务做尽调' },
  { term: 'A轮', category: 'finance', weight: 15, hint: 'A 轮，需要规范财务做尽调' },
  { term: '挂牌', category: 'finance', weight: 22, hint: '新三板 / 北交所挂牌，财税合规高优先' },

  // ── 经营变更信号（中等意向 —— 工商动作触发财税审视）──
  { term: '注册资本变更', category: 'change', weight: 12, hint: '股本变动，可能涉及税务筹划' },
  { term: '注册资本增加', category: 'change', weight: 14, hint: '增资，印花税 / 实缴入资合规' },
  { term: '股东变更', category: 'change', weight: 13, hint: '股权变更，个税 / 转让税筹划机会' },
  { term: '法人变更', category: 'change', weight: 10, hint: '决策层变动，可能换代账' },
  { term: '新设分公司', category: 'change', weight: 14, hint: '扩张，新主体需要做账' },
  { term: '新设子公司', category: 'change', weight: 15, hint: '扩张 + 跨主体，集团财税方案' },
  { term: '迁址', category: 'change', weight: 7, hint: '地址变更，税务登记调整' },
  { term: '注销', category: 'change', weight: 8, hint: '注销流程涉及税务清算服务' },

  // ── 风险信号（强意向 —— 已经踩坑或即将踩坑，需合规救火）──
  { term: '税务行政处罚', category: 'risk', weight: 22, hint: '直接税务问题，强意向救火' },
  { term: '欠税公告', category: 'risk', weight: 20, hint: '直接税务问题' },
  { term: '行政处罚', category: 'risk', weight: 16, hint: '可能税务违规，需要合规咨询' },
  { term: '经营异常', category: 'risk', weight: 14, hint: '工商异常，可能换代账' },
  { term: '严重违法', category: 'risk', weight: 12, hint: '黑名单风险，谨慎触达' },
  { term: '法人被限高', category: 'risk', weight: 6, hint: '高风险企业，谨慎触达，但有合规需求' },
  { term: '失信', category: 'risk', weight: 5, hint: '失信主体，触达需评估' },
];

export interface SignalMatch {
  category: SignalCategory;
  /** 命中的词典 term。 */
  term: string;
  /** 0-25。 */
  weight: number;
  /** 该词条的财税解读。 */
  hint: string;
  /** raw_texts 数组下标。 */
  raw_text_idx: number;
  /** 命中处的上下文片段（前后 30 字符）。 */
  snippet: string;
}

/**
 * 在一段文本里扫描所有信号。
 * 同一 term 在同一 text 内只计一次（避免单文本反复加权）。
 */
function scanText(text: string, idx: number, allowed: Set<SignalCategory>): SignalMatch[] {
  const hits: SignalMatch[] = [];
  const seen = new Set<string>();
  for (const entry of FINANCE_TAX_SIGNALS) {
    if (!allowed.has(entry.category)) continue;
    if (seen.has(entry.term)) continue;
    const pos = text.indexOf(entry.term);
    if (pos === -1) continue;
    seen.add(entry.term);
    const start = Math.max(0, pos - 30);
    const end = Math.min(text.length, pos + entry.term.length + 30);
    hits.push({
      category: entry.category,
      term: entry.term,
      weight: entry.weight,
      hint: entry.hint,
      raw_text_idx: idx,
      snippet: text.slice(start, end),
    });
  }
  return hits;
}

export function matchSignals(
  rawTexts: string[],
  categories?: SignalCategory[],
): SignalMatch[] {
  const allowed: Set<SignalCategory> = new Set(
    categories && categories.length > 0
      ? categories
      : ['tender', 'recruit', 'finance', 'change', 'risk'],
  );
  const all: SignalMatch[] = [];
  rawTexts.forEach((t, i) => {
    all.push(...scanText(t, i, allowed));
  });
  return all;
}

/** 把一组 matches 聚合成 total_weight + 推断意向等级。 */
export function summarizeSignals(matches: SignalMatch[]): {
  total_weight: number;
  inferred_intent: '高' | '中' | '低' | '无';
  by_category: Record<SignalCategory, number>;
} {
  const by_category: Record<SignalCategory, number> = {
    tender: 0, recruit: 0, finance: 0, change: 0, risk: 0,
  };
  let total = 0;
  // 同一 term 跨多个 text 命中时，权重递减（avoid 单一信号刷分）：
  // 第 1 次 100% / 第 2 次 50% / 第 3 次以后 25%。
  const termCount = new Map<string, number>();
  for (const m of matches) {
    const seen = termCount.get(m.term) ?? 0;
    const factor = seen === 0 ? 1 : seen === 1 ? 0.5 : 0.25;
    const adjusted = Math.round(m.weight * factor);
    total += adjusted;
    by_category[m.category] += adjusted;
    termCount.set(m.term, seen + 1);
  }
  total = Math.min(total, 100);
  const inferred_intent: '高' | '中' | '低' | '无' =
    total >= 60 ? '高' : total >= 30 ? '中' : total > 0 ? '低' : '无';
  return { total_weight: total, inferred_intent, by_category };
}
