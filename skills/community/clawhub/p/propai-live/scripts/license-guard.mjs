#!/usr/bin/env node
import {
  evaluateState,
  getExitCode,
  loadState,
  mergeValidationIntoState,
  normalizeApiBaseUrl,
  parseArgs,
  postJson,
  printError,
  printJson,
  resolveMachineId,
  resolveStateFilePath,
  safeApiError,
  saveState,
  shouldRunRemoteValidation,
  toIsoNow,
  withinOfflineGrace,
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
      "Enforce PropAI Live license before execution.",
      "",
      "Usage:",
      "  node scripts/license-guard.mjs --mode read|write [--require-entitlement <name>]",
      "",
      "Options:",
      "  --mode <read|write>         Guard mode (default: read)",
      "  --require-entitlement <id>  Require a specific entitlement",
      "  --api <url>                 Override API base URL",
      "  --force-remote              Force remote validation now",
      "  --state-dir <path>          Override local state directory",
      "  --machine-id <value>        Override machine fingerprint",
      "  --timeout-ms <value>        Request timeout in milliseconds",
      "  --help                      Show this help text",
      "",
    ].join("\n"),
  );
}

function fail(reason, message, detail) {
  printError(message, detail);
  process.exit(getExitCode(reason));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const mode = getArg(args, ["mode"], "read").toLowerCase() === "write" ? "write" : "read";
  const requiredEntitlement = getArg(args, ["require-entitlement"]);
  const stateFile = resolveStateFilePath(getArg(args, ["state-dir"]));
  const timeoutMs = Number(getArg(args, ["timeout-ms"], "10000"));
  const forceRemote = Boolean(args["force-remote"]);

  let state = await loadState(stateFile);
  if (!state) {
    fail(
      "missing",
      "No local license state found.",
      "Activate first with scripts/license-activate.mjs.",
    );
  }

  const localCheck = evaluateState(state, mode, requiredEntitlement);
  if (!localCheck.ok) {
    fail(localCheck.reason, "Local license check failed.", localCheck.message);
  }

  const nowMs = Date.now();
  const apiBaseUrl = normalizeApiBaseUrl(
    getArg(args, ["api"], state.apiBaseUrl || process.env.PROPAI_LIVE_LICENSE_API_URL || ""),
  );
  const runRemoteValidation = forceRemote || shouldRunRemoteValidation(state, nowMs);
  let remoteStatus = "skipped";
  let warning = "";

  if (runRemoteValidation && apiBaseUrl) {
    const machineId = resolveMachineId(getArg(args, ["machine-id"], state.machineId || process.env.PROPAI_LIVE_MACHINE_ID));
    const validateUrl = `${apiBaseUrl}/v1/licenses/validate`;
    const payload = {
      product: state.product || "propai-live",
      machineId,
      licenseToken: state.licenseToken,
      licenseId: state.licenseId,
    };

    try {
      const response = await postJson(
        validateUrl,
        payload,
        Number.isFinite(timeoutMs) ? timeoutMs : 10000,
      );
      if (response.ok) {
        const body = response.data || {};
        if (body.valid === false || String(body.status || "").toLowerCase() === "revoked") {
          fail("invalid_status", "Remote license check rejected license.", safeApiError(response));
        }
        state = mergeValidationIntoState(
          {
            ...state,
            apiBaseUrl,
            machineId,
          },
          body,
        );
        await saveState(stateFile, state);
        remoteStatus = "validated";
      } else {
        if (withinOfflineGrace(state, nowMs)) {
          remoteStatus = "degraded";
          warning = `Remote validation failed (${safeApiError(response)}), running within offline grace window.`;
        } else {
          fail("network", "Remote license validation failed and offline grace is exhausted.", safeApiError(response));
        }
      }
    } catch (error) {
      if (withinOfflineGrace(state, nowMs)) {
        remoteStatus = "degraded";
        warning = `Remote validation error (${error?.message || String(error)}), running within offline grace window.`;
      } else {
        fail(
          "network",
          "Remote license validation error and offline grace is exhausted.",
          error?.message || String(error),
        );
      }
    }
  }

  const finalCheck = evaluateState(state, mode, requiredEntitlement);
  if (!finalCheck.ok) {
    fail(finalCheck.reason, "License guard failed.", finalCheck.message);
  }

  printJson({
    ok: true,
    checked_at: toIsoNow(),
    mode,
    required_entitlement: requiredEntitlement || null,
    remote_status: remoteStatus,
    status: state.status || null,
    plan: state.plan || null,
    license_id: state.licenseId || null,
    expires_at: state.expiresAt || null,
    entitlements: Array.isArray(state.entitlements) ? state.entitlements : [],
    state_file: stateFile,
    warning: warning || null,
  });
}

main().catch((error) => {
  printError("Unexpected guard failure.", error?.message || String(error));
  process.exit(getExitCode("unknown"));
});

