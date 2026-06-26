## Description: <br>
Query Multisage for synthesized multi-expert answers from Claude, GPT, and Gemini. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waleedkadous](https://clawhub.ai/user/waleedkadous) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when they want an agent to consult Multisage for multiple AI perspectives, synthesized answers, or deeper research on a prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to Multisage and downstream AI providers. <br>
Mitigation: Use the skill only with content intended for external processing; avoid secrets, private code, regulated data, or other sensitive material. <br>
Risk: API key setup may look through local environment files for MULTISAGE_API_KEY. <br>
Mitigation: Configure the key through deliberate secret handling and avoid printing, copying, or sharing .env file contents. <br>
Risk: Deep research mode can spend additional credits and run for several minutes. <br>
Mitigation: Use deep research only when the user explicitly wants a higher-cost, longer-running query, and check or cancel outstanding threads when needed. <br>


## Reference(s): <br>
- [ClawHub Multisage page](https://clawhub.ai/waleedkadous/multisage) <br>
- [Multisage API key settings](https://multisage.ai/settings) <br>
- [Multisage pricing](https://multisage.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional CLI JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Standard queries consume 1 credit; deep research consumes 5 credits, may take 5-25 minutes, and prompts are documented as truncated to 1000 characters.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
