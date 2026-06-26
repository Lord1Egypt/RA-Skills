## Description: <br>
Removes image backgrounds with Bria RMBG 2.0 and returns transparent PNG cutouts from local files or image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, designers, developers, and commerce teams use this skill to create transparent PNG cutouts, product images, headshot cutouts, and foreground extractions through Bria's background-removal API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to Bria's API for background removal. <br>
Mitigation: Use only images approved for third-party processing and confirm the Bria account terms before submitting sensitive content. <br>
Risk: Bria access tokens and API keys may be stored locally in plaintext at ~/.bria/credentials. <br>
Mitigation: Restrict local credential file permissions, delete credentials after use on shared systems, and rotate tokens if exposure is suspected. <br>
Risk: The bundled helper can call broader Bria API actions beyond background removal. <br>
Mitigation: Review or constrain the helper to the remove_background endpoint when deploying a background-removal-only workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/galbria/image-remove-background) <br>
- [Remove Background API Reference](references/api-endpoints.md) <br>
- [Shell Client](references/code-examples/bria_client.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash snippets, API result URLs, and optional downloaded PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bria authentication; selected images are sent to Bria's API and results are returned as transparent PNG URLs.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
