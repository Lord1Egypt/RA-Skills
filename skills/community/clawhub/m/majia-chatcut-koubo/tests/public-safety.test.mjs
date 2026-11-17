import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const gate = path.join(root, "scripts/check-public-safety.mjs");

function temporaryRepository(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "public-safety-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  return directory;
}

function writeFile(directory, relativePath, value) {
  const absolutePath = path.join(directory, relativePath);
  fs.mkdirSync(path.dirname(absolutePath), {recursive: true});
  fs.writeFileSync(absolutePath, value);
}

function runGate(directory, args = ["--root", directory]) {
  const result = spawnSync(process.execPath, [gate, ...args], {
    cwd: root,
    encoding: "utf8",
  });
  return {...result, output: `${result.stdout}${result.stderr}`};
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");
}

test("public safety gate scans text recursively and skips excluded binary content", (t) => {
  const directory = temporaryRepository(t);
  const allowedHome = ["", "Users", "example", "public-project"].join("/");
  const hiddenToken = ["AK", "IA", "1234567890ABCDEF"].join("");
  writeFile(directory, "README.md", `documented path: ${allowedHome}\n`);
  writeFile(directory, "node_modules/private.txt", hiddenToken);
  writeFile(directory, "coverage/private.txt", hiddenToken);
  writeFile(directory, ".git/private.txt", hiddenToken);
  writeFile(
    directory,
    "assets/blob.dat",
    Buffer.concat([Buffer.from([0, 1, 2]), Buffer.from(hiddenToken)]),
  );

  const result = runGate(directory);
  assert.equal(result.status, 0, result.output);
  assert.match(result.stdout, /public safety audit passed/);
});

test("absolute home findings report only relative path, rule, and line", (t) => {
  const directory = temporaryRepository(t);
  const privateHome = ["", "Users", "private-person", "project"].join("/");
  writeFile(directory, "docs/note.md", `safe line\n${privateHome}\n`);

  const result = runGate(directory);
  assert.equal(result.status, 1, result.output);
  assert.match(
    result.stderr,
    /FAIL path=docs\/note\.md rule=ABSOLUTE_HOME_PATH line=2/,
  );
  assert.equal(result.output.includes(privateHome), false, result.output);
  assert.doesNotMatch(result.output, new RegExp(escapeRegExp(directory)));
});

test("common token and private-key signatures fail without value disclosure", async (t) => {
  await t.test("access token", (subtest) => {
    const directory = temporaryRepository(subtest);
    const token = ["AK", "IA", "1234567890ABCDEF"].join("");
    writeFile(directory, "config.env", `PUBLIC=true\nVALUE=${token}\n`);

    const result = runGate(directory);
    assert.equal(result.status, 1, result.output);
    assert.match(result.stderr, /path=config\.env rule=SECRET_TOKEN line=2/);
    assert.equal(result.output.includes(token), false, result.output);
  });

  await t.test("private key header", (subtest) => {
    const directory = temporaryRepository(subtest);
    const header = ["-".repeat(5), "BEGIN ", "PRIVATE KEY", "-".repeat(5)].join("");
    writeFile(directory, "keys/material.pem", `${header}\nredacted-body\n`);

    const result = runGate(directory);
    assert.equal(result.status, 1, result.output);
    assert.match(
      result.stderr,
      /path=keys\/material\.pem rule=PRIVATE_KEY_MATERIAL line=1/,
    );
    assert.equal(result.output.includes(header), false, result.output);
  });

  await t.test("generic secret assignment", (subtest) => {
    const directory = temporaryRepository(subtest);
    const keyName = ["api", "_key"].join("");
    const value = ["real", "Secret", "Value", "1234567890"].join("");
    writeFile(directory, "settings.env", `${keyName}=${value}\n`);

    const result = runGate(directory);
    assert.equal(result.status, 1, result.output);
    assert.match(
      result.stderr,
      /path=settings\.env rule=SECRET_ASSIGNMENT line=1/,
    );
    assert.equal(result.output.includes(value), false, result.output);
  });
});

