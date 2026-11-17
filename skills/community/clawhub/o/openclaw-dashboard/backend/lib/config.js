'use strict';
/**
 * Centralized configuration — reads environment variables once.
 * Every provider imports from here instead of reading process.env directly.
 */
const path = require('path');

const HOME = process.env.HOME || '';
const DOT_OPENCLAW = path.join(HOME, '.openclaw');

module.exports = {
  // Server
  PORT:   parseInt(process.env.DASHBOARD_PORT || '18791', 10),
  HOST:   process.env.DASHBOARD_HOST || '127.0.0.1',
  AUTH_TOKEN: process.env.OPENCLAW_AUTH_TOKEN || '',
  COOKIE_SECURE: process.env.DASHBOARD_COOKIE_SECURE === '1',
  CONTROL_UI_URL: process.env.OPENCLAW_CONTROL_UI_URL || 'http://127.0.0.1:18789/',

  // Paths
  HOME,
  DOT_OPENCLAW,
  WORKSPACE: process.env.OPENCLAW_WORKSPACE || path.join(DOT_OPENCLAW, 'workspace'),

  // Sessions
  SESSIONS_FILE: process.env.OPENCLAW_SESSIONS_FILE
    || path.join(DOT_OPENCLAW, 'agents', 'main', 'sessions', 'sessions.json'),
  SESSIONS_DIR: path.join(DOT_OPENCLAW, 'agents', 'main', 'sessions'),
  SUBAGENT_RUNS_FILE: process.env.OPENCLAW_SUBAGENT_RUNS
    || path.join(DOT_OPENCLAW, 'subagents', 'runs.json'),

  // Cron
  CRON_STORE_PATH: path.join(DOT_OPENCLAW, 'cron', 'jobs.json'),
  CRON_RUNS_DIR:   path.join(DOT_OPENCLAW, 'cron', 'runs'),

  // Watchdog
  WATCHDOG_DIR: process.env.OPENCLAW_WATCHDOG_DIR
    || path.join(DOT_OPENCLAW, 'watchdogs', 'gateway-discord'),

  // Spark
  SPARK_METRICS_GT_FILE: process.env.OPENCLAW_SPARK_METRICS_GT
    || path.join(DOT_OPENCLAW, 'spark-metrics', 'ground-truth.json'),
  SPARK_WATCHDOG_STATE: path.join(DOT_OPENCLAW, 'spark-watchdog-state.json'),

  // Ledger
  LEDGER_DB: process.env.OPENCLAW_LEDGER_DB
    || path.join(DOT_OPENCLAW, 'ledger.db'),

  // OpenClaw config
  OPENCLAW_CONFIG_FILE: process.env.OPENCLAW_CONFIG_FILE
    || path.join(DOT_OPENCLAW, 'openclaw.json'),
  OPENCLAW_CONFIG_BASELINE: process.env.OPENCLAW_CONFIG_BASELINE_FILE
    || path.join(DOT_OPENCLAW, 'openclaw.json.good'),

  // Ground Truth
  GROUND_TRUTH_FILE: path.join(
    process.env.OPENCLAW_WORKSPACE || path.join(DOT_OPENCLAW, 'workspace'),
    'MODEL_GROUND_TRUTH.md'
  ),

  // Feature flags
  ENABLE_CONFIG_ENDPOINT:  process.env.OPENCLAW_ENABLE_CONFIG_ENDPOINT === '1',
  ENABLE_COPILOT:          process.env.OPENCLAW_ENABLE_COPILOT === '1',
  CORS_ALLOWED_ORIGINS:    (process.env.DASHBOARD_CORS_ORIGINS || '').split(',').filter(Boolean),

  // Local API Hub
  LOCAL_API_HUB_PORT: parseInt(process.env.LOCAL_API_HUB_PORT || '3456', 10),
  LOCAL_API_HUB_HOST: process.env.LOCAL_API_HUB_HOST || '127.0.0.1',
  get LOCAL_API_HUB_URL() {
    return `http://${this.LOCAL_API_HUB_HOST}:${this.LOCAL_API_HUB_PORT}`;
  },

  // Meeting Copilot (opt-in)
  COPILOT_API_KEY: process.env.ALIBABA_CLOUD_API_KEY || '',
  COPILOT_MODEL: process.env.OPENCLAW_COPILOT_MODEL || 'qwen3-omni-flash-2025-12-01',
  COPILOT_REDIS_URL: process.env.OPENCLAW_COPILOT_REDIS_URL || 'redis://127.0.0.1:6379',

  // Limits
  MAX_BODY:   1 * 1024 * 1024,
  MAX_UPLOAD: 20 * 1024 * 1024,
  MAX_UNTRUSTED_PROMPT_FIELD: 800,
  MAX_CRON_MESSAGE_LENGTH: 3000,

  // Tasks — stored outside skill dir to avoid Git tracking user data
  TASKS_FILE: process.env.OPENCLAW_DASHBOARD_TASKS
    || path.join(DOT_OPENCLAW, 'dashboard', 'tasks.json'),
  ATTACHMENTS_DIR: process.env.OPENCLAW_DASHBOARD_ATTACHMENTS
    || path.join(DOT_OPENCLAW, 'dashboard', 'attachments'),
  SKILLS_DIR: path.join(
    process.env.OPENCLAW_WORKSPACE || path.join(DOT_OPENCLAW, 'workspace'),
    'skills'
  ),
  MEMORY_DIR: path.join(
    process.env.OPENCLAW_WORKSPACE || path.join(DOT_OPENCLAW, 'workspace'),
    'memory'
  ),

};
