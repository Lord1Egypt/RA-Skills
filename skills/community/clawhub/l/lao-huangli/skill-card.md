## Description: <br>
Use when users ask for 老黄历/黄历/择日/宜忌/冲煞/干支/节气 explanations, or need a reproducible engineering workflow to compute calendar fields and derive traditional almanac recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cikichen](https://clawhub.ai/user/cikichen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compute and explain Lao Huangli calendar fields, solar terms, sexagenary-cycle values, auspicious and inauspicious activities, and rule-derived almanac recommendations. It is intended for cultural and calendar reference with explicit rule-version and boundary disclosures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may install Python dependencies and download a JPL ephemeris file into a local cache for astronomical calculations. <br>
Mitigation: Review dependency installation and cache behavior before deployment, especially in restricted or offline environments. <br>
Risk: Almanac recommendations may be mistaken for authoritative legal, medical, financial, or safety advice. <br>
Mitigation: Present results as cultural and calendar reference only, and keep explicit disclaimers that they do not replace professional or safety-critical decisions. <br>
Risk: Different Huangli rule profiles can produce different recommendations for the same date because of year-boundary, day-boundary, and ruleset choices. <br>
Mitigation: Include the selected profile, timezone, year boundary, day boundary, ruleset version, and source references in outputs. <br>


## Reference(s): <br>
- [Calculation Pipeline](references/calculation-pipeline.md) <br>
- [Rules and Variants](references/rules-and-variants.md) <br>
- [Qinding Xiejibianfangshu on Wikisource](https://zh.wikisource.org/wiki/%E6%AC%BD%E5%AE%9A%E5%8D%94%E7%B4%80%E8%BE%A8%E6%96%B9%E6%9B%B8_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-style structured explanations, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish deterministic calendar calculations from rule-derived almanac judgments and include timezone, boundary, ruleset, and source-reference context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
