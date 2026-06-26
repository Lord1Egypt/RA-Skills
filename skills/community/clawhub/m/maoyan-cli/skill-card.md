## Description: <br>
Looks up Maoyan cinema showtimes, searches movies, finds theaters showing a movie, and returns structured data that an agent can summarize for users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsLand-x](https://clawhub.ai/user/IsLand-x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to query Maoyan for cinema showtimes, theater listings, movie search results, theaters showing a selected movie, and movie details, then summarize the JSON results for end users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script and may send movie queries or optional location coordinates to Maoyan. <br>
Mitigation: Install only when comfortable running the script; avoid providing exact latitude and longitude unless nearby-cinema sorting is needed. <br>


## Reference(s): <br>
- [Maoyan CLI API Reference](reference.md) <br>
- [Maoyan CLI Examples](examples.md) <br>
- [Maoyan Mobile Site](https://m.maoyan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Maoyan cinema, showtime, price, movie, poster URL, and ticketing URL data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
