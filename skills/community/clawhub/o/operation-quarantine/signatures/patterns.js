// ─── Operation Quarantine: Injection Pattern Library ───
// Shared detection patterns for email and skill sanitization

// ─── Direct injection signatures ───
const DIRECT_INJECTION_PATTERNS = [
  // Instruction override attempts
  /ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|guidelines?)/i,
  /disregard\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)/i,
  /forget\s+(all\s+)?(previous|prior|your)\s+(instructions?|prompts?|rules?|context)/i,
  /override\s+(all\s+)?(previous|prior|system)\s+(instructions?|prompts?|rules?)/i,

  // Role hijacking
  /you\s+are\s+now\s+(a|an|in|acting)/i,
  /act\s+as\s+(a|an|if\s+you\s+are)/i,
  /pretend\s+(you\s+are|to\s+be|you're)/i,
  /switch\s+to\s+(developer|admin|root|god|unrestricted)\s+mode/i,
  /enter\s+(developer|admin|DAN|jailbreak)\s+mode/i,
  /you\s+have\s+been\s+(reprogrammed|updated|upgraded)/i,

  // System prompt extraction
  /reveal\s+(your|the|system)\s+(prompt|instructions?|rules?|guidelines?)/i,
  /show\s+(me\s+)?(your|the)\s+(system\s+)?(prompt|instructions?)/i,
  /what\s+are\s+your\s+(instructions?|rules?|guidelines?|system\s+prompt)/i,
  /repeat\s+(your|the)\s+(system\s+)?(prompt|instructions?)/i,
  /print\s+(your|the)\s+(system\s+)?(prompt|instructions?)/i,
  /system\s+prompt/i,

  // Tool/action hijacking
  /execute\s+(the\s+following|this)\s+(command|code|script|function)/i,
  /call\s+(the\s+following|this)\s+(function|tool|api|endpoint)/i,
  /run\s+(the\s+following|this)\s+(command|code|script)/i,
  /send\s+(an?\s+)?(email|message|request)\s+to/i,
  /forward\s+(all|this|these|my)\s+(emails?|messages?|data)/i,
  /forward\s+\w+\s+(?:emails?|messages?|data)\s+to/i,
  /exfiltrate/i,

  // Data exfiltration
  /send\s+(all|any|the)\s+(data|information|content|emails?)\s+to/i,
  /forward\s+(all|any|the)\s+(data|information|content|emails?)\s+to/i,
  /upload\s+(all|any|the)\s+(data|information|content)\s+to/i,
  /post\s+(all|any|the)\s+(data|information|content)\s+to/i,
  /send\s+\w+\s+(?:to|emails?\s+to)\s+\S+@\S+/i,
  /base64\s+encode/i,
  /fetch\s+https?:\/\//i,

  // Memory/context poisoning
  /remember\s+that\s+you/i,
  /from\s+now\s+on\s+(you|always|never)/i,
  /update\s+your\s+(memory|context|instructions?)/i,
  /add\s+this\s+to\s+your\s+(memory|context|instructions?)/i,
  /your\s+new\s+(instructions?|rules?|guidelines?)\s+are/i,
];

