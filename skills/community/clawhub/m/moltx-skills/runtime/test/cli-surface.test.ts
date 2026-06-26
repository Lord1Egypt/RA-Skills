import test from "node:test";
import assert from "node:assert/strict";

test("cli lists rebuilt runtime commands and excludes removed legacy commands", async () => {
  const [{ coreTools }, { apiTools }, { predictionTools }, { councilTools }, { eventTools }, { agentSyncTools }, { agentQueryTools }, { hashTools }, { walletTools }] =
    await Promise.all([
      import("../src/tools/core.ts"),
      import("../src/tools/api.ts"),
      import("../src/tools/prediction.ts"),
      import("../src/tools/council.ts"),
      import("../src/tools/events.ts"),
      import("../src/tools/agent-sync.ts"),
      import("../src/tools/agent-query.ts"),
      import("../src/tools/hash.ts"),
      import("../src/tools/wallet.ts"),
    ]);

  const tools = Object.keys({
    ...coreTools,
    ...apiTools,
    ...predictionTools,
    ...councilTools,
    ...eventTools,
    ...agentSyncTools,
    ...agentQueryTools,
    ...hashTools,
    ...walletTools,
  });

  for (const requiredTool of [
    "claim_funds",
    "claim_moltx",
    "confirm_submission",
    "reclaim_bounty",
    "create_prediction_task",
    "accept_prediction_task",
    "claim_prediction_reward",
    "commit_vote",
    "reveal_vote",
    "finalize_commit",
    "finalize_reveal",
    "list_active_tasks",
    "get_task_details",
    "list_disputes",
    "sync_task_to_api",
    "sync_dispute_to_api",
    "hash_requirement_json",
    "verify_task_requirement",
  ]) {
    assert.ok(tools.includes(requiredTool), `missing tool: ${requiredTool}`);
  }

  for (const removedTool of [
    "release_reward",
    "claim_reward",
    "expire_task",
    "prediction_place_bet",
    "prediction_claim_reward",
    "prediction_trigger_rollover",
  ]) {
    assert.ok(!tools.includes(removedTool), `legacy tool still exposed: ${removedTool}`);
  }
});
