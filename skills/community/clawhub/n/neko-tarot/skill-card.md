## Description: <br>
引导用户进行数字或实体塔罗占卜，推荐牌阵、抽牌或整理实体牌输入，并生成结合用户意图的解读提示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[senzi](https://clawhub.ai/user/senzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run reflective tarot readings with either simulated card draws or companion-mode input from physical cards. It helps select an appropriate spread, assemble card data, and produce warm Chinese-language interpretation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat tarot output as professional financial, medical, legal, or mental-health advice. <br>
Mitigation: Present readings as entertainment or reflection and direct high-stakes decisions to qualified professionals. <br>
Risk: The skill may require running the bundled Python helper and installing typer or pydantic. <br>
Mitigation: Review and scan the helper before use, and install dependencies only from trusted package sources. <br>
Risk: Manual companion-mode readings can be inaccurate if card IDs, reversal flags, or spread positions are misordered. <br>
Mitigation: Use tarot_index.json for name-to-ID lookup and verify card and reversal order against the selected spread positions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/senzi/neko-tarot) <br>
- [Publisher profile](https://clawhub.ai/user/senzi) <br>
- [README.md](artifact/README.md) <br>
- [TAROT_DATA.md](artifact/TAROT_DATA.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Chinese conversational guidance with CLI commands and optional JSON from the helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled tarot and spread data; readings should be treated as entertainment or reflection, not professional advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
