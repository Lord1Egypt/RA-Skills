## Description:

Plc is a shell-based helper labeled for programmable logic controller programming that stores and manages local JSONL entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run local status, add, list, search, remove, export, statistics, and configuration commands for JSONL note data associated with PLC work. Security evidence says to treat it as a local note/config store rather than a PLC programming helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled as a PLC programming helper, but security evidence says the artifacts implement a generic local data store with deletion and export features.

Mitigation: Review behavior before installation and treat generated entries as local note/config data rather than validated PLC programming guidance.

Risk: The config path and export/serialization handling may be unsafe for untrusted values or sensitive industrial information.

Mitigation: Avoid storing credentials or sensitive industrial details, and do not run config commands with untrusted values until those paths are fixed and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/plc)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Structured text to stdout and JSONL/CSV files for stored or exported entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the PLC_DIR environment variable when set; otherwise stores local data under ~/.plc/.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
