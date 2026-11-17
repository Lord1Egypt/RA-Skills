## Description:

Validate JSONL files for broken lines, summarize counts, time ranges, and key distributions. Use when checking evolution logs, memory graph exports, or any line-delimited JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operators use this skill to check JSONL logs and exports for malformed records, then review valid and invalid counts, timestamp coverage, and common keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is medium confidence because inspection was incomplete and tool-scope information was missing.

Mitigation: Review the skill's file access and commands before installing, and use it only with data you are permitted to inspect.

Risk: Invalid-line previews can include up to 120 characters from malformed records, which may contain sensitive data.

Mitigation: Review report output before sharing it, especially when validating files that may contain sensitive values.

Risk: The validator reads the entire file into memory, which may exhaust available memory for very large JSONL files.

Mitigation: Use it only on files that fit available memory; the skill documentation recommends a streaming approach for very large files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/147258xuan/skills/jsonl-validator)

## Skill Output:

**Output Type(s):** [Text, Shell exit code]

**Output Format:** [Plain-text validation report printed to standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports valid and invalid line counts, timestamp range when available, frequent JSON keys, and up to five invalid-line previews. Exit codes distinguish valid input, invalid JSON lines, and usage or missing-file errors.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
