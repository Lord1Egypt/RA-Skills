import test from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import {
  mkdtempSync,
  writeFileSync,
  symlinkSync,
  mkdirSync,
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  svgRootInfo,
  sameFile,
  safeUrl,
  assertBudget,
  listenOnSafePort,
} from "../lib.mjs";

// Windows creates symlinks only with Developer Mode or elevation. Those cases are
// skipped rather than failed, so the suite still means something on a stock Windows box.
function symlinkAllowed(target, link) {
  try {
    symlinkSync(target, link);
    return true;
  } catch (error) {
    if (error.code === "EPERM" || error.code === "EACCES") return false;
    throw error;
  }
}

// A directory junction needs no elevation on Windows, and Node treats the type as a
// plain symlink everywhere else — so alias resolution can be exercised everywhere.
function linkDir(target, link) {
  symlinkSync(target, link, "junction");
}

test("SVG: ignore comments, declarations, doctypes, and quoted >", () => {
  const s = svgRootInfo(
    `<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x "y">]><!-- <svg width="999" height="999"> --><svg data-note="a > b" width="40" height="20"/>`,
  );
  assert.deepEqual(s.size, { w: 40, h: 20 });
  assert.match(s.tag, /a > b/);
});
test("SVG: use positive fractional and exponential viewBox extents", () => {
  assert.deepEqual(svgRootInfo('<svg viewBox="-1,-2,.5,5e-1"/>').size, {
    w: 0.5,
    h: 0.5,
  });
});
test("SVG: ignore stroke-width and namespaced attributes", () => {
  assert.deepEqual(
    svgRootInfo('<svg stroke-width="7" data-height="88" viewBox="0 0 24 12"/>')
      .size,
    { w: 24, h: 12 },
  );
});
test("SVG: preserve explicit dimension when completing from viewBox", () => {
  assert.deepEqual(svgRootInfo('<svg width="100px" viewBox="0 0 4 2"/>').size, {
    w: 100,
    h: 50,
  });
});
test("SVG: flag invalid/empty viewBox rather than append duplicate", () => {
  const s = svgRootInfo('<svg width="30" height="30" viewBox=""/>');
  assert.equal(s.hasViewBoxAttr, true);
  assert.equal(s.hasViewBox, false);
});
test("SVG: reject missing root; nonintrinsic units do not become pixels", () => {
  assert.throws(() => svgRootInfo("<!-- <svg/> -->"), /no <svg>/);
  assert.equal(svgRootInfo('<svg width="10em" height="20%"/>').size, null);
});
test("pixel budget: reject oversized axes, area, NaN and zero", () => {
  assert.doesNotThrow(() => assertBudget(1200, 630, 2, 64e6));
  for (const [w, h, d] of [
    [32768, 1, 1],
    [5000, 5000, 2],
    [NaN, 10, 1],
    [0, 10, 1],
  ])
    assert.throws(() => assertBudget(w, h, d, 64e6));
});
test("URL diagnostics strip credentials, queries and fragments", () => {
  assert.equal(
    safeUrl("https://u:secret@example.org/x?token=private#frag"),
    "https://example.org/x",
  );
});
test("sameFile handles aliases and symlinks", (t) => {
  const dir = mkdtempSync(join(tmpdir(), "html-shot-unit-"));
  try {
    const real = join(dir, "real");
    mkdirSync(real);
    writeFileSync(join(real, "a"), "x");
    linkDir(real, join(dir, "alias"));
    assert.equal(sameFile(real, join(dir, "alias")), true);
    assert.equal(sameFile(real, join(dir, "other")), false);
    if (symlinkAllowed(join(real, "a"), join(dir, "b")))
      assert.equal(sameFile(join(real, "a"), join(dir, "b")), true);
    else
      t.diagnostic(
        "file symlinks need Developer Mode or elevation here; the file-alias case did not run",
      );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
test("fixture servers bind above Chromium's restricted ports", async () => {
  const server = createServer(() => {});
  await listenOnSafePort(server);
  try {
    assert.ok(server.address().port > 10080);
  } finally {
    await new Promise((ok) => server.close(ok));
  }
});
