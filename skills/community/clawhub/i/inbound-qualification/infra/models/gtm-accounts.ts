import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The shared GTM accounts model, declared exactly as every pipeline declares
// it (scripts/native-models.json). A project that installs several pipelines
// keeps one: rewire the imports to the first copy and drop the others.
//
// A submission's company lands here, matched on `website` (the email domain).
export const gtmAccounts = defineModel("gtm_accounts", {
  name: "GTM accounts",
  kind: "native",
  extractSlug: "defineAccount",
  folder: modelsFolder,
});
