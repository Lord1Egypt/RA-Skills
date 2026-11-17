import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { leadResearcher } from "../agents/lead-researcher";
import { slack } from "../connectors/slack";
import { playsFolder } from "../folders";
import { gtmContacts } from "../models/gtm-contacts";
import { slackChannelId } from "../settings";

// One qualified inbound contact in, one brief and tier on the record and one
// Slack note out. It runs after the form's tool has answered the page, so the
// research never slows the visitor down.
//
// Keep this body to straight calls, writes and template strings. It is parsed
// from source, and constructs that typecheck and plan cleanly can still fail
// at runtime: optional chaining failed a live run with `OptionalMemberExpression
// … got "MemberExpression"`. No `?.`, no `??`, no `||` fallbacks, no indexing
// into an agent's answer; the contract checks the compiled expressions.
const researchLead = defineWorkflow(
  "research_qualified_lead",
  {
    // `defineContact` columns plus the inbound ones the form wrote.
    input: z.object({
      id: z.string(),
      account_id: z.string().optional(),
      first_name: z.string().optional(),
      last_name: z.string().optional(),
      email: z.string().optional(),
      title: z.string().optional(),
      linkedin_url: z.string().optional(),
    }),
    output: z.object({ tier: z.string() }),
    uses: { slack, leadResearcher },
    // The body is parsed from source, not executed: the model handle and the
    // channel constant it names are handed to the parser here.
    imports: { gtmContacts, slackChannelId },
  },
  ({ input, uses, model }) => {
    const verdict = uses.leadResearcher({
      prompt: `Research and tier this qualified inbound lead. Contact: ${JSON.stringify(input)}. The company is the gtm_accounts row with id ${input.account_id}.`,
    });

    // The research and its stamp land on one node, so a contact is never
    // marked researched without carrying the research. Bare slugs: the write
    // path nests them under `custom` itself.
    model.customColumn({
      modelUuid: gtmContacts.uuid,
      id: input.id,
      mappings: [
        { columnSlug: "inbound_tier", value: verdict.answer.tier },
        { columnSlug: "inbound_brief", value: verdict.answer.brief },
        {
          columnSlug: "inbound_rationale",
          value: `${verdict.answer.rationale} Sources: ${verdict.answer.sources}`,
        },
        { columnSlug: "inbound_researched_at", value: new Date() },
      ],
    });

    uses.slack.postMessage({
      channelId: slackChannelId,
      format: "markdown",
      disableUnfurling: true,
      body: `:mag: *${input.first_name} ${input.last_name}* (${input.email}): tier *${verdict.answer.tier}*\n${verdict.answer.brief}\n_${verdict.answer.rationale}_\nSources: ${verdict.answer.sources}`,
    });

    return { tier: verdict.answer.tier };
  },
);

// Researches each contact the form qualified, once.
//
// Who: `inbound_status` "qualified", the value the form's tool writes, so a
// not-qualified submitter or a contact loaded from elsewhere never pays for
// research. Once: `changeKinds: ["added"]` creates runs for rows entering the
// filter, and the blank `inbound_researched_at` is the second key, so a
// re-enable or a manual run never pays twice.
//
// Ships disabled. Enabling is the last yes after a pilot, and `added` does not
// backfill contacts that qualified while it was off: run it once by hand for
// those.
export const researchQualifiedLeads = definePlay("research_qualified_leads", {
  description:
    "Researches each contact the form qualified, writes a tier and a brief onto the record, and posts a note to Slack.",
  folder: playsFolder,
  model: gtmContacts,
  workflow: researchLead,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: gtmContacts.columns.custom__inbound_status,
            operator: "is",
            values: ["qualified"],
          },
          {
            kind: "date",
            columnSlug: gtmContacts.columns.custom__inbound_researched_at,
            operator: "isNull",
          },
        ],
      },
    ],
  },
  isEnabled: false,
  runCreationRule: "noConcurrency",
  changeKinds: ["added"],
  schedule: { type: "cron", cron: "*/15 * * * *" },
});
