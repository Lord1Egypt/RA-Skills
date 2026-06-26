## Description: <br>
Universal travel planning skill for OpenClaw agents. Plan itineraries, check weather, discover attractions, and estimate budgets through natural conversation using free APIs, with no API key required for core features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asif2BD](https://clawhub.ai/user/Asif2BD) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to generate destination itineraries, weather summaries, travel guides, attraction lists, and budget estimates for travel planning conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination lookups are sent to public travel and weather providers. <br>
Mitigation: Avoid entering highly sensitive travel plans and review whether use of Nominatim, Wikivoyage, Open-Meteo, or optional Visual Crossing is acceptable for the deployment context. <br>
Risk: Raw API responses are cached locally in a SQLite database. <br>
Mitigation: Delete or redirect ~/.openclaw/cache/tour-planner.db, or set TOUR_PLANNER_CACHE_PATH, when local retention of lookup data is not desired. <br>
Risk: Installing the package builds the better-sqlite3 native module. <br>
Mitigation: Install in an environment where native Node.js dependencies are allowed and review dependency provenance before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/Asif2BD/openclaw-tour-planner) <br>
- [Project Website](https://openclaw.tours) <br>
- [Project Documentation](https://openclaw.tours/docs) <br>
- [Nominatim Search API Documentation](https://nominatim.org/release-docs/develop/api/Search/) <br>
- [Open-Meteo Forecast Documentation](https://open-meteo.com/en/docs#weathervariables) <br>
- [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api) <br>
- [Wikivoyage API Endpoint](https://en.wikivoyage.org/w/api.php) <br>
- [better-sqlite3 Dependency](https://github.com/WiseLibs/better-sqlite3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown travel plans and summaries, with JSON available for agent processing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include itineraries, weather summaries, destination guides, attraction lists, budget estimates, and packing guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
