#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const readline = require("readline");
const https = require("https");

const SKILL_DIR = path.join(__dirname, "..", "skill");
const CLAUDE_SKILLS = path.join(
  process.env.HOME || process.env.USERPROFILE,
  ".claude",
  "skills",
  "introspect"
);
const PKG_NAME = "@umang-boss/introspect";

const CYAN = "\x1b[36m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const RED = "\x1b[31m";
const BOLD = "\x1b[1m";
const DIM = "\x1b[2m";
const RESET = "\x1b[0m";

function log(msg) {
  console.log(msg);
}

function banner() {
  log("");
  log(`${BOLD}${CYAN}  🔍 Introspect — Discover Your Developer DNA${RESET}`);
  log(`${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}`);
  log("");
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function checkPython() {
  try {
    execSync("python3 --version", { stdio: "pipe" });
    return true;
  } catch {
    return false;
  }
}

function checkClaude() {
  const claudeDir = path.join(
    process.env.HOME || process.env.USERPROFILE,
    ".claude"
  );
  return fs.existsSync(claudeDir);
}

function getLocalVersion() {
  try {
    return require("../package.json").version;
  } catch {
    return "unknown";
  }
}

function getInstalledVersion() {
  try {
    const versionFile = path.join(CLAUDE_SKILLS, ".introspect-version");
    if (fs.existsSync(versionFile)) {
      return fs.readFileSync(versionFile, "utf-8").trim();
    }
    // Fallback: check if installed at all
    if (fs.existsSync(path.join(CLAUDE_SKILLS, "SKILL.md"))) {
      return "unknown (pre-1.1.0)";
    }
    return null; // Not installed
  } catch {
    return null;
  }
}

function writeVersionFile(version) {
  try {
    const versionFile = path.join(CLAUDE_SKILLS, ".introspect-version");
    fs.writeFileSync(versionFile, version);
  } catch {
    // Non-critical
  }
}

function fetchLatestVersion() {
  return new Promise((resolve, reject) => {
    const url = `https://registry.npmjs.org/${encodeURIComponent(PKG_NAME)}/latest`;
    https
      .get(url, { headers: { Accept: "application/json" } }, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          try {
            const pkg = JSON.parse(data);
            resolve(pkg.version || null);
          } catch {
            resolve(null);
          }
        });
      })
      .on("error", () => resolve(null));
  });
}

function compareVersions(a, b) {
  // Returns: -1 if a < b, 0 if equal, 1 if a > b
  if (!a || !b || a === "unknown" || b === "unknown") return -1;
  const pa = a.replace(/^v/, "").split(".").map(Number);
  const pb = b.replace(/^v/, "").split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    const na = pa[i] || 0;
    const nb = pb[i] || 0;
    if (na > nb) return 1;
    if (na < nb) return -1;
  }
  return 0;
}

// ─── Commands ──────────────────────────────────────────────

function install() {
  banner();

  log(`${BOLD}  Checking prerequisites...${RESET}`);
  log("");

  const hasPython = checkPython();
  const hasClaude = checkClaude();

  log(
    `  ${hasPython ? GREEN + "✔" : RED + "✖"} Python 3${RESET}${
      hasPython ? "" : " — required for analysis engine"
    }`
  );
  log(
    `  ${hasClaude ? GREEN + "✔" : RED + "✖"} Claude Code (~/.claude/)${RESET}${
      hasClaude ? "" : " — required for session data"
    }`
  );
  log("");

  if (!hasClaude) {
    log(`${RED}  ✖ Claude Code not found. Install Claude Code first:${RESET}`);
    log(`    https://docs.anthropic.com/en/docs/claude-code`);
    log("");
    process.exit(1);
  }

  if (!hasPython) {
    log(`${RED}  ✖ Python 3 not found. Install it:${RESET}`);
    log(`    Ubuntu/Debian: sudo apt install python3`);
    log(`    macOS: brew install python3`);
    log(`    Android/Termux: pkg install python`);
    log("");
    process.exit(1);
  }

  if (fs.existsSync(CLAUDE_SKILLS)) {
    if (isSilent) {
      doInstall();
      return;
    }

    const installed = getInstalledVersion();
    const current = getLocalVersion();
    log(`${YELLOW}  ⚠ Introspect already installed at:${RESET}`);
    log(`    ${CLAUDE_SKILLS}`);
    if (installed) {
      log(`    ${DIM}Installed version: ${installed}${RESET}`);
      log(`    ${DIM}Package version:   ${current}${RESET}`);
    }
    log("");

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    rl.question(`  Overwrite with v${current}? (y/N) `, (answer) => {
      rl.close();
      if (answer.toLowerCase() === "y" || answer.toLowerCase() === "yes") {
        doInstall();
      } else {
        log(`\n${CYAN}  Skipped. Existing installation preserved.${RESET}\n`);
      }
    });
    return;
  }

  doInstall();
}

