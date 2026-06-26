// Operation Quarantine: Email Sanitizer
import { convert } from "html-to-text";

function stripHtml(html) {
  if (!html || typeof html !== "string") return html || "";
  let cleaned = html
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<[^>]+style\s*=\s*["'][^"']*(?:display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0|font-size\s*:\s*0)[^"']*["'][^>]*>[\s\S]*?<\/[^>]+>/gi, " [HIDDEN CONTENT REMOVED] ")
    .replace(/<[^>]+style\s*=\s*["'][^"']*(?:height\s*:\s*0|width\s*:\s*0)[^"']*["'][^>]*>[\s\S]*?<\/[^>]+>/gi, " [HIDDEN CONTENT REMOVED] ")
    .replace(/<[^>]+style\s*=\s*["'][^"']*color\s*:\s*(?:white|#fff(?:fff)?|transparent|rgba?\([^)]*,\s*0\s*\))[^"']*["'][^>]*>[\s\S]*?<\/[^>]+>/gi, " [HIDDEN TEXT REMOVED] ");
  try {
    cleaned = convert(cleaned, {
      wordwrap: false,
      preserveNewlines: true,
      selectors: [
        { selector: "a", options: { hideLinkHrefIfSameAsText: true } },
        { selector: "img", format: "skip" },
      ],
    });
  } catch {
    cleaned = cleaned.replace(/<[^>]*>/g, " ");
  }
  cleaned = cleaned
    .replace(/[\u200B\u200C\u200D\u2060\uFEFF]/g, "")
    .replace(/\s+/g, " ")
    .trim();
  return cleaned;
}

function extractEmailMeta(rawContent) {
  const meta = { sender: null, subject: null, date: null, to: null };
  const fromMatch = rawContent.match(/(?:^|\n)From:\s*(.+?)(?:\n|$)/i);
  if (fromMatch) meta.sender = fromMatch[1].trim();
  const subjectMatch = rawContent.match(/(?:^|\n)Subject:\s*(.+?)(?:\n|$)/i);
  if (subjectMatch) meta.subject = subjectMatch[1].trim();
  const dateMatch = rawContent.match(/(?:^|\n)Date:\s*(.+?)(?:\n|$)/i);
  if (dateMatch) meta.date = dateMatch[1].trim();
  const toMatch = rawContent.match(/(?:^|\n)To:\s*(.+?)(?:\n|$)/i);
  if (toMatch) meta.to = toMatch[1].trim();
  return meta;
}

function sanitizeEmail(rawContent, isHtml = null) {
  if (isHtml === null) {
    isHtml = /<html|<body|<div|<table|<p\s/i.test(rawContent);
  }
  const meta = extractEmailMeta(rawContent);
  const cleanText = isHtml ? stripHtml(rawContent) : rawContent;
  const hadHiddenContent = cleanText.includes("[HIDDEN CONTENT REMOVED]") ||
                           cleanText.includes("[HIDDEN TEXT REMOVED]");
  return {
    cleanText,
    meta,
    isHtml,
    hadHiddenContent,
    originalLength: rawContent.length,
    cleanLength: cleanText.length,
    compressionRatio: rawContent.length > 0 ? cleanText.length / rawContent.length : 1,
  };
}

export { sanitizeEmail, stripHtml, extractEmailMeta };
