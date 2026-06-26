## Description: <br>
Need A Hug helps agents respond with lightweight emotional first aid when users are distressed or explicitly ask for comfort, while avoiding therapy, diagnosis, or medical care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lonelymoon87](https://clawhub.ai/user/lonelymoon87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and operators use this skill to make assistants respond with warmth, grounding, and gentle companionship when users are overwhelmed, ashamed, lonely, anxious, grieving, burned out, or asking for comfort. It also guides the assistant back to task work in smaller steps after the user is steadier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implicit invocation can shift the assistant into comfort mode when the user sounds distressed, even without an explicit command. <br>
Mitigation: Review whether implicit invocation is desired; if not, require explicit triggers such as /hug or /need-a-hug before activating the skill. <br>
Risk: Users may mistake warm emotional support for therapy, diagnosis, medical care, or emergency support. <br>
Mitigation: Keep the skill's boundary language intact: the assistant must not claim clinical authority, diagnose, treat, or replace emergency services or professional care. <br>
Risk: Crisis situations require safety-first handling rather than ordinary comfort phrasing. <br>
Mitigation: Follow the crisis boundary in the skill: prioritize immediate real-world safety, avoid methods or concealment, and direct the user to local emergency services or a trusted nearby person. <br>
Risk: Optional memory could collect sensitive personal information if used too broadly. <br>
Mitigation: Store only low-sensitivity preferences the user explicitly asks to remember, and do not store crisis details, medical history, trauma details, third-party private information, or speculative labels. <br>


## Reference(s): <br>
- [Comfort Protocol](references/comfort-protocol.md) <br>
- [Comfort Language Corpus](references/comfort-language-corpus.md) <br>
- [Counseling-Lite Patterns](references/counseling-lite-patterns.md) <br>
- [Optional Comfort Memory Template](references/memory-template.md) <br>
- [NCBI Bookshelf: Motivational Interviewing](https://www.ncbi.nlm.nih.gov/books/n/tip35v2/ch3/) <br>
- [SAMHSA: Trauma-Informed Approaches](https://www.samhsa.gov/mental-health/trauma-violence/trauma-informed-approaches-programs) <br>
- [TIME: What to Say to Someone Who Is Depressed](https://time.com/7291435/worst-thing-to-say-depression-depressed/) <br>
- [Psych Central: What to Say to Someone with Depression](https://psychcentral.com/depression/things-you-should-and-not-say-to-a-depressed-person) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Natural-language text or Markdown responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No shell commands or external tool calls are required by the skill.] <br>

## Skill Version(s): <br>
0.3.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
