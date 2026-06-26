## Description: <br>
通过紫薇斗数解释命运 A skill to interpret fate using Ziwei astrology principles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HerbertHe](https://clawhub.ai/user/HerbertHe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can provide birth date, birth time, calendar type, leap-month status, and gender so an agent can calculate a Ziwei astrology chart, summarize astrolabe and horoscope data, and provide interpretive fate guidance. The skill is intended for astrology interpretation and reflective guidance, not deterministic or professional advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise birth details and gender may be embedded in a third-party ziwei.pub chart URL. <br>
Mitigation: Prefer the local Node.js and iztro calculation path when possible, and open or share the ziwei.pub URL only after the user is comfortable exposing those details. <br>
Risk: Local chart calculation depends on a trusted Node.js runtime and iztro installation. <br>
Mitigation: Use a trusted Node.js 18 or newer environment and a trusted iztro installation before running generated code. <br>
Risk: Astrology outputs may be overread as deterministic life guidance. <br>
Mitigation: Present conclusions as interpretive astrology and reflective advice, and avoid replacing professional, medical, legal, financial, or safety-critical judgment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HerbertHe/interpret-fate-via-ziwei) <br>
- [Ziwei astrolabe chart](https://ziwei.pub/astrolabe/) <br>
- [Iztro discussions](https://github.com/SylarLong/iztro/discussions) <br>
- [Astrolabe reference](docs/learn-astrolabe.md) <br>
- [Palace reference](docs/learn-palace.md) <br>
- [Star reference](docs/learn-star.md) <br>
- [Mutagen reference](docs/learn-mutagen.md) <br>
- [Pattern reference](docs/learn-pattern.md) <br>
- [Setup reference](docs/learn-setup.md) <br>
- [Ziwei Doushu Complete Book](docs/learn-ancient-book.md) <br>
- [Stars Q&A reference](docs/learn-ancient-book-qa.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with explanatory text, a generated chart URL, and optional Node.js code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Ziwei chart data, horoscope period data, interpretive conclusions, and user-facing advice] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
