## Description: <br>
Processes external resources into stored knowledge with quality scoring and routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to evaluate external articles, papers, and documentation, then route useful material into structured long-term knowledge stores. It also guides storage, validation, application to local projects or skill infrastructure, and pruning decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can make persistent local changes to code, skills, documentation, and the knowledge corpus. <br>
Mitigation: Review proposed paths and diffs before applying changes, and require explicit approval for pruning, archiving, deleting, or modifying stored knowledge. <br>
Risk: High-scoring entries default toward GitHub Discussions publication, which may expose private notes or sensitive research. <br>
Mitigation: Disable or gate the Discussion promotion workflow, confirm the target repository and category, and review the exact Discussion payload before publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-memory-palace-knowledge-intake) <br>
- [Claude Night Market Memory Palace Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [About the KonMari Method](https://konmari.com/about-the-konmari-method/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with structured entries, checklists, and inline code or shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent knowledge-corpus entries, proposed code or skill updates, local storage metadata, and optional GitHub Discussion payloads.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
