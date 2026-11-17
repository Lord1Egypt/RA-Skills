## Description:

LINE 貼圖生成大師 helps agents plan LINE sticker sets, write 12-panel Traditional Chinese sticker copy, produce 4x3 image-generation prompts, check consistency and readability, and guide slicing, background removal, preview, and ZIP export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qpooqp777](https://clawhub.ai/user/qpooqp777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan LINE sticker packs, create reusable 12-panel scripts and image prompts, check Taiwan Traditional Chinese wording, and prepare outputs for image processing tools. It is especially useful when a consistent character bible, safe workplace copy, and post-generation quality review are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references running an unpinned third-party npm project, which can introduce local code-execution supply-chain risk.

Mitigation: Review or pin the external project before running it, use a clean throwaway environment, and avoid exposing production credentials or sensitive files.

Risk: Sticker copy for workplace or public use can unintentionally include offensive, targeted, or confidential content.

Mitigation: Apply the included Traditional Chinese and workplace-risk review rules, prefer neutral alternatives for public release, and review each panel before distribution.

## Reference(s):

- [Skill README](artifact/README.md)
- [LINE Sticker Factory Integration Reference](artifact/references/line-sticker-factory.md)
- [Taiwan Traditional Chinese Copy Check Rules](artifact/references/zh-tw-copy-check.md)
- [Workplace Meme Catalog](artifact/references/workplace-meme-catalog.md)
- [Top 10 Sticker Copy Guide](artifact/references/top-10-sticker-copy-guide.md)
- [Little Monk Kind Words Site Reference](artifact/references/little-monk-kind-words-site.md)
- [4x3 LINE Sticker Prompt Template](artifact/templates/line-sticker-prompt-template.md)
- [line-sticker-factory](https://github.com/qpooqp777/line-sticker-factory)
- [Little Monk Kind Words Site](https://qpooqp777.github.io/little-monk-kind-words-site/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sticker scripts, fenced prompt blocks, review tables, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include character bibles, 12-panel sticker plans, image-generation prompts, Traditional Chinese copy checks, quality checks, and external tool setup guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
