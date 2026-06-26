#!/usr/bin/env node

const fs = require('fs');
const {
  defaultQueue,
  deriveProfileId,
  ensureDir,
  normalizeFit,
  normalizeStatus,
  readJson,
  renderMarkdown,
  resolvePaths,
  upsertEntry,
  writeJson
} = require('./session-utils');

const args = process.argv.slice(2);

function hasFlag(name) {
  return args.includes(name);
}

function getArg(name, fallback = '') {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] || fallback;
}

function loadQueue(dir) {
  const paths = resolvePaths(dir);
  ensureDir(paths.root);
  const queue = readJson(paths.queuePath, defaultQueue());
  return { paths, queue };
}

function saveQueue(paths, queue) {
  writeJson(paths.queuePath, queue);
}

function printUsage() {
  console.log('Usage:');
  console.log('  node queue.js --init --dir hinge-data');
  console.log('  node queue.js --add --dir hinge-data --name "Ava" --fit "strong yes" --hook "climbing" --best-opener "..."');
  console.log('  node queue.js --mark --dir hinge-data --profile-id ava-123 --status approved');
  console.log('  node queue.js --stage --dir hinge-data --profile-id ava-123 --message "..."');
  console.log('  node queue.js --list --dir hinge-data');
  console.log('  node queue.js --render --dir hinge-data');
}

if (args.length === 0) {
  printUsage();
  process.exit(1);
}

const dir = getArg('--dir', 'hinge-data');

if (hasFlag('--init')) {
  const { paths, queue } = loadQueue(dir);
  saveQueue(paths, queue);
  if (!fs.existsSync(paths.stagedMessagePath)) {
    fs.writeFileSync(paths.stagedMessagePath, '');
  }
  console.log(`Queue ready at ${paths.queuePath}`);
  process.exit(0);
}

if (hasFlag('--add')) {
  const { paths, queue } = loadQueue(dir);
  const name = getArg('--name');
  if (!name) {
    console.error('Missing --name');
    process.exit(1);
  }

  const profileId = getArg('--profile-id', deriveProfileId(name));
  const entry = {
    profileId,
    name,
    fit: normalizeFit(getArg('--fit', 'maybe')),
    status: normalizeStatus(getArg('--status', 'new')),
    source: getArg('--source', 'discover'),
    hook: getArg('--hook'),
    bestOpener: getArg('--best-opener'),
    backupOpener: getArg('--backup-opener'),
    note: getArg('--note')
  };

  upsertEntry(queue, entry);
  saveQueue(paths, queue);
  console.log(`Saved ${profileId}`);
  process.exit(0);
}

if (hasFlag('--mark')) {
  const profileId = getArg('--profile-id');
  const status = normalizeStatus(getArg('--status'));
  if (!profileId) {
    console.error('Missing --profile-id');
    process.exit(1);
  }

  const { paths, queue } = loadQueue(dir);
  const entry = queue.entries.find(item => item.profileId === profileId);
  if (!entry) {
    console.error(`Profile not found: ${profileId}`);
    process.exit(1);
  }

  upsertEntry(queue, { ...entry, status });
  saveQueue(paths, queue);
  console.log(`Updated ${profileId} -> ${status}`);
  process.exit(0);
}

if (hasFlag('--stage')) {
  const profileId = getArg('--profile-id');
  const message = getArg('--message');
  if (!profileId || !message) {
    console.error('Missing --profile-id or --message');
    process.exit(1);
  }

  const { paths, queue } = loadQueue(dir);
  const entry = queue.entries.find(item => item.profileId === profileId);
  if (!entry) {
    console.error(`Profile not found: ${profileId}`);
    process.exit(1);
  }

  upsertEntry(queue, { ...entry, stagedMessage: message, status: 'staged' });
  saveQueue(paths, queue);
  fs.writeFileSync(paths.stagedMessagePath, message);
  console.log(`Staged message for ${profileId}`);
  process.exit(0);
}

if (hasFlag('--list')) {
  const { queue } = loadQueue(dir);
  if (queue.entries.length === 0) {
    console.log('No profiles queued.');
    process.exit(0);
  }

  for (const entry of queue.entries) {
    console.log(`${entry.profileId} | ${entry.name} | ${entry.fit} | ${entry.status} | ${entry.hook || ''}`);
  }
  process.exit(0);
}

if (hasFlag('--render')) {
  const { paths, queue } = loadQueue(dir);
  const markdown = renderMarkdown(queue);
  fs.writeFileSync(paths.markdownPath, markdown);
  console.log(`Wrote ${paths.markdownPath}`);
  process.exit(0);
}

printUsage();
process.exit(1);
