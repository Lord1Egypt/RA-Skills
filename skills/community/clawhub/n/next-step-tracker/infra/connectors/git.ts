import { defineConnector } from "@cargo-ai/cdk";

// The git provider the coding harness clones through. The tracker reads the
// call log entries under cadence/log/calls/ from that checkout and writes
// nothing back: its state lives in the commitments model, not in a pull
// request.
//
// Nothing imports this handle. The agent leaves `repository.connector` unset,
// and plan/deploy resolve it from the project's own GitHub connector — this
// one. Bound, not created: `default: true` authorizes nothing, a deploy cannot
// mint an OAuth grant (`cargo-ai project add connector/github` does).
export const git = defineConnector("github", {
  integration: "github",
  default: true,
});
