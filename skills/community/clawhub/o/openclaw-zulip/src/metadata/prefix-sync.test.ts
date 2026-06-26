import { describe, it, expect } from "vitest";
import { extractStatusPrefix, inferStatusFromRename, STATUS_PREFIXES } from "./prefix-sync.js";

describe("extractStatusPrefix", () => {
  it("extracts 🔴 as open", () => {
    const result = extractStatusPrefix("🔴 login bug");
    expect(result).toEqual({ prefix: "🔴", status: "open", baseName: "login bug" });
  });

  it("extracts 🟡 as wip", () => {
    const result = extractStatusPrefix("🟡 login bug");
    expect(result).toEqual({ prefix: "🟡", status: "wip", baseName: "login bug" });
  });

  it("extracts ✅ as done", () => {
    const result = extractStatusPrefix("✅ login bug");
    expect(result).toEqual({ prefix: "✅", status: "done", baseName: "login bug" });
  });

  it("returns null prefix for unprefixed topics", () => {
    const result = extractStatusPrefix("login bug");
    expect(result).toEqual({ prefix: null, status: null, baseName: "login bug" });
  });

  it("handles leading whitespace", () => {
    const result = extractStatusPrefix("  🔴 login bug");
    expect(result).toEqual({ prefix: "🔴", status: "open", baseName: "login bug" });
  });

  it("handles prefix with no space after", () => {
    const result = extractStatusPrefix("🔴login bug");
    expect(result).toEqual({ prefix: "🔴", status: "open", baseName: "login bug" });
  });

  it("handles empty string", () => {
    const result = extractStatusPrefix("");
    expect(result).toEqual({ prefix: null, status: null, baseName: "" });
  });
});

describe("inferStatusFromRename", () => {
  it("detects prefix change from open to wip", () => {
    expect(inferStatusFromRename("🔴 login bug", "🟡 login bug")).toBe("wip");
  });

  it("detects prefix change from wip to done", () => {
    expect(inferStatusFromRename("🟡 login bug", "✅ login bug")).toBe("done");
  });

  it("detects prefix added", () => {
    expect(inferStatusFromRename("login bug", "🔴 login bug")).toBe("open");
  });

  it("returns null when prefix removed", () => {
    expect(inferStatusFromRename("🔴 login bug", "login bug")).toBeNull();
  });

  it("returns null when prefix unchanged", () => {
    expect(inferStatusFromRename("🔴 old name", "🔴 new name")).toBeNull();
  });

  it("returns null when neither has prefix", () => {
    expect(inferStatusFromRename("old name", "new name")).toBeNull();
  });
});

describe("STATUS_PREFIXES", () => {
  it("has exactly 3 entries", () => {
    expect(STATUS_PREFIXES.size).toBe(3);
  });
});
