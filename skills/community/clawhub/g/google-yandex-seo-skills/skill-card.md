## Description: <br>
Use this skill when the user wants an SEO audit, technical SEO review, page-level Google or Yandex analysis, robots.txt or sitemap validation, canonical/indexability checks, or a client-ready SEO report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Horosheff](https://clawhub.ai/user/Horosheff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and SEO practitioners use this skill to run page-level Google and Yandex SEO audits, inspect crawlability and indexability signals, and produce prioritized findings for client-ready reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit can make outbound website requests from the user's environment, including redirects, robots.txt, and sitemap discovery. <br>
Mitigation: Run it only against sites the user owns or is authorized to test, avoid internal or sensitive URLs, and review crawl targets before enabling broader crawl mode. <br>
Risk: Local npm dependencies must run on the user's machine before audit artifacts are produced. <br>
Mitigation: Install and execute the skill only in a trusted workspace after reviewing the bundled dependencies and scripts. <br>


## Reference(s): <br>
- [IndexLift SEO Auditor ClawHub release](https://clawhub.ai/Horosheff/google-yandex-seo-skills) <br>
- [Check Inventory](references/checks.md) <br>
- [Install Guide](references/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Agent guidance plus generated Markdown and JSON audit artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prioritized SEO findings, category scores, page snapshots, and Google/Yandex-specific breakdowns.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
