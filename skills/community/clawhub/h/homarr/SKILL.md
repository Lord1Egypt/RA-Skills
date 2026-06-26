---
name: homarr
description: Work on Homarr dashboards, board styling, custom CSS, iframe widgets, embedded mini-apps, native widgets, apps, and integrations. Use when requests mention Homarr, Homarr widgets, iframe embeds, dashboard items, board appearance, Mantine/custom CSS in Homarr, Homarr integrations, or contributing/fixing Homarr native widgets/integrations.
---

# Homarr

Use this skill to choose the right Homarr path, avoid fragile CSS, and verify iframe/widget/integration work.

## Start with the right category

Classify the request first:

- **Board visual tweak**: use Homarr board appearance settings first; use scoped custom CSS only when needed. Read [styling.md](references/styling.md).
- **Unsupported UI or custom mini-widget**: host a separate page/app and embed it with the iFrame widget. Read [iframe-widgets.md](references/iframe-widgets.md).
- **Supported third-party data**: configure a Homarr integration and matching native widget. Read [native-widgets-integrations.md](references/native-widgets-integrations.md).
- **Unsupported service but native Homarr behavior is required**: modify/contribute Homarr source; keep secrets server-side. Read [native-widgets-integrations.md](references/native-widgets-integrations.md).

Do not promise runtime custom widgets/plugins: official Homarr does not support arbitrary custom widgets as runtime extensions. Practical alternatives are built-in widgets, iFrame embeds, custom CSS, or source contributions.

## Core concepts

Keep these distinct:

- **Board**: dashboard page containing items.
- **App**: link/bookmark entry with URL, icon, description, optional ping URL.
- **Integration**: Homarr server-side connection to a supported third-party service.
- **Widget**: board item that shows data or controls an integration.
- **iFrame widget**: browser embed of an external URL; Homarr does not proxy traffic.

## General workflow

1. Identify whether the task is CSS, iframe, app, integration, or native widget work.
2. Prefer official Homarr settings and built-in integrations before custom code.
3. For CSS, use widget custom classes and board-scoped CSS; avoid generated Mantine suffix classes.
4. For iframes, verify client-reachable URL, protocol, frame headers, theme, and transparent body.
5. For integrations, verify base URL, secrets, server/container reachability, and test connection.
6. For native widgets, verify supported integrations, options, loading/empty/error states, edit/preview mode, and permissions.
7. Make minimal reversible changes.
8. Verify with curl/headers/DevTools and, for Homarr source work, lint/typecheck/test.
9. Document any fragile selectors, unsupported CSS assumptions, or reverse-proxy/header requirements.

## Quick decisions

| Need | Use |
|---|---|
| Change board/item colors/radius/background | Board appearance first, then scoped custom CSS |
| Style one widget | Widget custom class + board custom CSS |
| Embed unsupported web UI | iFrame widget |
| Embed custom mini-widget | Separate HTML/app + iFrame widget |
| Show data from supported service | Integration + supported native widget |
| Show unsupported service natively | Homarr source contribution |
| Hide unauthorized control | Permissions, not CSS |
| Fix white iframe background | `theme=dark`, transparent body, inner container, headers/mixed-content checks |
| Fix “card inside card” | Remove inner wrapper background/border/radius/shadow/blur |

## Official docs to check

- Styling: `https://homarr.dev/docs/advanced/styling/`
- Boards: `https://homarr.dev/docs/management/boards/`
- iFrame widget: `https://homarr.dev/docs/widgets/iframe/`
- Apps: `https://homarr.dev/docs/management/apps/`
- Integrations: `https://homarr.dev/docs/management/integrations/`
- Widgets catalog: `https://homarr.dev/docs/category/widgets/`
- Integrations catalog: `https://homarr.dev/docs/category/integrations/`
- FAQ/custom widgets: `https://homarr.dev/docs/community/faq/`
- Developer setup: `https://homarr.dev/docs/advanced/development/getting-started/`
- Third-party iframe reference: `https://github.com/diogovalentte/homarr-iframes`

## Safety rules

- Treat custom CSS as unsupported and potentially fragile after updates.
- Do not use CSS as security or permissions.
- Do not expose API keys in CSS, iframe URLs, or client-rendered code.
- For native integrations, keep secrets server-side through Homarr integration APIs.
- For iframes, enable only needed permissions such as fullscreen, autoplay, microphone, camera, geolocation, payment, or modals.
- Remember public boards may expose visible embedded content to unauthenticated users if board access allows it.
