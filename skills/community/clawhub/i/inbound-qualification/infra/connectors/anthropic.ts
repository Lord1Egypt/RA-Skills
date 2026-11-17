import { defineConnector } from "@cargo-ai/cdk";

// The model the deep-research agent runs on. `default: true` binds the
// workspace's authorized Anthropic connector rather than creating one, so the
// pipeline deploys with no key of its own. The form's tool does not use it:
// the page answer pays for no model call.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
