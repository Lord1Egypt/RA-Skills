## Description:

Master skill for the Ollang translation platform that routes user intent to sub-skills for file uploads, order creation, status checks, revisions, QC, projects, folders, and human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mazizulak](https://clawhub.ai/user/mazizulak)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Ollang users use this skill to operate Ollang translation, captioning, dubbing, QC, revision, project, folder, and human-review workflows from an agent using natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording can route generic translation, captioning, or dubbing requests into authenticated Ollang actions.

Mitigation: Confirm the user intends to use Ollang before authenticated operations, especially uploads, order actions, QC, revisions, and human review.

Risk: File uploads send user-selected content to the external Ollang service.

Mitigation: Review the selected files and obtain explicit user approval before upload, particularly for confidential, regulated, or sensitive media and documents.

Risk: Order creation, rerun, QC evaluation, cancellation, and human review can affect billing, credits, or account state.

Mitigation: Require clear confirmation before billable or state-changing calls and summarize the intended action, target order or project, and likely account impact.

Risk: The skill uses an API key for authenticated requests.

Mitigation: Read OLLANG_API_KEY from the environment, avoid asking users to paste credentials into chat, and stop if the key is missing or appears misconfigured.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mazizulak/skills/ollang-skills)
- [Ollang website](https://ollang.com)
- [Ollang API documentation](https://api-docs.ollang.com)
- [Ollang API key portal](https://lab.ollang.com)
- [Ollang API status](https://status.ollang.com)
- [Ollang integration API base](https://api-integration.ollang.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with inline curl commands, tables, and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated operations require OLLANG_API_KEY; the health check endpoint is public.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
