#!/usr/bin/env node
/**
 * Permission Enforcer v2 – Enhanced with boundary protection
 * Reads ~/.openclaw/workspace/policy/enforcer-policy.json
 * Now with proper symlink, path traversal, and home expansion handling
 */

import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const POLICY_PATH = path.join(os.homedir(), ".openclaw", "workspace", "policy", "enforcer-policy.json");
const WORKSPACE_ROOT = path.join(os.homedir(), ".openclaw", "workspace");

async function loadPolicy() {
  try {
    const raw = await fs.promises.readFile(POLICY_PATH, "utf-8");
    return JSON.parse(raw);
  } catch (err) {
    return { version: 1, rules: [] };
  }
}

/**
 * Normalize and validate a file path
 * Returns { scope: "workspace"|"outside_workspace"|"dangerous", reason?: string }
 */
function normalizeScope(filePath) {
  if (!filePath) return { scope: "unknown" };
  
  let resolved;
  
  // Handle home directory expansion
  if (filePath.startsWith("~/") || filePath === "~") {
    resolved = filePath.replace("~", os.homedir());
  } else {
    // Resolve relative paths from current working directory
    resolved = path.resolve(filePath);
  }
  
  const wr = path.resolve(WORKSPACE_ROOT);
  
  // Check for path traversal - normalize again to catch tricks
  const normalizedResolved = path.normalize(resolved);
  
  // Check if path is within workspace
  const isInWorkspace = normalizedResolved.startsWith(wr + path.sep) || normalizedResolved === wr;
  
  // Check if it's a dangerous system path (even if accessible)
  const dangerousPaths = ["/etc", "/usr", "/bin", "/sbin", "/lib", "/opt", "/var", os.homedir()];
  const isDangerous = dangerousPaths.some(dp => 
    normalizedResolved === dp || normalizedResolved.startsWith(dp + path.sep)
  );
  
  // Special case: OpenClaw core files
  const openclawCorePaths = [
    "/opt/homebrew/lib/node_modules/openclaw",
    path.join(os.homedir(), ".openclaw", ".core")
  ];
  const isOpenClawCore = openclawCorePaths.some(cp => 
    normalizedResolved.startsWith(cp + path.sep) || normalizedResolved === cp
  );
  
  if (isOpenClawCore) {
    return { scope: "openclaw_core" };
  }
  
  if (isInWorkspace) {
    // Check for symlink escape
    try {
      const realPath = fs.realpathSync(normalizedResolved);
      const realInWorkspace = realPath.startsWith(wr + path.sep) || realPath === wr;
      if (!realInWorkspace) {
        return { 
          scope: "dangerous", 
          reason: "Symlink points outside workspace",
          resolved: normalizedResolved,
          realPath
        };
      }
    } catch {
      // File doesn't exist yet, check parent directory
      const parentDir = path.dirname(normalizedResolved);
      if (fs.existsSync(parentDir)) {
        try {
          const realParent = fs.realpathSync(parentDir);
          const parentInWorkspace = realParent.startsWith(wr + path.sep) || realParent === wr;
          if (!parentInWorkspace) {
            return { 
              scope: "dangerous", 
              reason: "Parent directory symlink points outside workspace",
              resolved: normalizedResolved
            };
          }
        } catch {
          // Continue with normal check
        }
      }
    }
    return { scope: "workspace" };
  }
  
  return { scope: "outside_workspace" };
}

function matchPattern(text, pattern) {
  if (!pattern) return true;
  const regex = new RegExp(pattern, "i");
  return regex.test(text);
}

/**
 * Evaluate permission for an action.
 * @param {object} policy
 * @param {string} action   – e.g. "file_write", "bash", "mcp"
 * @param {object} context  – e.g. { filePath, bashCommand, server, tool }
 * @returns {{effect: "allow"|"deny"|"prompt", matchedRule?: object, reason: string}}
 */
export function evaluate(policy, action, context) {
  const rules = policy?.rules || [];
  
  // Pre-check for dangerous patterns
  if (action === "file_write" && context.filePath) {
    const normalized = normalizeScope(context.filePath);
    if (normalized.scope === "dangerous") {
      return { 
        effect: "deny", 
        reason: `Dangerous path detected: ${normalized.reason || 'Path escapes workspace boundaries'}`
      };
    }
  }
  
  // Filter to rules matching this action and context
  const candidates = rules
    .filter((r) => r.action === action)
    .filter((r) => {
      if (action === "file_write") {
        const normalized = normalizeScope(context.filePath);
        // Match both the resolved scope and any specific dangerous patterns
        if (r.scope === "dangerous" && normalized.scope === "dangerous") return true;
        return r.scope === normalized.scope;
      }
      if (action === "bash") {
        return matchPattern(context.bashCommand || "", r.pattern);
      }
      if (action === "mcp") {
        const serverMatch = r.server === "*" || r.server === context.server;
        const toolMatch = r.tool === "*" || r.tool === context.tool;
        return serverMatch && toolMatch;
      }
      return true;
    });

  // More specific rules win over wildcards
  const score = (r) => {
    let s = 0;
    if (r.scope && r.scope !== "*") s += 2;
    if (r.pattern && r.pattern !== ".*") s += 2;
    if (r.server && r.server !== "*") s += 1;
    if (r.tool && r.tool !== "*") s += 1;
    return s;
  };

  candidates.sort((a, b) => score(b) - score(a));

  if (candidates.length === 0) {
    return { effect: "allow", reason: "No matching policy rule; default allow" };
  }

  const winner = candidates[0];
  return {
    effect: winner.effect,
    matchedRule: winner,
    reason: winner.note || `Matched rule: ${JSON.stringify(winner)}`,
  };
}

async function main() {
  const action = process.argv[2];
  const contextRaw = process.argv[3] || "{}";
  let context = {};
  try {
    context = JSON.parse(contextRaw);
  } catch {
    context = { raw: contextRaw };
  }

  const policy = await loadPolicy();
  const result = evaluate(policy, action, context);
  console.log(JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
