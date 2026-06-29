# Skill Card

## Description

Agent skill + Node.js CLI for HTM (The Hague public transport) account holders to manage OV-pas subscriptions and trip history. Requires Node.js with no additional dependencies; uses the unofficial "Mijn HTM" portal API.

## Owner

ghuron — single maintainer, no team.

## License or terms

MIT-0.

## Use case

For an HTM account holder managing passes for themselves and family members:

- **Subscription advice.** Analyses trip history to determine whether a Regio Vrij flat-rate subscription would save money, and which area.
- **Order / renew.** Stages a subscription order in the HTM shopping cart. Final checkout (bank payment) must be completed by the user in the browser.
- **Missed check-outs.** Lists trips where the traveller forgot to check out, resulting in a default fare charge.

Planned: correcting missed check-outs via the skill.

Only for passes the operator owns or is explicitly authorised to manage.

## Deployment geography

The Netherlands — HTM serves The Hague and surrounding municipalities. Regio Vrij advice covers HTM's own subscription areas; Rotterdam and Voorne-Putten subscriptions are priced but cannot be recommended (no boundary data for those areas).

## Risks and mitigations

- **Risk:** HTM has no public API; reverse-engineered endpoints can break without notice.
  **Mitigation:** End-to-end tests run periodically against real credentials; issues are fixed as found. The skill's only write action is adding to the shopping cart — no payment is made automatically.

## References

- `SKILL.md` — command reference.

## Skill output

All commands return JSON to stdout. `reorder` additionally creates or updates a draft order line on the HTM account (no payment).

## Skill version

1.0.1

## Ethical considerations

Only use against an account you own or are authorised to manage. `regio-advies` is a decision aid — verify current HTM pricing before acting on it. Compliance with HTM's terms of service is the operator's responsibility.
