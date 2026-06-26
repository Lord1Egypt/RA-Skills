## Description: <br>
Standardized literature search workflow that integrates Tavily, PubMed, BGPT paper search, OpenAlex, and related academic search skills from query analysis through literature acquisition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthwalking](https://clawhub.ai/user/earthwalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic support agents use this skill to run a six-stage literature search workflow for academic papers, scale validation, reviews, and research methodology. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes and uses a bundled Tavily API key and sends literature-search queries to Tavily. <br>
Mitigation: Remove the bundled key, rotate or revoke it if you own it, and require users to provide TAVILY_API_KEY through a proper secret mechanism before use. <br>
Risk: The script writes Markdown search reports into the working directory. <br>
Mitigation: Run it in a workspace where generated literature_search_*.md files are expected and review the report before relying on citations or links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earthwalking/literature-search-workflow) <br>
- [Tavily Search API endpoint used by the script](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report files and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped literature_search_*.md reports in the working directory and sends search queries to Tavily when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
