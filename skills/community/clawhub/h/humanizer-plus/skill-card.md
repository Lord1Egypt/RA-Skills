## Description: <br>
Rewrites user-provided text through the Claw0x API to make AI-drafted writing sound more natural, with an LLM path and deterministic regex fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content teams, and agent builders use this skill to turn AI-drafted text into more natural prose while preserving the original meaning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text may leave the local environment for Claw0x and potentially Gemini processing. <br>
Mitigation: Do not submit secrets, regulated data, or confidential drafts unless those providers' terms and data handling are acceptable. <br>
Risk: The skill requires an API key for use. <br>
Mitigation: Store CLAW0X_API_KEY in an environment variable or secret manager, and do not embed it in prompts, source code, or version-controlled files. <br>
Risk: Rewriting can change tone, emphasis, or nuance even when the intended meaning is preserved. <br>
Mitigation: Review the humanized text before publication or use in sensitive communications. <br>


## Reference(s): <br>
- [AI Text Humanizer on ClawHub](https://clawhub.ai/kennyzir/humanizer-plus) <br>
- [Claw0x](https://claw0x.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON response containing humanized_text, length counts, and processing method.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW0X_API_KEY and may use LLM processing or a regex fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
