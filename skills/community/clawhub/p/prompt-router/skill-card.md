## Description: <br>
Prompt-Router routes user prompts to likely local skills using deterministic text matching, with low-confidence requests falling back to LLM routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiwell0721](https://clawhub.ai/user/aiwell0721) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route simple, high-frequency prompts to matching local skills quickly while sending ambiguous or complex prompts to LLM-based routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The router reads the local skills directory and can be used to auto-select skills. <br>
Mitigation: Install only where local skill discovery and routing are intended; keep confirmation or LLM fallback for low-confidence, sensitive, or destructive actions. <br>
Risk: Bundled metadata scripts can rewrite other installed skills' SKILL.md files. <br>
Mitigation: Do not run metadata rewrite scripts unless manifest changes are intended; review diffs or back up the skills directory first. <br>
Risk: Prompt logging, monitoring, or auto-PR workflows could expose user prompts or create unreviewed changes if enabled without controls. <br>
Mitigation: Disable those workflows unless explicit consent, redaction, retention limits, and credential controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiwell0721/prompt-router) <br>
- [Prompt-Router SKILL.md](artifact/SKILL.md) <br>
- [Prompt-Router README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell examples; command-line helper output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routing output may include matched skill name, skill path, confidence, score, and invocation or fallback decision.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
