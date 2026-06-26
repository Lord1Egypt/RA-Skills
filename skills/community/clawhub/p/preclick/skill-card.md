## Description: <br>
Companion skill for @cybrlab/preclick-openclaw. Requires PreClick plugin tools to assess URLs for threats and intent alignment before navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cplusdev](https://clawhub.ai/user/cplusdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill before opening, downloading from, or otherwise acting on URLs so they can check for threat signals and whether the destination appears aligned with the user's stated intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL scans depend on a separate PreClick plugin and may expose sensitive URLs or embedded tokens to that scanner. <br>
Mitigation: Install only if you trust the PreClick plugin, review its permissions and network behavior, and avoid scanning links that contain private tokens, account identifiers, or sensitive internal URLs. <br>
Risk: Scan results can be incomplete or unavailable, and a low-risk result is not a guarantee that a destination is safe. <br>
Mitigation: Follow the returned access directive, retry temporary failures once, and use confidence-aware language when reporting results to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cplusdev/preclick) <br>
- [Publisher profile](https://clawhub.ai/user/cplusdev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline tool names and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to call PreClick plugin tools, interpret directives, and report results without guaranteeing safety.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
