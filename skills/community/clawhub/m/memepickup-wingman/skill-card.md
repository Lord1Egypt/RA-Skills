## Description:

Dating wingman that generates openers, replies, profile analysis, date plans, and coaching via the MemePickup API for Hinge, Tinder, Bumble, and Instagram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samcraw1](https://clawhub.ai/user/samcraw1)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to get dating-app openers, reply suggestions, screenshot and profile analysis, date planning, preference handling, and coaching through MemePickup. Agents can use it to call MemePickup helpers, return dating guidance, and optionally coordinate user-approved auto-swipe workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private dating messages, screenshots, profile images, and preferences may be sent to remote MemePickup/OpenAI-backed processing.

Mitigation: Use the skill only when the user accepts that data sharing, avoid unrelated sensitive content, and keep activation limited to dating-related contexts.

Risk: API keys can be exposed if pasted into chat, shell startup files, or other shared logs.

Mitigation: Prefer OpenClaw configuration, environment variables, or a secrets manager; rotate the MemePickup API key if it is disclosed.

Risk: Auto-swipe can automate real dating-app account actions and may violate platform terms, causing account bans or unintended likes, messages, follows, or skips.

Mitigation: Require explicit user opt-in, show the auto-swipe warning, keep the documented 30-profile cap and randomized delays, and stop immediately on CAPTCHA, API errors, interaction failures, pause, or stop requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samcraw1/skills/memepickup-wingman)
- [MemePickup homepage](https://memepickup.com)
- [MemePickup App Store listing](https://apps.apple.com/app/memepickup)
- [Auto-Swipe Reference](references/AUTO-SWIPE.md)
- [OpenClaw Setup](references/OPENCLAW-SETUP.md)
- [Manus Setup](references/MANUS-SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash command examples; API helper calls return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMEPICKUP_API_KEY and internet access; API-backed actions may consume MemePickup credits.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
