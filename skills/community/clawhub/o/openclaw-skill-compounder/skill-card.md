## Description: <br>
A multi-skill orchestrator that chains independent skills into automated compound workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-long-2022](https://clawhub.ai/user/jack-long-2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to classify a user goal, select a matching multi-skill template, and generate a step-by-step call chain for content creation, research, media analysis, investment analysis, knowledge management, or skill improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chains can trigger downstream publishing, portfolio updates, or persistent knowledge-base changes without consistently requiring clear final approval. <br>
Mitigation: Review every generated chain before it runs and require explicit manual approval before publishing, updating portfolio records, writing wiki indexes or concept graphs, using logged-in scraping, or applying generated skill changes. <br>
Risk: The workflow relies on downstream skills and accounts whose behavior and permissions are outside this skill's direct control. <br>
Mitigation: Verify each downstream skill, connected account, and permission before execution; keep auto_publish and update_portfolio disabled by default. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-long-2022/openclaw-skill-compounder) <br>
- [CHAIN.md](artifact/CHAIN.md) <br>
- [REGISTRY.md](artifact/REGISTRY.md) <br>
- [Pipeline templates](artifact/TEMPLATES/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and YAML-style workflow definitions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates ordered skill chains, input mappings, fallback handling, and validation guidance for downstream execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
