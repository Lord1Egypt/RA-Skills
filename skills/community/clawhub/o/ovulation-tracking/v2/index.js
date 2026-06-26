/**
 * Fertility Tracker v2.0 - Main Module
 * 
 * AI-powered fertility tracking with personalized pattern detection
 * and multi-signal fusion for accurate ovulation prediction.
 * 
 * New in v2.0:
 * - Automatic temperature pattern detection (Type A/B/C/D)
 * - Multi-signal Bayesian fusion (temp + HRV + LH + mucus + symptoms)
 * - Pre-ovulatory dip detection
 * - Multi-cycle learning (gets smarter over time)
 * - Internal vs external mucus education
 */

const fs = require('fs').promises;
const path = require('path');
const TemperaturePatternDetector = require('./pattern-detector');
const MultiSignalFusion = require('./multi-signal-fusion');

class FertilityTrackerV2 {
  constructor(configPath = './config.json') {
    this.configPath = configPath;
    this.config = null;
    this.patternDetector = new TemperaturePatternDetector();
    this.signalFusion = new MultiSignalFusion();
    this.currentCycle = {
      startDate: null,
      day: 0,
      temperatures: [],
      hrv: [],
      lh: [],
      mucus: [],
      symptoms: [],
      ovulationDay: null
    };
    this.userProfile = {
      pattern: null,
      cycleHistory: []
    };
  }

  /**
   * Initialize tracker - load config and user profile
   */
  async initialize() {
    // Load config
    try {
      const configData = await fs.readFile(this.configPath, 'utf8');
      this.config = JSON.parse(configData);
    } catch (error) {
      throw new Error(`Failed to load config from ${this.configPath}: ${error.message}`);
    }

    // Load user profile if exists
    const profilePath = path.join(path.dirname(this.configPath), 'user-profile.json');
    try {
      const profileData = await fs.readFile(profilePath, 'utf8');
      this.userProfile = JSON.parse(profileData);
      
      // Import learned pattern
      if (this.userProfile.pattern) {
        this.patternDetector.importPattern(this.userProfile.pattern);
      }
    } catch (error) {
      console.log('No existing user profile found. Starting fresh.');
    }

    // Load current cycle data
    await this._loadCurrentCycle();
    
    console.log('✅ Fertility Tracker v2.0 initialized');
    if (this.userProfile.pattern && this.userProfile.pattern.userPattern) {
      const p = this.userProfile.pattern.userPattern;
      console.log(`📊 Learned pattern: ${p.name} (${(p.confidence * 100).toFixed(0)}% confidence)`);
    }
  }

  /**
   * Daily check - main monitoring function
   * Run this once per day (e.g., in heartbeat or cron)
   */
  async dailyCheck() {
    await this.initialize();

    // Fetch latest Oura data
    await this._fetchOuraData();

    // Calculate current cycle day
    this.currentCycle.day = this._calculateCycleDay();

    console.log(`\n📅 Cycle Day ${this.currentCycle.day}`);

    // Run multi-signal fusion
    const prediction = this.signalFusion.fuseSignals({
      temperature: this.currentCycle.temperatures,
      hrv: this.currentCycle.hrv,
      lh: this.currentCycle.lh,
      mucus: this.currentCycle.mucus,
      symptoms: this.currentCycle.symptoms,
      currentDay: this.currentCycle.day
    });

    console.log(`🎯 Ovulation prediction: Day ${prediction.mostLikelyDay} (${(prediction.confidence * 100).toFixed(0)}% confidence)`);
    console.log(`📊 Signals used: ${prediction.signalsUsed.join(', ')}`);

    // Check for actionable alerts
    await this._processAlerts(prediction);

    // Save cycle data
    await this._saveCurrentCycle();

    return {
      cycleDay: this.currentCycle.day,
      prediction,
      userPattern: this.userProfile.pattern?.userPattern
    };
  }

  /**
   * Record LH test result
   */
  async recordLHTest(result, day = null) {
    await this.initialize();
    
    const targetDay = day || this.currentCycle.day;
    this.currentCycle.lh[targetDay] = result;

    if (result === 'positive' || result === 'peak') {
      console.log(`🔬 LH surge detected on Day ${targetDay}!`);
      
      // Send alert to partner
      await this._sendOvulationAlert(targetDay);
    }

    await this._saveCurrentCycle();
  }

