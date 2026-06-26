export function normalizeLine(line) {
  return line
    .trim()
    .replace(/^\[\[reply_to_current\]\]\s*/i, "")
    .replace(/^\[\[[^\]]+\]\]\s*/i, "")
    .replace(/^\[[A-Za-z]{3}\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+UTC\]\s*/, "")
    .replace(/^([-*]\s+)+/, "")
    .replace(/^#{1,6}\s+/, "")
    .replace(/`/g, "")
    .trim();
}

export function toLines(text) {
  return text
    .split(/\r?\n/)
    .map((line) => normalizeLine(line))
    .filter(Boolean);
}

export function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

export function clip(items, limit) {
  return items.slice(0, limit);
}
