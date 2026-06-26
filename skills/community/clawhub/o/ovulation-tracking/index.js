const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

class FertilityTracker {
  constructor(configPath = './config.json') {
    this.config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    this.cycleStart = new Date(this.config.cycleStart);
    this.ouraToken = this.loadToken(this.config.ouraToken);
  }
  
  loadToken(tokenConfig) {
    if (typeof tokenConfig === 'string' && tokenConfig.startsWith('file:')) {
      const filePath = tokenConfig.replace('file:', '').replace('~', process.env.HOME);
      return fs.readFileSync(filePath, 'utf8').trim();
    }
    return tokenConfig;
  }
  
  getCycleDay() {
    const today = new Date();
    const diff = today - this.cycleStart;
    return Math.floor(diff / (1000 * 60 * 60 * 24)) + 1;
  }
  
  getExpectedOvulation() {
    const avgLength = this.config.averageCycleLength || 30;
    return {
      min: Math.floor(avgLength * 0.5),
      max: Math.floor(avgLength * 0.7)
    };
  }
  
  async getOuraData(startDate, endDate) {
    const url = `https://api.ouraring.com/v2/usercollection/daily_readiness?start_date=${startDate}&end_date=${endDate}`;
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${this.ouraToken}` }
    });
    return await response.json();
  }
  
  async dailyCheck() {
    const cycleDay = this.getCycleDay();
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    
    const data = await this.getOuraData(yesterday, today);
    if (!data.data || data.data.length === 0) {
      console.log('No Oura data available');
      return;
    }
    
    const latest = data.data[data.data.length - 1];
    const hvrBalance = latest.contributors?.hrv_balance || 0;
    const tempDeviation = latest.temperature_deviation || 0;
    
    console.log(`Day ${cycleDay}: HRV=${hvrBalance}, Temp=${tempDeviation.toFixed(2)}°C`);
    
    // Check for ovulation signals
    const expectedOv = this.getExpectedOvulation();
    if (cycleDay >= expectedOv.min && cycleDay <= expectedOv.max) {
      if (hvrBalance < this.config.alerts.hvrThreshold) {
        console.log('⚠️  Significant HRV drop detected');
        
        if (Math.abs(tempDeviation) < this.config.alerts.tempThreshold) {
          console.log('✅ Temperature normal - likely hormonal');
          console.log('🔔 Recommendation: Take LH test today');
        } else {
          console.log('⚠️  Temperature elevated - check for illness');
          if (this.config.alerts.oysterProtocol) {
            await this.sendOysterAlert(`HRV=${hvrBalance}, Temp=${tempDeviation.toFixed(2)}°C`);
          }
        }
      }
    }
    
    return { cycleDay, hvrBalance, tempDeviation };
  }
  
  async recordLHTest(result) {
    const cycleDay = this.getCycleDay();
    
    if (result === 'positive') {
      console.log(`✅ LH surge detected on Day ${cycleDay}`);
      await this.sendOvulationAlert({
        cycleDay,
        surgeDetected: new Date().toISOString(),
        expectedOvulation: 'Tomorrow or day after (12-36h window)',
        fertilityWindow: 'TODAY through +48 hours',
        action: 'Sex tonight + tomorrow night for optimal timing'
      });
    } else {
      console.log(`ℹ️  LH negative on Day ${cycleDay} - continue monitoring`);
    }
  }
  
  async sendOvulationAlert(data) {
    const transporter = nodemailer.createTransport({
      service: this.config.email.service,
      auth: {
        user: this.config.email.from,
        pass: this.config.email.pass
      }
    });
    
    const subject = `🎯 Ovulation Alert: Fertile Window Open (Day ${data.cycleDay})`;
    const body = `
LH SURGE DETECTED TODAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ovulation happening in next 12-36 hours.

📅 TIMING:
• LH Surge: Today (Day ${data.cycleDay})
• Expected Ovulation: ${data.expectedOvulation}
• Peak Fertility: ${data.fertilityWindow}

🎯 ACTION PLAN:
✅ Sex tonight
✅ Sex tomorrow
✅ Optional: Day after for extra coverage

Temperature spike will confirm ovulation in 1-2 days.

Good luck! 🍀

—Kale 🥬
Your AI Fertility Tracker
`;
    
    await transporter.sendMail({
      from: this.config.email.from,
      to: this.config.email.to,
      subject: subject,
      text: body
    });
    
    console.log(`✅ Ovulation alert sent to ${this.config.email.to}`);
  }
  
  async sendOysterAlert(reason) {
    const transporter = nodemailer.createTransport({
      service: this.config.email.service,
      auth: {
        user: this.config.email.from,
        pass: this.config.email.pass
      }
    });
    
    const subject = '🦪 Oyster Alert: Significant HRV Drop + Elevated Temperature';
    const body = `
OYSTER PROTOCOL TRIGGERED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Significant stress/illness indicators detected.

📊 METRICS:
${reason}

⚠️ RECOMMENDATION:
This combination suggests illness or severe stress, not just hormonal changes.

🛑 ACTION:
• Rest today
• Monitor symptoms
• Hydrate well
• Check temperature manually

Will continue monitoring. Update you tomorrow.

—Kale 🥬
Your AI Health Guardian
`;
    
    await transporter.sendMail({
      from: this.config.email.from,
      to: this.config.email.to,
      subject: subject,
      text: body
    });
    
    console.log(`⚠️  Oyster alert sent to ${this.config.email.to}`);
  }
  
  async confirmOvulation() {
    const cycleDay = this.getCycleDay();
    const today = new Date().toISOString().split('T')[0];
    const twoDaysAgo = new Date(Date.now() - 172800000).toISOString().split('T')[0];
    
    const data = await this.getOuraData(twoDaysAgo, today);
    if (!data.data || data.data.length < 2) {
      console.log('Not enough data for confirmation');
      return false;
    }
    
    const recent = data.data.slice(-2);
    const avgTemp = recent.reduce((sum, d) => sum + (d.temperature_deviation || 0), 0) / recent.length;
    
    if (avgTemp >= 0.3 && avgTemp <= 0.8) {
      console.log(`✅ Temperature spike confirmed (${avgTemp.toFixed(2)}°C) - ovulation occurred`);
      return true;
    } else {
      console.log(`ℹ️  No temperature spike yet (${avgTemp.toFixed(2)}°C) - waiting`);
      return false;
    }
  }
}

module.exports = FertilityTracker;
