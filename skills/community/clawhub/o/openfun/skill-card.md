## Description: <br>
Create viral short-form videos using AI by analyzing trending patterns, generating original content, rendering videos, and downloading MP4s. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyluvis](https://clawhub.ai/user/andyluvis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developer agents use this skill to find short-form video trends, remix a trend into branded original content, render the result, and download the finished video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on the third-party openfun-cli npm package and OpenFun service. <br>
Mitigation: Install only from the expected npm package and use the skill only when the publisher and service are trusted. <br>
Risk: OpenFun login persists a token in ~/.openfun/config.json. <br>
Mitigation: Treat the config file as sensitive, avoid printing or sharing it, and remove stored credentials when access is no longer needed. <br>
Risk: Automated trend, remix, render, and download runs can consume plan credits. <br>
Mitigation: Set explicit limits for trend counts, remixes, renders, and downloads before running batches. <br>


## Reference(s): <br>
- [OpenFun Skill Page](https://clawhub.ai/andyluvis/openfun) <br>
- [OpenFun Website](https://www.openfun.ai) <br>
- [OpenFun CLI Repository](https://github.com/andyluvis/openfun-cli) <br>
- [OpenFun CLI npm Package](https://www.npmjs.com/package/openfun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OpenFun CLI data commands emit JSON by default; download commands can write MP4 files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
