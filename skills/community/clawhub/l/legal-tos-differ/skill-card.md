## Description:

Fetches Terms of Service documents, stores snapshots, and performs semantic diffing to identify meaningful legal changes across Privacy Risks, Financial Changes, and User Rights categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance reviewers, and policy analysts use this skill to track Terms of Service or privacy policy pages, capture snapshots, and produce semantic change analysis focused on privacy, financial, and user-rights impacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool commands accept URL and label values that may execute unintended shell commands if crafted maliciously.

Mitigation: Use only trusted inputs, review command invocations before execution, and run the skill in a constrained environment.

Risk: The skill fetches arbitrary URLs, which may expose internal services or untrusted network locations.

Mitigation: Restrict allowed URLs to expected public legal-document hosts and avoid running the skill where internal network access is available.

Risk: Fetched page content can influence the generated semantic analysis prompt.

Mitigation: Treat generated analysis as review support, verify important legal conclusions manually, and avoid relying on untrusted page content without review.

Risk: Removing a tracked URL can permanently delete associated snapshot data.

Mitigation: Back up snapshot data before removal and confirm the target URL before using the remove command.

## Reference(s):

- [Legal/TOS Diff-er ClawHub page](https://clawhub.ai/liverock/skills/legal-tos-differ)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown command output and structured semantic analysis prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores fetched document snapshots as JSON files and returns markdown summaries or comparison prompts.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
