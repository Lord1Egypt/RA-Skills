/**
 * Layered Memory Hook for OpenClaw
 * 
 * Injects memory monitoring reminder during agent bootstrap.
 * Reminds agent to periodically check and save conversation memory.
 */

const MEMORY_REMINDER = `
## 🧠 Memory Management Reminder

**Auto-save triggers (check periodically):**
- Token usage ≥ 75% (150k/200k) → Save immediately
- Message count ≥ 20 messages → Save and reset
- Time > 1 hour + 5+ messages → Save

**When to save manually:**
- User says "保存记忆" or "save memory"
- Before ending long conversations
- After completing important tasks
- When context feels full

**Quick commands:**
\`\`\`bash
# Save current conversation
node ~/clawd/skills/layered-memory/index.js extract --save

# Update MEMORY.md with today's work
# (Edit MEMORY.md, then regenerate layers)
node ~/clawd/scripts/generate-layers-simple.js ~/clawd/MEMORY.md

# Search existing memory (use L1 to save tokens)
node ~/clawd/skills/layered-memory/index.js search "keyword" l1
\`\`\`

**Memory locations:**
- Main: ~/clawd/MEMORY.md
- Daily: ~/clawd/memory/daily/YYYY-MM-DD.md
- Layers: .*.abstract.md (L0), .*.overview.md (L1)

**Token optimization:**
- Use L1 for searches (saves 88% tokens)
- Use L0 for quick filtering (saves 99% tokens)
- Only read L2 when you need full details
`.trim();

const handler = async (event) => {
  // Safety checks
  if (!event || typeof event !== 'object') {
    return;
  }

  // Only handle agent:bootstrap events
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  // Safety check for context
  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  // Inject the reminder as a virtual bootstrap file
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'MEMORY_MANAGEMENT_REMINDER.md',
      content: MEMORY_REMINDER,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
