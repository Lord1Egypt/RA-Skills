import { Model } from './types';
import modelsData from '../data/models-full.json';

/**
 * 模型评分结果
 * 
 * 包含模型的评分、推荐理由和完整的模型配置。
 */
export interface ModelScore {
  /** 模型 ID */
  modelId: string;
  /** 评分（0-100） */
  score: number;
  /** 推荐理由 */
  reason: string;
  /** 完整的模型配置 */
  model: Model;
}

/**
 * 输入特征提取结果
 * 
 * 从用户输入中提取的决策特征，用于智能推荐模型。
 * 每个特征对应一类决策要素（如风险、价值、竞争等）。
 */
interface InputFeatures {
  /** 是否提到风险相关词汇 */
  hasRisk: boolean;
  /** 是否表达不确定性 */
  hasUncertainty: boolean;
  /** 是否涉及价值评估 */
  hasValue: boolean;
  /** 是否涉及竞争分析 */
  hasCompetition: boolean;
  /** 是否包含情绪化表达 */
  hasEmotion: boolean;
  /** 是否有从众倾向 */
  hasHerd: boolean;
  /** 是否关注长期 */
  hasLongTerm: boolean;
  /** 是否关注短期 */
  hasShortTerm: boolean;
  /** 是否涉及资源成本 */
  hasResource: boolean;
  /** 是否涉及机会选择 */
  hasOpportunity: boolean;
  /** 是否涉及激励机制 */
  hasIncentive: boolean;
  /** 是否涉及信任问题 */
  hasTrust: boolean;
}

/**
 * 智能推荐引擎
 * 
 * 基于用户输入的语义特征和场景上下文，智能评分并推荐最相关的思维模型。
 * 
 * 推荐算法：
 * 1. 特征提取：从用户输入中提取 12 种决策特征
 * 2. 基础评分：所有模型起始分 50 分
 * 3. 场景加分：根据场景类型给特定模型加分（最高 20 分）
 * 4. 特征加分：根据输入特征给相关模型加分（最高 30 分）
 * 5. 排序筛选：按评分降序排列，返回 Top 5
 * 
 * @example
 * ```typescript
 * const recommender = new SmartRecommender();
 * const scores = await recommender.analyzeAndScore(
 *   '大家都在买这只股票，我要不要跟？',
 *   'investment'
 * );
 * // 返回评分最高的 5 个模型
 * console.log(scores[0].model.name); // '从众心理'
 * console.log(scores[0].score); // 85
 * console.log(scores[0].reason); // '存在从众倾向，保持独立思考'
 * ```
 */
export class SmartRecommender {
  /** 思维模型配置列表（从 models-full.json 加载） */
  private models: Model[];
  
  /**
   * 构造函数
   * 
   * 从 models-full.json 文件加载完整的思维模型配置。
   */
  constructor() {
    this.models = (modelsData as any).models;
  }
  
  /**
   * 分析并评分（主入口）
   * 
   * 根据用户输入和场景类型，智能推荐最相关的思维模型。
   * 
   * @param userInput - 用户输入的决策问题
   * @param scenarioId - 场景 ID（如 'investment', 'product' 等）
   * @returns 评分结果数组（Top 5，按评分降序）
   * 
   * @example
   * ```typescript
   * const scores = await recommender.analyzeAndScore(
   *   '这个产品值得投资吗？风险大不大？',
   *   'investment'
   * );
   * ```
   */
  async analyzeAndScore(userInput: string, scenarioId: string): Promise<ModelScore[]> {
    // 1. 提取输入特征
    const features = this.extractFeatures(userInput);
    // 2. 计算所有模型的评分
    const scores = this.calculateScores(features, scenarioId);
    // 3. 排序并返回 Top 5
    return scores.sort((a, b) => b.score - a.score).slice(0, 5);
  }
  
