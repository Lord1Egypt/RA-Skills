import { describe, expect, it } from "vitest";

import { isBroadcastLiteral, resolveWecomTarget, resolveScopedWecomTarget } from "./target.js";

describe("wecom target - broadcast guard", () => {
  it("flags bare @all as a broadcast literal", () => {
    expect(isBroadcastLiteral("@all")).toBe(true);
    expect(isBroadcastLiteral("@ALL")).toBe(true);
    expect(isBroadcastLiteral("@everyone")).toBe(true);
    expect(isBroadcastLiteral("*")).toBe(true);
    expect(isBroadcastLiteral("all")).toBe(true);
  });

  it("does not flag regular userids or chat ids", () => {
    expect(isBroadcastLiteral("ZhaoBo")).toBe(false);
    expect(isBroadcastLiteral("wrabc123")).toBe(false);
    expect(isBroadcastLiteral("12345")).toBe(false);
    expect(isBroadcastLiteral(undefined)).toBe(false);
    expect(isBroadcastLiteral("")).toBe(false);
  });

  it("refuses @all as a raw target", () => {
    expect(resolveWecomTarget("@all")).toBeUndefined();
    expect(resolveWecomTarget("@everyone")).toBeUndefined();
    expect(resolveWecomTarget("*")).toBeUndefined();
  });

  it("refuses @all even when wrapped in wecom:user: prefix", () => {
    expect(resolveWecomTarget("wecom:user:@all")).toBeUndefined();
    expect(resolveWecomTarget("user:@all")).toBeUndefined();
    expect(resolveWecomTarget("wecom-agent:@all")).toBeUndefined();
    expect(resolveWecomTarget("party:@all")).toBeUndefined();
  });

  it("refuses broadcast literal via scoped target helper", () => {
    expect(resolveScopedWecomTarget("@all", "default")).toBeUndefined();
    expect(resolveScopedWecomTarget("wecom-agent:default:@all", "default")).toBeUndefined();
  });

  it("still resolves legitimate targets", () => {
    expect(resolveWecomTarget("ZhaoBo")).toEqual({ touser: "ZhaoBo" });
    expect(resolveWecomTarget("user:ZhaoBo")).toEqual({ touser: "ZhaoBo" });
    expect(resolveWecomTarget("party:1")).toEqual({ toparty: "1" });
    expect(resolveWecomTarget("wrabc123")).toEqual({ chatid: "wrabc123" });
    expect(resolveWecomTarget("12345")).toEqual({ touser: "12345" });
  });
});
