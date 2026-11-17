## Description:

Movie and TV recommendation and critique assistant. Suggests films and series from taste, mood, or context; surfaces ratings, cast, runtime, and where to watch on major global streaming platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to choose movies or TV shows by taste, mood, occasion, similar titles, and runtime constraints. It helps produce concise recommendation reports with factual metadata, caveats, and region-dependent streaming guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI stub stores user queries and command history in a local plaintext JSON data file.

Mitigation: Review local data retention before use, avoid entering sensitive viewing preferences, and clear or relocate the data file when persistence is not needed.

Risk: The documentation asks users to install unused unpinned Python dependencies.

Mitigation: Pin and audit dependencies before installation, or skip installing optional packages until real API integration requires them.

Risk: Movie ratings, metadata, and streaming availability can be incorrect or stale if not sourced at response time.

Mitigation: Use TMDb, OMDb, JustWatch, provider search, or user-provided data for factual claims, and label availability as region- and date-dependent.

## Reference(s):

- [Movie Advisor Guide](references/movie_advisor_guide.md)
- [TMDb API](https://developer.themoviedb.org/docs/getting-started)
- [OMDb API](https://www.omdbapi.com/)
- [JustWatch](https://www.justwatch.com)
- [Public APIs - Entertainment](https://github.com/public-apis/public-apis)
- [Movie Advisor ClawHub Page](https://clawhub.ai/clawkk/skills/movie-advisor)
- [clawkk Publisher Profile](https://clawhub.ai/user/clawkk)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, JSON]

**Output Format:** [Markdown recommendation report with tables and optional JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendation reports should mark missing data as unavailable and note that streaming availability is region-dependent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