  /**
   * Record cervical mucus observation
   */
  async recordMucus(type, day = null) {
    await this.initialize();
    
    const targetDay = day || this.currentCycle.day;
    this.currentCycle.mucus[targetDay] = type;

    if (type === 'peak' || type === 'egg-white') {
      console.log(`💧 Peak mucus detected on Day ${targetDay}`);
    }

    await this._saveCurrentCycle();
  }

  /**
   * Record symptoms
   */
  async recordSymptoms(symptoms, day = null) {
    await this.initialize();
    
    const targetDay = day || this.currentCycle.day;
    this.currentCycle.symptoms[targetDay] = symptoms;

    if (symptoms.pain === 'ovulatory' || symptoms.cramping === 'sharp') {
      console.log(`⚡ Ovulation pain detected on Day ${targetDay}`);
    }

    await this._saveCurrentCycle();
  }

  /**
   * End current cycle and start new one
   * Call this when period starts
   */
  async startNewCycle(startDate) {
    await this.initialize();

    // Save completed cycle to history
    if (this.currentCycle.startDate) {
      const completedCycle = {
        ...this.currentCycle,
        endDate: new Date().toISOString()
      };
      
      this.userProfile.cycleHistory.push(completedCycle);

      // Re-learn pattern from all cycles
      if (this.userProfile.cycleHistory.length >= 2) {
        const pattern = this.patternDetector.learnFromCycles(
          this.userProfile.cycleHistory.filter(c => c.ovulationDay !== null)
        );
        
        this.userProfile.pattern = this.patternDetector.exportPattern();
        
        console.log(`\n🧠 Pattern updated from ${this.userProfile.cycleHistory.length} cycles`);
        console.log(`   Type: ${pattern.name}`);
        console.log(`   Confidence: ${(pattern.confidence * 100).toFixed(0)}%`);
        console.log(`   Consistency: ${(pattern.consistency * 100).toFixed(0)}%`);
      }

      // Save user profile
      await this._saveUserProfile();
    }

    // Reset current cycle
    this.currentCycle = {
      startDate: startDate || new Date().toISOString().split('T')[0],
      day: 1,
      temperatures: [],
      hrv: [],
      lh: [],
      mucus: [],
      symptoms: [],
      ovulationDay: null
    };

    await this._saveCurrentCycle();
    console.log(`✨ New cycle started: ${this.currentCycle.startDate}`);
  }

  /**
   * Get user's learned temperature pattern
   */
  getUserPattern() {
    return this.userProfile.pattern?.userPattern || null;
  }

  /**
   * Get cycle history
   */
  getCycleHistory() {
    return this.userProfile.cycleHistory;
  }

  // ==================== PRIVATE METHODS ====================

  /**
   * Fetch latest data from Oura Ring
   */
  async _fetchOuraData() {
    // Implementation: fetch temperature and HRV from Oura API
    // For now, placeholder - you'll integrate with actual Oura skill
    console.log('📡 Fetching Oura data...');
    
    // TODO: Integrate with Oura skill
    // const ouraData = await ouraSkill.getDailySleep(startDate, endDate);
    // this.currentCycle.temperatures = ouraData.temperatures;
    // this.currentCycle.hrv = ouraData.hrv;
  }

  /**
   * Calculate current cycle day
   */
  _calculateCycleDay() {
    if (!this.currentCycle.startDate) return 0;
    
    const start = new Date(this.currentCycle.startDate);
    const today = new Date();
    const diffDays = Math.floor((today - start) / (1000 * 60 * 60 * 24));
    
    return diffDays + 1; // Day 1 = first day of period
  }

