## Description: <br>
End-to-end brand marketing workflow that turns brand inputs into content assets, competitor analysis, performance scoring, and iteration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, content teams, and developers use this skill to generate brand briefs, multi-channel content plans, competitor signal analysis, performance reports, and next-step iteration plans from structured brand inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand and competitor data may be sent to configured LLM or search providers. <br>
Mitigation: Use only approved provider configurations and avoid submitting sensitive, confidential, or regulated brand data unless the provider is authorized for that data. <br>
Risk: The artifact includes local messaging-gateway capability that can use an OpenClaw gateway token for Telegram or Feishu messaging. <br>
Mitigation: Audit or remove gateway_client.py unless messaging is required, and restrict any gateway token to the minimum accounts and recipients needed. <br>
Risk: Bundled benchmark and demo evidence are not sufficient proof that the workflow is safe or accurate for every brand campaign. <br>
Mitigation: Review generated marketing recommendations, run the integration tests and representative brand scenarios, and keep human approval for publishing, payments, login gates, and captcha gates. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/halfmoon82/halfmoon82-brand-marketing-workflow) <br>
- [Publisher Profile](https://clawhub.ai/user/halfmoon82) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [ClawHub Manifest](artifact/clawhub.yaml) <br>
- [Integration Test Evidence](artifact/evidence/integration_test_result.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON workflow results with generated marketing text, markdown-style reports, configuration guidance, and command-line usage examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces brand briefs, content strategies, content assets, competitor clusters, performance scores, authorization status, browser compliance status, and iteration plans.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
