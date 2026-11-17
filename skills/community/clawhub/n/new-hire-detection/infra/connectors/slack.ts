import { defineConnector } from "@cargo-ai/cdk";

// Where the team hears about a new hire. One message per qualified person, in
// one channel the operator named. Binds the workspace's DEFAULT Slack
// connector rather than creating one: authorize it once
// (`cargo-ai project add connector/slack`) and this declaration resolves to it.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
