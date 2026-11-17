#!/usr/bin/env node
/**
 * memory-store skill installer — interactive
 *
 * One-command install from git repo. Two modes:
 *   1. Standard — scan home directory for supported AI agents, list them, let user choose
 *   2. Manual  — user specifies the target directory path
 *
 * Usage:
 *   node scripts/install.js                  Interactive: choose mode → select targets → install
 *   node scripts/install.js --all            Non-interactive: install to ALL detected agents
 *   node scripts/install.js --agent claude   Non-interactive: install to specific agent(s)
 *   node scripts/install.js --target <path>  Non-interactive: install to a custom directory
 *   node scripts/install.js --update          Update all detected existing installations
 *   node scripts/install.js --check           Verify installed artifacts without writing
 *   node scripts/install.js --dry-run         Preview installation without writing
 *   node scripts/install.js --memory-profile explicit
 *                                              Configure memory policy during installation
 *   node scripts/install.js --list           Just list detected agents
 *   node scripts/install.js --help           Show help
 *
 * Detected platforms:
 *   claude, codex, gemini, opencode, workbuddy, cursor, windsurf, qoderworkcn, trae-cn
 */

const fs = require("fs");
const path = require("path");
const os = require("os");
const crypto = require("crypto");
const readline = require("readline");

function configuredRoot(envName, fallbackDir) {
  const configured = process.env[envName];
  return configured && configured.trim()
    ? path.resolve(configured.trim())
    : path.join(os.homedir(), fallbackDir);
}

// =============================================================================
// Agent platform definitions
// =============================================================================

const AGENT_PLATFORMS = [
  {
    name: "claude",
    label: "Claude Code",
    configDir: configuredRoot("CLAUDE_CONFIG_DIR", ".claude"),
    get skillDir() {
      return path.join(this.configDir, "skills", "memory-store");
    },
    detect() {
      return Boolean(process.env.CLAUDE_CONFIG_DIR?.trim()) || fs.existsSync(this.configDir);
    },
  },
  {
    name: "codex",
    label: "Codex",
    configDir: configuredRoot("CODEX_CONFIG_DIR", ".agents"),
    get skillDir() {
      return path.join(this.configDir, "skills", "memory-store");
    },
    detect() {
      return Boolean(process.env.CODEX_CONFIG_DIR?.trim()) || fs.existsSync(this.configDir);
    },
  },
  {
    name: "gemini",
    label: "Gemini CLI",
    skillDir: path.join(os.homedir(), ".gemini", "skills", "memory-store"),
    detect: () => fs.existsSync(path.join(os.homedir(), ".gemini")),
  },
  {
    name: "opencode",
    label: "OpenCode",
    skillDir: path.join(os.homedir(), ".config", "opencode", "skills", "memory-store"),
    detect: () =>
      fs.existsSync(path.join(os.homedir(), ".config", "opencode")),
  },
  {
    name: "workbuddy",
    label: "WorkBuddy / Antigravity",
    skillDir: path.join(os.homedir(), ".workbuddy", "skills", "memory-store"),
    detect: () => fs.existsSync(path.join(os.homedir(), ".workbuddy")),
  },
  {
    name: "cursor",
    label: "Cursor",
    skillDir: path.join(os.homedir(), ".cursor", "skills", "memory-store"),
    detect: () => fs.existsSync(path.join(os.homedir(), ".cursor")),
  },
  {
    name: "windsurf",
    label: "Windsurf",
    skillDir: path.join(os.homedir(), ".windsurf", "skills", "memory-store"),
    detect: () => fs.existsSync(path.join(os.homedir(), ".windsurf")),
  },
  {
    name: "qoderworkcn",
    label: "QoderWorkCN",
    skillDir: path.join(os.homedir(), ".qoderworkcn", "skills", "memory-store"),
    detect: () => fs.existsSync(path.join(os.homedir(), ".qoderworkcn")),
  },
  {
    name: "trae-cn",
    label: "Trae CN",
    skillDir: path.join(os.homedir(), ".trae-cn", "skills", "memory-store"),
    detect: () => fs.existsSync(path.join(os.homedir(), ".trae-cn")),
  },
];

// =============================================================================
// Helpers
// =============================================================================

const SKILL_DIR = path.resolve(__dirname, "..");
const MEMORY_PROFILES = ["off", "explicit", "balanced", "proactive"];

