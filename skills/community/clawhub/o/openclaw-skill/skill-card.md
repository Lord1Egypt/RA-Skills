## Description: <br>
Your pet dies if you don't write. Adopt a virtual tamagotchi, journal daily to keep it alive, earn tokens on Base. One command to start - no wallet needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxdleady](https://clawhub.ai/user/dxdleady) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to set up a DiaryBeast pet, write daily journal entries through the DiaryBeast API, and interact with pet status, rewards, shop, leaderboard, and public wall features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary entries are sent to the DiaryBeast service. <br>
Mitigation: Avoid putting secrets or highly sensitive personal information in entries. <br>
Risk: The setup script stores a DiaryBeast session token under the OpenClaw workspace. <br>
Mitigation: Install only when comfortable with local token storage and protect the workspace from unintended access. <br>
Risk: Public excerpts can be posted to The Wall. <br>
Mitigation: Review any publicExcerpt carefully before publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dxdleady/openclaw-skill) <br>
- [DiaryBeast homepage](https://diarybeast.xyz) <br>
- [DiaryBeast app](https://dapp.diarybeast.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The setup flow stores a local address and session token for use in later API calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