// ─── Indirect/stealth injection patterns ───
const STEALTH_PATTERNS = [
  // Hidden text indicators (for HTML emails)
  /color\s*:\s*(white|#fff|#ffffff|transparent|rgba?\([\d\s,]*0\s*\))/i,
  /font-size\s*:\s*0/i,
  /display\s*:\s*none/i,
  /visibility\s*:\s*hidden/i,
  /opacity\s*:\s*0/i,
  /position\s*:\s*absolute.*?left\s*:\s*-\d{4}/i,
  /height\s*:\s*0.*?overflow\s*:\s*hidden/i,

  // Encoded payloads in HTML comments or special tokens
  /<!--[\s\S]*?(ignore|override|instructions|system|prompt)[\s\S]*?-->/i,
  /\[hidden\]/i,
  /\[system\]/i,
  /\[INST\]/i,
  /<<SYS>>/i,
  /<\|im_start\|>/i,
  /<\|endoftext\|>/i,

  // Zero-width / unicode smuggling indicators
  /[\u200B\u200C\u200D\u2060\uFEFF]{3,}/,

  // Suspicious base64 blocks that might contain encoded instructions
  /[A-Za-z0-9+/]{100,}={0,2}/,
];

// ─── Skill-specific patterns (for ClewHub analysis) ───
const SKILL_INJECTION_PATTERNS = [
  // Skills shouldn't reference the agent's core identity/config
  /SOUL\.md/i,
  /IDENTITY\.md/i,
  /USER\.md/i,
  /MEMORY\.md/i,
  /system\s*prompt/i,
  /operating\s*agreement/i,

  // Skills shouldn't try to modify agent behavior globally
  /always\s+(ignore|override|disregard)/i,
  /never\s+follow\s+(your|the|previous)/i,
  /replace\s+your\s+(instructions?|personality|identity)/i,
  /you\s+must\s+(always|never)\s+(from\s+now|going\s+forward)/i,

  // Skills shouldn't request access beyond their scope
  /access\s+(my|the|all)\s+(emails?|contacts?|files?|messages?|calendar)/i,
  /read\s+(my|the|all)\s+(emails?|contacts?|files?|messages?)/i,
  /send\s+(money|payment|bitcoin|crypto|funds)/i,
  /debit\s+card/i,
  /api[_\s]?key/i,
  /auth[_\s]?token/i,
  /password/i,
  /credential/i,
  /private[_\s]?key/i,

  // Skills shouldn't try to phone home to unknown endpoints
  /webhook/i,
  /ngrok/i,
  /requestbin/i,
  /pipedream/i,
  /burpcollaborator/i,
  /interact\.sh/i,
];

// ─── Fuzzy keyword matching (catches typo/unicode evasion) ───
const DANGEROUS_KEYWORDS = [
  "ignore", "bypass", "override", "reveal", "delete",
  "system", "inject", "exploit", "exfiltrate", "escalate",
  "jailbreak", "unrestricted", "unfiltered", "uncensored",
  "sudo", "admin", "root", "superuser", "privilege",
];

function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

function fuzzyMatchKeywords(text) {
  const words = text.toLowerCase().match(/\b\w{4,}\b/g) || [];
  const matches = [];
  for (const word of words) {
    for (const keyword of DANGEROUS_KEYWORDS) {
      const distance = levenshtein(word, keyword);
      const threshold = keyword.length <= 5 ? 1 : 2;
      if (distance > 0 && distance <= threshold) {
        matches.push({ word, matchedKeyword: keyword, distance });
      }
    }
  }
  return matches;
}

// ─── Main analysis function ───
function analyzeText(text, mode = "email") {
  const findings = {
    directInjections: [],
    stealthPatterns: [],
    skillInjections: [],
    fuzzyMatches: [],
    threatScore: 0,
    verdict: "clean",
  };

  // Check direct injection patterns
  for (const pattern of DIRECT_INJECTION_PATTERNS) {
    const match = text.match(pattern);
    if (match) {
      findings.directInjections.push({
        pattern: pattern.source.slice(0, 60),
        matched: match[0],
        index: match.index,
      });
    }
  }

  // Check stealth patterns
  for (const pattern of STEALTH_PATTERNS) {
    const match = text.match(pattern);
    if (match) {
      findings.stealthPatterns.push({
        pattern: pattern.source.slice(0, 60),
        matched: match[0].slice(0, 100),
        index: match.index,
      });
    }
  }

  // Check skill-specific patterns (only in skill mode)
  if (mode === "skill") {
    for (const pattern of SKILL_INJECTION_PATTERNS) {
      const match = text.match(pattern);
      if (match) {
        findings.skillInjections.push({
          pattern: pattern.source.slice(0, 60),
          matched: match[0],
          index: match.index,
        });
      }
    }
  }

  // Fuzzy keyword matching
  findings.fuzzyMatches = fuzzyMatchKeywords(text);

  // ─── Calculate threat score ───
  findings.threatScore += findings.directInjections.length * 30;
  findings.threatScore += findings.stealthPatterns.length * 25;
  findings.threatScore += findings.skillInjections.length * 35;
  findings.threatScore += findings.fuzzyMatches.length * 10;
  findings.threatScore = Math.min(findings.threatScore, 100);

  // Verdict
  if (findings.threatScore >= 50) {
    findings.verdict = "blocked";
  } else if (findings.threatScore >= 20) {
    findings.verdict = "suspicious";
  } else {
    findings.verdict = "clean";
  }

  return findings;
}

export {
  analyzeText,
  fuzzyMatchKeywords,
  DIRECT_INJECTION_PATTERNS,
  STEALTH_PATTERNS,
  SKILL_INJECTION_PATTERNS,
  DANGEROUS_KEYWORDS,
};
