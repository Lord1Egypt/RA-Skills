/**
 * wechatServiceSetupAdapter 测试 —— v2.0.0 新增的 CLI `channels add` 入口。
 *
 * 关键不变量：
 *  1. resolveAccountId 提供值时按 trim 后回传，没提供时返回 default
 *  2. applyAccountConfig 写出 kebab-case 配置 key（channels["wechat-service"]，不是 wechatService）
 *  3. --name / --token 经 CLI 入参写入对应字段
 *  4. 环境变量 WECHAT_SERVICE_APP_ID / APP_SECRET / ENCODING_AES_KEY 被读取
 *  5. 非 default 账号用 WECHAT_SERVICE_<UPPER_ACCOUNTID>_APP_ID 这种带 accountId 的前缀
 *  6. 没填 encodingAESKey 时 encryptMode 落到 plain
 *  7. validateInput 校验 name 长度
 */
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import { wechatServiceSetupAdapter } from "./onboarding.js";

const ORIGINAL_ENV = { ...process.env };

function emptyCfg(): OpenClawConfig {
  return {} as unknown as OpenClawConfig;
}

describe("wechatServiceSetupAdapter", () => {
  beforeEach(() => {
    // 清理可能影响测试的 env
    for (const k of Object.keys(process.env)) {
      if (k.startsWith("WECHAT_SERVICE_")) delete process.env[k];
    }
  });

  afterEach(() => {
    process.env = { ...ORIGINAL_ENV };
  });

  describe("resolveAccountId", () => {
    it("returns provided accountId trimmed", () => {
      const id = wechatServiceSetupAdapter.resolveAccountId?.({
        cfg: emptyCfg(),
        accountId: "  shop-a  ",
      });
      expect(id).toBe("shop-a");
    });

    it("falls back to 'default' when accountId omitted", () => {
      const id = wechatServiceSetupAdapter.resolveAccountId?.({
        cfg: emptyCfg(),
        accountId: undefined,
      });
      expect(id).toBe("default");
    });
  });

  describe("validateInput", () => {
    it("returns null when no issues", () => {
      const result = wechatServiceSetupAdapter.validateInput?.({
        cfg: emptyCfg(),
        accountId: "main",
        input: { name: "我的公众号" },
      });
      expect(result).toBe(null);
    });

    it("rejects name longer than 60 chars", () => {
      const longName = "x".repeat(80);
      const result = wechatServiceSetupAdapter.validateInput?.({
        cfg: emptyCfg(),
        accountId: "main",
        input: { name: longName },
      });
      expect(result).toContain("name 太长");
    });
  });

  describe("applyAccountConfig", () => {
    it("writes kebab-case key channels[wechat-service] (not legacy wechatService)", () => {
      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "main",
        input: { name: "我的公众号", token: "MY_TOKEN" },
      }) as { channels?: Record<string, unknown> };
      expect(cfg.channels?.["wechat-service"]).toBeDefined();
      expect(cfg.channels?.wechatService).toBeUndefined();
    });

    it("writes name + token from CLI input", () => {
      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "main",
        input: { name: "我的公众号", token: "TOKEN_VALUE" },
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };
      const main = cfg.channels?.["wechat-service"]?.accounts?.main;
      expect(main?.name).toBe("我的公众号");
      expect(main?.token).toBe("TOKEN_VALUE");
      expect(main?.enabled).toBe(true);
    });

    it("reads default-account env vars (WECHAT_SERVICE_APP_ID / APP_SECRET / ENCODING_AES_KEY)", () => {
      process.env.WECHAT_SERVICE_APP_ID = "wxFAKEAPPID";
      process.env.WECHAT_SERVICE_APP_SECRET = "FAKESECRET";
      process.env.WECHAT_SERVICE_ENCODING_AES_KEY = "x".repeat(43);

      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "default",
        input: { token: "TOKEN" },
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };

      const acc = cfg.channels?.["wechat-service"]?.accounts?.default;
      expect(acc?.appId).toBe("wxFAKEAPPID");
      expect(acc?.appSecret).toBe("FAKESECRET");
      expect(acc?.encodingAESKey).toBe("x".repeat(43));
      expect(acc?.encryptMode).toBe("safe");
    });

    it("non-default account reads WECHAT_SERVICE_<ACCOUNTID>_* env vars", () => {
      process.env.WECHAT_SERVICE_SHOP_A_APP_ID = "wxSHOP_A";
      process.env.WECHAT_SERVICE_SHOP_A_APP_SECRET = "SHOP_A_SECRET";
      // default-prefix vars 不应该被读到
      process.env.WECHAT_SERVICE_APP_ID = "wxDEFAULT";

      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "shop-a",
        input: {},
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };

      const acc = cfg.channels?.["wechat-service"]?.accounts?.["shop-a"];
      expect(acc?.appId).toBe("wxSHOP_A");
      expect(acc?.appSecret).toBe("SHOP_A_SECRET");
    });

    it("non-default account falls back to generic env vars when account-prefixed missing", () => {
      // 只有 generic env，没有 SHOP_A 专用
      process.env.WECHAT_SERVICE_APP_ID = "wxFALLBACK";

      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "shop-a",
        input: {},
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };

      const acc = cfg.channels?.["wechat-service"]?.accounts?.["shop-a"];
      expect(acc?.appId).toBe("wxFALLBACK");
    });

    it("falls back to encryptMode=plain when no AES key in env (test only, not for prod)", () => {
      // 没设任何 ENCODING_AES_KEY env
      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "main",
        input: { token: "T" },
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };

      const acc = cfg.channels?.["wechat-service"]?.accounts?.main;
      expect(acc?.encryptMode).toBe("plain");
      expect(acc?.encodingAESKey).toBeUndefined();
    });

    it("preserves existing accounts when adding a new one", () => {
      const baseCfg = {
        channels: {
          "wechat-service": {
            enabled: true,
            accounts: {
              old: { appId: "wxOLD", enabled: true },
            },
          },
        },
      } as unknown as OpenClawConfig;

      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: baseCfg,
        accountId: "new",
        input: { name: "New Account" },
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };

      const accounts = cfg.channels?.["wechat-service"]?.accounts;
      expect(accounts?.old).toBeDefined();
      expect(accounts?.old?.appId).toBe("wxOLD");
      expect(accounts?.new).toBeDefined();
      expect(accounts?.new?.name).toBe("New Account");
    });

    it("sets defaultAccount when first added", () => {
      const cfg = wechatServiceSetupAdapter.applyAccountConfig({
        cfg: emptyCfg(),
        accountId: "shop-a",
        input: { name: "Shop A" },
      }) as { channels?: { "wechat-service"?: { defaultAccount?: string } } };
      expect(cfg.channels?.["wechat-service"]?.defaultAccount).toBe("shop-a");
    });
  });

  describe("applyAccountName", () => {
    it("updates name when provided", () => {
      const cfg = wechatServiceSetupAdapter.applyAccountName?.({
        cfg: emptyCfg(),
        accountId: "main",
        name: "我的新名字",
      }) as { channels?: { "wechat-service"?: { accounts?: Record<string, Record<string, unknown>> } } };
      expect(cfg.channels?.["wechat-service"]?.accounts?.main?.name).toBe("我的新名字");
    });

    it("returns cfg unchanged when name is empty", () => {
      const baseCfg = emptyCfg();
      const cfg = wechatServiceSetupAdapter.applyAccountName?.({
        cfg: baseCfg,
        accountId: "main",
        name: "  ",
      });
      expect(cfg).toBe(baseCfg);
    });
  });
});
