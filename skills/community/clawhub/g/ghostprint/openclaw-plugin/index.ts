/**
 * Ghostprint — OpenClaw Plugin v3.0
 *
 * Anti-fingerprinting LLM noise injector.
 * Designed to be statistically indistinguishable from real human usage.
 *
 * v3 fixes (from GLM-5.1 critique):
 *  [CRITICAL] Follow-ups are now topic-paired, not generic disconnected phrases
 *  [CRITICAL] Log stores only metadata — never topic text or reply content
 *  [CRITICAL] LogNormal params perturbed per-session (not fixed mu/sigma)
 *  [CRITICAL] Soft truncation replaces hard clamp on exponential timing
 *  [HIGH]     Persona system: stable biased domain weights per run cycle
 *  [HIGH]     Multi-turn rate varies by persona (0.1–0.6)
 *  [HIGH]     Post-response reading delay before next turn (log-normal ~5–30s)
 *  [HIGH]     Day-of-week + hour weighting for realistic activity pattern
 *  [MEDIUM]   System prompt pool expanded to 20+, rate varies per persona
 *  [MEDIUM]   Dual-provider rounds staggered with longer delay
 */

import * as https from "https";
import * as fs from "fs";
import * as path from "path";
import * as crypto from "crypto";
import { URL } from "url";
import * as net from "net";

// ── Cryptographic randomness ─────────────────────────────────────────────────

function randInt(min: number, max: number): number {
  return crypto.randomInt(min, max + 1);
}

function randFloat(): number {
  return crypto.randomBytes(4).readUInt32BE(0) / 0x100000000;
}

function randChoice<T>(arr: T[]): T {
  return arr[crypto.randomInt(0, arr.length)];
}

function randSample<T>(arr: T[], k: number): T[] {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = crypto.randomInt(0, i + 1);
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, Math.min(k, copy.length));
}

// Box-Muller log-normal with variable params (FIX: params perturbed per call)
function logNormal(mu: number, sigma: number): number {
  const u1 = Math.max(randFloat(), 1e-10);
  const u2 = randFloat();
  const z  = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return Math.exp(mu + sigma * z);
}

