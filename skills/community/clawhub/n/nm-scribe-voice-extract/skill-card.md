## Description:

Extracts a user's writing voice from text samples via SICO comparative analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers use the skill to analyze anonymized writing samples and create a reusable voice profile for consistent writing. It guides sample collection, comparative extraction, and profile and register creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing samples may contain private details that are copied into profile storage, and sample files may be overwritten.

Mitigation: Review sample contents and storage paths before intake, remove sensitive details, and back up existing profile files.

Risk: The security scan was partial because two referenced paths were missing, leaving some referenced material unreviewed.

Mitigation: Check the missing paths or confirm they are no longer needed, then review the complete skill before installation.

## Reference(s):

- [Claude Night Market Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)
- [Research basis for voice extraction](modules/research-basis.md)
- [Sample intake guidance](modules/sample-intake.md)
- [SICO extraction guidance](modules/sico-extraction.md)
- [Register creation guidance](modules/register-creation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown voice profile and register files, a JSON manifest, and comparative text analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Builds a reusable voice profile from user-provided writing samples; the documented validation target is at least three samples and 500 total words.]

## Skill Version(s):

1.10.3 (source: frontmatter, confirmed by server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
