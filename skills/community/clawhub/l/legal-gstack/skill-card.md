## Description:

Legal Gstack is a Chinese-language legal workflow automation suite with specialist roles for legal research, document drafting, evidence analysis, trial preparation, live operations, client intake, conflict checks, and case management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcochen823](https://clawhub.ai/user/marcochen823)

### License/Terms of Use:

MIT-0

## Use Case:

External legal practitioners and legal operations users can use this skill to standardize matter intake, research, drafting, evidence review, trial preparation, conflict checks, case tracking, and content operations around local matter folders. Human legal review remains required before relying on any advice, filings, deadlines, or client-facing output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works with case files, client communications, conflict checks, and live-comment archives that may contain confidential legal information.

Mitigation: Use approved protected local storage, limit access to matter folders, and handle generated reports and archives as confidential work product.

Risk: Legal research, drafting, evidence analysis, trial preparation, deadline, and intake outputs may be incomplete or unsuitable for a specific matter.

Mitigation: Require qualified human legal review before relying on outputs for advice, filings, strategy, deadlines, acceptance decisions, or client-facing communication.

Risk: The artifact reads from and writes to local Documents paths for active matters, templates, legal documents, and archives.

Mitigation: Verify generated paths before saving, archiving, replacing, or organizing files, especially when closing matters or updating knowledge-base materials.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown and generated local matter documents or reports, with command-style usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized around local Documents folders for matters, legal documents, knowledge-base material, conflict checks, and live-operation archives.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
