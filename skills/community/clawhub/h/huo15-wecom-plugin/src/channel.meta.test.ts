import { describe, expect, it } from "vitest";
import { wecomPlugin } from "./channel.js";

describe("wecomPlugin meta", () => {
  it("uses chinese-facing labels in channel selection", () => {
    expect(wecomPlugin.meta.label).toBe("WeCom (企业微信)");
    expect(wecomPlugin.meta.selectionLabel).toBe("WeCom (企业微信)");
    expect(wecomPlugin.meta.blurb).toContain("企业微信官方推荐三方插件");
    expect(wecomPlugin.meta.docsLabel).toBe("企业微信");
    expect(wecomPlugin.meta.selectionDocsPrefix).toBe("文档：");
  });

  it("exposes a setupWizard for guided setup discovery", () => {
    expect(wecomPlugin.setupWizard?.channel).toBe("wecom");
  });

  it("preserves fully qualified WeCom messaging targets during normalization", () => {
    expect(wecomPlugin.messaging?.normalizeTarget?.("wecom:user:zhangsan")).toBe(
      "wecom:user:zhangsan",
    );
    expect(wecomPlugin.messaging?.normalizeTarget?.("wecom-agent:blue:user:zhangsan")).toBe(
      "wecom-agent:blue:user:zhangsan",
    );
    expect(wecomPlugin.messaging?.normalizeTarget?.("wecom:zhangsan")).toBe("zhangsan");
  });
});
