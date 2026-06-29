## Description: <br>
Fetch passes, products, and trips, and order new products from the HTM Mijn HTM portal for The Hague public transport account holders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghuron](https://clawhub.ai/user/ghuron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External HTM account holders use this skill to list passes, inspect products and trip history, evaluate Regio Vrij subscription value, and stage supported products in the HTM shopping cart for manual checkout. Use it only for passes the operator owns or is authorized to manage. <br>

### Deployment Geography for Use: <br>
The Netherlands <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires HTM account credentials and accesses account passes, products, and trip history. <br>
Mitigation: Store HTM_LOGIN and HTM_PASSWORD as secrets, run the skill only in a trusted environment, and use it only with accounts and passes you own or are authorized to manage. <br>
Risk: The reorder command can create or update a draft line in the HTM shopping cart. <br>
Mitigation: Review the returned cart in the browser before payment; the skill does not complete checkout or bank authorization automatically. <br>
Risk: The skill depends on unofficial HTM portal and order API behavior that may change without notice. <br>
Mitigation: Treat failures as possible portal changes, verify current HTM pricing before acting on advice, and rerun or update the skill when HTM changes its portal behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghuron/skills/htm) <br>
- [HTM website](https://www.htm.nl) <br>
- [HTM shopping cart](https://www.htm.nl/winkelwagen/) <br>
- [Command reference](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON printed to stdout by Node.js CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The reorder command also creates or updates a draft HTM cart line and returns a checkout URL; payment remains manual in the browser.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
