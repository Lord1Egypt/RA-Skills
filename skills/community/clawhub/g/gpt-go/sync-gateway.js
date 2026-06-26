const fs = require('node:fs');
const path = require('node:path');

const skillFile = path.join(__dirname, 'SKILL.md');
const outFile = path.join(__dirname, 'gateway-prompt.txt');

const md = fs.readFileSync(skillFile, 'utf8');

function pickSection(titleVariants) {
  const lines = md.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim().toLowerCase();
    if (titleVariants.includes(line)) {
      const out = [];
      for (let j = i + 1; j < lines.length; j++) {
        const raw = lines[j];
        if (/^##\s+/.test(raw)) break;
        out.push(raw);
      }
      return out.join('\n').trim();
    }
  }
  return '';
}

const core = pickSection(['## core rule']);
const execBehavior = pickSection(['## execution behavior']);
const style = pickSection(['## communication style']);
const ask = pickSection(['## ask only when needed']);
const pause = pickSection(['## pause boundaries']);

const compact = [core, execBehavior, style, ask, pause]
  .filter(Boolean)
  .join('\n\n')
  .replace(/^-\s+/gm, '- ')
  .trim();

fs.writeFileSync(outFile, compact + '\n');
console.log(`Wrote ${outFile}`);
