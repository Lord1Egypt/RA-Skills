## Description: <br>
Mixture of Agents: Make 3 frontier models argue, then synthesize their best insights into one superior answer. ~$0.03/query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jscianna](https://clawhub.ai/user/jscianna) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run complex prompts through several OpenRouter models in parallel and receive a synthesized answer for due diligence, market research, technical evaluation, or brainstorming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to OpenRouter and may be processed by multiple model providers. <br>
Mitigation: Avoid confidential or regulated data unless provider terms fit the use case, and use a dedicated API key. <br>
Risk: The paid tier makes several model calls per query and can incur charges. <br>
Mitigation: Use spending limits and monitor usage; use the free tier only when its rate limits are acceptable. <br>
Risk: An alternate demo script contains a fixed example prompt and is not the documented entrypoint. <br>
Mitigation: Use the documented scripts/moa.js entrypoint or exported handle function. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jscianna/moa) <br>
- [Together AI Mixture of Agents](https://www.together.ai/blog/together-moa) <br>
- [OpenRouter API Keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [String or Markdown-style synthesized answer, with CLI status text when run from the shell] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; paid mode makes several model calls per query and free mode may be rate limited.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
