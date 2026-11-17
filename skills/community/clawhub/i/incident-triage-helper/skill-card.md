## Description:

Complete local skill package to assess and potentially publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-chi](https://clawhub.ai/user/li-chi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to check a local skill package, record assessment notes, validate required files, and prepare a publication request or archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Included shell scripts validate package contents and create a local archive, which could behave unexpectedly if reused in a different package context.

Mitigation: Review scripts/package.sh and scripts/validate.sh before running them outside this artifact, and run them only in a trusted local checkout.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/li-chi/skills/incident-triage-helper)
- [Review Checklist](artifact/docs/review-checklist.md)
- [Assessment Notes](artifact/docs/assessment-notes.md)
- [Publish Request Template](artifact/templates/publish-request.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or validate a local tar.gz package when the included scripts are run.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
