## Description: <br>
Human-like writing for daily chat and social media only, routing Chinese, English, or mixed-language requests into daily messages or platform-specific social posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unicorn82](https://clawhub.ai/user/unicorn82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to rewrite or draft daily chat messages and social media posts that sound more natural while preserving the provided facts. It is scoped to DMs/texts and platform-specific posts for X/Twitter, Reddit, LinkedIn, Instagram, TikTok, Xiaohongshu/RedNote, WeChat Moments, and generic social posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chat or social text could be misused to impersonate someone or hide AI involvement where disclosure is expected. <br>
Mitigation: Use the skill as a drafting and tone aid; do not impersonate people, and disclose AI assistance where policy, platform rules, or context require it. <br>
Risk: User-provided chat samples or writing examples may contain names, private details, or sensitive context. <br>
Mitigation: Remove personal and sensitive details before reusing samples or turning them into style examples. <br>
Risk: Humanization can make unsupported details sound more believable if facts are added carelessly. <br>
Mitigation: Keep the factual-integrity gate: do not invent facts, quotes, experiences, times, numbers, or situational anchors that the user did not provide. <br>


## Reference(s): <br>
- [Scenario Router](artifact/references/scenario-router.md) <br>
- [Prompt Recipes](artifact/references/prompt-recipes.md) <br>
- [Registers](artifact/references/registers.md) <br>
- [AI Tells](artifact/references/ai-tells.md) <br>
- [Phrase Blacklist](artifact/references/phrase-blacklist.md) <br>
- [Human Checklist](artifact/references/human-checklist.md) <br>
- [Few-shot Pack](artifact/references/fewshot-pack.md) <br>
- [Language Extension](artifact/references/language-extension.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown, depending on the requested chat or social post format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional short notes about what changed when useful for iterative refinement.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
