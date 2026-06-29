## Description: <br>
Benchmark AI API models over time and detect quality degradation with a local CLI that runs standardized tests, stores score history, and alerts when recent scores drop against historical results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to benchmark model outputs across reasoning, coding, writing, instruction-following, and hallucination checks, then monitor local score history for degradation alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted model outputs may contain secrets, proprietary data, or other sensitive content. <br>
Mitigation: Review and redact model outputs before passing them to the CLI. <br>
Risk: Command-line JSON submissions can be captured in shell history or briefly visible to local process observers. <br>
Mitigation: Use sanitized inputs, avoid pasting sensitive outputs directly on shared systems, and clear shell history when needed. <br>
Risk: The benchmark uses keyword-style scoring, so results can miss qualitative issues or overstate quality for responses that match expected terms. <br>
Mitigation: Treat score trends as a lightweight signal and review sampled model outputs before making deployment or purchasing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/model-watch) <br>
- [Project homepage from metadata](https://github.com/minirr890112-byte/model-watch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI writes local score history to ~/.hermes/model-watch-history.json and reports trend and alert summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version; artifact frontmatter reports 1.2.0 and pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
