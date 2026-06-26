## Description: <br>
Browse the web via Plasmate, a fast headless browser engine for agents that compiles HTML into a Semantic Object Model (SOM), supports AWP and CDP compatibility, and is optimized for lower-latency, lower-token web extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Builder-NC](https://clawhub.ai/user/Builder-NC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to navigate web pages, capture SOM snapshots, click or type into referenced elements, scroll pages, and extract structured web data through Plasmate's AWP helper or CDP-compatible server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing Plasmate or running its shell installer can execute code from the selected distribution channel. <br>
Mitigation: Install only from a trusted channel; prefer cargo install plasmate or inspect and verify the installer before running it. <br>
Risk: The Python helper may install the websockets package at runtime. <br>
Mitigation: Run the helper in a virtual environment or another controlled Python environment. <br>
Risk: The helper can start a local Plasmate automation server on port 9222 and leave it running. <br>
Mitigation: Check for and stop any Plasmate server that remains after use. <br>
Risk: Browser automation can click or type on sensitive websites. <br>
Mitigation: Require explicit confirmation before allowing click or type actions on sensitive sites. <br>


## Reference(s): <br>
- [Plasmate homepage](https://plasmate.app) <br>
- [Plasmate documentation](https://docs.plasmate.app) <br>
- [Plasmate source](https://github.com/plasmate-labs/plasmate) <br>
- [Plasmate privacy](https://plasmate.app/privacy) <br>
- [ClawHub skill page](https://clawhub.ai/Builder-NC/plasmate) <br>
- [Publisher profile](https://clawhub.ai/user/Builder-NC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python helper usage, JavaScript CDP examples, and JSON SOM outputs from Plasmate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the plasmate binary; the helper may install the Python websockets package and can start a local Plasmate server on port 9222.] <br>

## Skill Version(s): <br>
3.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