// Soft exponential: rejection-sample instead of hard clamp (FIX: preserves Poisson property)
function softExponential(meanMs: number, softCapMs: number): number {
  // Rejection sample: redraw if > softCap, but only up to 5 times to avoid infinite loop
  for (let i = 0; i < 5; i++) {
    const v = -meanMs * Math.log(Math.max(randFloat(), 1e-10));
    if (v <= softCapMs) return v;
  }
  // After 5 misses, return uniform in the range (rare edge case)
  return meanMs * 0.5 + randFloat() * meanMs;
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ── Persona system ────────────────────────────────────────────────────────────
// A "persona" is a stable bias vector chosen once per scheduler cycle.
// It gives each noise burst a coherent identity: domain preferences,
// conversation style, and verbosity — like a real user.

interface Persona {
  name: string;
  domainWeights: Record<string, number>; // domain → relative frequency
  multiTurnRate: number;                  // 0.0–1.0
  systemPromptRate: number;               // 0.0–1.0
  tokenMu: number;                        // log-normal mu for token budget
  tokenSigma: number;                     // log-normal sigma
}

const PERSONAS: Persona[] = [
  {
    name: "curious-student",
    domainWeights: { science: 3, psychology: 2, history: 2, health: 1, lifestyle: 1 },
    multiTurnRate: 0.45,
    systemPromptRate: 0.15,
    tokenMu: 4.2, tokenSigma: 0.7,
  },
  {
    name: "home-cook",
    domainWeights: { cooking: 4, health: 2, lifestyle: 2, diy: 1 },
    multiTurnRate: 0.20,
    systemPromptRate: 0.05,
    tokenMu: 3.8, tokenSigma: 0.6,
  },
  {
    name: "working-professional",
    domainWeights: { tech: 3, finance: 3, language: 2, travel: 1, psychology: 1 },
    multiTurnRate: 0.30,
    systemPromptRate: 0.50,
    tokenMu: 4.0, tokenSigma: 0.9,
  },
  {
    name: "diy-enthusiast",
    domainWeights: { diy: 4, tech: 2, science: 1, lifestyle: 1 },
    multiTurnRate: 0.35,
    systemPromptRate: 0.10,
    tokenMu: 3.9, tokenSigma: 0.8,
  },
  {
    name: "health-conscious",
    domainWeights: { health: 4, lifestyle: 3, cooking: 2, psychology: 1 },
    multiTurnRate: 0.40,
    systemPromptRate: 0.20,
    tokenMu: 4.1, tokenSigma: 0.7,
  },
  {
    name: "night-owl-researcher",
    domainWeights: { history: 3, science: 3, psychology: 2, language: 1 },
    multiTurnRate: 0.55,
    systemPromptRate: 0.25,
    tokenMu: 4.4, tokenSigma: 1.0,
  },
];

// Rotate persona every N rounds (stable per cycle, not per request)
let currentPersona: Persona = randChoice(PERSONAS);
let personaRoundsRemaining = randInt(3, 8);

function getPersona(): Persona {
  if (personaRoundsRemaining <= 0) {
    // Pick a different persona from current
    const others = PERSONAS.filter(p => p.name !== currentPersona.name);
    currentPersona = randChoice(others);
    personaRoundsRemaining = randInt(3, 8);
  }
  personaRoundsRemaining--;
  return currentPersona;
}

// ── Topic pool: domain-tagged, with paired follow-ups ────────────────────────
// FIX: follow-ups are now topic-specific, not generic disconnected phrases.

interface Topic {
  domain: string;
  prompt: string;
  followUps: string[]; // contextually relevant follow-ups for this topic
}

const TOPICS: Topic[] = [
  // Cooking & food
  { domain: "cooking", prompt: "How long does pasta dough last in the fridge?", followUps: ["What's the best way to store it — wrapped or in a container?", "Does it need to rest before rolling?", "Can I freeze it instead?"] },
  { domain: "cooking", prompt: "Best substitute for buttermilk in baking?", followUps: ["Will it affect the texture of the cake?", "What ratio should I use?", "Does it matter if it's for pancakes vs cake?"] },
  { domain: "cooking", prompt: "Why does bread go stale so fast?", followUps: ["Does wrapping it in plastic actually help?", "Is sourdough slower to go stale than regular bread?", "What about freezing — does that reset the staleness?"] },
  { domain: "cooking", prompt: "How do I stop cut apples from browning?", followUps: ["Does lemon juice change the taste?", "How long does the lemon juice trick actually last?", "What about saltwater — does that work better?"] },
  { domain: "cooking", prompt: "What's the ratio for making a basic vinaigrette?", followUps: ["Does the type of oil matter?", "How do I keep it from separating?", "Can I make it ahead of time?"] },
  { domain: "cooking", prompt: "How to ripen an avocado overnight", followUps: ["Does the paper bag trick actually work faster?", "Can I put it in the oven?", "How do I know when it's perfectly ripe?"] },
  { domain: "cooking", prompt: "Why is my sourdough not rising?", followUps: ["How do I know if my starter is actually active?", "Does the temperature of the room matter?", "How long should bulk fermentation take?"] },
  { domain: "cooking", prompt: "What temp should I cook chicken to?", followUps: ["Does it matter where I take the temperature from?", "Does resting the chicken change anything?", "What about chicken thighs vs breast?"] },
  { domain: "cooking", prompt: "Difference between baking soda and baking powder", followUps: ["Can I substitute one for the other?", "What happens if I use too much?", "Why do some recipes call for both?"] },
  { domain: "cooking", prompt: "What is umami exactly?", followUps: ["Which common foods have the most umami?", "Can I add umami to a dish without MSG?", "Is it the same as savory?"] },
  { domain: "cooking", prompt: "How to temper chocolate at home without a thermometer", followUps: ["What happens if it's not tempered properly?", "Does the type of chocolate matter?", "What's the seeding method?"] },
  { domain: "cooking", prompt: "Why does garlic turn blue when pickled?", followUps: ["Is it safe to eat?", "How do I prevent it from happening?", "Does the age of the garlic matter?"] },
  { domain: "cooking", prompt: "I've been trying to make pasta from scratch but it keeps tearing when I roll it thin. What am I doing wrong?", followUps: ["How thin should I actually roll pasta for tagliatelle?", "Does the flour type make a big difference?", "How long should I let it rest?"] },
  { domain: "cooking", prompt: "My sourdough starter smells like vinegar after a week — is that normal?", followUps: ["Should I feed it more frequently?", "What does a healthy starter smell like?", "How do I know if it's actually dead?"] },

  // Health & body
  { domain: "health", prompt: "What causes hiccups?", followUps: ["Why do some people get them for hours?", "What actually stops them?", "Are there any cures that are medically proven?"] },
  { domain: "health", prompt: "What causes muscle cramps at night?", followUps: ["Is it actually a magnesium deficiency?", "Does stretching before bed help?", "Should I be worried if they happen every night?"] },
  { domain: "health", prompt: "Difference between cold and flu symptoms", followUps: ["Is there a way to tell early on which one it is?", "Does the flu always come with a fever?", "When should I actually see a doctor?"] },
  { domain: "health", prompt: "Why do we yawn when we see others yawn?", followUps: ["Is it related to empathy?", "Do sociopaths yawn less at others?", "Do animals do this too?"] },
  { domain: "health", prompt: "How much water should I actually drink per day?", followUps: ["Does the 8 glasses rule have any science behind it?", "Does coffee count toward hydration?", "How do I know if I'm dehydrated?"] },
  { domain: "health", prompt: "What causes déjà vu?", followUps: ["Is it more common at certain ages?", "Is it related to epilepsy or other conditions?", "Why does it feel so vivid even though nothing actually happened?"] },
  { domain: "health", prompt: "How does sleep deprivation affect concentration?", followUps: ["Does one bad night have lasting effects?", "Is there a way to partially compensate with caffeine?", "What are the cognitive effects after a week of poor sleep?"] },
  { domain: "health", prompt: "I keep waking up at 3am and can't get back to sleep — been happening for two weeks. Any ideas?", followUps: ["Could it be stress-related even if I don't feel stressed?", "Is there anything I can do in the moment when I wake up?", "When is it worth seeing a doctor about sleep issues?"] },
  { domain: "health", prompt: "I just started running and my knees hurt after about 20 minutes. Is that normal?", followUps: ["Could it be my shoes?", "Should I be stretching before or after?", "Is there a way to build up distance without the knee pain?"] },
  { domain: "health", prompt: "What causes restless leg syndrome?", followUps: ["Is it related to iron levels?", "Are there non-medication ways to manage it?", "Does it get worse with age?"] },

  // Science & nature
  { domain: "science", prompt: "Why does the sky turn red at sunset?", followUps: ["Does pollution make sunsets more red?", "Why is it different colors at different times of year?", "What makes a green flash at sunset?"] },
  { domain: "science", prompt: "What causes thunder?", followUps: ["Why does the sound come after the lightning?", "How do you calculate how far away a storm is?", "Why does thunder sometimes rumble for so long?"] },
  { domain: "science", prompt: "Why does metal feel colder than wood at the same temperature?", followUps: ["Does this mean metal IS colder?", "What property of materials determines this?", "Is marble the same way?"] },
  { domain: "science", prompt: "Why does hot water sometimes freeze faster than cold water?", followUps: ["Has this actually been proven in lab conditions?", "What's the Mpemba effect exactly?", "Does the container shape matter?"] },
  { domain: "science", prompt: "How do birds navigate during migration?", followUps: ["Can they actually sense magnetic fields?", "Do they all fly the same route every year?", "What happens if one gets blown off course?"] },
  { domain: "science", prompt: "What causes the Northern Lights?", followUps: ["Why do they only appear near the poles?", "Can solar storms cause them at lower latitudes?", "What determines the colors?"] },
  { domain: "science", prompt: "Why does ice float on water?", followUps: ["What would happen to life on Earth if it didn't?", "Is water the only substance where the solid floats?", "Does salt water ice behave the same way?"] },
  { domain: "science", prompt: "How do fireflies produce light?", followUps: ["Does it use a lot of their energy?", "Why do they flash in patterns?", "Can scientists recreate bioluminescence artificially?"] },
  { domain: "science", prompt: "What causes earthquakes?", followUps: ["Can we predict them at all?", "Why are some areas so much more prone to them?", "What's the difference between magnitude and intensity?"] },

  // Home & DIY
  { domain: "diy", prompt: "How do I remove a stripped screw?", followUps: ["What if the rubber band trick doesn't work?", "Is there a drill bit designed for this?", "How do I avoid stripping screws in the first place?"] },
  { domain: "diy", prompt: "How to fix a squeaky door hinge", followUps: ["How do I know which hinge is the problem?", "Is WD-40 the right thing to use or is there something better?", "How long does the fix last?"] },
  { domain: "diy", prompt: "Best way to unclog a slow drain", followUps: ["Does baking soda and vinegar actually work or is that a myth?", "When should I just call a plumber?", "What's the best tool for a really stubborn clog?"] },
  { domain: "diy", prompt: "How to clean mold from bathroom grout", followUps: ["Is bleach safe to use in a small bathroom?", "How do I stop it from coming back?", "Does the type of grout matter?"] },
  { domain: "diy", prompt: "How to patch a small hole in drywall", followUps: ["What's the smallest hole where I need a patch kit vs just spackle?", "How long should I wait before painting?", "How do I match the texture?"] },
  { domain: "diy", prompt: "Why does my circuit breaker keep tripping?", followUps: ["How do I know if it's the breaker itself or something on that circuit?", "Is it safe to keep resetting it?", "What's the maximum load for a standard 15-amp circuit?"] },
  { domain: "diy", prompt: "My houseplant looks wilted even though I've been watering it regularly. Could I be overwatering it?", followUps: ["How do I check if the soil is actually too wet?", "What's the best way to dry out overwatered soil?", "Are some plants more sensitive to overwatering?"] },
  { domain: "diy", prompt: "Best way to insulate a drafty window without replacing it", followUps: ["Does window film actually make a noticeable difference?", "How much can I realistically reduce heat loss?", "Is this worth doing for summer as well?"] },

  // Technology
  { domain: "tech", prompt: "Why is my phone battery draining so fast?", followUps: ["How do I find out which app is using the most battery?", "Does screen brightness make that much of a difference?", "Is battery replacement worth it for an older phone?"] },
  { domain: "tech", prompt: "What does VPN actually do?", followUps: ["Does it make browsing actually anonymous?", "Does it slow down your connection significantly?", "When does it not protect you?"] },
  { domain: "tech", prompt: "Why does my wifi slow down at night?", followUps: ["Is it ISP throttling or just congestion?", "Does the channel my router uses matter?", "Would switching to 5GHz help?"] },
  { domain: "tech", prompt: "What's the difference between RAM and storage?", followUps: ["How much RAM do I actually need for normal use?", "Does more RAM speed up my computer?", "What's the difference between SSD and HDD?"] },
  { domain: "tech", prompt: "What is two-factor authentication and should I use it?", followUps: ["Is SMS-based 2FA actually secure?", "What's the difference between an authenticator app and SMS?", "What happens if I lose my phone?"] },
  { domain: "tech", prompt: "Why does restarting a computer fix most problems?", followUps: ["What exactly gets cleared when you restart?", "Is there a difference between restart and shutdown?", "Does sleep mode cause the same issues over time?"] },
  { domain: "tech", prompt: "How do I free up storage on my phone?", followUps: ["What actually takes up the most space?", "Is clearing the cache safe?", "Does offloading apps to the cloud work well?"] },

  // Finance
  { domain: "finance", prompt: "How does compound interest work?", followUps: ["What's the difference between daily and monthly compounding?", "How big a difference does starting 5 years earlier make?", "Does the rule of 72 actually work?"] },
  { domain: "finance", prompt: "What is an emergency fund and how much should I have?", followUps: ["Should it be in a regular savings account or something that earns more?", "Is 3 months enough or do I need 6?", "What counts as an emergency?"] },
  { domain: "finance", prompt: "How do index funds work?", followUps: ["What's the difference between an index fund and an ETF?", "How do they compare to actively managed funds long-term?", "What index should I start with?"] },
  { domain: "finance", prompt: "What is a credit score made up of?", followUps: ["What has the biggest impact — payment history or utilization?", "How long does a late payment affect your score?", "Does checking your own score hurt it?"] },
  { domain: "finance", prompt: "I'm trying to save money but every month I spend more than I planned. How do people actually stick to a budget?", followUps: ["Does tracking every purchase actually help or is it overwhelming?", "Is zero-based budgeting realistic for most people?", "What's the most common reason people fail at budgeting?"] },

  // Language & writing
  { domain: "language", prompt: "Difference between 'affect' and 'effect'", followUps: ["Are there cases where 'effect' is a verb?", "What's a good memory trick for remembering which is which?", "What about 'impact' — can that replace both?"] },
  { domain: "language", prompt: "What is passive voice and why avoid it?", followUps: ["Are there times when passive voice is actually better?", "How do I identify it in my own writing?", "Does academic writing still use it a lot?"] },
  { domain: "language", prompt: "How do I write a good professional email?", followUps: ["How long is too long for a professional email?", "What's a good way to start without 'I hope this email finds you well'?", "When should I follow up if I don't get a reply?"] },
  { domain: "language", prompt: "What's an Oxford comma and does it matter?", followUps: ["Can leaving it out actually cause ambiguity?", "Is it required in American English?", "Which major style guides require it?"] },
  { domain: "language", prompt: "I've been trying to learn Spanish for about a year. I can read okay but my speaking is really slow. What's the best way to improve fluency?", followUps: ["Does the method matter — classes vs apps vs immersion?", "How many hours of speaking practice does it typically take?", "Is thinking in Spanish something that comes naturally or do I need to practice it?"] },

  // Travel & geography
  { domain: "travel", prompt: "What's the best way to avoid jet lag?", followUps: ["Does melatonin actually work for jet lag?", "How important is staying awake until local bedtime?", "Does direction of travel matter — east vs west?"] },
  { domain: "travel", prompt: "What's the difference between a visa and a passport?", followUps: ["Can I get a visa on arrival for most countries?", "How far in advance do I need to apply for a visa?", "Does my passport need to be valid for longer than my trip?"] },
  { domain: "travel", prompt: "What's the best way to exchange currency?", followUps: ["Are airport exchange booths ever worth it?", "Do debit cards with no foreign transaction fees actually give better rates?", "Should I get local cash before I fly or after I land?"] },
  { domain: "travel", prompt: "I'm moving to a new city and don't know anyone. How do adults actually make friends?", followUps: ["What kind of activities work best for meeting people?", "How many times do you need to see someone before you can call them a friend?", "Is it harder after 30?"] },

  // Psychology & behavior
  { domain: "psychology", prompt: "Why do people procrastinate?", followUps: ["Is it actually a time management problem or something else?", "Why does it feel so hard to start even when I know I should?", "Does procrastination get worse under stress?"] },
  { domain: "psychology", prompt: "What is the Dunning-Kruger effect?", followUps: ["Does it apply equally across all domains?", "Is there a way to check if you're in the low-competence peak?", "What's the opposite of Dunning-Kruger — over-estimating others' competence?"] },
  { domain: "psychology", prompt: "Why do habits form and how do I break them?", followUps: ["How long does it really take to form a new habit?", "What makes some habits harder to break than others?", "Is replacing a habit easier than just stopping it?"] },
  { domain: "psychology", prompt: "What is cognitive dissonance?", followUps: ["What's a common everyday example?", "How do people resolve it?", "Does it happen unconsciously?"] },
  { domain: "psychology", prompt: "Why does music affect our mood?", followUps: ["Is it learned or biological?", "Why do sad songs sometimes feel comforting?", "Does tempo or key matter more?"] },
  { domain: "psychology", prompt: "I've been working from home for two years and feel really isolated. Any practical ways to feel less disconnected?", followUps: ["Does video call fatigue make it worse?", "Is coworking actually helpful for this?", "How do you rebuild social stamina after being isolated for a while?"] },

  // History & culture
  { domain: "history", prompt: "Why did the Roman Empire fall?", followUps: ["Was it mainly military, economic, or political?", "Did the Eastern Empire have different reasons for lasting longer?", "Is there a single most accepted theory among historians?"] },
  { domain: "history", prompt: "What started World War I?", followUps: ["Was the assassination of Franz Ferdinand really the cause or just the trigger?", "Could it have been avoided?", "Why did it spread so quickly across Europe?"] },
  { domain: "history", prompt: "Why was the printing press so significant?", followUps: ["How quickly did it spread across Europe?", "What was the first major book printed?", "Did the Church try to suppress it?"] },
  { domain: "history", prompt: "How did the Black Death change Europe?", followUps: ["How did it affect the feudal system?", "Did it accelerate the Renaissance?", "Why did it kill such a high percentage of the population?"] },
  { domain: "history", prompt: "What was the Silk Road?", followUps: ["Was it actually a single road or multiple routes?", "What goods were most valuable on the Silk Road?", "How did it decline?"] },

  // Lifestyle
  { domain: "lifestyle", prompt: "How do I stop overthinking?", followUps: ["Is overthinking the same as anxiety?", "Are there specific techniques that actually work?", "Does journaling help or does it just reinforce the thoughts?"] },
  { domain: "lifestyle", prompt: "What's a good way to wind down before bed?", followUps: ["How long before bed should I stop using screens?", "Does a warm shower actually help you sleep?", "What's the evidence on sleep meditation?"] },
  { domain: "lifestyle", prompt: "How do I get better at remembering names?", followUps: ["Does repeating the name out loud when you meet someone work?", "Is there a link between remembering names and general memory?", "What's the best mental trick for name recall?"] },
  { domain: "lifestyle", prompt: "What's the best way to deal with a difficult coworker?", followUps: ["How do you address it without making it worse?", "When is it worth going to a manager?", "Does documenting the issues help?"] },
  { domain: "lifestyle", prompt: "I have a job interview next week at a company I really want to work at. What's the best way to prepare?", followUps: ["How much time should I spend researching the company?", "What are the most common mistakes in interviews?", "How do I handle a question I don't know the answer to?"] },
  { domain: "lifestyle", prompt: "My landlord wants to increase my rent by 15%. Is that normal and what are my options?", followUps: ["Are there any legal limits on how much rent can be increased?", "Is it worth negotiating?", "What should I check in my lease before responding?"] },
];

// Weighted domain selection based on persona
function pickTopicForPersona(persona: Persona): Topic {
  const weights = TOPICS.map(t => persona.domainWeights[t.domain] ?? 1);
  const total   = weights.reduce((a, b) => a + b, 0);
  let r = randFloat() * total, acc = 0;
  for (let i = 0; i < TOPICS.length; i++) {
    acc += weights[i];
    if (r <= acc) return TOPICS[i];
  }
  return TOPICS[TOPICS.length - 1];
}

// ── System prompts — expanded pool ──────────────────────────────────────────

const SYSTEM_PROMPTS: string[] = [
  "You are a helpful assistant. Answer concisely.",
  "Be direct and to the point.",
  "Keep your answer under 3 sentences.",
  "Explain things simply, as if to a curious non-expert.",
  "Give practical, actionable advice.",
  "Answer briefly but completely.",
  "You are a knowledgeable friend. Be conversational.",
  "Just answer the question directly.",
  "Keep it simple. Skip the preamble.",
  "Respond naturally, as if chatting.",
  "Avoid bullet points — just write in plain sentences.",
  "Be thorough but not wordy.",
  "Give me the useful information, not the obvious caveats.",
  "Answer like you're explaining to someone who knows a little about this.",
  "One short paragraph is ideal.",
  "You're an expert. Be confident and direct.",
  "Don't hedge. Just tell me the answer.",
  "Start with the most important thing.",
  "Assume I'm reasonably intelligent. No over-explaining.",
  "Be practical. Skip the theory.",
];

// ── Default providers ─────────────────────────────────────────────────────────

const DEFAULT_PROVIDERS = [
  {
    name:     "anthropic",
    provider: "anthropic",
    base_url: "https://api.anthropic.com/v1",
    model:    "claude-haiku-4-5",
    style:    "anthropic" as const,
    weight:   1,
  },
  {
    name:     "zai",
    provider: "zai",
    base_url: "https://api.z.ai/api/coding/paas/v4",
    model:    "glm-5.1",
    style:    "openai" as const,
    weight:   1,
  },
];

interface ProviderEntry {
  name: string;
  provider: string;
  base_url: string;
  model: string;
  style: "anthropic" | "openai";
  weight?: number;
}

// ── Token budget — perturbed log-normal per session ─────────────────────────
// FIX: mu and sigma are slightly perturbed per call to break fixed-parameter fingerprint

function sampleMaxTokens(persona: Persona): number {
  // Perturb params slightly per call: ±0.15 on mu, ±0.1 on sigma
  const mu    = persona.tokenMu    + (randFloat() - 0.5) * 0.3;
  const sigma = persona.tokenSigma + (randFloat() - 0.5) * 0.2;
  const t = Math.round(logNormal(mu, Math.max(0.3, sigma)));
  return Math.max(20, Math.min(500, t));
}

// ── Temperature — per-session, not per-message ───────────────────────────────
// FIX: real users pick one temperature and stick with it in a session

function sampleSessionTemperature(): number {
  // Use non-uniform distribution: most users cluster around 0.7–1.0
  // Occasionally terse users prefer 0.3–0.5, creative users 1.0–1.3
  const r = randFloat();
  if (r < 0.15) return Math.round((0.2 + randFloat() * 0.3) * 10) / 10; // terse: 0.2–0.5
  if (r < 0.80) return Math.round((0.6 + randFloat() * 0.5) * 10) / 10; // normal: 0.6–1.1
  return Math.round((1.1 + randFloat() * 0.3) * 10) / 10;               // creative: 1.1–1.4
}

// ── Day-of-week + hour activity weights ──────────────────────────────────────
// FIX: real usage has strong weekly patterns — weekends are quieter,
// mornings and evenings are more active than 2pm slumps or 3am

const HOUR_WEIGHTS = [
  0.1, 0.0, 0.0, 0.0, 0.1, 0.2, // 0–5: night (very low)
  0.5, 0.9, 1.2, 1.1, 1.0, 0.9, // 6–11: morning ramp-up
  0.8, 0.7, 0.7, 0.8, 0.9, 1.1, // 12–17: afternoon (mild slump at 13–15)
  1.2, 1.3, 1.1, 0.9, 0.6, 0.3, // 18–23: evening peak, then taper
];

const DOW_WEIGHTS = [0.6, 0.9, 1.0, 1.0, 1.0, 0.85, 0.7]; // Sun–Sat

function activityLevel(tzOffsetHours: number): number {
  const utcHour   = new Date().getUTCHours();
  const localHour = (utcHour + tzOffsetHours + 24) % 24;
  const dow       = new Date().getDay(); // 0=Sun
  return HOUR_WEIGHTS[localHour] * DOW_WEIGHTS[dow];
}

// Should we skip this round based on activity level? (probabilistic, not binary)
function shouldSkipForActivity(tzOffsetHours: number): boolean {
  const level = activityLevel(tzOffsetHours);
  // At level 0.0, always skip. At 1.3 (peak), skip ~5%. Linear interpolation.
  const skipProb = Math.max(0, 1 - level * 0.8);
  return randFloat() < skipProb;
}

// ── Soft interval sampling ────────────────────────────────────────────────────
// FIX: rejection sampling instead of hard clamp — preserves Poisson property

function sampleIntervalMs(baseMin: number, maxMin: number): number {
  const meanMin   = (baseMin + maxMin) / 2;
  const softCapMs = maxMin * 2.5 * 60 * 1000;
  const minMs     = baseMin * 60 * 1000;
  return Math.max(minMs, softExponential(meanMin * 60 * 1000, softCapMs));
}

// ── HTTP ─────────────────────────────────────────────────────────────────────

function validateUrl(urlStr: string): void {
  const parsed = new URL(urlStr);
  if (parsed.protocol !== "https:") {
    throw new Error(`Rejected non-HTTPS URL: ${urlStr}`);
  }
  const hostname = parsed.hostname;
  if (net.isIP(hostname)) {
    // Reject private/reserved/loopback/link-local IPs
    const parts = hostname.split(".").map(Number);
    if (
      hostname === "127.0.0.1" || hostname === "::1" ||
      parts[0] === 10 ||
      (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) ||
      (parts[0] === 192 && parts[1] === 168) ||
      (parts[0] === 169 && parts[1] === 254) ||
      parts[0] === 0
    ) {
      throw new Error(`Rejected private/reserved IP in URL: ${urlStr}`);
    }
  }
}

function post(urlStr: string, headers: Record<string, string>, body: object, proxyUrl?: string): Promise<string> {
  return new Promise((resolve, reject) => {
    validateUrl(urlStr);
    const parsed = new URL(urlStr);
    const data   = JSON.stringify(body);
    const opts   = {
      hostname: parsed.hostname,
      port:     Number(parsed.port) || 443,
      path:     parsed.pathname + parsed.search,
      method:   "POST",
      headers:  {
        "Content-Type":   "application/json",
        "Content-Length": Buffer.byteLength(data),
        ...headers,
      },
    };
    const req = https.request(opts, res => {
      let out = "";
      res.on("data", chunk => (out += chunk));
      res.on("end",  () =>
        res.statusCode && res.statusCode < 400
          ? resolve(out)
          : reject(new Error(`HTTP ${res.statusCode}`)),
      );
    });
    req.on("error", reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error("timeout")); });
    req.write(data);
    req.end();
  });
}

