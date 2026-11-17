## Description:

Enables grounded question answering by automatically executing the Google Search tool within Gemini models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theoseo](https://clawhub.ai/user/theoseo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to answer questions that require recent web information, current data, or source-backed citations through Gemini's Google Search grounding tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts and related context are sent to Gemini/Google for grounded responses.

Mitigation: Use the skill only where sending prompts to Gemini/Google is acceptable, and avoid submitting sensitive data unless approved for that environment.

Risk: The skill requires a Gemini API key in the execution environment.

Mitigation: Use a restricted API key with minimal required permissions and rotate it according to local credential policy.

Risk: Unpinned dependency ranges can change install results over time.

Mitigation: Pin or review dependency versions when reproducible or controlled deployments matter.

## Reference(s):

- [Google Search Tool Reference](references/api_reference.md)
- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey)
- [uv Python Package Manager](https://github.com/astral-sh/uv)
- [ClawHub Skill Page](https://clawhub.ai/theoseo/skills/google-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language text or Markdown with citations, plus Python usage snippets and shell configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY; optional GEMINI_MODEL selects the Gemini model.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact pyproject.toml declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
