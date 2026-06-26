import { ScenarioDetector } from './detector';
import { ModelRecommender } from './recommender';
import { SmartRecommender } from './smart-recommender';
import { DialogueManager } from './dialogue';
import { ReportGenerator } from './reporter';
import { DialogueState } from './types';

/**
 * 芒格决策助手主入口
 * 
 * 基于查理·芒格的多元思维模型，帮助用户进行理性决策分析。
 * 
 * 核心功能：
 * 1. 场景识别：自动识别决策场景（投资、招聘、产品等）
 * 2. 模型推荐：根据场景推荐相关的思维模型
 * 3. 多轮对话：引导用户回答问题，收集决策信息
 * 4. 分析报告：生成包含评分、建议和风险提示的决策报告
 * 
 * 使用流程：
 * 1. startAnalysis() - 开始新的决策分析
 * 2. handleAnswer() - 处理用户的每个答案
 * 3. 自动生成报告（所有问题回答完毕后）
 * 
 * @example
 * ```typescript
 * const assistant = new MungerDecisionAssistant();
 * 
 * // 开始分析
 * const question1 = await assistant.startAnalysis('user123', '要不要投资这只股票？');
 * console.log(question1); // 显示第一个问题
 * 
 * // 回答问题
 * const question2 = await assistant.handleAnswer('user123', '我不太了解这个行业');
 * console.log(question2); // 显示下一个问题
 * 
 * // 继续回答...直到生成报告
 * ```
 */
export class MungerDecisionAssistant {
  /** 场景识别器 */
  private detector: ScenarioDetector;
  /** 模型推荐引擎 */
  private recommender: ModelRecommender;
  /** 智能推荐引擎（未使用，预留扩展） */
  private smartRecommender: SmartRecommender;
  /** 对话管理器 */
  private dialogue: DialogueManager;
  /** 报告生成器 */
  private reporter: ReportGenerator;

  /**
   * 构造函数
   * 
   * 初始化所有子模块。
   */
  constructor() {
    this.detector = new ScenarioDetector();
    this.recommender = new ModelRecommender();
    this.smartRecommender = new SmartRecommender();
    this.dialogue = new DialogueManager();
    this.reporter = new ReportGenerator();
  }

  /**
   * 开始新的决策分析
   * 
   * 创建新会话，识别场景，推荐模型，返回第一个问题。
   * 
   * 流程：
   * 1. 验证输入
   * 2. 创建会话
   * 3. 识别场景
   * 4. 推荐模型
   * 5. 设置会话状态
   * 6. 返回第一个问题
   * 
   * @param sessionId - 会话 ID（通常是用户 ID）
   * @param userInput - 用户输入的决策问题
   * @returns 第一个问题的文本（Markdown 格式）
   * 
   * @example
   * ```typescript
   * const question = await assistant.startAnalysis('user123', '要不要投资这只股票？');
   * // 返回：
   * // 📊 **场景识别：** 投资决策
   * // 🎯 **推荐模型：** 能力圈、逆向思维、安全边际
   * // ---
   * // ## 能力圈
   * // 你对这个行业了解多少？
   * ```
   */
  async startAnalysis(sessionId: string, userInput: string): Promise<string> {
    // 输入验证：确保用户提供了决策问题
    if (!userInput || userInput.trim().length === 0) {
      return '❌ 请提供决策问题描述';
    }

    // 1. 创建会话
    const context = this.dialogue.createSession(sessionId, userInput);

    // 2. 识别场景
    const detection = await this.detector.detect(userInput);
    const scenario = this.detector.getScenario(detection.scenarioId);

    if (!scenario) {
      return '❌ 无法识别决策场景，请提供更多信息';
    }

    // 3. 推荐模型
    const models = this.recommender.recommend(detection.suggestedModels);

    if (models.length === 0) {
      return '❌ 未找到相关模型';
    }

    // 4. 设置会话
    this.dialogue.setScenario(sessionId, scenario.id);
    this.dialogue.setModels(sessionId, models.map(m => m.id));
    this.dialogue.updateState(sessionId, DialogueState.QUESTIONING);

    // 5. 返回第一个问题
    const current = this.dialogue.getCurrentQuestion(sessionId, models);
    if (!current) {
      return '❌ 无法获取问题';
    }

    // 格式化输出：场景识别 + 推荐模型 + 第一个问题
    return `📊 **场景识别：** ${scenario.name}\n` +
           `🎯 **推荐模型：** ${models.map(m => m.name).join('、')}\n\n` +
           `---\n\n` +
           `## ${current.model.name}\n\n` +
           `${current.question}`;
  }

