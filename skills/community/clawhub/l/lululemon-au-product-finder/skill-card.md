## Description: <br>
Find a product on the Lululemon Australia site from a natural-language clothing description and return structured details such as product name, variant colors, sizes, prices, URLs, and provenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ensonfun](https://clawhub.ai/user/ensonfun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping or catalog-research agents use this skill to find Lululemon Australia products from fuzzy natural-language descriptions and return structured variant details from official sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The anti-bot fallback may reuse an existing browser session, which can expose logged-in browsing state if used carelessly. <br>
Mitigation: Use an isolated or guest browser profile for fallback browsing, and only reuse a personal logged-in session with explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ensonfun/lululemon-au-product-finder) <br>
- [Lululemon Australia homepage](https://www.lululemon.com.au/en-au/home) <br>
- [Lululemon AU Anti-Bot And Data Source Notes](references/anti-bot-and-sources.md) <br>
- [Lululemon AU Fallback Ladder](references/fallback-ladder.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Structured JSON object, usually embedded in Markdown when explanation is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes field-level provenance, confidence, coverage, and official source URLs; partial results may use nulls or empty arrays.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
