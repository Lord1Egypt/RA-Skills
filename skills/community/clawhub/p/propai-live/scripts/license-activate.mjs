#!/usr/bin/env node
import {
  PRODUCT_SLUG,
  getExitCode,
  maskLicenseKey,
  normalizeActivationPayload,
  normalizeApiBaseUrl,
  parseArgs,
  postJson,
  printError,
  printJson,
  resolveMachineId,
  resolveStateFilePath,
  saveState,
  safeApiError,
  toIsoNow,
} from "./license-lib.mjs";

function getArg(args, names, fallback = "") {
  for (const name of names) {
    if (args[name] != null && args[name] !== true) {
      return String(args[name]);
    }
  }
  return fallback;
}

function printHelp() {
  process.stdout.write(
    [
      "Activate a PropAI Live license and cache it locally.",
      "",
      "Usage:",
      "  node scripts/license-activate.mjs --key <license-key> --api <https://license-api>",
      "",
      "Options:",
      "  --key <value>             License key (required)",
      "  --api <url>               License API base URL (or PROPAI_LIVE_LICENSE_API_URL)",
      "  --machine-id <value>      Override machine fingerprint",
      "  --state-dir <path>        Override local state directory",
      "  --client-version <value>  Client version marker",
      "  --timeout-ms <value>      Request timeout in milliseconds",
      "  --help                    Show this help text",
      "",
    ].join("\n"),
  );
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const licenseKey = getArg(args, ["key"]);
  if (!licenseKey) {
    printError("Missing --key.");
    process.exit(getExitCode("missing"));
  }

  const apiBaseUrl = normalizeApiBaseUrl(
    getArg(args, ["api"], process.env.PROPAI_LIVE_LICENSE_API_URL || ""),
  );
  if (!apiBaseUrl) {
    printError("Missing --api (or PROPAI_LIVE_LICENSE_API_URL).");
    process.exit(getExitCode("missing"));
  }

  const machineId = resolveMachineId(getArg(args, ["machine-id"], process.env.PROPAI_LIVE_MACHINE_ID));
  const stateFile = resolveStateFilePath(getArg(args, ["state-dir"]));
  const timeoutMs = Number(getArg(args, ["timeout-ms"], "10000"));
  const activationUrl = `${apiBaseUrl}/v1/licenses/activate`;

  const payload = {
    key: licenseKey,
    product: PRODUCT_SLUG,
    machineId,
    clientVersion: getArg(args, ["client-version"], "1.0.0"),
    runtime: `node-${process.version}`,
  };

  const result = await postJson(activationUrl, payload, Number.isFinite(timeoutMs) ? timeoutMs : 10000);
  if (!result.ok) {
    printError("License activation failed.", safeApiError(result));
    process.exit(getExitCode("network"));
  }

  const normalized = normalizeActivationPayload(result.data || {});
  if (!normalized.licenseToken) {
    printError("License activation response is missing token.");
    process.exit(getExitCode("bad_state"));
  }

  const nowIso = toIsoNow();
  const state = {
    product: PRODUCT_SLUG,
    apiBaseUrl,
    machineId,
    licenseToken: normalized.licenseToken,
    licenseId: normalized.licenseId,
    licenseKeyMask: maskLicenseKey(licenseKey),
    status: normalized.status,
    plan: normalized.plan,
    entitlements: normalized.entitlements,
    expiresAt: normalized.expiresAt,
    activatedAt: nowIso,
    lastValidatedAt: nowIso,
    offlineGraceUntil: normalized.offlineGraceUntil,
    nextRemoteCheckAt: normalized.nextRemoteCheckAt,
  };

  await saveState(stateFile, state);
  printJson({
    ok: true,
    status: state.status,
    plan: state.plan,
    license_id: state.licenseId || null,
    license_key: state.licenseKeyMask,
    entitlements: state.entitlements,
    expires_at: state.expiresAt || null,
    offline_grace_until: state.offlineGraceUntil || null,
    next_remote_check_at: state.nextRemoteCheckAt || null,
    state_file: stateFile,
  });
}

main().catch((error) => {
  printError("Unexpected activation failure.", error?.message || String(error));
  process.exit(getExitCode("unknown"));
});

