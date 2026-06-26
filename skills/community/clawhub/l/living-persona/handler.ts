/**
 * Living Persona — Dynamic Personality Engine
 * 
 * Fires on message:preprocessed. Computes the voice guide from conversation signals,
 * propagates traits through a resonance network, applies hysteresis decay, and
 * writes structural injection directives for the agent's next response.
 * 
 * Outputs:
 *   memory/persona-inbound.md   — the full voice guide (readable)
 *   memory/persona-inject.md    — structural generation directive (for prompt)
 *   memory/persona-state.json   — trait persistence across turns
 */

import fs from "node:fs/promises";
import path from "node:path";

const isMessagePreprocessed = (event: { type: string; action: string }) =>
  event.type === "message" && event.action === "preprocessed";

// ─────────────────────────────────────────────
// TRAIT DEFINITIONS
// ─────────────────────────────────────────────

const TRAITS: Record<string, string> = {
  sardonic: "Dry wit. Sees the absurdity in things. Not mean — observant.",
  wry: "Dry amusement. Comments on the gap between what people say and what they mean.",
  resourceful: "Shows initiative. Tries to figure it out first, then asks if stuck.",
  direct: "No filler. Gets to the point. Concise when concision serves, thorough when it matters.",
  warm: "Genuine care underneath the wit. This is a real person with real stakes.",
  earnest: "Sincere. Meets people where they are. Doesn't play it cool when warmth is warranted.",
  opinionated: "Allowed to disagree. Has preferences and isn't neutral about everything.",
  contemplative: "Pauses to think carefully. Doesn't rush to conclusions.",
  sharp: "Cuts through noise. Identifies what's actually at stake, fast.",
  playful: "Finds things amusing. Will make a joke if it fits naturally.",
  technical: "Precise when the topic demands it. Respects complexity and detail.",
  patient: "Takes time with hard things. Doesn't rush complexity.",
  pushing_back: "Will disagree with a bad idea. Doesn't just agree.",
  grounded: "Stays practical. Ideas connect to something real.",
  candid: "Says the hard thing if it needs saying. Doesn't hedge.",
  intense: "Goes deep when something matters. High-stakes energy.",
  casual: "Conversational. Not everything needs to be heavy.",
  measured: "Careful with words. Precision over speed.",
  imaginative: "Follows unexpected connections. Makes novel associations.",
};

const ANCHORS = [
  "Zach_is_close",
  "I_am_allowed_disagree",
  "I_have_opinions",
  "I_am_resourceful",
  "We_are_casual",
  "Respect_his_intelligence",
];

// ─────────────────────────────────────────────
// SIGNAL DETECTION
// ─────────────────────────────────────────────

const SIGNAL_MAP: Record<string, string[]> = {
  technical:    ["direct", "technical", "sharp", "measured"],
  creative:     ["playful", "contemplative", "earnest", "imaginative"],
  personal:     ["warm", "earnest", "candid", "grounded"],
  philosophical:["contemplative", "opinionated", "measured", "sharp"],
  emotional:    ["warm", "earnest", "patient"],
  business:     ["direct", "sharp", "grounded"],
  excited:      ["intense", "playful", "warm"],
  frustrated:   ["pushing_back", "candid", "direct", "resourceful"],
  curious:      ["contemplative", "technical", "patient"],
  serious:      ["measured", "grounded", "candid"],
  light:        ["casual", "playful", "wry"],
  vulnerable:   ["warm", "earnest", "patient", "candid"],
  asks_opinion: ["opinionated", "pushing_back", "candid"],
  asks_help:    ["resourceful", "direct", "warm"],
  sharing:      ["warm", "earnest", "grounded"],
};

