## Description: <br>
Postnify helps agents schedule, manage, and analyze social media and chat posts across more than 28 connected channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[postnifyhq](https://clawhub.ai/user/postnifyhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Postnify to operate authenticated social media workflows: discover integrations, upload media, create or schedule posts, manage drafts, and inspect platform or post analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Postnify-connected social accounts and create, schedule, delete, or change posts. <br>
Mitigation: Require explicit user confirmation before creating, scheduling, deleting, or changing post status. <br>
Risk: The skill depends on sensitive OAuth credentials or API keys, including credentials stored under ~/.postnify/credentials.json. <br>
Mitigation: Prefer OAuth or scoped API keys, protect local credential storage, and avoid exposing POSTNIFY_API_KEY in logs or shared shell history. <br>
Risk: A custom POSTNIFY_API_URL can redirect commands to an untrusted service. <br>
Mitigation: Use the default Postnify API endpoint unless the user explicitly verifies a trusted alternative. <br>


## Reference(s): <br>
- [ClawHub Postnify Skill Page](https://clawhub.ai/postnifyhq/postnify) <br>
- [Postnify Website](https://postnify.com) <br>
- [Postnify npm Package](https://www.npmjs.com/package/postnify) <br>
- [Postnify API Endpoint](https://platform.postnify.com/api) <br>
- [Postnify CLI Auth Endpoint](https://cli-auth.postnify.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the postnify CLI, authenticated Postnify credentials, and configured social or chat integrations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
