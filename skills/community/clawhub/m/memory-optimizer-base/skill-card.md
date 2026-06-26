## Description: <br>
A multi-agent memory management skill that maintains private and public memory spaces, generates daily summaries, and supports cross-agent knowledge retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2720480371](https://clawhub.ai/user/2720480371) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to organize per-agent memory, summarize daily activity into medium-term records, publish selected summaries to a shared public memory area, and search shared knowledge across agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents in the same workspace may access another agent's private memory if they choose that agent ID. <br>
Mitigation: Use simple, controlled agent IDs, limit workspace access to trusted agents, and review private memory paths before enabling shared use. <br>
Risk: The release has review concerns around private-memory isolation, path scoping, and upload confirmation defaults. <br>
Mitigation: Before use, set upload.require_upload_confirm to true, keep memory.base_path scoped to the intended workspace, and manually review summaries before publishing them to public memory. <br>
Risk: Public memory uploads can make summarized private content visible to other agents. <br>
Mitigation: Keep upload.auto_publish disabled, require human confirmation, and inspect generated summaries for sensitive information before upload. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/2720480371/memory-optimizer-base) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line text with Markdown memory files and JSON configuration data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and searches local memory files under configured private and public workspace paths.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
