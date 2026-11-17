import { defineFolder } from "@cargo-ai/cdk";

// One folder per pipeline, so "what put this agent here, and what came with
// it" is answered by looking, and removing the pipeline is a bounded job.
export const agentsFolder = defineFolder("next_step_tracker_agents", {
  kind: "agent",
  name: "Next-step tracker",
});

export const modelsFolder = defineFolder("next_step_tracker_models", {
  kind: "model",
  name: "Next-step tracker",
});
