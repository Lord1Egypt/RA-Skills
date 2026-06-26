import assert from "node:assert/strict";
import type { DatabaseSync } from "node:sqlite";
import { describe, it, beforeEach } from "node:test";
import { handleMetaCommand, type CommandContext } from "./command-handler.ts";
import { initDatabase } from "./schema.ts";
import { MetadataStore } from "./store.ts";

describe("handleMetaCommand", () => {
  let db: DatabaseSync;
  let store: MetadataStore;
  const ctx: CommandContext = { streamId: 1, topicName: "test-topic" };

  beforeEach(() => {
    db = initDatabase(":memory:");
    store = new MetadataStore(db);
  });

  describe("show", () => {
    it("shows 'no metadata' when topic has none", () => {
      const result = handleMetaCommand(store, ctx, "/meta show");
      assert.ok(result.includes("No metadata"));
      assert.ok(result.includes("test-topic"));
    });

    it("shows formatted metadata", () => {
      store.upsert(1, "test-topic", { status: "wip", priority: "p1", assignee: "alice" });
      const result = handleMetaCommand(store, ctx, "/meta show");
      assert.ok(result.includes("📋 Topic: test-topic"));
      assert.ok(result.includes("Status: wip"));
      assert.ok(result.includes("Priority: p1"));
      assert.ok(result.includes("Assignee: alice"));
    });

    it("shows dashes for null fields", () => {
      store.upsert(1, "test-topic", { status: "open" });
      const result = handleMetaCommand(store, ctx, "/meta show");
      assert.ok(result.includes("Priority: —"));
      assert.ok(result.includes("Assignee: —"));
      assert.ok(result.includes("Due: —"));
      assert.ok(result.includes("Labels: —"));
    });

    it("shows labels", () => {
      store.upsert(1, "test-topic", { status: "open", labels: ["bug", "urgent"] });
      const result = handleMetaCommand(store, ctx, "/meta show");
      assert.ok(result.includes("[bug, urgent]"));
    });
  });

  describe("set", () => {
    it("creates and returns updated metadata", () => {
      const result = handleMetaCommand(store, ctx, "/meta set status=wip priority=p0");
      assert.ok(result.includes("✅ Updated"));
      assert.ok(result.includes("Status: wip"));
      assert.ok(result.includes("Priority: p0"));
    });

    it("preserves existing fields", () => {
      store.upsert(1, "test-topic", { status: "open", assignee: "bob" });
      const result = handleMetaCommand(store, ctx, "/meta set status=done");
      assert.ok(result.includes("Status: done"));
      assert.ok(result.includes("Assignee: bob"));
    });
  });

  describe("label", () => {
    it("adds a label", () => {
      store.upsert(1, "test-topic", { status: "open" });
      const result = handleMetaCommand(store, ctx, "/meta label add urgent");
      assert.ok(result.includes("🏷️ Added label: urgent"));
      assert.ok(result.includes("[urgent]"));
    });

    it("removes a label", () => {
      store.upsert(1, "test-topic", { status: "open", labels: ["bug", "urgent"] });
      const result = handleMetaCommand(store, ctx, "/meta label rm bug");
      assert.ok(result.includes("🏷️ Removed label: bug"));
      assert.ok(result.includes("[urgent]"));
    });
  });

  describe("list", () => {
    beforeEach(() => {
      store.upsert(1, "topic-a", { status: "open", assignee: "alice" });
      store.upsert(1, "topic-b", { status: "done", assignee: "bob" });
      store.upsert(1, "topic-c", { status: "open" });
    });

    it("lists all topics in stream", () => {
      const result = handleMetaCommand(store, ctx, "/meta list");
      assert.ok(result.includes("Topics in stream (3)"));
      assert.ok(result.includes("topic-a"));
      assert.ok(result.includes("topic-b"));
      assert.ok(result.includes("topic-c"));
    });

    it("filters by status", () => {
      const result = handleMetaCommand(store, ctx, "/meta list status=open");
      assert.ok(result.includes("(2)"));
      assert.ok(result.includes("topic-a"));
      assert.ok(!result.includes("topic-b"));
    });

    it("shows 'no topics' for empty result", () => {
      const result = handleMetaCommand(store, ctx, "/meta list status=blocked");
      assert.ok(result.includes("No topics found"));
    });

    it("includes assignee in list items", () => {
      const result = handleMetaCommand(store, ctx, "/meta list");
      assert.ok(result.includes("@alice"));
      assert.ok(result.includes("@bob"));
    });
  });

  describe("clear", () => {
    it("clears existing metadata", () => {
      store.upsert(1, "test-topic", { status: "wip" });
      const result = handleMetaCommand(store, ctx, "/meta clear");
      assert.ok(result.includes("🗑️ Cleared"));
      assert.equal(store.get(1, "test-topic"), null);
    });

    it("reports when nothing to clear", () => {
      const result = handleMetaCommand(store, ctx, "/meta clear");
      assert.ok(result.includes("No metadata to clear"));
    });
  });

  describe("errors", () => {
    it("returns error for invalid command", () => {
      const result = handleMetaCommand(store, ctx, "not a command");
      assert.ok(result.includes("❌"));
    });

    it("returns error for unknown action", () => {
      const result = handleMetaCommand(store, ctx, "/meta unknown");
      assert.ok(result.includes("❌"));
      assert.ok(result.includes("Unknown action"));
    });
  });
});
