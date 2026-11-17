/**
 * core/fingerprints — AI-tool fingerprints (language-agnostic).
 *
 * Migrated verbatim from avoid-ai-writing. Three near-definitive AI-origin
 * signals: unfilled placeholders, chatbot citation-markup leaks, AI-tool UTM
 * tracking params. Each is a fingerprint — single hit is strong evidence the
 * text was copy-pasted from a specific chat tool, regardless of language.
 *
 * Adapted from Aboudjem/humanizer-skill P33-P35.
 */
'use strict';

// Unfilled slot-fill placeholders. Catches the canonical "[Your Name]" family
// plus dated stubs and HTML/MD comments with placeholder verbs.
const AI_PLACEHOLDERS = [
  /\[(?:Your|Insert|Add|Enter|Describe|Specify|Choose|Pick)[^\]\n]{1,80}\]/gi,
  /\[(?:Recipient|Sender|Topic|Subject|Salutation|Closing|Position|Department|Project Name|Company Name|Date)(?:\s+[^\]\n]{0,60})?\]/gi,
  /\[(?:INSERT|FILL\s+IN|ADD|TODO|TBD|PLACEHOLDER)[^\]\n]{0,80}\]/g,
  /\b(?:19|20)\d{2}-XX-XX\b/g,
  /\bXX\/XX\/(?:19|20)\d{2}\b/g,
  /<!--\s*(?:add|fill\s+in|insert|todo|placeholder)[^>]{0,120}-->/gi,
];

// Chatbot citation/markup tokens that leak through copy-paste.
const AI_CITATION_MARKUP = [
  /\bcite(?:turn|news|search|navigation)\d+(?:search|turn|news|navigation)\d+/gi,
  /contentReference\s*\[oaicite:[^\]]+\]\s*\{[^}]*\}/gi,
  /\boai_citation\b/gi,
  /\[attached_file:\d+\]/gi,
  /\bgrok_card\b/gi,
];

// UTM/tracking parameters auto-appended by AI tools to URLs they generate.
const AI_UTM_SOURCE = [
  /[?&]utm_source=(?:chatgpt|openai|copilot|claude|grok|gemini|perplexity)(?:\.com|\.ai)?\b/gi,
  /[?&]referrer=(?:chatgpt|copilot|grok|claude|gemini|perplexity)\.(?:com|ai)\b/gi,
];

module.exports = {
  AI_PLACEHOLDERS,
  AI_CITATION_MARKUP,
  AI_UTM_SOURCE,
};