function doInstall() {
  const version = getLocalVersion();
  log(`${BOLD}  Installing v${version} to ~/.claude/skills/introspect ...${RESET}`);
  log("");

  try {
    copyDir(SKILL_DIR, CLAUDE_SKILLS);

    const reportsDir = path.join(CLAUDE_SKILLS, "reports");
    fs.mkdirSync(reportsDir, { recursive: true });

    // Write version tracker
    writeVersionFile(version);

    log(`${GREEN}  ✔ Installed v${version} successfully!${RESET}`);
    log("");
    log(`${BOLD}  Location:${RESET} ${CLAUDE_SKILLS}`);
    log("");
    log(`${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}`);
    log("");
    log(`${BOLD}  How to use:${RESET}`);
    log("");
    log(`  Open Claude Code and say:`);
    log(`  ${GREEN}> introspect my last 7 days${RESET}`);
    log(`  ${GREEN}> analyze my sessions from the past month${RESET}`);
    log(`  ${GREEN}> give me my developer DNA${RESET}`);
    log("");
    log(`  Or run directly:`);
    log(
      `  ${GREEN}$ python3 ~/.claude/skills/introspect/scripts/analyze.py --days 7 --sessions 10${RESET}`
    );
    log("");
    log(`  ${DIM}Check for updates: npx ${PKG_NAME} update${RESET}`);
    log("");
    log(`${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}`);
    log(`${BOLD}  Happy introspecting! 🔍🧠${RESET}`);
    log("");
  } catch (err) {
    log(`${RED}  ✖ Installation failed: ${err.message}${RESET}`);
    process.exit(1);
  }
}

function uninstall() {
  banner();

  if (!fs.existsSync(CLAUDE_SKILLS)) {
    log(`${YELLOW}  Introspect is not installed.${RESET}\n`);
    process.exit(0);
  }

  log(`${BOLD}  Removing from ~/.claude/skills/introspect ...${RESET}`);
  fs.rmSync(CLAUDE_SKILLS, { recursive: true, force: true });
  log(`${GREEN}  ✔ Uninstalled successfully.${RESET}\n`);
}

