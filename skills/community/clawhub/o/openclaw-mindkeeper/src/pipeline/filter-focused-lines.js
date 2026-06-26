export function filterFocusedLines(lines, focusTerms = []) {
  const terms = focusTerms
    .map((term) => String(term).trim())
    .filter(Boolean);

  if (terms.length === 0) {
    return lines;
  }

  const regex = new RegExp(terms.map(escapeRegex).join("|"), "i");
  return lines.filter((line) => regex.test(line));
}

function escapeRegex(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
