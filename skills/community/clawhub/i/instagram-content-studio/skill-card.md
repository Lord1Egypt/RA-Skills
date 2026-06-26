## Description: <br>
Manage an Instagram account by viewing profile and post data, publishing images, carousels, videos, and Reels, and reading or writing comments through agent-run scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uyeong](https://clawhub.ai/user/uyeong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate an Instagram account for profile review, media publishing, and comment workflows after credentials and permissions are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish Instagram media and create comments or replies on an account. <br>
Mitigation: Confirm the exact files, captions, comment text, and target posts before allowing publish or comment commands. <br>
Risk: Access tokens and Meta app secrets are read from and refreshed into plaintext .env files. <br>
Mitigation: Use a dedicated .env file outside source control, avoid arbitrary --env paths, and grant only the minimum Meta permissions required. <br>
Risk: Local media uploads briefly expose selected files through a public cloudflared tunnel. <br>
Mitigation: Prefer public media URLs when possible and only use local files that are acceptable to expose temporarily. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/uyeong/instagram-content-studio) <br>
- [Agent Skills open standard](https://agentskills.io) <br>
- [Meta for Developers](https://developers.facebook.com/) <br>
- [Cloudflare Quick Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [JSON command output with Markdown command examples and brief user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts write machine-readable JSON to stdout, log to stderr, and may update token values in the configured .env file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
