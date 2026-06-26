## Description: <br>
A multilingual SOP for running an autonomous SEO/GEO agent that manages keyword mapping, landing-page planning, daily reporting, IndexNow, AI-crawler access, and conversion-oriented content workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris-1031](https://clawhub.ai/user/gingiris-1031) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, growth marketers, technical SEOs, and content teams use this skill to operate an SEO/GEO agent for search optimization workflows, including keyword-to-landing-page tracking, daily reports, CTA blocks, and AI-search-friendly publishing practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward using third-party SEO accounts, API keys, publishing tokens, and site-changing workflows. <br>
Mitigation: Use project-scoped, least-privilege credentials stored in a secret manager, avoid personal or root tokens, and set API budget limits. <br>
Risk: SEO publishing, robots.txt edits, IndexNow pushes, and other public-facing or paid actions can affect real sites and accounts. <br>
Mitigation: Require human approval before publishing, deployment, robots.txt changes, IndexNow pushes, or any paid or public-facing action. <br>
Risk: SEO automation guidance may produce incorrect, misleading, or unsuitable changes for a specific site. <br>
Mitigation: Review recommendations and scan the skill before deployment, especially when connecting it to real sites or accounts. <br>


## Reference(s): <br>
- [Full SEO/GEO Agent SOP](references/full-sop.md) <br>
- [Hugging Face dataset](https://huggingface.co/datasets/Gingiris/gingiris-seo-geo-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with tables, templates, checklists, and inline configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill output intended for human review before site, account, publishing, or paid actions.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