test("local exact deny and allow lists are applied without echoing literals", async (t) => {
  await t.test("deny literal blocks", (subtest) => {
    const directory = temporaryRepository(subtest);
    const denied = ["LOCAL", "_PRIVATE", "_TERM"].join("");
    writeFile(directory, ".ota-deny-list.txt", `${denied}\n`);
    writeFile(directory, "content.txt", `public line\n${denied}\n`);

    const result = runGate(directory);
    assert.equal(result.status, 1, result.output);
    assert.match(
      result.stderr,
      /path=content\.txt rule=LOCAL_DENY_LITERAL line=2/,
    );
    assert.equal(result.output.includes(denied), false, result.output);
  });

  await t.test("exact allow literal exempts public content", (subtest) => {
    const directory = temporaryRepository(subtest);
    const publicLiteral = ["PUBLIC", "_EXEMPT", "_TERM"].join("");
    writeFile(directory, ".ota-deny-list.txt", `${publicLiteral}\n`);
    writeFile(directory, ".ota-allow-list.txt", `${publicLiteral}\n`);
    writeFile(directory, "content.txt", `${publicLiteral}\n`);

    const result = runGate(directory);
    assert.equal(result.status, 0, result.output);
  });
});

test("allow list cannot suppress built-in safety rules", (t) => {
  const directory = temporaryRepository(t);
  const token = ["AK", "IA", "1234567890ABCDEF"].join("");
  writeFile(directory, ".ota-allow-list.txt", `${token}\n`);
  writeFile(directory, "content.txt", `${token}\n`);

  const result = runGate(directory);
  assert.equal(result.status, 1, result.output);
  assert.match(
    result.stderr,
    /path=\.ota-allow-list\.txt rule=SECRET_TOKEN line=1/,
  );
  assert.match(
    result.stderr,
    /path=content\.txt rule=SECRET_TOKEN line=1/,
  );
  assert.equal(result.output.includes(token), false, result.output);
});

test("placeholder markers embedded in real-looking secrets do not bypass scanning", (t) => {
  const directory = temporaryRepository(t);
  const keyName = ["api", "_key"].join("");
  const value = ["real", "example", "Secret", "Value", "123456"].join("");
  writeFile(directory, "settings.env", `${keyName}=${value}\n`);

  const result = runGate(directory);
  assert.equal(result.status, 1, result.output);
  assert.match(
    result.stderr,
    /path=settings\.env rule=SECRET_ASSIGNMENT line=1/,
  );
  assert.equal(result.output.includes(value), false, result.output);
});

test("symbolic links fail closed without being followed", (t) => {
  const directory = temporaryRepository(t);
  writeFile(directory, "target.txt", "safe\n");
  fs.symlinkSync("target.txt", path.join(directory, "private-link.txt"));

  const result = runGate(directory);
  assert.equal(result.status, 1, result.output);
  assert.match(
    result.stderr,
    /FAIL path=private-link\.txt rule=SYMLINK line=0/,
  );
});

test("public safety CLI accepts only one exact --root option", async (t) => {
  const directory = temporaryRepository(t);
  writeFile(directory, "safe.txt", "safe\n");
  const cases = [
    ["unknown", ["--unknown"], /unknown or unsupported option/],
    ["equals form", [`--root=${directory}`], /unknown or unsupported option/],
    ["duplicate", ["--root", directory, "--root", directory], /duplicate option/],
    ["missing value", ["--root"], /--root requires a value/],
  ];
  for (const [name, args, expected] of cases) {
    await t.test(name, () => {
      const result = runGate(directory, args);
      assert.equal(result.status, 2, result.output);
      assert.match(result.stderr, expected);
    });
  }
});

test("unreadable root failures use stable exit 2 without absolute paths", (t) => {
  const directory = temporaryRepository(t);
  const missingRoot = path.join(directory, "private-missing-root");
  const result = runGate(directory, ["--root", missingRoot]);
  assert.equal(result.status, 2, result.output);
  assert.match(
    result.stderr,
    /ERROR path=\. rule=ROOT_UNAVAILABLE line=0 code=ENOENT/,
  );
  assert.equal(result.output.includes(missingRoot), false, result.output);
});
