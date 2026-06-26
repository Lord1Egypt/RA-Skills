## Description: <br>
Find professional emails and contacts from a name and company or domain using SerpAPI and OpenAI GPT-4o-mini. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales, recruiting, and business development users can use this skill to search public web results for professional contact information for a company or domain, optionally focused on a named person. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospecting queries, names, domains, and search snippets may be sent to SerpAPI or Brave Search and OpenAI. <br>
Mitigation: Use the skill only when those disclosures are acceptable under privacy, workplace, and customer-data policies. <br>
Risk: API keys may be exposed if credentials are committed or hard-coded. <br>
Mitigation: Store API keys in environment variables or a secrets manager and avoid committing credentials into the script. <br>
Risk: Guessed or extracted emails may be inaccurate or inappropriate to contact. <br>
Mitigation: Verify contact details before use and follow applicable privacy, anti-spam, and outreach rules. <br>


## Reference(s): <br>
- [Email Patterns Reference](references/patterns.md) <br>
- [Contact Finder ClawHub Page](https://clawhub.ai/mrnsmh/openclaw-skill-contact-finder) <br>
- [SerpAPI](https://serpapi.com) <br>
- [SerpAPI Search Endpoint](https://serpapi.com/search) <br>
- [Brave Search API Endpoint](https://api.search.brave.com/res/v1/web/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain-text table or JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires company and domain inputs, accepts an optional person name, and labels contact confidence as high, medium, or low.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
