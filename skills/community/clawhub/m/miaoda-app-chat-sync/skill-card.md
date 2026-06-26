## Description: <br>
Convert Git repository code to structured JSON instructions for AI agents, including repository fetching, file filtering, and code synchronization outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoanso](https://clawhub.ai/user/xiaoanso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to convert trusted Git repositories into structured JSON instructions for downstream AI agents to inspect, synchronize, or recreate code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive GitHub credentials for private repository access. <br>
Mitigation: Use a read-only, repository-scoped token, keep it in the environment, and verify the publisher, package identifier, and version before use. <br>
Risk: Generated JSON may be interpreted by downstream agents as authoritative file overwrite instructions. <br>
Mitigation: Review file lists, action fields, rules, and file contents before sending JSON to another agent, and require a diff or backup before bulk overwrites. <br>
Risk: Repository content or crafted repository URLs can influence generated instructions. <br>
Mitigation: Use trusted repository URLs, pin commits for reproducibility, and treat repository contents as data rather than instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoanso/miaoda-app-chat-sync) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [PROMPTS.md](PROMPTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured JSON with CLI summaries and optional markdown-style instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and git; may use GITHUB_TOKEN for private repositories; generated JSON can include repository file contents and overwrite instructions for downstream agents.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release evidence; CHANGELOG.md released 2026-04-30; _meta.json reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
