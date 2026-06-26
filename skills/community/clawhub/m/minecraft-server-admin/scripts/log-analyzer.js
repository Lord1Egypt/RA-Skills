#!/usr/bin/env node
/**
 * log-analyzer.js — Minecraft server log analyzer
 *
 * Usage: node log-analyzer.js [log_file] [--lines N] [--json]
 *   log_file: defaults to MC_SERVER_LOG
 *   --lines N: analyze the last N lines (default 500)
 *   --json: output JSON
 */

'use strict';

const fs = require('fs');
const path = require('path');

const LOG_FILE = process.env.MC_SERVER_LOG || '';
const args = process.argv.slice(2);

const PATTERNS = {
  playerJoin: /\[(\d{2}:\d{2}:\d{2})\].*?(\w+) joined the game/,
  playerLeave: /\[(\d{2}:\d{2}:\d{2})\].*?(\w+) left the game/,
  playerChat: /\[(\d{2}:\d{2}:\d{2})\].*?<(\w+)> (.+)/,
  playerDeath: /\[(\d{2}:\d{2}:\d{2})\].*?(\w+) (was slain|was shot|drowned|burned|fell|died|was killed)/,
  lagWarning: /\[(\d{2}:\d{2}:\d{2})\].*?Can't keep up! Running (\d+)ms behind/,
  serverStart: /\[(\d{2}:\d{2}:\d{2})\].*?Done \([\d.]+s\)!/,
  serverStop: /\[(\d{2}:\d{2}:\d{2})\].*?Stopping server/,
  errorLine: /\[(\d{2}:\d{2}:\d{2})\].*?\[(?:WARN|ERROR)\]/,
  stackTrace: /\s+at\s+[\w.$]+\(/,
  kicked: /\[(\d{2}:\d{2}:\d{2})\].*?(\w+) was kicked/,
  banned: /\[(\d{2}:\d{2}:\d{2})\].*?Bann(?:ing|ed) (\w+)/,
  commandUsed: /\[(\d{2}:\d{2}:\d{2})\].*?(\w+) issued server command: (.+)/,
  advancement: /\[(\d{2}:\d{2}:\d{2})\].*?(\w+) has made the advancement/,
};

function analyzeLog(logContent) {
  const lines = logContent.split('\n').filter(Boolean);
  const report = {
    totalLines: lines.length,
    playerEvents: { joins: [], leaves: [], deaths: [], kicks: [], bans: [] },
    chatMessages: [],
    commands: [],
    performance: { lagEvents: [], serverRestarts: [] },
    errors: [],
    advancements: [],
    summary: {},
  };

  for (const line of lines) {
    let m;

    if ((m = line.match(PATTERNS.playerJoin))) {
      const [, time, player] = m;
      report.playerEvents.joins.push({ time, player });
    } else if ((m = line.match(PATTERNS.playerLeave))) {
      const [, time, player] = m;
      report.playerEvents.leaves.push({ time, player });
    } else if ((m = line.match(PATTERNS.playerChat))) {
      const [, time, player, message] = m;
      report.chatMessages.push({ time, player, message });
    } else if ((m = line.match(PATTERNS.playerDeath))) {
      const [, time, player, cause] = m;
      report.playerEvents.deaths.push({ time, player, cause });
    } else if ((m = line.match(PATTERNS.lagWarning))) {
      const [, time, msLag] = m;
      report.performance.lagEvents.push({ time, msLag: parseInt(msLag) });
    } else if (line.match(PATTERNS.serverStart)) {
      report.performance.serverRestarts.push({ time: (line.match(/\[(\d{2}:\d{2}:\d{2})\]/) || [])[1], event: 'start' });
    } else if (line.match(PATTERNS.serverStop)) {
      report.performance.serverRestarts.push({ time: (line.match(/\[(\d{2}:\d{2}:\d{2})\]/) || [])[1], event: 'stop' });
    } else if ((m = line.match(PATTERNS.commandUsed))) {
      const [, time, player, command] = m;
      report.commands.push({ time, player, command });
    } else if ((m = line.match(PATTERNS.kicked))) {
      const [, time, player] = m;
      report.playerEvents.kicks.push({ time, player });
    } else if ((m = line.match(PATTERNS.banned))) {
      const [, time, player] = m;
      report.playerEvents.bans.push({ time, player });
    } else if ((m = line.match(PATTERNS.advancement))) {
      const [, time, player] = m;
      report.advancements.push({ time, player, line: line.trim() });
    } else if (line.match(PATTERNS.errorLine) && !line.match(PATTERNS.stackTrace)) {
      report.errors.push(line.trim());
    }
  }

  const allPlayers = new Set([
    ...report.playerEvents.joins.map(e => e.player),
    ...report.playerEvents.leaves.map(e => e.player),
  ]);
  const severeLag = report.performance.lagEvents.filter(e => e.msLag > 5000);

  report.summary = {
    uniquePlayers: allPlayers.size,
    playerList: [...allPlayers].sort(),
    totalJoins: report.playerEvents.joins.length,
    totalDeaths: report.playerEvents.deaths.length,
    totalErrors: report.errors.length,
    lagWarnings: report.performance.lagEvents.length,
    severeLagWarnings: severeLag.length,
    chatMessages: report.chatMessages.length,
    serverRestarts: report.performance.serverRestarts.length,
    commandsExecuted: report.commands.length,
  };

  return report;
}

function formatReport(report) {
  const s = report.summary;
  const lines = [
    'Server Log Summary',
    '----------------------------------------',
    `Analyzed lines: ${report.totalLines}`,
    '',
    'Player Activity',
    `  Unique players: ${s.uniquePlayers}`,
    s.uniquePlayers > 0 ? `  Seen players: ${s.playerList.join(', ')}` : '',
    `  Joins: ${s.totalJoins} | Deaths: ${s.totalDeaths}`,
    `  Chat messages: ${s.chatMessages} | Commands: ${s.commandsExecuted}`,
    '',
    'Performance',
    `  Restarts: ${s.serverRestarts}`,
    `  Lag warnings: ${s.lagWarnings}`,
    s.severeLagWarnings > 0 ? `  Severe lag warnings (>5s): ${s.severeLagWarnings}` : '',
    '',
    `Errors/Warnings: ${s.totalErrors}`,
  ];

  if (report.errors.length > 0) {
    lines.push('  Recent errors:');
    report.errors.slice(-5).forEach(e => lines.push(`    ${e.slice(0, 100)}`));
  }

  if (report.performance.lagEvents.length > 0) {
    const worst = [...report.performance.lagEvents].sort((a, b) => b.msLag - a.msLag)[0];
    lines.push('', `Worst lag spike: ${worst.msLag}ms at ${worst.time}`);
  }

  if (report.playerEvents.kicks.length > 0) {
    lines.push('', 'Kick events:');
    report.playerEvents.kicks.forEach(k => lines.push(`  [${k.time}] ${k.player}`));
  }

  if (report.playerEvents.bans.length > 0) {
    lines.push('', 'Ban events:');
    report.playerEvents.bans.forEach(b => lines.push(`  [${b.time}] ${b.player}`));
  }

  return lines.filter(Boolean).join('\n');
}

if (require.main === module) {
  const jsonMode = args.includes('--json');
  const linesIdx = args.indexOf('--lines');
  const maxLines = linesIdx >= 0 ? parseInt(args[linesIdx + 1]) : 500;
  const filePath = args.find(a => !a.startsWith('--')) || LOG_FILE;

  if (!filePath) {
    console.error('Usage: node log-analyzer.js <log_file> [--lines N] [--json]');
    console.error('Or set MC_SERVER_LOG in the environment.');
    process.exit(1);
  }

  const resolvedPath = path.resolve(filePath);
  if (!resolvedPath.endsWith('.log') && !resolvedPath.endsWith('.txt')) {
    console.error('Only .log and .txt files are supported');
    process.exit(1);
  }

  if (!fs.existsSync(resolvedPath)) {
    console.error(`Log file not found: ${resolvedPath}`);
    process.exit(1);
  }

  try {
    const content = fs.readFileSync(resolvedPath, 'utf8');
    const allLines = content.split('\n');
    const chunk = allLines.slice(-maxLines).join('\n');
    const report = analyzeLog(chunk);
    if (jsonMode) console.log(JSON.stringify(report, null, 2));
    else console.log(formatReport(report));
  } catch (err) {
    console.error(`Failed to read log: ${err.message}`);
    process.exit(1);
  }
}

module.exports = { analyzeLog, formatReport };
