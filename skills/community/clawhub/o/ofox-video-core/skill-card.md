## Description:

ofox-video-core provides a shared execution layer for Ofox video API jobs, including job creation, polling, result download, and actual cost reporting for direct low-level use or scenario skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this library skill to submit Ofox video generation jobs, inspect available models and pricing, resume or debug jobs by id, and share common video API execution behavior across scenario skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Ofox video jobs can spend money if an agent runs a billable command without user agreement.

Mitigation: Use the documented dry-run cost table, get an explicit yes, and only then run the same command with --approved.

Risk: OFOX_API_KEY is a credential used for external Ofox API requests.

Mitigation: Keep the key private, avoid logging or echoing it, and verify OFOX_API_BASE_URL is unset or points to the expected host before use.

Risk: Local frame files supplied to the script may be encoded into requests sent to Ofox.

Mitigation: Use only files intended for upload to Ofox and tell the user when local media will be sent to the service.

Risk: Real-person reference inputs require authorization and can implicate likeness or privacy rights.

Mitigation: Use --real-person true only when the user has confirmed they are authorized to use the likeness; do not use it as a moderation bypass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/ofox-video-core)
- [Ofox publisher profile](https://clawhub.ai/user/ofoxai)
- [Homepage from ClawHub metadata](https://github.com/ofoxai/skills/tree/main/skills/ofox-video-core)
- [Ofox API key settings](https://app.ofox.ai)
- [API parameter reference](references/api-params.md)
- [Approval gate](references/approval-gate.md)
- [Video pricing](references/pricing.md)
- [Prompt structure for Seedance video jobs](references/prompt-structure.md)
- [Bundled model snapshot](references/models-snapshot.json)
- [Bundled pricing snapshot](references/pricing-snapshot.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce video job ids, polling URLs, downloaded mp4 paths, metadata sidecars, cost estimates, and actual cost reports when the referenced script is used.]

## Skill Version(s):

2.0.3 (source: frontmatter, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
