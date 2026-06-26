## Description: <br>
Find nearby takeaways in Ireland and browse menus via Deliveroo/Just Eat. Uses Google Places API for discovery and browser automation for menu scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cotyledonlab](https://clawhub.ai/user/cotyledonlab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find Irish takeaway restaurants by location or cuisine and inspect menu information from food-delivery sites before deciding what to order. <br>

### Deployment Geography for Use: <br>
Ireland <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send town, postcode, address, or restaurant lookup details to Google Places and food-delivery sites. <br>
Mitigation: Use it only when sharing that location context with those external services is acceptable. <br>
Risk: Google Places API key usage can create quota or billing exposure. <br>
Mitigation: Use a restricted Google Places API key and monitor quota and billing. <br>
Risk: Browser automation against delivery sites could enter login, payment, or ordering flows if a user extends the workflow beyond menu viewing. <br>
Mitigation: Keep use to discovery and menu browsing unless a future release explicitly scopes and reviews ordering behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/cotyledonlab/irish-takeaway) <br>
- [Deliveroo Ireland](https://deliveroo.ie/) <br>
- [Just Eat Ireland](https://www.just-eat.ie/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized restaurant or menu results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include restaurant names, ratings, menu items, prices, allergens, and setup guidance when supported by the queried services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
