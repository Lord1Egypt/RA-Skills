## Description: <br>
Provides Jin10 financial news alerts, cached recent item browsing, detail lookup, and impact analysis for Hong Kong equities and related markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akinding](https://clawhub.ai/user/akinding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve Jin10 financial news, inspect item details, and request concise impact analysis for Hong Kong stocks, the Hang Seng Tech Index, Tencent, and Alibaba. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package references Python scripts and TOOLS.md that are not included in the artifact, so the runtime behavior is not fully reviewable from this release. <br>
Mitigation: Ask the publisher to include the referenced scripts and documentation, then review the complete package before installation. <br>
Risk: The skill describes token use and a background fetcher without explicit controls for lifecycle or cleanup. <br>
Mitigation: Document token handling and provide clear start, stop, disable, and cleanup controls before running the background fetcher. <br>
Risk: Financial impact analysis and related stock recommendations may be incomplete or unsuitable for trading decisions. <br>
Mitigation: Treat outputs as informational, verify against authoritative market sources, and apply human review before acting on financial conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akinding/jin10-news) <br>
- [Publisher profile](https://clawhub.ai/user/akinding) <br>
- [Jin10 data source](https://www.jin10.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown text with command examples, news summaries, item details, and impact analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recent alerts are read from a local cache when available; detail and deep-analysis outputs are selected by item number.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
