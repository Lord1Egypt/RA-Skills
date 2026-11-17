## Description:

Connects an OOMOL account to tl;dv to find meetings, retrieve meeting details, notes and transcripts, and import publicly accessible recording URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use the skill to search their tl;dv meetings, retrieve meeting details, notes and transcripts, or submit a publicly accessible recording URL for import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the oo CLI can execute unverified remote software.

Mitigation: Review CLI installation separately and verify a fixed release before allowing execution.

Risk: Automatic skill synchronization may introduce broader agent changes without clear approval.

Mitigation: Check automatic skill synchronization before use and disable it if its changes are not intended.

Risk: The connected account can expose sensitive meeting content, and importing a recording changes tl;dv state.

Mitigation: Consider the sensitivity of meeting data and confirm each import before submitting its recording URL.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [tl;dv API documentation](https://doc.tldv.io/index.html)
- [tl;dv website](https://tldv.io)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, JSON]

**Output Format:** [Structured JSON responses and Markdown meeting notes or transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and the user's connected tl;dv account.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
