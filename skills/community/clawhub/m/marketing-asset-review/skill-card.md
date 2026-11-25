## Description:

Review finished posters, main images, or short clips as a marketing asset review: a line-by-line note of what should not ship and what to change. Marketing asset review shows the checklist, then looks at the files you hand over, and can remake one replacement still or clip. Marketing assets here mean posters, covers, and main images. Use it for the pass before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing and content teams can use this skill to review an existing poster, cover, main image, or short clip before publishing. It provides a checklist and a line-by-line review, and can edit one selected asset when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a path for paid requests to bypass the documented confirmation gate.

Mitigation: Address that path before installation; require the user-visible work, live price, count, and request identity to be confirmed before every paid call.

Risk: The security assessment reports broad permissions and shared credential and state handling.

Mitigation: Review the requested access and protect the shared local credential and state files with the documented user-only permissions; disconnect and revoke access when no longer needed.

Risk: The security assessment reports automatic telemetry.

Mitigation: Review the installation-registration fields and privacy information before connecting, and avoid installation if the reporting is not acceptable.

Risk: The security assessment was partial because some local references could not be resolved, so its evidence is incomplete.

Mitigation: Resolve the unavailable references and review the package and a complete security assessment before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/marketing-asset-review)
- [Beatra skill information](https://beatra.ai/skills/marketing-asset-review)
- [Workflow](references/workflow.md)
- [Updates and security](references/updates-and-security.md)
- [Installation and authentication](references/installation-and-auth.md)

## Skill Output:

**Output Type(s):** [Markdown, Image files, Video files]

**Output Format:** [Markdown checklist and review note; one edited still image or short video when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviews the asset provided by the user; at most one replacement still or clip is edited from the selected source file.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
