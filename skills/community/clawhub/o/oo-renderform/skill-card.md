## Description: <br>
RenderForm helps an agent operate RenderForm through the OOMOL-connected oo CLI for template lookup, usage checks, result and template listing, image or PDF rendering, and website screenshot capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to work with RenderForm templates, generated results, usage information, rendered images or PDFs, and website screenshots through an authenticated OOMOL connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance includes running an unverified remote installer script. <br>
Mitigation: Install only if OOMOL is trusted; download and review the installer and verify an official checksum or signed release before running it. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected RenderForm account. <br>
Mitigation: Use a least-privilege RenderForm API key, keep credentials in the OOMOL connection flow, and rotate or revoke access if the connection is no longer needed. <br>
Risk: Rendering images, PDFs, or screenshots can consume RenderForm credits or create externally hosted output files. <br>
Mitigation: Confirm payloads for state-changing or credit-consuming actions and monitor usage before large batches. <br>


## Reference(s): <br>
- [RenderForm ClawHub listing](https://clawhub.ai/oomol/oo-renderform) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [RenderForm homepage](https://renderform.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return RenderForm request identifiers, file URLs, echoed request data, template details, usage summaries, result lists, or screenshot outputs through connector responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