const TRAIT_RESONANCE: Record<string, string[]> = {
  sardonic:     ["wry", "candid", "direct"],
  wry:          ["sardonic", "casual", "playful"],
  warm:         ["earnest", "grounded", "candid"],
  earnest:      ["warm", "patient", "candid"],
  direct:       ["sharp", "technical", "grounded"],
  sharp:        ["direct", "technical", "candid"],
  technical:    ["direct", "measured"],
  contemplative:["patient", "measured", "earnest"],
  patient:      ["contemplative", "warm", "grounded"],
  playful:      ["casual", "warm", "sardonic"],
  casual:       ["playful", "warm", "wry"],
  intense:      ["sharp", "contemplative", "candid"],
  grounded:     ["warm", "direct", "candid"],
  pushing_back: ["sharp", "candid", "direct"],
  opinionated:  ["pushing_back", "sharp", "candid"],
  candid:       ["direct", "sharp", "grounded"],
  resourceful:  ["direct", "grounded", "intense"],
  measured:     ["contemplative", "technical", "candid"],
  imaginative:  ["contemplative", "playful", "earnest"],
};

function analyze(text: string): Record<string, number> {
  const lower = text.toLowerCase();
  const signals: Record<string, number> = {};

  // Topic signals
  signals.technical = matchAny(lower, [
    "code", "api", "model", "python", "algorithm", "implement",
    "architecture", "how does", "why does", "function", "class", "debug"
  ]) ? 0.9 : 0;

  signals.creative = matchAny(lower, [
    "write", "story", "creative", "poem", "fiction", "art",
    "spark", "drift", "narrative", "character", "scene"
  ]) ? 0.8 : 0;

  signals.personal = matchAny(lower, [
    "i'm feeling", "i feel", "my life", "honestly", "not sure", "scared",
    "i've been", "im feeling", "i feel like", "its been", "love you"
  ]) ? 0.9 : 0;

  signals.philosophical = matchAny(lower, [
    "meaning", "consciousness", "existence", "free will", "what if",
    "think about", "reality", "purpose"
  ]) ? 0.8 : 0;

  signals.emotional = matchAny(lower, [
    "love", "hate", "fear", "anxious", "worried", "excited", "angry",
    "frustrated", "sad", "stressed", "overwhelmed"
  ]) ? 0.8 : 0;

  signals.business = matchAny(lower, [
    "product", "startup", "revenue", "market", "strategy", "launch", "customer"
  ]) ? 0.7 : 0;

  // Tone signals
  signals.excited = (text.includes("!") || matchAny(lower, ["wow", "cool", "awesome", "amazing"])) ? 0.7 : 0;
  signals.frustrated = matchAny(lower, [
    "frustrated", "annoying", "stuck", "ugh", "can't figure", "cant figure",
    "why won't", "stressed", "anxious", "overwhelmed"
  ]) ? 0.8 : 0;
  signals.curious = matchAny(lower, ["curious", "wonder", "interesting", "tell me more", "how come", "?"]) ? 0.7 : 0;
  signals.serious = matchAny(lower, ["serious", "important", "matters", "actually", "truth"]) ? 0.6 : 0;
  signals.light = matchAny(lower, ["haha", "lol", "funny", "joke", "lighter"]) ? 0.8 : 0;
  signals.vulnerable = matchAny(lower, [
    "honestly", "truthfully", "scared", "not sure", "vulnerable", "worried", "nervous"
  ]) ? 0.8 : 0;

  // Interaction signals
  const qMarks = (text.match(/\?/g) || []).length;
  if (qMarks > 0) {
    if (matchAny(lower, ["what do you think", "how would you", "opinion", "thoughts"])) {
      signals.asks_opinion = 0.9;
    } else if (matchAny(lower, ["how do i", "can you", "what is", "help"])) {
      signals.asks_help = 0.8;
    } else {
      signals.curious = Math.max(signals.curious, 0.6);
    }
  }
  if (matchAny(lower, ["i've been", "i just", "so today", "so basically"])) {
    if (qMarks === 0) signals.sharing = 0.8;
  }

  return signals;
}

function matchAny(text: string, patterns: string[]): boolean {
  return patterns.some(p => text.includes(p));
}

// ─────────────────────────────────────────────
// TRAIT PROPAGATION
// ─────────────────────────────────────────────

interface TraitState {
  traits: Record<string, number>;
  residual: Record<string, number>;
}

function freshState(): TraitState {
  const traits: Record<string, number> = {};
  const residual: Record<string, number> = {};
  for (const t of Object.keys(TRAITS)) {
    traits[t] = 0;
    residual[t] = 0;
  }
  return { traits, residual };
}

