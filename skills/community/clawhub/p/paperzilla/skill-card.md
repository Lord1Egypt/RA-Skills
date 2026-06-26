## Description: <br>
Use the Paperzilla CLI (pz) to browse research projects and feeds, inspect canonical papers and project recommendations, leave feedback, export JSON, and generate Atom feed URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pors](https://clawhub.ai/user/pors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to operate Paperzilla from an agent session: browsing project feeds, inspecting canonical papers and project-specific recommendations, exporting structured JSON, and managing recommendation feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to authenticate with Paperzilla and run project-specific feedback commands. <br>
Mitigation: Use the intended account only and require confirmation before running `pz feedback` commands. <br>
Risk: `pz feed ... --atom` can expose a personal feed URL. <br>
Mitigation: Treat Atom feed URLs like secrets and avoid sharing them outside trusted contexts. <br>
Risk: The skill depends on an external `pz` binary and Paperzilla service behavior. <br>
Mitigation: Install the CLI only from trusted Paperzilla sources and verify commands before execution. <br>


## Reference(s): <br>
- [Paperzilla CLI documentation](https://docs.paperzilla.ai/guides/cli) <br>
- [Paperzilla CLI quickstart](https://docs.paperzilla.ai/guides/cli-getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to prefer --json for structured Paperzilla CLI output.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
