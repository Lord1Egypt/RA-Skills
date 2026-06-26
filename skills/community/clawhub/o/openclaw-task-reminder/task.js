#!/usr/bin/env node

/**
 * Simple Task Reminder
 * Manage tasks with priorities
 */

const fs = require('fs');
const path = require('path');

const TASKS_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'tasks.json');

// Load tasks from file
function loadTasks() {
  try {
    if (fs.existsSync(TASKS_FILE)) {
      const data = fs.readFileSync(TASKS_FILE, 'utf8');
      return JSON.parse(data);
    }
    return [];
  } catch (error) {
    return [];
  }
}

// Save tasks to file
function saveTasks(tasks) {
  const dir = path.dirname(TASKS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(TASKS_FILE, JSON.stringify(tasks, null, 2));
}

// Get priority emoji
function getPriorityEmoji(priority) {
  switch (priority) {
    case 'high': return '🔴';
    case 'medium': return '🟡';
    case 'low': return '🟢';
    default: return '⚪';
  }
}

// Get priority order
function getPriorityOrder(priority) {
  switch (priority) {
    case 'high': return 1;
    case 'medium': return 2;
    case 'low': return 3;
    default: return 4;
  }
}

// Add a new task
function addTask(description, priority = 'medium') {
  const tasks = loadTasks();
  const newTask = {
    id: Date.now(),
    description,
    priority: priority.toLowerCase(),
    status: 'pending',
    createdAt: new Date().toISOString()
  };
  tasks.push(newTask);
  saveTasks(tasks);
  console.log(`✅ Task added: ${description} (${getPriorityEmoji(newTask.priority)} ${newTask.priority})`);
}

// List all tasks
function listTasks() {
  const tasks = loadTasks();
  if (tasks.length === 0) {
    console.log('📋 No tasks yet. Add one with "node task.js add <description>"');
    return;
  }

  // Sort by status (pending first), then priority
  const sorted = tasks.sort((a, b) => {
    if (a.status !== b.status) {
      return a.status === 'pending' ? -1 : 1;
    }
    return getPriorityOrder(a.priority) - getPriorityOrder(b.priority);
  });

  console.log('\n📋 Task List');
  console.log('─'.repeat(80));

  sorted.forEach(task => {
    const status = task.status === 'pending' ? '⬜' : '✅';
    const priority = getPriorityEmoji(task.priority);
    const desc = task.description.length > 50 ? task.description.substring(0, 50) + '...' : task.description;
    console.log(`${status} ${priority} ${desc}`);
  });

  console.log('─'.repeat(80));

  const pendingCount = tasks.filter(t => t.status === 'pending').length;
  console.log(`\n📊 ${pendingCount} pending task${pendingCount !== 1 ? 's' : ''}\n`);
}

// Mark task as done
function doneTask(taskId) {
  const tasks = loadTasks();
  const task = tasks.find(t => t.id === parseInt(taskId));

  if (!task) {
    console.log('❌ Task not found');
    return;
  }

  task.status = 'done';
  task.completedAt = new Date().toISOString();
  saveTasks(tasks);
  console.log(`✅ Task completed: ${task.description}`);
}

// Clear completed tasks
function clearTasks() {
  const tasks = loadTasks();
  const completedCount = tasks.filter(t => t.status === 'done').length;

  if (completedCount === 0) {
    console.log('📋 No completed tasks to clear');
    return;
  }

  const remaining = tasks.filter(t => t.status !== 'done');
  saveTasks(remaining);
  console.log(`🧹 Cleared ${completedCount} completed task${completedCount !== 1 ? 's' : ''}`);
}

// Show help
function showHelp() {
  console.log(`
📋 OpenClaw Task Reminder

Usage:
  node task.js add "<description>" [--priority high|medium|low]
  node task.js list
  node task.js done <task_id>
  node task.js clear

Examples:
  node task.js add "Review PR #123" --priority high
  node task.js add "Write documentation"
  node task.js list
  node task.js done 1234567890
  node task.js clear

Priorities:
  🔴 high   - Urgent tasks
  🟡 medium - Regular tasks
  🟢 low    - Nice-to-have tasks
`);
}

// Main function
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'add': {
      let description = args[1];
      let priority = 'medium';

      // Parse flags
      const priorityFlag = args.indexOf('--priority');
      if (priorityFlag !== -1 && args[priorityFlag + 1]) {
        priority = args[priorityFlag + 1];
      }

      if (!description) {
        console.log('❌ Please provide a task description');
        showHelp();
        process.exit(1);
      }

      addTask(description, priority);
      break;
    }

    case 'list':
    case 'ls':
      listTasks();
      break;

    case 'done': {
      const taskId = args[1];
      if (!taskId) {
        console.log('❌ Please provide a task ID');
        showHelp();
        process.exit(1);
      }
      doneTask(taskId);
      break;
    }

    case 'clear':
      clearTasks();
      break;

    default:
      showHelp();
      break;
  }
}

main();