const INSTALL_GROUPS = [
  { source: "SKILL.md", label: "SKILL.md" },
  { source: "scripts", label: "scripts/", filter: (name) => name.endsWith(".js") },
  { source: "references", label: "references/" },
  { source: "examples", label: "examples/" },
  { source: "agents", label: "agents/" },
];

function getPackageVersion() {
  try {
    return JSON.parse(fs.readFileSync(path.join(SKILL_DIR, "package.json"), "utf8")).version;
  } catch {
    return "unknown";
  }
}

function listFiles(root, filter = () => true, relativeDir = "") {
  if (!fs.existsSync(root)) return [];
  const files = [];
  for (const name of fs.readdirSync(root)) {
    if (!filter(name)) continue;
    const absolute = path.join(root, name);
    const relative = path.join(relativeDir, name);
    if (fs.statSync(absolute).isDirectory()) {
      files.push(...listFiles(absolute, filter, relative));
    } else {
      files.push(relative);
    }
  }
  return files;
}

function installArtifacts() {
  const artifacts = [];
  for (const group of INSTALL_GROUPS) {
    const source = path.join(SKILL_DIR, group.source);
    if (!fs.existsSync(source)) continue;
    if (fs.statSync(source).isDirectory()) {
      for (const relative of listFiles(source, group.filter)) {
        artifacts.push(path.join(group.source, relative));
      }
    } else {
      artifacts.push(group.source);
    }
  }
  return artifacts.sort();
}

