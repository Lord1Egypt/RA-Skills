import type { Edict } from './types.js';

/**
 * Plain text renderer: one edict per line with inline metadata.
 */
export function renderPlain(edicts: Edict[]): string {
  if (edicts.length === 0) return '';

  return edicts
    .map((e) => {
      const meta = [`[${e.confidence}]`, e.category];
      if (e.tags.length > 0) meta.push(e.tags.join(', '));
      return `- ${e.text} (${meta.join(', ')})`;
    })
    .join('\n');
}

/**
 * Markdown renderer: grouped by category with headers.
 */
export function renderMarkdown(edicts: Edict[]): string {
  if (edicts.length === 0) return '_No edicts._\n';

  const groups = new Map<string, Edict[]>();
  for (const e of edicts) {
    const list = groups.get(e.category) ?? [];
    list.push(e);
    groups.set(e.category, list);
  }

  const lines: string[] = [`# Edicts (${edicts.length} items)\n`];

  for (const [category, items] of groups) {
    lines.push(`## ${category}\n`);
    for (const e of items) {
      const badges: string[] = [`${e.confidence}`];
      if (e.expiresAt) badges.push(`expires: ${e.expiresAt}`);
      lines.push(`- ${e.text} _(${badges.join(', ')})_`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

/**
 * JSON renderer: clean array of edicts for programmatic consumption.
 */
export function renderJson(edicts: Edict[]): string {
  const clean = edicts.map(({ _tokens: _ignored, ...rest }) => rest);
  return JSON.stringify(clean, null, 2);
}
