## Description: <br>
Provides Chuck Norris jokes by random selection, category, or keyword search from chucknorris.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Chuck Norris jokes, search jokes by keyword, list categories, and configure an MCP endpoint for joke retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Joke results may include explicit or offensive content. <br>
Mitigation: Review outputs before sharing or using them in environments where humor or explicit categories may be inappropriate. <br>
Risk: Search keywords and joke requests are sent to a third-party gateway. <br>
Mitigation: Do not submit secrets, private text, or sensitive identifiers as search terms or tool arguments. <br>
Risk: The optional MCP setup runs mcp-remote through npx. <br>
Mitigation: Use the MCP configuration only in trusted Node and npm environments, and pin or review dependencies when required by local policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-chucknorris) <br>
- [Pipeworx Chuck Norris pack](https://pipeworx.io/packs/chucknorris) <br>
- [Pipeworx Chuck Norris MCP endpoint](https://gateway.pipeworx.io/chucknorris/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct examples; optional MCP setup uses npx mcp-remote and the Pipeworx gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
