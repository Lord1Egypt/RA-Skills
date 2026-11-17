import { defineAgent } from "@cargo-ai/cdk";

import { trackerPrompt } from "./tracker.prompt";
import { anthropic } from "../connectors/anthropic";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { gtmAccounts } from "../models/gtm-accounts";
import { gtmActivities } from "../models/gtm-activities";
import { commitments } from "../models/commitments";

// The tracker: every promise made on a call, kept or chased.
//
// A Claude Code harness agent, because its input is the call log in the
// repository (cadence/log/calls/, written by call-capture) and only a harness
// has a checkout. It reads that checkout and writes nothing back. Its state is
// the commitments model, so a promise is extracted once, closed once, and
// nudged at most once a day, without a pull request to review every morning.
//
// Evidence comes from models declared in this folder, read-only: `gtm_activities`
// (what the team did on each account after a call) and `gtm_accounts` (who owns
// each one). Both are native, so the example deploys with no CRM; a team on
// HubSpot, Salesforce or Attio swaps them for connector-backed models and the
// prompt does not change. Slack is `postMessage` with the channel
// locked, the same way standup locks it: a nudge quotes what a customer said
// on a call, and a channel the agent picks is how that lands in front of them.
//
// No `capabilities`: the repository is the context this agent needs, and the
// prompt holds every read to read-only.
export const tracker = defineAgent("commitment_tracker", {
  name: "Next-step tracker",
  description:
    "Records every commitment made on a call, closes the ones the activity log shows were kept, and posts the ones due or overdue to Slack.",
  color: "yellow",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  // No `state`: deploy binds this project's connected state (cargo.state.json).
  // The harness clones that state's production branch, so it reads the call
  // entries that were merged, not the ones still in an open call-capture pull
  // request. A project whose state is not connected deploys this agent
  // unbound, with an empty sandbox; `cargo-ai project check` prints which.
  env: {
    // IANA timezone "today" is computed in, for due dates and the one post a
    // day. The cron is 14:00 UTC, which is 7am here during PDT; change both
    // together.
    TRACKER_TIMEZONE: "America/Los_Angeles",
  },
  uses: [
    { ref: commitments, readOnly: false },
    // Evidence only. A tracker that could write activities could close its own
    // commitments.
    { ref: gtmActivities, readOnly: true },
    { ref: gtmAccounts, readOnly: true },
    {
      ref: slack.actions.postMessage,
      config: {
        // PLACEHOLDER: the channel the nudges land in, as a Slack id (C…)
        // read from the connector's channel autocomplete. Locked.
        channelId: "C0123456789",
        format: "markdown",
        disableUnfurling: true,
      },
    },
  ],
  triggers: [
    {
      type: "cron",
      name: "weekday_morning",
      // 14:00 UTC, Monday to Friday: an hour after call-capture's 07:00 UTC
      // scribe, and 7am PT during PDT.
      cron: "0 14 * * 1-5",
      text: "Run the next-step tracker. Follow your system prompt exactly: extract new commitments, close the kept ones on evidence, post what is due today or overdue once.",
    },
  ],
  systemPrompt: trackerPrompt,
  evaluator: {
    rubric:
      "Was every new commitment quoted from a call entry and recorded once? Was every closed one backed by a cited activity or later call entry? Did at most one message post, listing only open commitments due today or earlier and not already nudged today?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
