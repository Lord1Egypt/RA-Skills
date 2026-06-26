import { describe, it, expect } from "vitest";
import { formatThreadId, parseThreadId, getThreadTopic, isThreadMessage } from "./threading.js";

describe("threading", () => {
  describe("formatThreadId", () => {
    it("formats stream and topic", () => {
      expect(formatThreadId("general", "daily-standup")).toBe("general#daily-standup");
    });
  });

  describe("parseThreadId", () => {
    it("parses stream#topic", () => {
      expect(parseThreadId("general#daily-standup")).toEqual({
        stream: "general",
        topic: "daily-standup",
      });
    });

    it("returns undefined for stream-only (no topic)", () => {
      expect(parseThreadId("general")).toBeUndefined();
    });

    it("returns undefined for empty string", () => {
      expect(parseThreadId("")).toBeUndefined();
    });
  });

  describe("getThreadTopic", () => {
    it("extracts topic from thread id", () => {
      expect(getThreadTopic("general#daily-standup")).toBe("daily-standup");
    });

    it("returns undefined for invalid thread id", () => {
      expect(getThreadTopic("general")).toBeUndefined();
    });
  });

  describe("isThreadMessage", () => {
    it("returns true for group message with topic", () => {
      expect(isThreadMessage({ isGroup: true, topic: "my-topic" })).toBe(true);
    });

    it("returns false for DM", () => {
      expect(isThreadMessage({ isGroup: false, topic: undefined })).toBe(false);
    });

    it("returns false for group message without topic", () => {
      expect(isThreadMessage({ isGroup: true, topic: "" })).toBe(false);
    });
  });
});
