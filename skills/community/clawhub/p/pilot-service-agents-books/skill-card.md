## Description: <br>
Book search and catalogs for Project Gutenberg through Gutendex and Open Library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to discover book-search service agents, inspect their filter contracts, and query Project Gutenberg or Open Library records by title, author, ISBN, or other supported filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local Pilot Protocol daemon, pilotctl, network 9 membership, and reachable service agents; unavailable or misconfigured dependencies can prevent successful catalog queries. <br>
Mitigation: Confirm pilotctl is on PATH, start the daemon, join network 9, and use list-agents plus each agent's /help response to verify availability and supported filters before querying. <br>
Risk: Some responses may be generated summaries rather than raw catalog data, so they can omit details or phrase results imprecisely. <br>
Mitigation: Use /data for structured catalog results when accuracy matters and review upstream links or metadata before relying on summarized output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-books) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and a reachable list-agents directory agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
