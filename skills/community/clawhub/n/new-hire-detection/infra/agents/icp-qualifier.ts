import { defineAgent } from "@cargo-ai/cdk";

import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";

// The qualifier: one judgment per company a new hire just joined, and the
// gate in front of the Slack post. With the `crm_routing` variation it moves to
// the new-account route only: customers and accounts with an open deal are
// qualified by definition, and scoring them again can drop an account somebody
// already sold.
//
// An agent instead of a headcount filter, because the company object carries
// more than a number: description, specialties, industry and locations. That
// is what lets it apply exclusions no filter can, such as competitors,
// agencies reselling someone else's product, holding companies, and pages that
// are not an operating business.
//
// A classifier, not a writer: temperature 0, and the output enforced by the
// JSON schema below rather than asked for in the prompt. `context` (read-only)
// is what connects it to the ICP; without it the prompt's reference to icp.md
// reads nothing and the agent invents a plausible ICP for every company. The
// step budget covers reading the ICP and answering, nothing more: it judges
// on the enriched company it is handed, never on a web search.
//
// The ICP is deliberately NOT in this prompt. It lives in the project's
// context repo (`context/icp.md` in a scaffolded project), so changing who
// qualifies is a reviewed commit rather than a deploy. The skill's own
// context/icp.md is the example to copy there.
//
// No writable model, no CRM and no Slack in reach. The agent hands back a
// verdict and the play acts on it: the gate is a branch in the workflow, never
// a choice the agent makes by writing or posting.
export const icpQualifier = defineAgent("new_hire_icp_qualifier", {
  color: "blue",
  connector: anthropic,
  languageModel: "claude-sonnet-4-5", // PLACEHOLDER — your model of choice
  temperature: 0,
  maxSteps: 3,
  systemPrompt: [
    "You decide whether a company belongs in a B2B seller's ideal customer profile, because someone in a buying role just joined it.",
    "Read icp.md from the workspace context before every judgment. It is the rubric; nothing in this prompt overrides it.",
    "Judge only on the company object you are given. An absent fact is an absent fact: never invent a headcount, an industry or a location.",
    "A disqualifier in the ICP makes the company not ICP, whatever else fits. Competitors of the seller are always disqualified.",
    "Return the verdict only. The play decides what to post or write; you do neither.",
    "Answer in the exact JSON shape requested: a score from 0 to 100, a tier, whether it is ICP, a two-sentence rationale naming the ICP lines that decided it, and your confidence.",
  ].join(" "),
  output: {
    type: "jsonSchema",
    jsonSchema: {
      type: "object",
      properties: {
        fit_score: {
          type: "number",
          description: "0 to 100 against icp.md.",
        },
        fit_tier: {
          type: "string",
          enum: ["Tier 1", "Tier 2", "Tier 3"],
          description: "Tier 1 is the best fit.",
        },
        is_icp: {
          type: "boolean",
          description:
            "True only when no disqualifier applies and the fit is worth a rep's time.",
        },
        rationale: {
          type: "string",
          description:
            "Two sentences naming the ICP lines that decided the verdict and the company facts behind them.",
        },
        confidence: {
          type: "string",
          enum: ["high", "medium", "low"],
          description: "Low when the company object was too thin to judge.",
        },
      },
      required: ["fit_score", "fit_tier", "is_icp", "rationale", "confidence"],
      additionalProperties: false,
    },
  },
  capabilities: [{ slug: "context", config: { isReadOnly: true } }],
  folder: agentsFolder,
});
