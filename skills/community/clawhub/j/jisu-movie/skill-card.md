## Description: <br>
Looks up current movies, theater showtimes, movie details, and city theater lists through JisuAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer movie availability, theater, showtime, and movie-detail questions in Chinese-language agent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Movie names, city or theater identifiers, dates, keywords, and the JisuAPI key are sent to JisuAPI. <br>
Mitigation: Use only when sharing those values with JisuAPI is acceptable, and avoid precise personal location or sensitive context unless needed. <br>
Risk: Results depend on JisuAPI availability, account permissions, rate limits, and movie data coverage. <br>
Mitigation: Handle API errors explicitly and verify showtimes, prices, and ticket links before relying on recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/jisu-movie) <br>
- [JisuAPI Movie API Documentation](https://www.jisuapi.com/api/movie/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses with concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and JISU_API_KEY; calls JisuAPI over HTTPS.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
