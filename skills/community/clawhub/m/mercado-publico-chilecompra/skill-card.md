## Description:

Operate and assist across Chile's Mercado Público / ChileCompra supplier workflows using both the public API and the private supplier portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdovarela](https://clawhub.ai/user/fdovarela)

### License/Terms of Use:

MIT-0

## Use Case:

External suppliers and their agent operators use this skill to search, monitor, report on, and prepare actions for Mercado Publico / ChileCompra workflows. It supports API-first read-only discovery and authenticated portal review for licitaciones, purchase orders, quotations, direct purchase, agile purchase, complaints, reporting, and portal diagnostics.

### Deployment Geography for Use:

Chile

## Known Risks and Mitigations:

Risk: Optional API caching can save the Mercado Publico API ticket to disk in plaintext.

Mitigation: Keep caching disabled unless cache handling redacts the ticket, uses a private cache directory, and any ticket that may have been cached in a shared or backed-up location is rotated.

Risk: Authenticated portal actions may change procurement, contractual, commercial, or payment-related state.

Mitigation: Require explicit user approval before sending offers or quotations, accepting or rejecting purchase orders, requesting cancellation, submitting complaints, or taking any other state-changing portal action.

Risk: ClaveUnica email OTP handling can expose short-lived login codes if the mail channel is not explicitly authorized and controlled.

Mitigation: Use only a user-selected and validated OTP access mechanism, avoid persisting OTPs or logging full codes, and fall back to manual OTP entry when automated access is not confirmed.

Risk: Hybrid portal routing, disabled buttons, CAPTCHA, 404s, and server errors can make portal state ambiguous.

Mitigation: Diagnose the observed state first, explain the likely cause, and continue only through the next safe read, prepare, or explicitly confirmed action.

## Reference(s):

- [Mercado Publico Authenticated Supplier Shell](https://www.mercadopublico.cl/Portal/Modules/Menu/Menu.aspx)
- [Mercado Publico Public API](https://api.mercadopublico.cl/servicios/v1)
- [Login/Auth State Machine](references/login-state-machine.md)
- [Auth y sesión](references/auth-y-sesion.md)
- [Acceso al correo para OTP](references/acceso-a-correo-otp.md)
- [Contrato conceptual otp-provider](references/otp-provider-contract.md)
- [Runbooks operativos mínimos](references/runbooks.md)
- [Arquitectura y ruteo del portal](references/arquitectura-y-ruteo.md)
- [API pública de Mercado Público](references/api-publica.md)
- [Licitaciones](references/licitaciones.md)
- [Órdenes de compra](references/ordenes-de-compra.md)
- [Cotizaciones, trato directo y compra ágil](references/cotizaciones-trato-directo-y-compra-agil.md)
- [Reclamos y centro de ayuda](references/reclamos-y-ayuda.md)
- [Gestión y reportería](references/gestion-y-reporteria.md)
- [Diagnóstico y guardrails](references/diagnostico-y-guardrails.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration]

**Output Format:** [Markdown guidance with optional shell commands, API JSON, or key-value summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MERCADO_PUBLICO_API_TICKET for public API helper use; portal actions require explicit user confirmation before state changes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
