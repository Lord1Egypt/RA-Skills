## Description: <br>
Queries multiple AI assistants independently on the same complex question, compares their responses, and synthesizes a concise cross-validated analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangsaizz](https://clawhub.ai/user/zhangsaizz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to ask the same analysis question across multiple AI providers, compare the answers, and produce a synthesized Markdown report for complex topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to multiple third-party AI providers through logged-in user sessions. <br>
Mitigation: Use only data approved for those providers; avoid secrets, personal data, regulated data, internal documents, and confidential business material unless explicitly authorized. <br>
Risk: Browser session data and generated reports can persist locally. <br>
Mitigation: Protect or clear the browser-profile directory regularly, and review saved reports before backing them up or sharing them. <br>
Risk: Synthesized reports can carry forward inaccurate, outdated, or conflicting claims from provider responses. <br>
Mitigation: Cross-check important facts with authoritative sources before using the output for decisions. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/zhangsaizz/multi-ai-search-analysis) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Python Usage Guide](artifact/scripts/USAGE.md) <br>
- [AI Platform Configuration](artifact/config/ai-platforms.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with comparison tables, synthesized summaries, setup commands, and optional chart assets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include timestamps, provider names, extracted data tables, quality scores, and generated chart files.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
