## Description: <br>
Searches Podcast Index for podcasts and episodes, retrieves feed and episode details, and summarizes authenticated API responses for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ComicStrip](https://clawhub.ai/user/ComicStrip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when users need podcast discovery, episode lookup, trending podcast information, or metadata from Podcast Index. It is intended for authenticated, read-only lookups against the Podcast Index API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Podcast Index API Documentation](https://podcastindex.org/api/docs) <br>
- [ClawHub release page](https://clawhub.ai/ComicStrip/podcastindex) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Markdown summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PODCASTINDEX_API_KEY and PODCASTINDEX_API_SECRET. Avoid exposing authentication headers, API keys, secrets, or generated hashes in logs or responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
