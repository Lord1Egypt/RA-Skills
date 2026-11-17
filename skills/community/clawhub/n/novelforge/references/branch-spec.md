# Agent hand-off contract

The workflow has four roles with separate outputs. Roles may be implemented by
different agents or by one orchestrator, but the artifact boundaries remain.

| Role | Reads | Writes |
| --- | --- | --- |
| Builder | project profile, prior settlement, explicit references | blueprint JSON |
| Writer | locked Context Ticket, blueprint, active engine snapshot | chapter text |
| Text reviewer | chapter text, profile, linter output | text review JSON |
| Story reviewer | ticket, settlement history, declared dependencies | engine review JSON |

The orchestrator runs `novelforgectl` between roles. A role may propose content, but
only the script advances machine state. Reviews never edit the chapter; the
writer applies a hash-checked narrow patch and reruns all checks.

## Required hand-off fields

- chapter ID and current state;
- input hashes used by the role;
- selected engine card IDs, if any;
- explicit changes, unresolved questions, and evidence locations;
- a deterministic output path.

Missing fields stop the next role. Human notes can explain a decision but cannot
replace a required JSON artifact.
