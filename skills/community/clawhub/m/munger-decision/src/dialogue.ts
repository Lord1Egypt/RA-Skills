import { DialogueContext, DialogueState, Model } from './types';

/**
 * 对话管理器
 * 
 * 负责管理多轮对话的状态和流程控制。
 * 每个用户会话独立存储，支持并发多用户。
 * 
 * 核心功能：
 * 1. 会话生命周期管理（创建、更新、删除）
 * 2. 对话状态流转控制
 * 3. 问题进度跟踪
 * 4. 答案记录存储
 * 5. 过期会话清理
 * 
 * 对话流程：
 * START → SCENARIO_CONFIRM → MODEL_SELECT → QUESTIONING → REPORT → END
 * 
 * @example
 * ```typescript
 * const dialogue = new DialogueManager();
 * 
 * // 创建会话
 * const context = dialogue.createSession('user123', '要不要投资？');
 * 
 * // 设置场景和模型
 * dialogue.setScenario('user123', 'investment');
 * dialogue.setModels('user123', ['06', '07', '10']);
 * 
 * // 记录答案
 * dialogue.recordAnswer('user123', '06', 0, '我不太了解这个行业');
 * 
 * // 移动到下一个问题
 * dialogue.nextQuestion('user123', model);
 * ```
 */
export class DialogueManager {
  /** 会话上下文存储（key: sessionId, value: DialogueContext） */
  private contexts: Map<string, DialogueContext>;

  /**
   * 构造函数
   * 
   * 初始化会话存储容器。
   */
  constructor() {
    this.contexts = new Map();
  }

