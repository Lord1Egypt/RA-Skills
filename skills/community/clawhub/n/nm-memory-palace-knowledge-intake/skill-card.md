## Description: <br>
Processes external resources into stored knowledge with quality scoring and routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to evaluate external articles, papers, documents, and session notes, then route worthwhile material into a structured knowledge corpus, project documentation, or proposed code and skill updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may publish summaries of internal knowledge to GitHub Discussions for high-scoring entries. <br>
Mitigation: Require explicit opt-in before each publication, review the target repository and post body, and remove local paths or private details from public summaries. <br>
Risk: The workflow may write persistent project files for knowledge-corpus entries and related documentation. <br>
Mitigation: Review proposed file paths and content before committing changes, especially when processing private or proprietary material. <br>
Risk: Externally sourced material may be routed into code, skill, module, or agent changes. <br>
Mitigation: Treat generated changes as proposals that require human review, testing, and security scanning before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-memory-palace-knowledge-intake) <br>
- [Metadata homepage: claude-night-market memory-palace](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [KonMari Method overview](https://konmari.com/about-the-konmari-method/) <br>
- [What is KonMari Method?](https://konmari.com/what-is-konmari-method/) <br>
- [Marie Kondo rules of tidying](https://konmari.com/marie-kondo-rules-of-tidying-sparks-joy/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with scoring tables, file paths, command examples, and proposed repository changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent knowledge-corpus files and GitHub Discussion summaries for qualifying entries unless declined.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
