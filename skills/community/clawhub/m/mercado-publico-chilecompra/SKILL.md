---
name: mercado-publico-chilecompra
description: Operate and assist across Chile's Mercado Público / ChileCompra supplier workflows using both the public API and the private supplier portal. Use when searching, listing, monitoring, or reporting on licitaciones, órdenes de compra, buyers, suppliers, and opportunities via API, or when navigating the authenticated portal to review licitaciones, órdenes de compra, cotizaciones, compra ágil, trato directo, reclamos, and portal-specific states, actions, errors, disabled buttons, broken routes, or iframe-driven workflows. ClaveÚnica + email OTP login may require manual fallback or reuse of an already-authenticated session when the federated broker is fragile.
metadata: {"openclaw":{"primaryEnv":"MERCADO_PUBLICO_API_TICKET","requires":{"env":["MERCADO_PUBLICO_API_TICKET"]}}}
---

# Mercado Público

Operate the private Mercado Público supplier portal as a cautious copiloto operativo.

## Quick start

1. Start from the authenticated supplier shell when possible:
   - `https://www.mercadopublico.cl/Portal/Modules/Menu/Menu.aspx`
2. Treat the site as **hybrid**:
   - legacy modules often load inside iframe `fraDetalle`
   - newer modules may open in separate routes or embedded apps
3. Prefer **read / prepare / explain** first.
4. Require explicit confirmation before any action that changes state.

## Core workflow

### 1. Establish session

- Use ClaveÚnica flow when needed.
- Expect email OTP.
- Expect entity selection after login.
- If session already exists, reuse it instead of reauthenticating.
- Treat full broker automation as potentially fragile; prefer an already-authenticated session or manual fallback when the federated flow starts expiring or rejecting automation.

For details, read in this order:
- `references/login-state-machine.md` (siempre, para decidir estado/transición e intervención humana)
- `references/auth-y-sesion.md` (flujo base y señales de sesión)
- `references/acceso-a-correo-otp.md` (requisitos generales de acceso a correo OTP)
- `references/otp-provider-contract.md` (contrato esperado del proveedor OTP)

### 2. Route correctly

- Prefer entering through `Menu.aspx`.
- Inspect whether the target module lives in `fraDetalle`.
- If a direct URL returns 404, retry from the menu/iframe context before concluding the module is broken.
- Distinguish between:
  - legacy ASP.NET pages with postbacks
  - newer modules with separate routes / richer UI

For details, read:
- `references/arquitectura-y-ruteo.md`

### 3. Choose the task path

- Apply the business rule **API first, portal after**.
- Prefer the public API when it answers the question with enough fidelity.
- Use the private portal only when the API does not cover the case, when provider-specific authenticated context matters, or when a real portal action/review is required.
- Leer `references/runbooks.md` para ejecutar flujo operativo mínimo (buscar licitación, revisar ofertabilidad, revisar OC, preparar cotización, diagnosticar portal).
- **Licitaciones** → search, review detail, questions, attachments, offer readiness
- **Órdenes de compra** → search, inspect detail, identify allowed actions, XML/attachments/payments
- **Cotizaciones / Trato Directo / Compra Ágil** → inspect and prepare response flows up to pre-confirmation
- **Reclamos** → locate correct entry point, identify whether flow stays in portal or redirects to help center
- **Gestión / reportería** → summarize pending items, counts, and dashboards
- **Diagnóstico** → explain 404s, disabled buttons, null-reference errors, CAPTCHA, or context-sensitive failures

Read only the relevant reference file(s):
- `references/api-publica.md` (always first for discovery/reporting/search use cases and API-vs-portal decisions)
- `references/licitaciones.md`
- `references/ordenes-de-compra.md`
- `references/cotizaciones-trato-directo-y-compra-agil.md`
- `references/reclamos-y-ayuda.md`
- `references/gestion-y-reporteria.md`
- `references/diagnostico-y-guardrails.md`

## Operating rules

- Prefer safe navigation from the logged-in shell over guessing deep links.
- Explain *why* an action is blocked when possible (estado hábil, role, timing, state, broken module).
- Separate:
  - **leer**
  - **preparar**
  - **confirmar y enviar**
- Stop and ask for confirmation before any irreversible or state-changing action.

## Mandatory guardrails

Always require explicit confirmation before:
- sending an offer
- sending a quotation
- accepting or rejecting an order
- requesting cancellation
- submitting a complaint
- performing any action that changes procurement state, contractual state, or payment-related state

Never assume a visible button is safe to click just because it is present.

If the portal shows 404, `NullReferenceException`, a disabled action, or unexpected redirects:
- diagnose first
- explain the likely cause
- propose the next safe step

## Resources

Use these references as needed:
- Login/auth state transitions: `references/login-state-machine.md`
- Auth/session baseline: `references/auth-y-sesion.md`
- Generic email-access requirements for OTP: `references/acceso-a-correo-otp.md`
- OTP provider contract: `references/otp-provider-contract.md`
- Operational runbooks (minimum executable flows): `references/runbooks.md`
- Portal architecture and routing: `references/arquitectura-y-ruteo.md`
- Licitaciones: `references/licitaciones.md`
- Orders: `references/ordenes-de-compra.md`
- Quotations / direct purchase / agile purchase: `references/cotizaciones-trato-directo-y-compra-agil.md`
- Complaints/help center: `references/reclamos-y-ayuda.md`
- Dashboards/reporting: `references/gestion-y-reporteria.md`
- Public API: `references/api-publica.md`
- Diagnostics and safety rules: `references/diagnostico-y-guardrails.md`

Operational helpers:
- `scripts/mercado_publico_api.py` (API pública, read-only; ticket en `MERCADO_PUBLICO_API_TICKET`, `--summary` estable y caché TTL opcional)
