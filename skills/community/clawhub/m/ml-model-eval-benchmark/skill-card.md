## Description: <br>
Compare model candidates using weighted metrics and deterministic ranking outputs. Use for benchmark leaderboards and model promotion decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and evaluation engineers use this skill to rank model candidates from weighted metrics, produce benchmark leaderboards, and support model promotion decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark inputs or generated artifacts may contain sensitive evaluation data. <br>
Mitigation: Use non-sensitive or approved evaluation data where possible and review generated JSON, Markdown, or CSV artifacts before sharing. <br>
Risk: The benchmark script writes to the output path supplied by the user. <br>
Mitigation: Review the output path before running the script and write artifacts to an intended project or scratch directory. <br>
Risk: Large or repeated benchmark runs may consume local compute or storage. <br>
Mitigation: Keep inputs scoped to the benchmark need, use the script's bounded input behavior, and monitor generated artifact size. <br>


## Reference(s): <br>
- [Benchmarking Guide](artifact/references/benchmarking-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/0x-Professor/ml-model-eval-benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON, Markdown, or CSV benchmark artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records metric weights, ranked model candidates, recommended model, and dry-run status when using the bundled benchmark script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
