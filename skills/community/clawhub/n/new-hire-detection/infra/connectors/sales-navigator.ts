import { defineConnector } from "@cargo-ai/cdk";

// The source: Sales Navigator people searches, extracted by `fetchLeadSearch`
// on ../models/new-hires.ts. Bound with `default: true`, and it runs on
// Cargo's managed identities, so there is no LinkedIn seat, no cookie and no
// key to configure. Every extracted lead bills in credits.
//
// Two of its actions are design-time CLI calls, never deployed resources:
//   - `searchPersonMetrics` takes one search URL and returns `total_leads`.
//     It is the count-first gate: one cheap call tells you whether a search
//     fits under the 2,500-per-URL cap before you pay to extract it.
//   - `searchLeads` takes structured filters and is how you check that a
//     search URL returns the people you meant before it becomes the model.
export const salesNavigator = defineConnector("sales_navigator", {
  integration: "salesNavigator",
  default: true,
});
