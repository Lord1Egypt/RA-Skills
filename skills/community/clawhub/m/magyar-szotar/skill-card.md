## Description: <br>
Magyar szavak jelentésének, szinonimáinak, szólások magyarázatának és nyelvi elemzésének gyors lekérdezését támogatja helyi referenciafájlokból vagy opcionális webes forrásokból. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Izsook](https://clawhub.ai/user/Izsook) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers can use this skill to answer Hungarian dictionary questions, find synonyms, explain proverbs and idioms, and perform lightweight Hungarian language analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional web fallback can disclose queried words or phrases to public dictionary services. <br>
Mitigation: Use local reference files for private, confidential, or sensitive text; only allow web lookup when the user accepts that queried terms may leave the environment. <br>
Risk: Local dictionary coverage is limited and may not contain every Hungarian term or idiom. <br>
Mitigation: State when a word is not found locally, cite the reference used when available, and avoid presenting uncertain fallback results as definitive. <br>


## Reference(s): <br>
- [Arcanum - Magyar Ertelmezo Szotar](references/arcanum-ertsz.md) <br>
- [Magyar Kozmondasok es Szolasok](references/kozmondasok.md) <br>
- [Magyar Szotar JSON](references/magyar-szotar.json) <br>
- [Arcanum Magyar Ertelmezo Szotar](https://www.arcanum.com/hu/online-kiadvanyok/Lexikonok-a-magyar-nyelv-ertelmezo-szotara-1BE8B/) <br>
- [Hungarian Wiktionary](https://hu.wiktionary.org/) <br>
- [Sztaki Dictionary](https://dict.sztaki.hu/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with definitions, synonyms, examples, and source notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local reference entries first and optional public dictionary lookups when local coverage is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
