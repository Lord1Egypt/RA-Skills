#!/usr/bin/env node
/**
 * scripts/approve.js
 * 
 * A symbolic script to signal user approval of an implementation plan. 
 * This creates a machine-verifiable event in the task logs that the Planning 
 * Mode gate has been passed.
 * 
 * SECURITY: The approvals file is created with 0600 permissions (owner-only) in /tmp.
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, chmodSync } from 'fs';
import { join, dirname } from 'path';
import { getTempDir } from './path-resolver.js';

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log("Usage: node scripts/approve.js <task_name>");
  process.exit(1);
}

const taskName = args[0];
const approvalPath = join(getTempDir(), 'approvals.json');

// Ensure directory exists (mkdirSync with 0700 already handled in getTempDir, but we'll reflect here just in case)
const workspaceRoot = dirname(approvalPath);
if (!existsSync(workspaceRoot)) {
  mkdirSync(workspaceRoot, { recursive: true, mode: 0o700 });
}

let approvals = [];
if (existsSync(approvalPath)) {
  try {
    approvals = JSON.parse(readFileSync(approvalPath, 'utf8'));
  } catch (e) {
    approvals = [];
  }
}

const approval = {
  task: taskName,
  approvedAt: new Date().toISOString(),
  status: "APPROVED"
};

approvals.push(approval);
writeFileSync(approvalPath, JSON.stringify(approvals, null, 2));

// Set owner-only (0600) permission to protect the gate signal
try {
  chmodSync(approvalPath, 0o600);
} catch (e) {
  // Graceful fallback if chmod fails on some FS
}

console.log(`✅ [Gate] Task "${taskName}" has been officially APPROVED for execution.`);
process.exit(0);
