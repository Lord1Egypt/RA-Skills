## Description: <br>
IPO Model helps agents analyze tasks as recursive input-process-output structures and choose between direct reasoning and tool-assisted execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure writing, analysis, planning, coding, file operations, and tool-selection tasks with the IPO framework. It is most useful when an agent needs a repeatable way to decompose a broad request into inputs, processing steps, outputs, and optional tool use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad process-control guidance could influence an agent to modify files or handle private data without enough safeguards. <br>
Mitigation: Require explicit previews, approved directories, backups, and confirmation before changes. <br>
Risk: Tool-assisted IPO workflows may result in API calls or generated reports leaving the local environment. <br>
Mitigation: Require clear user consent before any API call or report is sent outside the local environment. <br>


## Reference(s): <br>
- [IPO Model on ClawHub](https://clawhub.ai/wangjiaocheng/ipo-model) <br>
- [IPO Model Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with optional code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include IPO trees when the user asks for expanded analysis; otherwise returns final results directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
