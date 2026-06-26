## Description: <br>
Mem0 Memory Layer is a knowledge skill for LLM agents and chatbots that describes fact extraction, embedding, deduplication, storage, and hybrid retrieval across self-hosted Memory and hosted MemoryClient modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this knowledge skill to guide Mem0 long-term memory integrations for LLM agents and chatbots. The artifact set also contains finance and ZVT backtesting behavior, so users should review scope before running generated actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags a scope mismatch: the skill is advertised as a Mem0 memory helper, while authoritative artifacts also include finance, ZVT, and backtesting workflows. <br>
Mitigation: Review the artifacts for the intended purpose before use and do not install it as a normal Mem0 helper unless the publisher aligns the release to one clear scope. <br>
Risk: The artifact behavior can involve financial or broker credentials and generated finance/backtest code. <br>
Mitigation: Use an isolated workspace for testing, avoid real financial or broker credentials, and review generated code before executing it. <br>
Risk: The advertised Mem0 behavior can involve telemetry, retained memory, and sensitive stored data. <br>
Mitigation: Disable or control telemetry and memory retention, and avoid storing sensitive personal or regulated data unless appropriate controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/mem0-memory-layer) <br>
- [Doramagic crystal page](https://doramagic.ai/zh/crystal/mem0-memory-layer) <br>
- [Seed reference artifact](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local memory storage, telemetry settings, provider credentials, and finance/backtest workflows depending on the matched artifact content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
