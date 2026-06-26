## Description: <br>
Navigate and use OpenClaw documentation efficiently with cached doc fetch/search tooling, sitemap routing, category guidance, config snippet lookup, and source-linked answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollieb89](https://clawhub.ai/user/ollieb89) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents answering OpenClaw setup, configuration, troubleshooting, automation, platform, and provider questions use this skill to route docs, fetch or search cached pages, and return source-linked configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local bash scripts for documentation fetch, search, cache, and change tracking. <br>
Mitigation: Review scripts before use and run them in an environment where local shell execution is acceptable. <br>
Risk: The skill fetches public OpenClaw docs over the network and may return stale cached content when offline or past the configured TTL. <br>
Mitigation: Refresh the cache for time-sensitive answers and state cache freshness when using cached or offline results. <br>
Risk: Cache cleanup and refresh commands remove Markdown files from the configured cache directory. <br>
Mitigation: Keep OPENCLAW_DOCS_CACHE_DIR dedicated to this skill so cleanup cannot affect unrelated Markdown files. <br>
Risk: A local .openclawdocs-env.sh helper file can change the base URL, TTL, or cache path used by the scripts. <br>
Mitigation: Review or avoid added .openclawdocs-env.sh files before running the bundled scripts. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/ollieb89/new-openclaw-docs) <br>
- [Operations Guide](references/operations.md) <br>
- [Routing Guide](references/routing.md) <br>
- [Common Config Snippets](snippets/common-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown answers with source paths or URLs, inline shell commands, and JSON configuration snippets when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on local cached documentation freshness and network availability for doc fetches.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; artifact/package.json reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
