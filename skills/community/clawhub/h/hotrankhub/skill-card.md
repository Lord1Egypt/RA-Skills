## Description: <br>
HotRank Hub lets agents retrieve standardized JSON hot-list data from 47 public platforms through a third-party HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rpeng666](https://clawhub.ai/user/Rpeng666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer trend and hot-topic questions by retrieving current rankings from social, video, technology, finance, news, entertainment, lifestyle, and community platforms. Agents can return a single platform list, compare platforms, or summarize cross-platform topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the disclosed third-party service at airouter.tech for public trending-topic lookups. <br>
Mitigation: Install and enable it only where outbound calls to that service are acceptable, and avoid sending private or sensitive user data in platform queries. <br>
Risk: Ambiguous user requests may map to the wrong platform or an overly broad set of hot lists. <br>
Mitigation: Ask the user to confirm or narrow the target platform when the intended source is unclear. <br>
Risk: Scheduled polling or repeated multi-platform lookups can create unnecessary traffic. <br>
Mitigation: Keep polling opt-in, apply local caching aligned with the documented five-minute refresh window, and rate-limit concurrent requests. <br>
Risk: Hot-list data is sourced from third-party platforms and may be incomplete, stale, or inaccurate. <br>
Mitigation: Present results as public trend signals and verify important claims against primary sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Rpeng666/hotrankhub) <br>
- [Publisher profile](https://clawhub.ai/user/Rpeng666) <br>
- [HotRank Hub API base](https://airouter.tech/api) <br>
- [HotRank Hub homepage](https://airouter.tech) <br>
- [API reference](artifact/api-reference.md) <br>
- [Usage examples](artifact/examples.md) <br>
- [Supported source list](artifact/sources.json) <br>
- [User guide](artifact/USER_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON payloads and JavaScript, TypeScript, or curl examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying API returns read-only public hot-list data with code, message, data, and timestamp fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
