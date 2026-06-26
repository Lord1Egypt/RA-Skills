import { describe, expect, it } from "vitest";
import {
  formatStreamTopic,
  isStreamTarget,
  normalizeZulipAllowEntry,
  normalizeZulipAllowlist,
  normalizeZulipMessagingTarget,
  parseStreamTopic,
} from "./normalize.js";

describe("zulip normalize", () => {
  describe("parseStreamTopic", () => {
    it("parses stream#topic", () => {
      expect(parseStreamTopic("general#greetings")).toEqual({
        stream: "general",
        topic: "greetings",
      });
    });

    it("parses stream-only with trailing #", () => {
      expect(parseStreamTopic("general#")).toEqual({
        stream: "general",
        topic: undefined,
      });
    });

    it("returns undefined for no separator", () => {
      expect(parseStreamTopic("general")).toBeUndefined();
    });

    it("returns undefined for empty stream", () => {
      expect(parseStreamTopic("#topic")).toBeUndefined();
    });

    it("returns undefined for empty input", () => {
      expect(parseStreamTopic("")).toBeUndefined();
      expect(parseStreamTopic("  ")).toBeUndefined();
    });

    it("handles streams with spaces", () => {
      expect(parseStreamTopic("my stream#my topic")).toEqual({
        stream: "my stream",
        topic: "my topic",
      });
    });
  });

  describe("formatStreamTopic", () => {
    it("formats stream and topic", () => {
      expect(formatStreamTopic("general", "greetings")).toBe("general#greetings");
    });

    it("formats stream only", () => {
      expect(formatStreamTopic("general")).toBe("general");
      expect(formatStreamTopic("general", undefined)).toBe("general");
    });
  });

  describe("isStreamTarget", () => {
    it("detects stream targets", () => {
      expect(isStreamTarget("general#greetings")).toBe(true);
      expect(isStreamTarget("general#")).toBe(true);
    });

    it("rejects non-stream targets", () => {
      expect(isStreamTarget("12345")).toBe(false);
      expect(isStreamTarget("user@example.com")).toBe(false);
    });
  });

  describe("normalizeZulipMessagingTarget", () => {
    it("returns undefined for empty input", () => {
      expect(normalizeZulipMessagingTarget("")).toBeUndefined();
      expect(normalizeZulipMessagingTarget("  ")).toBeUndefined();
      expect(normalizeZulipMessagingTarget("\n")).toBeUndefined();
    });

    it("passes through short-form stream#topic", () => {
      expect(normalizeZulipMessagingTarget("general#greetings")).toBe("general#greetings");
    });

    it("passes through short-form user id", () => {
      expect(normalizeZulipMessagingTarget("12345")).toBe("12345");
    });

    it("strips group: prefix", () => {
      expect(normalizeZulipMessagingTarget("group:general#greetings")).toBe("general#greetings");
    });

    it("strips direct: prefix", () => {
      expect(normalizeZulipMessagingTarget("direct:12345")).toBe("12345");
    });

    it("strips full zulip:account:group: prefix", () => {
      expect(normalizeZulipMessagingTarget("zulip:myorg:group:general#greetings")).toBe(
        "general#greetings",
      );
    });

    it("strips full zulip:account:direct: prefix", () => {
      expect(normalizeZulipMessagingTarget("zulip:myorg:direct:12345")).toBe("12345");
    });

    it("strips zulip: without account when followed by group:", () => {
      expect(normalizeZulipMessagingTarget("zulip:group:general#hi")).toBe("general#hi");
    });

    it("is case-insensitive for prefixes", () => {
      expect(normalizeZulipMessagingTarget("ZULIP:myorg:GROUP:general#hi")).toBe("general#hi");
      expect(normalizeZulipMessagingTarget("Direct:12345")).toBe("12345");
    });

    it("returns undefined for empty target after prefix strip", () => {
      expect(normalizeZulipMessagingTarget("group:")).toBeUndefined();
      expect(normalizeZulipMessagingTarget("direct:")).toBeUndefined();
    });
  });

  describe("normalizeZulipAllowEntry", () => {
    it("lowercases and strips zulip: prefix", () => {
      expect(normalizeZulipAllowEntry("Zulip:Alice@example.com")).toBe("alice@example.com");
    });

    it("strips direct: prefix", () => {
      expect(normalizeZulipAllowEntry("direct:12345")).toBe("12345");
    });

    it("strips group: prefix", () => {
      expect(normalizeZulipAllowEntry("group:general#greetings")).toBe("general#greetings");
    });

    it("strips combined zulip:direct: prefix", () => {
      expect(normalizeZulipAllowEntry("zulip:direct:12345")).toBe("12345");
    });

    it("returns empty for empty input", () => {
      expect(normalizeZulipAllowEntry("")).toBe("");
      expect(normalizeZulipAllowEntry("  ")).toBe("");
    });
  });

  describe("normalizeZulipAllowlist", () => {
    it("normalizes all entries and filters empties", () => {
      expect(
        normalizeZulipAllowlist(["Zulip:Alice@example.com", "", "direct:12345", 67890]),
      ).toEqual(["alice@example.com", "12345", "67890"]);
    });

    it("returns empty array for undefined", () => {
      expect(normalizeZulipAllowlist()).toEqual([]);
    });

    it("handles numeric entries", () => {
      expect(normalizeZulipAllowlist([123, 456])).toEqual(["123", "456"]);
    });
  });
});
