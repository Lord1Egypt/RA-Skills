## Description: <br>
Moore Pyramid Memory System provides a five-layer local memory pattern for cross-session continuity, including startup-loaded memory files, daily summaries, archives, and a persistent todo list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tosspi](https://clawhub.ai/user/tosspi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to guide an agent in maintaining local, cross-session project memory through structured memory files, summaries, archives, and todos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to automatically save and reload conversation-derived memory across sessions, which can retain sensitive details without clear user controls. <br>
Mitigation: Before using it for sensitive work, confirm where memory files are stored, review and delete retained content as needed, and require consent before saving conversation details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tosspi/moore-pyramid-memory-system) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with file paths, tables, and example markdown snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may cause an agent to create or update local memory files and scheduled archive scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
