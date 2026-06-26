## Description: <br>
AgentMail (agentmail.to) lets agents read, create, update, and delete AgentMail data through OOMOL's AgentMail connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent read, search, draft, send, label, and administer AgentMail resources through an OOMOL-connected account. It supports mail workflows as well as account resources such as inboxes, pods, domains, webhooks, metrics, API keys, and allow or block lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or remove real AgentMail resources, including mail, drafts, inboxes, domains, webhooks, API keys, and allow or block lists. <br>
Mitigation: Review the exact action name, target resource, and JSON payload before approving any write, send, API-key, webhook, domain, inbox, or delete operation. <br>
Risk: The skill requires a trusted OOMOL-connected account with sensitive AgentMail access. <br>
Mitigation: Install and use the skill only when the OOMOL publisher and connected AgentMail account are trusted for the intended mail-management tasks. <br>
Risk: Incorrect payloads could affect unintended AgentMail resources. <br>
Mitigation: Inspect the live connector schema before each action and match payloads to the authoritative input fields. <br>


## Reference(s): <br>
- [ClawHub AgentMail skill page](https://clawhub.ai/oomol/oo-agent-mail) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [AgentMail homepage](https://agentmail.to) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions return JSON responses from the oo connector when run with --json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
