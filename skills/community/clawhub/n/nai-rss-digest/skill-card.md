## Description: <br>
Generate a structured daily or weekly markdown digest from an OPML list of RSS/Atom feeds, optionally filtered by keywords, for Obsidian or Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to turn OPML feed lists into daily or weekly markdown news digests for Obsidian, Discord, email, or scheduled workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided OPML feed URLs are fetched over the network, and article titles or summaries come from external feed content. <br>
Mitigation: Review feed URLs before running or scheduling the workflow, and treat generated article text as external content rather than trusted instructions. <br>
Risk: Scheduled digest jobs can repeatedly fetch feeds and write markdown files to configured output paths. <br>
Mitigation: Review cron commands before enabling them and choose output paths intentionally. <br>
Risk: Unreachable or malformed feeds are skipped with warnings, so a digest may be incomplete. <br>
Mitigation: Check stderr warnings and validate the feed list when expected sources are missing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/newageinvestments25-byte/nai-rss-digest) <br>
- [Atom syndication namespace](http://www.w3.org/2005/Atom) <br>
- [RSS content module namespace](http://purl.org/rss/1.0/modules/content/) <br>
- [Dublin Core namespace](http://purl.org/dc/elements/1.1/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest files, JSON intermediate data, and command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OPML input, fetches external feed URLs, and can write digest files to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
