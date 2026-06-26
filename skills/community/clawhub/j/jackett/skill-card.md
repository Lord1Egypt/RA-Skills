## Description: <br>
Search torrent indexers with Jackett. Use when the user asks to "search torrents", "search with Jackett", "find releases", "search indexers", "list Jackett indexers", "check Jackett capabilities", "search movie/tv/music/book releases", or mentions Jackett/Torznab-based torrent search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imyukehan](https://clawhub.ai/user/imyukehan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users with a configured Jackett instance use this skill to search torrent indexers, inspect indexer capabilities, and return Jackett/Torznab results in agent-readable form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Jackett API key is a credential that could expose configured indexers if mishandled. <br>
Mitigation: Store it only in the documented config file or environment variables, keep file permissions restrictive, and do not commit it to source control. <br>
Risk: Jackett results can include download links from configured torrent indexers. <br>
Mitigation: Do not automatically open or fetch returned links; check the source, safety, and legality before using any result. <br>
Risk: Returned results depend on the trustworthiness of the user's Jackett instance and configured indexers. <br>
Mitigation: Use only trusted Jackett instances and indexers, and inspect capabilities or narrow searches before acting on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imyukehan/jackett) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Torznab feed schema](http://torznab.com/schemas/2015/feed) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; parsed search results as JSON or raw XML when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parsed searches default to a 20-result client-side limit and support offset paging, indexer filters, category filters, typed searches, and raw XML output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
