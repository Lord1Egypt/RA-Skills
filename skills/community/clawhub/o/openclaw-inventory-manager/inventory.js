const fs = require("fs");
const path = require("path");
const os = require("os");
const readline = require("readline");
const logger = require("./utils/logger");
const scanner = require("./utils/scanner");
const securityScrubber = require("./utils/securityScrubber");
const sourceDetector = require("./utils/sourceDetector");
const gitManager = require("./utils/gitManager");
const manifestGenerator = require("./utils/manifestGenerator");

/**
 * OpenClaw Skill Inventory Manager (v1.0.0)
 * Main Controller & CLI Router
 *
 * SECURITY: This tool only reads SKILL.md metadata files and generates
 * manifest reports. It does NOT collect, transmit, or store credentials.
 */

const CONFIG_PATH = path.join(os.homedir(), ".openclaw", "inventory.json");

function resolveManifestPath(config) {
  let manifestPath = config.manifestPath || "~/.openclaw/SKILLS_MANIFEST.json";
  
  if (manifestPath.startsWith("~")) {
    manifestPath = path.join(os.homedir(), manifestPath.slice(1));
  } else if (!path.isAbsolute(manifestPath)) {
    manifestPath = path.resolve(path.dirname(CONFIG_PATH), manifestPath);
  }
  
  return manifestPath;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    throw new Error("Configuration not found. Please run 'inventory init' first.");
  }
  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
    config.manifestPath = resolveManifestPath(config);
    return config;
  } catch (e) {
    throw new Error(`Failed to parse inventory.json: ${e.message}`);
  }
}

async function run() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "init":
      await handleInit(args.slice(1));
      break;
    case "bootstrap":
      await handleBootstrap();
      break;
    case "status":
      await handleStatus();
      break;
    case "sync":
      await handleSync(args.slice(1));
      break;
    case "list":
      await handleList();
      break;
    default:
      showHelp();
  }
}

async function handleBootstrap() {
  console.log(`\x1b[36m
  █   █  █  █  █▀▀  █▀▀█  █▀▀      █▀▀█  █▀▀█  █▀▀  █  █     █▀▀█  █▀▀█  █▀▀█  █▀▄▀█
  █   █  █▀▀█  █▀▀  █▄▄▀  █▀▀      █▄▄█  █▄▄▀  █▀▀  █  █     █▀▀▄  █▄▄▀  █  █  █ █ █
   ▀▄▀   ▀  ▀  ▀▀▀  ▀  ▀  ▀▀▀      ▀  ▀  ▀  ▀  ▀▀▀  ▀▀▀▀     ▀▀▀▀  ▀  ▀  ▀▀▀▀  ▀   ▀
  \x1b[0m`);
  logger.header("Where are you from - Guided Setup");
  logger.info("Welcome! Let's get your skill inventory sorted in 3 simple steps.");

  // 1. Config Check/Creation
  const configDir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true });
  
  if (!fs.existsSync(CONFIG_PATH)) {
    const defaultConfig = {
      searchRoots: ["~/.openclaw/skills", "./skills"],
      maxDepth: 5,
      excludedDirs: ["node_modules", ".git", "dist", ".cache"],
      maskPatterns: ["sk-", "ghp_", "hf_", "AIza", "Bearer"],
      autoPush: false,
      manifestPath: "~/.openclaw/SKILLS_MANIFEST.json"
    };
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(defaultConfig, null, 2));
    logger.success("STEP 1: Default configuration created (~/.openclaw/inventory.json).");
  } else {
    logger.info("STEP 1: Configuration already exists. Skipping.");
  }

  // 2. Git Check/Initialization
  logger.info("STEP 2: Preparing local Git tracking...");
  gitManager.init(process.cwd());

  // 3. Initial Scan and Report
  logger.info("STEP 3: Performing your FIRST-EVER skill audit...");
  await handleSync([]);
  
  console.log("\n\x1b[32m✔ SUCCESS!\x1b[0m Your skill inventory is ready.");
  console.log("Check \x1b[33mSKILLS_MANIFEST.md\x1b[0m in your current folder to see what I found!");
  console.log("\nNext Steps: Run \x1b[36minventory sync --push\x1b[0m to save this to GitHub.");
}

