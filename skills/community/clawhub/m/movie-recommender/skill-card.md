## Description: <br>
Recommends movies from mood, genre, cast, director, or year preferences, checks Douban ratings, and helps manage watched and want-to-watch lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an agent for movie discovery can ask for recommendations by mood or genre, look up movie ratings and details, view a Top250 list, and maintain simple watched or want-to-watch records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Movie searches are sent to Douban during live lookup. <br>
Mitigation: Use the skill only when sharing movie queries with Douban is acceptable. <br>
Risk: Watched and want-to-watch preferences are saved as local JSON files. <br>
Mitigation: Delete the generated JSON files when movie preferences are sensitive on the device. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/movie-recommender) <br>
- [Douban Developers](https://developers.douban.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted conversational responses with movie recommendations, ratings, lists, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may reflect live Douban lookups, cached Douban data, or bundled fallback movie data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
