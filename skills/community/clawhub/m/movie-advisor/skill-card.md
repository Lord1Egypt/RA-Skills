## Description: <br>
Suggests movies and TV shows based on taste, mood, or context, with ratings, cast, runtime, and region-dependent streaming guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to choose movies or TV shows, compare title fit, and prepare concise recommendation reports with factual metadata and where-to-watch caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Movie requests entered through the helper script may be retained in local command history. <br>
Mitigation: Avoid sensitive personal or account details in requests, and delete data/movie_advisor_data.json if retained history is not desired. <br>
Risk: Optional Python dependencies are unpinned. <br>
Mitigation: Install dependencies in an isolated environment and review dependency versions before use. <br>


## Reference(s): <br>
- [Movie Advisor Guide](references/movie_advisor_guide.md) <br>
- [TMDb API](https://developer.themoviedb.org/docs/getting-started) <br>
- [OMDb API](https://www.omdbapi.com/) <br>
- [JustWatch](https://www.justwatch.com) <br>
- [Public APIs - Entertainment](https://github.com/public-apis/public-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendation report with tables; helper CLI responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streaming availability is region-dependent and should be verified locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
