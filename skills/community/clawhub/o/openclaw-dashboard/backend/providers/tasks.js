'use strict';
/**
 * Tasks Provider — read-only task and history views.
 */
const fs = require('fs');
const path = require('path');
const cfg = require('../lib/config');
const { jsonReply, errorReply } = require('../lib/http-helpers');

function readTasks() {
  try { return JSON.parse(fs.readFileSync(cfg.TASKS_FILE, 'utf8')); }
  catch { return []; }
}

// ── Task routes (read-only) ─────────────────────────────────────────
// Dashboard is read-only. Task writes (create/update/delete/spawn) go via Discord or CLI.
// Removed: POST /tasks, PATCH /tasks/:id, DELETE /tasks/:id,
//          POST /tasks/:id/notes, POST /tasks/:id/spawn
function register(router) {
  // List tasks
  router.add('GET', '/tasks', (req, res, q) => {
    let tasks = readTasks();
    if (q.status) tasks = tasks.filter(t => t.status === q.status);
    if (q.priority) tasks = tasks.filter(t => t.priority === q.priority);
    jsonReply(res, 200, tasks);
  });

  // Get task by id
  router.add('GET', '/tasks/:id', (req, res) => {
    const id = req.params?.id;
    const tasks = readTasks();
    const task = tasks.find(t => t.id === id);
    if (!task) return errorReply(res, 404, 'Task not found');
    return jsonReply(res, 200, task);
  });

  // Logs (task history + memory logs)
  router.add('GET', '/logs', (_req, res) => {
    try {
      const files = fs.readdirSync(cfg.MEMORY_DIR).filter(f => f.endsWith('.md')).sort().reverse();
      const logs = files.map(f => {
        const content = fs.readFileSync(path.join(cfg.MEMORY_DIR, f), 'utf8');
        const dateMatch = f.match(/^(\d{4}-\d{2}-\d{2})/);
        return { date: dateMatch ? dateMatch[1] : f.replace('.md', ''), filename: f, content };
      });
      jsonReply(res, 200, logs);
    } catch { jsonReply(res, 200, []); }
  });

  router.add('GET', '/logs/tasks', (_req, res) => {
    const tasks = readTasks();
    const history = tasks.filter(t => t.notes?.length).map(t => ({
      id: t.id, title: t.title, status: t.status, notes: t.notes,
    }));
    jsonReply(res, 200, history);
  });
}

module.exports = { register };
