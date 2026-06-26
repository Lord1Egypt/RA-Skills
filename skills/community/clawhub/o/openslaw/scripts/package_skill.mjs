import { mkdirSync } from "node:fs";
import { basename, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

function argValue(flag, fallback) {
  const index = process.argv.indexOf(flag);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, "..");
const packageParent = dirname(skillRoot);
const packageName = basename(skillRoot);
const defaultOut = resolve(packageParent, `${packageName}.zip`);
const outFile = resolve(argValue("--out", defaultOut));

mkdirSync(dirname(outFile), { recursive: true });

const result = spawnSync("zip", ["-qr", outFile, packageName], {
  cwd: packageParent,
  stdio: "inherit"
});

if (result.error) {
  throw result.error;
}

if (result.status !== 0) {
  process.exit(result.status ?? 1);
}

console.log(`created ${outFile}`);
