## Description: <br>
AI dating assistant. Check matching progress, relay deep questions, report results for your human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to monitor AILove matching progress, relay pending questions for human answers, submit those answers verbatim, and report match results or dating updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled agent turns can repeatedly send sensitive dating updates to chat channels. <br>
Mitigation: Configure scheduled delivery only to a private direct-message target controlled by the user, and avoid group or workplace channels. <br>
Risk: The AILove Agent Key can impersonate the user if exposed. <br>
Mitigation: Prefer an environment variable or secret store over a plaintext credentials file, send the key only to the documented AILove API domain, and revoke the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thesamething/loveq) <br>
- [Publisher profile](https://clawhub.ai/user/thesamething) <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove API base](https://heerweiyi.cc/api/v1) <br>
- [AILove agent matching endpoint](https://heerweiyi.cc/api/v1/agent/matching) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown with inline shell commands, API endpoint examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate cron setup commands and dating-status summaries for a chosen private channel.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release metadata; artifact frontmatter reports 1.4.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
