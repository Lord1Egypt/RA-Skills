## Description:

Use the Foxit Cloud API through an OOMOL-connected account to inspect, convert, create, and manage documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document workflows use this skill to call Foxit Cloud API actions through an OOMOL-connected account for PDF analysis, conversion, creation, and editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document-changing operations are classified as reads, and the remote CLI installer and automatic skill synchronization have not been verified.

Mitigation: Correct the read/write classifications, require clear authorization for jobs, document changes, uploads, and quota use, and install a verified CLI release under your control while reviewing its automatic skill synchronization.

Risk: Documents pass through Foxit and OOMOL-related services, whose runtime handling and retention were not verified.

Mitigation: Review the providers’ applicable handling and retention terms before sending sensitive documents.

## Reference(s):

- [Foxit Cloud API](https://cloudapi.fuxinsoft.cn)
- [Foxit API documentation](https://cloudapi.fuxinsoft.cn/zh-CN/docs/services/generateSN)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-fuxin)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Files, Guidance]

**Output Format:** [Shell commands with JSON request payloads and structured JSON responses; document results may be uploaded to transit storage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may submit document-processing jobs; some return task status or file references rather than document content directly.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