  /**
   * 提取输入特征
   * 
   * 使用正则表达式从用户输入中提取 12 种决策特征。
   * 每个特征对应一类关键词，用于后续的模型评分。
   * 
   * 特征类型：
   * - 风险类：风险、失败、损失等
   * - 认知类：不确定、不了解等
   * - 价值类：估值、价格、值得等
   * - 竞争类：竞争、护城河、优势等
   * - 情绪类：热门、火、爆、涨跌等
   * - 从众类：大家都、别人都、跟风等
   * - 时间类：长期/短期、持续/快速等
   * - 资源类：成本、预算、资源等
   * - 机会类：机会、选择、替代等
   * - 激励类：激励、利益、动机等
   * - 信任类：信任、可靠、诚信等
   * 
   * @param input - 用户输入
   * @returns 特征提取结果
   * 
   * @example
   * ```typescript
   * const features = recommender.extractFeatures('大家都在买，我也想买');
   * console.log(features.hasHerd); // true
   * console.log(features.hasEmotion); // false
   * ```
   */
  private extractFeatures(input: string): InputFeatures {
    return {
      hasRisk: /风险|失败|损失|亏损|危险|问题/.test(input),
      hasUncertainty: /不确定|不了解|不懂|不清楚|疑问|困惑/.test(input),
      hasValue: /估值|价格|价值|值得|合理|贵|便宜/.test(input),
      hasCompetition: /竞争|对手|护城河|壁垒|优势|差异/.test(input),
      hasEmotion: /热门|火|爆|涨|跌|暴涨|暴跌|疯狂/.test(input),
      hasHerd: /大家都|别人都|跟风|流行|趋势|主流/.test(input),
      hasLongTerm: /长期|持续|复利|积累|未来|战略/.test(input),
      hasShortTerm: /短期|快速|立即|马上|紧急|当下/.test(input),
      hasResource: /成本|预算|资源|投入|花费|支出/.test(input),
      hasOpportunity: /机会|选择|替代|方案|对比|权衡/.test(input),
      hasIncentive: /激励|利益|动机|目的|好处|收益/.test(input),
      hasTrust: /信任|可靠|诚信|靠谱|保证|承诺/.test(input),
    };
  }
  
  /**
   * 计算所有模型的评分
   * 
   * 遍历所有模型，根据特征和场景计算评分，过滤掉评分为 0 的模型。
   * 
   * @param features - 输入特征
   * @param scenarioId - 场景 ID
   * @returns 评分结果数组（过滤掉评分为 0 的模型）
   */
  private calculateScores(features: InputFeatures, scenarioId: string): ModelScore[] {
    return this.models.map(model => ({
      modelId: model.id,
      score: this.scoreModel(model, features, scenarioId),
      reason: this.generateReason(model, features),
      model
    })).filter(s => s.score > 0); // 过滤掉评分为 0 的模型
  }
  
  /**
   * 计算单个模型的评分
   * 
   * 评分算法：
   * 1. 基础分：50 分
   * 2. 场景加分：根据场景类型加分（0-20 分）
   * 3. 特征加分：根据输入特征加分（0-30 分）
   * 4. 总分范围：0-100 分
   * 
   * @param model - 模型配置
   * @param features - 输入特征
   * @param scenarioId - 场景 ID
   * @returns 评分（0-100）
   */
  private scoreModel(model: Model, features: InputFeatures, scenarioId: string): number {
    let score = 50; // 基础分
    score += this.getScenarioBonus(model.id, scenarioId); // 场景加分
    score += this.getFeatureBonus(model, features); // 特征加分
    return Math.min(100, Math.max(0, score)); // 限制在 0-100 范围
  }
  
  /**
   * 获取场景加分
   * 
   * 根据场景类型和模型 ID，返回场景相关性加分。
   * 不同场景对不同模型有不同的加分规则。
   * 
   * 场景加分规则：
   * - investment（投资）：能力圈+15、逆向思维+20、安全边际+20、护城河+15、复利效应+15
   * - product（产品）：第一性原理+20、能力圈+10、二阶思维+15、用户体验+15
   * - hiring（招聘）：第一性原理+15、能力圈+10、文化匹配+15
   * - strategy（战略）：第一性原理+20、逆向思维+20、护城河+15
   * 
   * @param modelId - 模型 ID
   * @param scenarioId - 场景 ID
   * @returns 加分（0-20）
   */
  private getScenarioBonus(modelId: string, scenarioId: string): number {
    const rules: Record<string, Record<string, number>> = {
      investment: { '06': 15, '07': 20, '10': 20, '09': 15, '44': 15 },
      product: { '08': 20, '06': 10, '02': 15, '43': 15 },
      hiring: { '08': 15, '06': 10, '45': 15 },
      strategy: { '08': 20, '07': 20, '09': 15 }
    };
    return rules[scenarioId]?.[modelId] || 0;
  }
  
