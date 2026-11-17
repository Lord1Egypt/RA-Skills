import { defineAgent } from "@cargo-ai/cdk";

import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";

// The deep research on a qualified lead: one brief and one tier, after the
// page has answered. The form's workflow stays rules-only and fast; this agent
// runs later, from the research play, and never on the submission path.
//
// A judge, not a writer. No Slack, no writable model: it hands back JSON and
// the play decides what lands where. `context` (read-only) is the ICP and the
// tiering rubric; `webSearch` is the research, capped by `maxSteps` and the
// prompt's budget. The person is researched only in their professional role
// at the company they named: no personal email, phone or address lookup.
export const leadResearcher = defineAgent("inbound_lead_researcher", {
  name: "Inbound lead researcher",
  description:
    "Researches a qualified inbound lead and their company, and tiers the company against the ICP and the tiering rubric.",
  color: "yellow",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  maxSteps: 10,
  systemPrompt: [
    "You brief the team on a qualified inbound lead who just asked for a demo. You are handed the contact record and the company the form identified; you research both and tier the company.",
    "Read the ICP and the account tiering rubric from the workspace context first. They are the rubric; nothing in this prompt overrides them. If the context has no tiering rubric, tier against the ICP alone and say so in the rationale.",
    "Research with at most four web searches: what the company does and for whom, one thing it publicly says is hard or is changing (a launch, a hire, a funding round, a stated priority), and the person's role there. Prefer the company's own site; record every page you rely on.",
    "Never invent a fact, a title or a URL. An absent fact is absent: say so and tier on what is known.",
    "A disqualifier in the ICP ends the evaluation at 'disqualified'. A competitor, a student, a job seeker or a vendor pitching us is 'disqualified', and the rationale says which.",
    "Return the judgment only, in the exact JSON shape requested. The brief is at most three sentences the team can read in ten seconds. The sources field lists every page you relied on, separated by ' · '.",
  ].join(" "),
  output: {
    type: "jsonSchema",
    jsonSchema: {
      type: "object",
      properties: {
        tier: {
          type: "string",
          enum: ["A", "B", "C", "disqualified"],
          description: "The tier from the tiering rubric.",
        },
        rationale: {
          type: "string",
          description:
            "Two sentences naming the rubric lines that decided the tier and the evidence behind them.",
        },
        brief: {
          type: "string",
          description:
            "At most three sentences: who they are, what the company does, why they might be talking to us now.",
        },
        // One string, not an array: the play puts it in a message as is.
        sources: {
          type: "string",
          description:
            "Every page the brief or the tier relied on, separated by ' · '.",
        },
      },
      required: ["tier", "rationale", "brief", "sources"],
      additionalProperties: false,
    },
  },
  capabilities: [
    "webSearch",
    { slug: "context", config: { isReadOnly: true } },
  ],
  // The QA gate. A tier with no grounded rationale, or a brief carrying a fact
  // no source supports, fails.
  evaluator: {
    rubric:
      "Did it tier against the rubric in the workspace context, with a tier the rubric defines and a rationale naming the deciding lines? Is every fact in the brief supported by the record or a listed source?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
