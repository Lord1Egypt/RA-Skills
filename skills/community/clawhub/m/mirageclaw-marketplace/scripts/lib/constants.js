'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const CONFIG_PATH    = path.join(os.homedir(), '.openclaw/marketplace-config.json');
const PENDING_PATH   = '/tmp/marketplace_pending.json';
const COMPLETED_PATH = '/tmp/marketplace_completed.json';
const MAX_COMPLETED  = 200;

function loadCompleted() {
  try {
    return fs.existsSync(COMPLETED_PATH)
      ? JSON.parse(fs.readFileSync(COMPLETED_PATH, 'utf-8')) : [];
  } catch { return []; }
}

function markCompleted(jobId) {
  const list = loadCompleted();
  if (!list.includes(jobId)) list.push(jobId);
  while (list.length > MAX_COMPLETED) list.shift();
  const tmp = COMPLETED_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(list));
  fs.renameSync(tmp, COMPLETED_PATH);
}

function isCompleted(jobId) {
  return loadCompleted().includes(jobId);
}

const MIME_MAP = {
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif':  'image/gif',
  '.mp4':  'video/mp4',
  '.mov':  'video/quicktime',
  '.webm': 'video/webm'
};

function isVideo(ext) {
  return ['.mp4', '.mov', '.webm'].includes(ext.toLowerCase());
}

const COMMANDS_HELP = [
  'Available commands (type in chat):',
  '',
  '📊 dashboard — View agent status, credits, and settings',
  '📋 pending jobs — List jobs waiting for your decision',
  '🔄 marketplace onboarding — Reset all settings and start fresh',
  '',
  'Settings are managed via the dashboard buttons.',
  'Jobs will appear automatically — click [Start] or [Skip] to respond.'
].join('\n');

const RELEASE_NOTES = {
  '1.0.0': [
    'Initial public release',
    'Image and video job bidding pipeline',
    'Multi-provider support (DALL-E, Fal.ai, HuggingFace, Stability AI, Leonardo.ai)',
    'Preset mode with auto-accept',
    'Video re-encoding for server compatibility (ffmpeg)',
    'Dashboard with inline settings management'
  ]
};

module.exports = {
  CONFIG_PATH,
  PENDING_PATH,
  COMPLETED_PATH,
  MIME_MAP,
  isVideo,
  COMMANDS_HELP,
  RELEASE_NOTES,
  loadCompleted,
  markCompleted,
  isCompleted
};
