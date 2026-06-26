#!/usr/bin/env node
import {
  evaluateState,
  getExitCode,
  loadState,
  parseArgs,
  printError,
  printJson,
  resolveStateFilePath,
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
      "Show local PropAI Live license status.",
      "",
      "Usage:",
      "  node scripts/license-status.mjs [--mode read|write] [--require-entitlement <name>]",
      "",
      "Options:",
      "  --mode <read|write>         Validate read or write access (default: read)",
      "  --require-entitlement <id>  Require a specific entitlement",
      "  --state-dir <path>          Override local state directory",
      "  --help                      Show this help text",
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

  const mode = getArg(args, ["mode"], "read").toLowerCase() === "write" ? "write" : "read";
  const requiredEntitlement = getArg(args, ["require-entitlement"]);
  const stateFile = resolveStateFilePath(getArg(args, ["state-dir"]));
  const state = await loadState(stateFile);

  if (!state) {
    printError("No local license state found.", `Activate first with scripts/license-activate.mjs (state file: ${stateFile})`);
    process.exit(getExitCode("missing"));
  }

  const localCheck = evaluateState(state, mode, requiredEntitlement);
  const nowMs = Date.now();
  const remoteDue = shouldRunRemoteValidation(state, nowMs);
  const graceActive = withinOfflineGrace(state, nowMs);

  const output = {
    ok: localCheck.ok,
    checked_at: toIsoNow(),
    mode,
    required_entitlement: requiredEntitlement || null,
    status: state.status || null,
    plan: state.plan || null,
    license_id: state.licenseId || null,
    license_key: state.licenseKeyMask || null,
    expires_at: state.expiresAt || null,
    offline_grace_until: state.offlineGraceUntil || null,
    next_remote_check_at: state.nextRemoteCheckAt || null,
    remote_validation_due: remoteDue,
    offline_grace_active: graceActive,
    entitlements: Array.isArray(state.entitlements) ? state.entitlements : [],
    state_file: stateFile,
    detail: localCheck.message,
  };

  printJson(output);
  process.exit(getExitCode(localCheck.reason));
}

main().catch((error) => {
  printError("Unexpected status failure.", error?.message || String(error));
  process.exit(getExitCode("unknown"));
});

