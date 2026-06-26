/**
 * Fertility Tracker v2.0 - Multi-Signal Fusion
 * 
 * Combines multiple data sources for accurate ovulation detection:
 * - Temperature (Oura Ring)
 * - HRV (Oura Ring) 
 * - LH tests (manual input)
 * - Cervical mucus (manual input)
 * - Symptoms (manual input - cramping, breast tenderness, etc.)
 * 
 * Uses Bayesian fusion to calculate ovulation probability.
 */

class MultiSignalFusion {
  constructor() {
    // Prior probabilities for each cycle day
    this.priorOvulationProb = this._generatePriorDistribution();
  }

  /**
   * Generate prior probability distribution for ovulation by cycle day
   * Based on typical 28-32 day cycles
   */
  _generatePriorDistribution() {
    const probs = new Array(35).fill(0);
    
    // Ovulation most likely Days 13-17
    for (let day = 13; day <= 17; day++) {
      probs[day] = 0.15; // Peak probability
    }
    
    // Tails
    for (let day = 10; day <= 12; day++) {
      probs[day] = 0.05;
    }
    for (let day = 18; day <= 20; day++) {
      probs[day] = 0.05;
    }
    
    // Normalize
    const sum = probs.reduce((a, b) => a + b, 0);
    return probs.map(p => p / sum);
  }

  /**
   * Fuse all available signals to estimate ovulation day
   * @param {Object} signals - { temperature, hrv, lh, mucus, symptoms, currentDay }
   * @returns {Object} Ovulation prediction with confidence
   */
  fuseSignals(signals) {
    const {
      temperature = [],
      hrv = [],
      lh = [],
      mucus = [],
      symptoms = [],
      currentDay
    } = signals;

    // Initialize likelihood array
    let likelihood = new Array(currentDay + 1).fill(1.0);

    // Temperature signal
    if (temperature && temperature.length > 0) {
      const tempLikelihood = this._temperatureLikelihood(temperature, currentDay);
      likelihood = this._multiply(likelihood, tempLikelihood);
    }

    // HRV signal
    if (hrv && hrv.length > 0) {
      const hrvLikelihood = this._hrvLikelihood(hrv, currentDay);
      likelihood = this._multiply(likelihood, hrvLikelihood);
    }

    // LH signal (strongest signal)
    if (lh && lh.length > 0) {
      const lhLikelihood = this._lhLikelihood(lh, currentDay);
      likelihood = this._multiply(likelihood, lhLikelihood);
    }

    // Mucus signal
    if (mucus && mucus.length > 0) {
      const mucusLikelihood = this._mucusLikelihood(mucus, currentDay);
      likelihood = this._multiply(likelihood, mucusLikelihood);
    }

    // Symptoms signal
    if (symptoms && symptoms.length > 0) {
      const symptomsLikelihood = this._symptomsLikelihood(symptoms, currentDay);
      likelihood = this._multiply(likelihood, symptomsLikelihood);
    }

    // Posterior = Prior × Likelihood
    const posterior = this._multiply(
      this.priorOvulationProb.slice(0, currentDay + 1),
      likelihood
    );

    // Normalize
    const sum = posterior.reduce((a, b) => a + b, 0);
    const normalized = posterior.map(p => p / sum);

    // Find most likely day
    const maxProb = Math.max(...normalized);
    const mostLikelyDay = normalized.indexOf(maxProb);

    // Calculate confidence interval (80%)
    const sortedDays = normalized
      .map((prob, day) => ({ day, prob }))
      .sort((a, b) => b.prob - a.prob);
    
    let cumProb = 0;
    const credibleInterval = [];
    for (const { day, prob } of sortedDays) {
      credibleInterval.push(day);
      cumProb += prob;
      if (cumProb >= 0.8) break;
    }

    return {
      mostLikelyDay,
      confidence: maxProb,
      credibleInterval: credibleInterval.sort((a, b) => a - b),
      signalsUsed: this._getSignalsUsed(signals),
      distribution: normalized
    };
  }

  /**
   * Calculate temperature likelihood
   * High probability for days with pre-ovulatory dip or post-ovulatory rise
   */
  _temperatureLikelihood(temps, currentDay) {
    const likelihood = new Array(currentDay + 1).fill(0.1);
    
    // Look for dips (ovulation likely next day)
    for (let i = 1; i < temps.length - 1; i++) {
      if (temps[i] !== null && temps[i - 1] !== null) {
        const dip = temps[i - 1] - temps[i];
        if (dip >= 0.2) {
          // Strong dip signal
          if (i < currentDay) {
            likelihood[i] = 5.0; // High likelihood
          }
        }
      }
    }

    // Look for sustained rise (ovulation was 1-3 days before)
    const baseline = this._mean(temps.slice(0, Math.min(14, temps.length)));
    for (let i = 2; i < temps.length; i++) {
      if (temps[i] !== null && temps[i - 1] !== null) {
        const rise = temps[i] - baseline;
        const sustained = temps[i - 1] - baseline;
        
        if (rise >= 0.2 && sustained >= 0.2) {
          // Temperature rise detected - ovulation was 1-3 days ago
          if (i - 1 >= 0) likelihood[i - 1] = 3.0;
          if (i - 2 >= 0) likelihood[i - 2] = 4.0;
          if (i - 3 >= 0) likelihood[i - 3] = 2.0;
        }
      }
    }

    return likelihood;
  }

