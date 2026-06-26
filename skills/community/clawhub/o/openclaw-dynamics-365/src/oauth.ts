/**
 * openclaw-dynamics-365 — Azure AD OAuth 2.0 helpers
 *
 * Microsoft Dynamics 365 uses Microsoft Entra ID (Azure AD) for authentication.
 * This module implements the Authorization Code Flow with PKCE-compatible
 * redirect for server-side OAuth integrations.
 *
 * Docs: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth
 */

import type { Dynamics365Config, OAuthTokens } from "./types.js";

const AUTHORITY_BASE = "https://login.microsoftonline.com";

/**
 * Build the OAuth 2.0 scope for a given Dynamics 365 instance.
 * The resource URI is derived from the instance URL (org-specific).
 */
function buildScope(instanceUrl: string): string {
  const origin = instanceUrl.replace(/\/$/, "");
  return `${origin}/.default offline_access`;
}

/**
 * Build the Microsoft Entra ID authorization URL.
 * Redirect the user's browser to this URL to start the OAuth flow.
 *
 * @param config   App Registration credentials
 * @param redirectUri  Must match a registered Redirect URI in Azure Portal
 * @param state    CSRF token — verify on callback
 */
export function getAuthorizationUrl(
  config: Dynamics365Config,
  redirectUri: string,
  state: string,
): string {
  const tenant = config.tenantId || "common";
  const scope = buildScope(config.instanceUrl);

  const params = new URLSearchParams({
    client_id: config.clientId,
    response_type: "code",
    redirect_uri: redirectUri,
    scope,
    state,
    prompt: "select_account",
  });

  return `${AUTHORITY_BASE}/${tenant}/oauth2/v2.0/authorize?${params}`;
}

/**
 * Exchange an authorization code for access + refresh tokens.
 * Call this in the OAuth callback handler after the user is redirected back.
 *
 * @throws Error with status details if the request fails
 */
export async function exchangeCodeForTokens(
  config: Dynamics365Config,
  code: string,
  redirectUri: string,
): Promise<OAuthTokens> {
  const tenant = config.tenantId || "common";
  const scope = buildScope(config.instanceUrl);

  const resp = await fetch(
    `${AUTHORITY_BASE}/${tenant}/oauth2/v2.0/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: config.clientId,
        client_secret: config.clientSecret,
        grant_type: "authorization_code",
        code,
        redirect_uri: redirectUri,
        scope,
      }),
    },
  );

  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`Azure AD token exchange failed: ${resp.status} ${body}`);
  }

  const data = (await resp.json()) as {
    access_token: string;
    refresh_token: string;
    expires_in: number;
  };

  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
    expiresAt: Date.now() + data.expires_in * 1000,
    instanceUrl: config.instanceUrl,
  };
}

/**
 * Refresh an expired access token using a stored refresh token.
 * Dynamics 365 access tokens expire after ~1 hour.
 * Refresh tokens are long-lived but can be invalidated by policy changes.
 *
 * @throws Error if the refresh fails (user must re-authorize)
 */
export async function refreshAccessToken(
  config: Dynamics365Config,
  refreshToken: string,
): Promise<OAuthTokens> {
  const tenant = config.tenantId || "common";
  const scope = buildScope(config.instanceUrl);

  const resp = await fetch(
    `${AUTHORITY_BASE}/${tenant}/oauth2/v2.0/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: config.clientId,
        client_secret: config.clientSecret,
        grant_type: "refresh_token",
        refresh_token: refreshToken,
        scope,
      }),
    },
  );

  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`Azure AD token refresh failed: ${resp.status} ${body}`);
  }

  const data = (await resp.json()) as {
    access_token: string;
    refresh_token?: string;
    expires_in: number;
  };

  return {
    accessToken: data.access_token,
    // Microsoft may or may not rotate the refresh token
    refreshToken: data.refresh_token ?? refreshToken,
    expiresAt: Date.now() + data.expires_in * 1000,
    instanceUrl: config.instanceUrl,
  };
}

/**
 * Check whether a stored access token is expired (with a 60s buffer).
 */
export function isTokenExpired(tokens: OAuthTokens): boolean {
  return Date.now() >= tokens.expiresAt - 60_000;
}
