## Description: <br>
This skill helps an agent build search links and search workflows across 10 free search engines, including Baidu, Bing, 360 Search, Sogou, WeChat search, Toutiao, Jisilu, Ecosia, and WolframAlpha. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, researchers, and developers use this skill to run single-engine searches or compare up to three search engines for everyday research, WeChat article discovery, technical lookup, financial community search, and scientific or mathematical queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to third-party search engines. <br>
Mitigation: Avoid secrets, sensitive internal topics, personal data, or confidential business terms in search queries. <br>
Risk: The skill declares broad read, exec, glob, and grep tool access and includes examples that generate shell commands and callback URLs. <br>
Mitigation: Review proposed commands and callback URLs before approval, and only run commands that are necessary for the search task. <br>
Risk: Search results and generated summaries can be incomplete, stale, biased, or misleading. <br>
Mitigation: Cross-check important findings across multiple sources and verify source dates before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-search-tool-free) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with search links, URL templates, and optional shell command or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated third-party search-engine URLs; does not automatically aggregate full page contents in the free edition.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
