## Description: <br>
Mysteel_ReportWrite helps agents generate commodity market research reports from Mysteel data when users ask for market analysis, price trends, supply-demand analysis, or strategy reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and commodity-market analysts use this skill to request daily, weekly, in-depth, or strategy-style research reports that combine Mysteel report outlines with structured Markdown analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Mysteel API key is stored in a local markdown file and may be exposed if the workspace is shared or synced. <br>
Mitigation: Use a dedicated key, restrict workspace access, and remove or rotate the key after use or before sharing the workspace. <br>
Risk: Report prompts are sent to Mysteel, which may disclose confidential business details included in the request. <br>
Mitigation: Avoid confidential or sensitive details unless sharing them with Mysteel is acceptable for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyb92/mysteel-reportwrite) <br>
- [API key configuration reference](artifact/references/api_key.md) <br>
- [Mysteel API caller script](artifact/scripts/call_mysteel_api.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research report with structured sections; the helper script returns JSON for outline generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mysteel API key stored in references/api_key.md and sends report prompts to Mysteel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