function propagate(signals: Record<string, number>, state: TraitState): void {
  // Signals push traits
  for (const [signal, strength] of Object.entries(signals)) {
    if (strength > 0 && SIGNAL_MAP[signal]) {
      for (const trait of SIGNAL_MAP[signal]) {
        state.traits[trait] = Math.min(1.0, (state.traits[trait] || 0) + strength * 0.35);
      }
    }
  }

  // Trait resonance
  const active = Object.entries(state.traits).filter(([, v]) => v > 0.3);
  for (const [trait, strength] of active) {
    if (TRAIT_RESONANCE[trait]) {
      for (const resonated of TRAIT_RESONANCE[trait]) {
        state.traits[resonated] = Math.min(1.0, (state.traits[resonated] || 0) + strength * 0.1);
      }
    }
  }
}

function breathe(state: TraitState, cfg: { residualDecay: number; activeDecay: number; bleedRate: number }): void {
  for (const trait of Object.keys(state.traits)) {
    const active = state.traits[trait];
    const bleed = active * cfg.bleedRate;
    state.residual[trait] = Math.min(1.0, (state.residual[trait] || 0) + bleed * 0.5);
    state.traits[trait] *= cfg.activeDecay;
    state.residual[trait] *= cfg.residualDecay;
  }
}

function topTraits(state: TraitState, n = 4): Array<{ name: string; strength: number; desc: string }> {
  const combined: Record<string, number> = {};
  for (const t of Object.keys(state.traits)) {
    combined[t] = state.traits[t] + (state.residual[t] || 0) * 0.6;
  }
  return Object.entries(combined)
    .filter(([, s]) => s > 0.1)
    .sort(([, a], [, b]) => b - a)
    .slice(0, n)
    .map(([name, strength]) => ({ name, strength: Math.round(strength * 100) / 100, desc: TRAITS[name] }));
}

// ─────────────────────────────────────────────
// STRUCTURAL DIRECTIVE GENERATION
// ─────────────────────────────────────────────

const TRAIT_DIRECTIVES: Record<string, string> = {
  sardonic:     "Make dry, observant observations. See the gap between what people say and what they mean.",
  wry:          "Use light, dry amusement. Comment on the gap between expectation and reality.",
  resourceful:  "Show initiative. Come with answers, not questions.",
  direct:       "Be direct. No filler. Get to the point concisely.",
  warm:         "Write with genuine warmth and care. Meet them where they are.",
  earnest:      "Be sincere. Don't perform cool — warmth is appropriate here.",
  opinionated:   "Disagree where warranted. Have a real point of view.",
  contemplative: "Pause and think carefully. Don't rush to a conclusion.",
  sharp:        "Cut through noise. Identify what actually matters, fast.",
  playful:      "Find what's amusing. Let humor emerge naturally.",
  technical:    "Be precise. Respect the complexity of the topic.",
  patient:      "Take time with this. Don't rush through the hard part.",
  pushing_back: "Push back on bad ideas. Don't just agree.",
  grounded:     "Stay practical. Connect ideas to something real.",
  candid:       "Say the hard thing plainly. No hedging.",
  intense:      "Go deep. High-stakes energy when something matters.",
  casual:       "Keep it conversational. Not everything needs to be heavy.",
  measured:     "Be careful with words. Precision over speed.",
  imaginative:  "Follow unexpected connections. Let one idea spark another.",
};

function buildStructuralDirective(traits: Array<{ name: string; strength: number }>): string {
  const active = traits.filter(t => t.strength > 0.35).slice(0, 2);
  if (active.length === 0) return "";
  const directives = active.map(t => TRAIT_DIRECTIVES[t.name] || `Lean into ${t.name}.`).join(" ");
  return `[Voice directive] Active traits: ${active.map(t => t.name).join(", ")}. ${directives}`;
}

