## Description: <br>
Detects 43 AI writing patterns and rewrites text in 5 voice profiles. Use when (1) AI text reads like a chatbot, (2) preparing content for publication, (3) auditing prose for AI tells, (4) editing a file in place. Outputs a 0-100 AI-tell score on demand. Pure Markdown, zero dependencies, no network calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aboudjem](https://clawhub.ai/user/aboudjem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, developers, and other external users use this skill to detect AI-like writing patterns, rewrite prose in a chosen voice, score AI-tell density, or apply targeted in-place edits to Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make AI-assisted writing harder to identify as AI-assisted. <br>
Mitigation: Use it only where that transformation is acceptable, and keep human review accountable for publication, authorship, or disclosure requirements. <br>
Risk: Edit mode can modify local Markdown files in place. <br>
Mitigation: Run detect or rewrite mode first, review proposed changes, and check diffs before keeping edits to important files. <br>
Risk: Optional brand context may include sensitive writing samples or private material. <br>
Mitigation: Keep secrets and confidential content out of humanizer-context.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aboudjem/humanizer-skill) <br>
- [Hacker News discussion on AI writing patterns](https://news.ycombinator.com/item?id=46646939) <br>
- [Gone Travelling Productions: AI giveaways in writing](https://gonetravellingproductions.com/2025/08/20/ai-giveaways-in-writing/) <br>
- [Writewithai: dead giveaways in AI content](https://writewithai.substack.com/p/10-dead-giveaways-your-content-screams) <br>
- [Wikipedia: signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [AI Detectors: spotting AI writing patterns](https://www.aidetectors.io/blog/spotting-ai-writing-patterns) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown reports, rewritten text, edit summaries, and optional score headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit local Markdown files in place when invoked with edit mode and a file path.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
