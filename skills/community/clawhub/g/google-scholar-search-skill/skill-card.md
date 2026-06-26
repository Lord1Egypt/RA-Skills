## Description: <br>
Search academic literature through Google Scholar with keyword, author, and year filters, retrieve author profile details, and export results as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, students, and developers use this skill to find academic papers, explore author profiles, filter literature searches by author or publication year, and save structured search results for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and author lookups are sent to Google Scholar or related libraries. <br>
Mitigation: Avoid private, confidential, or sensitive research terms when privacy matters. <br>
Risk: Google Scholar scraping can be blocked, rate-limited, or return variable results. <br>
Mitigation: Use official or more stable APIs such as Semantic Scholar or PubMed when reliability is required. <br>
Risk: The skill can write JSON output to a user-specified path. <br>
Mitigation: Save output files to a dedicated non-critical directory and review paths before execution. <br>
Risk: Installing dependencies or remote packages introduces normal supply-chain risk. <br>
Mitigation: Install from trusted sources, review installer commands, and consider pinning dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JackKuo666/google-scholar-search-skill) <br>
- [Google Scholar](https://scholar.google.com/) <br>
- [scholarly Python package](https://pypi.org/project/scholarly/) <br>
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) <br>
- [Google-Scholar-MCP-Server](https://github.com/JackKuo666/Google-Scholar-MCP-Server) <br>
- [SemanticScholar-Search-Skill](https://github.com/JackKuo666/semanticScholar-search-skill) <br>
- [PubMed-Search-Skill](https://github.com/JackKuo666/pubmed-search-skill) <br>
- [Sci-Hub-Search-Skill](https://github.com/JackKuo666/sci-hub-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, JSON files, guidance] <br>
**Output Format:** [Console text, JSON, Markdown usage guidance, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write JSON results to a user-specified output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
