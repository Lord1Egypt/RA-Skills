import assert from "node:assert/strict";
import type { DatabaseSync } from "node:sqlite";
import { describe, it, beforeEach } from "node:test";
import { initDatabase } from "./schema.ts";
import { MetadataStore } from "./store.ts";

describe("MetadataStore", () => {
  let db: DatabaseSync;
  let store: MetadataStore;

  beforeEach(() => {
    db = initDatabase(":memory:");
    store = new MetadataStore(db);
  });

  describe("schema initialization", () => {
    it("creates topic_metadata table", () => {
      const row = db
        .prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='topic_metadata'")
        .get() as { name: string } | undefined;
      assert.equal(row?.name, "topic_metadata");
    });

    it("creates topic_rename_log table", () => {
      const row = db
        .prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='topic_rename_log'")
        .get() as { name: string } | undefined;
      assert.equal(row?.name, "topic_rename_log");
    });

    it("creates indexes", () => {
      const indexes = db
        .prepare(
          "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_topic_meta%'",
        )
        .all() as { name: string }[];
      const names = indexes.map((i) => i.name).toSorted();
      assert.deepEqual(names, ["idx_topic_meta_status", "idx_topic_meta_stream"]);
    });
  });

  describe("get", () => {
    it("returns null for non-existent topic", () => {
      assert.equal(store.get(1, "nonexistent"), null);
    });

    it("returns metadata after upsert", () => {
      store.upsert(1, "bug report", { status: "open" });
      const result = store.get(1, "bug report");
      assert.equal(result?.stream_id, 1);
      assert.equal(result?.topic_name, "bug report");
      assert.equal(result?.status, "open");
      assert.deepEqual(result?.labels, []);
    });
  });

  describe("upsert", () => {
    it("creates new entry if not exists", () => {
      const result = store.upsert(1, "new topic", {
        status: "wip",
        priority: "p1",
        assignee: "alice",
      });
      assert.equal(result.status, "wip");
      assert.equal(result.priority, "p1");
      assert.equal(result.assignee, "alice");
    });

    it("updates existing entry", () => {
      store.upsert(1, "topic", { status: "open" });
      const updated = store.upsert(1, "topic", {
        status: "done",
        priority: "p0",
      });
      assert.equal(updated.status, "done");
      assert.equal(updated.priority, "p0");
    });

    it("preserves fields not in update", () => {
      store.upsert(1, "topic", {
        status: "open",
        assignee: "bob",
      });
      const updated = store.upsert(1, "topic", { status: "wip" });
      assert.equal(updated.status, "wip");
      assert.equal(updated.assignee, "bob");
    });
  });

  describe("list", () => {
    beforeEach(() => {
      store.upsert(1, "topic-a", {
        status: "open",
        assignee: "alice",
      });
      store.upsert(1, "topic-b", {
        status: "done",
        assignee: "bob",
      });
      store.upsert(1, "topic-c", {
        status: "open",
        assignee: "alice",
      });
      store.upsert(2, "other-stream", { status: "open" });
    });

    it("lists all for a stream", () => {
      const results = store.list(1);
      assert.equal(results.length, 3);
    });

    it("filters by status", () => {
      const results = store.list(1, { status: "open" });
      assert.equal(results.length, 2);
    });

    it("filters by assignee", () => {
      const results = store.list(1, { assignee: "alice" });
      assert.equal(results.length, 2);
    });

    it("filters by label", () => {
      store.addLabel(1, "topic-a", "urgent");
      const results = store.list(1, { label: "urgent" });
      assert.equal(results.length, 1);
      assert.equal(results[0].topic_name, "topic-a");
    });
  });

  describe("remove", () => {
    it("removes existing entry and returns true", () => {
      store.upsert(1, "topic", { status: "open" });
      assert.equal(store.remove(1, "topic"), true);
      assert.equal(store.get(1, "topic"), null);
    });

    it("returns false for non-existent entry", () => {
      assert.equal(store.remove(1, "nonexistent"), false);
    });
  });

  describe("labels", () => {
    beforeEach(() => {
      store.upsert(1, "topic", { status: "open" });
    });

    it("adds a label", () => {
      const result = store.addLabel(1, "topic", "bug");
      assert.deepEqual(result.labels, ["bug"]);
    });

    it("does not add duplicate labels", () => {
      store.addLabel(1, "topic", "bug");
      const result = store.addLabel(1, "topic", "bug");
      assert.deepEqual(result.labels, ["bug"]);
    });

    it("removes a label", () => {
      store.addLabel(1, "topic", "bug");
      store.addLabel(1, "topic", "feature");
      const result = store.removeLabel(1, "topic", "bug");
      assert.deepEqual(result.labels, ["feature"]);
    });
  });

  describe("rename", () => {
    it("handleRename updates topic name and logs", () => {
      store.upsert(1, "old-name", {
        status: "wip",
        assignee: "alice",
      });
      store.handleRename(1, "old-name", "new-name");

      assert.equal(store.get(1, "old-name"), null);
      const renamed = store.get(1, "new-name");
      assert.equal(renamed?.status, "wip");
      assert.equal(renamed?.assignee, "alice");
    });

    it("logs rename history", () => {
      store.upsert(1, "v1", { status: "open" });
      store.handleRename(1, "v1", "v2");
      store.handleRename(1, "v2", "v3");

      const history = store.getRenameHistory(1, "v2");
      assert.equal(history.length, 2);
      assert.equal(history[0].old_name, "v1");
      assert.equal(history[0].new_name, "v2");
      assert.equal(history[1].old_name, "v2");
      assert.equal(history[1].new_name, "v3");
    });
  });
});
