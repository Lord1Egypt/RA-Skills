#!/usr/bin/env node
// Search YouMind grok-imagine prompt library
// Usage: node scripts/search.mjs --q "cinematic" --limit 5 --page 1

const args = process.argv.slice(2);
const getArg = (flag, def) => { const i = args.indexOf(flag); return i !== -1 ? args[i+1] : def; };

const q = getArg('--q', '');
const limit = parseInt(getArg('--limit', '6'));
const page = parseInt(getArg('--page', '1'));
const model = 'grok-imagine';

const res = await fetch('https://youmind.com/youhome-api/video-prompts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Origin': 'https://youmind.com' },
  body: JSON.stringify({ model, page, limit, q: q || undefined }),
});
const data = await res.json();
console.log(JSON.stringify(data, null, 2));
