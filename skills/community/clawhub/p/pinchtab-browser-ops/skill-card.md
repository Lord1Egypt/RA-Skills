## Description:

Browser automation via PinchTab CLI (nav/snap/find/click/fill/press/text) with low-token accessibility-tree flow for operating websites, filling forms, publishing content, collecting page text, and running repeatable browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiszhou](https://clawhub.ai/user/wiszhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to guide an agent through PinchTab browser automation with fresh accessibility snapshots, deterministic element actions, and completion checks. It includes a Xiaohongshu long-form draft workflow with manual handling for login, CAPTCHA, SMS, and 2FA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates websites through the user's active browser session, which can affect authenticated accounts or sensitive forms.

Mitigation: Review actions before allowing publishing or form submission on sensitive sites, and require the user to complete login, QR scan, SMS, CAPTCHA, and 2FA steps manually.

Risk: Dynamic pages can rerender and make previously captured element references stale, leading to incorrect clicks or fills.

Mitigation: Use fresh PinchTab snapshots after major state changes, wait 1-2 seconds around critical actions, and retry at most twice before asking for human intervention.

Risk: The eval fallback can bypass the normal low-token accessibility-tree flow if used too broadly.

Mitigation: Use eval only with explicit approval for a short-lived unblock, then return immediately to nav, snap, find, click, fill, press, and text commands.

## Reference(s):

- [PinchTab Browser Ops Skill](https://clawhub.ai/wiszhou/skills/pinchtab-browser-ops)
- [Xiaohongshu Long-Form Workflow](references/xiaohongshu-longform.md)
- [Xiaohongshu Creator Publish Page](https://creator.xiaohongshu.com/publish/publish)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running PinchTab environment and user-controlled browser session for authenticated or sensitive steps.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
