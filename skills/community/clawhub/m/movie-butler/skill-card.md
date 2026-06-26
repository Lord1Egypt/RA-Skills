## Description: <br>
整合 TMDB 与 Emby/Plex 的观影助手，用于电影查询、媒体库检索、观影记录、统计报告和个性化推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzhilei951](https://clawhub.ai/user/duzhilei951) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People who manage a personal Emby/Plex movie library can use this skill to look up film metadata, check local availability, record viewing history and ratings, and receive recommendations based on taste, mood, work context, and recent additions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact ships real-looking API and server defaults. <br>
Mitigation: Replace shipped defaults with your own least-privilege TMDB and Emby credentials, and rotate any key that may have been exposed. <br>
Risk: An Emby token may be sent to third-party movie APIs. <br>
Mitigation: Do not run the current code with an Emby token until request headers are restricted to Emby URLs only. <br>
Risk: Viewing history, ratings, feelings, mood, and work context can be stored in plaintext. <br>
Mitigation: Treat movie-memory.md as private and avoid using the skill on shared machines unless plaintext local records are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duzhilei951/movie-butler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with movie details, recommendation lists, statistics, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local markdown memory file with viewing history, ratings, weekly plans, and context notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