async function update() {
  banner();

  const installed = getInstalledVersion();
  const localPkg = getLocalVersion();

  log(`${BOLD}  Checking for updates...${RESET}`);
  log("");

  if (!installed) {
    log(`${YELLOW}  Introspect is not installed.${RESET}`);
    log(`  Run: ${GREEN}npx ${PKG_NAME}${RESET} to install.`);
    log("");
    process.exit(0);
  }

  log(`  📦 Installed: ${BOLD}${installed}${RESET}`);
  log(`  📦 Package:   ${BOLD}${localPkg}${RESET}`);

  // Check npm registry for latest
  log(`  🌐 Checking npm registry...`);
  const latest = await fetchLatestVersion();

  if (latest) {
    log(`  📦 Latest:    ${BOLD}${latest}${RESET}`);
  } else {
    log(`  ${YELLOW}⚠ Could not reach npm registry. Using package version.${RESET}`);
  }
  log("");

  const targetVersion = latest || localPkg;
  const cmp = compareVersions(installed, targetVersion);

  if (cmp >= 0 && installed !== "unknown (pre-1.1.0)") {
    log(`${GREEN}  ✔ Already up to date! (v${installed})${RESET}`);
    log("");
    return;
  }

  log(`${CYAN}  ⬆ Update available: ${installed} → ${targetVersion}${RESET}`);
  log("");

  // If the local package is already the latest, just copy files
  if (compareVersions(localPkg, targetVersion) >= 0) {
    log(`${BOLD}  Updating skill files...${RESET}`);
    try {
      copyDir(SKILL_DIR, CLAUDE_SKILLS);
      const reportsDir = path.join(CLAUDE_SKILLS, "reports");
      fs.mkdirSync(reportsDir, { recursive: true });
      writeVersionFile(localPkg);

      log(`${GREEN}  ✔ Updated to v${localPkg}!${RESET}`);
      log("");
    } catch (err) {
      log(`${RED}  ✖ Update failed: ${err.message}${RESET}`);
      process.exit(1);
    }
  } else {
    // Need to fetch latest from npm first
    log(`  ${BOLD}To get the latest version, run:${RESET}`);
    log("");
    log(`  ${GREEN}npx ${PKG_NAME}@latest update${RESET}`);
    log("");
    log(`  ${DIM}This downloads the latest package from npm and updates your skill.${RESET}`);
    log("");
  }
}

async function checkVersion() {
  banner();

  const installed = getInstalledVersion();
  const localPkg = getLocalVersion();

  log(`  📦 Package version:   ${BOLD}${localPkg}${RESET}`);
  log(`  📦 Installed version: ${BOLD}${installed || "not installed"}${RESET}`);

  log(`  🌐 Checking npm...`);
  const latest = await fetchLatestVersion();

  if (latest) {
    log(`  📦 Latest on npm:     ${BOLD}${latest}${RESET}`);

    if (installed && compareVersions(installed, latest) >= 0 && !installed.startsWith("unknown")) {
      log("");
      log(`  ${GREEN}✔ Up to date!${RESET}`);
    } else {
      log("");
      log(`  ${YELLOW}⬆ Update available!${RESET}`);
      log(`  Run: ${GREEN}npx ${PKG_NAME}@latest update${RESET}`);
    }
  } else {
    log(`  ${YELLOW}⚠ Could not reach npm registry${RESET}`);
  }
  log("");
}

// ─── CLI Router ────────────────────────────────────────────

const args = process.argv.slice(2);
const isSilent = args.includes("--silent");
const hasHelp = args.includes("--help") || args.includes("-h");
const hasVersion = args.includes("--version") || args.includes("-v");
const command = hasHelp
  ? "--help"
  : hasVersion
    ? "--version"
    : args.filter((a) => !a.startsWith("--"))[0] || "install";

switch (command) {
  case "install":
  case "i":
    install();
    break;
  case "uninstall":
  case "remove":
    uninstall();
    break;
  case "update":
  case "upgrade":
  case "u":
    update();
    break;
  case "check":
  case "status":
    checkVersion();
    break;
  case "--help":
  case "-h":
    banner();
    log(`${BOLD}  Usage:${RESET}`);
    log("");
    log(`    npx ${PKG_NAME}              Install skill to Claude`);
    log(`    npx ${PKG_NAME} install      Install skill to Claude`);
    log(`    npx ${PKG_NAME} update       Update to latest version`);
    log(`    npx ${PKG_NAME} check        Check installed vs latest version`);
    log(`    npx ${PKG_NAME} uninstall    Remove skill from Claude`);
    log(`    npx ${PKG_NAME} --version    Show package version`);
    log(`    npx ${PKG_NAME} --help       Show this help`);
    log("");
    log(`${DIM}  Tip: Use @latest to ensure you have the newest package:${RESET}`);
    log(`  ${GREEN}npx ${PKG_NAME}@latest update${RESET}`);
    log("");
    break;
  case "--version":
  case "-v":
    log(getLocalVersion());
    break;
  default:
    log(`${RED}Unknown command: ${command}${RESET}`);
    log(`Run: npx ${PKG_NAME} --help`);
    process.exit(1);
}
