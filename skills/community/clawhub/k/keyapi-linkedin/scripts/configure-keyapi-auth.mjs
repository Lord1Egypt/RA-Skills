import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const minNodeMajor = 18;
const managedBlockStart = "# >>> keyapi-skills >>>";
const managedBlockEnd = "# <<< keyapi-skills <<<";

function requireSupportedNodeVersion() {
  const major = Number(process.versions.node.split(".")[0]);
  if (Number.isNaN(major) || major < minNodeMajor) {
    throw new Error(`Node.js >= ${minNodeMajor} is required. Current version: ${process.versions.node}`);
  }
}

function parseArgs(argv) {
  const args = {
    status: false
  };

  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }

    const [rawKey, inlineValue] = token.split("=", 2);
    const key = rawKey.slice(2);

    if (key === "status") {
      args.status = true;
      continue;
    }

    const nextValue = inlineValue ?? argv[index + 1];
    if (!nextValue || nextValue.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    if (inlineValue === undefined) {
      index += 1;
    }

    if (key === "profile") args.profilePath = path.resolve(nextValue);
    else if (key === "token") args.token = nextValue;
    else throw new Error(`Unsupported argument: --${key}`);
  }

  return args;
}

function isPlaceholder(value) {
  if (!value) {
    return true;
  }

  return new Set([
    "",
    "your_token",
    "your_token_here",
    "your_keyapi_token",
    "keyapi_token",
    "changeme",
    "replace_me",
    "todo"
  ]).has(String(value).trim().toLowerCase());
}

function requireRealValue(name, value) {
  if (isPlaceholder(value)) {
    throw new Error(`Missing or placeholder value for ${name}`);
  }
  return String(value).trim();
}

function detectProfilePath(explicitPath) {
  if (explicitPath) {
    return explicitPath;
  }

  const homeDir = os.homedir();
  const shell = process.env.SHELL || "";

  if (process.platform === "win32") {
    return path.join(homeDir, "Documents", "PowerShell", "Microsoft.PowerShell_profile.ps1");
  }
  if (shell.includes("zsh")) {
    return path.join(homeDir, ".zshrc");
  }
  if (shell.includes("bash")) {
    const bashrc = path.join(homeDir, ".bashrc");
    return fs.existsSync(bashrc) ? bashrc : path.join(homeDir, ".bash_profile");
  }

  return path.join(homeDir, ".profile");
}

function detectProfileKind(profilePath) {
  return profilePath.toLowerCase().endsWith(".ps1") ? "powershell" : "posix";
}

function ensureParentDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function powershellQuote(value) {
  return `'${String(value).replace(/'/g, "''")}'`;
}

function stripManagedBlock(contents) {
  const escapedStart = managedBlockStart.replace(/[.*+?^${}()|[]\\]/g, "\\$&");
  const escapedEnd = managedBlockEnd.replace(/[.*+?^${}()|[]\\]/g, "\\$&");
  const pattern = new RegExp(`${escapedStart}[\\s\\S]*?${escapedEnd}\\n?`, "g");
  return contents.replace(pattern, "").trimEnd();
}

function buildManagedBlock(values, profileKind) {
  if (profileKind === "powershell") {
    return [
      managedBlockStart,
      `$env:KEYAPI_TOKEN = ${powershellQuote(values.token)}`,
      managedBlockEnd,
      ""
    ].join("\n");
  }

  return [
    managedBlockStart,
    `export KEYAPI_TOKEN=${shellQuote(values.token)}`,
    managedBlockEnd,
    ""
  ].join("\n");
}

function extractManagedBlock(contents) {
  const startIndex = contents.indexOf(managedBlockStart);
  if (startIndex === -1) {
    return undefined;
  }
  const endIndex = contents.indexOf(managedBlockEnd, startIndex + managedBlockStart.length);
  if (endIndex === -1) {
    return undefined;
  }
  return contents.slice(startIndex + managedBlockStart.length, endIndex);
}

