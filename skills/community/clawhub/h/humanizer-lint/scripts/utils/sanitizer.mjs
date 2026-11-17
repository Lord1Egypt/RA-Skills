const ENTITY = 'TOKEN_ENTITY';

function isCompleteListItem(text) {
  const words = text.match(/[\p{L}\p{N}]+/gu) ?? [];
  return words.length >= 5 && /[.!?]["')\]]?$/.test(text.trim());
}

export function sanitizeMarkdown(input) {
  let text = String(input ?? '').replace(/\r\n?/g, '\n');
  text = text.replace(/^---\s*\n[\s\S]*?\n---\s*(?:\n|$)/, '');
  text = text.replace(/^(?:```|~~~)[^\n]*\n[\s\S]*?^(?:```|~~~)\s*$/gm, '\n');
  text = text.replace(/\[([^\]]+)\]\(https?:\/\/[^\s)]+\)/gi, '$1');
  text = text.replace(/`[^`\n]+`/g, ENTITY);
  text = text.replace(/https?:\/\/[^\s)]+/gi, (match) => {
    const trailing = match.match(/[.!?,;:]+$/u)?.[0] ?? '';
    return `${ENTITY}${trailing}`;
  });

  const sourceLines = text.split('\n');
  const lines = [];
  for (let index = 0; index < sourceLines.length; index += 1) {
    const rawLine = sourceLines[index];
    if (/^\s*#{1,6}\s+/.test(rawLine)) {
      lines.push('');
      continue;
    }
    if (/^\s*\|.*\|\s*$/.test(rawLine)) {
      lines.push('');
      continue;
    }

    let line = rawLine.replace(/^\s*>\s?/, '');
    const list = line.match(/^\s*(?:[-*+]|\d+\.)\s+(.*)$/);
    if (list) {
      let item = list[1].trim();
      let cursor = index + 1;
      while (cursor < sourceLines.length && /^\s{2,}\S/.test(sourceLines[cursor])) {
        item += ` ${sourceLines[cursor].replace(/^\s*>\s?/, '').trim()}`;
        cursor += 1;
      }
      index = cursor - 1;
      line = isCompleteListItem(item) ? item : '';
    }
    lines.push(line.trimEnd());
  }

  return lines.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}
