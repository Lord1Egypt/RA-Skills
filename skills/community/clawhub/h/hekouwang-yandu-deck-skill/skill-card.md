## Description:

把文章制作成可翻页、可自动播放的 keynote 风格网页演示，自托管字体并可发布到 Cloudflare Pages；留言板和站点分析为可选功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to turn articles into interactive presentation decks, build a local site, and optionally publish it to Cloudflare Pages. A separate paid content skill is needed for its full article-generation workflow; the deck engine can also be used on its own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the deploy option publishes the deck to the public web.

Mitigation: Before deployment, review the content and confirm the Cloudflare Pages project name and intended release.

Risk: When enabled, the optional comments feature stores visitor nicknames, comment text, and a salted IP hash; scan coverage is partial.

Mitigation: Keep comments disabled unless needed, review the publishing and network behavior, and configure the IP salt for the deployment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huiyonghkw/skills/hekouwang-yandu-deck-skill)
- [Live site and demos](https://hekouwang.pages.dev)
- [Project homepage](https://github.com/huiyonghkw/hekouwang-yandu-deck-skill)

## Skill Output:

**Output Type(s):** [HTML, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [HTML deck and site files, Python and shell scripts, configuration files, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Builds a local preview; deployment is optional and requires Cloudflare configuration.]

## Skill Version(s):

1.3.6 (source: SKILL.md frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