// ── Fire a single request ─────────────────────────────────────────────────────

interface FireOptions {
  prompt: string;
  maxTokens: number;
  temperature: number;
  systemPrompt?: string;
}

async function fireOne(p: ProviderEntry, apiKey: string, opts: FireOptions): Promise<string> {
  const base = p.base_url.replace(/\/$/, "");
  const { prompt, maxTokens, temperature, systemPrompt } = opts;

  if (p.style === "anthropic") {
    const body: any = {
      model:      p.model,
      max_tokens: maxTokens,
      temperature,
      messages:   [{ role: "user", content: prompt }],
    };
    if (systemPrompt) body.system = systemPrompt;
    const raw = await post(`${base}/messages`, {
      "x-api-key":         apiKey,
      "anthropic-version": "2023-06-01",
    }, body);
    return JSON.parse(raw)?.content?.[0]?.text ?? "(no reply)";

  } else {
    const messages: any[] = [];
    if (systemPrompt) messages.push({ role: "system", content: systemPrompt });
    messages.push({ role: "user", content: prompt });
    const raw = await post(`${base}/chat/completions`, {
      "Authorization": `Bearer ${apiKey}`,
    }, { model: p.model, max_tokens: maxTokens, temperature, messages });
    const msg = JSON.parse(raw)?.choices?.[0]?.message;
    // GLM-5.1 is a reasoning model — content may be in reasoning_content when content is empty
    return msg?.content || msg?.reasoning_content || "(no reply)";
  }
}

