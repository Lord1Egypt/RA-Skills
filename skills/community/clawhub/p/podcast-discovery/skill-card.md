## Description: <br>
Podcast discovery for Wherever.Audio -- find shows and episodes, generate wherever.audio links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aegrumet](https://clawhub.ai/user/aegrumet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to resolve podcast show or episode requests into playable Wherever.Audio links, including RSS-backed show links and episode links selected from compact feed search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper fetches podcast feed URLs and has a bounded URL-fetching hardening gap when exposed to arbitrary RSS URLs. <br>
Mitigation: Use it for public podcast discovery, prefer RSS URLs resolved through Clawsica, and add URL validation or allowlists before exposing the helper to untrusted inputs. <br>
Risk: Runtime behavior depends on Python feed parsing and fuzzy matching dependencies. <br>
Mitigation: Pin and review Python dependencies in sensitive environments before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aegrumet/podcast-discovery) <br>
- [Clawsica API](references/CLAWSICA_API.md) <br>
- [Local Episode Search Tooling](references/LOCAL_EPISODE_SEARCH.md) <br>
- [Wherever.Audio](https://wherever.audio) <br>
- [Clawsica Public Show Search](https://clawsica.wherever.audio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown responses with Wherever.Audio links and compact JSON from local feed tooling when commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes link-first responses and avoids returning raw RSS XML, full feed dumps, or large metadata blobs.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
