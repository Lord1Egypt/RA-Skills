#!/usr/bin/env node

/**
 * Habit Tracker CLI
 * A command-line tool for tracking habits, logging progress, and viewing statistics
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const DATA_DIR = path.join(os.homedir(), '.config', 'habit-tracker');
const HABITS_FILE = path.join(DATA_DIR, 'habits.json');
const LOGS_FILE = path.join(DATA_DIR, 'logs.json');

// Ensure data directory exists
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// Load habits from file
function loadHabits() {
  ensureDataDir();
  if (!fs.existsSync(HABITS_FILE)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(HABITS_FILE, 'utf8'));
  } catch (e) {
    return [];
  }
}

// Save habits to file
function saveHabits(habits) {
  ensureDataDir();
  fs.writeFileSync(HABITS_FILE, JSON.stringify(habits, null, 2));
}

// Load logs from file
function loadLogs() {
  ensureDataDir();
  if (!fs.existsSync(LOGS_FILE)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(LOGS_FILE, 'utf8'));
  } catch (e) {
    return [];
  }
}

// Save logs to file
function saveLogs(logs) {
  ensureDataDir();
  fs.writeFileSync(LOGS_FILE, JSON.stringify(logs, null, 2));
}

// Generate unique ID
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Get today's date string (YYYY-MM-DD)
function getToday() {
  return new Date().toISOString().split('T')[0];
}

// Get current timestamp
function getTimestamp() {
  return new Date().toISOString();
}

// Add a new habit
function addHabit(name, options = {}) {
  const habits = loadHabits();

  // Check if habit already exists
  if (habits.some(h => h.name.toLowerCase() === name.toLowerCase())) {
    console.error(`Error: Habit "${name}" already exists.`);
    process.exit(1);
  }

  const habit = {
    id: generateId(),
    name: name,
    description: options.description || '',
    frequency: options.frequency || 'daily', // daily, weekly, monthly
    target: parseInt(options.target) || 1,
    reminder: options.reminder || null, // HH:MM format
    createdAt: getTimestamp(),
    active: true
  };

  habits.push(habit);
  saveHabits(habits);

  console.log(`✓ Habit "${name}" created successfully!`);
  console.log(`  ID: ${habit.id}`);
  console.log(`  Frequency: ${habit.frequency}`);
  console.log(`  Target: ${habit.target} time(s) per ${habit.frequency === 'daily' ? 'day' : habit.frequency === 'weekly' ? 'week' : 'month'}`);
  if (habit.reminder) {
    console.log(`  Reminder: ${habit.reminder}`);
  }
}

// List all habits
function listHabits() {
  const habits = loadHabits();

  if (habits.length === 0) {
    console.log('No habits found. Create one with: habit add <name>');
    return;
  }

  console.log('\n📋 Your Habits:\n');
  console.log('ID                           | Name                 | Frequency | Target | Reminder');
  console.log('-'.repeat(90));

  habits.forEach(habit => {
    const reminder = habit.reminder || '-';
    console.log(
      `${habit.id.substr(0, 28).padEnd(28)} | ${habit.name.substr(0, 20).padEnd(20)} | ${habit.frequency.padEnd(9)} | ${String(habit.target).padEnd(6)} | ${reminder}`
    );
  });
  console.log();
}

// Log a habit completion
function logHabit(habitIdOrName, options = {}) {
  const habits = loadHabits();
  const logs = loadLogs();

  // Find habit by ID or name
  let habit = habits.find(h => h.id === habitIdOrName);
  if (!habit) {
    habit = habits.find(h => h.name.toLowerCase() === habitIdOrName.toLowerCase());
  }

  if (!habit) {
    console.error(`Error: Habit "${habitIdOrName}" not found.`);
    process.exit(1);
  }

  const logEntry = {
    id: generateId(),
    habitId: habit.id,
    habitName: habit.name,
    date: options.date || getToday(),
    timestamp: getTimestamp(),
    note: options.note || '',
    count: parseInt(options.count) || 1
  };

  logs.push(logEntry);
  saveLogs(logs);

  console.log(`✓ Logged ${logEntry.count} completion(s) for "${habit.name}" on ${logEntry.date}`);
  if (logEntry.note) {
    console.log(`  Note: ${logEntry.note}`);
  }
}

// View habit logs
function viewLogs(habitIdOrName, options = {}) {
  const habits = loadHabits();
  const logs = loadLogs();

  let filteredLogs = logs;

  // Filter by habit if specified
  if (habitIdOrName) {
    let habit = habits.find(h => h.id === habitIdOrName);
    if (!habit) {
      habit = habits.find(h => h.name.toLowerCase() === habitIdOrName.toLowerCase());
    }

    if (!habit) {
      console.error(`Error: Habit "${habitIdOrName}" not found.`);
      process.exit(1);
    }

    filteredLogs = logs.filter(l => l.habitId === habit.id);
  }

  // Filter by date range
  if (options.days) {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - parseInt(options.days));
    filteredLogs = filteredLogs.filter(l => new Date(l.date) >= cutoff);
  }

  // Sort by date descending
  filteredLogs.sort((a, b) => new Date(b.date) - new Date(a.date));

  if (filteredLogs.length === 0) {
    console.log('No logs found.');
    return;
  }

  console.log('\n📝 Habit Logs:\n');
  console.log('Date       | Habit                | Count | Note');
  console.log('-'.repeat(70));

  filteredLogs.forEach(log => {
    console.log(
      `${log.date} | ${log.habitName.substr(0, 20).padEnd(20)} | ${String(log.count).padEnd(5)} | ${log.note || '-'}`
    );
  });
  console.log();
}

// Calculate statistics
function calculateStats(habitIdOrName, options = {}) {
  const habits = loadHabits();
  const logs = loadLogs();

  let targetHabits = habits;

  if (habitIdOrName) {
    let habit = habits.find(h => h.id === habitIdOrName);
    if (!habit) {
      habit = habits.find(h => h.name.toLowerCase() === habitIdOrName.toLowerCase());
    }

    if (!habit) {
      console.error(`Error: Habit "${habitIdOrName}" not found.`);
      process.exit(1);
    }

    targetHabits = [habit];
  }

  const days = parseInt(options.days) || 30;
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);

  console.log(`\n📊 Statistics (Last ${days} days):\n`);

  targetHabits.forEach(habit => {
    const habitLogs = logs.filter(l =>
      l.habitId === habit.id && new Date(l.date) >= cutoff
    );

    const totalCompletions = habitLogs.reduce((sum, l) => sum + l.count, 0);
    const uniqueDays = new Set(habitLogs.map(l => l.date)).size;

    // Calculate completion rate based on frequency
    let expectedCompletions = days;
    if (habit.frequency === 'weekly') {
      expectedCompletions = Math.ceil(days / 7) * habit.target;
    } else if (habit.frequency === 'monthly') {
      expectedCompletions = Math.ceil(days / 30) * habit.target;
    } else {
      expectedCompletions = days * habit.target;
    }

    const completionRate = expectedCompletions > 0
      ? Math.min(100, Math.round((totalCompletions / expectedCompletions) * 100))
      : 0;

    // Calculate streak
    const streak = calculateStreak(habit.id, logs);

    console.log(`📌 ${habit.name}`);
    console.log(`   Total completions: ${totalCompletions}`);
    console.log(`   Active days: ${uniqueDays}`);
    console.log(`   Completion rate: ${completionRate}%`);
    console.log(`   Current streak: ${streak.current} days`);
    console.log(`   Longest streak: ${streak.longest} days`);
    console.log();
  });
}

// Calculate streak
function calculateStreak(habitId, logs) {
  const habitLogs = logs
    .filter(l => l.habitId === habitId)
    .sort((a, b) => new Date(b.date) - new Date(a.date));

  const uniqueDates = [...new Set(habitLogs.map(l => l.date))].sort().reverse();

  let currentStreak = 0;
  let longestStreak = 0;
  let tempStreak = 0;
  let prevDate = null;

  const today = getToday();
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().split('T')[0];

  // Calculate current streak
  for (const date of uniqueDates) {
    if (currentStreak === 0 && (date === today || date === yesterdayStr)) {
      currentStreak = 1;
    } else if (currentStreak > 0) {
      const expectedDate = new Date(prevDate);
      expectedDate.setDate(expectedDate.getDate() - 1);
      if (date === expectedDate.toISOString().split('T')[0]) {
        currentStreak++;
      } else {
        break;
      }
    }
    prevDate = date;
  }

  // Calculate longest streak
  prevDate = null;
  for (const date of uniqueDates) {
    if (!prevDate) {
      tempStreak = 1;
    } else {
      const expectedDate = new Date(prevDate);
      expectedDate.setDate(expectedDate.getDate() - 1);
      if (date === expectedDate.toISOString().split('T')[0]) {
        tempStreak++;
      } else {
        longestStreak = Math.max(longestStreak, tempStreak);
        tempStreak = 1;
      }
    }
    prevDate = date;
  }
  longestStreak = Math.max(longestStreak, tempStreak);

  return { current: currentStreak, longest: longestStreak };
}

// Generate report
function generateReport(options = {}) {
  const habits = loadHabits();
  const logs = loadLogs();

  if (habits.length === 0) {
    console.log('No habits found. Create one with: habit add <name>');
    return;
  }

  const days = parseInt(options.days) || 7;
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);

  console.log(`\n📈 Habit Tracker Report (Last ${days} days)\n`);
  console.log('=' .repeat(60));
  console.log();

  let totalHabits = 0;
  let completedHabits = 0;

  habits.forEach(habit => {
    if (!habit.active) return;
    totalHabits++;

    const habitLogs = logs.filter(l =>
      l.habitId === habit.id && new Date(l.date) >= cutoff
    );

    const totalCompletions = habitLogs.reduce((sum, l) => sum + l.count, 0);
    const streak = calculateStreak(habit.id, logs);

    // Calculate weekly progress
    const weeklyData = {};
    for (let i = 0; i < days; i++) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split('T')[0];
      weeklyData[dateStr] = 0;
    }

    habitLogs.forEach(l => {
      if (weeklyData[l.date] !== undefined) {
        weeklyData[l.date] += l.count;
      }
    });

    // Build progress bar
    const progressBar = Object.entries(weeklyData)
      .sort(([a], [b]) => b.localeCompare(a))
      .map(([date, count]) => count > 0 ? '█' : '░')
      .join('');

    const completionRate = Math.round((totalCompletions / (days * habit.target)) * 100);
    if (completionRate >= 80) completedHabits++;

    console.log(`${habit.name}`);
    console.log(`  ${progressBar}`);
    console.log(`  Completions: ${totalCompletions} | Streak: ${streak.current} days | Rate: ${completionRate}%`);
    console.log();
  });

  console.log('=' .repeat(60));
  console.log(`\nSummary: ${completedHabits}/${totalHabits} habits on track (≥80% completion)`);
  console.log();
}

// Delete a habit
function deleteHabit(habitIdOrName) {
  const habits = loadHabits();
  const logs = loadLogs();

  let habitIndex = habits.findIndex(h => h.id === habitIdOrName);
  if (habitIndex === -1) {
    habitIndex = habits.findIndex(h => h.name.toLowerCase() === habitIdOrName.toLowerCase());
  }

  if (habitIndex === -1) {
    console.error(`Error: Habit "${habitIdOrName}" not found.`);
    process.exit(1);
  }

  const habit = habits[habitIndex];

  // Remove habit
  habits.splice(habitIndex, 1);
  saveHabits(habits);

  // Remove associated logs
  const filteredLogs = logs.filter(l => l.habitId !== habit.id);
  saveLogs(filteredLogs);

  console.log(`✓ Habit "${habit.name}" and its logs deleted successfully.`);
}

// Edit a habit
function editHabit(habitIdOrName, options = {}) {
  const habits = loadHabits();

  let habit = habits.find(h => h.id === habitIdOrName);
  if (!habit) {
    habit = habits.find(h => h.name.toLowerCase() === habitIdOrName.toLowerCase());
  }

  if (!habit) {
    console.error(`Error: Habit "${habitIdOrName}" not found.`);
    process.exit(1);
  }

  if (options.name) habit.name = options.name;
  if (options.description !== undefined) habit.description = options.description;
  if (options.frequency) habit.frequency = options.frequency;
  if (options.target) habit.target = parseInt(options.target);
  if (options.reminder !== undefined) habit.reminder = options.reminder;

  saveHabits(habits);
  console.log(`✓ Habit updated successfully!`);
}

// Check reminders
function checkReminders() {
  const habits = loadHabits();
  const now = new Date();
  const currentTime = now.toTimeString().slice(0, 5); // HH:MM

  const dueHabits = habits.filter(h => {
    if (!h.active || !h.reminder) return false;
    return h.reminder === currentTime;
  });

  if (dueHabits.length > 0) {
    console.log('\n⏰ Reminders:\n');
    dueHabits.forEach(habit => {
      console.log(`  📌 ${habit.name} - Time to complete!`);
    });
    console.log();
  }
}

// Show help
function showHelp() {
  console.log(`
Habit Tracker CLI - Track your habits and build consistency

Usage: habit <command> [options]

Commands:
  add <name>              Add a new habit
    --frequency <type>    Frequency: daily, weekly, monthly (default: daily)
    --target <n>          Target completions per period (default: 1)
    --reminder <time>     Reminder time in HH:MM format
    --description <text>  Habit description

  list                    List all habits

  log <habit>             Log a habit completion
    --count <n>           Number of completions (default: 1)
    --date <YYYY-MM-DD>   Date of completion (default: today)
    --note <text>         Optional note

  logs [habit]            View habit logs
    --days <n>            Show logs from last n days

  stats [habit]           Show statistics
    --days <n>            Calculate stats for last n days (default: 30)

  report                  Generate a progress report
    --days <n>            Report period in days (default: 7)

  edit <habit>            Edit a habit
    --name <new-name>     New name
    --frequency <type>    New frequency
    --target <n>          New target
    --reminder <time>     New reminder time

  delete <habit>          Delete a habit and its logs

  reminder                Check for due reminders

  help                    Show this help message

Examples:
  habit add "Exercise" --frequency daily --target 1 --reminder "08:00"
  habit log "Exercise" --count 1 --note "Morning run"
  habit stats "Exercise" --days 30
  habit report --days 7
`);
}

// Parse command line arguments
function parseArgs(args) {
  const command = args[0];
  const options = {};
  const positional = [];

  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      options[key] = value;
    } else {
      positional.push(args[i]);
    }
  }

  return { command, options, positional };
}

// Main entry point
function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    showHelp();
    process.exit(0);
  }

  const { command, options, positional } = parseArgs(args);

  switch (command) {
    case 'add':
      if (!positional[0]) {
        console.error('Error: Habit name is required.');
        process.exit(1);
      }
      addHabit(positional[0], options);
      break;

    case 'list':
      listHabits();
      break;

    case 'log':
      if (!positional[0]) {
        console.error('Error: Habit name or ID is required.');
        process.exit(1);
      }
      logHabit(positional[0], options);
      break;

    case 'logs':
      viewLogs(positional[0], options);
      break;

    case 'stats':
      calculateStats(positional[0], options);
      break;

    case 'report':
      generateReport(options);
      break;

    case 'edit':
      if (!positional[0]) {
        console.error('Error: Habit name or ID is required.');
        process.exit(1);
      }
      editHabit(positional[0], options);
      break;

    case 'delete':
      if (!positional[0]) {
        console.error('Error: Habit name or ID is required.');
        process.exit(1);
      }
      deleteHabit(positional[0]);
      break;

    case 'reminder':
      checkReminders();
      break;

    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;

    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }
}

main();
