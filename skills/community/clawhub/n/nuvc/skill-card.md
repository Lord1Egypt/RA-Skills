## Description: <br>
Score business ideas, get startup roasts, analyze markets, and extract structured data - powered by the same AI engine behind 250+ VC investment memos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuvcai](https://clawhub.ai/user/nuvcai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, startup operators, investors, and agents use this skill to submit business ideas, pitch text, market questions, or metrics to NUVC for scoring, market analysis, competitive analysis, startup feedback, structured extraction, and model availability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business ideas, pitch text, market notes, and metrics submitted through the skill are sent to NUVC's remote API for processing. <br>
Mitigation: Use the skill only when NUVC's privacy and retention terms fit the data, and avoid submitting confidential customer data, regulated data, sensitive investor materials, or proprietary plans unless approved. <br>
Risk: The skill depends on a private NUVC_API_KEY environment variable. <br>
Mitigation: Keep NUVC_API_KEY out of prompts, logs, shared transcripts, source control, and public configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nuvcai/nuvc) <br>
- [NUVC API keys](https://nuvc.ai/api-platform/keys) <br>
- [NUVC API documentation](https://nuvc.ai/api-platform/docs) <br>
- [NUVC website](https://nuvc.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown responses by default, raw JSON when --json is explicitly requested, and shell commands for agent execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and NUVC_API_KEY; sends submitted business, pitch, market, and metric text to NUVC's remote API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