function parseManagedValue(rawValue, profilePath) {
  const value = rawValue.trim();
  if (value.startsWith("'") && value.endsWith("'")) {
    const inner = value.slice(1, -1);
    if (profilePath.toLowerCase().endsWith(".ps1")) {
      return inner.replace(/''/g, "'");
    }
    return inner.split("'\\''").join("'");
  }
  if (value.startsWith('"') && value.endsWith('"')) {
    return value.slice(1, -1);
  }
  return value;
}

function readTokenFromManagedProfile(profilePath) {
  if (!fs.existsSync(profilePath)) {
    return undefined;
  }

  const block = extractManagedBlock(fs.readFileSync(profilePath, "utf8"));
  if (!block) {
    return undefined;
  }

  const powershellMatch = block.match(/^\s*\$env:KEYAPI_TOKEN\s*=\s*(.+?)\s*$/m);
  const posixMatch = block.match(/^\s*export\s+KEYAPI_TOKEN=(.+?)\s*$/m);
  const rawValue = powershellMatch?.[1] ?? posixMatch?.[1];
  if (!rawValue) {
    return undefined;
  }

  const token = parseManagedValue(rawValue, profilePath).trim();
  return isPlaceholder(token) ? undefined : token;
}

function authIsAvailable(profilePath) {
  return !isPlaceholder(process.env.KEYAPI_TOKEN) || !isPlaceholder(readTokenFromManagedProfile(profilePath));
}

async function collectCredentials(args) {
  const token = args.token ? requireRealValue("KEYAPI_TOKEN", args.token) : undefined;

  if (token) {
    return { token };
  }

  const rl = createInterface({ input, output });

  try {
    output.write("KeyAPI setup will save KEYAPI_TOKEN into your shell environment variables.\n");
    const enteredToken = await rl.question("Paste KEYAPI_TOKEN: ");

    return {
      token: requireRealValue("KEYAPI_TOKEN", enteredToken)
    };
  } finally {
    rl.close();
  }
}

function writeProfile(profilePath, credentials) {
  ensureParentDir(profilePath);
  const profileKind = detectProfileKind(profilePath);
  const existing = fs.existsSync(profilePath) ? fs.readFileSync(profilePath, "utf8") : "";
  const cleaned = stripManagedBlock(existing);
  const block = buildManagedBlock(credentials, profileKind);
  const next = cleaned ? `${cleaned}\n\n${block}` : block;
  fs.writeFileSync(profilePath, next);
  return profileKind;
}

function printStatus(profilePath) {
  const profileKind = detectProfileKind(profilePath);
  const available = authIsAvailable(profilePath);
  process.stdout.write(
    `${JSON.stringify(
      {
        authStatus: available ? "available" : "unavailable",
        available,
        profilePath,
        profileKind,
        message: available
          ? "KeyAPI credentials are available. You can run keyapi-api.mjs requests now."
          : "KeyAPI credentials are unavailable. Run node scripts/configure-keyapi-auth.mjs."
      },
      null,
      2
    )}\n`
  );
}

async function main() {
  requireSupportedNodeVersion();
  const args = parseArgs(process.argv);
  const profilePath = detectProfilePath(args.profilePath);

  if (args.status) {
    printStatus(profilePath);
    return;
  }

  const credentials = await collectCredentials(args);
  const profileKind = writeProfile(profilePath, credentials);
  const reloadHint =
    profileKind === "powershell" ? `. ${profilePath}` : `source ${profilePath}`;

  process.stdout.write(
    [
      "KeyAPI environment variable setup complete.",
      `- shell profile: ${profilePath}`,
      `- profile kind: ${profileKind}`,
      "- auth mode: bearer_token",
      "- API base URL: https://api.keyapi.ai",
      "- status: available",
      "- Next step: retry the KeyAPI request.",
      `- To refresh this shell manually, run: ${reloadHint}`
    ].join("\n") + "\n"
  );
}

try {
  await main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
