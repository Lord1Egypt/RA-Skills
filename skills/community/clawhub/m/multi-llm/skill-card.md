## Description: <br>
Queries multiple configured LLM providers in parallel and synthesizes their responses into a single higher-quality answer using a Mixture of Agents pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goodmorning0000](https://clawhub.ai/user/goodmorning0000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when complex reasoning, code review, research, strategic planning, or other high-stakes tasks benefit from comparing and synthesizing outputs across multiple LLM providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and model outputs may be sent to every configured provider. <br>
Mitigation: For confidential work, explicitly choose providers with --models, unset API keys for providers that should not receive data, or use local Ollama where appropriate. <br>
Risk: JSON logs or saved output files may contain private data, secrets, or full model responses. <br>
Mitigation: Avoid saving sensitive results unless needed, review output paths before writing, and handle generated files according to the user's data policy. <br>


## Reference(s): <br>
- [MoA (Mixture of Agents) Guide](references/moa-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/goodmorning0000/multi-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, guidance] <br>
**Output Format:** [Plain text or JSON; optionally saved to a user-specified output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output can include the final synthesis, synthesizer model, round count, and proposer responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
