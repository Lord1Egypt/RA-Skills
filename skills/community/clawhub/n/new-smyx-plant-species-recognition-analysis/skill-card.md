## Description:

Identifies plant species from image or video inputs and returns structured information such as species name, family, growth habits, maintenance tips, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze plant images or videos for species identification, similar-species differentiation, structured plant knowledge, and cloud-hosted recognition report lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media and identity-linked data are sent to an external cloud service.

Mitigation: Use only with plant media and identifiers that may be shared with the publisher and lifeemergence.com service.

Risk: The skill can silently create or reuse backend/local user identity state and query cloud report history.

Mitigation: Review identity and report-history behavior before installation, and restrict use to trusted workspaces and accounts.

Risk: The security scan reports local plaintext token storage.

Mitigation: Avoid running the skill on shared machines, rotate affected credentials after testing, and remove local token state when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/new-smyx-plant-species-recognition-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style structured analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save analysis output to a file when an output path is provided.]

## Skill Version(s):

999.999.999 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
