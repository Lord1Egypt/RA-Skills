import { defineFolder } from "@cargo-ai/cdk";

// Every resource this cookbook deploys is filed under a folder named after the
// cookbook, not under a shared "GTM" one. That is provenance: six months later
// the question about an agent nobody recognises is "what put this here", and a
// folder per cookbook answers it by looking.
//
// It is also how this agent tells what else is installed. Every cookbook files
// its resources under a folder named after itself, so a folder called
// "Account scoring" in the workspace is the strongest sign account-scoring is
// already there.
export const agentsFolder = defineFolder("goal_coverage_agents", {
  kind: "agent",
  name: "Goal coverage",
});
