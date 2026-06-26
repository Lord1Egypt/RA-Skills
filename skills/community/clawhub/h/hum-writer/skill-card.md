## Description: <br>
AI content writer that researches, outlines, drafts, publishes, and manages engagement for LinkedIn and X using the user's voice and style guidelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jyek](https://clawhub.ai/user/jyek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and operators use Hum to turn user-owned voice, audience, channel, and knowledge files into researched social posts, daily feed digests, and publication workflows for X and LinkedIn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive social credentials and X session cookies. <br>
Mitigation: Store tokens and cookies securely, grant only the access needed, and review configured credential files or environment variables before running connected workflows. <br>
Risk: Publishing, following, digest sending, analytics scraping, and image generation can create external side effects. <br>
Mitigation: Confirm the target account, recipient, content, platform, and image provider before running publish, engage, digest, analytics, or image generation commands. <br>
Risk: The server security guidance warns that the loop dry-run mode is unreliable until fixed. <br>
Mitigation: Do not rely on dry-run alone for the daily loop; review each planned action before allowing the loop to post, send, follow, or publish. <br>
Risk: The dashboard may be unsafe around untrusted web browsing. <br>
Mitigation: Run the dashboard only in a trusted local context and avoid combining it with untrusted browsing sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jyek/hum-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with JSON files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local content, feed, and configuration files, and can prepare or execute publishing and engagement actions when connected credentials are available.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and artifact/version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
