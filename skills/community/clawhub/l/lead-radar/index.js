/**
 * Lead Radar — OpenClaw Skill Entry Point
 *
 * This file is loaded by the OpenClaw runtime.
 * The actual daily scan logic lives in cron.js.
 */

const { run } = require('./cron');

module.exports = {
  // OpenClaw calls this on the cron schedule defined in SKILL.md
  async execute(context) {
    try {
      await run(context);
    } catch (err) {
      console.error('Lead Radar execution failed:', err);

      // Try to notify the user via Telegram even on crash
      try {
        const { sendTelegram } = require('./lib/telegram');
        await sendTelegram(
          process.env.TELEGRAM_CHAT_ID,
          `\u26A0\uFE0F Lead Radar: Run failed — ${err.message}. Will retry next scheduled run.`
        );
      } catch (_) {
        // Swallow notification errors
      }
    }
  },
};
