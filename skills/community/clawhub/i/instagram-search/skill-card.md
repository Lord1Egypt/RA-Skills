## Description: <br>
Instagram Search searches Instagram posts, reels, and profiles through Xpoz MCP to help find influencers, track hashtags, analyze engagement, and export data without a Meta developer account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, researchers, marketers, and developers use this skill to run Instagram content and profile searches, discover influencers or trends, and export search results for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Instagram search queries and returned social-media data are processed through Xpoz. <br>
Mitigation: Use the skill only when sending those queries to Xpoz is acceptable for the intended workflow. <br>
Risk: CSV exports may contain personal or profile data from social-media results. <br>
Mitigation: Export, store, and redistribute results only for a legitimate purpose and in line with platform terms, privacy expectations, and applicable law. <br>


## Reference(s): <br>
- [Instagram Search on ClawHub](https://clawhub.ai/atyachin/instagram-search) <br>
- [Xpoz](https://xpoz.ai) <br>
- [xpoz-setup prerequisite skill](https://clawhub.ai/skills/xpoz-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches can return exported CSV data through Xpoz operation polling, with artifact evidence describing exports up to 64K rows.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
