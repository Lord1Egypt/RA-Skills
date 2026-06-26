## Description: <br>
Mysteel Price Search helps agents query Mysteel commodity spot and futures prices, macroeconomic indicators, industrial supply-chain data, import-export and inventory data, financial market data, and settlement voucher inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to ask natural-language questions about commodity prices, market indicators, regional comparisons, and historical trends. Agents can call the bundled Python client to fetch JSON responses from Mysteel or save filtered price data as CSV files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user query text and an API token to the external Mysteel search API. <br>
Mitigation: Use only an approved Mysteel token, keep the token out of chat transcripts and source control, and avoid sending sensitive query text unless the data-sharing path is approved. <br>
Risk: CSV output can create local files containing market data returned by the API. <br>
Mitigation: Use the documented row and date filters, review generated files before reuse, and keep output directories under normal workspace data-handling controls. <br>
Risk: The security scan reports a clean verdict, but the skill still executes local Python code and makes network requests. <br>
Mitigation: Run it only in trusted workspaces, review commands before execution, and rely on the published scan summary as the security baseline. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyb92/mysteel-pricesearch) <br>
- [API Reference](references/api_reference.md) <br>
- [Mysteel AI Search API endpoint](https://mcp.mysteel.com/mcp/info/ai-search/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON API responses, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV mode supports row limits, date filters, output directory selection, and cleanup of old or excess CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
