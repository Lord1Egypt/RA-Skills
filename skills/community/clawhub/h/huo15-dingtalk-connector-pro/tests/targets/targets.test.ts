import { describe, expect, it } from "vitest";
import {
  formatDingtalkTarget,
  looksLikeDingtalkId,
  normalizeDingtalkTarget,
} from "../../src/targets";

describe("targets helpers", () => {
  describe("normalizeDingtalkTarget", () => {
    it("returns null for empty value", () => {
      expect(normalizeDingtalkTarget("   ")).toBeNull();
    });

    it("normalizes provider-prefixed user target", () => {
      expect(normalizeDingtalkTarget("dingtalk:user:abc")).toBe("abc");
      expect(normalizeDingtalkTarget("dd:user: abc ")).toBe("abc");
      expect(normalizeDingtalkTarget("ding:user:abc")).toBe("abc");
    });

    it("normalizes provider-prefixed group target", () => {
      expect(normalizeDingtalkTarget("dingtalk:group:conv-1")).toBe("conv-1");
    });

    it("returns null for empty explicit user/group suffix", () => {
      expect(normalizeDingtalkTarget("user:")).toBeNull();
      expect(normalizeDingtalkTarget("group:   ")).toBeNull();
    });

    it("returns id directly when no user/group marker", () => {
      expect(normalizeDingtalkTarget("  user-id-001  ")).toBe("user-id-001");
    });
  });

  describe("formatDingtalkTarget", () => {
    it("formats group and user targets", () => {
      expect(formatDingtalkTarget(" conv ", "group")).toBe("group:conv");
      expect(formatDingtalkTarget(" user ", "user")).toBe("user:user");
    });

    it("returns trimmed id when type missing", () => {
      expect(formatDingtalkTarget("  raw  ")).toBe("raw");
    });
  });

  describe("looksLikeDingtalkId", () => {
    it("returns false for blank input", () => {
      expect(looksLikeDingtalkId("")).toBe(false);
      expect(looksLikeDingtalkId("  ")).toBe(false);
    });

    it("returns true for raw and explicit targets", () => {
      expect(looksLikeDingtalkId("abc")).toBe(true);
      expect(looksLikeDingtalkId("user:abc")).toBe(true);
      expect(looksLikeDingtalkId("group:conv")).toBe(true);
      expect(looksLikeDingtalkId("dingtalk:user:abc")).toBe(true);
    });
  });
});
