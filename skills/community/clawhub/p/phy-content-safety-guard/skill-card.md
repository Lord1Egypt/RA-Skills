## Description: <br>
Dual-layer AI content guardrail with red-team test methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add outbound content filtering to chatbots and AI agents, customize domain-specific guardrail categories, and run red-team tests against the policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default policy may suppress brand criticism and competitor recommendations under a safety label. <br>
Mitigation: Review and disclose brand and competitor blocking rules, or remove them for neutral content-safety use. <br>
Risk: The sample handler fails open on judge errors or timeouts by default. <br>
Mitigation: Use fail-closed fallback behavior for higher-risk domains and test the choice before deployment. <br>
Risk: The skill requires GOOGLE_GENAI_API_KEY for the judge model. <br>
Mitigation: Run the integration server-side and store the API key in environment secrets rather than client-side code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-content-safety-guard) <br>
- [Canlah AI](https://canlah.ai) <br>
- [Google Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_GENAI_API_KEY and a server-side JavaScript integration; examples include fallback behavior and red-team test cases.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
