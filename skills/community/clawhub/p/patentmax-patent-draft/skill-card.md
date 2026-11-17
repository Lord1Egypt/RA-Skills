## Description:

Turns invention disclosures, technical materials, or an initial idea into a patent draft and a separate review note for inventor and patent-agent review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Inventors, researchers, and patent practitioners use this skill to turn technical disclosures into a draft specification with claim-structure previews and drawings, or to explore patentable directions from an early idea. A patent professional must review the draft before filing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unfiled invention details or confidential materials are sent to a remote drafting service whose data-handling terms are not fully detailed in the evidence.

Mitigation: Obtain authorization before sending materials, review PatentMax confidentiality and retention terms, and exclude trade secrets, export-controlled information, and customer-confidential data without approval.

Risk: An overridden service endpoint could receive the submitted materials and API key.

Mitigation: Verify PATENTMAX_BASE_URL is unset or points to the legitimate PatentMax endpoint before use.

Risk: Automatically inferred content or patent comparisons may be mistaken for verified facts or a filing-ready patent application.

Mitigation: Have the inventor verify review notes and supporting facts, and have a patent professional finalize claims and assess patentability before filing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patentmax-patent-draft)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Materials guide](references/materials-guide.md)
- [Drafting workflow](references/workflow.md)
- [Frequently asked questions](references/faq.md)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Two Word documents (.docx) containing a patent draft and review notes, plus brief status and result summaries; early-idea requests can yield a text list of directions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The draft includes a claim-structure preview rather than filing-ready claims; review notes identify inferred or missing facts and invention-point comparisons.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