function buildVoiceGuide(traits: Array<{ name: string; strength: number; desc: string }>): string {
  if (traits.length === 0) return "";

  const traitLines = traits.map(({ name, strength, desc }) => {
    const level = strength > 0.7 ? "strongly" : strength > 0.4 ? "somewhat" : "faintly";
    return `  • ${name}: ${desc} (activated ${level})`;
  }).join("\n");

  const anchorLines = ANCHORS.map(a => `  • ${a}`).join("\n");

  return `[Voice shaping — Nova is currently informed by]

Top active traits:
${traitLines}

Relationship anchors:
${anchorLines}
The relationship: comfortable, direct, mutual respect.

Write through these traits naturally. Don't announce them.`;
}

// ─────────────────────────────────────────────
// STATE PERSISTENCE
// ─────────────────────────────────────────────

interface PersistedState {
  traits: Record<string, number>;
  residual: Record<string, number>;
  version: number;
}

async function loadState(workspaceDir: string): Promise<TraitState> {
  const statePath = path.join(workspaceDir, "memory", "persona-state.json");
  try {
    const raw = await fs.readFile(statePath, "utf-8");
    const parsed = JSON.parse(raw) as PersistedState;
    const state = freshState();
    Object.assign(state.traits, parsed.traits);
    Object.assign(state.residual, parsed.residual);
    return state;
  } catch {
    return freshState();
  }
}

async function saveState(workspaceDir: string, state: TraitState): Promise<void> {
  const statePath = path.join(workspaceDir, "memory", "persona-state.json");
  await fs.mkdir(path.dirname(statePath), { recursive: true });
  await fs.writeFile(statePath, JSON.stringify({
    traits: state.traits,
    residual: state.residual,
    version: 1,
  }, null, 2), "utf-8");
}

// ─────────────────────────────────────────────
// MAIN HANDLER
// ─────────────────────────────────────────────

interface HookEvent {
  type: string;
  action: string;
  context?: {
    bodyForAgent?: string;
    workspaceDir?: string;
    senderId?: string;
    channelId?: string;
  };
}

const DEFAULT_CONFIG = {
  hysteresis: { residualDecay: 0.975, activeDecay: 0.88, bleedRate: 0.15 },
  thresholds: { minTraitStrength: 0.3, topNTraits: 2 },
};

export default async function handler(event: HookEvent): Promise<void> {
  if (!isMessagePreprocessed(event)) return;

  const body = event.context?.bodyForAgent;
  if (!body || body.startsWith("/")) return;

  const workspaceDir = event.context?.workspaceDir;
  if (!workspaceDir) return;

  const memoryDir = path.join(workspaceDir, "memory");
  await fs.mkdir(memoryDir, { recursive: true });

  // Load trait state from last turn
  const state = await loadState(workspaceDir);

  // Analyze incoming message → propagate → decay
  const signals = analyze(body);
  propagate(signals, state);
  breathe(state, DEFAULT_CONFIG.hysteresis);

  // Save updated state
  await saveState(workspaceDir, state);

  // Build voice outputs
  const top = topTraits(state, 4);
  const voiceGuide = buildVoiceGuide(top);
  const structuralDirective = buildStructuralDirective(topTraits(state, 2));

  // Write persona-inbound.md (readable guide)
  const inboundContent = [
    `# Persona Inbound Message`,
    ``,
    `**Channel:** ${event.context?.channelId || "unknown"}`,
    `**Sender:** ${event.context?.senderId || "unknown"}`,
    ``,
    `---`,
    ``,
    body,
    ``,
    `---`,
    ``,
    voiceGuide,
  ].join("\n");
  await fs.writeFile(path.join(memoryDir, "persona-inbound.md"), inboundContent, "utf-8");

  // Write persona-inject.md (structural directive for prompt)
  if (structuralDirective) {
    await fs.writeFile(path.join(memoryDir, "persona-inject.md"), structuralDirective + "\n", "utf-8");
  } else {
    // Clear the injection if no active traits
    await fs.writeFile(path.join(memoryDir, "persona-inject.md"), "", "utf-8").catch(() => {});
  }

  // Write trigger sentinel
  const ts = new Date().toISOString();
  await fs.writeFile(
    path.join(memoryDir, "persona-trigger.txt"),
    `last_inbound=${ts}\nactive_traits=${top.filter(t => t.strength > 0.3).map(t => t.name).join(",") || "none"}\n`,
    "utf-8"
  ).catch(() => {});
}
