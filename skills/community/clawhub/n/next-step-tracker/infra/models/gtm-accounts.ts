import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// Who owns each account: the name a nudge is grouped under. The tracker reads
// `name`, `website` and `owner_id` and never writes them.
//
// A native `defineAccount` model, so the example needs no CRM. If another
// pipeline in the project already declares the account universe (tam-building,
// account-scoring), rewire the import to that model and drop this file. If the
// accounts live in a CRM, swap this for a connector-backed model of its
// companies (`crm-backed` in SKILL.md).
//
// `gtm_accounts` is a shared native model (scripts/native-models.json): every
// pipeline that needs accounts declares it under this slug, so a project that
// installs several keeps one, with each pipeline's added columns merged.
export const gtmAccounts = defineModel("gtm_accounts", {
  name: "GTM accounts",
  kind: "native",
  extractSlug: "defineAccount",
  folder: modelsFolder,
});
