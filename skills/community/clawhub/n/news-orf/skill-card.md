## Description: <br>
Fetches ORF.at news, sport, and science RSS feeds and formats verified headlines into sectioned Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximedogawa](https://clawhub.ai/user/maximedogawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to answer ORF-related news requests by fetching public ORF RSS feeds and presenting Nachrichten, Sport, and Science headlines with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Austria-news prompts may select this ORF-specific source when the user expects source-neutral coverage. <br>
Mitigation: State that results are from ORF feeds and confirm the intended source when source neutrality matters. <br>
Risk: Live RSS feeds may be empty, unavailable, or only partially fetched. <br>
Mitigation: Report affected sections as unavailable and do not invent missing headlines or links. <br>
Risk: Headlines can be misclassified if news, sport, and science feed boundaries are ignored. <br>
Mitigation: Fetch each needed feed separately and place items only under the section matching their source feed and hostname. <br>


## Reference(s): <br>
- [ORF RSS Overview](https://rss.orf.at/) <br>
- [ORF Nachrichten Feed](https://rss.orf.at/news.xml) <br>
- [ORF Sport Feed](https://rss.orf.at/sport.xml) <br>
- [ORF Science Feed](https://rss.orf.at/science.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with section headings and linked headline lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live fetches of ORF RSS feeds; uses feed item titles and links without inventing stories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
