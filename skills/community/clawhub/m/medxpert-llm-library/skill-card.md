## Description:

Guides users through setting up a local LLM knowledge base on existing hardware, including model deployment, document preparation, retrieval-augmented question answering, and library management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers, knowledge workers, and small teams use the skill to choose a local model and organize document search and question answering on available hardware. It provides setup guidance for keeping work local, with privacy safeguards requiring verification before confidential files are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy claims are not enforced, and the bundled audit does not establish network isolation for confidential files.

Mitigation: Require a verified local-only endpoint, review host permissions and installers, and reject file symlinks that lead outside the library before using confidential data.

Risk: Sensitive-data scan output may print private information openly.

Mitigation: Mask scan output and avoid exposing it in logs or shared terminals.

Risk: Summarization replaces the library index.

Mitigation: Use a dedicated library folder and back up the index before summarizing.

## Reference(s):

- [Project homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [MedXpert knowledge base](https://medxpert.cn)
- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/medxpert-llm-library)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup steps vary with hardware, operating system, model, and privacy requirements.]

## Skill Version(s):

1.29.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
