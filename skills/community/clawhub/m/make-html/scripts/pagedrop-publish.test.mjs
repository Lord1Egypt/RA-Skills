import assert from "node:assert/strict";
import { chmod, mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(new URL("./pagedrop-publish.mjs", import.meta.url));

async function createFixture({ bootstrap = false } = {}) {
  const root = await mkdtemp(path.join(tmpdir(), "pagedrop-publish-test-"));
  const binDir = path.join(root, "bin");
  const htmlPath = path.join(root, "artifact.html");
  const ghLogPath = path.join(root, "gh.log");
  const ghPath = path.join(binDir, "gh");

  await mkdir(binDir);
  await writeFile(
    htmlPath,
    [
      "<!doctype html>",
      '<html lang="en"><body>Fixture',
      bootstrap ? '<script src="https://pagedrop.ai/pagedrop.js"></script>' : "",
      "</body></html>",
    ].join(""),
  );
  await writeFile(
    ghPath,
    `#!${process.execPath}
import { appendFileSync } from "node:fs";
appendFileSync(process.env.GH_TEST_LOG, JSON.stringify(process.argv.slice(2)) + "\\n");
const args = process.argv.slice(2);
if (args[0] === "gist" && args[1] === "create") {
  console.log("https://gist.github.com/tester/abc123");
} else if (args[0] === "api" && args[1] === "user") {
  console.log("tester");
}
`,
  );
  await chmod(ghPath, 0o755);

  return { binDir, ghLogPath, htmlPath };
}

function runPublisher(fixture, args = []) {
  return spawnSync(process.execPath, [scriptPath, fixture.htmlPath, ...args], {
    encoding: "utf8",
    env: {
      ...process.env,
      GH_TEST_LOG: fixture.ghLogPath,
      PATH: `${fixture.binDir}${path.delimiter}${process.env.PATH ?? ""}`,
    },
  });
}

test("publishes the default pagedrop.ai gist route", async () => {
  const fixture = await createFixture();
  const result = runPublisher(fixture, ["--description", "Review"]);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), "https://pagedrop.ai/g/tester/abc123");

  const calls = (await readFile(fixture.ghLogPath, "utf8"))
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
  assert.deepEqual(calls, [
    ["auth", "status"],
    ["gist", "create", fixture.htmlPath, "--desc", "Review #pagedrop"],
    ["api", "user", "--jq", ".login"],
  ]);
});

test("requires the pagedrop.ai bootstrap before publishing an h route", async () => {
  const fixture = await createFixture();
  const result = runPublisher(fixture, ["--route", "h"]);

  assert.equal(result.status, 1);
  assert.match(result.stderr, /route h requires https:\/\/pagedrop\.ai\/pagedrop\.js/);
});

test("publishes an h route when the pagedrop.ai bootstrap is present", async () => {
  const fixture = await createFixture({ bootstrap: true });
  const result = runPublisher(fixture, ["--route", "h"]);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), "https://pagedrop.ai/h/tester/abc123");
});
