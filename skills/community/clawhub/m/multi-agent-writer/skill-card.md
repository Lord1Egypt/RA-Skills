## Description: <br>
Use when requests involve writing articles, generating news, fetching hotspots, or producing content for social media such as WeChat and Xiaohongshu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonelake](https://clawhub.ai/user/gonelake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a multi-agent writing workflow that gathers recent topics, drafts articles or social posts, and reviews the result before producing final content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer pulls mutable remote code and installs Python dependencies at install time. <br>
Mitigation: Review the cloned project and its dependencies before running production mode. <br>
Risk: The installer can register the skill across multiple local agent environments. <br>
Mitigation: Use an explicit --agent target instead of automatic or all-agent installation when limiting scope matters. <br>
Risk: Production mode may send user content to configured search or LLM providers. <br>
Mitigation: Use a dedicated LLM API key and avoid sending sensitive unpublished content to those providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gonelake/multi-agent-writer) <br>
- [Publisher profile](https://clawhub.ai/user/gonelake) <br>
- [External project repository referenced by artifact](https://github.com/gonelake/multi-agent) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI examples; generated writing outputs may be Markdown or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use demo mode without an API key or production mode with LLM configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
