#!/usr/bin/env node

/**
 * Daily Planner Skill - Main Implementation
 * Proactive personal assistant for daily planning and motivation
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// Load configuration
const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Utility functions
function getCurrentDate() {
  const now = new Date();
  return {
    date: now.toISOString().split('T')[0],
    day: now.toLocaleDateString('en-US', { weekday: 'long' }),
    time: now.toLocaleTimeString('en-US', { hour12: false }),
    hour: now.getHours(),
    timestamp: now.toISOString()
  };
}

function getTimeOfDay(hour) {
  if (hour >= 5 && hour < 12) return 'morning';
  if (hour >= 12 && hour < 17) return 'afternoon';
  if (hour >= 17 && hour < 22) return 'evening';
  return 'night';
}

function loadTemplate(templateName) {
  const templatePath = path.join(__dirname, 'templates', `${templateName}.md`);
  try {
    return fs.readFileSync(templatePath, 'utf8');
  } catch (error) {
    return `# ${templateName.charAt(0).toUpperCase() + templateName.slice(1)} Planning\n\nPlan your ${templateName} here.`;
  }
}

function getRandomMotivation() {
  const messages = config.motivation.messages;
  return messages[Math.floor(Math.random() * messages.length)];
}

function getCelebrationMessage(progress) {
  if (progress >= 100) {
    return config.motivation.celebrationMessages[0];
  } else if (progress >= 75) {
    return config.motivation.celebrationMessages[1];
  } else if (progress >= 50) {
    return config.motivation.celebrationMessages[2];
  } else if (progress >= 25) {
    return config.motivation.celebrationMessages[3];
  }
  return config.motivation.celebrationMessages[4];
}

// Core planning functions
function createMorningPlan() {
  const current = getCurrentDate();
  const timeOfDay = getTimeOfDay(current.hour);
  
  console.log(`🌅 Good morning ${config.user.name}!`);
  console.log(`📅 Today is ${current.day}, ${current.date}`);
  console.log(`⏰ Current time: ${current.time}`);
  console.log('='.repeat(50));
  
  const template = loadTemplate('morning');
  const plan = template
    .replace('{date}', current.date)
    .replace('{day}', current.day)
    .replace('{user}', config.user.name)
    .replace('{motivation}', getRandomMotivation());
  
  console.log(plan);
  console.log('='.repeat(50));
  
  // Save plan to file
  const planPath = config.storage.dailyPlansPath.replace('{date}', current.date);
  const fullPath = planPath.replace('~', process.env.HOME || os.homedir());
  fs.writeFileSync(fullPath, plan);
  
  console.log(`💾 Plan saved to: ${fullPath}`);
  
  return plan;
}

function checkProgress() {
  const current = getCurrentDate();
  const timeOfDay = getTimeOfDay(current.hour);
  
  console.log(`📊 ${timeOfDay.charAt(0).toUpperCase() + timeOfDay.slice(1)} Progress Check`);
  console.log(`⏰ ${current.time}`);
  console.log('='.repeat(50));
  
  // In a real implementation, this would read actual progress
  // For now, simulate progress check
  const progress = Math.floor(Math.random() * 100);
  const tasksCompleted = Math.floor(progress / 100 * config.planning.maxTasksPerDay);
  
  console.log(`🎯 Progress: ${progress}% complete`);
  console.log(`✅ Tasks completed: ${tasksCompleted}/${config.planning.maxTasksPerDay}`);
  console.log(`💬 ${getCelebrationMessage(progress)}`);
  console.log(`✨ ${getRandomMotivation()}`);
  console.log('='.repeat(50));
  
  if (progress < 50 && current.hour >= 14) {
    console.log('⚠️  You\'re falling behind schedule. Consider adjusting your plan.');
  }
  
  return { progress, tasksCompleted };
}

function eveningReview() {
  const current = getCurrentDate();
  
  console.log(`🌙 Evening Review - ${current.day}, ${current.date}`);
  console.log(`⏰ ${current.time}`);
  console.log('='.repeat(50));
  
  const template = loadTemplate('evening');
  const review = template
    .replace('{date}', current.date)
    .replace('{day}', current.day)
    .replace('{user}', config.user.name);
  
  console.log(review);
  console.log('='.repeat(50));
  
  // Ask about tomorrow's plan
  console.log('🔮 Quick preview for tomorrow:');
  console.log('1. What\'s the most important task for tomorrow?');
  console.log('2. Any meetings or appointments?');
  console.log('3. What would make tomorrow a great day?');
  console.log('='.repeat(50));
  
  console.log('💤 Good night! Rest well and recharge for tomorrow. 🌟');
  
  return review;
}

function sendNotification(message, channel = 'telegram') {
  if (!config.notifications.enabled) return;
  
  console.log(`📨 Sending notification via ${channel}:`);
  console.log(message);
  
  // In a real implementation, this would use OpenClaw's messaging system
  // For now, just log it
  const notification = {
    channel,
    message,
    timestamp: getCurrentDate().timestamp,
    type: 'daily-planner'
  };
  
  console.log('✅ Notification prepared (would be sent via OpenClaw messaging)');
  return notification;
}

// Command line interface
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'auto';
  
  switch (command) {
    case 'morning':
      createMorningPlan();
      break;
      
    case 'progress':
    case 'check':
      checkProgress();
      break;
      
    case 'evening':
    case 'review':
      eveningReview();
      break;
      
    case 'motivate':
      console.log(`💪 ${getRandomMotivation()}`);
      break;
      
    case 'auto':
      const current = getCurrentDate();
      const timeOfDay = getTimeOfDay(current.hour);
      
      switch (timeOfDay) {
        case 'morning':
          createMorningPlan();
          break;
        case 'afternoon':
          checkProgress();
          break;
        case 'evening':
          eveningReview();
          break;
        default:
          console.log(`🌙 Good ${timeOfDay}, ${config.user.name}!`);
          console.log(`✨ ${getRandomMotivation()}`);
      }
      break;
      
    case 'help':
    default:
      showHelp();
      break;
  }
}

function showHelp() {
  console.log('📅 Daily Planner Skill - Usage Guide');
  console.log('='.repeat(50));
  console.log('Commands:');
  console.log('  morning     - Create morning plan');
  console.log('  progress    - Check current progress');
  console.log('  evening     - Evening review');
  console.log('  motivate    - Get random motivation');
  console.log('  auto        - Auto-detect based on time (default)');
  console.log('  help        - Show this help');
  console.log('');
  console.log('Examples:');
  console.log('  node planner.js morning');
  console.log('  node planner.js progress');
  console.log('  node planner.js auto');
  console.log('');
  console.log('Configuration:');
  console.log(`  User: ${config.user.name}`);
  console.log(`  Timezone: ${config.user.timezone}`);
  console.log(`  Schedule: ${config.schedule.morningCheckin}, ${config.schedule.afternoonCheckin}, ${config.schedule.eveningReview}`);
  console.log('='.repeat(50));
}

// Run if called directly
if (require.main === module) {
  main();
}

// Export for testing and integration
module.exports = {
  createMorningPlan,
  checkProgress,
  eveningReview,
  getRandomMotivation,
  getCurrentDate,
  config
};