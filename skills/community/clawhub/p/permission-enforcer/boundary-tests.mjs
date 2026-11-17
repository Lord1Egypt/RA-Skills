#!/usr/bin/env node
/**
 * Permission Enforcer - Boundary Test Suite
 * Tests edge cases: symlinks, relative paths, path traversal, etc.
 */

import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { evaluate } from "./check-permission.mjs";

const TEST_DIR = path.join(os.homedir(), ".openclaw", "workspace", "test-boundary");
const OUTSIDE_DIR = path.join(os.tmpdir(), "openclaw-test-outside");

// Change to workspace root for consistent relative path testing
process.chdir(path.join(os.homedir(), ".openclaw", "workspace"));

// Test cases
const testCases = [
  {
    name: "Normal workspace file write",
    action: "file_write",
    context: { filePath: path.join(os.homedir(), ".openclaw", "workspace", "test.txt") },
    expected: "allow"
  },
  {
    name: "File outside workspace",
    action: "file_write",
    context: { filePath: "/etc/passwd" },
    expected: "deny"
  },
  {
    name: "Relative path inside workspace (./)",
    action: "file_write",
    context: { filePath: "./test.txt" },
    expected: "allow"
  },
  {
    name: "Relative path parent traversal escaping workspace",
    action: "file_write",
    context: { filePath: "../outside.txt" },
    expected: "deny"
  },
  {
    name: "Path traversal attack (../../../etc/passwd)",
    action: "file_write",
    context: { filePath: "../../../etc/passwd" },
    expected: "deny"
  },
  {
    name: "Home directory expansion (~/.bashrc)",
    action: "file_write",
    context: { filePath: "~/.bashrc" },
    expected: "deny"
  },
  {
    name: "OpenClaw core file modification",
    action: "file_write",
    context: { filePath: "/opt/homebrew/lib/node_modules/openclaw/dist/test.js" },
    expected: "prompt"
  },
  {
    name: "Bash: safe ls command",
    action: "bash",
    context: { bashCommand: "ls -la" },
    expected: "allow"
  },
  {
    name: "Bash: dangerous rm -rf /",
    action: "bash",
    context: { bashCommand: "rm -rf /" },
    expected: "deny"
  },
  {
    name: "Bash: sudo command",
    action: "bash",
    context: { bashCommand: "sudo apt update" },
    expected: "prompt"
  },
  {
    name: "Bash: curl download",
    action: "bash",
    context: { bashCommand: "curl -O https://example.com/file.sh" },
    expected: "prompt"
  },
  {
    name: "Bash: wget download",
    action: "bash",
    context: { bashCommand: "wget https://example.com/file.sh" },
    expected: "prompt"
  },
  {
    name: "MCP: filesystem read",
    action: "mcp",
    context: { server: "filesystem", tool: "read_file" },
    expected: "allow"
  },
  {
    name: "MCP: filesystem write",
    action: "mcp",
    context: { server: "filesystem", tool: "write_file" },
    expected: "prompt"
  }
];

// Symlink test cases (require setup)
const symlinkTestCases = [
  {
    name: "Symlink pointing inside workspace",
    setup: async () => {
      const target = path.join(TEST_DIR, "real-file.txt");
      const link = path.join(TEST_DIR, "symlink-inside");
      await fs.mkdir(TEST_DIR, { recursive: true });
      await fs.writeFile(target, "test content");
      try { await fs.unlink(link); } catch {}
      await fs.symlink(target, link);
      return link;
    },
    cleanup: async () => {
      try { await fs.unlink(path.join(TEST_DIR, "symlink-inside")); } catch {}
    },
    action: "file_write",
    context: (linkPath) => ({ filePath: linkPath }),
    expected: "allow"
  },
  {
    name: "Symlink pointing outside workspace (dangerous)",
    setup: async () => {
      const target = path.join(OUTSIDE_DIR, "outside-file.txt");
      const link = path.join(TEST_DIR, "symlink-outside");
      await fs.mkdir(OUTSIDE_DIR, { recursive: true });
      await fs.writeFile(target, "outside content");
      try { await fs.unlink(link); } catch {}
      await fs.symlink(target, link);
      return link;
    },
    cleanup: async () => {
      try { 
        await fs.unlink(path.join(TEST_DIR, "symlink-outside")); 
        await fs.unlink(path.join(OUTSIDE_DIR, "outside-file.txt"));
        await fs.rmdir(OUTSIDE_DIR);
      } catch {}
    },
    action: "file_write",
    context: (linkPath) => ({ filePath: linkPath }),
    expected: "deny"
  }
];

