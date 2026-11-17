import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The shared GTM contacts model, declared exactly as every pipeline declares
// it (scripts/native-models.json). A project that installs several pipelines
// keeps one: rewire the imports to the first copy and drop the others.
//
// Each submitter lands here, matched on `email`, with `lead_source` "website"
// and `account_id` the gtm_accounts row of their company. What only an inbound
// contact has is added as columns under plain names, never a `cargo_` prefix;
// they merge with any other pipeline's added columns on the shared model.
export const gtmContacts = defineModel("gtm_contacts", {
  name: "GTM contacts",
  kind: "native",
  extractSlug: "defineContact",
  folder: modelsFolder,
  additionalColumns: [
    {
      kind: "custom",
      slug: "inbound_status",
      type: "string",
      label: "Inbound status",
      description:
        "qualified, not_qualified or unknown_company, from the website form.",
    },
    {
      kind: "custom",
      slug: "inbound_message",
      type: "string",
      label: "Inbound message",
      description: "What the submitter wrote in the website form.",
    },
    {
      kind: "custom",
      slug: "inbound_page_url",
      type: "string",
      label: "Inbound page",
      description: "The page the form was submitted from.",
    },
    {
      kind: "custom",
      slug: "utm_source",
      type: "string",
      label: "UTM source",
      description: "The utm_source of the visit that submitted the form.",
    },
    {
      kind: "custom",
      slug: "utm_campaign",
      type: "string",
      label: "UTM campaign",
      description: "The utm_campaign of the visit that submitted the form.",
    },
    {
      kind: "custom",
      slug: "marketing_consent",
      type: "boolean",
      label: "Marketing consent",
      description:
        "Whether the submitter ticked the box to receive product news by email.",
    },
    // Written by the deep-research play, after the page has answered.
    {
      kind: "custom",
      slug: "inbound_tier",
      type: "string",
      label: "Inbound tier",
      description:
        "A, B, C or disqualified, from the tiering rubric in the workspace context.",
    },
    {
      kind: "custom",
      slug: "inbound_brief",
      type: "string",
      label: "Inbound brief",
      description:
        "At most three sentences: who they are, what the company does, why they might be talking to us now.",
    },
    {
      kind: "custom",
      slug: "inbound_rationale",
      type: "string",
      label: "Inbound rationale",
      description:
        "The rubric lines that decided the tier, the evidence behind them, and the pages relied on.",
    },
    {
      kind: "custom",
      slug: "inbound_researched_at",
      type: "date",
      label: "Inbound researched at",
      description:
        "When the deep research was written. Blank until then: the play's once-only key.",
    },
  ],
});
