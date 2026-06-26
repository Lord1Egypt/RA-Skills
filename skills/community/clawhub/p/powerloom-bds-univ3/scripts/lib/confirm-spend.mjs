/**
 * Gate on-chain spends behind explicit human/agent acknowledgment.
 *
 * - Interactive (stdin + stdout are TTY): print summary, require typing CONFIRM.
 * - Non-interactive: require argv --yes/-y OR envVar set to yes|1|true (case-insensitive).
 *
 * Matches patterns ClawScan / auditors expect: no silent broadcast after quote fetch.
 */

import readline from "readline";

function truthyEnv(val) {
  const v = String(val ?? "").trim().toLowerCase();
  return v === "yes" || v === "1" || v === "true";
}

export function argvHasYesFlag() {
  return process.argv.includes("--yes") || process.argv.includes("-y");
}

export async function confirmSpendBeforeBroadcast({
  scriptTag,
  envConfirmVar,
  summaryLines,
}) {
  if (argvHasYesFlag() || truthyEnv(process.env[envConfirmVar])) {
    return;
  }

  const ttyIn = process.stdin.isTTY;
  const ttyOut = process.stdout.isTTY;

  for (const line of summaryLines) {
    console.error(line);
  }

  if (!ttyIn || !ttyOut) {
    console.error(
      `[${scriptTag}] Refusing to broadcast without explicit confirmation (non-interactive shell).`,
    );
    console.error(
      `  Inspect the quote details above, then either:` +
        ` (a) re-run with --yes (preferred for OpenClaw: ephemeral argv, do not persist in skill env), or (b) set ${envConfirmVar}=yes for a single CI invocation only`,
    );
    console.error(
      `  Autonomous agents (OpenClaw, CI) should only set ${envConfirmVar}=yes after the operator verified recipient, token, chain, and amount.`,
    );
    process.exit(1);
  }

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const answer = await new Promise((resolve) => {
    rl.question(
      `[${scriptTag}] Irreversible on-chain payment will be broadcast. Type CONFIRM to proceed: `,
      resolve,
    );
  });
  rl.close();

  if (String(answer).trim() !== "CONFIRM") {
    console.error(`[${scriptTag}] Aborted — confirmation text did not match CONFIRM.`);
    process.exit(1);
  }
}
