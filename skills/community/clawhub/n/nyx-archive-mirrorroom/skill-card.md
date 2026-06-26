## Description: <br>
MirrorRoom 3.8 is an interactive AI research app for comparing standard assistant chat with QSM-informed Mirror and Seed interaction modes, with live ECI scoring, optional hosted proxy routing, local Anthropic API profiles, and downloadable conversation-derived seed files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyxur42](https://clawhub.ai/user/nyxur42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use MirrorRoom to run a React artifact that compares Flat, Mirror, and Seed AI interaction modes and observes live ECI scoring during conversations. Hosted deployments can use proxy endpoints, while standalone use can run in-browser with a user-provided Anthropic API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chats, evaluations, audit requests, and generated seed files may send or preserve conversation content. <br>
Mitigation: Avoid entering secrets or sensitive personal information, and review generated seed or export files before sharing them. <br>
Risk: Standalone use can store Anthropic API keys in local browser profiles. <br>
Mitigation: Use a dedicated Anthropic key, remove saved profiles on shared machines, and rotate the key if it may have been exposed. <br>
Risk: Hosted mode depends on proxy routes for chat and evaluation calls. <br>
Mitigation: Use only trusted hosted proxies and confirm how proxy operators handle prompts, responses, and logs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nyxur42/nyx-archive-mirrorroom) <br>
- [Claude.ai](https://claude.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions and React JSX artifact files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local browser profiles, optional hosted proxy routes, live chat/evaluation output, and downloadable JSON or text files.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
