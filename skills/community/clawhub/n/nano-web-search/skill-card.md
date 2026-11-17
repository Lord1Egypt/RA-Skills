## Description:

AI-powered web search via NanoGPT API with multiple providers (linkup, tavily, exa, kagi, perplexity, valyu, brave). Supports searchResults, sourcedAnswer, and structured output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twolf01](https://clawhub.ai/user/twolf01)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web searches through NanoGPT providers and return search results, sourced answers, or structured data for downstream tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, domain filters, and API credentials are sent to NanoGPT's external web API.

Mitigation: Avoid confidential queries, keep NANOGPT_API_KEY out of logs and prompts, and use the skill only where NanoGPT API use is approved.

Risk: Runtime dependencies and shell execution introduce ordinary integration risk.

Mitigation: Install dependencies in a virtual environment, review commands before execution, and use pinned requirements when hardening for production.

## Reference(s):

- [NanoGPT homepage](https://nano-gpt.com)
- [NanoGPT web API endpoint](https://nano-gpt.com/api/web)
- [ClawHub skill page](https://clawhub.ai/twolf01/skills/nano-web-search)
- [ClawHub publisher profile](https://clawhub.ai/user/twolf01)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Code, Shell commands]

**Output Format:** [Markdown or JSON search output with optional shell and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANOGPT_API_KEY and sends queries, filters, and provider choices to the NanoGPT web API.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
