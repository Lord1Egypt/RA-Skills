## Description: <br>
Write full-length technical books using multi-agent AI orchestration, with parallel research, writing, and review agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical authors, and engineering teams use this skill to plan, draft, review, integrate, and polish long-form technical books from a topic or source repository. It is also intended for revising individual chapters while preserving the broader manuscript workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run for a long time while reading repositories, writing many files, spawning subagents, and calling external AI or research services. <br>
Mitigation: Run it in a clean working directory with an explicit budget and review each phase checkpoint before continuing. <br>
Risk: The workflow may access provider keys or work with private and sensitive repositories. <br>
Mitigation: Use only approved repositories and credentials, avoid exporting secrets, and confirm any external-service use before sending content outside the workspace. <br>
Risk: The workflow may overwrite chapters, create pull requests, merge changes, push to git, or publish generated material. <br>
Mitigation: Review remotes, diffs, and generated manuscripts before any destructive file update, merge, push, or publishing action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/git-repo-to-book) <br>
- [Publisher Profile](https://clawhub.ai/user/chunhualiao) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Reference Implementation: openclaw-paradigm-book](https://github.com/chunhualiao/openclaw-paradigm-book) <br>
- [DeepWiki API](https://api.deepwiki.com/v1/chat) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown manuscripts, JSON metadata, project files, and optional HTML export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces chapter files, research notes, review notes, merged manuscripts, metadata, and optional HTML output for agent-driven book projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
