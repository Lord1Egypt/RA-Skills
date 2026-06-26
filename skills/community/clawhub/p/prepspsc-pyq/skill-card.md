## Description: <br>
PrepSPSC PYQ API helps agents search Sikkim PSC previous year questions, generate mock tests from exam patterns, and return MCQs with answers, explanations, topics, cognitive levels, and difficulty metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[himyeticapital](https://clawhub.ai/user/himyeticapital) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External learners, educators, and developers use this skill for SPSC exam preparation, previous-year-question search, mock test generation, progress tracking, and reference examples for AI question generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses PrepSPSC's external API and requires an API key. <br>
Mitigation: Keep the API key private, prefer the PREPSPSC_API_KEY environment variable, and review generated shell commands before running them. <br>
Risk: Optional progress, analytics, bookmark, and leaderboard features can store study activity with PrepSPSC. <br>
Mitigation: Avoid personally identifying user IDs or sensitive bookmark notes, and use those features only when study activity storage is acceptable. <br>


## Reference(s): <br>
- [PrepSPSC website](https://prepspsc.com) <br>
- [PrepSPSC developer API key page](https://prepspsc.com/developers) <br>
- [ClawHub skill page](https://clawhub.ai/himyeticapital/prepspsc-pyq) <br>
- [PrepSPSC PYQ API endpoint](https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external API responses containing MCQs, answers, explanations, topics, cognitive levels, difficulty, progress, analytics, bookmarks, or leaderboard data.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
