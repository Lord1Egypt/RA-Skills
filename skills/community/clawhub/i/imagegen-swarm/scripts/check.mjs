#!/usr/bin/env node
import { ENGINES, PY, probeEngine, readSmokeCache, readinessState, run } from "./readiness.mjs";
import { smokeMain } from "./smoke.mjs";

async function main(args) {
  if (args[0] === "--live") return smokeMain(args.slice(1));
  if (args.length) throw new Error("Usage: node check.mjs [--live [smoke options]]");
  console.log("imagegen-swarm readiness check");
  const pillow = await run(PY, ["-c", "import PIL; print(PIL.__version__)"]);
  console.log(pillow.code === 0 ? "Pillow " + pillow.stdout.trim() : "Pillow missing. Run " + PY + " -m pip install pillow.");

  const latest = await readSmokeCache();
  const states = {};
  for (const engine of ENGINES) {
    const probe = await probeEngine(engine);
    const details = [probe.reason];
    if (probe.budget) details.push(probe.budget);
    if (probe.remoteDir) details.push("remote_dir=" + probe.remoteDir);
    if (probe.billingMode) {
      details.push("billing mode " + probe.billingMode + (probe.free ? " (免费可用)" : " (会扣积分)"));
    }
    console.log(engine + " — " + details.join(" "));
    states[engine] = readinessState(probe.loggedIn, latest[engine]);
  }
  console.log("\nReadiness by engine");
  for (const engine of ENGINES) console.log(engine.padEnd(7) + " " + states[engine]);
  return pillow.code !== 0 || Object.values(states).every(state => state.startsWith("NOT READY")) ? 1 : 0;
}

main(process.argv.slice(2)).then(code => { process.exitCode = code; }).catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
