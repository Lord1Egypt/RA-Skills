## Description:

Finds commonly used IPC patent classification codes for a described technology and explains their meanings with representative patents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Inventors, researchers, and patent professionals can describe a technology to identify IPC classes commonly used by similar patents. They can use the plain-language explanations and representative patents to choose a classification or broaden a patent search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests and redirects may expose credentials or send them to untrusted destinations.

Mitigation: Ask the publisher to restrict requests and redirects to trusted HTTPS destinations; avoid valuable API keys until this is addressed.

Risk: Patent identifiers and file paths need safeguards before filesystem access.

Mitigation: Ask the publisher to validate patent identifiers before filesystem access, and avoid running with access to important files until corrected.

Risk: Technical details, spending, and locally saved credentials may need additional care.

Mitigation: Share only approved technical details, agree a spending limit, and consider whether to save credentials locally.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/ipc-code-finder)
- [PatentMax API reference](references/api-reference.md)
- [PatentMax search workflow](references/search-workflow.md)
- [PatentMax API platform](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Guidance, CSV file, Patent search results]

**Output Format:** [Excel-compatible UTF-8 CSV reference table with a concise conversational explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes IPC codes, plain-language meanings, counts among similar patents, representative patents, and suggested search use.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
