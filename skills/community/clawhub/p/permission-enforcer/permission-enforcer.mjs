#!/usr/bin/env node
/**
 * Permission Enforcer - Unified permission checking
 * Reads policy from ~/.openclaw/workspace/policy/enforcer-policy.json
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const POLICY_PATH = path.join(process.env.HOME, '.openclaw', 'workspace', 'policy', 'enforcer-policy.json');
const WORKSPACE_ROOT = path.join(process.env.HOME, '.openclaw', 'workspace');
const OPENCLAW_CORE_PATHS = [
  '/opt/homebrew/lib/node_modules/openclaw',
  path.join(process.env.HOME, '.openclaw', 'agents'),
  path.join(process.env.HOME, '.openclaw', 'gateway')
];

// Load policy
function loadPolicy() {
  try {
    const content = fs.readFileSync(POLICY_PATH, 'utf-8');
    return JSON.parse(content);
  } catch (err) {
    console.error('[PermissionEnforcer] Failed to load policy:', err.message);
    return { rules: [] };
  }
}

// Check if path is within workspace
function isInWorkspace(targetPath) {
  const resolved = path.resolve(targetPath);
  return resolved.startsWith(WORKSPACE_ROOT);
}

// Check if path is OpenClaw core
function isOpenClawCore(targetPath) {
  const resolved = path.resolve(targetPath);
  return OPENCLAW_CORE_PATHS.some(corePath => resolved.startsWith(corePath));
}

// Match pattern against string
function matchPattern(str, pattern) {
  // Convert glob-like pattern to regex
  const regex = new RegExp(pattern.replace(/\*/g, '.*'));
  return regex.test(str);
}

// Check permission
export function checkPermission(action, target, options = {}) {
  const policy = loadPolicy();
  
  // Determine scope/pattern
  let scope = null;
  let pattern = null;
  
  if (action === 'file_write') {
    if (isOpenClawCore(target)) {
      scope = 'openclaw_core';
    } else if (isInWorkspace(target)) {
      scope = 'workspace';
    } else {
      scope = 'outside_workspace';
    }
  } else if (action === 'bash') {
    pattern = target; // target is the command string
  } else if (action === 'mcp') {
    // target is { tool, server }
    scope = `${options.server}/${options.tool}`;
  }
  
  // Find matching rules (last match wins)
  let matchedRule = null;
  
  for (const rule of policy.rules) {
    if (rule.action !== action) continue;
    
    if (scope && rule.scope === scope) {
      matchedRule = rule;
    } else if (pattern && rule.pattern && matchPattern(pattern, rule.pattern)) {
      matchedRule = rule;
    } else if (action === 'mcp' && rule.server === options.server) {
      if (rule.tool === '*' || rule.tool === options.tool) {
        matchedRule = rule;
      }
    }
  }
  
  if (!matchedRule) {
    return { allowed: true }; // Default allow if no rule matches
  }
  
  if (matchedRule.effect === 'deny') {
    return {
      allowed: false,
      reason: matchedRule.description || `${action} denied by policy`,
      rule: matchedRule
    };
  }
  
  if (matchedRule.effect === 'prompt') {
    return {
      allowed: false,
      prompt: true,
      message: matchedRule.description || `Confirm ${action}?`,
      rule: matchedRule
    };
  }
  
  return { allowed: true, rule: matchedRule };
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const action = process.argv[2];
  const target = process.argv[3];
  
  if (!action || !target) {
    console.log('Usage: permission-enforcer.mjs <action> <target>');
    console.log('  action: file_write, bash, mcp');
    console.log('  target: path for file_write, command for bash, tool for mcp');
    process.exit(1);
  }
  
  const result = checkPermission(action, target);
  console.log(JSON.stringify(result, null, 2));
}
