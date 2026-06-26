## Description: <br>
Use when an agent needs to drive a real Chrome window via opencli to inspect pages, fill forms, click through logged-in flows, extract ad-hoc data, and interpret structured browser command envelopes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide browser automation against a live Chrome session, including page inspection, form entry, navigation, extraction, network-response review, and validation after critical writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad agent control of a real Chrome window, including logged-in browser sessions and sensitive account flows. <br>
Mitigation: Use a dedicated browser profile or test account, supervise sensitive sessions, and require explicit confirmation before form submissions, purchases, account changes, posts, or saving extracted data. <br>
Risk: Captured API responses and network data can persist after browser automation work. <br>
Mitigation: Clear the opencli network cache after sensitive work and avoid capturing or retaining data that is not needed for the task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liberalchang/opencli-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON envelope examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages inspect-first browser actions, structured command envelopes, and verification after writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