async function handleInit(args) {
  logger.header("Initializing Inventory Manager");
  const remoteUrl = args[0];
  
  // 1. Create config directory if not exists
  const configDir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  // 2. Create default config if not exists
  if (!fs.existsSync(CONFIG_PATH)) {
    const defaultConfig = {
      searchRoots: ["~/.openclaw/skills", "./skills"],
      maxDepth: 5,
      excludedDirs: ["node_modules", ".git", "dist", ".cache"],
      maskPatterns: ["sk-", "ghp_", "hf_", "AIza", "Bearer"],
      autoPush: false,
      manifestPath: "~/.openclaw/SKILLS_MANIFEST.json"
    };
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(defaultConfig, null, 2));
    logger.success(`Config created at ${CONFIG_PATH}`);
  }

  // 3. Initialize Git in current workspace
  gitManager.init(process.cwd(), remoteUrl);
  logger.success("Initialization complete.");
}

async function handleStatus() {
  logger.header("Inventory Status Check");
  const config = loadConfig();
  const skills = scanner.scan(config.searchRoots, {
    maxDepth: config.maxDepth,
    excludedDirs: config.excludedDirs
  });

  const changed = gitManager.status(process.cwd(), config.manifestPath);
  if (changed) {
    logger.warn("Changes detected in local skills. Run 'inventory sync' to update manifest.");
  } else {
    logger.success("Inventory is up to date with last commit.");
  }

  console.log(`\nDetected Skills: ${skills.length}`);
  skills.forEach(s => {
    const source = sourceDetector.detect(s.path, s.realPath);
    console.log(`${source.icon} ${s.name} (${s.path}) [${source.method}]`);
  });
}

async function handleSync(args) {
  logger.header("Syncing Inventory & Committing");
  const config = loadConfig();
  const shouldPush = args.includes("--push") || config.autoPush;

  // 1. Scan and detect sources
  const rawSkills = scanner.scan(config.searchRoots, {
    maxDepth: config.maxDepth,
    excludedDirs: config.excludedDirs
  });

  const skillsWithMetadata = rawSkills.map(s => {
    const info = sourceDetector.detect(s.path, s.realPath);

    // Read SKILL.md content and scrub sensitive data before adding to manifest
    let description = "";
    try {
      const rawContent = fs.readFileSync(s.skillFilePath, "utf8");
      if (s.isPrivate) {
        // For private skills, only extract YAML frontmatter metadata
        description = securityScrubber.extractMetadataOnly(rawContent, config.maskPatterns || []);
      } else {
        // For public skills, scrub any accidentally embedded secrets
        const scrubbed = securityScrubber.scrub(rawContent, config.maskPatterns || []);
        // Extract just the description from frontmatter for the manifest
        const descMatch = scrubbed.match(/description:\s*(.+)/);
        description = descMatch ? descMatch[1].trim() : "(no description)";
      }
    } catch (e) {
      description = "(could not read SKILL.md)";
    }

    return { ...s, ...info, description };
  });

  // 2. Generate Manifests
  const templatePath = path.join(__dirname, "templates", "manifest-template.md");
  manifestGenerator.generate(skillsWithMetadata, config.manifestPath, templatePath);

  // 3. Git Sync
  const committed = gitManager.commit(process.cwd(), `chore(inventory): update skills manifest [${new Date().toISOString()}]`);
  
  if (committed && shouldPush) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    await new Promise((resolve) => {
      rl.question("Push changes to GitHub repository? (y/N): ", (answer) => {
        rl.close();
        if (answer.toLowerCase() === "y") {
          logger.info("Proceeding to push to remote...");
          gitManager.push(process.cwd());
        } else {
          logger.warn("Push cancelled by user.");
        }
        resolve();
      });
    });
  }
}

async function handleList() {
  const config = loadConfig();
  const skills = scanner.scan(config.searchRoots, {
    maxDepth: config.maxDepth,
    excludedDirs: config.excludedDirs
  });
  
  logger.header("Installed Skills List");
  const table = skills.map(s => {
    const info = sourceDetector.detect(s.path, s.realPath);
    return { name: s.name, method: info.method, source: info.source, private: s.isPrivate };
  });
  console.table(table);
}

function showHelp() {
  console.log(`
Usage: inventory <command> [options]

Commands:
  bootstrap          Interactive/Guided setup for first-time users
  init [remote]      Initialize inventory config and git repository
  status             Check for changes and list detected skills
  sync [--push]      Update manifests and commit (optionally push)
  list               Display table of all installed skills
  `);
}

run().catch(err => {
  logger.error(err.message);
  process.exit(1);
});
