## Description: <br>
Search, compare, and monitor 대한민국 property listings from 네이버 부동산 with natural-language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn Korean real-estate questions into Naver Real Estate searches, candidate complex comparisons, listing summaries, and price-watch drafts. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: The skill wraps a local tmp/naverland-scrapper dependency. <br>
Mitigation: Inspect or otherwise trust that local dependency before installation or execution. <br>
Risk: Search queries, watch rules, and candidate cache files can reveal property interests or alert thresholds. <br>
Mitigation: Avoid unnecessary personal details in queries, and review or clear watch-rules.json and candidate-cache.json when that state is sensitive. <br>
Risk: Live Naver listing searches can be rate limited or incomplete, especially for broad candidate discovery. <br>
Mitigation: Prefer direct complex URLs or IDs, narrow ambiguous searches to one to three candidate complexes, and verify listings before decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twbeatles/naver-real-estate-search) <br>
- [README](README.md) <br>
- [Design notes](references/design.md) <br>
- [Candidate seed builder notes](references/candidate-seed-builder.md) <br>
- [Candidate seeds](references/candidate-seeds.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Korean text or Markdown summaries, JSON records, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Naver listing URLs and local watch or candidate-cache JSON state.] <br>

## Skill Version(s): <br>
2026.4.16 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