  /**
   * 获取特征加分
   * 
   * 根据模型类型和输入特征，返回特征相关性加分。
   * 核心模型（ID 01-30）使用精确规则，其他模型使用分类规则。
   * 
   * 核心模型加分规则（精确匹配）：
   * - 06 能力圈：情绪+20、从众+20、不确定+10
   * - 07 逆向思维：风险+25、不确定+15
   * - 08 第一性原理：不确定+20、无情绪+10
   * - 09 护城河：竞争+25、长期+15
   * - 10 安全边际：风险+20、价值+15
   * - 11 多元思维：情绪+从众+30
   * - 12 确认偏误：情绪+15、从众+10
   * - 13 锚定效应：价值+20
   * - 14 损失厌恶：风险+20、价值+10
   * - 15 从众心理：从众+25
   * - 16 稀缺性：短期+15、机会+10
   * - 17 权威影响：信任+20
   * - 18 承诺一致：激励+15
   * - 19 对事不对人：信任+15
   * - 20 对比原则：价值+15、机会+10
   * - 21 可得性启发：情绪+15
   * - 22 代表性启发：不确定+15
   * - 23 沉没成本：资源+20、风险+10
   * - 24 框架效应：价值+15
   * - 25 后见之明：风险+10
   * - 26 过度自信：风险+15、不确定+10
   * - 27 禀赋效应：价值+15
   * - 28 现状偏误：机会+15
   * - 29 赌徒谬误：情绪+20
   * - 30 光环效应：信任+15
   * 
   * 分类规则（其他模型）：
   * - 心理学类：情绪+15、从众+10
   * - 商业类：竞争+20、长期+15
   * - 投资类：价值+20、风险+15
   * - 经济学类：资源+20、机会+15
   * - 系统类：长期+20、竞争+10
   * 
   * @param model - 模型配置
   * @param features - 输入特征
   * @returns 加分（0-30）
   */
  private getFeatureBonus(model: Model, features: InputFeatures): number {
    let bonus = 0;
    
    // 核心模型（精确规则）
    const coreRules: Record<string, () => number> = {
      '06': () => (features.hasEmotion ? 20 : 0) + (features.hasHerd ? 20 : 0) + (features.hasUncertainty ? 10 : 0),
      '07': () => (features.hasRisk ? 25 : 0) + (features.hasUncertainty ? 15 : 0),
      '08': () => (features.hasUncertainty ? 20 : 0) + (!features.hasEmotion ? 10 : 0),
      '09': () => (features.hasCompetition ? 25 : 0) + (features.hasLongTerm ? 15 : 0),
      '10': () => (features.hasRisk ? 20 : 0) + (features.hasValue ? 15 : 0),
      '11': () => (features.hasEmotion && features.hasHerd ? 30 : 0),
      '12': () => (features.hasEmotion ? 15 : 0) + (features.hasHerd ? 10 : 0),
      '13': () => features.hasValue ? 20 : 0,
      '14': () => (features.hasRisk ? 20 : 0) + (features.hasValue ? 10 : 0),
      '15': () => features.hasHerd ? 25 : 0,
      '16': () => (features.hasShortTerm ? 15 : 0) + (features.hasOpportunity ? 10 : 0),
      '17': () => features.hasTrust ? 20 : 0,
      '18': () => features.hasIncentive ? 15 : 0,
      '19': () => features.hasTrust ? 15 : 0,
      '20': () => (features.hasValue ? 15 : 0) + (features.hasOpportunity ? 10 : 0),
      '21': () => features.hasEmotion ? 15 : 0,
      '22': () => features.hasUncertainty ? 15 : 0,
      '23': () => (features.hasResource ? 20 : 0) + (features.hasRisk ? 10 : 0),
      '24': () => features.hasValue ? 15 : 0,
      '25': () => features.hasRisk ? 10 : 0,
      '26': () => (features.hasRisk ? 15 : 0) + (features.hasUncertainty ? 10 : 0),
      '27': () => features.hasValue ? 15 : 0,
      '28': () => features.hasOpportunity ? 15 : 0,
      '29': () => features.hasEmotion ? 20 : 0,
      '30': () => features.hasTrust ? 15 : 0,
    };
    
    if (coreRules[model.id]) {
      // 核心模型使用精确规则
      bonus += coreRules[model.id]();
    } else {
      // 其他模型使用分类规则
      bonus += this.getCategoryBonus(model.category, features);
    }
    
    return bonus;
  }
  
