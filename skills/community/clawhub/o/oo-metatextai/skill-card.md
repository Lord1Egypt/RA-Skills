## Description:

MetatextAI (metatext.ai). Use this skill for ANY MetatextAI request — reading, creating, and updating data. Whenever a task involves MetatextAI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill through the oo CLI to inspect and manage MetatextAI guardrail policies, evaluate chat transcripts, and run test scans. Policy creation and test scans can change application state, so review their effects before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI startup synchronization and setup defaults may affect the agent environment without clearly explaining those effects.

Mitigation: Consider disabling startup skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting, and review setup effects before running the CLI.

Risk: The remote installers and deployed CLI binary were not verified.

Mitigation: Prefer a verified CLI release and review the installation source before installing.

Risk: Chat transcripts submitted for evaluation may be processed by OOMOL and MetatextAI.

Mitigation: Submit only transcripts you are authorized to share with both services.

Risk: Policy changes and test scans can affect the connected MetatextAI application.

Mitigation: Review policy changes and test scans before approval.

## Reference(s):

- [MetatextAI API documentation](https://docs.metatext.ai/introduction)
- [MetatextAI](https://metatext.ai)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected MetatextAI action; some actions modify guardrail configuration or run scans.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
