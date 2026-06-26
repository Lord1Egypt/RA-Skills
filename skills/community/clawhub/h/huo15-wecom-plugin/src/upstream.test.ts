import { describe, expect, it } from "vitest";

import { resolveScopedWecomTarget } from "./target.js";
import {
  buildUpstreamAgentSessionTarget,
  parseUpstreamAgentSessionTarget,
} from "./upstream/index.js";

describe("upstream target helpers", () => {
  it("builds and parses the canonical upstream agent target", () => {
    const target = buildUpstreamAgentSessionTarget("zhangsan", "acct-a", "corp-up");

    expect(target).toBe("wecom-agent-upstream:acct-a:corp-up:zhangsan");
    expect(parseUpstreamAgentSessionTarget(target)).toEqual({
      accountId: "acct-a",
      upstreamCorpId: "corp-up",
      userId: "zhangsan",
    });
  });

  it("keeps compatibility with legacy upstream-prefixed targets", () => {
    expect(
      parseUpstreamAgentSessionTarget("wecom-agent-upstream:acct-a:corp-up:zhangsan"),
    ).toEqual({
      accountId: "acct-a",
      upstreamCorpId: "corp-up",
      userId: "zhangsan",
    });
  });

  it("keeps compatibility with query-style upstream targets", () => {
    expect(
      parseUpstreamAgentSessionTarget(
        "wecom-agent:acct-a:user:zhangsan?upstream_corp=corp-up",
      ),
    ).toEqual({
      accountId: "acct-a",
      upstreamCorpId: "corp-up",
      userId: "zhangsan",
    });
  });

  it("resolves upstream-scoped targets to the real touser without leaking corp metadata", () => {
    expect(
      resolveScopedWecomTarget("wecom-agent-upstream:acct-a:corp-up:zhangsan", "default"),
    ).toEqual({
      accountId: "acct-a",
      target: { touser: "zhangsan" },
      rawTarget: "zhangsan",
    });

    expect(
      resolveScopedWecomTarget(
        "wecom-agent:acct-a:user:zhangsan?upstream_corp=corp-up",
        "default",
      ),
    ).toEqual({
      accountId: "acct-a",
      target: { touser: "zhangsan" },
      rawTarget: "zhangsan",
    });
  });

  it("keeps normal users and upstream users distinguishable", () => {
    // 普通用户目标：不带 upstream 标识，应按普通 agent target 解析
    expect(resolveScopedWecomTarget("wecom-agent:acct-a:user:zhangsan", "default")).toEqual({
      accountId: "acct-a",
      target: { touser: "zhangsan" },
      rawTarget: "user:zhangsan",
    });

    // 上下游用户目标：带 upstream_corp，应走 upstream 解析
    expect(
      resolveScopedWecomTarget(
        "wecom-agent:acct-a:user:zhangsan?upstream_corp=corp-up",
        "default",
      ),
    ).toEqual({
      accountId: "acct-a",
      target: { touser: "zhangsan" },
      rawTarget: "zhangsan",
    });
  });
});