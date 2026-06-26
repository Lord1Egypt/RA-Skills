#!/usr/bin/env node
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, basename, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

if (process.argv.includes('--help')) {
  console.log('Usage: node scripts/compile-agents.mjs');
  console.log('');
  console.log('Generates a concise AGENTS.md guide from rules/*.md summaries.');
  process.exit(0);
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');
const rulesDir = join(rootDir, 'rules');
const outFile = join(rootDir, 'AGENTS.md');

const CATEGORY_CONFIG = [
  {
    title: 'Layout & Overflow',
    priority: 'CRITICAL',
    prefixes: ['layout-'],
    note: 'Prevent overlap, clipping, and broken responsive behavior.',
  },
  {
    title: 'Design Tokens',
    priority: 'CRITICAL',
    prefixes: ['token-'],
    note: 'All reusable values must flow through variables and themes.',
  },
  {
    title: 'Anti-AI Aesthetic',
    priority: 'HIGH',
    prefixes: ['aesthetic-'],
    note: 'Avoid generic AI-looking visual patterns and copycat styling.',
  },
  {
    title: 'Component System',
    priority: 'HIGH',
    prefixes: ['component-'],
    note: 'Build reusable primitives and compose via ref + descendants + slot.',
  },
  {
    title: 'Typography',
    priority: 'MEDIUM',
    prefixes: ['typo-'],
    note: 'Use readable scale, rhythm, and hierarchy for all text content.',
  },
  {
    title: 'Color System',
    priority: 'MEDIUM',
    prefixes: ['color-'],
    note: 'Enforce semantic color usage, accessibility, and dark mode parity.',
  },
  {
    title: 'Spacing System',
    priority: 'MEDIUM',
    prefixes: ['spacing-'],
    note: 'Keep spacing decisions consistent and token-driven.',
  },
  {
    title: 'Showcase & Style Guide',
    priority: 'MEDIUM',
    prefixes: ['showcase-'],
    note: 'Use a pre-design process and finish with system-level QA checks.',
  },
];

function parseFrontmatter(raw) {
  const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!fmMatch) return { meta: {}, body: raw };

  const meta = {};
  for (const line of fmMatch[1].split('\n')) {
    const match = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (match) meta[match[1]] = match[2].trim();
  }

  return { meta, body: raw.slice(fmMatch[0].length) };
}

function cleanLine(line) {
  return line
    .replace(/\s+/g, ' ')
    .replace(/`/g, '')
    .replace(/\*\*/g, '')
    .replace(/^[-*]\s*/, '')
    .trim();
}

function extractSummary(body) {
  const lines = body.split('\n');
  const collected = [];
  let inCode = false;

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (line.startsWith('```')) {
      inCode = !inCode;
      continue;
    }
    if (inCode) continue;
    if (!line) {
      if (collected.length) break;
      continue;
    }
    if (line.startsWith('#')) continue;
    if (line.startsWith('**Incorrect') || line.startsWith('**Correct')) break;

    const normalized = cleanLine(line);
    if (!normalized) continue;
    collected.push(normalized);
    if (collected.join(' ').length > 190) break;
  }

  if (!collected.length) return 'See rule file for detailed constraints and examples.';

  let summary = collected.join(' ');
  summary = summary.replace(/\s+/g, ' ').trim();
  if (summary.length > 170) summary = `${summary.slice(0, 167).trim()}...`;
  return summary;
}

function titleFromFile(fileName) {
  return basename(fileName, '.md')
    .split('-')
    .map(x => x.charAt(0).toUpperCase() + x.slice(1))
    .join(' ');
}

const rules = readdirSync(rulesDir)
  .filter(f => f.endsWith('.md'))
  .sort()
  .map(file => {
    const raw = readFileSync(join(rulesDir, file), 'utf8');
    const { meta, body } = parseFrontmatter(raw);
    return {
      file,
      title: meta.title || titleFromFile(file),
      impact: meta.impact || 'MEDIUM',
      summary: extractSummary(body),
    };
  });

