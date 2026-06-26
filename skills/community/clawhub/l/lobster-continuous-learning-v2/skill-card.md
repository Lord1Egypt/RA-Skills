## Description: <br>
Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills, commands, and agents with project-scoped isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to capture local session activity, derive project-scoped behavioral patterns, and manage learned instincts that can evolve into reusable skills, commands, or agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claude Code activity may be broadly recorded into local observation files. <br>
Mitigation: Install only when local activity recording is intended, avoid sensitive repositories, narrow hook matchers where possible, and regularly review or delete local observations and registries. <br>
Risk: The background observer can write learned behavior files without per-action review. <br>
Mitigation: Keep observer.enabled false unless background analysis and automatic instinct-file writes are acceptable, then review generated instincts before relying on, exporting, or promoting them. <br>
Risk: Exported or promoted instincts may carry patterns learned from private or sensitive work. <br>
Mitigation: Review generated instincts, evolved outputs, logs, and registries before export or promotion, and remove sensitive or project-specific details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/lobster-continuous-learning-v2) <br>
- [ECC-Tools GitHub App](https://github.com/apps/ecc-tools) <br>
- [Continuous learning longform guide](https://x.com/affaanmustafa/status/2014040193557471352) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, JSON configuration, JSONL observations, YAML or Markdown instinct files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local observations, instincts, evolved skills, commands, agents, logs, and project registries under ~/.claude/homunculus when hooks or the observer are enabled.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
