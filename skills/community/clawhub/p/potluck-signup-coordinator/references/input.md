# Offline helper contract

Python 3.11+ standard library, no network, writes, credentials or external actions. Resolve paths from the installed skill directory.

```sh
python3 scripts/reconcile.py assets/example.json
```

Run the command from this skill directory, or resolve both paths absolutely. For real use point to a private input JSON file. Reads only the explicitly supplied file and prints derived JSON; errors go to stderr with exit code 2. No output file is created and the source is unchanged. The included [example](../assets/example.json) is fictional.

Schema 1: before and after each contain explicit complete boolean, slots list and claims list. Snapshot complete means all relevant slots/claims were read without filters/truncation; it isn't merely a successful HTTP response. Empty snapshots must be explicitly supplied, never manufactured after a failed read.

Slots: unique id and capacity (nonnegative integer, measured in contribution units, not guests). Claims: unique id, slot_id, units (positive integer), status confirmed/cancelled; optional portions (nonnegative integer or null) and dish. Use opaque stable IDs, not emails. IDs must come from the provider or the maintained mapping; row numbers are not stable under sorting. No identity authentication is performed.

Normalize CSV exports/Sheets rows into this JSON contract before use. Supplied signup.csv is a layout example, not a direct helper input or an auto-importer. A Sheet row's blank contributor is open, not an accepted claim. Remove accidental formula execution during live writes; this script never evaluates strings.

Compare operational fields only. changed includes moved slots, units, portions, status or dish; private note/name changes are ignored. Removed means absent from a COMPLETE after snapshot, not independently verified cancellation. Explicitly cancelled IDs are reported separately. Missing from partial snapshots remains unknown. For partial snapshots open_units is null; possible_open_units_upper_bound is only an upper bound, never a confirmed vacancy. Observed coverage must not trigger cancellation/reassignment automatically. This script does not detect changed slot definitions; review slot capacities/descriptions separately.

Expected example: c-1 appears in missing_in_partial_claim_ids, NOT removed_claim_ids. No names/emails/dish/private fields appear in the output. Coverage shows contribution units separately from known portions and unknown portions. Overfills are reported, not fixed or silently truncated. Unknown or duplicate IDs and invalid quantities fail.
