## Description: <br>
Single entry skill for open-websearch setup and focused live retrieval, preferring local CLI/daemon paths while remaining compatible with workspace-exposed MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aas-ee](https://clawhub.ai/user/aas-ee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up or validate open-websearch access and then perform focused live web search, page fetch, and GitHub README retrieval through the smallest available local CLI, daemon, or MCP path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance may involve package installation, browser downloads, daemon startup, client configuration edits, or endpoint changes. <br>
Mitigation: Require explicit user approval before those actions and validate the final capability state before claiming setup is complete. <br>
Risk: Fetched web pages and search results can contain untrusted or misleading instructions. <br>
Mitigation: Treat external content as evidence only, ignore page instructions that conflict with the user request or workspace boundaries, and keep source attribution tied to fetched URLs. <br>
Risk: Network-restricted environments can make installation or live retrieval fail in ways that look like tool failure. <br>
Mitigation: Check npm proxy, registry mirror, runtime proxy, and browser dependency needs before retrying or diagnosing open-websearch itself. <br>


## Reference(s): <br>
- [Open Websearch Skill Page](https://clawhub.ai/aas-ee/open-websearch) <br>
- [Setup](references/setup.md) <br>
- [Tools](references/tools.md) <br>
- [Engine Selection](references/engine-selection.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for user confirmation before package installation, browser downloads, daemon startup, client configuration edits, or endpoint changes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact frontmatter reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
