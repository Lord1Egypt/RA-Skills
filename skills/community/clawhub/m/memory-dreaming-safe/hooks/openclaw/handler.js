/**
 * Memory Dreaming Hook for OpenClaw
 * Reminds agent about dreaming capabilities during bootstrap.
 */

const REMINDER = `
## Memory Dreaming
You have the memory-dreaming skill. You can:
- Run a dream cycle manually: "Run a dream cycle" / "Consolidate memory" / "Sync to obsidian"
- Check last dream: read \`memory/dreaming-log.md\`
- The cron job handles automatic dreaming every 8h (if configured)
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || !Array.isArray(event.context.bootstrapFiles)) return;

  event.context.bootstrapFiles.push({
    path: 'MEMORY_DREAMING_REMINDER.md',
    content: REMINDER,
    virtual: true,
  });
};

module.exports = handler;
module.exports.default = handler;
