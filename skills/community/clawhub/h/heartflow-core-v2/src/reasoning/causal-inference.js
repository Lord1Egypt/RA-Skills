/**
 * 因果推理 (Causal Inference) v1.0.0
 *
 * 因果关系推理
 */

class CausalInference {
  constructor(options = {}) {
    this.causalRules = new Map();
    this.inferenceHistory = [];
    this.maxHistory = options.maxHistory || 100;
    this._registerDefaultRules();
  }

  /**
   * 注册默认因果规则
   */
  _registerDefaultRules() {
    const rules = [
      // 物理因果
      { cause: '重力', effect: '物体下落', type: 'physical' },
      { cause: '加热', effect: '温度升高', type: 'physical' },
      { cause: '冷却', effect: '温度降低', type: 'physical' },
      { cause: '推力', effect: '物体移动', type: 'physical' },
      { cause: '阻力', effect: '运动减慢', type: 'physical' },

      // 动作因果
      { cause: '提问', effect: '获得回答', type: 'social' },
      { cause: '学习', effect: '知识增加', type: 'cognitive' },
      { cause: '练习', effect: '技能提升', type: 'cognitive' },
      { cause: '沟通', effect: '理解加深', type: 'social' },

      // 结果因果
      { cause: '努力', effect: '成功可能性增加', type: 'action' },
      { cause: '粗心', effect: '错误可能性增加', type: 'action' },
      { cause: '计划', effect: '效率提高', type: 'action' },

      // 时间因果
      { cause: '时间流逝', effect: '变化发生', type: 'temporal' },
      { cause: '等待', effect: '耐心考验', type: 'temporal' }
    ];

    for (const rule of rules) {
      this.addRule(rule.cause, rule.effect, rule.type);
    }
  }

  /**
   * 添加因果规则
   */
  addRule(cause, effect, type = 'general') {
    const rule = {
      id: `rule-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      cause,
      effect,
      type,
      confidence: 0.8,
      createdAt: Date.now()
    };

    // 按原因索引
    if (!this.causalRules.has(cause)) {
      this.causalRules.set(cause, []);
    }
    this.causalRules.get(cause).push(rule);

    return rule.id;
  }

  /**
   * 推理原因
   */
  inferCauses(effect, context = {}) {
    const causes = [];

    // 查找直接原因
    for (const [cause, rules] of this.causalRules) {
      for (const rule of rules) {
        if (rule.effect === effect || effect.includes(rule.effect)) {
          causes.push({
            cause: rule.cause,
            confidence: rule.confidence,
            type: rule.type,
            rule: rule.id
          });
        }
      }
    }

    // 查找相关原因（模糊匹配）
    for (const [cause, rules] of this.causalRules) {
      if (cause.includes(effect) || effect.includes(cause)) {
        for (const rule of rules) {
          if (!causes.some(c => c.cause === rule.cause)) {
            causes.push({
              cause: rule.cause,
              confidence: rule.confidence * 0.7,
              type: rule.type,
              rule: rule.id
            });
          }
        }
      }
    }

    // 按置信度排序
    causes.sort((a, b) => b.confidence - a.confidence);

    const result = {
      effect,
      causes: causes.slice(0, 5),
      timestamp: Date.now()
    };

    this.inferenceHistory.push(result);
    this._trimHistory();

    return result;
  }

  /**
   * 推理结果
   */
  inferEffects(cause, context = {}) {
    const rules = this.causalRules.get(cause) || [];
    const effects = rules.map(rule => ({
      effect: rule.effect,
      confidence: rule.confidence,
      type: rule.type,
      rule: rule.id
    }));

    // 模糊匹配
    for (const [c, rules] of this.causalRules) {
      if (cause.includes(c) || c.includes(cause)) {
        for (const rule of rules) {
          if (!effects.some(e => e.effect === rule.effect)) {
            effects.push({
              effect: rule.effect,
              confidence: rule.confidence * 0.7,
              type: rule.type,
              rule: rule.id
            });
          }
        }
      }
    }

    // 按置信度排序
    effects.sort((a, b) => b.confidence - a.confidence);

    const result = {
      cause,
      effects: effects.slice(0, 5),
      timestamp: Date.now()
    };

    this.inferenceHistory.push(result);
    this._trimHistory();

    return result;
  }

  /**
   * 链式推理
   */
  chainReason(startCause, steps = 3) {
    const chain = [];
    let currentCause = startCause;
    const visited = new Set();

    for (let i = 0; i < steps; i++) {
      if (visited.has(currentCause)) break;

      visited.add(currentCause);
      const result = this.inferEffects(currentCause);

      if (result.effects.length === 0) break;

      const nextEffect = result.effects[0];
      chain.push({
        from: currentCause,
        to: nextEffect.effect,
        confidence: nextEffect.confidence,
        type: nextEffect.type
      });

      currentCause = nextEffect.effect;
    }

    return {
      startCause,
      chain,
      length: chain.length,
      totalConfidence: chain.reduce((prod, c) => prod * c.confidence, 1)
    };
  }

  /**
   * 因果验证
   */
  validateCausality(cause, effect) {
    const rules = this.causalRules.get(cause) || [];
    const rule = rules.find(r => r.effect === effect);

    if (rule) {
      return {
        valid: true,
        confidence: rule.confidence,
        type: rule.type,
        explanation: `因为${cause}，所以${effect}`
      };
    }

    // 尝试反向验证
    const reverseRules = [];
    for (const [c, rs] of this.causalRules) {
      for (const r of rs) {
        if (r.effect === cause) {
          reverseRules.push({ cause: c, effect: effect, confidence: r.confidence * 0.5 });
        }
      }
    }

    if (reverseRules.length > 0) {
      return {
        valid: false,
        confidence: 0,
        explanation: '无法直接验证，但可能存在间接因果关系',
        alternative: reverseRules[0]
      };
    }

    return {
      valid: false,
      confidence: 0,
      explanation: '缺乏因果证据'
    };
  }

  /**
   * 删除规则
   */
  deleteRule(ruleId) {
    for (const [cause, rules] of this.causalRules) {
      const index = rules.findIndex(r => r.id === ruleId);
      if (index !== -1) {
        rules.splice(index, 1);
        if (rules.length === 0) {
          this.causalRules.delete(cause);
        }
        return true;
      }
    }
    return false;
  }

  /**
   * 修剪历史
   */
  _trimHistory() {
    if (this.inferenceHistory.length > this.maxHistory) {
      this.inferenceHistory = this.inferenceHistory.slice(-this.maxHistory);
    }
  }

  /**
   * 获取统计
   */
  getStats() {
    let totalRules = 0;
    const byType = {};

    for (const rules of this.causalRules.values()) {
      totalRules += rules.length;
      for (const rule of rules) {
        byType[rule.type] = (byType[rule.type] || 0) + 1;
      }
    }

    return {
      totalRules,
      uniqueCauses: this.causalRules.size,
      byType,
      recentInferences: this.inferenceHistory.slice(-5)
    };
  }

  /**
   * 导出规则
   */
  exportRules() {
    const rules = [];
    for (const causeRules of this.causalRules.values()) {
      rules.push(...causeRules);
    }
    return rules;
  }

  /**
   * 导入规则
   */
  importRules(rules) {
    let imported = 0;
    for (const rule of rules) {
      if (rule.cause && rule.effect) {
        this.addRule(rule.cause, rule.effect, rule.type || 'general');
        imported++;
      }
    }
    return imported;
  }
}

module.exports = { CausalInference };
