## Description: <br>
Searches and summarizes recent robotics and related research papers from sources such as CrossRef and Google Scholar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyp41](https://clawhub.ai/user/wyp41) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and robotics developers use Paper Scout to find recent papers, filter them by topic, venue, and recency, and produce a structured literature digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches public academic websites and saves a dated Markdown report to the user's Desktop. <br>
Mitigation: Install only if that behavior is acceptable; change the output path or ask before writing when the Desktop is shared, synced, or contains sensitive research context. <br>
Risk: Google Scholar backup scraping may require interactive browser sessions and can be incomplete on JavaScript-heavy pages. <br>
Mitigation: Use CrossRef as the primary source and review the generated digest for missing fields, duplicates, and source quality before relying on it. <br>


## Reference(s): <br>
- [Paper Scout on ClawHub](https://clawhub.ai/wyp41/paper-scout) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown digest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves a dated academic digest with title, venue, year, authors, abstract, and contribution fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
