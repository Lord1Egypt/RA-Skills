/**
 * OAuth helpers — unit tests with fetch mocks
 *
 * Covers Azure AD OAuth 2.0 Authorization Code Flow for Dataverse access.
 *
 * Token endpoint docs:
 *  https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
 *
 * Dataverse OAuth docs:
 *  https://learn.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth
 */

import {
  exchangeCodeForTokens,
  getAuthorizationUrl,
  isTokenExpired,
  refreshAccessToken,
} from "../src/oauth.js";
import type { Dynamics365Config, OAuthTokens } from "../src/types.js";

// ─── Fixtures ────────────────────────────────────────────────────────────────

const CONFIG: Dynamics365Config = {
  clientId: "10b1389b-e0e9-48da-a431-765a92216007",
  clientSecret: "mock-secret-value",
  tenantId: "common",
  instanceUrl: "https://contoso.crm.dynamics.com",
};

const REDIRECT_URI = "http://localhost:3000/auth/dynamics365/callback";

/** Simulate a successful token endpoint response */
function mockTokenResponse(overrides: Partial<{
  access_token: string;
  refresh_token: string;
  expires_in: number;
}> = {}): Response {
  return new Response(
    JSON.stringify({
      token_type: "Bearer",
      access_token: overrides.access_token ?? "mock-access-token-abc123",
      refresh_token: overrides.refresh_token ?? "mock-refresh-token-xyz789",
      expires_in: overrides.expires_in ?? 3600,
      scope: `${CONFIG.instanceUrl}/.default offline_access`,
    }),
    {
      status: 200,
      headers: { "Content-Type": "application/json" },
    },
  );
}

/** Simulate a token endpoint error (e.g. invalid_grant) */
function mockTokenError(status: number, error: string, description: string): Response {
  return new Response(
    JSON.stringify({ error, error_description: description }),
    {
      status,
      headers: { "Content-Type": "application/json" },
    },
  );
}

// ─── getAuthorizationUrl ─────────────────────────────────────────────────────

describe("getAuthorizationUrl", () => {
  it("builds a valid Microsoft Entra ID authorization URL", () => {
    const url = getAuthorizationUrl(CONFIG, REDIRECT_URI, "csrf-state-123");

    expect(url).toContain("https://login.microsoftonline.com/common/oauth2/v2.0/authorize");
    expect(url).toContain(`client_id=${CONFIG.clientId}`);
    expect(url).toContain("response_type=code");
    expect(url).toContain(encodeURIComponent(REDIRECT_URI));
    expect(url).toContain("state=csrf-state-123");
    expect(url).toContain("prompt=select_account");
  });

  it("includes the instance-specific scope (not a generic Dynamics scope)", () => {
    const url = getAuthorizationUrl(CONFIG, REDIRECT_URI, "state");

    // Scope must be derived from instanceUrl per Microsoft docs:
    // https://learn.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth
    // For confidential client: <environment-url>/.default
    const expectedScope = encodeURIComponent(
      `${CONFIG.instanceUrl}/.default offline_access`,
    );
    expect(url).toContain(expectedScope);
  });

  it("uses tenant-specific URL when tenantId is a GUID", () => {
    const config: Dynamics365Config = {
      ...CONFIG,
      tenantId: "ef7a8bd9-3b7a-4e32-b5d4-90ee93ca8450",
    };
    const url = getAuthorizationUrl(config, REDIRECT_URI, "state");

    expect(url).toContain(
      `https://login.microsoftonline.com/${config.tenantId}/oauth2/v2.0/authorize`,
    );
  });

  it("defaults to 'common' tenant when tenantId is empty", () => {
    const config: Dynamics365Config = { ...CONFIG, tenantId: "" };
    const url = getAuthorizationUrl(config, REDIRECT_URI, "state");

    expect(url).toContain("login.microsoftonline.com/common/");
  });
});

// ─── exchangeCodeForTokens ───────────────────────────────────────────────────

