## Description: <br>
Helps agents register generated local files and return mobile-accessible OCC/Tailscale artifact viewer links instead of filesystem paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadoprizm](https://clawhub.ai/user/shadoprizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when generated files need to be shared through mobile or chat channels as stable viewer and download links rather than local filesystem paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Viewer and download links may expose registered generated outputs to anyone with access to the link or gallery network. <br>
Mitigation: Register only intended files, avoid private or secret-bearing content, and verify gallery access controls before sharing links. <br>
Risk: Registration can fail when paths are outside allowlisted roots or look credential-related. <br>
Mitigation: Do not invent URLs or bypass gallery checks; fix the path or root, or report the failure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shadoprizm/occ-artifact-gallery) <br>
- [OCC Artifact Gallery UI](https://n2-pro.tail1c2e65.ts.net/artifacts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with viewer_url and optional download_url fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include artifact type and size when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
