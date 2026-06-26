## Description: <br>
Build and maintain a personal knowledge Wiki using the LLM Wiki pattern with OpenClaw-optimized step-by-step execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayxjw](https://clawhub.ai/user/jayxjw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and maintain a local Obsidian-style personal knowledge base from raw documents, notes, PDFs, and Word files. It organizes sources, extracts entities and concepts, creates wiki pages, updates indexes, and supports queries over the maintained wiki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically process local files and write persistent notes. <br>
Mitigation: Use a dedicated ~/Obsidian Wiki folder, place only intended files in raw, review generated notes, and keep backups. <br>
Risk: The skill may run on a schedule and continue maintaining the wiki without per-file prompts. <br>
Mitigation: Review cron scheduling before enabling it and disable scheduled runs when autonomous maintenance is not desired. <br>
Risk: The skill can install Python packages for PDF and Word document support. <br>
Mitigation: Approve Python or pip installation only in an isolated environment when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jayxjw/obsidian-wiki-auto) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown wiki pages, JSON-like sub-agent task results, and setup or scheduling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local wiki folders, source summaries, entity pages, concept pages, index files, and logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