describe("exchangeCodeForTokens", () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it("exchanges authorization code for access + refresh tokens", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockTokenResponse());

    const tokens = await exchangeCodeForTokens(CONFIG, "auth-code-xyz", REDIRECT_URI);

    expect(tokens.accessToken).toBe("mock-access-token-abc123");
    expect(tokens.refreshToken).toBe("mock-refresh-token-xyz789");
    expect(tokens.instanceUrl).toBe(CONFIG.instanceUrl);
    expect(tokens.expiresAt).toBeGreaterThan(Date.now());
  });

  it("sends a POST to the correct token endpoint", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockTokenResponse());

    await exchangeCodeForTokens(CONFIG, "auth-code-xyz", REDIRECT_URI);

    const [url, init] = (global.fetch as jest.Mock).mock.calls[0];
    expect(url).toBe(
      "https://login.microsoftonline.com/common/oauth2/v2.0/token",
    );
    expect(init.method).toBe("POST");
    expect(init.headers["Content-Type"]).toBe("application/x-www-form-urlencoded");

    const body = new URLSearchParams(init.body as string);
    expect(body.get("grant_type")).toBe("authorization_code");
    expect(body.get("client_id")).toBe(CONFIG.clientId);
    expect(body.get("client_secret")).toBe(CONFIG.clientSecret);
    expect(body.get("code")).toBe("auth-code-xyz");
    expect(body.get("redirect_uri")).toBe(REDIRECT_URI);
  });

  it("sends instance-specific scope in token request", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockTokenResponse());

    await exchangeCodeForTokens(CONFIG, "code", REDIRECT_URI);

    const [, init] = (global.fetch as jest.Mock).mock.calls[0];
    const body = new URLSearchParams(init.body as string);
    expect(body.get("scope")).toBe(
      `${CONFIG.instanceUrl}/.default offline_access`,
    );
  });

  it("sets expiresAt ~1 hour from now (expires_in = 3600)", async () => {
    const before = Date.now();
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockTokenResponse({ expires_in: 3600 }),
    );

    const tokens = await exchangeCodeForTokens(CONFIG, "code", REDIRECT_URI);
    const after = Date.now();

    expect(tokens.expiresAt).toBeGreaterThanOrEqual(before + 3600 * 1000);
    expect(tokens.expiresAt).toBeLessThanOrEqual(after + 3600 * 1000);
  });

  it("throws on invalid_grant error (expired or already used code)", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockTokenError(400, "invalid_grant", "AADSTS70011: The provided authorization code expired"),
    );

    await expect(
      exchangeCodeForTokens(CONFIG, "expired-code", REDIRECT_URI),
    ).rejects.toThrow("Azure AD token exchange failed: 400");
  });

  it("throws on unauthorized_client error", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockTokenError(401, "unauthorized_client", "Client authentication failed"),
    );

    await expect(
      exchangeCodeForTokens(CONFIG, "code", REDIRECT_URI),
    ).rejects.toThrow("Azure AD token exchange failed: 401");
  });
});

// ─── refreshAccessToken ──────────────────────────────────────────────────────

describe("refreshAccessToken", () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it("exchanges refresh token for new access token", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockTokenResponse({ access_token: "new-access-token", expires_in: 3600 }),
    );

    const tokens = await refreshAccessToken(CONFIG, "old-refresh-token");

    expect(tokens.accessToken).toBe("new-access-token");
    expect(tokens.instanceUrl).toBe(CONFIG.instanceUrl);
  });

  it("sends grant_type=refresh_token to token endpoint", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockTokenResponse());

    await refreshAccessToken(CONFIG, "refresh-token-xyz");

    const [url, init] = (global.fetch as jest.Mock).mock.calls[0];
    expect(url).toContain("/oauth2/v2.0/token");
    const body = new URLSearchParams(init.body as string);
    expect(body.get("grant_type")).toBe("refresh_token");
    expect(body.get("refresh_token")).toBe("refresh-token-xyz");
  });

  it("preserves old refresh token when Microsoft does not rotate it", async () => {
    // Microsoft may omit refresh_token from the response when it is not rotated
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          access_token: "new-access-token",
          expires_in: 3600,
          // no refresh_token field
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );

    const tokens = await refreshAccessToken(CONFIG, "stable-refresh-token");

    expect(tokens.refreshToken).toBe("stable-refresh-token");
  });

  it("uses new refresh token when Microsoft rotates it", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockTokenResponse({ refresh_token: "rotated-refresh-token" }),
    );

    const tokens = await refreshAccessToken(CONFIG, "old-refresh-token");

    expect(tokens.refreshToken).toBe("rotated-refresh-token");
  });

  it("throws on invalid_grant (refresh token expired/revoked)", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockTokenError(400, "invalid_grant", "AADSTS700082: The refresh token has expired"),
    );

    await expect(
      refreshAccessToken(CONFIG, "expired-refresh-token"),
    ).rejects.toThrow("Azure AD token refresh failed: 400");
  });
});

// ─── isTokenExpired ──────────────────────────────────────────────────────────

describe("isTokenExpired", () => {
  const baseTokens: OAuthTokens = {
    accessToken: "token",
    refreshToken: "refresh",
    instanceUrl: CONFIG.instanceUrl,
    expiresAt: 0,
  };

  it("returns true when token is expired", () => {
    const tokens: OAuthTokens = {
      ...baseTokens,
      expiresAt: Date.now() - 1000, // 1s ago
    };
    expect(isTokenExpired(tokens)).toBe(true);
  });

  it("returns true when token expires within the 60s buffer", () => {
    const tokens: OAuthTokens = {
      ...baseTokens,
      expiresAt: Date.now() + 30_000, // expires in 30s — within 60s buffer
    };
    expect(isTokenExpired(tokens)).toBe(true);
  });

  it("returns false when token is valid with margin", () => {
    const tokens: OAuthTokens = {
      ...baseTokens,
      expiresAt: Date.now() + 600_000, // expires in 10min
    };
    expect(isTokenExpired(tokens)).toBe(false);
  });

  it("returns false when token expires exactly at the 60s boundary", () => {
    const tokens: OAuthTokens = {
      ...baseTokens,
      expiresAt: Date.now() + 61_000, // 1s beyond the buffer
    };
    expect(isTokenExpired(tokens)).toBe(false);
  });
});
