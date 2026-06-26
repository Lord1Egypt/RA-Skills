## Description: <br>
Researches recent discussion and signals for a topic across social, developer, web, and prediction-market sources, then summarizes what people are saying and what appears to be trending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run one-shot topical research, maintain a recurring watchlist, query accumulated research history, and generate briefings from recent findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags under-disclosed credential sharing, including GitHub setup behavior that may transmit a local GitHub CLI token to ScrapeCreators. <br>
Mitigation: Avoid setup --github unless that token sharing is intended; prefer explicit, narrowly scoped API keys and review ~/.config/last30days/.env after setup. <br>
Risk: The security review flags automatic package installation during setup. <br>
Mitigation: Run setup in a controlled environment and review any dependency installation prompts or setup output before continuing. <br>
Risk: The skill persists research history, briefings, and saved reports locally. <br>
Mitigation: Periodically review and prune ~/Documents/Last30Days, ~/.local/share/last30days, and saved briefing files for sensitive topics. <br>
Risk: The skill can use multiple third-party APIs, optional paid research modes, and configurable outbound webhook delivery. <br>
Mitigation: Set budget limits, enable only required providers, and review webhook delivery settings before running recurring watchlist jobs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mvanhorn/last30days-v3-beta) <br>
- [One-Shot Research Mode](references/research.md) <br>
- [Watchlist Management](references/watchlist.md) <br>
- [Morning Briefing](references/briefing.md) <br>
- [History & Knowledge Query](references/history.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research reports and briefings, JSON script output, and inline shell commands or configuration updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local research history, saved reports, briefings, and user configuration files.] <br>

## Skill Version(s): <br>
3.0.0-open (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
