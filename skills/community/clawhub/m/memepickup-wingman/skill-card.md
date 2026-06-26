## Description: <br>
Dating wingman that generates openers, replies, profile analysis, date plans, and coaching via the MemePickup API (Hinge/Tinder/Bumble/Instagram). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samcraw1](https://clawhub.ai/user/samcraw1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill as a dating assistant to generate openers and replies, analyze dating profile or conversation screenshots, manage preferences, plan dates, and receive coaching for Hinge, Tinder, Bumble, and Instagram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dating conversations, profile screenshots, and preferences may be sent to MemePickup and its processors. <br>
Mitigation: Install only if comfortable sharing that data; use secure secret storage or environment variables for the API key. <br>
Risk: Auto-swipe can use logged-in sessions and perform visible likes, skips, comments, follows, or DMs without per-profile confirmation. <br>
Mitigation: Keep auto-swipe disabled unless actively supervised, limit sessions, and stop on CAPTCHA, errors, or unexpected behavior. <br>
Risk: Auto-swipe may violate dating-app terms and can create account-ban or privacy risk. <br>
Mitigation: Require explicit user acceptance before enabling and make the account-ban and privacy consequences clear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samcraw1/memepickup-wingman) <br>
- [MemePickup Homepage](https://memepickup.com) <br>
- [MemePickup App Store Listing](https://apps.apple.com/app/memepickup) <br>
- [Auto-Swipe Reference](references/AUTO-SWIPE.md) <br>
- [Manus Setup](references/MANUS-SETUP.md) <br>
- [OpenClaw Setup](references/OPENCLAW-SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMEPICKUP_API_KEY; API-backed actions consume credits, while coaching and date planning can run locally.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release, skill frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
