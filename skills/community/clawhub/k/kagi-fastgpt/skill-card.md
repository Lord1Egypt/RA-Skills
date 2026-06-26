## Description: <br>
Ask questions and get AI-synthesized answers backed by live web search, via Kagi's FastGPT API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelazar](https://clawhub.ai/user/joelazar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to ask factual, API, and current-events questions and receive direct answers synthesized from live web sources with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to Kagi and API use may incur charges. <br>
Mitigation: Use the skill only with an approved Kagi account and API key, and monitor Kagi API billing. <br>
Risk: The wrapper can download and run a prebuilt GitHub release binary on first use. <br>
Mitigation: Prefer building the included Go source locally, or verify the downloaded release checksum before running the binary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joelazar/kagi-fastgpt) <br>
- [Kagi FastGPT API documentation](https://help.kagi.com/kagi/api/fastgpt.html) <br>
- [Kagi API settings](https://kagi.com/settings/api) <br>
- [Kagi API billing](https://kagi.com/settings/billing_api) <br>
- [GitHub release checksums](https://github.com/joelazar/kagi-skills/releases/download/${TAG}/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text with references by default, or structured JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token usage and API balance are written to stderr when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
