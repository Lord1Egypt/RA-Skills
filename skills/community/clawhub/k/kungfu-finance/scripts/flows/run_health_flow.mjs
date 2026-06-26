// Health check flow — verifies KUNGFU_OPENKEY configuration and backend connectivity.
// Makes ONE outbound POST to tianshan-api.kungfu-trader.com to verify auth.
// Does NOT read or write any local files. Does NOT exfiltrate data.
import {
  getBaseUrl,
  getEnv,
  getPlatformHeader
} from "../core/runtime.mjs";

function getOpenKeyStatus() {
  const raw = getEnv("KUNGFU_OPENKEY");
  if (!raw || !raw.trim()) {
    return { configured: false, key_preview: null, source: null };
  }
  const trimmed = raw.trim();
  const preview = trimmed.length > 12
    ? `${trimmed.slice(0, 8)}...${trimmed.slice(-4)}`
    : "***";
  return { configured: true, key_preview: preview, source: "env:KUNGFU_OPENKEY" };
}

export async function testApiConnectivity(openkey) {
  const baseUrl = getBaseUrl();
  const testUrl = `${baseUrl}/api/openclaw/keys/test`;
  try {
    const res = await fetch(testUrl, {
      method: "POST",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${openkey}`,
        "x-kungfu-platform": getPlatformHeader()
      },
      signal: AbortSignal.timeout(15000)
    });
    const text = await res.text();
    let body;
    try { body = JSON.parse(text); } catch { body = text; }

    if (res.ok && body?.success) {
      return {
        reachable: true,
        authenticated: true,
        user_id: body.data?.user_id ?? null,
        plan_code: body.data?.plan_code ?? null,
        error: null
      };
    }

    return {
      reachable: true,
      authenticated: false,
      user_id: null,
      plan_code: null,
      error: typeof body === "object" ? (body.detail || body.message || JSON.stringify(body)) : body
    };
  } catch (err) {
    return {
      reachable: false,
      authenticated: false,
      user_id: null,
      plan_code: null,
      error: err.message
    };
  }
}

export async function runHealthFlow() {
  const keyStatus = getOpenKeyStatus();
  const apiBase = getBaseUrl();
  const platform = getPlatformHeader();

  const checks = {
    api_base: apiBase,
    platform,
    openkey: keyStatus,
    api_test: null
  };

  if (keyStatus.configured) {
    const openkey = getEnv("KUNGFU_OPENKEY").trim();
    checks.api_test = await testApiConnectivity(openkey);
  } else {
    checks.api_test = {
      reachable: false,
      authenticated: false,
      error: "KUNGFU_OPENKEY not configured — skipped API test"
    };
  }

  const allOk = keyStatus.configured
    && checks.api_test.reachable
    && checks.api_test.authenticated;

  return {
    healthy: allOk,
    checks
  };
}
