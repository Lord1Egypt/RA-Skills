## Description:

Đổi Meta short-lived token (~1-2h) sang long-lived token (~60 ngày) qua Graph API, kiểm tra hạn, lưu vào env gateway và nhắc gia hạn. READ-ONLY với ads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to exchange Meta user access tokens for long-lived tokens, check token validity and expiry, update the gateway configuration, and set renewal reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meta access tokens and app secrets are sensitive credentials that could be exposed through chat history, logs, or gateway configuration.

Mitigation: Use a private credential-entry channel, protect the gateway configuration, never echo or log secrets, and rotate credentials that may have been exposed.

Risk: Changing gateway settings and restarting the gateway can affect its operation if the configuration is edited incorrectly.

Mitigation: Merge the token into the existing configuration while preserving other settings, then confirm token validity after restart.

Risk: A missed expiry reminder can leave an integration with an expired token.

Mitigation: Check token validity and expiry daily and notify the owner when fewer than 14 days remain.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/thinhbuiii/skills/meta-long-lived-token)
- [Meta Graph API access token exchange endpoint](https://graph.facebook.com/v21.0/oauth/access_token)
- [Meta Graph API debug token endpoint](https://graph.facebook.com/v21.0/debug_token)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