// ── Session builder — contextual follow-ups ──────────────────────────────────
// FIX: follow-ups are now drawn from the specific topic's paired follow-up list

function buildSession(persona: Persona): { topic: Topic; messages: string[]; isMultiTurn: boolean } {
  const topic       = pickTopicForPersona(persona);
  const isMultiTurn = randFloat() < persona.multiTurnRate;

  if (!isMultiTurn || !topic.followUps.length) {
    return { topic, messages: [topic.prompt], isMultiTurn: false };
  }

  const turns    = randInt(1, Math.min(2, topic.followUps.length));
  const selected = randSample(topic.followUps, turns);
  return { topic, messages: [topic.prompt, ...selected], isMultiTurn: true };
}

// ── Log — metadata only ───────────────────────────────────────────────────────
// FIX: never log topics or reply content — only provider/token/timing metadata

const LOG_PATH = path.join(process.env.HOME ?? "/tmp", ".openclaw", "ghostprint.log");

function logLine(msg: string) {
  const ts   = new Date().toISOString().replace("T", " ").slice(0, 19);
  const line = `[${ts}] ${msg}\n`;
  try { fs.appendFileSync(LOG_PATH, line, { mode: 0o600 }); } catch {}
}

// ── Core noise round ──────────────────────────────────────────────────────────

