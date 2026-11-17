## Description:

Novel Scraper Pro helps agents scrape web novel chapters, fill paginated chapter content, resume interrupted runs, and save formatted TXT outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to collect web novel chapters from supported sites, recover from interrupted scraping sessions, and produce merged local TXT files for reading or archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper fetches user-provided URLs and can reach arbitrary web targets.

Mitigation: Run it only against trusted public novel URLs and avoid internal, private-network, or sensitive endpoints.

Risk: The optional SPA mode delegates fetching to a browser helper for dynamic pages.

Mitigation: Use --force-spa only for trusted sites and review fetched content before relying on the output.

Risk: The helper scripts write local TXT, cache, state, and optional merged output files.

Mitigation: Keep output names simple, avoid path or traversal components in --output values, and review generated files before sharing them.

Risk: Documented cleanup commands remove cache or progress files permanently.

Mitigation: Check the exact paths before running cleanup commands and back up any progress or cached content that should be retained.

Risk: Dependencies are specified with minimum versions instead of fully pinned versions.

Mitigation: Pin and review dependencies in controlled deployments before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/novel-scraper-pro)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [Supported site configuration](artifact/configs/sites.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated TXT files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes chapter text files under the user's OpenClaw novels workspace, stores scraper cache under /tmp/novel_scraper_cache, and tracks resume state in the skill state directory.]

## Skill Version(s):

2.0.3 (source: server release evidence and changelog, released 2026-04-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
