// Local governance + OpenClaw gateway mode (no external LLM provider).
import { createLoopSystem, parseLoopYaml } from "@loop-engine/sdk";
import { OpenClawEventBus } from "@loop-engine/adapter-openclaw";
// This example demonstrates @loop-engine/adapter-openclaw directly.
// The other examples show generic Loop Engine patterns that work
// alongside OpenClaw — this one shows the adapter-specific integration.
const loop = parseLoopYaml(`
loopId: openclaw.change.approval
version: "1.0.0"
name: OpenClaw Change Approval
initialState: requested
states:
  - { stateId: requested, label: Requested }
  - { stateId: pending_approval, label: Pending Approval }
  - { stateId: completed, label: Completed, terminal: true }
transitions:
  - { transitionId: submit_change, from: requested, to: pending_approval, signal: submit_change, allowedActors: [automation] }
  - { transitionId: approve, from: pending_approval, to: completed, signal: approve, allowedActors: [human] }
`);
async function main() {
  const { engine, eventBus } = await createLoopSystem({ loops: [loop] });
  const openclawBus = new OpenClawEventBus({ channel: "ops-approvals", target: "openclaw://channel/sre", approvalStates: ["pending_approval"], events: ["loop.transition.executed", "loop.completed"] });
  const unsubscribe = eventBus.subscribe(async (event) => openclawBus.emit(event));
  await engine.startLoop({ loopId: "openclaw.change.approval" as never, aggregateId: "CHG-1001" as never, actor: { type: "automation", id: "deploy-bot" as never } });
  await engine.transition({ aggregateId: "CHG-1001" as never, transitionId: "submit_change" as never, actor: { type: "automation", id: "deploy-bot" as never } });
  await engine.transition({ aggregateId: "CHG-1001" as never, transitionId: "approve" as never, actor: { type: "human", id: "sre-oncall" as never } });
  unsubscribe();
  openclawBus.disconnect();
}
main().catch(console.error);