  /**
   * 获取分类加分
   * 
   * 根据模型分类和输入特征，返回分类相关性加分。
   * 用于非核心模型的评分。
   * 
   * @param category - 模型分类
   * @param features - 输入特征
   * @returns 加分（0-35）
   */
  private getCategoryBonus(category: string, features: InputFeatures): number {
    const rules: Record<string, () => number> = {
      psychology: () => (features.hasEmotion ? 15 : 0) + (features.hasHerd ? 10 : 0),
      business: () => (features.hasCompetition ? 20 : 0) + (features.hasLongTerm ? 15 : 0),
      investment: () => (features.hasValue ? 20 : 0) + (features.hasRisk ? 15 : 0),
      economics: () => (features.hasResource ? 20 : 0) + (features.hasOpportunity ? 15 : 0),
      systems: () => (features.hasLongTerm ? 20 : 0) + (features.hasCompetition ? 10 : 0),
    };
    return rules[category]?.() || 0;
  }
  
  /**
   * 生成推荐理由
   * 
   * 根据模型和输入特征，生成人性化的推荐理由。
   * 核心模型使用精确理由，其他模型使用通用理由。
   * 
   * 理由生成规则：
   * - 优先匹配核心模型的精确理由
   * - 未匹配时使用通用理由模板
   * - 理由应简洁、具体、有指导意义
   * 
   * @param model - 模型配置
   * @param features - 输入特征
   * @returns 推荐理由文本
   * 
   * @example
   * ```typescript
   * const reason = recommender.generateReason(model, { hasHerd: true });
   * // '存在从众倾向，保持独立思考'
   * ```
   */
  private generateReason(model: Model, features: InputFeatures): string {
    // 核心模型的精确理由
    const reasons: Record<string, () => string | null> = {
      '06': () => features.hasEmotion ? '存在情绪化表达，警惕认知偏误' : null,
      '07': () => features.hasRisk ? '你提到了风险，逆向思维帮助识别失败路径' : null,
      '08': () => features.hasUncertainty ? '存在不确定性，回归第一性原理思考' : null,
      '09': () => features.hasCompetition ? '涉及竞争分析，需要评估护城河' : null,
      '10': () => features.hasValue ? '涉及估值问题，需要评估安全边际' : null,
      '11': () => (features.hasEmotion && features.hasHerd) ? '多种心理倾向叠加，警惕极端效应' : null,
      '12': () => features.hasEmotion ? '可能存在确认偏误，寻找反面证据' : null,
      '13': () => features.hasValue ? '注意锚定效应，独立评估价值' : null,
      '14': () => features.hasRisk ? '损失厌恶可能影响判断，理性评估' : null,
      '15': () => features.hasHerd ? '存在从众倾向，保持独立思考' : null,
      '16': () => features.hasShortTerm ? '警惕稀缺性制造的紧迫感' : null,
      '17': () => features.hasTrust ? '注意权威影响，独立验证信息' : null,
      '18': () => features.hasIncentive ? '警惕承诺一致陷阱，灵活调整' : null,
      '19': () => features.hasTrust ? '将人与事分开评估' : null,
      '20': () => features.hasValue ? '注意对比原则的影响' : null,
      '21': () => features.hasEmotion ? '警惕可得性启发，寻找全面数据' : null,
      '22': () => features.hasUncertainty ? '避免代表性启发，关注统计规律' : null,
      '23': () => features.hasResource ? '警惕沉没成本谬误，关注未来价值' : null,
      '24': () => features.hasValue ? '注意框架效应，多角度评估' : null,
      '25': () => features.hasRisk ? '避免后见之明偏误' : null,
      '26': () => features.hasRisk ? '警惕过度自信，评估真实能力' : null,
      '27': () => features.hasValue ? '注意禀赋效应，客观评估价值' : null,
      '28': () => features.hasOpportunity ? '克服现状偏误，评估变革机会' : null,
      '29': () => features.hasEmotion ? '警惕赌徒谬误，每次独立评估' : null,
      '30': () => features.hasTrust ? '避免光环效应，全面评估' : null,
    };
    
    // 尝试返回精确理由，否则返回通用理由
    return reasons[model.id]?.() || `${model.name}适用于此类决策`;
  }
}
