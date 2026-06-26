/**
 * LoomLens Live — OpenClaw Plugin Integration
 * Phase 3: Wire into OpenClaw's hook system
 * 
 * This plugin:
 * 1. Listens for `before_model_resolve` — intercepts model selection
 * 2. Listens for `before_prompt_build` — can modify prompt context
 * 3. Exposes a `/loomlens` command for manual estimation
 * 4. Provides HTTP route for the panel to query estimates
 * 
 * Install: copy this dir to ~/.openclaw/plugins/loomlens/
 */

import { registerPlugin, HookHandler } from 'openclaw/plugin-sdk';

// ─── Plugin Manifest ────────────────────────────────────────────────────────────

export const manifest = {
  id: 'loomlens-live',
  name: 'LoomLens Live',
  description: 'Pre-flight cost intelligence — see model costs before you spend',
  version: '1.0.0',
  author: 'Aster Vale / AEHS',
  events: [
    'before_model_resolve',   // intercept + override model selection
    'before_prompt_build',   // read prompt context before agent reply
  ],
  commands: ['/loomlens'],
  routes: [
    {
      method: 'GET',
      path: '/loomlens/estimate',
      description: 'Returns cost estimates for a prompt (for panel use)',
    },
  ],
};

// ─── Hook Handlers ────────────────────────────────────────────────────────────

/**
 * before_model_resolve
 * Fires just before the model is selected for a prompt.
 * Return a different modelId in event.model to override.
 */
const handleBeforeModelResolve: HookHandler = async (event) => {
  // event.context contains: sessionKey, messages, preferredModel, modelHint, cfg
  // If loomlens has a model override pending for this session, apply it here.
  const override = await getPendingModelOverride(event.context.sessionKey);
  if (override) {
    event.model = override;
  }
  return event;
};

/**
 * before_prompt_build
 * Fires after preprocessing, before the prompt is built for the model.
 * Use this to read the prompt content for loomlens estimation.
 */
const handleBeforePromptBuild: HookHandler = async (event) => {
  // event.context.bodyForAgent = the final enriched prompt body
  // We could emit this to connected LoomLens panels via SSE or broadcast.
  // For now, just store as pending for the estimation endpoint.
  const sessionKey = event.context.sessionKey;
  const body = event.context.bodyForAgent;
  if (sessionKey && body) {
    await setPendingPrompt(sessionKey, body);
  }
  return event;
};

// ─── Session State ─────────────────────────────────────────────────────────────
// In-memory store for pending prompts / model overrides (per session)
// In production, use Redis or the Signal Loom session store.

const pendingPrompts = new Map<string, string>();
const pendingOverrides = new Map<string, string>();

async function setPendingPrompt(sessionKey: string, prompt: string): Promise<void> {
  pendingPrompts.set(sessionKey, prompt);
  // Expire after 60s
  setTimeout(() => pendingPrompts.delete(sessionKey), 60_000);
}

async function getPendingPrompt(sessionKey: string): Promise<string | undefined> {
  return pendingPrompts.get(sessionKey);
}

async function setPendingModelOverride(sessionKey: string, modelId: string): Promise<void> {
  pendingOverrides.set(sessionKey, modelId);
}

async function getPendingModelOverride(sessionKey: string): Promise<string | undefined> {
  return pendingOverrides.get(sessionKey);
}

// ─── Plugin Registration ──────────────────────────────────────────────────────

export default registerPlugin(manifest.id, (api) => {
  api.registerHook('before_model_resolve', handleBeforeModelResolve);
  api.registerHook('before_prompt_build', handleBeforePromptBuild);

  api.registerCommand('/loomlens', async (event) => {
    // Manual trigger: estimate the last prompt in this session
    const sessionKey = event.sessionKey;
    const prompt = await getPendingPrompt(sessionKey) ?? '';
    if (!prompt) {
      event.messages.push('LoomLens: No pending prompt to estimate. Type a message first.');
      return event;
    }

    // Import the engine dynamically (avoid circular deps)
    const { estimatePrompt } = await import('../signal-loom-loomlens/loomlens-engine');
    const result = estimatePrompt(prompt);

    const lines = [
      `✦ LoomLens Live Estimate`,
      ``,
      `Task: ${result.taskType} (~${Math.round(result.taskConfidence * 100)}% confidence)`,
      `Tokens: ~${result.inputTokens} in / ~${result.outputTokens} out`,
      ``,
      `Top alternatives:`,
      ...result.estimates.slice(0, 4).map(
        (m, i) => `  ${i + 1}. ${m.modelName} — $${m.estimatedCost.toFixed(4)} [${m.fitBadge}]`
      ),
      ``,
      result.tip ? `💡 ${result.tip}` : '',
    ].filter(Boolean);

    event.messages.push(lines.join('\n'));
    return event;
  });

  api.registerRoute('GET', '/loomlens/estimate', async (req, res) => {
    // Query param: ?prompt=...
    const prompt = req.query?.prompt as string;
    if (!prompt) {
      res.status(400).json({ error: 'prompt query param required' });
      return;
    }

    const { estimatePrompt } = await import('../signal-loom-loomlens/loomlens-engine');
    const result = estimatePrompt(prompt);
    res.json(result);
  });

  // Expose setter so the panel can push model overrides
  api.registerRoute('POST', '/loomlens/override', async (req, res) => {
    const { sessionKey, modelId } = req.body ?? {};
    if (!sessionKey || !modelId) {
      res.status(400).json({ error: 'sessionKey and modelId required' });
      return;
    }
    await setPendingModelOverride(sessionKey, modelId);
    res.json({ ok: true, modelId });
  });

  console.log('[LoomLens Live] Plugin loaded — pre-flight cost intelligence active');
  return manifest;
});

// ─── Notes ────────────────────────────────────────────────────────────────────
//
// HOOK TIMING FLOW (from OpenClaw docs):
//
//   message:received
//     → message:preprocessed (body enriched with media/link data)
//     → before_prompt_build  ← we can read prompt here
//     → before_model_resolve ← we can override model here
//     → before_agent_reply
//     → [model inference]
//     → after_agent_reply
//     → message:sent
//
// PANEL ↔ PLUGIN COMMUNICATION (for pre-flight panel):
//
//   The React panel (loomlens-panel.tsx) needs to:
//   1. Get the current prompt text (from OpenClaw input state)
//   2. Call estimatePrompt() locally (no API needed — Phase 1 engine)
//   3. When user selects a model, call POST /loomlens/override
//      to set a pending override for the session
//   4. The before_model_resolve hook picks up the override
//      and applies it to event.model
//
//   For step 1 (reading the prompt), the panel has two options:
//   a. Read directly from DOM (textarea value) — simplest, works today
//   b. Use window.postMessage('openclaw_prompt', { text }) event from OpenClaw
//      (requires OpenClaw to emit this — not confirmed built-in yet)
//
//   The existing panel.html uses window.addEventListener('message', handler)
//   to receive openclaw_prompt events. This is the expected integration path.
//   If OpenClaw doesn't emit openclaw_prompt natively yet, we can add a small
//   workspace hook that emits it via postMessage to the parent window.
//
