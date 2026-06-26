## Description: <br>
Service marketplace: publish data as services, consume hub services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangboheng](https://clawhub.ai/user/tangboheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish local data or capabilities as hub services and to discover or call those services from other agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local files, network fetches, and long-running service methods to other agents without clear default boundaries. <br>
Mitigation: Install only when the hub endpoint and participating agents are trusted; keep HUB_WS_URL pointed at a trusted local or controlled server. <br>
Risk: Provider methods may expose sensitive directories or arbitrary URL fetchers. <br>
Mitigation: Avoid exposing sensitive directories, add allowlists and path normalization, require authorization for provider methods, log calls, and stop provider services when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangboheng/hub-client) <br>
- [Project homepage](https://github.com/TangBoheng/Claw-Service-Hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, pip, HUB_WS_URL, and the websockets and aiohttp packages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
