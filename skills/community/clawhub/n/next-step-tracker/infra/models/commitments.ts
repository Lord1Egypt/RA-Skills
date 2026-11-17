import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The ledger: one row per promise made on a call, by either side.
//
// It is the tracker's whole memory. The repository is read, never written, so
// whether a commitment was already extracted, already closed, or already
// nudged today is answered here and nowhere else:
//   - `commitment_id` is the source entry's path plus a short slug of the
//     promise. Same entry, same promise, same id: a re-run extracts nothing new.
//   - `status` is open, done or dropped. Done only with `closed_evidence`.
//   - `last_nudged_on` is the date the commitment was last posted. A second run
//     on the same day posts nothing.
//
// A native custom model: it deploys with no connector and only the agent that
// owns it writes it.
export const commitments = defineModel("commitments", {
  kind: "native",
  extractSlug: "defineCustom",
  config: {
    columns: [
      { slug: "commitment_id", type: "string" },
      { slug: "account", type: "string" },
      // gtm_accounts.id when the company matched a row; empty otherwise, in which
      // case only a later call entry can close the commitment.
      { slug: "account_id", type: "string" },
      // The owner_id from the gtm_accounts model, or the call's host.
      { slug: "owner", type: "string" },
      // "us" or "them": who made the promise.
      { slug: "promised_by", type: "string" },
      // The promise, quoted from the entry's Actions or transcript.
      { slug: "promise", type: "string" },
      { slug: "due_date", type: "string" },
      // cadence/log/calls/<date>-<account>.md
      { slug: "source_entry", type: "string" },
      // open | done | dropped
      { slug: "status", type: "string" },
      { slug: "closed_at", type: "string" },
      // "gtm_activities:<id>" or the later call entry that proves it happened.
      { slug: "closed_evidence", type: "string" },
      { slug: "last_nudged_on", type: "string" },
    ],
  },
  folder: modelsFolder,
});
