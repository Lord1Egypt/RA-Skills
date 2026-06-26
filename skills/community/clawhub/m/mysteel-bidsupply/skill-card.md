## Description: <br>
Supports steel supply and demand spot-market queries and bidding data retrieval for users looking for buyers, suppliers, bidding information, or project opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to classify Chinese steel-market requests, configure a Mysteel API key, and query either bidding/project opportunities or steel supply and demand listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mysteel API keys are saved as plaintext local files. <br>
Mitigation: Use a dedicated or low-privilege Mysteel API key, keep references/api_key.md out of shared or synced workspaces, delete it when no longer needed, and rotate the key if the workspace may have been exposed. <br>
Risk: Steel procurement, supply, demand, and bidding searches are sent to Mysteel services. <br>
Mitigation: Install and use the skill only when those searches are appropriate to share with Mysteel. <br>


## Reference(s): <br>
- [Intent Guide](references/intent-guide.md) <br>
- [Mysteel_BidSupply on ClawHub](https://clawhub.ai/wyb92/mysteel-bidsupply) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise query guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill stores a Mysteel API key in a local references/api_key.md file and calls Mysteel HTTP APIs to retrieve results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