  /**
   * Calculate HRV likelihood
   * Low HRV (40% drop) signals ovulation in 1-3 days
   */
  _hrvLikelihood(hrv, currentDay) {
    const likelihood = new Array(currentDay + 1).fill(0.5);
    
    const baseline = this._mean(hrv.slice(0, Math.min(10, hrv.length)));
    
    for (let i = 0; i < hrv.length; i++) {
      if (hrv[i] !== null) {
        const drop = (baseline - hrv[i]) / baseline;
        
        if (drop >= 0.30) {
          // Significant HRV drop - ovulation likely in 1-3 days
          if (i + 1 <= currentDay) likelihood[i + 1] = 2.5;
          if (i + 2 <= currentDay) likelihood[i + 2] = 3.0;
          if (i + 3 <= currentDay) likelihood[i + 3] = 2.0;
        }
      }
    }

    return likelihood;
  }

  /**
   * Calculate LH likelihood
   * Positive LH = ovulation in 12-36 hours (strongest signal)
   */
  _lhLikelihood(lh, currentDay) {
    const likelihood = new Array(currentDay + 1).fill(0.1);
    
    for (let i = 0; i < lh.length; i++) {
      if (lh[i] === 'positive' || lh[i] === 'peak') {
        // LH surge - ovulation within 24-36 hours
        if (i <= currentDay) likelihood[i] = 8.0; // Very high
        if (i + 1 <= currentDay) likelihood[i + 1] = 10.0; // Strongest signal
        if (i + 2 <= currentDay) likelihood[i + 2] = 6.0;
      } else if (lh[i] === 'high') {
        if (i + 1 <= currentDay) likelihood[i + 1] = 3.0;
        if (i + 2 <= currentDay) likelihood[i + 2] = 2.0;
      }
    }

    return likelihood;
  }

  /**
   * Calculate mucus likelihood
   * Peak mucus (egg-white) = ovulation within 1-2 days
   */
  _mucusLikelihood(mucus, currentDay) {
    const likelihood = new Array(currentDay + 1).fill(0.5);
    
    for (let i = 0; i < mucus.length; i++) {
      if (mucus[i] === 'peak' || mucus[i] === 'egg-white') {
        // Peak mucus - ovulation imminent
        if (i <= currentDay) likelihood[i] = 4.0;
        if (i + 1 <= currentDay) likelihood[i + 1] = 5.0;
        if (i + 2 <= currentDay) likelihood[i + 2] = 3.0;
      } else if (mucus[i] === 'fertile' || mucus[i] === 'watery') {
        if (i + 1 <= currentDay) likelihood[i + 1] = 2.0;
        if (i + 2 <= currentDay) likelihood[i + 2] = 2.5;
      }
    }

    return likelihood;
  }

  /**
   * Calculate symptoms likelihood
   * Mittelschmerz (ovulation pain) = ovulation today or yesterday
   */
  _symptomsLikelihood(symptoms, currentDay) {
    const likelihood = new Array(currentDay + 1).fill(0.8);
    
    for (let i = 0; i < symptoms.length; i++) {
      const s = symptoms[i];
      
      if (s.cramping === 'sharp' || s.pain === 'ovulatory') {
        // Mittelschmerz - ovulation today
        if (i <= currentDay) likelihood[i] = 6.0;
        if (i - 1 >= 0) likelihood[i - 1] = 4.0;
      }
      
      if (s.discharge === 'bloody' || s.spotting) {
        // Ovulation spotting
        if (i <= currentDay) likelihood[i] = 3.0;
        if (i - 1 >= 0) likelihood[i - 1] = 4.0;
      }
      
      if (s.breastTenderness === 'increased') {
        // Post-ovulatory symptom
        if (i - 2 >= 0) likelihood[i - 2] = 1.5;
        if (i - 3 >= 0) likelihood[i - 3] = 1.5;
      }
    }

    return likelihood;
  }

  /**
   * Element-wise multiplication of two arrays
   */
  _multiply(arr1, arr2) {
    const minLength = Math.min(arr1.length, arr2.length);
    const result = new Array(minLength);
    for (let i = 0; i < minLength; i++) {
      result[i] = arr1[i] * arr2[i];
    }
    return result;
  }

  /**
   * Calculate mean, ignoring nulls
   */
  _mean(arr) {
    const valid = arr.filter(x => x !== null && !isNaN(x));
    if (valid.length === 0) return null;
    return valid.reduce((sum, x) => sum + x, 0) / valid.length;
  }

  /**
   * Get list of signals used in fusion
   */
  _getSignalsUsed(signals) {
    const used = [];
    if (signals.temperature && signals.temperature.length > 0) used.push('temperature');
    if (signals.hrv && signals.hrv.length > 0) used.push('HRV');
    if (signals.lh && signals.lh.length > 0) used.push('LH');
    if (signals.mucus && signals.mucus.length > 0) used.push('mucus');
    if (signals.symptoms && signals.symptoms.length > 0) used.push('symptoms');
    return used;
  }
}

module.exports = MultiSignalFusion;
