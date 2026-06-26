## Description: <br>
将正常中文文本转换为火星文（2005-2010年代非主流网络文体），使用 611 个汉字映射生成可辨认的非主流风格文本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cantoneyes](https://clawhub.ai/user/cantoneyes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Chinese text into readable 火星文 for novelty, social, or stylistic text generation. The script supports full conversion, probability-controlled conversion, deterministic output with a seed, and per-character mapping lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised --json option is currently unreliable because the script calls json.dumps without importing json. <br>
Mitigation: Use plain-text output for normal operation, or add the missing json import and retest before relying on JSON output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cantoneyes/mars-text-translator) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON when the script's --json option is fixed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conversion output is randomized unless a seed is supplied; unmapped characters are preserved.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and bundled version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
