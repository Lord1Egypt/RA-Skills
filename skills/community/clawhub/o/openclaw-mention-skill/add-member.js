#!/usr/bin/env node
/**
 * Add a member to the LID_CACHE manually
 * Usage: node add-member.js --lid <LID> --name <Name> [--phone <Phone>] [--group <GroupJID>] [--alias <Alias>...]
 */

const fs = require('fs');
const path = require('path');

const CACHE_PATH = process.env.LID_CACHE_PATH || '/home/openclaw/.openclaw/workspace/LID_CACHE.json';

function parseArgs(args) {
  const result = { aliases: [] };
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--lid': result.lid = args[++i]; break;
      case '--name': result.name = args[++i]; break;
      case '--phone': result.phone = args[++i]; break;
      case '--group': result.group = args[++i]; break;
      case '--alias': result.aliases.push(args[++i]); break;
      case '--help': case '-h': return null;
    }
  }
  return result;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));

  if (!opts || !opts.lid || !opts.name) {
    console.log(`Usage: node add-member.js --lid <LID> --name <Name> [options]

Options:
  --lid <LID>        WhatsApp LID (required)
  --name <Name>      Display name (required)
  --phone <Phone>    Phone number (e.g., 1234567890)
  --group <GroupJID> Add to specific group (e.g., 120363400000000000@g.us)
  --alias <Alias>    Additional alias (can be repeated)

Example:
  node add-member.js --lid 123456789012345 --name "John" --phone 1234567890 --alias "john" --group "120363400000000000@g.us"
`);
    process.exit(1);
  }

  let cache;
  try {
    cache = JSON.parse(fs.readFileSync(CACHE_PATH, 'utf8'));
  } catch {
    cache = { _names: {}, _aliases: {} };
  }

  // Add to _names
  if (!cache._names) cache._names = {};
  cache._names[opts.lid] = opts.name;
  console.log(`Added name: ${opts.lid} → ${opts.name}`);

  // Add to _aliases
  if (!cache._aliases) cache._aliases = {};
  const autoAliases = [
    opts.name.toLowerCase(),
    opts.name.toLowerCase().replace(/\s+/g, ''),
  ];
  const allAliases = [...new Set([...autoAliases, ...opts.aliases.map(a => a.toLowerCase())])];
  for (const alias of allAliases) {
    cache._aliases[alias] = opts.lid;
    console.log(`Added alias: ${alias} → ${opts.lid}`);
  }

  // Add to group
  if (opts.group) {
    if (!cache[opts.group]) cache[opts.group] = {};
    cache[opts.group][opts.lid] = opts.phone || '';
    console.log(`Added to group: ${opts.group}`);
  }

  // Add to ALL existing groups if phone is provided
  if (opts.phone && !opts.group) {
    let groupCount = 0;
    for (const key of Object.keys(cache)) {
      if (key.startsWith('_')) continue;
      if (!cache[key][opts.lid]) {
        cache[key][opts.lid] = opts.phone;
        groupCount++;
      }
    }
    if (groupCount) console.log(`Added to ${groupCount} existing groups`);
  }

  fs.writeFileSync(CACHE_PATH, JSON.stringify(cache, null, 2));
  console.log(`\nSaved to ${CACHE_PATH}`);
}

main();
