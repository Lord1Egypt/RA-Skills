/**
 * RFC 8628 Device Authorization Grant + token refresh.
 *
 * Flow:
 * 1. POST /oauth/register → get client_id (one-time, persisted with tokens)
 * 2. POST /oauth/device_authorization → get device_code + user_code
 * 3. Print verification URL for user
 * 4. Poll POST /oauth/token until approved
 * 5. On token expiry, use refresh_token to get new access_token
 */

import { type StoredTokens, isExpired, loadTokens, saveTokens } from "./token-store.js";

const DEVICE_CODE_GRANT = "urn:ietf:params:oauth:grant-type:device_code";

interface DeviceAuthResponse {
  device_code: string;
  user_code: string;
  verification_uri: string;
  verification_uri_complete: string;
  expires_in: number;
  interval: number;
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  scope: string;
}

interface Logger {
  info: (...args: unknown[]) => void;
  warn: (...args: unknown[]) => void;
  error: (...args: unknown[]) => void;
}

export class OttoAuth {
  private tokens: StoredTokens | null = null;
  private refreshing: Promise<string> | null = null;

  constructor(
    private serverUrl: string,
    private logger: Logger,
  ) {}

  /** Base URL without trailing /mcp/ path */
  private get baseUrl(): string {
    return this.serverUrl.replace(/\/mcp\/?$/, "");
  }

  /**
   * Get a valid access token. Loads from disk, refreshes if expired,
   * or runs the full device auth flow if no tokens exist.
   */
  async getAccessToken(): Promise<string> {
    if (!this.tokens) {
      this.tokens = await loadTokens(this.serverUrl);
    }

    if (this.tokens && !isExpired(this.tokens)) {
      return this.tokens.access_token;
    }

    if (this.tokens?.refresh_token) {
      return this.refresh();
    }

    return this.deviceAuthFlow();
  }

  /** Refresh using stored refresh_token. Deduplicates concurrent calls. */
  private async refresh(): Promise<string> {
    if (this.refreshing) return this.refreshing;

    this.refreshing = (async () => {
      try {
        const params = new URLSearchParams({
          grant_type: "refresh_token",
          refresh_token: this.tokens!.refresh_token,
          client_id: this.tokens!.client_id,
        });

        const res = await fetch(`${this.baseUrl}/oauth/token`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: params.toString(),
        });

        if (!res.ok) {
          this.logger.warn("[otto] Refresh failed, starting device auth flow");
          this.tokens = null;
          return this.deviceAuthFlow();
        }

        const data: TokenResponse = await res.json();
        await this.persistTokens(data, this.tokens!.client_id);
        return data.access_token;
      } finally {
        this.refreshing = null;
      }
    })();

    return this.refreshing;
  }

  /** Full device authorization flow — registers client, gets code, polls. */
  private async deviceAuthFlow(): Promise<string> {
    const clientId = await this.registerClient();
    const device = await this.requestDeviceCode(clientId);

    this.logger.info(
      `\n` +
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n` +
        `  Otto Travel — Device Authorization\n` +
        `\n` +
        `  Visit: ${device.verification_uri_complete}\n` +
        `\n` +
        `  Or go to: ${device.verification_uri}\n` +
        `  Enter code: ${device.user_code}\n` +
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`,
    );

    const tokenData = await this.pollForToken(device, clientId);
    await this.persistTokens(tokenData, clientId);
    return tokenData.access_token;
  }

  /** Register an OAuth client via DCR. One-time per server. */
  private async registerClient(): Promise<string> {
    const res = await fetch(`${this.baseUrl}/oauth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_name: "openclaw-otto-travel",
        redirect_uris: ["http://localhost"],
        grant_types: [DEVICE_CODE_GRANT],
      }),
    });

    if (!res.ok) {
      throw new Error(`[otto] Client registration failed: ${res.status}`);
    }

    const data = await res.json();
    return data.client_id;
  }

  /** Request a device code. */
  private async requestDeviceCode(clientId: string): Promise<DeviceAuthResponse> {
    const params = new URLSearchParams({ client_id: clientId });
    const res = await fetch(`${this.baseUrl}/oauth/device_authorization`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
    });

    if (!res.ok) {
      throw new Error(`[otto] Device authorization request failed: ${res.status}`);
    }

    return res.json();
  }

  /** Poll token endpoint until user approves or code expires. */
  private async pollForToken(device: DeviceAuthResponse, clientId: string): Promise<TokenResponse> {
    const deadline = Date.now() + device.expires_in * 1000;
    let interval = device.interval * 1000;

    while (Date.now() < deadline) {
      await sleep(interval);

      const params = new URLSearchParams({
        grant_type: DEVICE_CODE_GRANT,
        device_code: device.device_code,
        client_id: clientId,
      });

      const res = await fetch(`${this.baseUrl}/oauth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params.toString(),
      });

      if (res.ok) {
        return res.json();
      }

      const body = await res.json();
      switch (body.error) {
        case "authorization_pending":
          continue;
        case "slow_down":
          interval += 5000;
          continue;
        case "access_denied":
          throw new Error("[otto] User denied authorization");
        case "expired_token":
          throw new Error("[otto] Device code expired — please try again");
        default:
          throw new Error(`[otto] Token exchange failed: ${body.error}`);
      }
    }

    throw new Error("[otto] Device code expired — user did not authorize in time");
  }

  private async persistTokens(data: TokenResponse, clientId: string): Promise<void> {
    this.tokens = {
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      expires_at: Math.floor(Date.now() / 1000) + data.expires_in,
      scope: data.scope,
      client_id: clientId,
      server_url: this.serverUrl,
    };
    await saveTokens(this.tokens);
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
