## Description: <br>
Learns a user's writing style per connected outreach channel by collecting outbound samples, running a prompt-learning workflow, and saving reusable style prompts for future drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milstan](https://clawhub.ai/user/milstan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Outreach operators and agents use this skill to learn a tenant's per-channel writing style from opted-in sent-message history and produce reusable style prompts for drafting email, social, chat, or messaging outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and persist private sent-message history from connected accounts. <br>
Mitigation: Use only after opt-in consent, limit connected channels and accounts, prefer official APIs or exports, and review or delete raw training files and learned style profiles after use. <br>
Risk: Learned style quality can be weak when sample volume is low or message classification is inaccurate. <br>
Mitigation: Review training reports, sample counts, confidence notes, and style scores before relying on learned prompts for outreach. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/milstan/outclaw-style) <br>
- [Outclaw Homepage](https://github.com/leadbay/outclaw) <br>
- [Prompt Learning Protocol](https://gist.github.com/milstan/3b12f938f344f4ae1f511dd19e56adce) <br>
- [Style Learning Reference](references/style-learning.md) <br>
- [Style Learner Subagent](agents/style-learner.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown style prompt files with YAML frontmatter, compact training reports, and memory observations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write raw sample JSONL files and learned style files under configured tenant paths.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 2.1.33) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
