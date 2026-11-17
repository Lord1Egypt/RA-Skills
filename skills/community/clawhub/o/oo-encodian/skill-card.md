## Description:

Use the oo CLI to run Encodian PDF actions through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can process PDFs through an existing Encodian connection, including compressing files, extracting pages or text, and securing or unlocking documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes a remote installer whose current contents and resulting system changes are unverified.

Mitigation: Review the setup first and install a verified oo CLI release yourself.

Risk: Cross-agent skill synchronization may affect other installed skills.

Mitigation: Decide whether synchronization is acceptable and use OO_SKILLS_SYNC_DISABLED to disable it if needed.

Risk: Documents processed through the service may be shared with OOMOL and Encodian.

Mitigation: Submit only documents you are authorized to share with both providers.

## Reference(s):

- [Encodian API documentation](https://support.encodian.com/hc/en-gb/articles/13253632800284-Direct-API-Integration)
- [Encodian homepage](https://www.encodian.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Encodian on ClawHub](https://clawhub.ai/oomol/skills/oo-encodian)

## Skill Output:

**Output Type(s):** [API calls, Text, JSON, PDF content]

**Output Format:** [JSON action responses, extracted text, and base64 PDF content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF outputs are returned as base64 content.]

## Skill Version(s):

1.0.6 (source: artifact frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
