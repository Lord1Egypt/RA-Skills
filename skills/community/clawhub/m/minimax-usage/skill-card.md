## Description: <br>
Monitor Minimax Coding Plan usage to stay within API limits. Fetches current usage stats and provides status alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to check MiniMax Coding Plan prompt consumption, remaining allowance, reset timing, and status warnings before continuing API-backed coding work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads and executes a broader .env file than the setup instructions describe. <br>
Mitigation: Review or edit the script before installing, store only intended MiniMax variables where it reads them, or change it to safely parse a clearly scoped local config file. <br>
Risk: The skill requires sensitive MiniMax credentials. <br>
Mitigation: Keep API keys out of shared files, logs, and version control, and rotate them if they may have been exposed. <br>


## Reference(s): <br>
- [MiniMax basic information](https://platform.minimax.io/user-center/basic-information) <br>
- [MiniMax Coding Plan page](https://platform.minimax.io/user-center/payment/coding-plan) <br>
- [ClawHub skill page](https://clawhub.ai/TheSethRose/minimax-usage) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_CODING_API_KEY and MINIMAX_GROUP_ID to query current MiniMax Coding Plan usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
