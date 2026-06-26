/**
 * Zulip health check probe — uses GET /server_settings (no auth required).
 */

import { ZulipClient } from "./client.js";
import type { ZulipProbe, ZulipClientConfig } from "./types.js";

export async function probeZulip(config: ZulipClientConfig): Promise<ZulipProbe> {
  const client = new ZulipClient(config);
  const start = Date.now();

  try {
    const settings = await client.getServerSettings();
    const latencyMs = Date.now() - start;

    return {
      ok: true,
      realm: config.realm,
      version: settings.zulip_version,
      featureLevel: settings.zulip_feature_level,
      latencyMs,
    };
  } catch (err) {
    return {
      ok: false,
      error: `Zulip probe failed: ${err instanceof Error ? err.message : String(err)}`,
      realm: config.realm,
      version: "unknown",
      featureLevel: 0,
    };
  }
}