  /**
   * Process alerts based on prediction
   */
  async _processAlerts(prediction) {
    const { mostLikelyDay, confidence, signalsUsed } = prediction;
    const currentDay = this.currentCycle.day;

    // Alert 1: Pre-ovulatory (2-3 days before predicted ovulation)
    if (currentDay >= mostLikelyDay - 3 && currentDay < mostLikelyDay && confidence > 0.6) {
      if (signalsUsed.includes('HRV') && !signalsUsed.includes('LH')) {
        console.log(`⚠️  Pre-ovulatory alert: Start LH testing`);
        // TODO: Send notification
      }
    }

    // Alert 2: Ovulation imminent (predicted ovulation day ± 1)
    if (Math.abs(currentDay - mostLikelyDay) <= 1 && confidence > 0.7) {
      if (signalsUsed.includes('LH') || signalsUsed.includes('mucus')) {
        console.log(`🎯 Ovulation imminent: Optimal TTC timing NOW`);
        // TODO: Send partner alert if not already sent
      }
    }

    // Alert 3: Ovulation confirmed (post-ovulatory rise detected)
    if (currentDay > mostLikelyDay && confidence > 0.8) {
      if (signalsUsed.includes('temperature') && !this.currentCycle.ovulationDay) {
        this.currentCycle.ovulationDay = mostLikelyDay;
        console.log(`✅ Ovulation confirmed: Day ${mostLikelyDay}`);
        // TODO: Send confirmation notification
      }
    }
  }

  /**
   * Send ovulation alert to partner
   */
  async _sendOvulationAlert(ovulationDay) {
    console.log(`📧 Sending ovulation alert for Day ${ovulationDay}...`);
    
    // TODO: Integrate with email/messaging
    // const message = this._generateAlertEmail(ovulationDay);
    // await sendEmail(this.config.partner.email, message);
  }

  /**
   * Load current cycle data from file
   */
  async _loadCurrentCycle() {
    const cyclePath = path.join(path.dirname(this.configPath), 'current-cycle.json');
    try {
      const data = await fs.readFile(cyclePath, 'utf8');
      this.currentCycle = JSON.parse(data);
    } catch (error) {
      // No current cycle file - will be created on first save
    }
  }

  /**
   * Save current cycle data to file
   */
  async _saveCurrentCycle() {
    const cyclePath = path.join(path.dirname(this.configPath), 'current-cycle.json');
    await fs.writeFile(cyclePath, JSON.stringify(this.currentCycle, null, 2));
  }

  /**
   * Save user profile (learned patterns + cycle history)
   */
  async _saveUserProfile() {
    const profilePath = path.join(path.dirname(this.configPath), 'user-profile.json');
    await fs.writeFile(profilePath, JSON.stringify(this.userProfile, null, 2));
  }
}

module.exports = FertilityTrackerV2;

// CLI usage
if (require.main === module) {
  const tracker = new FertilityTrackerV2();
  
  const command = process.argv[2];
  
  switch (command) {
    case 'check':
      tracker.dailyCheck().then(result => {
        console.log('\n✅ Daily check complete');
        process.exit(0);
      });
      break;
    
    case 'lh':
      const result = process.argv[3] || 'negative';
      tracker.recordLHTest(result).then(() => {
        console.log(`✅ LH test recorded: ${result}`);
        process.exit(0);
      });
      break;
    
    case 'new-cycle':
      const startDate = process.argv[3] || new Date().toISOString().split('T')[0];
      tracker.startNewCycle(startDate).then(() => {
        process.exit(0);
      });
      break;
    
    case 'pattern':
      tracker.initialize().then(() => {
        const pattern = tracker.getUserPattern();
        if (pattern) {
          console.log('\n📊 Your Temperature Pattern:');
          console.log(`   Type: ${pattern.name}`);
          console.log(`   Days to rise: ${pattern.daysToRise}`);
          console.log(`   Confidence: ${(pattern.confidence * 100).toFixed(0)}%`);
          console.log(`   Cycles analyzed: ${pattern.cyclesAnalyzed}`);
        } else {
          console.log('\n⚠️  No pattern learned yet. Need at least 2 cycles.');
        }
        process.exit(0);
      });
      break;
    
    default:
      console.log('Fertility Tracker v2.0\n');
      console.log('Commands:');
      console.log('  node index.js check          - Run daily check');
      console.log('  node index.js lh [result]    - Record LH test (positive/negative)');
      console.log('  node index.js new-cycle [date] - Start new cycle');
      console.log('  node index.js pattern        - Show learned pattern');
      process.exit(0);
  }
}
