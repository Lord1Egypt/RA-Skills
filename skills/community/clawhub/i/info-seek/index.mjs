// DeepSeek Harness skill bundle for infoseek.
// Reads this repo's SKILL.md at runtime and registers it as a runtime skill,
// so the single SKILL.md stays the source of truth.
import { readFileSync } from 'node:fs'

const raw = readFileSync(new URL('./SKILL.md', import.meta.url), 'utf8')
const fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/)
if (!fm) throw new Error('SKILL.md frontmatter missing or malformed')
const meta = {}
for (const line of fm[1].split('\n')) {
  const i = line.indexOf(':')
  if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim()
}
if (!meta.name || !meta.description) {
  throw new Error('SKILL.md frontmatter requires name and description')
}

export const name = meta.name
export const inject = ['skills']

export function apply(ctx) {
  const disposer = ctx.skills.register({
    name: meta.name,
    description: meta.description,
    source: 'bundled',
    content: fm[2].trim(),
  })
  ctx.on('dispose', disposer)
}
