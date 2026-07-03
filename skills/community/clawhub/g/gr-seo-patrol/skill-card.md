## Description: <br>
Gr Seo Patrol helps agents run SEO/GEO patrols, track search rankings, audit site metadata and schema, and prepare controlled GitHub-backed content fixes such as canonical updates and internal-link rescue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris-1031](https://clawhub.ai/user/gingiris-1031) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and SEO practitioners use this skill to run daily SEO reports, diagnose ranking drops, inspect GA4 and llms.txt status, audit pages and sites, and prepare controlled fixes for Jekyll/GitHub-backed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify GitHub-hosted posts through canonical fixes, title rewrites, internal-link injection, or archive updates without a sufficiently clear approval boundary. <br>
Mitigation: Use a narrowly scoped GitHub token, keep dry-run mode enabled by default, set GR_SITE and GR_REPO explicitly, and require a reviewed diff plus explicit confirmation before applying content changes. <br>
Risk: SEO audit reports or ranking diagnoses can be misleading if script output is expanded beyond observed checks or if external API/site fetch results are stale or incomplete. <br>
Mitigation: Treat the scripts' structured JSON output as the source of truth, preserve location codes and statuses in reports, and require human review for recommendations that would change page content or metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gingiris-1031/gr-seo-patrol) <br>
- [DataForSEO Google Organic SERP API](https://api.dataforseo.com/v3/serp/google/organic/live/advanced) <br>
- [JeffLi1993 seo-audit-skill original repository](https://github.com/JeffLi1993/seo-audit-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON audit envelopes, shell commands, and code/configuration change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows depend on DATAFORSEO_B64, GITHUB_TOKEN, GR_SITE, GR_REPO, and related environment variables; write-capable workflows should remain in dry-run mode until reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
