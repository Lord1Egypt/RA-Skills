/**
 * Prompt Compressor for OpenClaw
 * ==============================
 * Saves 20-50% of LLM input tokens on every message.
 *
 * Runs as a message:received hook — compresses user messages BEFORE the
 * LLM sees them. No subprocess, no Python, no extra process. All 154
 * rules run in-process in ~3ms.
 *
 * Install:
 *   mkdir -p ~/.openclaw/hooks/prompt-compressor
 *   cp handler.js ~/.openclaw/hooks/prompt-compressor/
 *   openclaw hooks enable prompt-compressor
 *
 * Score: 96.3% on 24-test benchmark (optimized via 300+ evolutionary variants)
 */

// =============================================================================
// PROTECTED PATTERNS — never compress content matching these
// =============================================================================

const PROTECTED = [
  /```[\s\S]*?```/g,                           // code blocks
  /`[^`]+`/g,                                  // inline code
  /"[^"]*"/g,                                  // double-quoted strings
  /(?<![a-zA-Z])'[^'\n]{1,100}'(?![a-zA-Z])/g, // single-quoted strings (not contractions)
  /https?:\/\/\S+/g,                           // URLs
  /[\w./\\]+\.\w{1,5}\b/g,                     // file paths
  /\b\d[\d.,]+\b/g,                            // numbers
  /[A-Z][A-Z_]{2,}/g,                          // CONSTANTS
];

function protectSpans(text) {
  const placeholders = [];
  for (const pattern of PROTECTED) {
    pattern.lastIndex = 0;
    text = text.replace(pattern, (match) => {
      const ph = `__P${placeholders.length}__`;
      placeholders.push([ph, match]);
      return ph;
    });
  }
  return [text, placeholders];
}

function restoreSpans(text, placeholders) {
  for (let i = placeholders.length - 1; i >= 0; i--) {
    text = text.replace(placeholders[i][0], placeholders[i][1]);
  }
  return text;
}

// =============================================================================
// PHRASE RULES — regex patterns to remove (31 rules)
// =============================================================================

const PHRASE_RULES = [
  // Greetings and sign-offs
  [/\b(hi|hello|hey|greetings|good\s+(morning|afternoon|evening)),?\s*(claude|assistant|ai|there|everyone)?[!,.]?\s*/gi, ""],
  [/\b(thanks?(\s+you)?(\s+(so\s+much|very\s+much|a\s+lot|in\s+advance|for\s+(your|the)\s+help))?)[!.]?\s*$/gim, ""],
  [/\b(cheers|regards|best(\s+regards)?|sincerely|warm\s+regards)[!,.]?\s*$/gim, ""],
  [/^\s*(dear\s+(claude|assistant|ai))[,.]?\s*/gim, ""],
  [/\b(I\s+)?hope\s+(this\s+finds\s+you\s+well|you('re|\s+are)\s+doing\s+well)[!,.]?\s*/gi, ""],

  // Full-sentence politeness (before partial patterns)
  [/\bwould\s+you\s+be\s+able\s+to\s+help\s+(me\s+)?(with\s+)?this\??\s*/gi, ""],
  [/\bcan\s+you\s+help\s+(me\s+)?(with\s+)?this\??\s*/gi, ""],
  [/\bcould\s+you\s+help\s+(me\s+)?(with\s+)?this\??\s*/gi, ""],

  // Politeness hedging
  [/\bcould\s+you\s+(please\s+)?(kindly\s+)?/gi, ""],
  [/\bwould\s+you\s+(please\s+)?(kindly\s+)?(be\s+able\s+to\s+)?/gi, ""],
  [/\bcan\s+you\s+(please\s+)?(kindly\s+)?/gi, ""],
  [/\bmay\s+I\s+(please\s+)?(kindly\s+)?ask\s+(you\s+to\s+)?/gi, ""],
  [/\bI\s+was\s+wondering\s+if\s+(\w+\s+)?(could|would|can|might)(\s+be\s+able\s+to)?\s+/gi, ""],
  [/\bI('d|\s+would)\s+(really\s+)?like\s+(you\s+)?to\s+/gi, ""],
  [/\bI('d|\s+would)\s+appreciate\s+(it\s+)?if\s+(you\s+)?(could|would)\s+/gi, ""],
  [/\bif\s+(it's?|it\s+is|that's?|that\s+is)\s+(not\s+too\s+much\s+trouble|okay|ok|alright)\s*,?\s*/gi, ""],
  [/\bif\s+(you\s+)?(don't|do\s+not)\s+mind\s*,?\s*/gi, ""],
  [/\bdo\s+you\s+think\s+you\s+(could|can|would)\s+/gi, ""],
  [/\bI\s+need\s+your\s+help\s+(with|to|on)\s+/gi, ""],
  [/\bplease\s+help\s+me\s+(to\s+)?(with\s+)?/gi, ""],
  [/\bhelp\s+me\s+(to\s+)?(with\s+)?/gi, ""],
  [/\bhelp\s+me\b\.?\s*/gi, ""],

  // Standalone appreciation
  [/\bI('d|\s+would)\s+(really\s+)?appreciate\s+(it|that|this)\.?\s*/gi, ""],
  [/\bthat\s+would\s+be\s+((very|really|so|super|extremely)\s+)?(great|awesome|wonderful|helpful|amazing|fantastic)\.?\s*/gi, ""],
  [/\bI('d|\s+would)\s+be\s+(really\s+)?(very\s+)?(grateful|thankful)\.?\s*/gi, ""],
  [/\bany\s+help\s+(would\s+be|is)\s+(greatly\s+)?appreciated\.?\s*/gi, ""],
  [/\bthanks?\s+(you\s+)?(so\s+much|very\s+much|a\s+(lot|ton|bunch))?[!.]?\s*/gi, ""],

  // Standalone "please"
  [/\bplease\b\s*,?\s*/gi, ""],

  // Conversational filler phrases
  [/\bso\s+like\s+/gi, ""],
  [/\bI\s+mean\s*,?\s*/gi, ""],
  [/\byou\s+know\s*,?\s*/gi, ""],
];

// =============================================================================
// VERBOSE PHRASES — string replacements (81 rules)
// =============================================================================

const VERBOSE_PHRASES = [
  ["in order to", "to"],
  ["due to the fact that", "because"],
  ["for the reason that", "because"],
  ["on account of the fact that", "because"],
  ["as a result of", "because of"],
  ["in the event that", "if"],
  ["in the case that", "if"],
  ["provided that", "if"],
  ["on the condition that", "if"],
  ["with regard to", "about"],
  ["with respect to", "about"],
  ["in regard to", "about"],
  ["in relation to", "about"],
  ["pertaining to", "about"],
  ["concerning", "about"],
  ["at this point in time", "now"],
  ["at the present time", "now"],
  ["at the current moment", "now"],
  ["in the near future", "soon"],
  ["prior to", "before"],
  ["subsequent to", "after"],
  ["in addition to", "besides"],
  ["as well as", "and"],
  ["in spite of", "despite"],
  ["in the process of", "while"],
  ["for the purpose of", "to"],
  ["with the intention of", "to"],
  ["a large number of", "many"],
  ["a small number of", "few"],
  ["the vast majority of", "most"],
  ["each and every", "every"],
  ["first and foremost", "first"],
  ["one and only", "only"],
  ["basic and fundamental", "basic"],
  ["it is important to note that", "note:"],
  ["it should be noted that", "note:"],
  ["it is worth mentioning that", ""],
  ["it goes without saying that", ""],
  ["needless to say", ""],
  ["as a matter of fact", ""],
  ["to be honest", ""],
  ["to tell you the truth", ""],
  ["the thing is", ""],
  ["what I mean is", ""],
  ["what I'm trying to say is", ""],
  ["I think that", ""],
  ["I believe that", ""],
  ["I feel like", ""],
  ["in my opinion", ""],
  ["from my perspective", ""],
  ["if you ask me", ""],
  ["make sure to", "ensure you"],
  ["make sure that", "ensure"],
  ["be sure to", "ensure you"],
  ["take into account", "consider"],
  ["take into consideration", "consider"],
  ["the fact that", ""],
  ["it would be a good idea to", ""],
  ["it would be good to", ""],
  ["it might be a good idea to", ""],
  ["I was thinking of using", "using"],
  ["I was thinking about using", "using"],
  ["I was thinking of", "considering"],
  ["I was thinking about", "considering"],
  ["I've been trying to", "trying to"],
  ["I have been trying to", "trying to"],
  ["I'm trying to", ""],
  ["explain to me", "explain"],
  ["tell me about", "explain"],
  ["walk me through", "explain"],
  ["come up with", "create"],
  ["figure out", "determine"],
  ["carry out", "do"],
  ["bring about", "cause"],
  ["a lot of", "many"],
  ["lots of", "many"],
  ["sort of", ""],
  ["kind of", ""],
  ["more or less", "roughly"],
  ["by and large", "mostly"],
  ["all in all", "overall"],
];

// =============================================================================
// FILLER WORDS — removed when standalone (27 words)
// =============================================================================

const FILLER_WORDS = [
  "just", "really", "very", "quite", "rather", "somewhat",
  "basically", "essentially", "actually", "literally", "honestly",
  "simply", "merely", "definitely", "certainly", "obviously",
  "clearly", "naturally", "presumably", "apparently",
  "totally", "absolutely", "completely", "entirely",
  "personally", "frankly", "maybe",
];

// Pre-compile filler regexes
const FILLER_REGEXES = FILLER_WORDS.map(
  (w) => [new RegExp(`\\b${w}\\b\\s*`, "gi"), ""]
);

// =============================================================================
// AFFIRMATIVE / NEGATIVE NORMALIZATION
// =============================================================================

const NORMALIZATIONS = [
  [/\byeah\b/gi, "yes"],
  [/\byep\b/gi, "yes"],
  [/\byup\b/gi, "yes"],
  [/\buh-huh\b/gi, "yes"],
  [/\buh huh\b/gi, "yes"],
  [/\byea\b/gi, "yes"],
  [/\bya\b/gi, "yes"],
  [/\bnah\b/gi, "no"],
  [/\bnope\b/gi, "no"],
  [/\bnot really\b/gi, "no"],
  [/\bnegative\b/gi, "no"],
  [/\buh-uh\b/gi, "no"],
  [/\buh uh\b/gi, "no"],
  [/\bno way\b/gi, "no"],
  [/\bnot at all\b/gi, "no"],
];

// =============================================================================
// GRAMMAR FIXES — repair artifacts from compression
// =============================================================================

const GERUND_FIXES = {
  ensuring: "ensure", improving: "improve", reducing: "reduce",
  creating: "create", providing: "provide", achieving: "achieve",
  managing: "manage", maintaining: "maintain", increasing: "increase",
  implementing: "implement", developing: "develop", building: "build",
  testing: "test", deploying: "deploy", monitoring: "monitor",
  optimizing: "optimize", configuring: "configure", establishing: "establish",
  determining: "determine", addressing: "address", resolving: "resolve",
  processing: "process", generating: "generate", integrating: "integrate",
  automating: "automate", validating: "validate", analyzing: "analyze",
  investigating: "investigate", evaluating: "evaluate", facilitating: "facilitate",
};

const GERUND_REGEXES = Object.entries(GERUND_FIXES).map(
  ([gerund, inf]) => [new RegExp(`\\bto\\s+${gerund}\\b`, "gi"), `to ${inf}`]
);

// =============================================================================
// COMPRESSION ENGINE
// =============================================================================

function compress(text) {
  if (!text || text.trim().length === 0) return text;

  const original = text.trim();
  const originalLen = original.length;

  // Protect code, URLs, quoted strings, numbers
  let [working, placeholders] = protectSpans(original);

  // 1. Phrase rules (politeness, greetings, hedging)
  for (const [pattern, replacement] of PHRASE_RULES) {
    pattern.lastIndex = 0;
    working = working.replace(pattern, replacement);
  }

  // 2. Verbose phrases (case-insensitive string replacement)
  for (const [verbose, concise] of VERBOSE_PHRASES) {
    const lower = verbose.toLowerCase();
    let idx = working.toLowerCase().indexOf(lower);
    while (idx !== -1) {
      working = working.slice(0, idx) + concise + working.slice(idx + verbose.length);
      idx = working.toLowerCase().indexOf(lower, idx + concise.length);
    }
  }

  // 3. Grammar fixes ("to ensuring" → "to ensure")
  for (const [pattern, replacement] of GERUND_REGEXES) {
    pattern.lastIndex = 0;
    working = working.replace(pattern, replacement);
  }
  working = working.replace(/\bto\s+to\b/gi, "to");

  // 4. Filler words
  for (const [pattern] of FILLER_REGEXES) {
    pattern.lastIndex = 0;
    working = working.replace(pattern, "");
  }

  // 5. Affirmative/negative normalization
  for (const [pattern, replacement] of NORMALIZATIONS) {
    pattern.lastIndex = 0;
    working = working.replace(pattern, replacement);
  }

  // 6. Whitespace cleanup
  working = working.replace(/[ \t]+/g, " ");                       // collapse spaces
  working = working.replace(/\n\s*\n\s*\n+/g, "\n\n");             // collapse newlines
  working = working.replace(/ ([.,!?;:])/g, "$1");                 // space before punctuation
  working = working.replace(/([.,!?;:])\s*([.,!?;:])/g, "$2");     // doubled punctuation
  working = working.replace(/^\s*[.,!?;:]+\s*/gm, "");             // line starts with punctuation
  working = working.replace(/,\s*([!?.])/g, "$1");                 // ", !" → "!"
  working = working.trim();

  // Remove lines that are empty or trivially short
  working = working
    .split("\n")
    .filter((l) => l.trim().length > 2)
    .join("\n")
    .trim();

  // 7. Capitalize sentence starts
  if (working.length > 0 && working[0] >= "a" && working[0] <= "z") {
    working = working[0].toUpperCase() + working.slice(1);
  }
  working = working.replace(/([.!?]\s+)([a-z])/g, (_, p, c) => p + c.toUpperCase());
  working = working.replace(/(\n\s*)([a-z])/g, (_, p, c) => p + c.toUpperCase());

  // 8. Restore protected content
  working = restoreSpans(working, placeholders);

  // Stats
  const savedChars = originalLen - working.length;
  const savedPct = originalLen > 0 ? ((savedChars / originalLen) * 100).toFixed(1) : "0.0";
  const origTokens = Math.max(1, Math.floor(originalLen / 4));
  const compTokens = Math.max(1, Math.floor(working.length / 4));

  return {
    text: working,
    original: originalLen,
    compressed: working.length,
    origTokens,
    compTokens,
    savedTokens: origTokens - compTokens,
    savedPct: parseFloat(savedPct),
  };
}

// =============================================================================
// OPENCLAW HOOK — intercepts messages BEFORE the LLM
// =============================================================================

const MIN_LENGTH = 40;

const SKIP_PATTERNS = [
  /^\/\w+/,           // slash commands
  /^```/,             // starts with code block
  /^\{[\s\S]*\}$/,    // JSON object
  /^\[[\s\S]*\]$/,    // JSON array
  /^https?:\/\//,     // bare URL
];

function shouldCompress(content) {
  if (!content || content.length < MIN_LENGTH) return false;
  const trimmed = content.trim();
  for (const p of SKIP_PATTERNS) {
    if (p.test(trimmed)) return false;
  }
  return true;
}

const handler = async (event) => {
  if (event.type !== "message" || event.action !== "received") return;

  const content = event.context?.content;
  if (!shouldCompress(content)) return;

  const result = compress(content);
  if (result.text.length < content.length && result.text.length > 0) {
    event.context.content = result.text;
    console.log(
      `[prompt-compressor] ${result.origTokens}→${result.compTokens} tokens (-${result.savedPct}%)`
    );
  }
};

export default handler;
