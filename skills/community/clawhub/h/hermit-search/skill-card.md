## Description: <br>
Local semantic search over knowledge base collections powered by Hermit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxgqcoder](https://clawhub.ai/user/xxxgqcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to install and operate Hermit for local semantic search across selected knowledge base folders, including collection management, indexing, querying, and service lifecycle tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad folders can place private or sensitive files into local search collections. <br>
Mitigation: Index narrow, dedicated folders and configure ignore rules for secrets, private files, generated files, and irrelevant file types. <br>
Risk: The workflow depends on installing and running the upstream Hermit tool and a local service. <br>
Mitigation: Install only when the upstream Hermit project is trusted, review the configured collections before use, and stop the local service when work is complete. <br>


## Reference(s): <br>
- [Hermit project homepage](https://github.com/xxxgqcoder/hermit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hermit commands documented by the skill return JSON when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
