import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { isParseError, parseMetaCommand } from "./command-parser.ts";

describe("parseMetaCommand", () => {
  describe("non-meta input", () => {
    it("rejects non /meta text", () => {
      const result = parseMetaCommand("hello world");
      assert.ok(isParseError(result));
    });

    it("rejects similar prefixes", () => {
      assert.ok(isParseError(parseMetaCommand("/metadata show")));
    });
  });

  describe("show", () => {
    it("bare /meta defaults to show", () => {
      const result = parseMetaCommand("/meta");
      assert.ok(!isParseError(result));
      assert.equal(result.action, "show");
    });

    it("explicit /meta show", () => {
      const result = parseMetaCommand("/meta show");
      assert.ok(!isParseError(result));
      assert.equal(result.action, "show");
    });

    it("handles extra whitespace", () => {
      const result = parseMetaCommand("  /meta   show  ");
      assert.ok(!isParseError(result));
      assert.equal(result.action, "show");
    });
  });

  describe("set", () => {
    it("sets a single field", () => {
      const result = parseMetaCommand("/meta set status=wip");
      assert.ok(!isParseError(result));
      assert.equal(result.action, "set");
      if (result.action === "set") {
        assert.equal(result.updates.status, "wip");
      }
    });

    it("sets multiple fields", () => {
      const result = parseMetaCommand("/meta set status=open priority=p1 assignee=alice");
      assert.ok(!isParseError(result));
      if (result.action === "set") {
        assert.equal(result.updates.status, "open");
        assert.equal(result.updates.priority, "p1");
        assert.equal(result.updates.assignee, "alice");
      }
    });

    it("errors on no args", () => {
      const result = parseMetaCommand("/meta set");
      assert.ok(isParseError(result));
    });

    it("errors on invalid key=value", () => {
      const result = parseMetaCommand("/meta set foobar");
      assert.ok(isParseError(result));
    });

    it("errors on unknown field", () => {
      const result = parseMetaCommand("/meta set color=red");
      assert.ok(isParseError(result));
    });

    it("errors on invalid status", () => {
      const result = parseMetaCommand("/meta set status=invalid");
      assert.ok(isParseError(result));
    });

    it("errors on invalid priority", () => {
      const result = parseMetaCommand("/meta set priority=p9");
      assert.ok(isParseError(result));
    });

    it("sets due_date", () => {
      const result = parseMetaCommand("/meta set due_date=2026-05-01");
      assert.ok(!isParseError(result));
      if (result.action === "set") {
        assert.equal(result.updates.due_date, "2026-05-01");
      }
    });

    it("clears assignee with empty value", () => {
      const result = parseMetaCommand("/meta set assignee=");
      assert.ok(!isParseError(result));
      if (result.action === "set") {
        assert.equal(result.updates.assignee, null);
      }
    });
  });

  describe("label", () => {
    it("parses label add", () => {
      const result = parseMetaCommand("/meta label add bug");
      assert.ok(!isParseError(result));
      if (result.action === "label") {
        assert.equal(result.op, "add");
        assert.equal(result.tag, "bug");
      }
    });

    it("parses label rm", () => {
      const result = parseMetaCommand("/meta label rm feature");
      assert.ok(!isParseError(result));
      if (result.action === "label") {
        assert.equal(result.op, "rm");
        assert.equal(result.tag, "feature");
      }
    });

    it("handles multi-word tags", () => {
      const result = parseMetaCommand("/meta label add high priority");
      assert.ok(!isParseError(result));
      if (result.action === "label") {
        assert.equal(result.tag, "high priority");
      }
    });

    it("errors on missing args", () => {
      assert.ok(isParseError(parseMetaCommand("/meta label")));
      assert.ok(isParseError(parseMetaCommand("/meta label add")));
    });

    it("errors on invalid op", () => {
      const result = parseMetaCommand("/meta label delete bug");
      assert.ok(isParseError(result));
    });
  });

  describe("list", () => {
    it("parses list with no filter", () => {
      const result = parseMetaCommand("/meta list");
      assert.ok(!isParseError(result));
      assert.equal(result.action, "list");
      if (result.action === "list") {
        assert.deepEqual(result.filter, {});
      }
    });

    it("parses list with status filter", () => {
      const result = parseMetaCommand("/meta list status=open");
      assert.ok(!isParseError(result));
      if (result.action === "list") {
        assert.equal(result.filter.status, "open");
      }
    });

    it("parses list with multiple filters", () => {
      const result = parseMetaCommand("/meta list status=wip assignee=bob");
      assert.ok(!isParseError(result));
      if (result.action === "list") {
        assert.equal(result.filter.status, "wip");
        assert.equal(result.filter.assignee, "bob");
      }
    });

    it("errors on unknown filter key", () => {
      const result = parseMetaCommand("/meta list color=red");
      assert.ok(isParseError(result));
    });

    it("errors on invalid filter format", () => {
      const result = parseMetaCommand("/meta list foobar");
      assert.ok(isParseError(result));
    });
  });

  describe("clear", () => {
    it("parses clear", () => {
      const result = parseMetaCommand("/meta clear");
      assert.ok(!isParseError(result));
      assert.equal(result.action, "clear");
    });
  });

  describe("unknown action", () => {
    it("returns error for unknown action", () => {
      const result = parseMetaCommand("/meta foobar");
      assert.ok(isParseError(result));
      assert.ok(result.error.includes("Unknown action"));
    });
  });
});
