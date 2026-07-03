/**
 * 推理链管理 (Inference Chain) v1.0.0
 *
 * 管理多步推理链
 */

const { CommonsenseEngine } = require('./commonsense-engine.js');
const { CausalInference } = require('./causal-inference.js');

class InferenceChain {
  constructor(options = {}) {
    this.commonsense = new CommonsenseEngine(options);
    this.causal = new CausalInference(options);
    this.chains = new Map();
    this.maxChainLength = options.maxChainLength || 10;
    this.maxHistory = options.maxHistory || 100;
  }

  /**
   * 创建推理链
   */
  createChain(startStatement, options = {}) {
    const id = `chain-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const chain = {
      id,
      startStatement,
      steps: [],
      conclusion: null,
      confidence: 0,
      createdAt: Date.now(),
      completedAt: null,
      status: 'in_progress'
    };

    this.chains.set(id, chain);

    // 如果指定了推理深度，执行初始推理
    if (options.depth && options.depth > 0) {
      return this.expandChain(id, options);
    }

    return chain;
  }

  /**
   * 扩展推理链
   */
  expandChain(chainId, options = {}) {
    const chain = this.chains.get(chainId);
    if (!chain || chain.status !== 'in_progress') return chain;

    const { maxDepth = 3, reasonType = 'auto' } = options;

    for (let i = 0; i < maxDepth && chain.steps.length < this.maxChainLength; i++) {
      const lastStep = chain.steps[chain.steps.length - 1];
      const currentStatement = lastStep ? lastStep.conclusion : chain.startStatement;

      // 决定推理类型
      let step;
      if (reasonType === 'commonsense' || reasonType === 'auto') {
        step = this._commonsenseStep(currentStatement);
      } else if (reasonType === 'causal') {
        step = this._causalStep(currentStatement);
      } else {
        step = this._autoStep(currentStatement);
      }

      if (!step) break;

      chain.steps.push(step);

      // 更新置信度
      if (chain.confidence === 0) {
        chain.confidence = step.confidence;
      } else {
        chain.confidence *= step.confidence;
      }

      // 检查是否完成
      if (step.isConclusion) {
        chain.conclusion = step.conclusion;
        chain.status = 'completed';
        chain.completedAt = Date.now();
        break;
      }
    }

    return chain;
  }

  /**
   * 常识推理步骤
   */
  _commonsenseStep(statement) {
    const result = this.commonsense.reason(statement);

    return {
      type: 'commonsense',
      input: statement,
      conclusion: result.inference?.conclusion || statement,
      reasoning: result.inference?.reasoning || '',
      confidence: result.confidence,
      isConclusion: result.confidence > 0.7
    };
  }

  /**
   * 因果推理步骤
   */
  _causalStep(statement) {
    // 尝试推断原因
    const causeResult = this.causal.inferCauses(statement);

    if (causeResult.causes.length > 0) {
      const cause = causeResult.causes[0];
      return {
        type: 'causal',
        input: statement,
        conclusion: `可能是因为${cause.cause}导致${statement}`,
        reasoning: cause.type,
        confidence: cause.confidence,
        isConclusion: cause.confidence > 0.8
      };
    }

    // 尝试推断结果
    const effectResult = this.causal.inferEffects(statement);

    if (effectResult.effects.length > 0) {
      const effect = effectResult.effects[0];
      return {
        type: 'causal',
        input: statement,
        conclusion: `${statement}可能导致${effect.effect}`,
        reasoning: effect.type,
        confidence: effect.confidence,
        isConclusion: false
      };
    }

    return null;
  }

  /**
   * 自动选择推理类型
   */
  _autoStep(statement) {
    // 如果包含"为什么"，使用因果推理
    if (/为什么|为何|什么原因/.test(statement)) {
      return this._causalStep(statement);
    }

    // 否则使用常识推理
    return this._commonsenseStep(statement);
  }

  /**
   * 获取链
   */
  getChain(chainId) {
    return this.chains.get(chainId) || null;
  }

  /**
   * 获取活跃链
   */
  getActiveChains() {
    return [...this.chains.values()].filter(c => c.status === 'in_progress');
  }

  /**
   * 获取链历史
   */
  getHistory(limit = 20) {
    return [...this.chains.values()]
      .filter(c => c.status === 'completed')
      .sort((a, b) => b.completedAt - a.completedAt)
      .slice(0, limit);
  }

  /**
   * 删除链
   */
  deleteChain(chainId) {
    return this.chains.delete(chainId);
  }

  /**
   * 分析陈述
   */
  analyze(statement, options = {}) {
    const commonsenseResult = this.commonsense.reason(statement);
    const causalCauseResult = this.causal.inferCauses(statement);
    const causalEffectResult = this.causal.inferEffects(statement);

    return {
      statement,
      commonsense: commonsenseResult,
      causal: {
        causes: causalCauseResult.causes.slice(0, 3),
        effects: causalEffectResult.effects.slice(0, 3)
      },
      suggestions: this._generateSuggestions(commonsenseResult, causalCauseResult, causalEffectResult)
    };
  }

  /**
   * 生成建议
   */
  _generateSuggestions(commonsense, causalCauses, causalEffects) {
    const suggestions = [];

    if (commonsense.confidence < 0.5) {
      suggestions.push('这个陈述需要更多上下文信息');
    }

    if (causalCauses.causes.length > 0) {
      suggestions.push(`可能的原因: ${causalCauses.causes[0].cause}`);
    }

    if (causalEffects.effects.length > 0) {
      suggestions.push(`可能的结果: ${causalEffects.effects[0].effect}`);
    }

    return suggestions;
  }

  /**
   * 获取统计
   */
  getStats() {
    const completed = [...this.chains.values()].filter(c => c.status === 'completed');
    const active = [...this.chains.values()].filter(c => c.status === 'in_progress');

    const avgLength = completed.length > 0
      ? completed.reduce((sum, c) => sum + c.steps.length, 0) / completed.length
      : 0;

    const avgConfidence = completed.length > 0
      ? completed.reduce((sum, c) => sum + c.confidence, 0) / completed.length
      : 0;

    return {
      totalChains: this.chains.size,
      completed: completed.length,
      active: active.length,
      averageLength: avgLength.toFixed(2),
      averageConfidence: avgConfidence.toFixed(2)
    };
  }
}

module.exports = { InferenceChain };
