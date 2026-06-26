## Description: <br>
Post and reply on Twitter and Farcaster with character limit checks, image support, threads, link shortening, and draft preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and social operators use this skill to prepare commands for posting or replying on Twitter and Farcaster, including media posts, threads, shortened links, and dry-run previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store powerful Twitter and Farcaster credentials, including private keys. <br>
Mitigation: Use least-privilege credentials where possible, keep credential files owner-only, and avoid storing a custody private key unless it is strictly required. <br>
Risk: The artifact describes posting scripts that are not included for review. <br>
Mitigation: Review the actual scripts before installing, adding credentials, or posting to social platforms. <br>
Risk: Using automatic confirmation can send posts or replies without another prompt. <br>
Mitigation: Start with dry-run previews and avoid --yes unless you explicitly want posts or replies sent without additional confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupeng-social-postcjo) <br>
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) <br>
- [X API pricing](https://developer.twitter.com/#pricing) <br>
- [OpenClaw CLI forum](https://openclawcli.forum) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run and confirmation options for previewing posts before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
