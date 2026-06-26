## Description: <br>
Token-safe prompt assembly with memory orchestration for agents that construct LLM prompts with memory retrieval, using two-phase context construction, a memory safety valve, and hard limits on memory injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexunitario-sketch](https://clawhub.ai/user/alexunitario-sketch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to assemble prompts that combine system instructions, recent dialog, current user input, and optional retrieved memories while staying within a token budget. It is intended for agents that need memory retrieval without making memory a hard dependency for prompt construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token estimates are heuristic and may differ from the tokenizer used by the target model. <br>
Mitigation: Test estimates against the actual model and tokenizer before relying on the safety threshold in production. <br>
Risk: Memory retrieval can introduce sensitive or stale user data into prompts. <br>
Mitigation: Use memory stores with user consent, review, deletion controls, and limits on sensitive data. <br>
Risk: The artifact describes strong overflow guarantees even though the implementation depends on configuration and estimation quality. <br>
Mitigation: Treat the helper as a conservative prompt assembly pattern and validate limits for each deployment. <br>


## Reference(s): <br>
- [Memory Data Standards](references/memory_standards.md) <br>
- [Token Estimation Strategies](references/token_estimation.md) <br>
- [Prompt Safe on ClawHub](https://clawhub.ai/alexunitario-sketch/prompt-assemble) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples; the bundled script returns assembled prompt strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable token limits, safety margin, memory retrieval count, and memory summary length.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
