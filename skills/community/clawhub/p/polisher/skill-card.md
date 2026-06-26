## Description: <br>
Polishes user-provided text by fixing grammar, improving wording, and making prompts sound natural and concise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Supremes](https://clawhub.ai/user/Supremes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and prompt authors use this skill to rewrite text for clearer, more natural phrasing while preserving the original meaning. It is useful for quick grammar fixes, prompt wording improvements, and concise alternative phrasings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Polished text may unintentionally change the user's intended meaning. <br>
Mitigation: Review the polished output against the original text; the skill instructs the agent to preserve intent exactly. <br>
Risk: The skill could introduce facts that were not present in the source text if outputs are accepted without review. <br>
Mitigation: Use the skill's no-new-facts constraint and check rewritten text before using it in final prompts or communications. <br>
Risk: Ambiguous source text may need clarification before it can be polished reliably. <br>
Mitigation: Use the Notes field to flag ambiguity and request clarification when wording could support multiple meanings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Supremes/polisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise labeled sections: Polished, Alternative, and Notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves original meaning and avoids adding facts not present in the source text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
