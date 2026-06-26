## Description: <br>
Enables grounded question answering by automatically executing the Google Search tool within Gemini models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theoseo](https://clawhub.ai/user/theoseo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to answer questions that require current web information or verifiable citations by calling Gemini with Google Search grounding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search prompts and related query context are sent to Google/Gemini. <br>
Mitigation: Avoid submitting secrets or regulated data, and use the skill only where sending query context to Google/Gemini is acceptable. <br>
Risk: Gemini API usage can incur cost or expose an overly broad credential. <br>
Mitigation: Use a restricted Gemini API key, monitor API usage and billing, and rotate the key if exposure is suspected. <br>
Risk: Dependency versions may change over time when installed from version ranges. <br>
Mitigation: Pin dependencies locally when reproducible builds are required. <br>


## Reference(s): <br>
- [Google Search Tool Reference](references/api_reference.md) <br>
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey) <br>
- [Google Web Search on ClawHub](https://clawhub.ai/theoseo/google-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language text or Markdown answer with grounded citation links; helper code returns a string.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and can optionally use GEMINI_MODEL to select the Gemini model.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact pyproject.toml reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
