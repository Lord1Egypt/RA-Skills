## Description: <br>
OpenClaw Smartness Eval evaluates an OpenClaw agent across 14 intelligence dimensions and produces scores, evidence, risk flags, recommendations, and trend reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yh22e](https://clawhub.ai/user/yh22e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run quick, standard, or deep evaluations of OpenClaw workspaces after upgrades or during recurring capability audits. It combines scoped test commands, runtime state, scoring rubrics, and trend comparison into reproducible agent intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local state files and generated reports may contain sensitive prompts, operational data, scores, evidence metrics, or risk flags. <br>
Mitigation: Install only in a trusted OpenClaw workspace, review or redact local state before evaluation, and keep generated reports private unless they are safe to share. <br>
Risk: The optional LLM judge can send score summaries, evidence metrics, and risk flags to the configured LLM provider. <br>
Mitigation: Use --llm-judge only with an approved provider and configured API key, and only when sending those summaries is acceptable. <br>
Risk: Evaluation runs execute scoped workspace test commands. <br>
Mitigation: Rely on the command whitelist and review task-suite changes before running the skill in a workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yh22e/openclaw-smartness-eval) <br>
- [Project Repository](https://github.com/xyva-yuangui/smartness-eval) <br>
- [Architecture Documentation](docs/ARCHITECTURE.md) <br>
- [Scoring Formulas](docs/SCORING.md) <br>
- [Security Policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON run files, Markdown reports, JSONL history records, and optional stdout in JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes evaluation artifacts under state/smartness-eval/ and can include optional LLM judge summaries only when explicitly enabled.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
