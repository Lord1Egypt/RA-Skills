## Description: <br>
Automatically adds index entries for MEMORY.md and memory/ files, with tag classification and key decision tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengnessly](https://clawhub.ai/user/mengnessly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep local memory files discoverable by adding index entries, tags, and decision references after important memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated indexing can modify MEMORY.md and files under memory/. <br>
Mitigation: Review scripts before use and prefer preview or confirmation before automated writes. <br>
Risk: Subjects or tags passed to shell commands could be unsafe if they contain untrusted input. <br>
Mitigation: Sanitize subjects and tags before invoking local shell scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mengnessly/memory-auto-index) <br>
- [Publisher Profile](https://clawhub.ai/user/mengnessly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces indexing conventions, script invocation patterns, tag guidance, and maintenance checks for local memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