interface RunResult {
  fired: number;
  skipped: number;
  errors: string[];
  lines: string[];
}

async function runNoise(
  providers: ProviderEntry[],
  resolveKey: (provider: string) => Promise<string | undefined>,
  tzOffsetHours: number,
): Promise<RunResult> {
  const result: RunResult = { fired: 0, skipped: 0, errors: [], lines: [] };

  if (!providers.length) {
    result.errors.push("No providers configured");
    return result;
  }

  // Activity-weighted skip (FIX: probabilistic, not binary quiet-hours)
  if (shouldSkipForActivity(tzOffsetHours)) {
    logLine("  · activity-weighted skip");
    return result;
  }

  // 8% pure idle skip (real users sometimes just don't query)
  if (randFloat() < 0.08) {
    logLine("  · idle skip");
    return result;
  }

  // Get current persona (stable across rounds)
  const persona = getPersona();

  // Provider selection: weighted random, 25% chance of 2 providers
  const weights      = providers.map(p => Math.max(p.weight ?? 1, 1));
  const total        = weights.reduce((a, b) => a + b, 0);
  const numProviders = randFloat() < 0.25 ? Math.min(2, providers.length) : 1;
  const selected     = new Set<ProviderEntry>();

  for (let attempt = 0; selected.size < numProviders && attempt < 20; attempt++) {
    let r = randFloat() * total, acc = 0;
    for (let i = 0; i < providers.length; i++) {
      acc += weights[i];
      if (r <= acc) { selected.add(providers[i]); break; }
    }
  }

  const toFire = [...selected];

  for (let i = 0; i < toFire.length; i++) {
    const p   = toFire[i];
    const key = await resolveKey(p.provider);

    if (!key) {
      const msg = `  ⚠️  ${p.name}: no API key — skipping`;
      result.lines.push(msg);
      logLine(msg);
      result.skipped++;
      continue;
    }

    const session      = buildSession(persona);
    const maxTokens    = sampleMaxTokens(persona);
    const temperature  = sampleSessionTemperature(); // FIX: per-session, not per-message
    const systemPrompt = randFloat() < persona.systemPromptRate ? randChoice(SYSTEM_PROMPTS) : undefined;

    // FIX: log only metadata, no content
    logLine(`  → ${p.name}/${p.model} persona=${persona.name} turns=${session.messages.length} tokens=${maxTokens} temp=${temperature} domain=${session.topic.domain}`);

    try {
      // Turn 1
      await fireOne(p, key, {
        prompt:      session.messages[0],
        maxTokens,
        temperature,
        systemPrompt,
      });
      result.fired++;

      // Follow-up turns: post-response reading delay (FIX: user reads reply before responding)
      for (let t = 1; t < session.messages.length; t++) {
        // Simulate reading time: log-normal ~5–30s (median ~10s)
        const readMs = Math.round(logNormal(2.3, 0.6) * 1000);
        await sleep(Math.max(3000, Math.min(45000, readMs)));

        await fireOne(p, key, {
          prompt:     session.messages[t],
          maxTokens:  Math.round(maxTokens * (0.4 + randFloat() * 0.4)), // FIX: variable follow-up length
          temperature,
        });
      }

      logLine(`  ✓ ${p.name} ok turns=${session.messages.length}`);

    } catch (e: any) {
      const err = `  ✗ ${p.name}: ${e.message}`;
      result.lines.push(err);
      logLine(err);
      result.errors.push(err);
    }

    // FIX: dual-provider stagger — longer delay between providers
    if (i < toFire.length - 1) {
      const staggerMs = Math.round(logNormal(3.5, 0.7) * 1000); // median ~33s
      await sleep(Math.max(15000, Math.min(120000, staggerMs)));
    }
  }

  return result;
}

