#!/usr/bin/env node

/**
 * Meeting Efficiency Pro - Setup Wizard
 * Interactive setup for configuring the skill
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const configPath = path.join(__dirname, '..', 'config', 'default.json');

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

async function runSetup() {
  console.log('🚀 Meeting Efficiency Pro - Setup Wizard\n');
  console.log('This wizard will help you configure the skill.\n');

  // Load existing config or create default
  let config = {};
  try {
    if (fs.existsSync(configPath)) {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      console.log('📁 Found existing configuration.\n');
    }
  } catch (error) {
    console.log('⚠️ Could not load existing config, starting fresh.\n');
  }

  console.log('=== AI Provider Configuration ===\n');
  
  const aiProvider = await question('Select AI provider (openai/grok/none) [openai]: ') || 'openai';
  config.ai_provider = aiProvider.toLowerCase();
  
  if (config.ai_provider !== 'none') {
    const apiKey = await question(`Enter your ${config.ai_provider.toUpperCase()} API key (press Enter to skip): `);
    if (apiKey) {
      config.ai_api_key = apiKey;
    } else {
      console.log('⚠️ No API key provided. Some features will be limited.\n');
    }
  }

  console.log('\n=== Calendar Integration ===\n');
  
  const calendarType = await question('Select calendar type (google/outlook/ical/none) [none]: ') || 'none';
  config.calendar_type = calendarType.toLowerCase();
  
  if (config.calendar_type !== 'none') {
    console.log(`\n📝 ${config.calendar_type.charAt(0).toUpperCase() + config.calendar_type.slice(1)} Calendar setup:`);
    console.log('You will need to configure OAuth credentials separately.');
    console.log('See references/calendar-setup.md for instructions.\n');
  }

  console.log('=== Task Manager Integration ===\n');
  
  const taskManager = await question('Select task manager (todoist/asana/jira/none) [none]: ') || 'none';
  config.task_manager = taskManager.toLowerCase();
  
  if (config.task_manager !== 'none') {
    const token = await question(`Enter your ${config.task_manager} API token (press Enter to skip): `);
    if (token) {
      config.task_manager_token = token;
    }
  }

  console.log('\n=== Automation Settings ===\n');
  
  const autoBriefing = await question('Enable daily briefing? (yes/no) [yes]: ') || 'yes';
  config.auto_briefing = autoBriefing.toLowerCase() === 'yes';
  
  if (config.auto_briefing) {
    const briefingTime = await question('Daily briefing time (HH:MM) [08:00]: ') || '08:00';
    config.briefing_time = briefingTime;
  }

  const efficiencyThreshold = await question('Efficiency threshold (0-100) [70]: ') || '70';
  config.efficiency_threshold = parseInt(efficiencyThreshold);

  console.log('\n=== Notification Settings ===\n');
  
  const efficiencyAlerts = await question('Receive efficiency alerts? (yes/no) [yes]: ') || 'yes';
  const dailyBriefing = await question('Receive daily briefing? (yes/no) [yes]: ') || 'yes';
  const weeklyReport = await question('Receive weekly report? (yes/no) [yes]: ') || 'yes';
  
  config.notifications = {
    efficiency_alerts: efficiencyAlerts.toLowerCase() === 'yes',
    daily_briefing: dailyBriefing.toLowerCase() === 'yes',
    weekly_report: weeklyReport.toLowerCase() === 'yes'
  };

  console.log('\n=== Analytics Settings ===\n');
  
  const trackEfficiency = await question('Track efficiency metrics? (yes/no) [yes]: ') || 'yes';
  const trackSavings = await question('Track time savings? (yes/no) [yes]: ') || 'yes';
  const trackCosts = await question('Track meeting costs? (yes/no) [yes]: ') || 'yes';
  
  config.analytics = {
    track_efficiency: trackEfficiency.toLowerCase() === 'yes',
    track_time_savings: trackSavings.toLowerCase() === 'yes',
    track_costs: trackCosts.toLowerCase() === 'yes'
  };

  console.log('\n=== Saving Configuration ===\n');
  
  // Ensure config directory exists
  const configDir = path.dirname(configPath);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // Save configuration
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`✅ Configuration saved to: ${configPath}\n`);
  
  console.log('=== Setup Summary ===\n');
  console.log('AI Provider:', config.ai_provider);
  console.log('Calendar:', config.calendar_type);
  console.log('Task Manager:', config.task_manager);
  console.log('Daily Briefing:', config.auto_briefing ? `Enabled (${config.briefing_time})` : 'Disabled');
  console.log('Efficiency Threshold:', config.efficiency_threshold);
  console.log('\n=== Next Steps ===\n');
  
  if (config.calendar_type !== 'none') {
    console.log('1. Configure calendar OAuth credentials');
    console.log('   See: references/calendar-setup.md');
  }
  
  if (config.ai_provider !== 'none' && !config.ai_api_key) {
    console.log('2. Add your API key to config/default.json');
    console.log('   Or set it as environment variable');
  }
  
  console.log('\n3. Test your setup:');
  console.log('   /meeting-efficiency-pro test');
  console.log('\n4. Run a demo:');
  console.log('   /meeting-efficiency-pro demo');
  console.log('\n5. Get your first briefing:');
  console.log('   /meeting-efficiency-pro briefing');
  console.log('\n🎉 Setup complete! Your meeting optimization journey begins now.');
  
  rl.close();
}

// Handle cleanup
process.on('SIGINT', () => {
  console.log('\n\nSetup cancelled.');
  rl.close();
  process.exit(0);
});

// Run setup
runSetup().catch(error => {
  console.error('Setup error:', error);
  rl.close();
  process.exit(1);
});