  /**
   * 创建新会话
   * 
   * 为用户创建一个新的决策分析会话，初始化所有状态。
   * 
   * @param sessionId - 会话唯一标识符（通常是用户 ID）
   * @param userInput - 用户输入的决策问题
   * @returns 新创建的会话上下文
   * 
   * @example
   * ```typescript
   * const context = dialogue.createSession('user123', '要不要投资这只股票？');
   * console.log(context.state); // DialogueState.START
   * ```
   */
  createSession(sessionId: string, userInput: string): DialogueContext {
    const context: DialogueContext = {
      sessionId,
      state: DialogueState.START,
      userInput,
      selectedModels: [],
      currentModelIndex: 0,
      currentQuestionIndex: 0,
      answers: {},
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    
    this.contexts.set(sessionId, context);
    return context;
  }

  /**
   * 获取会话上下文
   * 
   * 根据会话 ID 查找会话上下文。
   * 
   * @param sessionId - 会话 ID
   * @returns 会话上下文，未找到返回 undefined
   * 
   * @example
   * ```typescript
   * const context = dialogue.getContext('user123');
   * if (context) {
   *   console.log(context.state);
   * }
   * ```
   */
  getContext(sessionId: string): DialogueContext | undefined {
    return this.contexts.get(sessionId);
  }

  /**
   * 更新会话状态
   * 
   * 更新会话的对话状态，并刷新更新时间戳。
   * 
   * @param sessionId - 会话 ID
   * @param state - 新的对话状态
   * 
   * @example
   * ```typescript
   * dialogue.updateState('user123', DialogueState.QUESTIONING);
   * ```
   */
  updateState(sessionId: string, state: DialogueState): void {
    const context = this.contexts.get(sessionId);
    if (context) {
      context.state = state;
      context.updatedAt = Date.now();
    }
  }

  /**
   * 设置场景
   * 
   * 为会话设置识别到的决策场景。
   * 
   * @param sessionId - 会话 ID
   * @param scenarioId - 场景 ID
   * 
   * @example
   * ```typescript
   * dialogue.setScenario('user123', 'investment');
   * ```
   */
  setScenario(sessionId: string, scenarioId: string): void {
    const context = this.contexts.get(sessionId);
    if (context) {
      context.scenario = scenarioId;
      context.updatedAt = Date.now();
    }
  }

  /**
   * 设置选中的模型
   * 
   * 为会话设置要使用的思维模型列表，并重置问题进度。
   * 
   * @param sessionId - 会话 ID
   * @param modelIds - 模型 ID 列表
   * 
   * @example
   * ```typescript
   * dialogue.setModels('user123', ['06', '07', '10']);
   * ```
   */
  setModels(sessionId: string, modelIds: string[]): void {
    const context = this.contexts.get(sessionId);
    if (context) {
      context.selectedModels = modelIds;
      context.currentModelIndex = 0; // 重置到第一个模型
      context.currentQuestionIndex = 0; // 重置到第一个问题
      context.updatedAt = Date.now();
    }
  }

  /**
   * 记录答案
   * 
   * 记录用户对某个模型某个问题的答案。
   * 答案按模型 ID 分组存储，每个模型的答案是一个数组。
   * 
   * @param sessionId - 会话 ID
   * @param modelId - 模型 ID
   * @param questionIndex - 问题索引（从 0 开始）
   * @param answer - 用户的答案
   * 
   * @example
   * ```typescript
   * dialogue.recordAnswer('user123', '06', 0, '我不太了解这个行业');
   * dialogue.recordAnswer('user123', '06', 1, '没有相关经验');
   * ```
   */
  recordAnswer(sessionId: string, modelId: string, questionIndex: number, answer: string): void {
    const context = this.contexts.get(sessionId);
    if (context) {
      // 初始化模型的答案数组（如果不存在）
      if (!context.answers[modelId]) {
        context.answers[modelId] = [];
      }
      // 记录答案
      context.answers[modelId][questionIndex] = answer;
      context.updatedAt = Date.now();
    }
  }

  /**
   * 移动到下一个问题
   * 
   * 将问题进度移动到下一个问题或下一个模型。
   * 
   * 移动逻辑：
   * 1. 当前问题索引 +1
   * 2. 如果当前模型的问题已完成，移动到下一个模型
   * 3. 如果所有模型的问题都已完成，返回 false
   * 
   * @param sessionId - 会话 ID
   * @param model - 当前模型配置（用于获取问题总数）
   * @returns true 表示还有下一个问题，false 表示所有问题已完成
   * 
   * @example
   * ```typescript
   * const hasNext = dialogue.nextQuestion('user123', currentModel);
   * if (!hasNext) {
   *   // 所有问题已完成，生成报告
   * }
   * ```
   */
  nextQuestion(sessionId: string, model: Model): boolean {
    const context = this.contexts.get(sessionId);
    if (!context) return false;

    // 移动到下一个问题
    context.currentQuestionIndex++;
    
    // 如果当前模型问题已完成
    if (context.currentQuestionIndex >= model.questions.length) {
      context.currentModelIndex++; // 移动到下一个模型
      context.currentQuestionIndex = 0; // 重置问题索引
      
      // 如果所有模型已完成
      if (context.currentModelIndex >= context.selectedModels.length) {
        return false; // 没有下一个问题了
      }
    }
    
    context.updatedAt = Date.now();
    return true; // 还有下一个问题
  }

  /**
   * 获取当前问题
   * 
   * 根据当前进度，获取应该提问的问题和对应的模型。
   * 
   * @param sessionId - 会话 ID
   * @param models - 模型配置列表
   * @returns 当前问题和模型，未找到返回 null
   * 
   * @example
   * ```typescript
   * const current = dialogue.getCurrentQuestion('user123', models);
   * if (current) {
   *   console.log(`${current.model.name}: ${current.question}`);
   * }
   * ```
   */
  getCurrentQuestion(sessionId: string, models: Model[]): { model: Model; question: string } | null {
    const context = this.contexts.get(sessionId);
    if (!context) return null;

    // 获取当前模型
    const currentModel = models[context.currentModelIndex];
    if (!currentModel) return null;

    // 获取当前问题
    const question = currentModel.questions[context.currentQuestionIndex];
    if (!question) return null;

    return { model: currentModel, question };
  }

  /**
   * 删除会话
   * 
   * 删除指定的会话，释放内存。
   * 通常在生成报告后调用。
   * 
   * @param sessionId - 会话 ID
   * 
   * @example
   * ```typescript
   * dialogue.deleteSession('user123');
   * ```
   */
  deleteSession(sessionId: string): void {
    this.contexts.delete(sessionId);
  }

  /**
   * 清理过期会话
   * 
   * 删除超过 24 小时未更新的会话，防止内存泄漏。
   * 建议定期调用（如每小时一次）。
   * 
   * @example
   * ```typescript
   * // 定期清理过期会话
   * setInterval(() => {
   *   dialogue.cleanupExpired();
   * }, 60 * 60 * 1000); // 每小时清理一次
   * ```
   */
  cleanupExpired(): void {
    const now = Date.now();
    const expireTime = 24 * 60 * 60 * 1000; // 24 小时

    for (const [sessionId, context] of this.contexts.entries()) {
      // 如果会话超过 24 小时未更新，删除
      if (now - context.updatedAt > expireTime) {
        this.contexts.delete(sessionId);
      }
    }
  }
}
