## Description:

Searches, recommends, and plays iQIYI video content through no-login search, recommendation, detail, qips playback/control, client-install, and H5 fallback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinkam](https://clawhub.ai/user/robinkam)

### License/Terms of Use:

Proprietary

## Use Case:

External users and developers use this skill to search iQIYI videos, request recommendations, inspect video or star details, generate playback/control deeplinks, check client installation paths, and fall back to H5 playback when the native client is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Authorization tokens can be exposed or sent outside the intended service.

Mitigation: Avoid passing Authorization tokens until request metadata is redacted, token output is prevented, and authenticated requests are restricted to the intended iQIYI HTTPS endpoint.

Risk: Live unauthenticated use sends search, recommendation, detail, or playback requests to iQIYI endpoints.

Mitigation: Use the no-login workflows for normal search and playback, and review privacy expectations before enabling authenticated history, favorites, or personalized flows.

Risk: qips deeplinks can launch or control the local iQIYI client.

Mitigation: Confirm the target action before execution, use only qips strings generated or validated by the skill, and reject dangerous third_play_url protocols.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robinkam/skills/iqiyi-skill)
- [Operation semantics](references/operations.md)
- [SOP](references/sop.md)
- [qips capabilities](docs/qips-capabilities.md)
- [qips API usage](references/qips/api-usage.md)
- [qips vtype recipes](references/qips/vtype-recipes.md)
- [qips channel table](references/qips/channel-table.md)
- [qips launch checklist](references/qips/launch-checklist.md)
- [iQIYI Feishu source wiki](https://iq.feishu.cn/wiki/WRmFw6W6bildBJkGTBnc1gtRnad)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional JSON API payloads, qips deeplinks, JavaScript examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use live iQIYI HTTPS requests or propose local qips:// client-launch commands; authenticated requests should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package/frontmatter metadata report 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
