## Description: <br>
Automatically discovers installed search-related skills, runs them in parallel, deduplicates results by URL, and returns an aggregated search summary with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chn012cjus](https://clawhub.ai/user/chn012cjus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to broaden web search coverage by aggregating locally installed search engines and returning a consolidated result list. It is useful when a single search provider may miss relevant sources or when result deduplication across multiple search skills is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically discovers and runs other local search-like skills with the user's privileges. <br>
Mitigation: Install and use it only in environments where the discovered search skills are trusted, audited, or restricted to an approved set. <br>
Risk: Fallback searches may send queries to Bing when local engines return no results. <br>
Mitigation: Avoid sensitive queries unless external search fallback is acceptable, or modify the skill to make fallback explicit and optional. <br>
Risk: Shared temporary JSON files may expose or mix query and result data across runs. <br>
Mitigation: Use isolated per-run temporary files and clear temporary data after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chn012cjus/multi-engine-auto-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text search report with headings, summaries, source names, titles, snippets, and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are aggregated from discovered local search skills, deduplicated by URL, and may fall back to Bing when no local results are returned.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
