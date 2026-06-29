/**
 * 心境演化 (Mood Evolution) v1.0.0
 *
 * 心境随时间的演化追踪
 */

class MoodEvolution {
  constructor(options = {}) {
    this.moodSnapshots = [];
    this.moodTrends = [];
    this.maxSnapshots = options.maxSnapshots || 1000;
    this.baseline = null;
  }

  /**
   * 记录心境快照
   */
  snapshot(mood, context = {}) {
    const snapshot = {
      id: `snapshot-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      mood: typeof mood === 'object' ? mood : { value: mood },
      valence: mood.valence || 0,
      arousal: mood.arousal || 0,
      dominance: mood.dominance || 0,
      context,
      timestamp: Date.now()
    };

    this.moodSnapshots.push(snapshot);

    // 清理旧快照
    if (this.moodSnapshots.length > this.maxSnapshots) {
      this.moodSnapshots = this.moodSnapshots.slice(-this.maxSnapshots);
    }

    // 更新基线
    this._updateBaseline();

    // 检测趋势
    this._detectTrend();

    return snapshot;
  }

  /**
   * 更新基线
   */
  _updateBaseline() {
    if (this.moodSnapshots.length < 10) return;

    const recent = this.moodSnapshots.slice(-50);
    const avgValence = recent.reduce((sum, s) => sum + s.valence, 0) / recent.length;
    const avgArousal = recent.reduce((sum, s) => sum + s.arousal, 0) / recent.length;

    this.baseline = {
      valence: avgValence,
      arousal: avgArousal,
      updatedAt: Date.now()
    };
  }

  /**
   * 检测趋势
   */
  _detectTrend() {
    if (this.moodSnapshots.length < 5) return;

    const recent = this.moodSnapshots.slice(-10);
    const old = this.moodSnapshots.slice(-20, -10);

    if (old.length < 3) return;

    // 计算平均值变化
    const recentAvgValence = recent.reduce((sum, s) => sum + s.valence, 0) / recent.length;
    const oldAvgValence = old.reduce((sum, s) => sum + s.valence, 0) / old.length;

    const recentAvgArousal = recent.reduce((sum, s) => sum + s.arousal, 0) / recent.length;
    const oldAvgArousal = old.reduce((sum, s) => sum + s.arousal, 0) / old.length;

    let trend = 'stable';

    if (recentAvgValence - oldAvgValence > 0.1) {
      trend = 'improving';
    } else if (recentAvgValence - oldAvgValence < -0.1) {
      trend = 'declining';
    }

    let arousalTrend = 'stable';
    if (recentAvgArousal - oldAvgArousal > 0.15) {
      arousalTrend = 'increasing';
    } else if (recentAvgArousal - oldAvgArousal < -0.15) {
      arousalTrend = 'decreasing';
    }

    this.moodTrends.push({
      valenceTrend: trend,
      arousalTrend,
      valenceChange: recentAvgValence - oldAvgValence,
      arousalChange: recentAvgArousal - oldAvgArousal,
      timestamp: Date.now()
    });

    // 清理旧趋势
    if (this.moodTrends.length > 100) {
      this.moodTrends = this.moodTrends.slice(-100);
    }
  }

  /**
   * 获取当前趋势
   */
  getCurrentTrend() {
    if (this.moodTrends.length === 0) return null;
    return this.moodTrends[this.moodTrends.length - 1];
  }

  /**
   * 获取基线
   */
  getBaseline() {
    return this.baseline;
  }

  /**
   * 计算与基线的偏差
   */
  getDeviation(currentMood) {
    if (!this.baseline) return null;

    return {
      valenceDeviation: currentMood.valence - this.baseline.valence,
      arousalDeviation: currentMood.arousal - this.baseline.arousal,
      magnitude: Math.sqrt(
        Math.pow(currentMood.valence - this.baseline.valence, 2) +
        Math.pow(currentMood.arousal - this.baseline.arousal, 2)
      )
    };
  }

  /**
   * 获取历史快照
   */
  getSnapshots(since = null, limit = 50) {
    let snapshots = this.moodSnapshots;

    if (since) {
      snapshots = snapshots.filter(s => s.timestamp >= since);
    }

    return snapshots.slice(-limit);
  }

  /**
   * 获取统计
   */
  getStats() {
    if (this.moodSnapshots.length === 0) {
      return {
        totalSnapshots: 0,
        baseline: null,
        currentTrend: null,
        averageValence: 0,
        averageArousal: 0
      };
    }

    const recent = this.moodSnapshots.slice(-100);

    return {
      totalSnapshots: this.moodSnapshots.length,
      baseline: this.baseline,
      currentTrend: this.getCurrentTrend(),
      averageValence: recent.reduce((sum, s) => sum + s.valence, 0) / recent.length,
      averageArousal: recent.reduce((sum, s) => sum + s.arousal, 0) / recent.length,
      volatility: this._calculateVolatility()
    };
  }

  /**
   * 计算波动性
   */
  _calculateVolatility() {
    if (this.moodSnapshots.length < 10) return 0;

    const recent = this.moodSnapshots.slice(-50);
    const valences = recent.map(s => s.valence);

    const mean = valences.reduce((a, b) => a + b, 0) / valences.length;
    const squaredDiffs = valences.map(v => Math.pow(v - mean, 2));
    const variance = squaredDiffs.reduce((a, b) => a + b, 0) / valences.length;

    return Math.sqrt(variance);
  }

  /**
   * 获取时间段内的平均心境
   */
  getAverageForPeriod(startTime, endTime) {
    const snapshots = this.moodSnapshots.filter(
      s => s.timestamp >= startTime && s.timestamp <= endTime
    );

    if (snapshots.length === 0) return null;

    return {
      valence: snapshots.reduce((sum, s) => sum + s.valence, 0) / snapshots.length,
      arousal: snapshots.reduce((sum, s) => sum + s.arousal, 0) / snapshots.length,
      dominance: snapshots.reduce((sum, s) => sum + s.dominance, 0) / snapshots.length,
      count: snapshots.length
    };
  }

  /**
   * 重置
   */
  reset() {
    this.moodSnapshots = [];
    this.moodTrends = [];
    this.baseline = null;
  }
}

module.exports = { MoodEvolution };
