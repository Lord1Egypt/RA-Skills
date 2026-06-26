#!/usr/bin/env node

/**
 * Meeting Efficiency Pro - Demo Script
 * Demonstrates the skill's capabilities with sample data
 */

const path = require('path');
const fs = require('fs');

// Add parent directory to module path
const parentDir = path.dirname(__dirname);
require('module').Module._nodeModulePaths(parentDir);

// Import skill modules
const Calendar = require('../lib/calendar');
const Analyzer = require('../lib/analyzer');
const Reporter = require('../lib/reporter');

// Demo configuration
const demoConfig = {
  ai_provider: 'openai',
  ai_api_key: 'demo-key',
  calendar_type: 'none',
  efficiency_threshold: 70
};

async function runDemo() {
  console.log('🎬 Meeting Efficiency Pro - Demonstration\n');
  console.log('==========================================\n');

  // Initialize modules
  const calendar = new Calendar(demoConfig);
  const analyzer = new Analyzer(demoConfig);
  const reporter = new Reporter(demoConfig);
  reporter.setAnalyzer(analyzer);

  console.log('1. 📅 Calendar Integration Demo');
  console.log('--------------------------------\n');
  
  const connectionTest = await calendar.testConnection();
  console.log(`Calendar Status: ${connectionTest.connected ? '✅ Connected' : '⚠️ Not Configured'}`);
  console.log(`Message: ${connectionTest.message}\n`);

  console.log('2. 🎯 Meeting Analysis Demo');
  console.log('---------------------------\n');
  
  const sampleMeeting = {
    id: 'demo-1',
    title: 'Quarterly Planning Session',
    description: 'Review Q3 results and plan Q4 initiatives with cross-functional team',
    startTime: '10:00',
    endTime: '12:00',
    duration: 120,
    attendees: 8,
    location: 'Board Room',
    recurring: false
  };

  console.log(`Analyzing: "${sampleMeeting.title}"`);
  console.log(`Duration: ${sampleMeeting.duration} minutes`);
  console.log(`Attendees: ${sampleMeeting.attendees}\n`);

  const analysis = await analyzer.analyzeMeeting(sampleMeeting);
  
  console.log('Analysis Results:');
  console.log(`  Efficiency Score: ${analysis.efficiencyScore}/100`);
  console.log(`  Meeting Type: ${analysis.meetingType}`);
  console.log(`  Optimal Duration: ${analysis.optimalDuration} minutes`);
  
  if (analysis.suggestions && analysis.suggestions.length > 0) {
    console.log(`  Suggestions:`);
    analysis.suggestions.forEach(suggestion => {
      console.log(`    • ${suggestion}`);
    });
  }

  console.log('\n3. 📝 Meeting Notes Processing Demo');
  console.log('-----------------------------------\n');
  
  const sampleNotes = `
Team Standup - March 14, 2025
Attendees: Alice, Bob, Charlie, Diana

Discussion:
- Project Alpha: Development on track, demo scheduled for Friday
- Project Beta: API integration delayed due to third-party issues
- Project Gamma: Design review completed, implementation starts Monday

Action Items:
- Alice: Follow up with API vendor about Beta integration (Due: Tomorrow)
- Bob: Prepare Alpha demo materials (Due: Friday)
- Charlie: Schedule Gamma kickoff meeting (Due: Today)

Decisions:
- Will extend Beta timeline by one week
- Approved additional budget for Alpha testing

Questions:
- Should we bring in additional resources for Beta?
- What's the priority for next week?

Unresolved:
- Budget approval for Gamma Phase 2
  `.trim();

  console.log('Processing meeting notes...\n');
  const notesAnalysis = await analyzer.processMeetingNotes(sampleNotes);
  
  console.log('Extracted Information:');
  console.log(`  Efficiency Score: ${notesAnalysis.efficiencyScore}/100`);
  
  console.log(`  Summary Points:`);
  notesAnalysis.summary.slice(0, 3).forEach(point => {
    console.log(`    • ${point}`);
  });
  
  console.log(`\n  Action Items:`);
  notesAnalysis.actionItems.forEach(item => {
    console.log(`    • ${item.text}`);
    console.log(`      Owner: ${item.owner}, Due: ${item.dueDate}, Priority: ${item.priority}`);
  });
  
  console.log(`\n  Questions:`);
  notesAnalysis.questions.forEach(question => {
    console.log(`    • ${question}`);
  });

  console.log('\n4. 📊 Weekly Reporting Demo');
  console.log('---------------------------\n');
  
  console.log('Generating weekly efficiency report...\n');
  const weeklyMeetings = calendar.getSampleMeetings('week');
  const weeklyReport = await reporter.generateWeeklyReport(weeklyMeetings);
  
  console.log('Weekly Report Summary:');
  console.log(`  Period: ${weeklyReport.period}`);
  console.log(`  Total Meetings: ${weeklyReport.totalMeetings}`);
  console.log(`  Total Time: ${weeklyReport.totalMinutes} minutes`);
  console.log(`  Average Efficiency: ${weeklyReport.averageEfficiency}/100`);
  console.log(`  Estimated Cost: $${weeklyReport.estimatedCost.toFixed(2)}`);
  console.log(`  Potential Savings: ${weeklyReport.potentialSavings} minutes\n`);
  
  console.log('Top Recommendations:');
  weeklyReport.recommendations.slice(0, 3).forEach((rec, index) => {
    console.log(`  ${index + 1}. ${rec}`);
  });

  console.log('\n5. 💡 Efficiency Optimization Demo');
  console.log('----------------------------------\n');
  
  const inefficientMeeting = {
    id: 'demo-2',
    title: 'Weekly Status Update',
    description: 'General team status update',
    startTime: '14:00',
    endTime: '16:00',
    duration: 120,
    attendees: 12,
    location: 'Conference Room',
    recurring: true
  };

  console.log(`Inefficient Meeting: "${inefficientMeeting.title}"`);
  console.log(`Current: ${inefficientMeeting.duration} minutes, ${inefficientMeeting.attendees} attendees\n`);
  
  const inefficientAnalysis = await analyzer.analyzeMeeting(inefficientMeeting);
  
  console.log('Current Analysis:');
  console.log(`  Efficiency Score: ${inefficientAnalysis.efficiencyScore}/100 ⚠️`);
  console.log(`  Meeting Type: ${inefficientAnalysis.meetingType}`);
  console.log(`  Optimal Duration: ${analyzer.calculateOptimalDuration(inefficientMeeting)} minutes`);
  console.log(`  Optimal Attendees: ${analyzer.calculateOptimalAttendees(inefficientMeeting)} people\n`);
  
  console.log('Optimization Suggestions:');
  inefficientAnalysis.suggestions.forEach((suggestion, index) => {
    console.log(`  ${index + 1}. ${suggestion}`);
  });

  console.log('\n6. 📈 ROI Calculation Demo');
  console.log('--------------------------\n');
  
  const weeklyStats = {
    totalMeetings: 15,
    totalMinutes: 720, // 12 hours
    averageEfficiency: 75,
    estimatedCost: 1800, // $1,800
    potentialSavings: 144 // 2.4 hours
  };
  
  console.log('Meeting Investment Analysis:');
  console.log(`  Weekly Meeting Time: ${weeklyStats.totalMinutes} minutes (${weeklyStats.totalMinutes/60} hours)`);
  console.log(`  Estimated Cost: $${weeklyStats.estimatedCost}`);
  console.log(`  Average Efficiency: ${weeklyStats.averageEfficiency}/100`);
  console.log(`  Potential Time Savings: ${weeklyStats.potentialSavings} minutes (${(weeklyStats.potentialSavings/weeklyStats.totalMinutes*100).toFixed(1)}%)\n`);
  
  const hourlyRate = 50;
  const potentialCostSavings = (weeklyStats.potentialSavings / 60) * hourlyRate * 8; // Assuming 8 attendees avg
  console.log(`  Potential Cost Savings: $${potentialCostSavings.toFixed(2)} per week`);
  console.log(`  Monthly Savings Potential: $${(potentialCostSavings * 4).toFixed(2)}`);
  console.log(`  Annual Savings Potential: $${(potentialCostSavings * 52).toFixed(2)}`);

  console.log('\n==========================================');
  console.log('🎉 Demo Complete!');
  console.log('\nKey Takeaways:');
  console.log('• AI-powered meeting analysis identifies inefficiencies');
  console.log('• Automated note processing extracts action items and decisions');
  console.log('• Weekly reporting tracks trends and ROI');
  console.log('• Optimization suggestions can save 20%+ of meeting time');
  console.log(`• Skill price: $149 | Potential annual savings: $${(potentialCostSavings * 52).toFixed(0)}+`);
  console.log('\nReady to optimize your meetings? Run:');
  console.log('  /meeting-efficiency-pro setup');
  console.log('  /meeting-efficiency-pro briefing');
}

// Run the demo
runDemo().catch(error => {
  console.error('Demo error:', error);
  process.exit(1);
});