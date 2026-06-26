## Description: <br>
Use this skill to create, edit, read, and export Google Slides presentations through authenticated gogcli MCP Slides tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an authenticated Google account to Google Slides workflows, including creating decks, reading slides, updating speaker notes, replacing slide images, and exporting presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Slides tools can read, export, modify, and delete presentation content. <br>
Mitigation: Install only when the npm package and configured Google account scope are trusted, and review presentation changes before relying on them. <br>
Risk: The generic run tool can extend beyond the listed Slides actions. <br>
Mitigation: Use the generic run tool only with explicit user direction and careful review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gogcli-mcp-slides) <br>
- [gogcli project](https://github.com/openclaw/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration snippets, and tool-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated MCP tool use that reads, modifies, exports, or deletes Google Slides presentation content.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
