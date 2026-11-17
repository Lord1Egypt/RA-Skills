import { defineConnector } from "@cargo-ai/cdk";

// The Slack workspace the inbound channel lives in, bound to the workspace's
// default connection.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
