## Description: <br>
Searches iQIYI for movies, TV dramas, variety shows, and related video content, returning search results and playback links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingcl](https://clawhub.ai/user/xingcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search iQIYI for films, TV shows, variety content, and playable iQIYI links. It is useful when a user asks what content is available on iQIYI or requests a playback link for a known title. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports that the documented search.sh flow can execute locally crafted Python if a search term or returned page content is maliciously shaped. <br>
Mitigation: Review before installing or executing, avoid sensitive or adversarial search terms, and prefer the file-based parser approach in search_v2.sh. <br>
Risk: The skill depends on the globally installed agent-browser command. <br>
Mitigation: Verify the agent-browser package source and version before installing it globally. <br>
Risk: Search results depend on the iQIYI web page structure and may fail or return incomplete results if the site changes. <br>
Mitigation: Treat returned links and metadata as best-effort search results and validate important results in the browser before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingcl/iqiyi-search) <br>
- [iQIYI search endpoint](https://so.iqiyi.com/so/q_${ENCODED_KEYWORD}) <br>
- [iQIYI website](https://www.iqiyi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON search results emitted by a shell-driven browser automation flow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 results with keyword, count, title, type, description, url, and rating fields when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
