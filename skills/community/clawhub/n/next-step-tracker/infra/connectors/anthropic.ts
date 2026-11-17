import { defineConnector } from "@cargo-ai/cdk";

// The model the tracker runs on. Every token a morning run spends is billed
// to this connector and metered against the agent's `languageModel` slug.
//
// `default: true` binds the workspace's existing Anthropic connector — the one
// authenticated once in the UI — rather than creating one, so this pipeline
// deploys with no env var of its own.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
