## Description: <br>
Query Korean multiplex box office rankings and upcoming movie data from Lotte Cinema, CGV, and Megabox, enriched with KOBIS movie details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uyeong](https://clawhub.ai/user/uyeong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to answer Korean cinema questions, including current box office rankings, upcoming releases, recommendations by genre, director, actor, or rating, and comparisons across Korean multiplex chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Movie queries are sent to the disclosed public GitHub Pages API, so unrelated private information in prompts could be exposed unnecessarily. <br>
Mitigation: Limit queries to the movie, cinema chain, genre, date, rating, director, or actor details needed for the cinema task. <br>
Risk: Some KOBIS enrichment fields can be null, and public movie data may lag real-world schedule changes. <br>
Mitigation: Null-check movie details before using them and avoid guessing missing genres, directors, actors, or release details. <br>


## Reference(s): <br>
- [K Cinema Bridge API](https://uyeong.github.io/k-cinema-bridge/) <br>
- [OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown responses with movie lists, comparisons, and source-backed recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tables; results depend on the public API data and nullable KOBIS detail fields.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
