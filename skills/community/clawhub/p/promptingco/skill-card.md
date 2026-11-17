## Description:

Interact with The Prompting Company platform to monitor brand visibility across AI engines, manage tracked prompts, review and publish content drafts, and retrieve SOV and AI traffic analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardtanoto](https://clawhub.ai/user/edwardtanoto)

### License/Terms of Use:


## Use Case:

External users and marketing teams use this skill to operate a Prompting Company workspace: selecting a brand, tracking prompts across AI engines, reviewing or publishing drafts, and retrieving share-of-voice and AI traffic analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a live browser session cookie that can access Prompting Company workspace data.

Mitigation: Use only a token for an account with the minimum necessary workspace permissions, avoid exposing the token in chat or logs, and rotate or revoke it after use.

Risk: Authenticated workflows can create prompts, approve items, create drafts, and publish live content.

Mitigation: Review selected brand, prompt, document, and publish actions before execution, and prefer saving drafts or submitting for review when publication is not intended.

Risk: The skill sends the session token into delegated multi-step workflows.

Mitigation: Run only in trusted agent environments and prefer a scoped API token if Prompting Company makes one available.

## Reference(s):

- [The Prompting Company API Quick Reference](artifact/references/api-guide.md)
- [Promptingco ClawHub Skill Page](https://clawhub.ai/edwardtanoto/skills/promptingco)
- [The Prompting Company App](https://app.promptingco.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with curl commands and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TPC_SESSION_TOKEN and can perform authenticated read and write actions in the user's Prompting Company workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
