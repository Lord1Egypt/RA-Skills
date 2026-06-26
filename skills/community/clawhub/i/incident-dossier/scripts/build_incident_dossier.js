const fs = require('fs');
const path = require('path');

function arg(name) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : null;
}
function args(name) {
  const out = [];
  for (let i = 0; i < process.argv.length; i++) if (process.argv[i] === name && process.argv[i + 1]) out.push(process.argv[i + 1]);
  return out;
}
function readText(p) { return fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''); }
function tryJson(text) { try { return JSON.parse(text); } catch { return null; } }
function readStructured(p) {
  const text = readText(p);
  if (p.endsWith('.jsonl')) {
    return text.split(/\r?\n/).map(s => s.trim()).filter(Boolean).map(line => tryJson(line) || { raw: line });
  }
  return tryJson(text) ?? text;
}
function collectEvents(value, source, acc) {
  if (Array.isArray(value)) return value.forEach(v => collectEvents(v, source, acc));
  if (!value || typeof value !== 'object') return;
  const candidate = { source, ts: value.ts ?? value.created_at ?? value.timestamp ?? null, kind: value.kind ?? value.status ?? value.event ?? 'record', job_id: value.job_id ?? null };
  if (candidate.ts || candidate.kind || candidate.job_id) acc.push(candidate);
  for (const v of Object.values(value)) {
    if (Array.isArray(v) || (v && typeof v === 'object')) collectEvents(v, source, acc);
  }
}
function main() {
  const inputs = args('--input');
  const out = arg('--out');
  if (!inputs.length || !out) {
    console.error('Usage: node build_incident_dossier.js --input <path> [--input <path> ...] --out <path>');
    process.exit(1);
  }
  const events = [];
  const evidence = [];
  for (const input of inputs) {
    const abs = path.resolve(input);
    const structured = readStructured(abs);
    evidence.push({ path: abs, kind: Array.isArray(structured) ? 'array/jsonl' : typeof structured });
    collectEvents(structured, abs, events);
  }
  events.sort((a, b) => (a.ts ?? 0) - (b.ts ?? 0));
  const topKinds = Object.entries(events.reduce((m, e) => (m[e.kind] = (m[e.kind] || 0) + 1, m), {})).sort((a,b)=>b[1]-a[1]).slice(0, 8);
  const lines = [];
  lines.push('# Incident Dossier', '');
  lines.push('## Summary', `- Evidence files: ${evidence.length}`, `- Parsed event count: ${events.length}`, `- Dominant signals: ${topKinds.map(([k,v]) => `${k} (${v})`).join(', ') || 'none'}`, '');
  lines.push('## Evidence');
  for (const item of evidence) lines.push(`- ${item.path} — ${item.kind}`);
  lines.push('', '## Timeline');
  if (!events.length) lines.push('- No structured events extracted.');
  else for (const e of events.slice(0, 50)) lines.push(`- ${e.ts ?? 'no-ts'} · ${e.kind} · ${e.job_id ?? 'no-job-id'} · ${path.basename(e.source)}`);
  lines.push('', '## Hypotheses', '- Inspect dominant event kinds and concentration points above.', '- Compare timeline gaps and duplicate signals before claiming root cause.', '', '## Next actions', '- Verify the highest-frequency event family against raw source lines.', '- Confirm whether the incident is ongoing or purely historical.');
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  fs.writeFileSync(path.resolve(out), lines.join('\n'), 'utf8');
  process.stdout.write(JSON.stringify({ ok: true, out: path.resolve(out), events: events.length, evidence: evidence.length }, null, 2) + '\n');
}
main();
