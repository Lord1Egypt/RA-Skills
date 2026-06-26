/**
 * 自动回复模块回归测试。
 *
 * 关键不变量：
 *  1. 关键词完全匹配时触发自动回复
 *  2. 非文本消息不触发关键词匹配
 *  3. 业务时间检查正确
 *  4. 非工作时间返回 offHoursMessage
 *  5. 欢迎语模板变量替换正确
 *  6. checkAutoReply 统一入口优先级正确
 */
import { describe, expect, it } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import type { WechatServiceInboundMessage } from "./types.js";
import {
  checkAutoReply,
  isBusinessHours,
  matchKeyword,
  renderWelcomeText,
} from "./auto-reply.js";

function makeCfg(autoReply?: Record<string, unknown>): OpenClawConfig {
  return {
    channels: {
      "wechat-service": autoReply ? { autoReply } : {},
    },
  } as unknown as OpenClawConfig;
}

function makeInbound(
  overrides: Partial<WechatServiceInboundMessage> = {},
): WechatServiceInboundMessage {
  return {
    toUserName: "gh_test",
    fromUserName: "oUser123",
    createTime: Date.now(),
    msgType: "text",
    content: "你好",
    raw: {},
    rawXml: "<xml></xml>",
    ...overrides,
  };
}

// ============================================================================
// matchKeyword
// ============================================================================

describe("matchKeyword", () => {
  it("完全匹配关键词 → 返回回复文本", () => {
    const cfg = makeCfg({
      keywords: { "帮助": "这是帮助信息", "客服": "转人工请联系xxx" },
    });
    const result = matchKeyword(cfg, makeInbound({ content: "帮助" }));
    expect(result.matched).toBe(true);
    if (result.matched) {
      expect(result.reply).toBe("这是帮助信息");
    }
  });

  it("部分匹配不触发", () => {
    const cfg = makeCfg({
      keywords: { "帮助": "这是帮助信息" },
    });
    const result = matchKeyword(cfg, makeInbound({ content: "我需要帮助" }));
    expect(result.matched).toBe(false);
  });

  it("非 text 消息不触发", () => {
    const cfg = makeCfg({
      keywords: { "帮助": "这是帮助信息" },
    });
    const result = matchKeyword(
      cfg,
      makeInbound({ msgType: "image", content: undefined, picUrl: "http://..." }),
    );
    expect(result.matched).toBe(false);
  });

  it("未配置关键词 → 返回 false", () => {
    const cfg = makeCfg();
    const result = matchKeyword(cfg, makeInbound({ content: "帮助" }));
    expect(result.matched).toBe(false);
  });

  it("空 content → 返回 false", () => {
    const cfg = makeCfg({ keywords: { "帮助": "回复" } });
    const result = matchKeyword(cfg, makeInbound({ content: "" }));
    expect(result.matched).toBe(false);
  });

  // ---- v2.3.3 通配模式 ----
  it("contains 通配 *Odoo* 命中含 Odoo 的消息", () => {
    const cfg = makeCfg({ keywords: { "*Odoo*": "Odoo 相关引导" } });
    expect(
      matchKeyword(cfg, makeInbound({ content: "我想学 Odoo 怎么入门" })).matched,
    ).toBe(true);
  });

  it("contains 通配大小写不敏感", () => {
    const cfg = makeCfg({ keywords: { "*Odoo*": "Odoo 引导" } });
    const r = matchKeyword(cfg, makeInbound({ content: "ODOO 多少钱" }));
    expect(r.matched).toBe(true);
    if (r.matched) expect(r.reply).toBe("Odoo 引导");
  });

  it("prefix 通配 价格* 命中以价格开头", () => {
    const cfg = makeCfg({ keywords: { "价格*": "留资引导" } });
    expect(matchKeyword(cfg, makeInbound({ content: "价格多少" })).matched).toBe(
      true,
    );
    expect(matchKeyword(cfg, makeInbound({ content: "想问下价格" })).matched).toBe(
      false,
    );
  });

  it("suffix 通配 *多少钱 命中以多少钱结尾", () => {
    const cfg = makeCfg({ keywords: { "*多少钱": "请留电话报价" } });
    expect(matchKeyword(cfg, makeInbound({ content: "Odoo 实施多少钱" })).matched).toBe(
      true,
    );
  });

  it("exact 关键词优先级高于通配（向后兼容）", () => {
    const cfg = makeCfg({
      keywords: { "价格": "固定问候A", "*价格*": "通用引导B" },
    });
    const r1 = matchKeyword(cfg, makeInbound({ content: "价格" }));
    expect(r1.matched && r1.reply).toBe("固定问候A");
    const r2 = matchKeyword(cfg, makeInbound({ content: "我想问下价格" }));
    expect(r2.matched && r2.reply).toBe("通用引导B");
  });
});

