#!/usr/bin/env node

const query = process.argv.slice(2).join(' ').trim();
if (!query) {
  console.error('Usage: node scripts/search-seedance-readme.mjs <keyword>');
  process.exit(1);
}

const sources = [
  'https://raw.githubusercontent.com/YouMind-OpenLab/awesome-seedance-2-prompts/main/README.md',
  'https://raw.githubusercontent.com/YouMind-OpenLab/awesome-seedance-2-prompts/main/README_zh.md'
];

const q = query.toLowerCase();

for (const url of sources) {
  const res = await fetch(url);
  if (!res.ok) {
    console.error(`Failed to fetch ${url}: ${res.status}`);
    continue;
  }
  const text = await res.text();
  const file = url.split('/').pop();
  const sections = text.split(/^### /m).slice(1);
  const matches = [];

  for (const section of sections) {
    const body = '### ' + section;
    if (body.toLowerCase().includes(q)) {
      const title = body.match(/^###\s+(.*)$/m)?.[1]?.trim() || '(untitled)';
      const promptBlock = body.match(/#### 📝 Prompt\n\n```\n([\s\S]*?)\n```/);
      const prompt = promptBlock ? promptBlock[1].trim() : '(no prompt block found)';
      matches.push({ title, prompt: prompt.slice(0, 900) });
    }
  }

  console.log(`\n=== ${file} | ${matches.length} matches for "${query}" ===`);
  for (const [i, m] of matches.slice(0, 8).entries()) {
    console.log(`\n[${i + 1}] ${m.title}\n${m.prompt}\n`);
  }
}
