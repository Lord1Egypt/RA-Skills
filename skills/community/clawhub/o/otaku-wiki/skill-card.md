## Description: <br>
番剧/角色百科问答：用 AniList API 快速查番、查角色、查声优与作品关联（无需数据库） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robin797860](https://clawhub.ai/user/Robin797860) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and anime fans use this skill to ask Chinese-language encyclopedia questions about anime titles, characters, voice actors, staff, and work comparisons using AniList lookup results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anime, character, and staff search terms are sent to AniList. <br>
Mitigation: Avoid using private or sensitive text as lookup terms. <br>
Risk: Responses depend on AniList availability and the accuracy of AniList data. <br>
Mitigation: Use the included AniList links to verify important facts before relying on them. <br>
Risk: The skill is designed to answer in Chinese. <br>
Mitigation: Use it when Chinese output is acceptable or request translation after the lookup. <br>


## Reference(s): <br>
- [AniList GraphQL API](https://graphql.anilist.co) <br>
- [ClawHub skill page](https://clawhub.ai/Robin797860/otaku-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Chinese Markdown summaries backed by JSON returned from the bundled AniList CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes AniList links and concise anime, character, staff, or comparison details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
