## Description:

LLM Knowledge Bases helps agents inspect, repair, and grow a local Markdown wiki from raw text, PDFs, images, and structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to operate a runtime-managed local wiki: compile source notes, answer from existing notes, maintain concept/entity/synthesis pages, repair source-id drift, and run wiki health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured runtime can read and update a local knowledge-base vault.

Mitigation: Run it with least privilege against only the intended vault, and use read-only or dry-run wording when changes are not intended.

Risk: The documented install path uses an unpinned @latest npm runtime.

Mitigation: Pin the npm runtime package version before deployment or repeatable review.

Risk: Broad prefixless triggers may route ordinary maintenance requests into persistent write workflows.

Mitigation: Use the explicit $llm-knowledge-bases prefix and narrow scope terms such as batch limits, read-only, or dry-run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/llm-knowledge-bases)
- [Repository layout](references/repo-layout.md)
- [Maintenance playbook](references/maintenance-playbook.md)
- [Andrej Karpathy public workflow attribution](https://x.com/karpathy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool calls, shell commands, configuration snippets, and wiki note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persistent wiki updates through the configured LLM Knowledge Bases runtime.]

## Skill Version(s):

1.2.2 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
