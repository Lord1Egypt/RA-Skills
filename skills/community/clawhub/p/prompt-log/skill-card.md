## Description:

Extract conversation transcripts from AI coding session logs (.jsonl) for Clawdbot, Claude Code, and Codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesash](https://clawhub.ai/user/thesash)

### License/Terms of Use:


## Use Case:

Developers and AI coding tool users use this skill to export local .jsonl session logs into markdown transcripts for review or recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported AI session transcripts can contain prompts, code, credentials, personal data, and confidential project context.

Mitigation: Review and redact generated markdown before sharing it outside the intended audience.

Risk: The artifact references scripts/extract.sh, but that script was not present in the inspected artifact.

Mitigation: Confirm the extraction script is supplied and reviewed before relying on the skill in a workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown transcript with command-oriented usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a transcript file under .prompt-log/ or to a user-specified output path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
