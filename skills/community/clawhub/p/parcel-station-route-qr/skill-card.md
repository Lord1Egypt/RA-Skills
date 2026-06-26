## Description: <br>
Add shelf route guidance and QR code scanning to a parcel station chatbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining a parcel-station chatbot use this skill to add shelf-location route guidance, QR scanning, and optional local HTTPS support for camera access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an unrelated Notion sync script that reads local credentials and sends data to Notion without being disclosed in the skill description. <br>
Mitigation: Remove the script before installation, or document exactly which credentials it reads and what data it sends before running it. <br>
Risk: The QR workflow can automatically send decoded QR content into the chatbot. <br>
Mitigation: Add a confirmation step so users can inspect decoded content before it is submitted. <br>
Risk: The optional self-signed HTTPS setup can train users to bypass browser certificate warnings. <br>
Mitigation: Use self-signed certificates only for local development on a trusted network, and use trusted certificates for production deployments. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [Self-signed certificate helper](artifact/references/gen-cert.js) <br>
- [jsQR local library bundle](artifact/references/jsqr.min.js) <br>
- [jsQR CDN source](https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes route-guide logic, QR scanner integration notes, and optional HTTPS certificate setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
