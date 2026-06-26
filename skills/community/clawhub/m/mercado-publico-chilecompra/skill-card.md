## Description: <br>
Operate and assist across Chile's Mercado Público / ChileCompra supplier workflows using both the public API and the private supplier portal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdovarela](https://clawhub.ai/user/fdovarela) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External suppliers and procurement operators use this skill to search, monitor, summarize, and prepare Mercado Público / ChileCompra workflows across public API data and authenticated supplier-portal tasks. It supports read-first review of licitaciones, órdenes de compra, cotizaciones, compra ágil, trato directo, reclamos, reporting, and portal diagnostics before any sensitive action is confirmed. <br>

### Deployment Geography for Use: <br>
Chile <br>

## Known Risks and Mitigations: <br>
Risk: Optional API caching can store request URLs containing the Mercado Público API ticket on the local host. <br>
Mitigation: Keep cache TTL at 0 unless the cache is patched to redact the ticket, and clear generated api-cache files after use. <br>
Risk: The skill can assist inside a sensitive supplier portal where bids, quotations, orders, cancellations, complaints, or payment-related actions may change procurement state. <br>
Mitigation: Use the read, prepare, confirm sequence and require explicit user confirmation before every state-changing or payment-related action. <br>
Risk: Authenticated login may involve email OTP access and supplier-account context. <br>
Mitigation: Prefer manual OTP or a dedicated narrowly scoped mailbox, avoid persisting OTP values, and use an already authenticated session when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fdovarela/mercado-publico-chilecompra) <br>
- [Publisher profile](https://clawhub.ai/user/fdovarela) <br>
- [Public API reference](references/api-publica.md) <br>
- [Operational runbooks](references/runbooks.md) <br>
- [Login/Auth state machine](references/login-state-machine.md) <br>
- [Auth and session guidance](references/auth-y-sesion.md) <br>
- [OTP provider contract](references/otp-provider-contract.md) <br>
- [Diagnostics and guardrails](references/diagnostico-y-guardrails.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command invocations and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require MERCADO_PUBLICO_API_TICKET for public API calls; portal workflows can require an authenticated session and manual or externally provided OTP handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
