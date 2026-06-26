#!/usr/bin/env node

const fs = require('fs');
const {
  AGENT_MODE_DEFINITIONS,
  buildAgentModePolicy,
  defaultConfig,
  defaultQueue,
  ensureDir,
  normalizeAgentMode,
  readJson,
  resolvePaths,
  writeJson
} = require('./session-utils');

const args = process.argv.slice(2);

function getArg(name, fallback = '') {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] || fallback;
}

const init = args.includes('--init');
const validate = args.includes('--validate');
const listAgentModes = args.includes('--list-agent-modes');
const setAgentModeArg = getArg('--set-agent-mode');
const setObserveSecondsArg = getArg('--set-observe-seconds');
const dir = getArg('--dir', 'hinge-data');

if (!init && !validate && !listAgentModes && !setAgentModeArg && !setObserveSecondsArg) {
  console.log('Usage:');
  console.log('  node onboarding.js --init --dir hinge-data');
  console.log('  node onboarding.js --validate --dir hinge-data');
  console.log('  node onboarding.js --list-agent-modes');
  console.log('  node onboarding.js --set-agent-mode <like_only|full_access|likes_with_comments_only> --dir hinge-data');
  console.log('  node onboarding.js --set-observe-seconds <0-300> --dir hinge-data');
  process.exit(1);
}

const paths = resolvePaths(dir);

if (listAgentModes) {
  console.log('Agent modes:');
  AGENT_MODE_DEFINITIONS.forEach((mode, index) => {
    console.log(`${index + 1}. ${mode.id} (${mode.label})`);
    console.log(`   ${mode.description}`);
  });
  process.exit(0);
}

if (setAgentModeArg) {
  ensureDir(paths.root);
  const config = readJson(paths.configPath, defaultConfig());
  const mode = normalizeAgentMode(setAgentModeArg);
  config.automation = config.automation || {};
  config.automation.agentMode = mode;
  writeJson(paths.configPath, config);
  const policy = buildAgentModePolicy(mode, config.automation.activeTabs || []);
  console.log(`Set automation.agentMode to ${policy.agentMode} (${policy.label}).`);
  console.log(`Active tabs in this mode: ${policy.activeTabs.join(', ')}`);
  console.log(`Replies: ${policy.allowReplies ? 'enabled' : 'disabled'}`);
  console.log(`Like comments: ${policy.allowLikeComments ? 'enabled' : 'disabled'}`);
  console.log(`Roses: ${policy.allowRoses ? 'enabled' : 'disabled'}`);
  process.exit(0);
}

if (setObserveSecondsArg) {
  ensureDir(paths.root);
  const config = readJson(paths.configPath, defaultConfig());
  const observeSeconds = Math.max(0, Math.min(300, Number(setObserveSecondsArg) || 0));
  config.automation = config.automation || {};
  config.automation.observeWarmupSeconds = observeSeconds;
  config.automation.observeBeforeTakeover = observeSeconds > 0;
  writeJson(paths.configPath, config);
  console.log(`Set observe warmup to ${observeSeconds}s.`);
  console.log(`Observe-before-takeover: ${config.automation.observeBeforeTakeover ? 'enabled' : 'disabled'}.`);
  process.exit(0);
}

if (init) {
  ensureDir(paths.root);

  if (!fs.existsSync(paths.configPath)) {
    writeJson(paths.configPath, defaultConfig());
    console.log(`Created ${paths.configPath}`);
  } else {
    console.log(`Exists ${paths.configPath}`);
  }

  if (!fs.existsSync(paths.queuePath)) {
    writeJson(paths.queuePath, defaultQueue());
    console.log(`Created ${paths.queuePath}`);
  } else {
    console.log(`Exists ${paths.queuePath}`);
  }

  if (!fs.existsSync(paths.stagedMessagePath)) {
    fs.writeFileSync(paths.stagedMessagePath, '');
    console.log(`Created ${paths.stagedMessagePath}`);
  } else {
    console.log(`Exists ${paths.stagedMessagePath}`);
  }

  console.log('');
  console.log('Next: fill in profile-preferences.json and start queueing profiles.');
  process.exit(0);
}

const config = readJson(paths.configPath, null);
const queue = readJson(paths.queuePath, null);

if (!config) {
  console.error(`Missing config: ${paths.configPath}`);
  process.exit(1);
}

if (!queue) {
  console.error(`Missing queue: ${paths.queuePath}`);
  process.exit(1);
}

const required = [];
const recommended = [];

if (!config.user?.goals) required.push('user.goals');
if (!config.user?.tone) required.push('user.tone');
if (!Array.isArray(config.user?.dealbreakers)) required.push('user.dealbreakers');
if (!config.ios?.appiumServer) recommended.push('ios.appiumServer');
if (!config.ios?.bundleId) recommended.push('ios.bundleId');
if (!config.ios?.deviceName) recommended.push('ios.deviceName');
if (!config.automation?.agentMode) recommended.push('automation.agentMode');
if (config.automation?.observeBeforeTakeover && !config.automation?.observeWarmupSeconds) {
  recommended.push('automation.observeWarmupSeconds');
}

if (required.length === 0) {
  console.log('Core Hinge session config looks usable.');
} else {
  console.log('Missing required fields:');
  required.forEach(item => console.log(`- ${item}`));
}

if (recommended.length > 0) {
  console.log('');
  console.log('Recommended for iOS automation:');
  recommended.forEach(item => console.log(`- ${item}`));
}

if (config.automation?.agentMode) {
  const policy = buildAgentModePolicy(config.automation.agentMode, config.automation?.activeTabs || []);
  console.log('');
  console.log(`Agent mode: ${policy.agentMode} (${policy.label})`);
  console.log(`Mode tabs: ${policy.activeTabs.join(', ')}`);
}

console.log('');
console.log(`Queued profiles: ${Array.isArray(queue.entries) ? queue.entries.length : 0}`);
process.exit(required.length === 0 ? 0 : 1);
