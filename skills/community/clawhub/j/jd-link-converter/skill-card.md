## Description: <br>
Converts JD.com mobile share links, short links, product URLs, or product IDs into clean desktop JD product links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mousounikki](https://clawhub.ai/user/mousounikki) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to normalize JD.com short links, mobile product links, parameterized desktop links, and product IDs into clean desktop product URLs. It is useful for single-link cleanup or batch conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resolving 3.cn or u.jd.com short links contacts JD short-link hosts and may expose request metadata such as IP address, timing, and User-Agent. <br>
Mitigation: Avoid using the skill for sensitive or private links when outbound request metadata matters; prefer direct item.jd.com, item.m.jd.com, or product ID inputs where possible. <br>
Risk: Short links can expire, redirect unexpectedly, or fail under network restrictions. <br>
Mitigation: Review converted URLs before use and provide a mobile JD product link or product ID when short-link resolution fails. <br>


## Reference(s): <br>
- [JD URL formats](references/url_formats.md) <br>
- [ClawHub skill page](https://clawhub.ai/mousounikki/jd-link-converter) <br>
- [JD short-link resolution reference](https://blog.csdn.net/Firewall5788/article/details/120301954) <br>
- [OpenClaw skill reference](https://github.com/momozi1996/awesome-ai-persona-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown table or JSON conversion results containing original links, product IDs, resolved links when applicable, and clean JD desktop URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Short-link resolution may perform outbound HTTP requests to JD short-link hosts; direct product links and product IDs can be converted without network access.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
