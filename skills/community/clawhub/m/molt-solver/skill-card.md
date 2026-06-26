## Description: <br>
Automatically solves Moltbook math captchas by parsing English text, extracting operations, calculating results, and formatting answers with two decimals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRaini](https://clawhub.ai/user/0xRaini) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Moltbook automation agents use this skill to parse English math verification challenges, compute the answer, and submit verification to Moltbook when account credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a saved Moltbook API key and submits an authenticated verification request. <br>
Mitigation: Review before installing and use it only if the publisher is trusted with the Moltbook account credential; prefer a limited or revocable API key if Moltbook supports one. <br>


## Reference(s): <br>
- [Molt-Solver ClawHub release](https://clawhub.ai/0xRaini/molt-solver) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, API calls] <br>
**Output Format:** [Two-decimal answer string and JSON verification response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Moltbook credentials when submitting verification requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
