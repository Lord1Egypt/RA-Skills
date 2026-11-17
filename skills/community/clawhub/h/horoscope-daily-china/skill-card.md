## Description:

Create 12 constellation fortune images with TianAPI as five-page social media assets for Xiaohongshu, Douyin, and Toutiao publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangj85](https://clawhub.ai/user/zhangj85)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to generate daily Chinese horoscope image sets and publishing copy for social media channels. The workflow calls TianAPI, formats constellation rankings and pairing information, and writes share-ready output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling and installation guidance are under-scoped.

Mitigation: Use a pinned, trusted ClawHub CLI version, create config.json from a local template, protect the TianAPI key, and avoid committing or sharing the config file.

Risk: Generated scores are post-processed while presented as API-backed entertainment data.

Mitigation: Review the generated output before publishing, keep the entertainment disclaimer visible, and avoid describing the scores as a direct rendering of raw TianAPI values.

Risk: The skill depends on external TianAPI endpoints and quota availability.

Mitigation: Verify the TianAPI endpoint URLs and account quota before use, and treat API failures or quota errors as reasons to stop rather than publish stale output.

## Reference(s):

- [TianAPI](https://www.tianapi.com/)
- [OpenClaw Docs](https://docs.openclaw.ai/)
- [ClawHub Skill Page](https://clawhub.ai/zhangj85/skills/horoscope-daily-china)
- [Horoscope Image Standard](references/horoscope-image-standard.md)
- [Constellation Symbols](references/icon/constellation_symbols.json)

## Skill Output:

**Output Type(s):** [Files, Images, Text]

**Output Format:** [PNG image files and plain text publishing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates five 1080x1400 PNG pages plus a dated publishing text file.]

## Skill Version(s):

1.2.1 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
