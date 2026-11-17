import { defineFolder } from "@cargo-ai/cdk";

// Every resource this skill deploys is filed under folders named after the
// skill, not under a shared "GTM" one. A workspace accumulates resources from
// several skills plus whatever the team wrote by hand, and the folder is what
// answers "what put this here, and what else came with it" by looking. It is
// also what makes removing a skill bounded rather than a hunt.
//
// Folders are per-kind, which is why there are three: this skill deploys a
// model, an agent and a play, and each kind is filed separately.
export const modelsFolder = defineFolder("new_hire_detection_models", {
  kind: "model",
  name: "New-hire detection",
});

export const agentsFolder = defineFolder("new_hire_detection_agents", {
  kind: "agent",
  name: "New-hire detection",
});

export const playsFolder = defineFolder("new_hire_detection_plays", {
  kind: "play",
  name: "New-hire detection",
});
