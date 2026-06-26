import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";

type PackFile = { path: string };
type PackEntry = {
  filename?: string;
  files?: PackFile[];
};

const ROOT = path.join(__dirname, "..");
const PACKAGE_JSON = path.join(ROOT, "package.json");

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) {
    throw new Error(message);
  }
}

function runNpm(args: string[], cwd: string, envOverrides: Record<string, string> = {}): string {
  return execFileSync("npm", args, {
    cwd,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    env: {
      ...process.env,
      npm_config_audit: "false",
      npm_config_fund: "false",
      ...envOverrides,
    },
  });
}

function getPackEntry(): PackEntry {
  const stdout = runNpm(
    ["pack", "--json", "--ignore-scripts"],
    ROOT,
    {
      // `npm pack --dry-run` and `npm publish --dry-run` propagate dry-run to child npm
      // invocations through npm_config_dry_run, which suppresses tarball creation.
      npm_config_dry_run: "false",
    },
  );
  const parsed = JSON.parse(stdout) as PackEntry[];
  assert(Array.isArray(parsed) && parsed.length > 0, "npm pack --json returned no metadata");
  return parsed[0];
}

function validatePackedFiles(entry: PackEntry, pkg: Record<string, any>) {
  const packedFiles = new Set((entry.files ?? []).map((file) => file.path));
  const requiredFiles = [
    "package.json",
    "README.md",
    "README_ja.md",
    "SKILL.md",
    "SECURITY.md",
    "guard-scanner",
    "openclaw.plugin.json",
    "dist/index.mjs",
    "dist/index.cjs",
    "dist/index.d.ts",
    "dist/openclaw-plugin.mjs",
    "dist/openclaw-plugin.cjs",
    "dist/openclaw-plugin.d.ts",
    "dist/mcp-server.mjs",
    "dist/mcp-server.cjs",
    "dist/types.d.ts",
  ];

  for (const file of requiredFiles) {
    assert(packedFiles.has(file), `packed tarball is missing ${file}`);
  }

  const exportTargets = [
    pkg.exports?.["."]?.import,
    pkg.exports?.["."]?.require,
    pkg.exports?.["./plugin"]?.import,
    pkg.exports?.["./plugin"]?.require,
    pkg.exports?.["./mcp"]?.import,
    pkg.exports?.["./mcp"]?.require,
    pkg.bin?.["guard-scanner"],
  ].filter(Boolean);

  for (const target of exportTargets) {
    const normalized = String(target).replace(/^\.\//, "");
    assert(packedFiles.has(normalized), `package export ${target} is missing from tarball`);
  }
}

function validateCleanInstall(entry: PackEntry, pkg: Record<string, any>) {
  assert(entry.filename, "npm pack metadata missing filename");
  const tarballPath = path.join(ROOT, entry.filename);
  assert(fs.existsSync(tarballPath), `npm pack did not create expected tarball: ${tarballPath}`);
  const installDir = fs.mkdtempSync(path.join(os.tmpdir(), "guard-scanner-install-"));
  fs.writeFileSync(
    path.join(installDir, "package.json"),
    JSON.stringify({ name: "guard-scanner-smoke", private: true }, null, 2),
  );

  runNpm(
    ["install", "--ignore-scripts", "--no-package-lock", "--no-audit", "--no-fund", tarballPath],
    installDir,
    {
      npm_config_dry_run: "false",
    },
  );

  const installedRoot = path.join(installDir, "node_modules", "@guava-parity", "guard-scanner");
  assert(fs.existsSync(path.join(installedRoot, "dist", "index.mjs")), "clean install missing dist/index.mjs");
  assert(fs.existsSync(path.join(installedRoot, "openclaw.plugin.json")), "clean install missing openclaw.plugin.json");
  assert(fs.existsSync(path.join(installedRoot, "guard-scanner")), "clean install missing root guard-scanner launcher");

  const binVersion = execFileSync(
    path.join(installDir, "node_modules", ".bin", "guard-scanner"),
    ["--version"],
    {
      cwd: installDir,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    },
  ).trim();
  assert(new RegExp(`guard-scanner v${pkg.version}`).test(binVersion), `unexpected .bin version output: ${binVersion}`);

  const fixturePath = path.join(ROOT, "tests", "fixtures", "benign", "math-helper");
  const binScan = execFileSync(
    path.join(installDir, "node_modules", ".bin", "guard-scanner"),
    [fixturePath, "--compliance", "owasp-asi", "--format", "json"],
    {
      cwd: installDir,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    },
  ).trim();
  const parsedScan = JSON.parse(binScan) as { compliance_mode?: string; findings?: unknown[] };
  assert(parsedScan.compliance_mode === "owasp-asi", "installed CLI must preserve compliance mode");
  assert(Array.isArray(parsedScan.findings), "installed CLI must return findings array");

  const execVersion = runNpm(
    ["exec", "--yes", `--package=${tarballPath}`, "--", "guard-scanner", "--version"],
    installDir,
    {
      npm_config_dry_run: "false",
    },
  ).trim();
  assert(new RegExp(`guard-scanner v${pkg.version}`).test(execVersion), `unexpected npm exec version output: ${execVersion}`);

  const packageSurface = execFileSync(
    "node",
    [
      "-e",
      "import * as pkg from '@guava-parity/guard-scanner'; import plugin from '@guava-parity/guard-scanner/plugin'; console.log(typeof pkg.GuardScanner, typeof pkg.scanToolCall, typeof pkg.MCPServer, typeof (plugin.default ?? plugin).register);",
    ],
    {
      cwd: installDir,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    },
  ).trim();
  assert(
    packageSurface === "function function function function",
    `unexpected installed package surface: ${packageSurface}`,
  );

  const mcpSurface = execFileSync(
    "node",
    [
      "-e",
      "import { MCPServer }  from '@guava-parity/guard-scanner/mcp'; const server = new MCPServer(); server._callTool('get_stats', {}).then((res)=>console.log(Boolean(res && res.content && res.content[0] && /Static Analysis/.test(res.content[0].text)))).catch((err)=>{console.error(err); process.exit(1);});",
    ],
    {
      cwd: installDir,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    },
  ).trim();
  assert(mcpSurface === "true", `unexpected MCP package surface: ${mcpSurface}`);

  fs.rmSync(tarballPath, { force: true });
}

function main() {
  const pkg = JSON.parse(fs.readFileSync(PACKAGE_JSON, "utf8")) as Record<string, any>;
  const packEntry = getPackEntry();
  validatePackedFiles(packEntry, pkg);
  validateCleanInstall(packEntry, pkg);
  console.log(`✅ tarball validation: ${packEntry.filename ?? "guard-scanner.tgz"} contains the compiled plugin surface`);
}

main();
