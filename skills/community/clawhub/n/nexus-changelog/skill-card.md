## Description:

Generate changelogs from git commits or descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to generate changelogs from git commit history or free-form release descriptions. It is suited for agent workflows that can send changelog input to the NEXUS service and provide a payment proof or supported payment credential.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changelog input may include private repository details or sensitive source history that is sent to a third-party service.

Mitigation: Review input before use, start in sandbox mode, and avoid sending private repository details unless approved.

Risk: The skill uses a paid remote service and can transmit payment credentials or payment proofs.

Mitigation: Keep payment credentials narrowly scoped and require explicit approval before paid requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-changelog)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [JSON object containing a generated changelog string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a payment proof or supported payment credential; free sandbox testing is documented.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