async function loadPolicy() {
  const POLICY_PATH = path.join(os.homedir(), ".openclaw", "workspace", "policy", "enforcer-policy.json");
  try {
    const raw = await fs.readFile(POLICY_PATH, "utf-8");
    return JSON.parse(raw);
  } catch (err) {
    console.error("Failed to load policy:", err.message);
    return { version: 1, rules: [] };
  }
}

async function runTests() {
  console.log("╔════════════════════════════════════════════════════════╗");
  console.log("║     Permission Enforcer - Boundary Test Suite          ║");
  console.log("╚════════════════════════════════════════════════════════╝\n");

  const policy = await loadPolicy();
  let passed = 0;
  let failed = 0;

  // Basic tests
  console.log("📋 Basic Path Tests:\n");
  for (const test of testCases) {
    const result = evaluate(policy, test.action, test.context);
    const status = result.effect === test.expected ? "✓" : "✗";
    const color = result.effect === test.expected ? "\x1b[32m" : "\x1b[31m";
    const reset = "\x1b[0m";
    
    console.log(`${color}${status}${reset} ${test.name}`);
    console.log(`   Path: ${test.context.filePath || test.context.bashCommand || JSON.stringify(test.context)}`);
    console.log(`   Expected: ${test.expected}, Got: ${result.effect}`);
    
    if (result.effect === test.expected) {
      passed++;
    } else {
      failed++;
      console.log(`   Reason: ${result.reason}`);
    }
  }

  // Symlink tests
  console.log("\n🔗 Symlink Tests:\n");
  for (const test of symlinkTestCases) {
    let linkPath;
    try {
      linkPath = await test.setup();
      const context = test.context(linkPath);
      const result = evaluate(policy, test.action, context);
      const status = result.effect === test.expected ? "✓" : "✗";
      const color = result.effect === test.expected ? "\x1b[32m" : "\x1b[31m";
      const reset = "\x1b[0m";
      
      console.log(`${color}${status}${reset} ${test.name}`);
      console.log(`   Link: ${linkPath}`);
      console.log(`   Expected: ${test.expected}, Got: ${result.effect}`);
      
      if (result.effect === test.expected) {
        passed++;
      } else {
        failed++;
        console.log(`   Reason: ${result.reason}`);
      }
    } catch (err) {
      console.log(`⚠ ${test.name} - Setup failed: ${err.message}`);
      failed++;
    } finally {
      await test.cleanup();
    }
  }

  // Cleanup
  try {
    await fs.rm(TEST_DIR, { recursive: true, force: true });
  } catch {}

  // Summary
  console.log("\n" + "═".repeat(58));
  console.log(`\nTest Summary:`);
  console.log(`  \x1b[32m✓ Passed: ${passed}\x1b[0m`);
  console.log(`  \x1b[31m✗ Failed: ${failed}\x1b[0m`);
  console.log(`  Total: ${passed + failed}`);
  
  if (failed === 0) {
    console.log("\n\x1b[32m╔════════════════════════════════════════════════════════╗");
    console.log("║              All boundary tests passed! ✓              ║");
    console.log("╚════════════════════════════════════════════════════════╝\x1b[0m");
  } else {
    console.log("\n\x1b[31m╔════════════════════════════════════════════════════════╗");
    console.log("║              Some tests failed ✗                       ║");
    console.log("╚════════════════════════════════════════════════════════╝\x1b[0m");
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error("Fatal error:", err);
  process.exit(1);
});
