## Description: <br>
Provides real-time verified news briefs and detailed intelligence reports from The Polaris Report, including category filters, search, trending briefs, confidence ratings, and bias ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JohnnyTarrr](https://clawhub.ai/user/JohnnyTarrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve current news briefs, generate topic-specific intelligence briefs, search verified brief archives, and inspect trending topics through The Polaris Report API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News queries, search terms, and brief topics are sent to The Polaris Report API. <br>
Mitigation: Avoid submitting secrets, private client information, or sensitive internal research unless the provider's privacy and retention practices are acceptable. <br>
Risk: The skill depends on an external news API for its results. <br>
Mitigation: Review returned briefs, confidence ratings, and links before using the output in decisions or downstream publications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JohnnyTarrr/polaris-news) <br>
- [The Polaris Report](https://thepolarisreport.com) <br>
- [API Documentation](https://thepolarisreport.com/docs) <br>
- [Agent Integration Guide](https://thepolarisreport.com/agents) <br>
- [Privacy Policy](https://thepolarisreport.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text or Markdown-like news briefs with links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include headlines, summaries, categories, confidence ratings, bias ratings, counter-arguments, result counts, and links returned by The Polaris Report API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
