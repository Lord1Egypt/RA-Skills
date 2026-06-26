## Description: <br>
Kannaka Eye runs a local Node.js glyph viewer that classifies text, files, or raw bytes into SGA classes and renders multi-layer Fano-plane visualizations, with optional native classifier, radio bridge, health dashboard, share link, and export features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickFlach](https://clawhub.ai/user/NickFlach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to launch a local visualization service for inspecting geometric glyphs derived from text, files, raw bytes, and optional audio perception data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The launcher may run a server.js file outside the reviewed package. <br>
Mitigation: Inspect the exact server.js path before running and ask the publisher to include the intended server file inside the reviewed skill package. <br>
Risk: Flux publishing can send glyph render event data to a remote endpoint when FLUX_URL is set. <br>
Mitigation: Leave FLUX_URL unset unless the destination is trusted and expected for the deployment. <br>
Risk: The local viewer is documented for local or trusted-network use and does not describe authentication. <br>
Mitigation: Bind and expose the service only in trusted environments, avoid sensitive inputs during review, and stop the background process after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NickFlach/kannaka-eye) <br>
- [Publisher profile](https://clawhub.ai/user/NickFlach) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and local service outputs including glyph JSON, PNG exports, share links, and status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local HTTP viewer; optional remote Flux publishing is enabled only when FLUX_URL is set.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
