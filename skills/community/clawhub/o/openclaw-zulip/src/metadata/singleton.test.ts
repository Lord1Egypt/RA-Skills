import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, it, expect, afterEach } from "vitest";
import { initMetadataStore, getMetadataStore, destroyMetadataStore } from "./singleton.ts";

describe("MetadataStore singleton", () => {
  let dir: string;

  afterEach(() => {
    destroyMetadataStore();
    if (dir) {
      try {
        rmSync(dir, { recursive: true, force: true });
      } catch {
        // ignore
      }
    }
  });

  it("getMetadataStore returns null before init", () => {
    expect(getMetadataStore()).toBeNull();
  });

  it("initMetadataStore creates and returns store", () => {
    dir = mkdtempSync(join(tmpdir(), "zulip-meta-"));
    const store = initMetadataStore(join(dir, "test.sqlite"));
    expect(store).toBeTruthy();
    expect(getMetadataStore()).toBe(store);
  });

  it("destroyMetadataStore clears singleton", () => {
    dir = mkdtempSync(join(tmpdir(), "zulip-meta-"));
    initMetadataStore(join(dir, "test.sqlite"));
    destroyMetadataStore();
    expect(getMetadataStore()).toBeNull();
  });

  it("double init replaces previous store", () => {
    dir = mkdtempSync(join(tmpdir(), "zulip-meta-"));
    initMetadataStore(join(dir, "a.sqlite"));
    const s2 = initMetadataStore(join(dir, "b.sqlite"));
    expect(getMetadataStore()).toBe(s2);
    // Verify the new store works
    s2.upsert(1, "test", { status: "wip" });
    expect(s2.get(1, "test")?.status).toBe("wip");
  });

  it("creates parent directories", () => {
    dir = mkdtempSync(join(tmpdir(), "zulip-meta-"));
    const deep = join(dir, "a", "b", "c", "test.sqlite");
    const store = initMetadataStore(deep);
    expect(store).toBeTruthy();
  });

  it("store CRUD works after init", () => {
    dir = mkdtempSync(join(tmpdir(), "zulip-meta-"));
    const store = initMetadataStore(join(dir, "test.sqlite"));
    store.upsert(1, "test-topic", { status: "wip" });
    const meta = store.get(1, "test-topic");
    expect(meta?.status).toBe("wip");
  });
});
