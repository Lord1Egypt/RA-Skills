import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { icpQualifier } from "../agents/icp-qualifier";
import { linkedin } from "../connectors/linkedin";
import { slack } from "../connectors/slack";
import { playsFolder } from "../folders";
import { newHires } from "../models/new-hires";

// PLACEHOLDER: the Slack channel every qualified new hire is posted to. A
// channel id (C…), not a name: names collide, and the connector's autocomplete
// resolves the id. Locked here so no run can post anywhere else.
const slackChannelId = "PLACEHOLDER_SLACK_CHANNEL_ID";

// One person who just took a target role somewhere in the market:
//
//   no domain        -> stop: nothing to qualify the company on
//   not ICP          -> stop: the channel only hears about companies worth a
//                       rep's time
//   ICP              -> one Slack message with the person, the company, the
//                       verdict and the links
//
// Ends at the Slack post. Nothing is written to a CRM and nothing is sent to
// the person. Writing into the CRM is the `crm_routing` variation, and a
// read-only "already in the CRM" line is `crm_lookup`; both are in
// references/crm-adaptation.md in the skill.
const routeNewHire = defineWorkflow(
  "route_new_hire",
  {
    // The `fetchLeadSearch` columns this workflow reads. Confirm them against
    // the live model after the first sync (`cargo-ai storage column list`).
    input: z.object({
      linkedin_profile_url: z.string(),
      sales_navigator_company_url: z.string(),
      first_name: z.string().optional(),
      last_name: z.string().optional(),
      job_title: z.string().optional(),
      company_name: z.string().optional(),
      tenure_length: z.string().optional(),
    }),
    output: z.object({
      status: z.enum(["posted", "not_icp", "no_domain"]),
      rationale: z.string().optional(),
    }),
    uses: { linkedin, slack, icpQualifier },
    imports: { slackChannelId },
  },
  ({ input, uses }) => {
    // The lead carries a company URL and a name, not the firmographics the
    // qualifier judges on. Enrich first, judge second.
    const company = uses.linkedin.enrichCompany({
      linkedinUrl: input.sales_navigator_company_url,
    });

    // The domain guard. A company page with no website is usually not an
    // operating business, and every CRM variation matches on the domain.
    if (!company.domain) {
      return { status: "no_domain" as const };
    }

    // The gate. Without it the channel hears about every new hire in the
    // market and stops being read within a week.
    const verdict = uses.icpQualifier({
      prompt: `Qualify ${company.company_name} (${company.domain}) against the ICP. ${input.first_name} ${input.last_name} just joined as ${input.job_title}. Company object: ${JSON.stringify(company)}`,
    });

    if (!verdict.answer.is_icp) {
      return {
        status: "not_icp" as const,
        rationale: verdict.answer.rationale,
      };
    }

    // Field names follow standup's locked postMessage use. Confirm them with
    // `cargo-ai project types` after the Slack connector is authorized.
    uses.slack.postMessage({
      channelId: slackChannelId,
      format: "markdown",
      disableUnfurling: true,
      body: `*New ${input.job_title} at ${company.company_name}* (${verdict.answer.fit_tier}, ${verdict.answer.fit_score}/100)\n${input.first_name} ${input.last_name} just joined ${company.company_name} (${company.domain}) as ${input.job_title}, ${input.tenure_length} in.\n\n${verdict.answer.rationale}\n\nPerson: ${input.linkedin_profile_url}\nCompany: ${company.linkedin_url}`,
    });

    return {
      status: "posted" as const,
      rationale: verdict.answer.rationale,
    };
  },
);

// Routes every person the search adds. There is no filter: the search URL
// already IS the audience, and a segment that restated it would be a drift
// trap.
//
// `changeKinds: ["added"]` is what makes a person posted once. The model
// re-extracts the whole search on every sync, and only people who were not in
// it before create a run. Drop it and every sync re-posts the whole search,
// paying for the enrichment and the qualifier again.
//
// Cron, not watch or realtime: `fetchLeadSearch` is a fetch-mode extractor,
// so realtime and watch both fail at deploy with integrationNotCompatible.
// Hourly, because the model syncs on its own schedule and a new row should not
// wait a day for its run; ticks with nothing added create nothing.
//
// Ships disabled. Enabling is the last yes after the pilot of ten, not an
// input. Enable, then execute once: `changeKinds: ["added"]` does not
// backfill rows that landed while the play was off.
export const routeNewHires = definePlay("route_new_hires", {
  description:
    "Posts each person who just took a target role at a company that fits the ICP to Slack, with the qualifier's verdict and the links.",
  folder: playsFolder,
  model: newHires,
  workflow: routeNewHire,
  isEnabled: false,
  runCreationRule: "noConcurrency",
  changeKinds: ["added"],
  schedule: { type: "cron", cron: "20 * * * *" },
});
