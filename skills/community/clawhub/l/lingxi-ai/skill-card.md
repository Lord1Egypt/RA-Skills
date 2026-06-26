## Description: <br>
Lingxi is an OpenClaw-oriented AI orchestration skill for interpreting user intent, routing work across specialized agents and tools, managing task memory, and returning consolidated results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Scarlett](https://clawhub.ai/user/AI-Scarlett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Lingxi to route multi-channel requests through a multi-agent workflow, manage task memory and dashboard records, and coordinate content, code, search, translation, publishing, and analysis tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad autonomous orchestration can trigger publishing, messaging, GitHub, skill changes, or other account-linked actions. <br>
Mitigation: Require manual approval before publishing, messaging, pushing to GitHub, changing skills, or invoking account-linked tools. <br>
Risk: Dashboard access and external integrations depend on tokens or credentials that may be exposed through weak access controls or URL parameters. <br>
Mitigation: Keep the dashboard local unless strong access controls are added, avoid passing tokens in URLs, and use least-privilege credentials. <br>
Risk: Memories, task logs, and dashboard records may contain sensitive user data. <br>
Mitigation: Define retention and deletion rules before use and treat stored memories and logs as sensitive data. <br>
Risk: The release has unclear or inconsistent disclosure of scope and privacy boundaries. <br>
Mitigation: Review the skill and configuration carefully before installing and document enabled channels, credentials, storage locations, and network behavior. <br>


## Reference(s): <br>
- [Lingxi ClawHub listing](https://clawhub.ai/AI-Scarlett/lingxi-ai) <br>
- [Lingxi README](artifact/README.md) <br>
- [Acknowledgments and methodology notes](artifact/ACKNOWLEDGMENTS.md) <br>
- [Complex Task Three-Step Methodology](https://mp.weixin.qq.com/s/jnipYTffY_KSfWjqXbyqPQ) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate external tools, dashboards, account-linked services, and persistent memory depending on local configuration.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata; artifact frontmatter reports 3.3.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
