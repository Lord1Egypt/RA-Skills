## Description: <br>
Perform Google searches and retrieve web or news results via Chrome browser running in WSL using remote debugging with OpenClaw tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesson-hh](https://clawhub.ai/user/jesson-hh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to launch or connect to a Chrome instance in WSL for Google search, news lookup, and web research through the OpenClaw browser tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome remote debugging on port 9222 can expose browser state while the debug session is running. <br>
Mitigation: Close Chrome or stop access to port 9222 when finished, and use the dedicated debug profile rather than important signed-in browser profiles. <br>
Risk: Searches may use zh-CN language settings by default, which can influence result localization. <br>
Mitigation: Set GOOGLE_SEARCH_LANG to the preferred locale before launching Chrome. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jesson-hh/google-search-wsl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and browser-tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for WSL Chrome remote debugging; no credential inputs are required by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
