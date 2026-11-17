import { defineConnector } from "@cargo-ai/cdk";

// The git provider the coding harness clones through, and pushes the branch and
// opens the pull request with. Its OAuth grant carries the `repo` scope, so this
// one connector is the agent's entire write path into the repository.
//
// Nothing imports this handle. That is deliberate: the agent leaves
// `repository.connector` unset, and plan/deploy resolve it from the project's
// own GitHub connector, this one. Declaring it is what makes it exist; wiring
// it by hand would only re-state what the resolver already knows.
//
// Bound, not created. `default: true` authorizes nothing: you grant it once in
// the browser (`cargo-ai project add connector/github`) and this declaration binds
// to it. A deploy cannot mint an OAuth grant.
export const git = defineConnector("github", {
  integration: "github",
  default: true,
});
