## Description:

GoGlobal guides users through deploying a VPS-based proxy service with BandwagonHost KiwiVM API links, 3x-ui panel setup, VLESS+Reality node creation, client setup, and connectivity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scientificinternet](https://clawhub.ai/user/scientificinternet)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to set up and verify proxy access on a VPS they own, with the agent providing step-by-step Chinese guidance instead of requiring SSH or command-line work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles KiwiVM API keys and generated control links that can operate or erase the user's VPS if exposed.

Mitigation: Use only a disposable or dedicated VPS, avoid sharing screenshots or browser history containing control links, and rotate the KiwiVM API key immediately after setup.

Risk: The setup runs root-level installation through an unpinned third-party 3x-ui installer.

Mitigation: Review the skill and installer before deployment, run it only on infrastructure prepared for this purpose, and avoid treating the release as low risk.

Risk: The management panel may initially use HTTP and expose administrator credentials on untrusted networks.

Mitigation: Change panel credentials through a safer channel, add HTTPS before routine administration, and avoid using the HTTP admin panel on untrusted networks.

Risk: The skill steers users through affiliate and download links while performing infrastructure setup.

Mitigation: Review the linked services and software sources before purchase or installation, and confirm they match the user's intended provider and client platform.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scientificinternet/skills/goglobal)
- [Publisher Profile](https://clawhub.ai/user/scientificinternet)
- [Client Download Page](https://help.bwh8l.net/index.html)
- [BandwagonHost Purchase Entry](https://bwh8l.net)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown text with browser links, setup steps, command-bearing API URLs, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed to respond in Chinese, advance one step at a time, and wait for user confirmation between setup phases.]

## Skill Version(s):

3.3.6 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
