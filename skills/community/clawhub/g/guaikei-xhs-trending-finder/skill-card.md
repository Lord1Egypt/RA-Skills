## Description:

Finds public Xiaohongshu notes, note details, comments, and creator posts for keyword research, trend monitoring, competitive analysis, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content creators, and data analysts use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator post data for trend analysis, content planning, competitive monitoring, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and Xiaohongshu links are sent to a third-party service.

Mitigation: Use the skill only for public Xiaohongshu data the user is authorized to process, confirm third-party data handling is acceptable, and protect or rotate GUAIKEI_API_TOKEN if exposed.

Risk: Retrieved data is automatically saved locally without redaction.

Mitigation: Periodically review, secure, or delete the generated logs directory, especially when links or retrieved content may be sensitive.

Risk: Security evidence marks the release as suspicious.

Mitigation: Review the skill before installing or deploying it, and apply the security guidance from the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-trending-finder)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON results with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save retrieved results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
