# Contextual localization

Read this reference when language, geography, jurisdiction, culture, or local operating practice may change the information architecture.

## Localization is not translation

Treat these as separate signals:

- response language and writing direction;
- country, region, and jurisdiction;
- cultural conventions and audience vocabulary;
- organizational and operational model;
- role boundaries and decision authority;
- currency, date, address, identity, communication, and regulatory conventions.

Never infer a country or a binding local rule from language alone. Persian may be used in Iran, Afghanistan, a diaspora product, or a multilingual product. English does not imply a US operating model.

## Response-language authority

Choose the response language in this order:

1. an explicit language request in the current turn;
2. the clear dominant natural language used in the current user message, including a starter with no product brief;
3. only when the current user message has no usable natural-language signal, the active language of this conversation;
4. a brief clarification only when the choice materially affects the deliverable.

Persistent memory, profile preferences, locale, location, prior chats, project records, and automatically supplied context never choose or override steps 1–3. They also do not supply a country, jurisdiction, current project, or product brief. Do not discard a starter's language merely because the starter lacks product context: an English empty starter receives an English brief request. Technical terms, stable identifiers, URLs, code, or short quotations in another language do not by themselves change the dominant language. A Persian message containing English terms such as `Sitemap` or `User Flow` still receives Persian unless it explicitly requests another language.

## When to ask

Ask a localization question only when the answer could change domains, items, labels, relationships, permissions, lifecycle, navigation, search, retention, or governance.

Useful product-language questions include:

> Is this product intended for one country or region? Local terminology and role responsibilities may change the structure.

> In your actual operation, is a building managed by one manager, an elected board, a management company, or a combination?

Do not ask for geography ceremonially when it has no architectural consequence.

## Model local context explicitly

Record only relevant fields in `meta.locale_context`, each with an evidence state where needed:

```json
{
  "language": "fa",
  "direction": "rtl",
  "locale_context": {
    "country": "IR",
    "region": null,
    "jurisdiction": "Iran",
    "currency": "IRR",
    "date_system": "solar-hijri",
    "operating_model": "single building manager",
    "evidence_status": "Confirmed"
  }
}
```

Omit, leave null, or mark Unknown when the user has not supplied the information. Do not fill locale fields from stereotypes.

## Roles and vocabulary

Do not combine roles merely because they are commonly mentioned together. `owner`, `resident`, `building manager`, `board member`, `management company`, `caretaker`, and `technician` may have different scope and authority.

- Keep distinct roles separate until the product confirms equivalent permissions.
- Preserve the user's preferred label as the human-facing term.
- Keep synonyms and regional variants as metadata, not duplicate objects.
- If a local term is ambiguous, explain the consequence and ask one concrete question.

## Research boundary

When local law, regulation, or current public infrastructure materially changes the IA, verify it with current authoritative sources if browsing is available. Generic market patterns are hypotheses, not confirmed local requirements. Never turn a cultural generalization into a product rule.
