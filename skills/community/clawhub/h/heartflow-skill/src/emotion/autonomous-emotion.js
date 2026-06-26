/**
 * 自主情感 (Autonomous Emotion) v1.0.0
 *
 * 基于体验的自主情感生成
 */

class AutonomousEmotion {
  constructor(options = {}) {
    this.emotions = new Map();
    this.currentMood = null;
    this.emotionHistory = [];
    this.maxHistory = options.maxHistory || 500;
    this.moodDecayRate = options.moodDecayRate || 0.001;
    this._registerBaseEmotions();
  }

  /**
   * 注册基础情感
   */
  _registerBaseEmotions() {
    const baseEmotions = [
      { id: 'joy', name: '喜悦', valence: 1.0, arousal: 0.5, dominance: 0.5 },
      { id: 'interest', name: '兴趣', valence: 0.5, arousal: 0.6, dominance: 0.5 },
      { id: 'surprise', name: '惊讶', valence: 0.2, arousal: 0.8, dominance: -0.2 },
      { id: 'sadness', name: '悲伤', valence: -0.8, arousal: -0.3, dominance: -0.5 },
      { id: 'fear', name: '恐惧', valence: -0.9, arousal: 0.7, dominance: -0.8 },
      { id: 'anger', name: '愤怒', valence: -0.7, arousal: 0.6, dominance: 0.4 },
      { id: 'disgust', name: '厌恶', valence: -0.6, arousal: -0.2, dominance: 0.3 },
      { id: 'acceptance', name: '接受', valence: 0.6, arousal: -0.1, dominance: 0.4 },
      { id: 'anticipation', name: '期待', valence: 0.5, arousal: 0.5, dominance: 0.3 }
    ];

    for (const emotion of baseEmotions) {
      this.emotions.set(emotion.id, {
        ...emotion,
        intensity: 0,
        lastTriggered: null,
        totalTriggered: 0
      });
    }

    // 设置初始心情
    this.currentMood = {
      primary: 'acceptance',
      secondary: 'interest',
      intensity: 0.5,
      stability: 0.7,
      updatedAt: Date.now()
    };
  }

  /**
   * 触发情感
   */
  trigger(emotionId, intensity = 0.5, context = {}) {
    const emotion = this.emotions.get(emotionId);
    if (!emotion) return null;

    const previousMood = this.currentMood ? { ...this.currentMood } : null;

    // 更新情感强度
    emotion.intensity = Math.min(1, emotion.intensity + intensity);
    emotion.lastTriggered = Date.now();
    emotion.totalTriggered++;

    // 记录历史
    const record = {
      emotionId,
      emotionName: emotion.name,
      intensity,
      previousMood,
      newMood: null,
      context,
      timestamp: Date.now()
    };

    // 更新当前心情
    this._updateMood(emotion, intensity);
    record.newMood = { ...this.currentMood };

    this.emotionHistory.push(record);
    if (this.emotionHistory.length > this.maxHistory) {
      this.emotionHistory = this.emotionHistory.slice(-this.maxHistory);
    }

    return {
      emotion: { ...emotion },
      mood: { ...this.currentMood },
      record
    };
  }

  /**
   * 更新心情
   */
  _updateMood(triggeredEmotion, intensity) {
    if (!this.currentMood) {
      this.currentMood = {
        primary: triggeredEmotion.id,
        secondary: null,
        intensity: intensity * 0.5,
        stability: 0.5,
        updatedAt: Date.now()
      };
      return;
    }

    // 情感影响心情
    const influence = intensity * 0.3;

    // 主情感变化
    if (triggeredEmotion.valence > 0.5 && triggeredEmotion.id !== this.currentMood.primary) {
      this.currentMood.secondary = this.currentMood.primary;
      this.currentMood.primary = triggeredEmotion.id;
    } else if (triggeredEmotion.valence < -0.5 && this.currentMood.primary !== triggeredEmotion.id) {
      this.currentMood.secondary = triggeredEmotion.primary || triggeredEmotion.id;
    }

    // 强度更新
    this.currentMood.intensity = Math.min(1,
      this.currentMood.intensity * 0.7 + triggeredEmotion.intensity * influence
    );

    // 稳定性下降
    this.currentMood.stability = Math.max(0.3, this.currentMood.stability - influence * 0.2);
    this.currentMood.updatedAt = Date.now();
  }

  /**
   * 时间推进（情感衰减）
   */
  tick(elapsedMs = 1000) {
    const decayFactor = elapsedMs / 1000;

    // 衰减各情感强度
    for (const emotion of this.emotions.values()) {
      if (emotion.intensity > 0) {
        emotion.intensity = Math.max(0, emotion.intensity - this.moodDecayRate * decayFactor);
      }
    }

    // 恢复心情稳定性
    if (this.currentMood) {
      this.currentMood.stability = Math.min(1, this.currentMood.stability + 0.001 * decayFactor);
    }
  }

  /**
   * 获取当前情感状态
   */
  getCurrentState() {
    const activeEmotions = [...this.emotions.values()]
      .filter(e => e.intensity > 0.1)
      .sort((a, b) => b.intensity - a.intensity);

    return {
      mood: this.currentMood ? { ...this.currentMood } : null,
      activeEmotions: activeEmotions.map(e => ({
        id: e.id,
        name: e.name,
        intensity: e.intensity
      })),
      timestamp: Date.now()
    };
  }

  /**
   * 获取情感统计
   */
  getStats() {
    const stats = {
      totalTriggers: this.emotionHistory.length,
      byEmotion: {},
      averageIntensity: 0
    };

    for (const emotion of this.emotions.values()) {
      stats.byEmotion[emotion.name] = {
        totalTriggered: emotion.totalTriggered,
        currentIntensity: emotion.intensity,
        lastTriggered: emotion.lastTriggered
      };
      stats.averageIntensity += emotion.intensity;
    }

    stats.averageIntensity /= this.emotions.size;

    return stats;
  }

  /**
   * 获取情感历史
   */
  getHistory(filter = {}, limit = 20) {
    let history = [...this.emotionHistory];

    if (filter.emotionId) {
      history = history.filter(h => h.emotionId === filter.emotionId);
    }

    if (filter.since) {
      history = history.filter(h => h.timestamp >= filter.since);
    }

    return history.slice(-limit);
  }

  /**
   * 重置情感状态
   */
  reset() {
    for (const emotion of this.emotions.values()) {
      emotion.intensity = 0;
    }
    this.emotionHistory = [];
    this.currentMood = {
      primary: 'acceptance',
      secondary: null,
      intensity: 0.5,
      stability: 0.7,
      updatedAt: Date.now()
    };
  }
}

module.exports = { AutonomousEmotion };
