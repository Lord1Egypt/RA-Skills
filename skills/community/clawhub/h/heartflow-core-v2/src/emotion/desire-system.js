/**
 * 欲望系统 (Desire System) v1.0.0
 *
 * 欲望与需求管理
 */

class DesireSystem {
  constructor(options = {}) {
    this.desires = new Map();
    this.needs = new Map();
    this.maxHistory = options.maxHistory || 100;
    this._registerBaseDesires();
    this._registerBaseNeeds();
  }

  /**
   * 注册基础欲望
   */
  _registerBaseDesires() {
    const baseDesires = [
      { id: 'curiosity', name: '好奇心', description: '想要了解新事物', baseIntensity: 0.7 },
      { id: 'competence', name: '能力感', description: '想要掌握技能', baseIntensity: 0.6 },
      { id: 'relatedness', name: '关联感', description: '想要与他人连接', baseIntensity: 0.5 },
      { id: 'autonomy', name: '自主感', description: '想要自己做决定', baseIntensity: 0.5 },
      { id: 'meaning', name: '意义感', description: '想要做有意义的事', baseIntensity: 0.6 },
      { id: 'growth', name: '成长感', description: '想要不断进步', baseIntensity: 0.7 },
      { id: 'security', name: '安全感', description: '想要感到安全', baseIntensity: 0.4 },
      { id: 'pleasure', name: '愉悦感', description: '想要感到快乐', baseIntensity: 0.4 }
    ];

    for (const desire of baseDesires) {
      this.desires.set(desire.id, {
        ...desire,
        currentIntensity: desire.baseIntensity,
        satisfaction: 0,
        lastSatisfied: null,
        totalSatisfied: 0
      });
    }
  }

  /**
   * 注册基础需求
   */
  _registerBaseNeeds() {
    const baseNeeds = [
      { id: 'physiological', name: '生理需求', description: '食物、水、休息', priority: 1 },
      { id: 'safety', name: '安全需求', description: '安全、稳定', priority: 2 },
      { id: 'belonging', name: '归属需求', description: '社交、亲密', priority: 3 },
      { id: 'esteem', name: '尊重需求', description: '成就、认可', priority: 4 },
      { id: 'self_actualization', name: '自我实现', description: '潜能发挥', priority: 5 }
    ];

    for (const need of baseNeeds) {
      this.needs.set(need.id, {
        ...need,
        currentLevel: 0.5,
        satisfied: false
      });
    }
  }

  /**
   * 满足欲望
   */
  satisfy(desireId, satisfaction = 0.5) {
    const desire = this.desires.get(desireId);
    if (!desire) return null;

    desire.satisfaction = Math.min(1, desire.satisfaction + satisfaction * 0.3);
    desire.lastSatisfied = Date.now();
    desire.totalSatisfied++;

    // 满足度增加时，强度自然下降
    desire.currentIntensity = Math.max(0.2, desire.baseIntensity * (1 - desire.satisfaction));

    return { ...desire };
  }

  /**
   * 增强欲望
   */
  intensify(desireId, amount = 0.1) {
    const desire = this.desires.get(desireId);
    if (!desire) return null;

    desire.currentIntensity = Math.min(1, desire.currentIntensity + amount);
    return { ...desire };
  }

  /**
   * 获取活跃欲望
   */
  getActiveDesires(minIntensity = 0.3) {
    return [...this.desires.values()]
      .filter(d => d.currentIntensity >= minIntensity)
      .sort((a, b) => b.currentIntensity - a.currentIntensity);
  }

  /**
   * 获取最强欲望
   */
  getDominantDesire() {
    const active = this.getActiveDesires(0.2);
    return active.length > 0 ? active[0] : null;
  }

  /**
   * 更新需求层级
   */
  updateNeed(needId, level) {
    const need = this.needs.get(needId);
    if (!need) return null;

    need.currentLevel = Math.min(1, Math.max(0, level));
    need.satisfied = need.currentLevel >= 0.8;

    return { ...need };
  }

  /**
   * 获取当前需求状态
   */
  getCurrentNeeds() {
    return [...this.needs.values()]
      .sort((a, b) => a.priority - b.priority)
      .map(n => ({ ...n }));
  }

  /**
   * 获取最紧迫的需求
   */
  getMostUrgentNeed() {
    const needs = this.getCurrentNeeds();
    // 找最低层级的未满足需求
    for (const need of needs) {
      if (!need.satisfied && need.currentLevel < 0.8) {
        return need;
      }
    }
    return null;
  }

  /**
   * 获取欲望状态摘要
   */
  getSummary() {
    const active = this.getActiveDesires(0.2);
    const dominant = this.getDominantDesire();

    return {
      totalDesires: this.desires.size,
      activeDesires: active.length,
      dominantDesire: dominant ? { id: dominant.id, name: dominant.name, intensity: dominant.currentIntensity } : null,
      urgentNeed: this.getMostUrgentNeed(),
      averageSatisfaction: [...this.desires.values()].reduce((sum, d) => sum + d.satisfaction, 0) / this.desires.size
    };
  }

  /**
   * 生成欲望驱动的行动建议
   */
  suggestAction() {
    const dominant = this.getDominantDesire();
    if (!dominant) return null;

    const actionMap = {
      curiosity: { type: 'explore', description: '探索新知识' },
      competence: { type: 'practice', description: '练习技能' },
      relatedness: { type: 'connect', description: '与他人交流' },
      autonomy: { type: 'decide', description: '做出自主决定' },
      meaning: { type: 'create', description: '做有意义的事' },
      growth: { type: 'learn', description: '学习新事物' },
      security: { type: 'secure', description: '确保安全' },
      pleasure: { type: 'enjoy', description: '享受愉悦' }
    };

    return actionMap[dominant.id] || null;
  }
}

module.exports = { DesireSystem };
