/**
 * Fertility Tracker v2.0 - Temperature Pattern Detector
 * 
 * Automatically detects user's personal temperature rise pattern:
 * - Type A: Immediate rise (1 day post-ovulation) - 60% of women
 * - Type B: Delayed rise (2-3 days post-ovulation) - 25% of women
 * - Type C: Gradual rise (3-5 days post-ovulation) - 10% of women
 * - Type D: No clear rise (unreliable for tracking) - 5% of women
 * 
 * Learns from 3+ cycles to identify individual pattern.
 */

class TemperaturePatternDetector {
  constructor() {
    this.patterns = {
      A: { name: 'Immediate Rise', daysToRise: 1, confidence: 0 },
      B: { name: 'Delayed Rise', daysToRise: 2, confidence: 0 },
      C: { name: 'Gradual Rise', daysToRise: 4, confidence: 0 },
      D: { name: 'No Clear Rise', daysToRise: null, confidence: 0 }
    };
    this.userPattern = null;
    this.cycleHistory = [];
  }

  /**
   * Analyze temperature data from a single cycle
   * @param {Object} cycleData - { ovulationDay, temperatures, dates }
   * @returns {Object} Pattern classification for this cycle
   */
  analyzeCycle(cycleData) {
    const { ovulationDay, temperatures, dates } = cycleData;
    
    if (!ovulationDay || !temperatures || temperatures.length < ovulationDay + 7) {
      return { pattern: null, confidence: 0, reason: 'Insufficient data' };
    }

    // Calculate baseline (follicular phase average)
    const follicularPhase = temperatures.slice(0, ovulationDay);
    const baseline = this._mean(follicularPhase.filter(t => t !== null));

    // Look for temperature rise after ovulation
    const postOvulation = temperatures.slice(ovulationDay, ovulationDay + 7);
    
    // Detect when temperature rises ≥0.2°C above baseline
    const riseThreshold = 0.2;
    let daysToRise = null;
    
    for (let i = 0; i < postOvulation.length; i++) {
      if (postOvulation[i] !== null && postOvulation[i] >= baseline + riseThreshold) {
        // Check if rise is sustained (next day also elevated)
        if (i < postOvulation.length - 1 && postOvulation[i + 1] >= baseline + riseThreshold) {
          daysToRise = i + 1; // +1 because day 0 = ovulation day
          break;
        }
      }
    }

    // Classify pattern
    let pattern, confidence;
    
    if (daysToRise === null) {
      pattern = 'D';
      confidence = 0.7;
    } else if (daysToRise === 1) {
      pattern = 'A';
      confidence = 0.9;
    } else if (daysToRise === 2 || daysToRise === 3) {
      pattern = 'B';
      confidence = 0.85;
    } else if (daysToRise >= 4) {
      pattern = 'C';
      confidence = 0.8;
    }

    return {
      pattern,
      confidence,
      daysToRise,
      baseline,
      riseDetected: daysToRise !== null,
      postOvulationTemps: postOvulation
    };
  }

  /**
   * Learn from multiple cycles to identify user's personal pattern
   * @param {Array} cycles - Array of cycle data objects
   * @returns {Object} User's identified pattern with confidence
   */
  learnFromCycles(cycles) {
    if (cycles.length < 2) {
      return {
        pattern: null,
        confidence: 0,
        message: 'Need at least 2 cycles to identify pattern',
        cyclesAnalyzed: cycles.length
      };
    }

    // Analyze each cycle
    const analyses = cycles.map(cycle => this.analyzeCycle(cycle));
    
    // Count pattern occurrences
    const patternCounts = { A: 0, B: 0, C: 0, D: 0 };
    analyses.forEach(a => {
      if (a.pattern) patternCounts[a.pattern]++;
    });

    // Find dominant pattern
    const dominant = Object.entries(patternCounts)
      .sort((a, b) => b[1] - a[1])[0];
    
    const [patternType, count] = dominant;
    const consistency = count / analyses.length;

    // Confidence increases with more cycles and higher consistency
    let confidence;
    if (cycles.length >= 3 && consistency >= 0.67) {
      confidence = 0.9; // High confidence
    } else if (cycles.length >= 2 && consistency >= 0.5) {
      confidence = 0.7; // Medium confidence
    } else {
      confidence = 0.5; // Low confidence
    }

    this.userPattern = {
      type: patternType,
      name: this.patterns[patternType].name,
      daysToRise: this.patterns[patternType].daysToRise,
      confidence,
      consistency,
      cyclesAnalyzed: cycles.length,
      distribution: patternCounts
    };

    this.cycleHistory = analyses;

    return this.userPattern;
  }

