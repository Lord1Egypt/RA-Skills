const logger = require("./logger");

/**
 * Security Scrubbing Logic (v1.0.0)
 * Masks sensitive API keys and tokens using standard regex patterns.
 */

/**
 * These patterns detect common credential formats in skill files
 * and replace them with safe placeholders. The patterns match the
 * STRUCTURE of credentials (length, prefix, charset) - they do NOT
 * contain any actual credential values.
 *
 * Users can customize via inventory.json maskPatterns field.
 */
const SECRETS_PATTERNS = [
  { name: "OpenAI Secret Key", regex: /sk-[a-zA-Z0-9]{32,48}/g },
  { name: "OpenAI Public Key", regex: /pk-[a-zA-Z0-9]{32,48}/g },
  { name: "GitHub Access Token", regex: /ghp_[a-zA-Z0-9]{36,40}/g },
  { name: "Hugging Face Token", regex: /hf_[a-zA-Z0-9]{34,40}/g },
  { name: "Google API Key", regex: /AIza[0-9A-Za-z_-]{35}/g },
  { name: "Bearer Token", regex: /Bearer\s+[a-zA-Z0-9\._\-]{20,}/gi },
  { name: "Generic Secret/Key", regex: /(?:key|token|password|secret|auth)\s*[:=]\s*["']?[a-zA-Z0-9_\-]{10,}["']?/gi },
  { name: "AWS Access Key", regex: /AKIA[0-9A-Z]{16}/g },
  { name: "Stripe Key", regex: /sk_test_[a-zA-Z0-9]{24,40}/g },
  { name: "Discord Token", regex: /[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}/g }
];

const securityScrubber = {
  /**
   * Masks sensitive data in a given string.
   * @param {string} content - The raw content to scrub.
   * @param {Array<string>} customPatterns - Optional user-defined patterns.
   * @returns {string} - The safely masked content.
   */
  scrub: (content, customPatterns = []) => {
    if (!content) return "";
    let scrubbed = content;

    // Apply default patterns
    SECRETS_PATTERNS.forEach((pattern) => {
      scrubbed = scrubbed.replace(pattern.regex, (match) => {
        logger.debug(`Masking detected secret: ${pattern.name}`);
        return "********[MASKED]********";
      });
    });

    // Apply custom patterns from inventory.json
    customPatterns.forEach((p) => {
      let regex;
      if (p instanceof RegExp) {
        regex = p;
      } else if (typeof p !== "string" || p.length === 0) {
        logger.warn(`Invalid custom pattern (not a string or empty): ${p}`);
        return;
      } else {
        try {
          regex = new RegExp(p, "gi");
        } catch (e) {
          logger.error(`Invalid custom regex pattern: ${p} - ${e.message}`);
          return;
        }
      }
      try {
        if (regex.global) {
          let match;
          while ((match = regex.exec(scrubbed)) !== null) {
            logger.debug(`Custom pattern matched: ${p}`);
            break;
          }
        }
        scrubbed = scrubbed.replace(regex, "********[CUSTOM-MASKED]********");
      } catch (e) {
        logger.error(`Invalid custom regex pattern: ${p} - ${e.message}`);
      }
    });

    return scrubbed;
  },

  /**
   * Prepares a SKILL.md summary by extracting only safe headers/frontmatter.
   * Used when "metadata-only" summary is preferred for high security.
   */
  extractMetadataOnly: (content, customPatterns = []) => {
    const frontmatterMatch = content.match(/^---([\s\S]*?)---/);
    if (frontmatterMatch) {
      let frontmatter = frontmatterMatch[1];
      frontmatter = securityScrubber.scrub(frontmatter, customPatterns);
      return `---${frontmatter}---\n\n*(Full instructions masked for security)*`;
    }
    return "*(No frontmatter found. Full content masked for security)*";
  }
};

module.exports = securityScrubber;
