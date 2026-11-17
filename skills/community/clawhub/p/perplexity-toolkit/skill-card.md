## Description:

Automates Perplexity searches, batch research, source extraction, aggregation, verification, and multi-turn work in a resident browser console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers and research agents use this skill to search Perplexity, collect cited answers, process batches, and continue research across browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit controls a logged-in Perplexity browser and includes anti-detection behavior.

Mitigation: Use a test or low-risk browser profile and avoid sensitive files or regulated data.

Risk: Default citation readbacks can reach untrusted URLs, including private-network addresses.

Mitigation: Disable default verification or enforce outbound network controls if private-network access is a concern.

Risk: Enabling the optional judge sends questions, answers, and failure context to TypeSafe.

Mitigation: Leave the judge disabled unless that data transfer is intended.

Risk: Deleting conversation history can remove wanted records.

Mitigation: Use --dry-run before deleting history.

## Reference(s):

- [ClawHub release](https://clawhub.ai/mfang0126/skills/perplexity-toolkit)
- [Perplexity Pro reference guide](artifact/docs/reference-pro-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Text, Markdown, or JSON, depending on the command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search answers can include citations; batch results and reports can be saved to files.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