  /**
   * Predict ovulation based on current cycle data and learned pattern
   * @param {Array} temperatures - Current cycle temperature data
   * @param {number} currentDay - Current cycle day
   * @returns {Object} Ovulation prediction
   */
  predictOvulation(temperatures, currentDay) {
    if (!this.userPattern) {
      return {
        predicted: false,
        reason: 'No pattern learned yet',
        recommendation: 'Continue tracking for 2-3 cycles'
      };
    }

    // Look for pre-ovulatory dip
    const recentTemps = temperatures.slice(Math.max(0, currentDay - 3), currentDay + 1);
    const hasDip = this._detectDip(recentTemps);

    // Look for temperature rise based on user's pattern
    const baseline = this._mean(temperatures.slice(0, Math.min(14, currentDay)));
    const recent = temperatures[currentDay - 1];

    if (hasDip) {
      return {
        predicted: true,
        signal: 'pre-ovulatory dip',
        ovulationWindow: `${currentDay} to ${currentDay + 1}`,
        confidence: 0.8,
        action: 'Ovulation likely within 12-24 hours. Optimal TTC timing!'
      };
    }

    // Check for temperature rise (post-ovulation)
    if (recent >= baseline + 0.2) {
      const estimatedOvulationDay = currentDay - this.userPattern.daysToRise;
      return {
        predicted: true,
        signal: 'temperature rise',
        ovulationDay: estimatedOvulationDay,
        confidence: this.userPattern.confidence,
        pattern: this.userPattern.name,
        action: `Temperature rise detected. Based on your ${this.userPattern.name} pattern, ovulation likely occurred on Day ${estimatedOvulationDay}.`
      };
    }

    return {
      predicted: false,
      reason: 'No ovulation signals detected yet',
      currentDay,
      waitingFor: hasDip ? 'temperature rise' : 'pre-ovulatory dip or LH surge'
    };
  }

  /**
   * Detect pre-ovulatory temperature dip
   * @param {Array} temps - Recent 3-4 days of temperature data
   * @returns {boolean} True if significant dip detected
   */
  _detectDip(temps) {
    if (temps.length < 3) return false;

    const validTemps = temps.filter(t => t !== null);
    if (validTemps.length < 3) return false;

    const latest = validTemps[validTemps.length - 1];
    const previous = validTemps.slice(0, -1);
    const avgPrevious = this._mean(previous);

    // Dip = latest temp is ≥0.2°C lower than previous 2-3 days
    return latest <= avgPrevious - 0.2;
  }

  /**
   * Calculate mean of array, ignoring nulls
   */
  _mean(arr) {
    const valid = arr.filter(x => x !== null && !isNaN(x));
    if (valid.length === 0) return null;
    return valid.reduce((sum, x) => sum + x, 0) / valid.length;
  }

  /**
   * Export user pattern for storage
   */
  exportPattern() {
    return {
      userPattern: this.userPattern,
      cycleHistory: this.cycleHistory,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Import previously learned pattern
   */
  importPattern(data) {
    this.userPattern = data.userPattern;
    this.cycleHistory = data.cycleHistory || [];
  }
}

module.exports = TemperaturePatternDetector;