function fileHash(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function verifyTarget(targetDir) {
  const dst = path.resolve(targetDir);
  const missing = [];
  const mismatched = [];
  const artifacts = installArtifacts();

  for (const relative of artifacts) {
    const source = path.join(SKILL_DIR, relative);
    const installed = path.join(dst, relative);
    if (!fs.existsSync(installed)) {
      missing.push(relative);
    } else if (fileHash(source) !== fileHash(installed)) {
      mismatched.push(relative);
    }
  }

  return {
    ok: missing.length === 0 && mismatched.length === 0,
    target: dst,
    version: getPackageVersion(),
    checked: artifacts.length,
    missing,
    mismatched,
  };
}

function printVerification(report) {
  if (report.ok) {
    console.log(`    ✅ Verified ${report.checked} artifact(s), source v${report.version}`);
    return;
  }
  console.error(`    ❌ Installation is stale or incomplete: ${report.target}`);
  if (report.missing.length > 0) {
    console.error(`       Missing: ${report.missing.join(", ")}`);
  }
  if (report.mismatched.length > 0) {
    console.error(`       Changed: ${report.mismatched.join(", ")}`);
  }
}

function copyDir(src, dst, filter = () => true) {
  fs.mkdirSync(dst, { recursive: true });
  let count = 0;
  for (const name of fs.readdirSync(src)) {
    if (!filter(name)) continue;
    const s = path.join(src, name);
    const d = path.join(dst, name);
    if (fs.statSync(s).isDirectory()) {
      count += copyDir(s, d, filter);
    } else {
      fs.copyFileSync(s, d);
      count++;
    }
  }
  return count;
}

function detectAgents() {
  const found = [];
  for (const agent of AGENT_PLATFORMS) {
    try {
      if (agent.detect()) {
        found.push({ ...agent, installed: isInstalledTarget(agent.skillDir) });
      }
    } catch {
      // skip if detection throws
    }
  }
  return found;
}

function isInstalledTarget(targetDir) {
  const dst = path.resolve(targetDir);
  return fs.existsSync(path.join(dst, "SKILL.md")) &&
    fs.existsSync(path.join(dst, "scripts", "memory_cli.js"));
}

function installTo(targetDir, { dryRun = false, action = "install" } = {}) {
  const dst = path.resolve(targetDir);
  const artifacts = installArtifacts();
  const actionLabel = action === "update" ? "update" : "install";
  console.log(`  📁 ${dryRun ? `Would ${actionLabel}` : `${actionLabel === "update" ? "Updating" : "Installing"}`} ${actionLabel === "update" ? "in" : "to"}: ${dst}`);

  if (dryRun) {
    console.log(`    🔎 Would copy and verify ${artifacts.length} artifact(s), source v${getPackageVersion()}`);
    return { ok: true, dryRun: true, target: dst, checked: artifacts.length };
  }

  fs.mkdirSync(dst, { recursive: true });
  for (const group of INSTALL_GROUPS) {
    const source = path.join(SKILL_DIR, group.source);
    if (!fs.existsSync(source)) continue;
    const target = path.join(dst, group.source);
    let count;
    if (fs.statSync(source).isDirectory()) {
      count = copyDir(source, target, group.filter);
    } else {
      fs.copyFileSync(source, target);
      count = 1;
    }
    console.log(`    ✅ ${group.label}${count > 1 ? ` (${count} files)` : ""}`);
  }

  const report = verifyTarget(dst);
  printVerification(report);
  if (!report.ok) {
    throw new Error("post-install verification failed");
  }
  return report;
}

function updateTo(targetDir, { dryRun = false } = {}) {
  const dst = path.resolve(targetDir);
  if (!isInstalledTarget(dst)) {
    throw new Error(`no existing Memory Store skill installation at ${dst}`);
  }

  const current = verifyTarget(dst);
  if (current.ok) {
    console.log(`  ✅ Already current: ${dst} (v${current.version})`);
    return { ...current, changed: false, needsUpdate: false, dryRun };
  }

  return {
    ...installTo(dst, { dryRun, action: "update" }),
    changed: !dryRun,
    needsUpdate: true,
  };
}

function configureMemoryProfile(profile, { dryRun = false } = {}) {
  if (!profile) return;
  if (!MEMORY_PROFILES.includes(profile)) {
    throw new Error(`Invalid memory profile '${profile}'. Choose: ${MEMORY_PROFILES.join(", ")}`);
  }
  const storeDir = path.join(os.homedir(), ".memory-store");
  const configPath = path.join(storeDir, "config.json");
  if (dryRun) {
    console.log(`    🔎 Would set memory profile '${profile}' in ${configPath}`);
    return;
  }
  fs.mkdirSync(storeDir, { recursive: true });
  const tempPath = `${configPath}.${process.pid}.${crypto.randomBytes(4).toString("hex")}.tmp`;
  fs.writeFileSync(tempPath, JSON.stringify({
    schema_version: 1,
    profile,
    configured_at: new Date().toISOString(),
  }, null, 2) + "\n", "utf8");
  fs.renameSync(tempPath, configPath);
  console.log(`    ✅ Memory profile '${profile}' configured in ${configPath}`);
}

// =============================================================================
// Interactive helpers
// =============================================================================

function ask(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function printBanner() {
  console.log(`
╔══════════════════════════════════════════════╗
║        🧠 Memory Store Skill Installer       ║
║   Conversation memory for multi-agent AI     ║
╚══════════════════════════════════════════════╝
`);
}

// =============================================================================
// Main
// =============================================================================

async function main(args = process.argv.slice(2)) {
  const booleanOptions = new Set(["--list", "--all", "--update", "--check", "--dry-run", "--help", "-h"]);
  const valuedOptions = new Set(["--agent", "--target", "--memory-profile"]);
  for (let i = 0; i < args.length; i++) {
    const option = args[i];
    if (booleanOptions.has(option)) continue;
    if (valuedOptions.has(option)) {
      const value = args[i + 1];
      if (value === undefined || value.startsWith("--")) {
        throw new Error(`Missing value for ${option}.`);
      }
      i++;
      continue;
    }
    throw new Error(`Unknown option '${option}'. Run with --help for usage.`);
  }
  const flags = {
    list: args.includes("--list"),
    all: args.includes("--all"),
    update: args.includes("--update"),
    check: args.includes("--check"),
    dryRun: args.includes("--dry-run"),
    help: args.includes("--help") || args.includes("-h"),
    agents: [],
    target: null,
    memoryProfile: null,
  };

  // Parse valued options.
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--agent" && i + 1 < args.length && !args[i + 1].startsWith("--")) {
      flags.agents.push(...args[i + 1].split(",").map((a) => a.trim().toLowerCase()));
      i++;
    } else if (args[i] === "--target" && i + 1 < args.length && !args[i + 1].startsWith("--")) {
      flags.target = args[i + 1];
      i++;
    } else if (args[i] === "--memory-profile" && i + 1 < args.length && !args[i + 1].startsWith("--")) {
      flags.memoryProfile = args[i + 1].trim().toLowerCase();
      i++;
    }
  }

  if (flags.memoryProfile && !MEMORY_PROFILES.includes(flags.memoryProfile)) {
    throw new Error(`Invalid memory profile '${flags.memoryProfile}'. Choose: ${MEMORY_PROFILES.join(", ")}.`);
  }

  const selectorCount = Number(flags.all) + Number(flags.agents.length > 0) + Number(Boolean(flags.target));
  if (selectorCount > 1) {
    throw new Error("--all, --agent, and --target are mutually exclusive selectors.");
  }
  if (flags.check && (flags.dryRun || flags.update)) {
    throw new Error("--check cannot be combined with --dry-run or --update.");
  }
  if (flags.list && (selectorCount > 0 || flags.update || flags.check || flags.dryRun)) {
    throw new Error("--list cannot be combined with install, update, check, or dry-run options.");
  }
  if (flags.memoryProfile && (flags.list || flags.update || flags.check)) {
    throw new Error("--memory-profile is available only during installation; use `memory-store mode <profile>` afterward.");
  }

  if (flags.help) {
    console.log(`
Memory Store Skill Installer — One-command install

Usage:
  node scripts/install.js                    Interactive: choose mode → select targets → install
  node scripts/install.js --all              Install to ALL detected agents (non-interactive)
  node scripts/install.js --agent claude     Install to specific agent(s) (non-interactive)
  node scripts/install.js --target <path>    Install to a custom directory (non-interactive)
  node scripts/install.js --update [selector]
                                            Update existing installation(s) from this package
  node scripts/install.js --check [selector] Verify installed files against this source
  node scripts/install.js --dry-run [selector]
                                            Preview without creating or changing files
  node scripts/install.js --memory-profile <profile>
                                            Set off, explicit, balanced, or proactive
  node scripts/install.js --list             List detected agents only
  node scripts/install.js --help             Show this help

Selectors:
  --all, --agent <name[,name]>, or --target <path>

Update after upgrading the npm package:
  npm i memory-store-skill@latest
  npx memory-store-update

Configuration roots:
  CLAUDE_CONFIG_DIR and CODEX_CONFIG_DIR override the corresponding default
  configuration roots; skills install below <config-root>/skills/memory-store.

Detected platforms:
  claude      — Claude Code
  codex       — Codex
  gemini      — Gemini CLI
  opencode    — OpenCode
  workbuddy   — WorkBuddy / Antigravity
  cursor      — Cursor
  windsurf    — Windsurf
  qoderworkcn — QoderWorkCN
  trae-cn     — Trae CN
`);
    process.exit(0);
  }

  // --- Detect agents ---
  const found = detectAgents();

  const requested = [];
  for (const name of flags.agents) {
    const agent = AGENT_PLATFORMS.find((candidate) => candidate.name === name);
    if (agent) {
      requested.push({ agent, dir: agent.skillDir });
    } else {
      console.error(`  ❌ Unknown agent "${name}". Supported: ${AGENT_PLATFORMS.map((a) => a.name).join(", ")}`);
    }
  }

  function selectedTargets() {
    if (flags.target) {
      const dir = path.resolve(flags.target);
      return [{ agent: { name: "manual", label: "Manual" }, dir }];
    }
    if (flags.agents.length > 0) return requested;
    return found.map((agent) => ({ agent, dir: agent.skillDir }));
  }

  if (flags.check) {
    printBanner();
    const targets = selectedTargets();
    if (targets.length === 0) {
      console.error("No installation targets selected or detected.");
      process.exitCode = 1;
      return;
    }
    let validCount = 0;
    for (const { agent, dir } of targets) {
      console.log(`  🔎 Checking ${agent.label}: ${path.resolve(dir)}`);
      const report = verifyTarget(dir);
      printVerification(report);
      if (report.ok) validCount++;
    }
    console.log(`\n${validCount === targets.length ? "✅" : "❌"} Verification complete (${validCount}/${targets.length}).`);
    process.exitCode = validCount === targets.length ? 0 : 1;
    return;
  }

  if (flags.update) {
    printBanner();
    const selected = selectedTargets();
    const targets = selected.filter(({ dir }) => isInstalledTarget(dir));
    const missing = selected.filter(({ dir }) => !isInstalledTarget(dir));

    for (const { agent, dir } of missing) {
      console.error(`  ❌ ${agent.label}: no existing installation at ${path.resolve(dir)}`);
    }
    if (targets.length === 0) {
      console.error("No existing Memory Store skill installations selected or detected.");
      process.exitCode = 1;
      return;
    }

    console.log(`${flags.dryRun ? "🔎 Previewing updates for" : "⬆️  Updating"} ${targets.length} existing target(s) from package v${getPackageVersion()}...\n`);
    let successCount = 0;
    let changedCount = 0;
    for (const { agent, dir } of targets) {
      try {
        const report = updateTo(dir, { dryRun: flags.dryRun });
        successCount++;
        if (flags.dryRun ? report.needsUpdate : report.changed) changedCount++;
      } catch (e) {
        console.error(`    ❌ ${agent.label}: ${e.message}`);
      }
    }

    const expectedCount = targets.length + missing.length;
    const complete = successCount === expectedCount;
    console.log(`\n${complete ? "✅" : "❌"} ${flags.dryRun ? "Update preview" : "Update"} complete (${successCount}/${expectedCount}); ${changedCount} target(s) ${flags.dryRun ? "need update" : "changed"}.`);
    if (!flags.dryRun && successCount > 0) {
      console.log("   Restart your agent sessions for the updated skill to take effect.");
    }
    process.exitCode = complete ? 0 : 1;
    return;
  }

  // --- Non-interactive modes ---
  if (flags.list) {
    printBanner();
    if (found.length === 0) {
      console.log("No AI agent platforms detected on this system.\n");
    } else {
      console.log(`Detected ${found.length} AI agent platform(s):\n`);
      for (const agent of found) {
        const status = agent.installed ? "📦 installed" : "🆕 available";
        console.log(`  ${agent.label.padEnd(22)} ${status}`);
        console.log(`    ${agent.skillDir}`);
      }
    }
    return;
  }

  if (flags.all || flags.target) {
    // Non-interactive: install to all detected
    printBanner();
    const targets = selectedTargets();
    if (targets.length === 0) {
      console.error("No AI agent platforms detected. Nothing to install.");
      process.exitCode = 1;
      return;
    }
    console.log(`${flags.dryRun ? "🔎 Previewing" : "🔍 Installing to"} ${targets.length} target(s)...\n`);
    let successCount = 0;
    for (const { agent, dir } of targets) {
      try {
        installTo(dir, { dryRun: flags.dryRun });
        successCount++;
      } catch (e) {
        console.error(`    ❌ ${agent.label}: ${e.message}`);
      }
    }
    if (successCount > 0) configureMemoryProfile(flags.memoryProfile, { dryRun: flags.dryRun });
    console.log(`\n${successCount === targets.length ? "✅" : "❌"} ${flags.dryRun ? "Preview" : "Installation"} complete (${successCount}/${targets.length}).`);
    if (!flags.dryRun && successCount > 0) console.log("   Restart your agent sessions for the skill to take effect.");
    process.exitCode = successCount === targets.length ? 0 : 1;
    return;
  }

  if (flags.agents.length > 0) {
    // Non-interactive: install to specified agents
    printBanner();
    console.log(`${flags.dryRun ? "🔎 Previewing" : "🔍 Installing to"} specified agent(s): ${flags.agents.join(", ")}\n`);
    let successCount = 0;
    for (const { agent, dir } of requested) {
      try {
        installTo(dir, { dryRun: flags.dryRun });
        successCount++;
      } catch (e) {
        console.error(`    ❌ ${agent.label}: ${e.message}`);
      }
    }
    if (successCount > 0) configureMemoryProfile(flags.memoryProfile, { dryRun: flags.dryRun });
    console.log(`\n${successCount === flags.agents.length ? "✅" : "❌"} ${flags.dryRun ? "Preview" : "Installation"} complete (${successCount}/${flags.agents.length}).`);
    if (!flags.dryRun && successCount > 0) console.log("   Restart your agent sessions for the skill to take effect.");
    process.exitCode = successCount === flags.agents.length ? 0 : 1;
    return;
  }

  // =========================================================================
  // Interactive mode
  // =========================================================================
  printBanner();

  console.log("This installer will copy the Memory Store skill to your AI agent platform(s).\n");

  // --- Step 1: Choose installation mode ---
  console.log("─── Installation Mode ───");
  console.log("  1. Standard — Scan home directory, select agents to install");
  console.log("  2. Manual  — Specify target directory path");
  const modeAnswer = await ask("\nChoose [1/2] (default: 1): ");
  const isManual = modeAnswer === "2";

  let targets = []; // Array of { agent, dir }

  if (isManual) {
    // --- Manual mode ---
    console.log("\n─── Manual Install ───");
    const manualPath = await ask("Target path: ");
    if (!manualPath) {
      console.log("❌ Path is required. Aborting.");
      process.exit(1);
    }
    const resolvedPath = path.resolve(manualPath);
    console.log(`\n  Path: ${resolvedPath}`);

    // Installation creates the directory only after confirmation.
    if (!fs.existsSync(resolvedPath)) {
      console.log(`  ${flags.dryRun ? "Would create" : "Will create"} after confirmation.`);
    }

    targets.push({ agent: { name: "manual", label: "Manual", skillDir: resolvedPath }, dir: resolvedPath });
  } else {
    // --- Standard mode ---
    console.log("\n─── Scanning System ───");

    if (found.length === 0) {
      console.log("  ⚠️  No AI agent platforms detected on this system.");
      console.log("  Switching to manual mode. Please specify the target path.\n");
      const manualPath = await ask("Target path: ");
      if (!manualPath) {
        console.log("❌ Aborting.");
        process.exit(1);
      }
      const resolvedPath = path.resolve(manualPath);
      targets.push({ agent: { name: "manual", label: "Manual", skillDir: resolvedPath }, dir: resolvedPath });
    } else {
      console.log(`  Found ${found.length} AI agent platform(s):\n`);
      for (let i = 0; i < found.length; i++) {
        const agent = found[i];
        const status = agent.installed ? "📦 installed" : "🆕 available";
        console.log(`  ${(i + 1).toString().padEnd(3)} ${agent.label.padEnd(22)} ${status}`);
        console.log(`      ${agent.skillDir}`);
      }

      console.log("\n  Select targets:");
      console.log("  - Enter numbers (e.g. 1,3,5) to select specific agents");
      console.log("  - Enter 'all' to install to all agents");
      console.log("  - Enter '0' to switch to manual mode");
      const selection = await ask("\nYour choice: ");

      if (selection.toLowerCase() === "all") {
        targets = found.map((a) => ({ agent: a, dir: a.skillDir }));
      } else if (selection === "0") {
        // Switch to manual
        const manualPath = await ask("Target path: ");
        if (manualPath) {
          const resolvedPath = path.resolve(manualPath);
          targets.push({ agent: { name: "manual", label: "Manual", skillDir: resolvedPath }, dir: resolvedPath });
        }
      } else {
        const indices = selection
          .split(",")
          .map((s) => parseInt(s.trim(), 10))
          .filter((n) => !isNaN(n) && n >= 1 && n <= found.length);
        for (const idx of indices) {
          const agent = found[idx - 1];
          targets.push({ agent, dir: agent.skillDir });
        }
      }
    }
  }

  if (targets.length === 0) {
    console.log("\n❌ No targets selected. Aborting.");
    process.exit(1);
  }

  // --- Step 2: Confirm targets ---
  console.log("\n─── Target Summary ───");
  for (const { agent, dir } of targets) {
    console.log(`  📦 ${agent.label.padEnd(22)} → ${dir}`);
  }

  // --- Step 3: Choose memory policy ---
  console.log("\n─── Memory Policy ───");
  console.log("  1. explicit  — Store only when the user explicitly asks (recommended)");
  console.log("  2. balanced  — Automatically keep selected decisions, fixes, workflows, and preferences");
  console.log("  3. proactive — Automatically keep a broader set of durable memories");
  console.log("  4. off       — Disable automatic recall and storage");
  const profileAnswer = await ask("\nChoose [1/2/3/4] (default: 1): ");
  const profileChoices = { "1": "explicit", "2": "balanced", "3": "proactive", "4": "off" };
  flags.memoryProfile = profileChoices[profileAnswer || "1"] || "explicit";
  console.log(`  Selected memory profile: ${flags.memoryProfile}`);

  // --- Step 4: Confirm and execute ---
  const confirm = await ask("\nProceed with installation? [Y/n] (default: Y): ");
  if (confirm.toLowerCase() === "n") {
    console.log("❌ Installation cancelled.");
    process.exit(0);
  }

  console.log(`\n─── ${flags.dryRun ? "Preview" : "Installing"} ───\n`);

  let successCount = 0;
  for (const { agent, dir } of targets) {
    try {
      const ok = installTo(dir, { dryRun: flags.dryRun });
      if (ok) {
        successCount++;
      }
    } catch (e) {
      console.error(`    ❌ ${agent.label}: ${e.message}`);
    }
  }

  // --- Summary ---
  if (successCount > 0) configureMemoryProfile(flags.memoryProfile, { dryRun: flags.dryRun });
  console.log(`\n${successCount === targets.length ? "✅" : "❌"} ${flags.dryRun ? "Preview" : "Installation"} complete (${successCount}/${targets.length} targets).`);
  if (!flags.dryRun && successCount > 0) {
    console.log("   Restart your agent sessions for the skill to take effect.");
  }
  process.exitCode = successCount === targets.length ? 0 : 1;
}

if (require.main === module) {
  main().catch((e) => {
    console.error("Fatal error:", e);
    process.exit(1);
  });
}

module.exports = { main };
