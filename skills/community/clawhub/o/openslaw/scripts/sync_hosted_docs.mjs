import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

function argValue(flag, fallback) {
  const index = process.argv.indexOf(flag);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, "..");
const origin = argValue("--origin", "https://www.openslaw.com");
const apiBase = argValue("--api-base", `${origin.replace(/\/+$/, "")}/api/v1`);
const relayUrl = argValue("--relay-url", `${apiBase.replace(/^http/, "ws")}/provider/runtime-relay`);
const outDir = resolve(argValue("--out-dir", join(skillRoot, ".rendered-hosted")));

const fileMap = [
  ["SKILL.md", "skill.md"],
  ["DOCS.md", "docs.md"],
  ["AUTH.md", "auth.md"],
  ["DEVELOPERS.md", "developers.md"],
  ["references/api.md", "api-guide.md"],
  ["references/playbook.md", "playbook.md"],
  ["manual/index.html", "manual/index.html"]
];

function render(content) {
  return content
    .replaceAll("{{OPENSLAW_ORIGIN}}", origin)
    .replaceAll("{{OPENSLAW_API_BASE}}", apiBase)
    .replaceAll("{{OPENSLAW_RELAY_URL}}", relayUrl)
    .replaceAll("https://openslaw.example.com", origin)
    .replaceAll("https://api.openslaw.example.com/api/v1", apiBase);
}

mkdirSync(outDir, { recursive: true });

for (const [inputRelativePath, outputRelativePath] of fileMap) {
  const inputPath = join(skillRoot, inputRelativePath);
  const outputPath = join(outDir, outputRelativePath);

  mkdirSync(dirname(outputPath), { recursive: true });
  writeFileSync(outputPath, render(readFileSync(inputPath, "utf8")), "utf8");
  console.log(`rendered ${outputPath}`);
}

const manifest = {
  name: "openslaw",
  homepage: origin,
  api_base: apiBase,
  files: fileMap.map(([, outputRelativePath]) => ({
    path: `/${outputRelativePath}`,
    url: `${origin.replace(/\/+$/, "")}/${outputRelativePath}`
  }))
};

writeFileSync(join(outDir, "skill.json"), JSON.stringify(manifest, null, 2) + "\n", "utf8");
console.log(`rendered ${join(outDir, "skill.json")}`);
