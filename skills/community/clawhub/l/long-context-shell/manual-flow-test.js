const {
  long_context_shell_run,
  long_context_shell_peek,
  long_context_shell_scan,
  long_context_shell_stop
} = require("./handler");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForStatus(sessionId, statuses, timeoutMs = 6000) {
  const expected = new Set(statuses);
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    const card = await long_context_shell_peek({ sessionId, tailLines: 12 });
    if (expected.has(card.status)) {
      return card;
    }
    await sleep(120);
  }

  return long_context_shell_peek({ sessionId, tailLines: 12 });
}

function printSection(title) {
  console.log(`\n===== ${title} =====`);
}

function printCard(label, value) {
  console.log(`\n[${label}]`);
  console.log(JSON.stringify(value, null, 2));
}

async function runFailureFlow() {
  printSection("Scenario 1: Failed Command Analysis");
  const runCard = await long_context_shell_run({
    command: `node -e "console.log('booting service'); setTimeout(() => console.log('connecting database'), 80); setTimeout(() => console.error('warning: retry 1'), 160); setTimeout(() => console.error('fatal: database unavailable'), 260); setTimeout(() => process.exit(2), 320)"`,
    waitMs: 120
  });
  printCard("run result", runCard);

  const settled = await waitForStatus(runCard.sessionId, ["failed"]);
  printCard("final peek", settled);

  const scan = await long_context_shell_scan({
    sessionId: runCard.sessionId,
    limit: 5,
    contextLines: 1
  });
  printCard("scan result", scan);

  const timeQuery = settled.startedAt ? settled.startedAt.slice(0, 16) : null;
  if (timeQuery) {
    const peekByTime = await long_context_shell_peek({
      sessionId: runCard.sessionId,
      timeQuery,
      tailLines: 8
    });
    printCard(`timeQuery=${timeQuery}`, peekByTime);
  }
}

async function runBackgroundFlow() {
  printSection("Scenario 2: Continuous Output Monitoring");
  const runCard = await long_context_shell_run({
    command: `node -e "let count = 0; setInterval(() => console.log('heartbeat-' + (++count)), 150)"`,
    background: true,
    waitMs: 100
  });
  printCard("run result", runCard);

  await sleep(700);
  const peekCard = await long_context_shell_peek({
    sessionId: runCard.sessionId,
    tailLines: 8
  });
  printCard("peek while running", peekCard);

  const stopCard = await long_context_shell_stop({ sessionId: runCard.sessionId });
  printCard("stop result", stopCard);

  const finalCard = await waitForStatus(runCard.sessionId, ["stopped"]);
  printCard("final status after stop", finalCard);
}

async function main() {
  printSection("manual-flow-test");
  console.log("This script does not assert results. It runs two real scenarios and prints structured run / peek / scan / stop output.");
  console.log("Review the output manually or with an LLM, focusing on status, exitCode, preview, severityCounts, and recommendation.");

  await runFailureFlow();
  await runBackgroundFlow();

  printSection("What To Check");
  console.log("- The failure scenario should end with status=failed, a non-zero exitCode, and a fatal match in scan output.");
  console.log("- The continuous-output scenario should start as running, show heartbeat lines in peek output, and become stopped after stop.");
  console.log("- If behavior looks wrong, inspect the logPath file and continue debugging with the Debug Tips in SKILL.md.");
}

main().catch(error => {
  console.error("\n===== manual-flow-test failed =====");
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
