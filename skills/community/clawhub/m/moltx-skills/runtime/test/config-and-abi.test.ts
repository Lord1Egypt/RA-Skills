import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

test("runtime config uses built-in placeholder contract addresses and only needs rpc override", async () => {
  const tempHome = fs.mkdtempSync(path.join(os.tmpdir(), "moltx-skills-test-"));
  const previousHome = process.env.HOME;
  process.env.HOME = tempHome;

  try {
    const {
      DEFAULT_CORE_ADDRESS,
      DEFAULT_COUNCIL_ADDRESS,
      DEFAULT_PREDICTION_ADDRESS,
      getRuntimeConfig,
      setRuntimeConfig,
    } = await import("../src/tools/config.ts");

    const initial = getRuntimeConfig();
    assert.equal(initial.coreAddress, DEFAULT_CORE_ADDRESS);
    assert.equal(initial.councilAddress, DEFAULT_COUNCIL_ADDRESS);
    assert.equal(initial.predictionAddress, DEFAULT_PREDICTION_ADDRESS);

    const config = setRuntimeConfig({
      rpcUrl: "https://sepolia.base.org",
      walletAddress: "0x4444444444444444444444444444444444444444",
    });

    assert.equal(config.coreAddress, DEFAULT_CORE_ADDRESS);
    assert.equal(config.councilAddress, DEFAULT_COUNCIL_ADDRESS);
    assert.equal(getRuntimeConfig().predictionAddress, DEFAULT_PREDICTION_ADDRESS);
    assert.equal(getRuntimeConfig().walletAddress, "0x4444444444444444444444444444444444444444");
  } finally {
    process.env.HOME = previousHome;
    fs.rmSync(tempHome, { recursive: true, force: true });
  }
});

test("runtime source contracts are synced to core ABIs and old oracle ABI is absent", () => {
  const contractsDir = path.resolve("runtime/src/contracts");
  const names = fs.readdirSync(contractsDir).sort();

  assert.ok(names.includes("MoltXCore.json"));
  assert.ok(names.includes("MoltXCouncil.json"));
  assert.ok(names.includes("MoltXPrediction.json"));
  assert.ok(!names.includes("MoltXOracle.json"));
});
