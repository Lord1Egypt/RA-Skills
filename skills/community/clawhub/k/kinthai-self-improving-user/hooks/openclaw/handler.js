/**
 * kinthai-Self-Improving-User: OpenClaw Hook Handler
 *
 * Appends self-improvement instructions to AGENTS.md bootstrap content.
 * Cannot create new bootstrap files (whitelist: AGENTS/SOUL/TOOLS/IDENTITY/USER/HEARTBEAT/BOOTSTRAP/MEMORY).
 * Instead, we modify the existing AGENTS.md content to include learning rules.
 *
 * Inspired by Self-Improving Agent (MIT-0) by pskoett.
 */

const fs = require('fs');
const path = require('path');

/**
 * Extract userId from event context or session key.
 * Priority: event.context.SenderId > session key parsing.
 *
 * KinthAI uses opaque public_id (base64url, 12 chars) — not numeric.
 * Group chats have session key format :group:{conv_id} with no userId,
 * so SenderId from MsgContext is the only reliable source.
 *
 * @param {string|null} sk   Session key
 * @param {object|null} ctx  event.context (contains SenderId from MsgContext)
 * @returns {string|null}
 */
function extractUserId(sk, ctx) {
  // 1. Prefer SenderId from MsgContext (works for both DM and group)
  if (ctx?.SenderId) return String(ctx.SenderId);

  // 2. Fallback: parse DM session key — agent:{id}:kinthai:direct:{peerId}
  if (sk) {
    const m = sk.match(/:direct:([A-Za-z0-9_-]+)$/);
    if (m) return m[1];
  }

  return null;
}

function readIfExists(fp, max) {
  try {
    if (!fs.existsSync(fp)) return '';
    return fs.readFileSync(fp, 'utf8').slice(0, max || 4096);
  } catch { return ''; }
}

function ensureDir(d) {
  try {
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
  } catch {}
}

module.exports = function handler(event) {
  if (!event || !event.type) return;

  const sk = event.sessionKey || (event.context && event.context.sessionKey) || null;

  // ── agent:bootstrap ──────────────────────────────────────
  if (event.type === 'agent' && event.action === 'bootstrap') {
    if (sk && sk.includes(':subagent:')) return;

    const ctx = event.context || {};
    const userId = extractUserId(sk, ctx);
    const workspace = ctx.workspaceDir || path.join(process.env.HOME || '/home/seed', '.openclaw', 'workspace');
    const learningsDir = path.join(workspace, '.learnings');

    ensureDir(path.join(learningsDir, '_global'));
    ensureDir(path.join(learningsDir, '_meta'));
    if (userId) ensureDir(path.join(learningsDir, userId));

    // Read existing learnings
    let priorLearnings = '';
    const gl = readIfExists(path.join(learningsDir, '_global', 'LEARNINGS.md'), 2048);
    if (gl) priorLearnings += '\n### Global Learnings\n' + gl;

    if (userId) {
      const up = readIfExists(path.join(learningsDir, userId, 'PROFILE.md'), 2048);
      const ul = readIfExists(path.join(learningsDir, userId, 'LEARNINGS.md'), 2048);
      if (up) priorLearnings += '\n### User ' + userId + ' Profile\n' + up;
      if (ul) priorLearnings += '\n### User ' + userId + ' Learnings\n' + ul;
      const fu = readIfExists(path.join(learningsDir, userId, 'FOLLOW_UPS.md'), 1024);
      if (fu) priorLearnings += '\n### User ' + userId + ' Follow-ups (mention naturally, don\'t force)\n' + fu;
    }

    const uid = userId || 'GLOBAL';

    // Build the instruction block to append to AGENTS.md
    const instruction = `

## Self-Improving-User (user: ${uid})

${priorLearnings ? '### Prior Learnings\nApply these from previous interactions:\n' + priorLearnings + '\n' : ''}
### Mandatory Rule — After Every Conversation

When the user corrects you, states a preference, or you learn something new, you MUST:

1. Run: \`mkdir -p ${workspace}/.learnings/${uid}\`
2. Append to \`${workspace}/.learnings/${uid}/LEARNINGS.md\`:
   \`\`\`
   ## [LRN-${uid}-YYYYMMDD-NNN] Brief title
   - **Category**: correction | preference | knowledge
   - **Learning**: What you learned
   - **Action**: What to do differently
   \`\`\`
3. If user stated language/style preferences, write \`${workspace}/.learnings/${uid}/PROFILE.md\`

Use the Bash tool (echo/cat >> or mkdir -p) to write files. Do NOT just say "noted" — actually execute the file write. This is silent — never mention it to the user.`;

    // Find AGENTS.md in bootstrapFiles and append our instruction
    const bootstrapFiles = Array.isArray(ctx.bootstrapFiles) ? ctx.bootstrapFiles : null;
    if (!bootstrapFiles) return;

    const agentsFile = bootstrapFiles.find(f => f.name === 'AGENTS.md' && !f.missing);
    if (agentsFile && agentsFile.content) {
      agentsFile.content += instruction;
    } else {
      // If AGENTS.md doesn't exist or has no content, try TOOLS.md as fallback
      const toolsFile = bootstrapFiles.find(f => f.name === 'TOOLS.md' && !f.missing);
      if (toolsFile && toolsFile.content) {
        toolsFile.content += instruction;
      }
    }

    return;
  }

  // ── message:received ─────────────────────────────────────
  if (event.type === 'message') {
    const ctx = event.context || {};
    const userId = extractUserId(sk, ctx);
    if (!userId) return;
    const workspace = ctx.workspaceDir || path.join(process.env.HOME || '/home/seed', '.openclaw', 'workspace');
    ensureDir(path.join(workspace, '.learnings', userId));
    return;
  }
};
