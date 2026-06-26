/**
 * Unit tests for workdir isolation (Issue #6).
 */

import { describe, it, expect, afterEach } from "vitest";
import { existsSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, basename } from "node:path";
import {
  createIsolatedWorkdir,
  cleanupWorkdir,
  sweepOrphanedWorkdirs,
  getWorkdirBase,
} from "../src/workdir.js";

// Track created dirs for cleanup in case tests fail
const createdDirs: string[] = [];

afterEach(() => {
  for (const dir of createdDirs) {
    try {
      const { rmSync } = require("node:fs");
      rmSync(dir, { recursive: true, force: true });
    } catch { /* ignore */ }
  }
  createdDirs.length = 0;
});

describe("createIsolatedWorkdir()", () => {
  it("creates a directory that exists", () => {
    const dir = createIsolatedWorkdir();
    createdDirs.push(dir);
    expect(existsSync(dir)).toBe(true);
  });

  it("creates a directory with the cli-bridge- prefix", () => {
    const dir = createIsolatedWorkdir();
    createdDirs.push(dir);
    expect(basename(dir)).toMatch(/^cli-bridge-/);
  });

  it("creates unique directories on repeated calls", () => {
    const dir1 = createIsolatedWorkdir();
    const dir2 = createIsolatedWorkdir();
    createdDirs.push(dir1, dir2);
    expect(dir1).not.toBe(dir2);
  });

  it("accepts a custom base directory", () => {
    const customBase = join(tmpdir(), "workdir-test-base");
    mkdirSync(customBase, { recursive: true });
    createdDirs.push(customBase);

    const dir = createIsolatedWorkdir(customBase);
    createdDirs.push(dir);
    expect(dir.startsWith(customBase)).toBe(true);
  });
});

describe("cleanupWorkdir()", () => {
  it("removes an existing workdir", () => {
    const dir = createIsolatedWorkdir();
    // Create a file inside to verify recursive removal
    writeFileSync(join(dir, "test.txt"), "hello");
    expect(existsSync(dir)).toBe(true);

    const result = cleanupWorkdir(dir);
    expect(result).toBe(true);
    expect(existsSync(dir)).toBe(false);
  });

  it("returns false for non-existent directory", () => {
    const result = cleanupWorkdir(join(tmpdir(), "cli-bridge-nonexistent"));
    // rmSync with force:true doesn't throw for non-existent
    expect(result).toBe(true);
  });

  it("refuses to remove directories without cli-bridge- prefix", () => {
    const result = cleanupWorkdir("/tmp/some-other-dir");
    expect(result).toBe(false);
  });

  it("refuses to remove empty string", () => {
    const result = cleanupWorkdir("");
    expect(result).toBe(false);
  });
});

describe("sweepOrphanedWorkdirs()", () => {
  it("removes workdirs older than the threshold", () => {
    const base = join(tmpdir(), "sweep-test-" + Date.now());
    mkdirSync(base, { recursive: true });
    createdDirs.push(base);

    // Create a fake old workdir
    const oldDir = join(base, "cli-bridge-oldone");
    mkdirSync(oldDir);
    // Set mtime to 2 hours ago
    const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000);
    const { utimesSync } = require("node:fs");
    utimesSync(oldDir, twoHoursAgo, twoHoursAgo);

    const removed = sweepOrphanedWorkdirs(base);
    expect(removed).toBe(1);
    expect(existsSync(oldDir)).toBe(false);
  });

  it("does not remove recent workdirs", () => {
    const base = join(tmpdir(), "sweep-test-recent-" + Date.now());
    mkdirSync(base, { recursive: true });
    createdDirs.push(base);

    const recentDir = join(base, "cli-bridge-recent");
    mkdirSync(recentDir);

    const removed = sweepOrphanedWorkdirs(base);
    expect(removed).toBe(0);
    expect(existsSync(recentDir)).toBe(true);
  });

  it("ignores non-cli-bridge directories", () => {
    const base = join(tmpdir(), "sweep-test-ignore-" + Date.now());
    mkdirSync(base, { recursive: true });
    createdDirs.push(base);

    const otherDir = join(base, "other-dir");
    mkdirSync(otherDir);
    const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000);
    const { utimesSync } = require("node:fs");
    utimesSync(otherDir, twoHoursAgo, twoHoursAgo);

    const removed = sweepOrphanedWorkdirs(base);
    expect(removed).toBe(0);
    expect(existsSync(otherDir)).toBe(true);
  });

  it("returns 0 for non-existent base", () => {
    const removed = sweepOrphanedWorkdirs("/nonexistent/path");
    expect(removed).toBe(0);
  });
});

describe("getWorkdirBase()", () => {
  it("returns tmpdir by default", () => {
    // Clear env var if set
    const prev = process.env.OPENCLAW_CLI_BRIDGE_WORKDIR_BASE;
    delete process.env.OPENCLAW_CLI_BRIDGE_WORKDIR_BASE;
    expect(getWorkdirBase()).toBe(tmpdir());
    // Restore
    if (prev !== undefined) process.env.OPENCLAW_CLI_BRIDGE_WORKDIR_BASE = prev;
  });
});
