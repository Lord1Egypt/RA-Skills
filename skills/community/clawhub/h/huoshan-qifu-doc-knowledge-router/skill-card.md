## Description:

Routes Huoshan and Qifu knowledge requests through a structured Feishu document index and returns relevant original Feishu links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzj997](https://clawhub.ai/user/zzj997)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and knowledge workers use this skill to find, recommend, or verify Huoshan and Qifu Feishu documents from the default index while preserving source links and read status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the current user's Feishu access to read the default Huoshan/Qifu index and linked documents.

Mitigation: Install only for users who should search that workspace content, and rely on existing Feishu document ACLs for access control.

Risk: The trigger wording is broad and may activate for general Huoshan, Qifu, Feishu knowledge-base, onboarding, or document-recommendation requests.

Mitigation: Review and narrow the trigger wording if the skill should run only when explicitly named.

Risk: The default Wiki URL determines the routing source for normal requests.

Mitigation: Confirm that the configured Feishu Wiki index is appropriate for the target workspace before deployment.

## Reference(s):

- [Default Huoshan Qifu Feishu Wiki INDEX](https://bytedance.larkoffice.com/wiki/UOzdwymi8ibRgBko04bcX1yRnNh)
- [ClawHub skill page](https://clawhub.ai/zzj997/skills/huoshan-qifu-doc-knowledge-router)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Feishu links, read-status labels, and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one to three ranked links per requested topic when relevant evidence is available.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
