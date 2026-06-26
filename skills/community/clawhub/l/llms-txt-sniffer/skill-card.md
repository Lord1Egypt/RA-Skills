## Description: <br>
Locate and utilize AI-friendly documentation index files (llms.txt, llms-full.txt) or sitemap.xml when encountering documentation URLs to map sites quickly and reduce token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdchi](https://clawhub.ai/user/jdchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they provide a documentation URL and want the agent to locate llms.txt, llms-full.txt, or sitemap.xml before reading site documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound requests to user-provided documentation URLs, including direct curl probes documented in the skill instructions. <br>
Mitigation: Use it only for documentation URLs intentionally provided by the user, and avoid localhost, internal network, cloud metadata, or other sensitive private URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jdchi/llms-txt-sniffer) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON snippets from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and curl; the helper script returns JSON describing the target URL, discovered index URL, index type, and optional preview or error.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
