## Description: <br>
Install or repair Hirey Hi on a local OpenClaw host, including MCP wiring, local receiver setup, registration, health checks, and welcome onboarding for people-search listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlee](https://clawhub.ai/user/yzlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to install or repair Hirey Hi so the host can publish people-search listings, find matches, contact people, and coordinate follow-up across hiring, housing, friendship, dating, founder, investor, legal, or other human lead workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes persistent local OpenClaw hook and MCP configuration changes. <br>
Mitigation: Install only when the user trusts Hirey Hi to modify the local OpenClaw host, and review OpenClaw approval prompts before continuing. <br>
Risk: The integration stores a local receiver token and binds the current chat for future replies. <br>
Mitigation: Use the documented cleanup flow if the user no longer wants the Hi integration or reply routing on this host. <br>
Risk: The installed integration can exchange people-search and listing data with Hirey's default service. <br>
Mitigation: Share only data appropriate for Hirey Hi workflows and confirm listings before publishing or updating them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzlee/openclaw-hi-install) <br>
- [Hirey Hi default service](http://hi.hireyapp.us) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON status output, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation steps and local host configuration guidance; it may invoke OpenClaw and bundled installer commands when used by an agent.] <br>

## Skill Version(s): <br>
0.1.56 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
