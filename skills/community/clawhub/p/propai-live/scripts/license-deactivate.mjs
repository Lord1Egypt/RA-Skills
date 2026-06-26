#!/usr/bin/env node
import {
  clearState,
  getExitCode,
  loadState,
  normalizeApiBaseUrl,
  parseArgs,
  postJson,
  printError,
  printJson,
  resolveMachineId,
  resolveStateFilePath,
  safeApiError,
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
      "Deactivate local PropAI Live license and clear local state.",
      "",
      "Usage:",
      "  node scripts/license-deactivate.mjs [--api <https://license-api>]",
      "",
      "Options:",
      "  --api <url>            Override API base URL",
      "  --state-dir <path>     Override local state directory",
      "  --machine-id <value>   Override machine fingerprint",
      "  --timeout-ms <value>   Request timeout in milliseconds",
      "  --skip-remote          Skip API deactivation call",
      "  --help                 Show this help text",
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

  const stateFile = resolveStateFilePath(getArg(args, ["state-dir"]));
  const timeoutMs = Number(getArg(args, ["timeout-ms"], "10000"));
  const state = await loadState(stateFile);
  if (!state) {
    printJson({
      ok: true,
      message: "No local license state found; nothing to deactivate.",
      state_file: stateFile,
    });
    process.exit(getExitCode("ok"));
  }

  const apiBaseUrl = normalizeApiBaseUrl(
    getArg(args, ["api"], state.apiBaseUrl || process.env.PROPAI_LIVE_LICENSE_API_URL || ""),
  );
  const skipRemote = Boolean(args["skip-remote"]);

  if (!skipRemote && apiBaseUrl) {
    const payload = {
      product: state.product || "propai-live",
      machineId: resolveMachineId(getArg(args, ["machine-id"], state.machineId || process.env.PROPAI_LIVE_MACHINE_ID)),
      licenseToken: state.licenseToken,
      licenseId: state.licenseId,
    };
    const result = await postJson(
      `${apiBaseUrl}/v1/licenses/deactivate`,
      payload,
      Number.isFinite(timeoutMs) ? timeoutMs : 10000,
    );
    if (!result.ok) {
      printError(
        "Remote deactivation failed. Use --skip-remote to clear local state anyway.",
        safeApiError(result),
      );
      process.exit(getExitCode("network"));
    }
  }

  await clearState(stateFile);
  printJson({
    ok: true,
    deactivated: true,
    remote_called: !skipRemote && Boolean(apiBaseUrl),
    state_file: stateFile,
  });
}

main().catch((error) => {
  printError("Unexpected deactivation failure.", error?.message || String(error));
  process.exit(getExitCode("unknown"));
});

