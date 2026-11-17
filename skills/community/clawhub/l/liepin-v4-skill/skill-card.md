## Description:

Automates Liepin candidate search and resume capture from Excel-based hiring criteria, producing structured candidate records, resume text, screenshots, and progress files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaoxinxin](https://clawhub.ai/user/qiaoxinxin)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and HR operators use this skill with an authorized Liepin account to search for candidates, score matches against hiring criteria, preserve resume evidence, and prepare candidate records for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized account automation or candidate outreach could violate account, site, or recruiting policies.

Mitigation: Use only with an authorized Liepin account and require human approval before enabling automated communication.

Risk: Candidate personal data, phone numbers, message previews, resume text, and screenshots may be stored locally.

Mitigation: Collect only necessary fields, restrict access to output folders, define short retention, and remove sensitive records when no longer needed.

Risk: Cookie handling and output-path assumptions may be unsuitable for production environments.

Mitigation: Review cookie storage and sanitize or configure output paths before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaoxinxin/skills/liepin-v4-skill)
- [Project homepage](https://github.com/qiaoxinxin/liepin-v4-skill)

## Skill Output:

**Output Type(s):** [files, text, configuration]

**Output Format:** [CSV candidate records, PNG resume screenshots, UTF-8 resume text, and JSON progress files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs under a desktop candidates directory and records resumable progress.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