  /**
   * 处理用户回答
   * 
   * 记录用户的答案，移动到下一个问题或生成报告。
   * 
   * 流程：
   * 1. 验证会话存在
   * 2. 获取当前问题
   * 3. 记录答案
   * 4. 移动到下一个问题
   * 5. 如果还有问题，返回下一个问题
   * 6. 如果所有问题已完成，生成报告
   * 
   * @param sessionId - 会话 ID
   * @param answer - 用户的答案
   * @returns 下一个问题或最终报告（Markdown 格式）
   * 
   * @example
   * ```typescript
   * const response = await assistant.handleAnswer('user123', '我不太了解这个行业');
   * // 如果还有问题，返回：
   * // ✅ 已记录
   * // ---
   * // ## 能力圈
   * // 你有相关经验吗？
   * 
   * // 如果所有问题已完成，返回完整的决策报告
   * ```
   */
  async handleAnswer(sessionId: string, answer: string): Promise<string> {
    // 验证会话存在
    const context = this.dialogue.getContext(sessionId);
    if (!context) {
      return '❌ 会话不存在，请使用 /munger analyze 开始分析';
    }

    // 获取当前模型和问题
    const models = this.recommender.recommend(context.selectedModels);
    const current = this.dialogue.getCurrentQuestion(sessionId, models);

    if (!current) {
      return '❌ 无法获取当前问题';
    }

    // 记录答案
    this.dialogue.recordAnswer(
      sessionId,
      current.model.id,
      context.currentQuestionIndex,
      answer
    );

    // 移动到下一个问题
    const hasNext = this.dialogue.nextQuestion(sessionId, current.model);

    if (!hasNext) {
      // 所有问题已完成，生成报告
      return this.generateReport(sessionId);
    }

    // 获取下一个问题
    const next = this.dialogue.getCurrentQuestion(sessionId, models);
    if (!next) {
      // 如果获取下一个问题失败，直接生成报告
      return this.generateReport(sessionId);
    }

    // 返回下一个问题
    return `✅ 已记录\n\n` +
           `---\n\n` +
           `## ${next.model.name}\n\n` +
           `${next.question}`;
  }

  /**
   * 生成决策报告（私有方法）
   * 
   * 根据会话上下文生成完整的决策分析报告，并清理会话。
   * 
   * @param sessionId - 会话 ID
   * @returns Markdown 格式的决策报告
   */
  private generateReport(sessionId: string): string {
    const context = this.dialogue.getContext(sessionId);
    if (!context) {
      return '❌ 会话不存在';
    }

    // 获取场景和模型信息
    const scenario = this.detector.getScenario(context.scenario || 'general');
    const models = this.recommender.recommend(context.selectedModels);

    // 生成报告
    const report = this.reporter.generate(
      context,
      models,
      scenario?.name || '通用决策'
    );

    // 格式化为 Markdown
    const markdown = this.reporter.formatMarkdown(report);

    // 清理会话（释放内存）
    this.dialogue.deleteSession(sessionId);

    return markdown;
  }

  /**
   * 列出所有模型
   * 
   * 返回所有可用的芒格思维模型清单，按分类组织。
   * 
   * @returns Markdown 格式的模型清单
   * 
   * @example
   * ```typescript
   * const list = assistant.listModels();
   * console.log(list);
   * // # 芒格思维模型清单
   * // ## 认知心理学
   * // - **06. 能力圈**：只在自己理解的领域做决策
   * // - **07. 逆向思维**：从失败路径反推成功策略
   * // ...
   * ```
   */
  listModels(): string {
    const models = this.recommender.listModels();
    
    let output = '# 芒格思维模型清单\n\n';
    
    // 按分类组织模型
    const categories = new Map<string, typeof models>();
    models.forEach(model => {
      if (!categories.has(model.category)) {
        categories.set(model.category, []);
      }
      categories.get(model.category)!.push(model);
    });

    // 输出每个分类的模型
    for (const [category, categoryModels] of categories) {
      output += `## ${category}\n\n`;
      categoryModels.forEach(model => {
        output += `- **${model.id}. ${model.name}**：${model.description}\n`;
      });
      output += `\n`;
    }

    return output;
  }
}

/**
 * 导出单例
 * 
 * 提供全局单例实例，方便直接使用。
 * 
 * @example
 * ```typescript
 * import { assistant } from './index';
 * const question = await assistant.startAnalysis('user123', '要不要投资？');
 * ```
 */
export const assistant = new MungerDecisionAssistant();