function renderCategoryTable(category) {
  const categoryRules = rules.filter(rule =>
    category.prefixes.some(prefix => rule.file.startsWith(prefix)),
  );

  const lines = [
    `### ${category.title}`,
    `> Priority: **${category.priority}** · ${category.note}`,
    '',
    '| Rule | File | Summary |',
    '|------|------|---------|',
  ];

  for (const rule of categoryRules) {
    lines.push(
      `| ${rule.title} | \`rules/${rule.file}\` | ${rule.summary} |`,
    );
  }

  lines.push('');
  return lines.join('\n');
}

const doc = [
  '# Pencil Skill — Agent Guide',
  '',
  '> This document guides AI agents in creating and editing `.pen` design files.',
  '> For full rule details, examples, and edge cases, see individual files in `rules/`.',
  '',
  '## Purpose & Scope',
  '',
  '- This is a **guide document**, not a full rule compilation.',
  '- Use it for fast orientation, then open each rule file for implementation details.',
  `- Current rule count: **${rules.length}** files across 8 categories.`,
  '- Source of truth: `rules/*.md`.',
  '',
  '## Quick Start',
  '',
  '1. Read current structure: `node scripts/read-tree.mjs <file.pen> --depth 2`',
  '2. Search reusable components first: `node scripts/search-nodes.mjs <file.pen> --reusable`',
  '3. Review variables/themes: `node scripts/get-variables.mjs <file.pen>`',
  '4. Apply edits in batches: `node scripts/batch-design.mjs <file.pen> --ops ...`',
  '5. Validate immediately: `node scripts/validate-pen.mjs <file.pen>`',
  '',
  '## Standard Editing Workflow',
  '',
  '```bash',
  '# 1) Inspect',
  'node scripts/read-tree.mjs assets/example-card.pen --depth 2',
  '',
  '# 2) Find reusable parts',
  'node scripts/search-nodes.mjs assets/example-card.pen --reusable',
  '',
  '# 3) Edit',
  "node scripts/batch-design.mjs assets/example-card.pen --ops '[{\"op\":\"update\",\"id\":\"title\",\"props\":{\"content\":\"Updated\"}}]'",
  '',
  '# 4) Validate',
  'node scripts/validate-pen.mjs assets/example-card.pen',
  '```',
  '',
  '## Critical Rules (Must Follow)',
  '',
  ...CATEGORY_CONFIG.map(renderCategoryTable),
  '## 5 Critical Rules (Never Violate)',
  '',
  '1. **`textGrowth` required** — Set `textGrowth` before using width/height behavior on text nodes.',
  '2. **`ref` target must exist** — Every `ref` must point to an existing reusable component ID.',
  '3. **No duplicate IDs** — Every node ID must be unique inside a `.pen` file.',
  '4. **Validate after every edit** — Always run `node scripts/validate-pen.mjs` before finishing.',
  '5. **Component reuse first** — Search existing reusable components before creating new ones.',
  '',
  '## Property Aliases',
  '',
  '- `fill` / `fills` — both accepted',
  '- `stroke` / `strokes` — both accepted',
  '- `effect` / `effects` — both accepted',
  '',
  '## CLI Tools Reference',
  '',
  '### Read Tools',
  '',
  '| Script | Purpose | Usage |',
  '|--------|---------|-------|',
  '| `read-tree.mjs` | Print node tree structure | `node scripts/read-tree.mjs file.pen [--depth 2] [--id nodeId]` |',
  '| `search-nodes.mjs` | Search nodes/components | `node scripts/search-nodes.mjs file.pen --type frame [--reusable] [--name regex]` |',
  '| `get-variables.mjs` | View variables/themes | `node scripts/get-variables.mjs file.pen [--format json]` |',
  '| `find-space.mjs` | Find empty-space coordinates | `node scripts/find-space.mjs file.pen --width 300 --height 200` |',
  '',
  '### Write Tools',
  '',
  '| Script | Purpose | Usage |',
  '|--------|---------|-------|',
  '| `batch-design.mjs` | Insert/update/delete/move/copy nodes | `node scripts/batch-design.mjs file.pen --ops \"[...]\"` |',
  '| `replace-props.mjs` | Bulk property replacement | `node scripts/replace-props.mjs file.pen --match \"{...}\" --replace \"{...}\"` |',
  '| `set-variables.mjs` | Add/update variables | `node scripts/set-variables.mjs file.pen --var \"name=type:value\"` |',
  '',
  '### Validation Tool',
  '',
  '| Script | Purpose | Usage |',
  '|--------|---------|-------|',
  '| `validate-pen.mjs` | Structural validation + lint | `node scripts/validate-pen.mjs file.pen` |',
  '',
  '## Schema Quick Reference',
  '',
  '| Node Type | Required Fields | Important Notes |',
  '|-----------|------------------|-----------------|',
  '| Root Document | `version`, `children` | `themes` and `variables` optional but recommended. |',
  '| `frame` | `type`, `id` | Use `layout` (`vertical`/`horizontal`) for container behavior; supports `slot`. |',
  '| `group` | `type`, `id` | Visual grouping only; avoid for layout logic. |',
  '| `text` | `type`, `id`, `content` | Set `textGrowth` before fixed sizing behavior. |',
  '| `rectangle` | `type`, `id` | Supports fill/stroke/effects; use tokens for values. |',
  '| `ellipse` | `type`, `id` | Use tokens for size and color; keep naming semantic. |',
  '| `line` | `type`, `id` | Prefer tokenized stroke thickness/color. |',
  '| `polygon` | `type`, `id` | Keep geometry and style tokenized. |',
  '| `path` | `type`, `id` | Validate path edits after any scripted change. |',
  '| `icon_font` | `type`, `id` | Use supported families only (lucide, feather, Material Symbols, phosphor). |',
  '| `ref` | `type`, `id`, `ref` | `ref` value must target an existing reusable component ID. |',
  '| `note` / `prompt` / `context` | `type`, `id` | Use for annotations and guidance, not visual structure. |',
  '',
  '## Batch Operation Reference',
  '',
  '| Operation | Required Keys | Description |',
  '|-----------|----------------|-------------|',
  '| `insert` | `op`, `parentId`, `node` | Insert a new node into parent children. |',
  '| `update` | `op`, `id`, `props` | Deep-merge patch into existing node. |',
  '| `delete` | `op`, `id` | Remove node and descendants. |',
  '| `move` | `op`, `id`, `toParentId` | Move node to another parent (`index` optional). |',
  '| `copy` | `op`, `id`, `newId` | Duplicate node tree; ensure IDs remain unique. `toParentId` optional (defaults to `root`). |',
  '',
  '## Validation Checklist',
  '',
  '- [ ] Root has `version` and `children`',
  '- [ ] No duplicate IDs',
  '- [ ] No `/` in node IDs',
  '- [ ] Every `ref` points to an existing reusable component',
  '- [ ] `text` nodes with width/height behavior have `textGrowth`',
  '- [ ] Variable references (`$...`) resolve to actual keys',
  '- [ ] `node scripts/validate-pen.mjs <file.pen>` passes',
  '',
  '## References',
  '',
  '- Schema: `references/pen-schema.json`',
  '- Types: `references/pen-types.ts`',
  '- Mapping: `references/pen-to-tailwind.md`',
  '- Patterns: `references/component-patterns.md`',
  '- Example: `assets/example-card.pen`',
  '',
  '---',
  '',
  'Need full details for any rule? Open the corresponding file in `rules/`.',
].join('\n');

writeFileSync(outFile, `${doc}\n`, 'utf8');
console.log(`Generated AGENTS.md guide with ${rules.length} summarized rules.`);
