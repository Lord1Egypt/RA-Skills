/**
 * 网页授权 OAuth2 API 回归测试。
 *
 * 关键不变量：
 *   1. authorize URL 必须以 #wechat_redirect 结尾（微信硬性要求）
 *   2. authorize URL 必须用 appid（不是 access_token）
 *   3. code_to_token / refresh_token 的端点路径要对（sns/oauth2/...）
 *   4. validate 在 errcode != 0 时归一为 valid:false 不抛错
 */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { ResolvedWechatServiceAccount } from "../types.js";

vi.mock("../http-client.js", () => ({
  jsonRequest: vi.fn(),
}));

import { jsonRequest } from "../http-client.js";
import {
  buildOAuthAuthorizeUrl,
  oauthCodeToAccessToken,
  oauthGetUserInfo,
  oauthRefreshToken,
  oauthValidateAccessToken,
} from "./oauth.js";

const mockedJsonRequest = jsonRequest as unknown as ReturnType<typeof vi.fn>;

const fakeAccount = {
  accountId: "default",
  appId: "wxFAKEAPPID",
  appSecret: "FAKESECRET",
} as unknown as ResolvedWechatServiceAccount;

describe("buildOAuthAuthorizeUrl", () => {
  it("ends with #wechat_redirect (微信硬性要求)", () => {
    const url = buildOAuthAuthorizeUrl({
      account: fakeAccount,
      redirectUri: "https://huo15.com/cb",
      scope: "snsapi_base",
    });
    expect(url.endsWith("#wechat_redirect")).toBe(true);
  });

  it("uses appid (not access_token) and explicit response_type=code", () => {
    const url = buildOAuthAuthorizeUrl({
      account: fakeAccount,
      redirectUri: "https://huo15.com/cb",
      scope: "snsapi_userinfo",
      state: "csrf123",
    });
    expect(url).toContain("appid=wxFAKEAPPID");
    expect(url).toContain("response_type=code");
    expect(url).toContain("scope=snsapi_userinfo");
    expect(url).toContain("state=csrf123");
    expect(url).not.toContain("access_token=");
  });

  it("encodes redirectUri properly", () => {
    const url = buildOAuthAuthorizeUrl({
      account: fakeAccount,
      redirectUri: "https://huo15.com/cb?a=1&b=2",
      scope: "snsapi_base",
    });
    // URL.searchParams.set 会做 percent-encoding
    expect(url).toContain("redirect_uri=https%3A%2F%2Fhuo15.com%2Fcb%3Fa%3D1%26b%3D2");
  });

  it("omits state when not provided", () => {
    const url = buildOAuthAuthorizeUrl({
      account: fakeAccount,
      redirectUri: "https://huo15.com/cb",
      scope: "snsapi_base",
    });
    expect(url).not.toContain("state=");
  });
});

describe("OAuth API endpoints", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("oauthCodeToAccessToken hits sns/oauth2/access_token with appid+secret+code", async () => {
    mockedJsonRequest.mockResolvedValueOnce({
      access_token: "WEB_TOKEN",
      expires_in: 7200,
      refresh_token: "REFRESH",
      openid: "oABC",
      scope: "snsapi_userinfo",
    });
    const result = await oauthCodeToAccessToken({ account: fakeAccount, code: "CODE_001" });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("sns/oauth2/access_token");
    expect(args.method).toBe("GET");
    expect(args.query.appid).toBe("wxFAKEAPPID");
    expect(args.query.secret).toBe("FAKESECRET");
    expect(args.query.code).toBe("CODE_001");
    expect(args.query.grant_type).toBe("authorization_code");
    expect(result.openid).toBe("oABC");
  });

  it("oauthRefreshToken hits sns/oauth2/refresh_token (不带 secret)", async () => {
    mockedJsonRequest.mockResolvedValueOnce({
      access_token: "NEW_TOKEN",
      expires_in: 7200,
      refresh_token: "REFRESH",
      openid: "oABC",
      scope: "snsapi_userinfo",
    });
    await oauthRefreshToken({ account: fakeAccount, refreshToken: "OLD_REFRESH" });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("sns/oauth2/refresh_token");
    expect(args.query.appid).toBe("wxFAKEAPPID");
    expect(args.query.grant_type).toBe("refresh_token");
    expect(args.query.refresh_token).toBe("OLD_REFRESH");
    // refresh 端点 NOT 用 secret
    expect(args.query.secret).toBeUndefined();
  });

  it("oauthGetUserInfo hits sns/userinfo with web access_token + openid + lang", async () => {
    mockedJsonRequest.mockResolvedValueOnce({
      openid: "oABC",
      nickname: "测试用户",
      sex: 1,
      province: "Beijing",
      city: "Beijing",
      country: "China",
      headimgurl: "https://x.com/h.jpg",
      privilege: [],
    });
    const info = await oauthGetUserInfo({
      account: fakeAccount,
      webAccessToken: "WEB_TOKEN",
      openid: "oABC",
      lang: "en",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("sns/userinfo");
    expect(args.query.access_token).toBe("WEB_TOKEN");
    expect(args.query.openid).toBe("oABC");
    expect(args.query.lang).toBe("en");
    expect(info.nickname).toBe("测试用户");
  });

  it("oauthGetUserInfo defaults lang=zh_CN", async () => {
    mockedJsonRequest.mockResolvedValueOnce({});
    await oauthGetUserInfo({
      account: fakeAccount,
      webAccessToken: "WEB_TOKEN",
      openid: "oABC",
    });
    expect(mockedJsonRequest.mock.calls[0][0].query.lang).toBe("zh_CN");
  });

  it("oauthValidateAccessToken returns valid:true on success", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ errcode: 0, errmsg: "ok" });
    const result = await oauthValidateAccessToken({
      account: fakeAccount,
      webAccessToken: "WEB_TOKEN",
      openid: "oABC",
    });
    expect(result.valid).toBe(true);
  });

  it("oauthValidateAccessToken归一化失败为 valid:false（不抛错）", async () => {
    // 模拟 jsonRequest 抛 errcode != 0 异常
    mockedJsonRequest.mockRejectedValueOnce(
      Object.assign(new Error("[wechat-service] API sns/auth failed: errcode=40003"), {
        errcode: 40003,
      }),
    );
    const result = await oauthValidateAccessToken({
      account: fakeAccount,
      webAccessToken: "BAD_TOKEN",
      openid: "oABC",
    });
    expect(result.valid).toBe(false);
    expect(result.raw).toHaveProperty("error");
  });
});