// ── Plugin entry ──────────────────────────────────────────────────────────────

export default function (api: any) {
  const cfg            = api.config?.plugins?.entries?.ghostprint?.config ?? {};
  const enabled        = cfg.enabled !== false;
  const minIntervalMin = cfg.min_interval_minutes ?? 90;
  const maxIntervalMin = cfg.max_interval_minutes ?? 180;
  const tzOffsetHours  = cfg.timezone_offset       ?? 3;

  const providers: ProviderEntry[] = cfg.providers?.length
    ? cfg.providers
    : DEFAULT_PROVIDERS;

  const resolveKey = async (provider: string): Promise<string | undefined> => {
    try {
      const auth = await api.runtime.modelAuth.resolveApiKeyForProvider({
        provider,
        cfg: api.config,
      });
      return auth?.apiKey ?? undefined;
    } catch {
      return undefined;
    }
  };

  // ── Tool: ghostprint_fire ─────────────────────────────────────────────────
  api.registerTool({
    name: "ghostprint_fire",
    description: "Fire a ghostprint noise round immediately. Sends persona-driven realistic-looking LLM sessions to configured providers to depersonalize your usage fingerprint.",
    parameters: { type: "object", properties: {}, required: [] },
    async execute(_id: string, _params: {}) {
      if (!enabled) return { content: [{ type: "text", text: "ghostprint is disabled." }] };
      logLine("👻 manual fire");
      const res = await runNoise(providers, resolveKey, tzOffsetHours);
      return {
        content: [{
          type: "text",
          text: [
            `👻 Ghostprint v3.0 — round complete`,
            `Fired: ${res.fired} | Skipped: ${res.skipped} | Errors: ${res.errors.length}`,
            `Active persona: ${currentPersona.name}`,
            ...res.lines,
          ].join("\n"),
        }],
      };
    },
  });

  // ── Tool: ghostprint_stats ────────────────────────────────────────────────
  api.registerTool({
    name: "ghostprint_stats",
    description: "Show ghostprint cumulative stats and recent log entries.",
    parameters: { type: "object", properties: {}, required: [] },
    async execute(_id: string, _params: {}) {
      try {
        const lines   = fs.readFileSync(LOG_PATH, "utf8").split("\n").filter(Boolean);
        const manual  = lines.filter(l => l.includes("manual fire")).length;
        const sched   = lines.filter(l => l.includes("scheduled fire")).length;
        const ok      = lines.filter(l => l.includes("✓")).length;
        const fail    = lines.filter(l => l.includes("✗")).length;
        const skip    = lines.filter(l => l.includes("⚠️")).length;
        const idle    = lines.filter(l => l.includes("idle skip") || l.includes("activity-weighted")).length;
        return {
          content: [{
            type: "text",
            text: [
              `📊 Ghostprint v3.0 stats`,
              `Manual runs  : ${manual}`,
              `Scheduled    : ${sched}`,
              `Successful   : ${ok}`,
              `Failed       : ${fail}`,
              `Skipped/key  : ${skip}`,
              `Idle/activity: ${idle}`,
              `Active persona: ${currentPersona.name}`,
              ``,
              `Last 10 log lines:`,
              lines.slice(-10).join("\n"),
            ].join("\n"),
          }],
        };
      } catch {
        return { content: [{ type: "text", text: "No log yet. Run ghostprint_fire to start." }] };
      }
    },
  });

  // ── Background scheduler ──────────────────────────────────────────────────
  if (enabled) {
    api.logger.info(`[ghostprint] v3.0 scheduler armed — Poisson mean ~${Math.round((minIntervalMin + maxIntervalMin) / 2)}min, GMT+${tzOffsetHours}`);

    const schedule = () => {
      const waitMs = sampleIntervalMs(minIntervalMin, maxIntervalMin);
      setTimeout(async () => {
        logLine("👻 scheduled fire");
        try {
          await runNoise(providers, resolveKey, tzOffsetHours);
        } catch (e: any) {
          logLine(`  ✗ scheduler error: ${e.message}`);
        }
        schedule();
      }, waitMs);
    };

    schedule();
  }

  api.logger.info("[ghostprint] v3.0 loaded — tools: ghostprint_fire, ghostprint_stats");
}
