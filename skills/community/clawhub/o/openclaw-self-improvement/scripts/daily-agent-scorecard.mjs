#!/usr/bin/env node
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import process from 'node:process';

import { buildAgentScorecard, buildRepairTickets, markdownScorecard, readAgentSessions, readJsonSafe, writeRepairTickets } from './harness-improvement-lib.mjs';

const workspace = process.env.WORKSPACE || resolve(process.env.HOME || '/Users/m1', '.openclaw/workspace');
const dataDir = resolve(workspace, 'mission-control', 'data');
const openclawHome = process.env.OPENCLAW_HOME || resolve(process.env.HOME || '/Users/m1', '.openclaw');
const defaultAgents = ['muddy', 'clawdy', 'woody', 'hunter', 'jk', 'tony', 'peter', 'elon', 'jenny', 'mark', 'karen', 'tully'];

function argValue(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index === -1 ? fallback : process.argv[index + 1] || fallback;
}

function hasFlag(name) {
  return process.argv.includes(name);
}

function shanghaiDate() {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Shanghai' });
}

const date = argValue('--date', shanghaiDate());
const reportPath = resolve(argValue('--report', resolve(dataDir, 'progress-report.json')));
const outputPath = argValue('--output', null);
const ticketsDir = argValue('--tickets-dir', resolve(dataDir, 'recovery-tickets-v3'));
const agents = (argValue('--agents', defaultAgents.join(',')) || '').split(',').map((agent) => agent.trim()).filter(Boolean);
const progressReport = readJsonSafe(reportPath, {});
const sessions = readAgentSessions(openclawHome, agents);
const scorecard = buildAgentScorecard({ date, progressReport, sessions });
const tickets = hasFlag('--repair') ? buildRepairTickets(scorecard) : [];
const writtenTickets = hasFlag('--repair') ? writeRepairTickets(tickets, ticketsDir) : [];
if (writtenTickets.length) scorecard.repairTickets = writtenTickets;

if (outputPath) {
  const path = resolve(outputPath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, hasFlag('--json') ? `${JSON.stringify(scorecard, null, 2)}\n` : markdownScorecard(scorecard));
  console.log(path);
} else if (hasFlag('--json')) {
  console.log(JSON.stringify(scorecard, null, 2));
} else {
  process.stdout.write(markdownScorecard(scorecard));
}
