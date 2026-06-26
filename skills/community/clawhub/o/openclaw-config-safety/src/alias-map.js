/**
 * Canonical alias mapping table
 * Source: TOOLS.md model aliases + runtime model registry
 *
 * Format: canonical → [known aliases]
 * Normalizer uses this to detect aliases and surface INFO (read-only)
 */

const ALIAS_MAP = {
  "nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b": [
    "deepseek-r1-32b",
    "deepseek-r1",
    "deepseek-r1-distill-qwen-32b",
    "deepseek-32b",
  ],
  "minimax/MiniMax-M2.7": [
    "minimax-m2.7",
    "m2.7",
    "minimax-m2.7",
    "MiniMax-M2.7",
  ],
  "nvidia/llama-3.2-1b-instruct": [
    "llama-1b",
    "llama3.2-1b",
    "llama-3.2-1b-instruct",
  ],
  "zai/glm-4.7": [
    "glm-4.7",
    "glm4.7",
    "zai-glm-4.7",
  ],
  "zai/glm-5.1": [
    "glm-5.1",
    "glm5.1",
    "glm-5.1-flash",
  ],
  "nvidia/qwen/qwen2.5-coder-32b-instruct": [
    "qwen2.5-coder-32b",
    "qwen-coder-32b",
  ],
  "nvidia/qwen/qwen3-next-80b-a3b-thinking": [
    "qwen3-next-80b",
    "qwen-next-80b",
  ],
  "ibm/granite-34b-code-instruct": [
    "granite-34b",
    "granite-34b-code",
  ],
  "morgan/llama3.1-70b": [
    "llama3.1-70b",
    "llama-70b",
  ],
  "morgan/llama3.1-8b": [
    "llama3.1-8b",
    "llama-8b",
  ],
  "morgan/llama3.1-8b-instruct": [
    "llama3.1-8b-instruct",
  ],
};

/**
 * Reverse lookup: alias → canonical
 * @param {string} alias
 * @returns {string|null} canonical ID or null if not found
 */
function resolveCanonical(alias) {
  if (!alias || typeof alias !== "string") return null;
  const normalized = alias.trim();
  for (const [canonical, aliases] of Object.entries(ALIAS_MAP)) {
    if (aliases.includes(normalized) || canonical === normalized) {
      return canonical;
    }
  }
  return null;
}

/**
 * Detect if a value is a known alias (not a full canonical ID)
 * @param {string} value
 * @returns {boolean}
 */
function isAlias(value) {
  if (!value || typeof value !== "string") return false;
  const canonical = resolveCanonical(value.trim());
  return canonical !== null && canonical !== value.trim();
}

module.exports = { ALIAS_MAP, resolveCanonical, isAlias };
