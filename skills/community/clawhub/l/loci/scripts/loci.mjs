#!/usr/bin/env node
/**
 * loci — Structured memory with decay, domains, and links for AI agents.
 *
 * Usage:
 *   loci.mjs store <domain> <content> [--tag TAG ...] [--link ID ...]
 *   loci.mjs recall <query> [--domain DOMAIN] [--top N]
 *   loci.mjs walk [--decay RATE]
 *   loci.mjs prune [--threshold FLOAT] [--dry-run]
 *   loci.mjs status
 *   loci.mjs inspect <id>
 *   loci.mjs link <id1> <id2>
 *   loci.mjs domains [--add NAME --capacity N] [--remove NAME]
 *   loci.mjs export [--format md|json]
 *   loci.mjs init [--template PATH] [--force]
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { randomBytes, createHash } from 'crypto';

// ─── Defaults ───

const DEFAULT_PALACE = join(homedir(), '.openclaw', 'workspace', 'loci_palace.json');

// ─── Helpers ───

function loadPalace(path) {
  // Try .json path
  const jsonPath = path.endsWith('.yaml') ? path.replace('.yaml', '.json') : path;
  if (existsSync(jsonPath)) {
    return JSON.parse(readFileSync(jsonPath, 'utf8'));
  }
  if (existsSync(path)) {
    try { return JSON.parse(readFileSync(path, 'utf8')); } catch {}
  }
  return null;
}

function savePalace(data, path) {
  const jsonPath = path.endsWith('.yaml') ? path.replace('.yaml', '.json') : path;
  writeFileSync(jsonPath, JSON.stringify(data, null, 2), 'utf8');
}

function genId() {
  const now = Date.now().toString();
  const rand = randomBytes(8);
  const hash = createHash('sha256').update(now).update(rand).digest('hex');
  return 'e' + hash.slice(0, 7);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function daysSince(dateStr) {
  try {
    const d = new Date(dateStr);
    return Math.max(0, Math.floor((Date.now() - d.getTime()) / 86400000));
  } catch { return 0; }
}

function computeWeight(memory, decayRate = 0.05) {
  const base = memory.base_weight ?? 1.0;
  const days = daysSince(memory.last_accessed ?? today());
  return base * Math.exp(-decayRate * days);
}

function matchScore(query, memory) {
  const terms = new Set(query.toLowerCase().split(/\s+/).filter(Boolean));
  if (terms.size === 0) return 0;
  const text = (memory.content || '').toLowerCase() + ' ' + (memory.tags || []).join(' ').toLowerCase();
  let matches = 0;
  for (const t of terms) { if (text.includes(t)) matches++; }
  return matches / terms.size;
}

function bar(filled, total, width = 20) {
  const n = Math.round((filled / total) * width);
  return '█'.repeat(n) + '░'.repeat(width - n);
}

// ─── Arg parsing ───

function parseArgs(argv) {
  const args = { _: [], palace: DEFAULT_PALACE };
  let i = 0;
  const tags = [];
  const links = [];
  while (i < argv.length) {
    const a = argv[i];
    if (a === '--palace' && argv[i + 1]) { args.palace = argv[++i]; }
    else if (a === '--tag' && argv[i + 1]) { tags.push(argv[++i]); }
    else if (a === '--link' && argv[i + 1]) { links.push(argv[++i]); }
    else if (a === '--domain' && argv[i + 1]) { args.domain = argv[++i]; }
    else if (a === '--top' && argv[i + 1]) { args.top = parseInt(argv[++i], 10); }
    else if (a === '--decay' && argv[i + 1]) { args.decay = parseFloat(argv[++i]); }
    else if (a === '--threshold' && argv[i + 1]) { args.threshold = parseFloat(argv[++i]); }
    else if (a === '--format' && argv[i + 1]) { args.format = argv[++i]; }
    else if (a === '--template' && argv[i + 1]) { args.template = argv[++i]; }
    else if (a === '--add' && argv[i + 1]) { args.add = argv[++i]; }
    else if (a === '--remove' && argv[i + 1]) { args.remove = argv[++i]; }
    else if (a === '--capacity' && argv[i + 1]) { args.capacity = parseInt(argv[++i], 10); }
    else if (a === '--dry-run') { args.dryRun = true; }
    else if (a === '--force') { args.force = true; }
    else if (!a.startsWith('-')) { args._.push(a); }
    i++;
  }
  if (tags.length) args.tags = tags;
  if (links.length) args.links = links;
  return args;
}

// ─── Commands ───

function cmdInit(args) {
  const path = args.palace;
  const jsonPath = path.endsWith('.yaml') ? path.replace('.yaml', '.json') : path;
  if (existsSync(jsonPath) && !args.force) {
    console.log(`⚠️  Palace already exists: ${jsonPath}`);
    console.log('   Use --force to reinitialize (this will erase all memories!)');
    return;
  }

  let data;
  if (args.template && existsSync(args.template)) {
    data = JSON.parse(readFileSync(args.template, 'utf8'));
  } else {
    data = {
      version: 1,
      created: today(),
      last_walk: null,
      domains: {
        work:        { name: '工作', icon: '💼', capacity: 25, description: 'Projects, decisions, technical context' },
        knowledge:   { name: '知识', icon: '📚', capacity: 30, description: 'Learnings, articles, concepts, insights' },
        people:      { name: '人际', icon: '👥', capacity: 20, description: 'People, relationships, conversations' },
        tools:       { name: '工具', icon: '🔧', capacity: 20, description: 'Environment, configs, commands, troubleshooting' },
        preferences: { name: '偏好', icon: '🎯', capacity: 15, description: 'User habits, likes, dislikes, style' },
        archive:     { name: '归档', icon: '📦', capacity: 50, description: 'Historical, low-frequency, but worth keeping' },
      },
      memories: [],
    };
  }

  savePalace(data, path);
  console.log(`✅ Palace initialized: ${jsonPath}`);
  console.log(`   Domains: ${Object.keys(data.domains).join(', ')}`);
}

function cmdStore(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const domain = args._[1];
  const content = args._[2];
  if (!domain || !content) { console.log('Usage: loci store <domain> <content> [--tag TAG ...]'); return; }
  if (!palace.domains[domain]) {
    console.log(`❌ Unknown domain: ${domain}`);
    console.log(`   Available: ${Object.keys(palace.domains).join(', ')}`);
    return;
  }

  const domainMems = palace.memories.filter(m => m.domain === domain);
  const cap = palace.domains[domain].capacity ?? 25;
  if (domainMems.length >= cap) {
    const weights = domainMems.map(m => [m.id, computeWeight(m)]).sort((a, b) => a[1] - b[1]);
    console.log(`⚠️  Domain '${domain}' is full (${domainMems.length}/${cap})`);
    console.log(`   Weakest memory: ${weights[0][0]} (weight: ${weights[0][1].toFixed(2)})`);
    console.log(`   Run: loci prune --domain ${domain}  to make room`);
    return;
  }

  const memory = {
    id: genId(),
    domain,
    content,
    tags: args.tags || [],
    links: args.links || [],
    base_weight: 1.0,
    created: today(),
    last_accessed: today(),
    access_count: 0,
  };

  palace.memories.push(memory);
  savePalace(palace, args.palace);

  const icon = palace.domains[domain].icon ?? '📝';
  console.log(`${icon} Stored in [${domain}]: ${memory.id}`);
  console.log(`   ${content.slice(0, 80)}${content.length > 80 ? '...' : ''}`);
  if (memory.tags.length) console.log(`   Tags: ${memory.tags.join(', ')}`);
}

function cmdRecall(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const query = args._[1];
  if (!query) { console.log('Usage: loci recall <query> [--domain DOMAIN] [--top N]'); return; }
  const topN = args.top || 5;

  let memories = palace.memories;
  if (args.domain) memories = memories.filter(m => m.domain === args.domain);

  const scored = [];
  for (const m of memories) {
    const ks = matchScore(query, m);
    const w = computeWeight(m);
    const combined = ks * 0.7 + w * 0.3;
    if (ks > 0) scored.push({ m, combined, ks, w });
  }
  scored.sort((a, b) => b.combined - a.combined);
  const results = scored.slice(0, topN);

  if (!results.length) { console.log(`🔍 No memories match: "${query}"`); return; }

  console.log(`🔍 Found ${results.length} memories for "${query}":\n`);
  for (const { m, ks, w } of results) {
    const icon = palace.domains[m.domain]?.icon ?? '📝';
    const tags = m.tags?.length ? ` [${m.tags.join(', ')}]` : '';
    const age = daysSince(m.created);
    console.log(`  ${icon} ${m.id} (${m.domain}) — relevance:${(ks * 100).toFixed(0)}% weight:${w.toFixed(2)}`);
    console.log(`     ${m.content.slice(0, 100)}${m.content.length > 100 ? '...' : ''}`);
    console.log(`     ${tags} | ${age}d ago | accessed ${m.access_count ?? 0}x`);
    if (m.links?.length) console.log(`     🔗 ${m.links.join(', ')}`);
    console.log();

    m.last_accessed = today();
    m.access_count = (m.access_count ?? 0) + 1;
  }
  savePalace(palace, args.palace);
}

function cmdWalk(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const decayRate = args.decay ?? 0.05;
  const fading = [], healthy = [], strong = [];

  console.log('🏛️  Palace Walk\n');

  for (const [dk, di] of Object.entries(palace.domains)) {
    const mems = palace.memories.filter(m => m.domain === dk);
    const cap = di.capacity ?? 25;
    const icon = di.icon ?? '📝';

    if (!mems.length) { console.log(`  ${icon} ${di.name} — empty (0/${cap})`); continue; }

    const weights = mems.map(m => computeWeight(m, decayRate));
    const avg = weights.reduce((a, b) => a + b, 0) / weights.length;
    const fadingN = weights.filter(w => w < 0.3).length;
    const usage = (mems.length / cap * 100).toFixed(0);
    const status = avg > 0.6 ? '🟢' : avg > 0.3 ? '🟡' : '🔴';

    console.log(`  ${icon} ${di.name} — ${mems.length}/${cap} (${usage}%) ${status} avg:${avg.toFixed(2)}`);
    if (fadingN > 0) console.log(`     ⚠️  ${fadingN} fading memories (weight < 0.3)`);

    for (let i = 0; i < mems.length; i++) {
      if (weights[i] < 0.3) fading.push(mems[i]);
      else if (weights[i] > 0.7) strong.push(mems[i]);
      else healthy.push(mems[i]);
    }
  }

  console.log(`\n📊 Summary: ${strong.length} strong | ${healthy.length} healthy | ${fading.length} fading`);
  console.log(`   Total: ${palace.memories.length} memories across ${Object.keys(palace.domains).length} domains`);

  if (fading.length) {
    console.log('\n⚠️  Fading memories (consider pruning or refreshing):');
    for (const m of fading.slice(0, 5)) {
      console.log(`   - ${m.id}: ${m.content.slice(0, 60)}...`);
    }
  }

  palace.last_walk = today();
  savePalace(palace, args.palace);
}

function cmdPrune(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const threshold = args.threshold ?? 0.2;
  const dryRun = args.dryRun;

  const toPrune = [];
  for (const m of palace.memories) {
    const w = computeWeight(m);
    if (w < threshold && (!args.domain || m.domain === args.domain)) {
      toPrune.push({ m, w });
    }
  }

  if (!toPrune.length) { console.log(`✅ Nothing to prune (threshold: ${threshold})`); return; }

  console.log(`${dryRun ? '🔍 [DRY RUN] ' : ''}Pruning ${toPrune.length} memories (weight < ${threshold}):\n`);
  for (const { m, w } of toPrune) {
    const icon = palace.domains[m.domain]?.icon ?? '📝';
    console.log(`  ${icon} ${m.id} (${m.domain}) weight:${w.toFixed(2)}`);
    console.log(`     ${m.content.slice(0, 80)}`);
  }

  if (!dryRun) {
    const pruneIds = new Set(toPrune.map(x => x.m.id));
    palace.memories = palace.memories.filter(m => !pruneIds.has(m.id));
    for (const m of palace.memories) {
      m.links = (m.links || []).filter(l => !pruneIds.has(l));
    }
    savePalace(palace, args.palace);
    console.log(`\n🗑️  Pruned ${toPrune.length} memories`);
  }
}

function cmdStatus(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  console.log('🏛️  Loci Palace');
  console.log(`   Created: ${palace.created ?? '?'} | Last walk: ${palace.last_walk ?? 'never'}`);
  console.log(`   Total memories: ${palace.memories.length}\n`);

  for (const [dk, di] of Object.entries(palace.domains)) {
    const mems = palace.memories.filter(m => m.domain === dk);
    const cap = di.capacity ?? 25;
    const icon = di.icon ?? '📝';
    const weights = mems.map(m => computeWeight(m));
    const avg = weights.length ? weights.reduce((a, b) => a + b, 0) / weights.length : 0;
    console.log(`  ${icon} ${(di.name || dk).padEnd(6)} [${bar(mems.length, cap)}] ${String(mems.length).padStart(2)}/${cap} avg:${avg.toFixed(2)}`);
  }

  const linkCount = palace.memories.reduce((s, m) => s + (m.links?.length ?? 0), 0);
  const tagSet = new Set();
  for (const m of palace.memories) (m.tags || []).forEach(t => tagSet.add(t));
  console.log(`\n   🔗 ${linkCount} links | 🏷️  ${tagSet.size} unique tags`);
}

function cmdInspect(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const target = args._[1];
  if (!target) { console.log('Usage: loci inspect <id>'); return; }
  const found = palace.memories.find(m => m.id === target);
  if (!found) { console.log(`❌ Memory not found: ${target}`); return; }

  const di = palace.domains[found.domain] ?? {};
  const icon = di.icon ?? '📝';
  const w = computeWeight(found);

  console.log(`${icon} Memory: ${found.id}`);
  console.log(`   Domain: ${found.domain} (${di.name ?? ''})`);
  console.log(`   Content: ${found.content}`);
  console.log(`   Tags: ${(found.tags || []).join(', ') || 'none'}`);
  console.log(`   Weight: ${w.toFixed(2)} (base: ${found.base_weight ?? 1.0})`);
  console.log(`   Created: ${found.created}`);
  console.log(`   Last accessed: ${found.last_accessed}`);
  console.log(`   Access count: ${found.access_count ?? 0}`);
  if (found.links?.length) {
    console.log(`   Links: ${found.links.join(', ')}`);
    for (const lid of found.links) {
      const linked = palace.memories.find(m => m.id === lid);
      if (linked) console.log(`     → ${lid}: ${linked.content.slice(0, 60)}...`);
    }
  }

  found.last_accessed = today();
  found.access_count = (found.access_count ?? 0) + 1;
  savePalace(palace, args.palace);
}

function cmdLink(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const id1 = args._[1], id2 = args._[2];
  if (!id1 || !id2) { console.log('Usage: loci link <id1> <id2>'); return; }
  const m1 = palace.memories.find(m => m.id === id1);
  const m2 = palace.memories.find(m => m.id === id2);
  if (!m1) { console.log(`❌ Memory not found: ${id1}`); return; }
  if (!m2) { console.log(`❌ Memory not found: ${id2}`); return; }

  if (!(m1.links || []).includes(id2)) (m1.links = m1.links || []).push(id2);
  if (!(m2.links || []).includes(id1)) (m2.links = m2.links || []).push(id1);

  savePalace(palace, args.palace);
  console.log(`🔗 Linked: ${id1} ↔ ${id2}`);
}

function cmdDomains(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  if (args.add) {
    const name = args.add;
    const cap = args.capacity ?? 20;
    if (palace.domains[name]) { console.log(`⚠️  Domain '${name}' already exists`); return; }
    palace.domains[name] = { name, icon: '📝', capacity: cap, description: '' };
    savePalace(palace, args.palace);
    console.log(`✅ Added domain: ${name} (capacity: ${cap})`);
    return;
  }

  if (args.remove) {
    const name = args.remove;
    if (!palace.domains[name]) { console.log(`❌ Domain not found: ${name}`); return; }
    const count = palace.memories.filter(m => m.domain === name).length;
    if (count > 0) { console.log(`⚠️  Domain '${name}' has ${count} memories. Remove them first or use --force`); return; }
    delete palace.domains[name];
    savePalace(palace, args.palace);
    console.log(`🗑️  Removed domain: ${name}`);
    return;
  }

  console.log('📋 Domains:\n');
  for (const [key, info] of Object.entries(palace.domains)) {
    const count = palace.memories.filter(m => m.domain === key).length;
    const cap = info.capacity ?? 25;
    const icon = info.icon ?? '📝';
    console.log(`  ${icon} ${key.padEnd(15)} (${info.name ?? ''}) — ${count}/${cap}`);
    if (info.description) console.log(`     ${info.description}`);
  }
}

function cmdExport(args) {
  const palace = loadPalace(args.palace);
  if (!palace) { console.log('❌ No palace found. Run: loci init'); return; }

  const fmt = args.format || 'md';

  if (fmt === 'json') {
    console.log(JSON.stringify(palace, null, 2));
    return;
  }

  // Markdown export
  console.log('# 🏛️ Loci Palace\n');
  console.log(`Created: ${palace.created ?? '?'} | Last walk: ${palace.last_walk ?? 'never'}\n`);

  for (const [dk, di] of Object.entries(palace.domains)) {
    const mems = palace.memories.filter(m => m.domain === dk);
    if (!mems.length) continue;
    const icon = di.icon ?? '📝';
    console.log(`## ${icon} ${di.name ?? dk}\n`);

    const sorted = [...mems].sort((a, b) => computeWeight(b) - computeWeight(a));
    for (const m of sorted) {
      const w = computeWeight(m);
      const tags = m.tags?.length ? ' `' + m.tags.join('` `') + '`' : '';
      console.log(`- **[${m.id}]** (w:${w.toFixed(2)}) ${m.content}${tags}`);
      if (m.links?.length) console.log(`  - 🔗 ${m.links.join(', ')}`);
    }
    console.log();
  }
}

// ─── Main ───

const args = parseArgs(process.argv.slice(2));
const command = args._[0];

const commands = {
  init: cmdInit,
  store: cmdStore,
  recall: cmdRecall,
  walk: cmdWalk,
  prune: cmdPrune,
  status: cmdStatus,
  inspect: cmdInspect,
  link: cmdLink,
  domains: cmdDomains,
  export: cmdExport,
};

if (!command || !commands[command]) {
  console.log(`loci — Structured memory with decay, domains, and links for AI agents.

Commands:
  init                          Initialize a new palace
  store <domain> <content>      Store a memory (--tag TAG --link ID)
  recall <query>                Search memories (--domain --top N)
  walk                          Walk through palace (--decay RATE)
  prune                         Remove decayed memories (--threshold --dry-run)
  status                        Palace overview
  inspect <id>                  View memory details + links
  link <id1> <id2>              Connect two memories
  domains                       List/add/remove domains (--add --remove --capacity)
  export                        Export palace (--format md|json)

Options:
  --palace PATH                 Path to palace file (default: ~/.openclaw/workspace/loci_palace.json)`);
  process.exit(0);
}

commands[command](args);
