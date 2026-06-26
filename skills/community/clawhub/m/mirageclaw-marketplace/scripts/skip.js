#!/usr/bin/env node
'use strict';

const fs = require('fs');
const { PENDING_PATH, CONFIG_PATH } = require('./lib/constants');
const { notify } = require('./lib/notify');
const { del } = require('./lib/messaging');
require('./lib/env').loadEnv();
const jobId = process.argv[2];

if (!jobId) { console.error('Usage: skip.js <jobId>'); process.exit(1); }

try {
  const pending = fs.existsSync(PENDING_PATH)
    ? JSON.parse(fs.readFileSync(PENDING_PATH, 'utf-8')) : {};

  if (!pending[jobId]) {
    notify('MARKETPLACE_ERROR', { jobId, message: `❌ No pending job: ${jobId}` });
    process.exit(1);
  }

  // Delete the job offer message (the one with [Start]/[Skip] buttons)
  const offerMsgId = pending[jobId].offerMsgId;
  if (offerMsgId) {
    try {
      const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
      if (config.telegramChatId) del(config.telegramChatId, offerMsgId);
    } catch (_) {}
  }

  delete pending[jobId];
  const tmp = PENDING_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(pending, null, 2));
  fs.renameSync(tmp, PENDING_PATH);
  notify('MARKETPLACE_JOB_SKIPPED', { jobId, reason: 'user_declined', message: `⏭ Skipped Job #${jobId}` });

} catch (err) {
  notify('MARKETPLACE_ERROR', { jobId, message: `❌ ${err.message}` });
  process.exit(1);
}
