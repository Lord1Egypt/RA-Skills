#!/usr/bin/env node

/**
 * Meeting Efficiency Pro - Main Entry Point
 * AI-powered meeting optimization for OpenClaw
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

// Load configuration
const configPath = path.join(__dirname, 'config', 'default.json');
let config = {};

try {
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
} catch (error) {
  console.error('Error loading config:', error.message);
}

// Import modules
const Calendar = require('./lib/calendar');
const Analyzer = require('./lib/analyzer');
const Reporter = require('./lib/reporter');

class MeetingEfficiencyPro {
  constructor() {
    this.calendar = new Calendar(config);
    this.analyzer = new Analyzer(config);
    this.reporter = new Reporter(config);
    this.commands = {
      setup: this.setup.bind(this),
      briefing: this.briefing.bind(this),
      analyze: this.analyzeMeeting.bind(this),
      process: this.processNotes.bind(this),
      'weekly-report': this.weeklyReport.bind(this),
      config: this.showConfig.bind(this),
      test: this.test.bind(this),
      demo: this.demo.bind(this),
      help: this.help.bind(this)
    };
  }

  async run(command, args = {}) {
    if (this.commands[command]) {
      return await this.commands[command](args);
    } else {
      console.error(`Unknown command: ${command}`);
      return this.help();
    }
  }

  async setup(args) {
    console.log('🚀 Setting up Meeting Efficiency Pro...\n');
    
    // Check for Node.js version
    try {
      const { stdout } = await execPromise('node --version');
      console.log(`✓ Node.js ${stdout.trim()}`);
    } catch (error) {
      console.error('✗ Node.js not found. Please install Node.js 16+');
      return;
    }

    // Check for npm
    try {
      const { stdout } = await execPromise('npm --version');
      console.log(`✓ npm ${stdout.trim()}`);
    } catch (error) {
      console.error('✗ npm not found');
      return;
    }

    // Install dependencies
    console.log('\n📦 Installing dependencies...');
    try {
      const { stdout, stderr } = await execPromise('npm install', { cwd: __dirname });
      console.log('✓ Dependencies installed');
    } catch (error) {
      console.error('✗ Failed to install dependencies:', error.message);
      return;
    }

    // Create default config if it doesn't exist
    if (!fs.existsSync(configPath)) {
      const defaultConfig = {
        ai_provider: 'openai',
        ai_api_key: '',
        calendar_type: 'none',
        auto_briefing: true,
        briefing_time: '08:00',
        efficiency_threshold: 70,
        task_manager: 'none'
      };

      const configDir = path.dirname(configPath);
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }

      fs.writeFileSync(configPath, JSON.stringify(defaultConfig, null, 2));
      console.log('✓ Created default configuration');
    }

    console.log('\n✅ Setup complete!');
    console.log('\nNext steps:');
    console.log('1. Edit config/default.json with your settings');
    console.log('2. Run /meeting-efficiency-pro test to verify setup');
    console.log('3. Run /meeting-efficiency-pro briefing for your first meeting analysis');
  }

  async briefing(args) {
    console.log('📅 Generating today\'s meeting briefing...\n');
    
    try {
      const meetings = await this.calendar.getTodaysMeetings();
      
      if (meetings.length === 0) {
        console.log('No meetings scheduled for today. Enjoy your productive day! 🎉');
        return;
      }

      console.log(`Found ${meetings.length} meeting(s) for today:\n`);
      
      for (const meeting of meetings) {
        const analysis = await this.analyzer.analyzeMeeting(meeting);
        console.log(`📌 ${meeting.title}`);
        console.log(`   ⏰ ${meeting.startTime} - ${meeting.endTime} (${meeting.duration} minutes)`);
        console.log(`   👥 Attendees: ${meeting.attendees || 'Not specified'}`);
        console.log(`   🎯 Efficiency Score: ${analysis.efficiencyScore}/100`);
        
        if (analysis.suggestions && analysis.suggestions.length > 0) {
          console.log(`   💡 Suggestions:`);
          analysis.suggestions.forEach(suggestion => {
            console.log(`     • ${suggestion}`);
          });
        }
        console.log('');
      }

      const summary = await this.analyzer.generateDailySummary(meetings);
      console.log('📊 Daily Summary:');
      console.log(`   Total meeting time: ${summary.totalMinutes} minutes`);
      console.log(`   Average efficiency: ${summary.averageEfficiency}/100`);
      console.log(`   Potential time savings: ${summary.potentialSavings} minutes`);
      
    } catch (error) {
      console.error('Error generating briefing:', error.message);
      console.log('\n💡 Tip: Run /meeting-efficiency-pro setup to configure calendar integration');
    }
  }

  async analyzeMeeting(args) {
    const meetingTitle = args._[0] || args.meeting;
    
    if (!meetingTitle) {
      console.error('Please provide a meeting title to analyze');
      console.log('Usage: /meeting-efficiency-pro analyze "Team Standup"');
      return;
    }

    console.log(`🔍 Analyzing meeting: ${meetingTitle}\n`);
    
    try {
      // For now, create a sample meeting object
      // In a real implementation, this would fetch from calendar
      const sampleMeeting = {
        title: meetingTitle,
        description: 'Sample meeting for analysis',
        duration: 60,
        attendees: 5,
        type: 'team'
      };

      const analysis = await this.analyzer.analyzeMeeting(sampleMeeting);
      
      console.log('📋 Meeting Analysis:');
      console.log(`   Efficiency Score: ${analysis.efficiencyScore}/100`);
      console.log(`   Meeting Type: ${analysis.meetingType}`);
      console.log(`   Optimal Duration: ${analysis.optimalDuration} minutes`);
      
      if (analysis.recommendations && analysis.recommendations.length > 0) {
        console.log('\n💡 Recommendations:');
        analysis.recommendations.forEach(rec => {
          console.log(`   • ${rec}`);
        });
      }
      
    } catch (error) {
      console.error('Error analyzing meeting:', error.message);
    }
  }

  async processNotes(args) {
    const notesFile = args.notes || args._[0];
    
    if (!notesFile) {
      console.error('Please provide meeting notes file');
      console.log('Usage: /meeting-efficiency-pro process --notes meeting-notes.txt');
      return;
    }

    console.log(`📝 Processing meeting notes: ${notesFile}\n`);
    
    try {
      let notesContent;
      
      if (fs.existsSync(notesFile)) {
        notesContent = fs.readFileSync(notesFile, 'utf8');
      } else if (fs.existsSync(path.join(__dirname, notesFile))) {
        notesContent = fs.readFileSync(path.join(__dirname, notesFile), 'utf8');
      } else {
        // Assume notes are provided directly
        notesContent = notesFile;
      }

      const result = await this.analyzer.processMeetingNotes(notesContent);
      
      console.log('✅ Meeting Notes Analysis Complete\n');
      console.log('📋 Summary:');
      result.summary.forEach(point => {
        console.log(`   • ${point}`);
      });
      
      console.log('\n🎯 Action Items:');
      if (result.actionItems && result.actionItems.length > 0) {
        result.actionItems.forEach(item => {
          console.log(`   • ${item.text} (Owner: ${item.owner}, Due: ${item.dueDate})`);
        });
      } else {
        console.log('   No action items identified');
      }
      
      console.log('\n🤔 Unresolved Questions:');
      if (result.questions && result.questions.length > 0) {
        result.questions.forEach(question => {
          console.log(`   • ${question}`);
        });
      } else {
        console.log('   All questions resolved');
      }
      
      console.log(`\n📊 Meeting Efficiency: ${result.efficiencyScore}/100`);
      
    } catch (error) {
      console.error('Error processing notes:', error.message);
    }
  }

  async weeklyReport(args) {
    console.log('📈 Generating weekly efficiency report...\n');
    
    try {
      // Get meetings from the past week
      const meetings = await this.calendar.getWeeklyMeetings();
      
      if (meetings.length === 0) {
        console.log('No meetings found for the past week.');
        return;
      }

      const report = await this.reporter.generateWeeklyReport(meetings);
      
      console.log('📊 Weekly Meeting Efficiency Report');
      console.log('====================================\n');
      
      console.log(`📅 Period: ${report.period}`);
      console.log(`📋 Total Meetings: ${report.totalMeetings}`);
      console.log(`⏰ Total Time: ${report.totalMinutes} minutes (${Math.round(report.totalMinutes / 60)} hours)`);
      console.log(`🎯 Average Efficiency: ${report.averageEfficiency}/100`);
      console.log(`💰 Estimated Cost: $${report.estimatedCost.toFixed(2)}`);
      console.log(`⏱️ Potential Savings: ${report.potentialSavings} minutes\n`);
      
      console.log('📈 Efficiency Trends:');
      report.trends.forEach(trend => {
        const trendIcon = trend.change > 0 ? '📈' : trend.change < 0 ? '📉' : '➡️';
        console.log(`   ${trendIcon} ${trend.category}: ${trend.value} (${trend.change > 0 ? '+' : ''}${trend.change}%)`);
      });
      
      console.log('\n🏆 Most Efficient Meetings:');
      report.topMeetings.forEach(meeting => {
        console.log(`   • ${meeting.title}: ${meeting.efficiency}/100`);
      });
      
      console.log('\n💡 Recommendations:');
      report.recommendations.forEach(rec => {
        console.log(`   • ${rec}`);
      });
      
    } catch (error) {
      console.error('Error generating weekly report:', error.message);
      console.log('\n💡 Tip: Configure calendar integration for accurate reporting');
    }
  }

  async showConfig(args) {
    console.log('⚙️ Current Configuration:\n');
    console.log(JSON.stringify(config, null, 2));
    
    console.log('\n📁 Config file location:', configPath);
    console.log('\n💡 To edit: edit config/default.json');
  }

  async test(args) {
    console.log('🧪 Running system tests...\n');
    
    const tests = [
      { name: 'Config file', test: () => fs.existsSync(configPath) },
      { name: 'Node modules', test: () => fs.existsSync(path.join(__dirname, 'node_modules')) },
      { name: 'Calendar module', test: () => fs.existsSync(path.join(__dirname, 'lib', 'calendar.js')) },
      { name: 'Analyzer module', test: () => fs.existsSync(path.join(__dirname, 'lib', 'analyzer.js')) },
      { name: 'Reporter module', test: () => fs.existsSync(path.join(__dirname, 'lib', 'reporter.js')) }
    ];

    let passed = 0;
    let failed = 0;

    for (const test of tests) {
      try {
        const result = test.test();
        if (result) {
          console.log(`✅ ${test.name}: OK`);
          passed++;
        } else {
          console.log(`❌ ${test.name}: Missing`);
          failed++;
        }
      } catch (error) {
        console.log(`❌ ${test.name}: Error - ${error.message}`);
        failed++;
      }
    }

    console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
    
    if (failed === 0) {
      console.log('\n🎉 All tests passed! System is ready.');
    } else {
      console.log('\n⚠️ Some tests failed. Run /meeting-efficiency-pro setup to fix issues.');
    }
  }

  async demo(args) {
    console.log('🎬 Running Meeting Efficiency Pro Demo...\n');
    
    // Run demo script
    const demoPath = path.join(__dirname, 'scripts', 'demo.js');
    
    if (fs.existsSync(demoPath)) {
      try {
        require(demoPath);
      } catch (error) {
        console.error('Error running demo:', error.message);
      }
    } else {
      console.log('Demo script not found. Creating sample demo...\n');
      
      console.log('📅 Sample Meeting Briefing:');
      console.log('---------------------------');
      console.log('1. Team Standup (9:00 AM - 9:15 AM)');
      console.log('   Efficiency: 85/100 ✓');
      console.log('   Suggestions: Consider reducing to 10 minutes');
      console.log('');
      console.log('2. Project Review (10:00 AM - 11:00 AM)');
      console.log('   Efficiency: 65/100 ⚠️');
      console.log('   Suggestions: Add agenda, reduce attendees from 8 to 5');
      console.log('');
      console.log('3. Client Call (2:00 PM - 3:00 PM)');
      console.log('   Efficiency: 90/100 ✓');
      console.log('   Suggestions: Send pre-meeting materials');
      console.log('');
      console.log('📊 Daily Summary:');
      console.log('• Total meeting time: 135 minutes');
      console.log('• Average efficiency: 80/100');
      console.log('• Potential savings: 27 minutes (20%)');
    }
  }

  help(args) {
    console.log('Meeting Efficiency Pro - Help\n');
    console.log('Usage: /meeting-efficiency-pro <command> [options]\n');
    console.log('Commands:');
    console.log('  setup                     Run interactive setup wizard');
    console.log('  briefing                  Get today\'s meeting briefing');
    console.log('  analyze <meeting-title>   Analyze specific meeting');
    console.log('  process --notes <file>    Process meeting notes file');
    console.log('  weekly-report             Generate weekly efficiency report');
    console.log('  config                    View current configuration');
    console.log('  test                      Run system tests');
    console.log('  demo                      Run demonstration');
    console.log('  help                      Show this help message\n');
    console.log('Examples:');
    console.log('  /meeting-efficiency-pro briefing');
    console.log('  /meeting-efficiency-pro analyze "Team Standup"');
    console.log('  /meeting-efficiency-pro process --notes "meeting-notes.txt"');
    console.log('  /meeting-efficiency-pro weekly-report\n');
    console.log('Documentation: https://clawhub.com/skills/meeting-efficiency-pro');
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
const command = args[0] || 'help';
const commandArgs = {};

// Simple argument parsing
for (let i = 1; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].substring(2);
    commandArgs[key] = args[i + 1] || true;
    i++;
  } else {
    if (!commandArgs._) commandArgs._ = [];
    commandArgs._.push(args[i]);
  }
}

// Run the skill
const skill = new MeetingEfficiencyPro();
skill.run(command, commandArgs).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});