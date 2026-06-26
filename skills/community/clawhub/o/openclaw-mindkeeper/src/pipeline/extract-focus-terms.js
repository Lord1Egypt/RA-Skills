const STOPWORDS = new Set([
  "a", "an", "and", "the", "for", "from", "into", "your", "this", "that", "with", "without",
  "daily", "brief", "mindkeeper", "turns", "memory", "clarity", "owner", "report", "summary",
  "de", "la", "si", "sau", "din", "pentru", "cu", "fara", "azi", "maine", "astazi",
  "focus", "today", "real", "work", "remaining", "open", "loops", "still", "needs",
  "user", "assistant", "next", "turn", "likely", "request", "asked", "complained", "acknowledged",
]);

export function extractFocusTerms({ explicitTerms = [], title = "", prompt = "" } = {}) {
  const explicit = explicitTerms.map((term) => String(term).trim().toLowerCase()).filter(Boolean);
  if (explicit.length > 0) {
    return [...new Set(explicit)];
  }

  const text = `${title} ${prompt}`.toLowerCase();
  const tokens = text
    .split(/[^\p{L}\p{N}-]+/u)
    .map((token) => token.trim())
    .filter((token) => token.length >= 4)
    .filter((token) => !STOPWORDS.has(token));

  return [...new Set(tokens)].slice(0, 6);
}
