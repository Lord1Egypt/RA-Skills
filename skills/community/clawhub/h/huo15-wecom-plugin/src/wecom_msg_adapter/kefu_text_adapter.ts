/**
 * Flatten an OpenClaw reply (which may contain markdown) into plain text
 * suitable for the WeCom `kf/send_msg` text channel.
 *
 * kefu's text content field renders literally — `##` becomes `##`, not a
 * heading. The adapter preserves the authoring intent while stripping
 * markup a user would otherwise see as noise.
 */
export function toKefuText(markdown: unknown, maxLength = 4096): string {
  if (markdown == null) return "";
  let text = String(markdown).replace(/\r\n/g, "\n").replace(/\r/g, "\n");

  text = preserveFencedCodeBlocks(text);
  text = convertImages(text);
  text = convertLinks(text);
  text = stripHeadings(text);
  text = stripBlockquotes(text);
  text = stripBold(text);
  text = stripItalic(text);
  text = stripStrikethrough(text);
  text = stripInlineCode(text);
  text = normalizeLists(text);
  text = stripThematicBreaks(text);
  text = stripHtml(text);
  text = cleanupWhitespace(text);

  if (maxLength != null && text.length > maxLength) {
    text = `${text.slice(0, Math.max(0, maxLength - 1))}…`;
  }
  return text;
}

function preserveFencedCodeBlocks(text: string): string {
  return text.replace(/```([a-zA-Z0-9_+\-]*)\n?([\s\S]*?)```/g, (_, _lang: string, code: string) => {
    const body = String(code || "").replace(/^\n+|\n+$/g, "");
    if (!body.trim()) return "";
    return `\n${body}\n`;
  });
}

function convertImages(text: string): string {
  // ![alt](url) — drop the URL; keep the alt text if any.
  return text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt: string, url: string) => {
    const trimmedAlt = alt.trim();
    if (trimmedAlt) return `${trimmedAlt}（图片：${url.trim()}）`;
    return `（图片：${url.trim()}）`;
  });
}

function convertLinks(text: string): string {
  // [label](url) → label (url). Bare URLs keep as-is.
  return text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label: string, url: string) => {
    const trimmedLabel = label.trim();
    const trimmedUrl = url.trim();
    if (!trimmedLabel) return trimmedUrl;
    if (trimmedLabel === trimmedUrl) return trimmedUrl;
    return `${trimmedLabel} (${trimmedUrl})`;
  });
}

function stripHeadings(text: string): string {
  return text.replace(/^\s{0,3}(#{1,6})\s+/gm, "");
}

function stripBlockquotes(text: string): string {
  return text.replace(/^\s{0,3}>\s?/gm, "");
}

function stripBold(text: string): string {
  return text.replace(/\*\*([^*\n]+)\*\*/g, "$1").replace(/__([^_\n]+)__/g, "$1");
}

function stripItalic(text: string): string {
  return text.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1$2").replace(/(^|[^_])_([^_\n]+)_/g, "$1$2");
}

function stripStrikethrough(text: string): string {
  return text.replace(/~~([^~\n]+)~~/g, "$1");
}

function stripInlineCode(text: string): string {
  return text.replace(/`([^`\n]+?)`/g, "$1");
}

function normalizeLists(text: string): string {
  return text
    .replace(/^\s*[-*+]\s+/gm, "• ")
    .replace(/^\s*\d+\.\s+/gm, (match) => match.trim() + " ");
}

function stripThematicBreaks(text: string): string {
  return text.replace(/^\s{0,3}([-*_])\1{2,}\s*$/gm, "");
}

function stripHtml(text: string): string {
  return text.replace(/<\/?[a-zA-Z][^>]*>/g, "");
}

function cleanupWhitespace(text: string): string {
  return text
    .replace(/\n{3,}/g, "\n\n")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/^\s+|\s+$/g, "");
}
