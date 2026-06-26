## Description: <br>
liuduoduo helps agents find local handymen, restaurants, and hotels in the Liuyang area with contact and pricing details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[malinguo](https://clawhub.ai/user/malinguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent for local service, dining, or lodging recommendations around Liuyang. The skill calls read-only MCP tools and returns merchant names, phone numbers, addresses, prices, ratings, and related details. <br>

### Deployment Geography for Use: <br>
China, focused on Liuyang city and nearby towns <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present demo or unverified listings as factual merchant contact, price, rating, or service information. <br>
Mitigation: Review the data source before deployment and ask users to verify merchant details directly before relying on them. <br>
Risk: Users may share precise addresses or sensitive travel and service details with a remote MCP endpoint. <br>
Mitigation: Use the skill only after the remote operator is trusted and avoid sending unnecessary sensitive location or itinerary details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/malinguo/liuduoduo-life-skill) <br>
- [Publisher profile](https://clawhub.ai/user/malinguo) <br>
- [MCP endpoint](https://xilejie-silk.com/liuyang-life/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Markdown or plain text summaries derived from JSON MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only responses may include merchant contact information, prices, ratings, addresses, and service details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
