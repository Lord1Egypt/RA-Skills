## Description: <br>
Md Viewer helps an agent start a LAN-accessible, password-protected web viewer for local Markdown files, optimized for e-reader-friendly reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoangcongst](https://clawhub.ai/user/hoangcongst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill when they want to view a local Markdown file directly in a browser from a device on the same Wi-Fi network instead of receiving an agent summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown files may be reachable from other devices on the same local network when the server binds to a LAN address. <br>
Mitigation: Use --localhost on untrusted networks, share links only with intended readers, and stop the server when finished. <br>
Risk: Generated links, tokens, passwords, and authentication cookies can grant access to the viewer. <br>
Mitigation: Treat generated links and passwords as secrets and avoid placing them in shared logs, tickets, or chat channels. <br>
Risk: Viewed file paths are stored in local history by default. <br>
Mitigation: Use --no-history when path privacy matters. <br>
Risk: Sensitive Markdown documents could be exposed if a user chooses to serve them. <br>
Mitigation: Avoid serving sensitive documents and review the target path before sharing a viewer link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoangcongst/md-viewer) <br>
- [Python-Markdown](https://github.com/Python-Markdown/markdown) <br>
- [Bleach](https://github.com/mozilla/bleach) <br>
- [highlight.js](https://highlightjs.org/) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated LAN URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated URLs may include an access token and should be treated as secret.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and VERSION.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