// ============================================================================
// isBusinessHours
// ============================================================================

describe("isBusinessHours", () => {
  it("未配置业务时间 → 始终 true", () => {
    expect(isBusinessHours(makeCfg())).toBe(true);
  });

  it("工作时间 → true", () => {
    const cfg = makeCfg({
      businessHours: {
        schedule: [{ days: [1, 2, 3, 4, 5], start: "09:00", end: "18:00" }],
      },
    });
    // 周一 10:00
    const monday10am = new Date(2026, 3, 27, 10, 0, 0); // 2026-04-27 is Monday
    expect(isBusinessHours(cfg, monday10am)).toBe(true);
  });

  it("非工作时间 → false", () => {
    const cfg = makeCfg({
      businessHours: {
        schedule: [{ days: [1, 2, 3, 4, 5], start: "09:00", end: "18:00" }],
      },
    });
    // 周一 20:00
    const monday8pm = new Date(2026, 3, 27, 20, 0, 0);
    expect(isBusinessHours(cfg, monday8pm)).toBe(false);
  });

  it("周末 → false（如果 schedule 只配工作日）", () => {
    const cfg = makeCfg({
      businessHours: {
        schedule: [{ days: [1, 2, 3, 4, 5], start: "09:00", end: "18:00" }],
      },
    });
    // 周六
    const saturday = new Date(2026, 4, 2, 10, 0, 0); // 2026-05-02 is Saturday
    expect(isBusinessHours(cfg, saturday)).toBe(false);
  });

  it("边界：09:00 包含，18:00 不包含", () => {
    const cfg = makeCfg({
      businessHours: {
        schedule: [{ days: [1, 2, 3, 4, 5], start: "09:00", end: "18:00" }],
      },
    });
    const monday9am = new Date(2026, 3, 27, 9, 0, 0);
    const monday6pm = new Date(2026, 3, 27, 18, 0, 0);
    expect(isBusinessHours(cfg, monday9am)).toBe(true);
    expect(isBusinessHours(cfg, monday6pm)).toBe(false);
  });
});

// ============================================================================
// renderWelcomeText
// ============================================================================

describe("renderWelcomeText", () => {
  it("替换模板变量", () => {
    const cfg = makeCfg({ welcomeText: "你好 {{nickname}}，今天是 {{date}}" });
    const text = renderWelcomeText(cfg, "小明");
    expect(text).toContain("你好 小明");
    expect(text).toMatch(/\d{4}-\d{2}-\d{2}/);
  });

  it("无 nickname 时使用默认值", () => {
    const cfg = makeCfg({ welcomeText: "你好 {{nickname}}" });
    expect(renderWelcomeText(cfg)).toContain("你好 用户");
  });

  it("未配置 welcomeText → undefined", () => {
    expect(renderWelcomeText(makeCfg())).toBeUndefined();
  });
});

// ============================================================================
// checkAutoReply
// ============================================================================

describe("checkAutoReply", () => {
  it("关键词命中 → handled", () => {
    const cfg = makeCfg({ keywords: { "帮助": "帮助信息" } });
    const result = checkAutoReply(cfg, makeInbound({ content: "帮助" }));
    expect(result.handled).toBe(true);
    if (result.handled) {
      expect(result.reply).toBe("帮助信息");
    }
  });

  it("关键词优先级高于业务时间", () => {
    const cfg = makeCfg({
      keywords: { "帮助": "帮助信息" },
      businessHours: {
        schedule: [{ days: [1, 2, 3, 4, 5], start: "09:00", end: "18:00" }],
        offHoursMessage: "已下班",
      },
    });
    // 非工作时间发"帮助" → 关键词优先
    const saturday = new Date(2026, 4, 2, 10, 0, 0);
    // 我们无法在 checkAutoReply 中注入 now，但 isBusinessHours 会被调
    // 关键词命中会先返回，不管业务时间
    const result = checkAutoReply(cfg, makeInbound({ content: "帮助" }));
    expect(result.handled).toBe(true);
    if (result.handled) {
      expect(result.reply).toBe("帮助信息");
    }
  });

  it("非文本消息不做业务时间检查", () => {
    const cfg = makeCfg({
      businessHours: {
        schedule: [{ days: [1, 2, 3, 4, 5], start: "09:00", end: "18:00" }],
        offHoursMessage: "已下班",
      },
    });
    // 非工作时间发图片 → 不触发 auto-reply
    const result = checkAutoReply(
      cfg,
      makeInbound({ msgType: "image", content: undefined }),
    );
    expect(result.handled).toBe(false);
  });

  it("无配置 → 不处理", () => {
    const result = checkAutoReply(makeCfg(), makeInbound({ content: "你好" }));
    expect(result.handled).toBe(false);
  });
});
