## Description:

Provides access to Tisane language-processing actions for analyzing and transforming text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to access Tisane actions for analyzing, comparing, extracting, detecting, and transforming text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified software.

Mitigation: Preinstall a verified oo CLI release and prevent automatic execution of fallback installers.

Risk: Startup skill synchronization may install additional agent skills.

Mitigation: Review whether synchronized skills are wanted; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Text sent for processing is handled by OOMOL and Tisane.

Mitigation: Submit only text that you permit OOMOL and Tisane to process.

## Reference(s):

- [Tisane API documentation](https://docs.tisane.ai/apis/tisane-api-short/nlu-nlp-methods)
- [Tisane](https://tisane.ai)
- [oo CLI commands](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [JSON service responses and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
