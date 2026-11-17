## Description:

Searches MGTV video resources and opens selected playback pages in the system browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kllb520](https://clawhub.ai/user/kllb520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to search for MGTV programs, open known MGTV video links, and receive a playable URL when a browser cannot be launched.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The direct URL path can open user-supplied links beyond the intended MGTV playback flow.

Mitigation: Use direct URLs only when the user explicitly provides a trusted MGTV link, and validate the destination before launching it.

Risk: Browser launching moves the user from the agent session into an external website.

Mitigation: Run the skill only for explicit MGTV search or playback requests, and rely on the printed URL fallback in headless or restricted environments.

Risk: Some documentation mentions installing Playwright even though the current release does not require it for normal use.

Mitigation: Do not install Playwright for standard MGTV search and playback unless a separate trusted workflow requires browser automation.

## Reference(s):

- [MGTV ClawHub skill page](https://clawhub.ai/kllb520/skills/mgtv)
- [kllb520 ClawHub publisher profile](https://clawhub.ai/user/kllb520)
- [MGTV search API endpoint](https://mobileso.bz.mgtv.com/pc/suggest/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with URLs and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open a system browser or print a playback URL when browser launch is unavailable.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
