## Description:

iflow-nb helps agents manage iflow knowledge bases, import files and URLs, search web or academic sources, and generate reports, presentations, podcasts, mind maps, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflow-ai-skill](https://clawhub.ai/user/iflow-ai-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent organize iflow notebooks, import source material, search existing or external content, and generate knowledge-base outputs for research, documentation, and team sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided files, URLs, notes, and generated requests to iflow using a credentialed API key.

Mitigation: Use it only with content suitable for iflow processing, avoid secrets or regulated data, and store IFLOW_API_KEY with restrictive permissions.

Risk: The skill can share notebooks and perform delete or batch-delete actions against remote knowledge-base content.

Mitigation: Require explicit user confirmation before sharing links, imports, all-file generation, delete, or batch-delete actions.

Risk: Changing IFLOW_BASE_URL can redirect authenticated requests away from the default iflow endpoint.

Mitigation: Keep IFLOW_BASE_URL unset unless the target endpoint is fully trusted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iflow-ai-skill/skills/iflow-nb)
- [iflow API reference](references/api.md)
- [iflow API key management](https://platform.iflow.cn/profile?tab=apiKey)
- [iflow service](https://iflow.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create remote iflow knowledge-base records, share links, and generated files through authenticated iflow API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
