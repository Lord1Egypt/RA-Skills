/**
 * 决策场景定义
 * 
 * 描述一个具体的决策场景（如投资、招聘、产品决策等），
 * 包含场景识别所需的关键词、正则模式和推荐的思维模型。
 * 
 * @example
 * ```typescript
 * const scenario: Scenario = {
 *   id: 'investment',
 *   name: '投资决策',
 *   keywords: ['投资', '股票', '买入'],
 *   patterns: ['是否.*投资', '要不要.*买'],
 *   models: ['06', '07', '10']
 * };
 * ```
 */
export interface Scenario {
  /** 场景唯一标识符 */
  id: string;
  /** 场景名称（用于展示） */
  name: string;
  /** 关键词列表（用于快速匹配） */
  keywords: string[];
  /** 正则表达式模式列表（用于精确匹配） */
  patterns: string[];
  /** 推荐的思维模型 ID 列表 */
  models: string[];
}

/**
 * 场景识别结果
 * 
 * 包含识别到的场景 ID、置信度和推荐的思维模型列表。
 * 置信度范围 0-1，越高表示匹配度越高。
 * 
 * @example
 * ```typescript
 * const output: DetectorOutput = {
 *   scenarioId: 'investment',
 *   confidence: 0.85,
 *   suggestedModels: ['06', '07', '10']
 * };
 * ```
 */
export interface DetectorOutput {
  /** 识别到的场景 ID */
  scenarioId: string;
  /** 置信度（0-1），越高表示匹配度越高 */
  confidence: number;
  /** 推荐的思维模型 ID 列表 */
  suggestedModels: string[];
}

/**
 * 芒格思维模型定义
 * 
 * 描述一个具体的思维模型（如能力圈、逆向思维等），
 * 包含模型的基本信息、提问列表和评分标准。
 * 
 * @example
 * ```typescript
 * const model: Model = {
 *   id: '06',
 *   name: '能力圈',
 *   category: '认知心理学',
 *   description: '只在自己理解的领域做决策',
 *   questions: ['你对这个领域了解多少？', '你有相关经验吗？'],
 *   scoring: {
 *     high: '深入理解，可以决策',
 *     low: '了解不足，需要学习'
 *   }
 * };
 * ```
 */
export interface Model {
  /** 模型唯一标识符 */
  id: string;
  /** 模型名称 */
  name: string;
  /** 模型分类（如认知心理学、商业模型等） */
  category: string;
  /** 模型描述 */
  description: string;
  /** 提问列表（用于引导用户思考） */
  questions: string[];
  /** 评分标准（key: 评分等级, value: 评分说明） */
  scoring: Record<string, string | undefined>;
}

/**
 * 对话状态枚举
 * 
 * 定义对话流程中的各个状态，用于控制对话流转。
 * 
 * 流程：START → SCENARIO_CONFIRM → MODEL_SELECT → QUESTIONING → REPORT → END
 */
export enum DialogueState {
  /** 初始状态 */
  START = 'start',
  /** 场景确认状态 */
  SCENARIO_CONFIRM = 'scenario_confirm',
  /** 模型选择状态 */
  MODEL_SELECT = 'model_select',
  /** 提问状态（核心状态） */
  QUESTIONING = 'questioning',
  /** 报告生成状态 */
  REPORT = 'report',
  /** 结束状态 */
  END = 'end'
}

/**
 * 对话上下文
 * 
 * 存储单个会话的完整状态，包括用户输入、选中的模型、
 * 当前进度、用户答案等信息。
 * 
 * @example
 * ```typescript
 * const context: DialogueContext = {
 *   sessionId: 'user123',
 *   state: DialogueState.QUESTIONING,
 *   userInput: '要不要投资这只股票？',
 *   scenario: 'investment',
 *   selectedModels: ['06', '07', '10'],
 *   currentModelIndex: 0,
 *   currentQuestionIndex: 1,
 *   answers: { '06': ['我不太了解这个行业'] },
 *   createdAt: 1234567890,
 *   updatedAt: 1234567900
 * };
 * ```
 */
export interface DialogueContext {
  /** 会话唯一标识符 */
  sessionId: string;
  /** 当前对话状态 */
  state: DialogueState;
  /** 用户的原始输入（决策问题） */
  userInput: string;
  /** 识别到的场景 ID（可选） */
  scenario?: string;
  /** 选中的思维模型 ID 列表 */
  selectedModels: string[];
  /** 当前正在提问的模型索引 */
  currentModelIndex: number;
  /** 当前模型的问题索引 */
  currentQuestionIndex: number;
  /** 用户答案（key: 模型 ID, value: 答案数组） */
  answers: Record<string, any>;
  /** 会话创建时间戳 */
  createdAt: number;
  /** 会话最后更新时间戳 */
  updatedAt: number;
}

/**
 * 单个模型的分析结果
 * 
 * 包含模型的评分、分析文本和用户的答案列表。
 * 
 * @example
 * ```typescript
 * const analysis: ModelAnalysis = {
 *   modelId: '06',
 *   modelName: '能力圈',
 *   answers: ['我不太了解这个行业', '没有相关经验'],
 *   score: 'low',
 *   analysis: '你对该领域了解不足，建议先学习再决策'
 * };
 * ```
 */
export interface ModelAnalysis {
  /** 模型 ID */
  modelId: string;
  /** 模型名称 */
  modelName: string;
  /** 用户的答案列表 */
  answers: string[];
  /** 评分结果（如 high、low、medium 等） */
  score: string;
  /** 分析文本（基于评分的详细说明） */
  analysis: string;
}

/**
 * 决策分析报告
 * 
 * 包含完整的决策分析结果，包括各模型的分析、
 * 综合建议和风险提示。
 * 
 * @example
 * ```typescript
 * const report: DecisionReport = {
 *   title: '要不要投资这只股票？',
 *   timestamp: 1234567890,
 *   scenario: '投资决策',
 *   analyses: [{ modelId: '06', modelName: '能力圈', ... }],
 *   recommendation: '建议暂缓，需要更多研究',
 *   risks: ['能力圈：了解不足', '安全边际：估值过高']
 * };
 * ```
 */
export interface DecisionReport {
  /** 决策主题（用户的原始问题） */
  title: string;
  /** 报告生成时间戳 */
  timestamp: number;
  /** 决策场景名称 */
  scenario: string;
  /** 各模型的分析结果列表 */
  analyses: ModelAnalysis[];
  /** 综合建议（基于所有模型的分析） */
  recommendation: string;
  /** 风险提示列表 */
  risks: string[];
}
