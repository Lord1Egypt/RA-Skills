# Homarr native widgets and integrations

Use this reference when configuring/debugging Homarr integrations or modifying Homarr source for native widgets/integrations.

## Integration management

Integration URL must be a base URL, not a deep settings/API path.

Good:

```text
http://sabnzbd.example.com
https://example.com/sabnzbd
```

Bad:

```text
http://sabnzbd.example.com/settings
https://example.com/sabnzbd/settings
```

Homarr does not allow creating an integration unless test connection succeeds.

## Integration troubleshooting

Check:

- base URL is correct;
- secrets/API keys are correct and have permissions;
- Homarr host/container can reach the service;
- DNS/firewall/VLAN/VPN allows access;
- reverse proxy/auth proxy is not blocking API;
- self-signed cert is added to Homarr trusted certificates;
- target service logs show request/auth details;
- Homarr logs show integration errors.

Remember: integration traffic is server-side from Homarr host/container, unlike iframe traffic which is from the browser.

## Secrets and permissions

Homarr stores integration secrets encrypted and does not pass them to the browser.

Rules:

- Keep API keys/tokens/passwords server-side.
- Do not pass secrets to React/client code.
- Read secrets through Homarr integration mechanisms.
- Gate interactive actions by integration permissions.

Distinguish permission levels:

- select/query integration data in items;
- interact with integration actions;
- full control over integration config/secrets.

Do not expose pause/resume/delete/etc actions without interact permission.

## Widget/integration relationship

Each widget supports specific integration kinds/categories. Check widget docs for Supported Integrations.

Some widgets support multiple integrations; some do not. Handle:

- 0 integrations selected;
- 1 integration;
- multiple integrations;
- loading state;
- empty data;
- error state;
- permission denied;
- partial failure from one integration.

## Native Homarr development setup

Use only when modifying Homarr source, not for external iframe mini-apps.

Prerequisites:

- Node.js LTS;
- pnpm latest;
- Git;
- Docker / Docker Desktop;
- GitHub account if contributing.

Setup:

```bash
git clone <fork-url> homarr
cd homarr
pnpm install
pnpm run docker:dev
cp .env.example .env
# set DB_URL to a sqlite path
pnpm run db:migration:sqlite:run
pnpm dev
```

Open:

```text
http://localhost:3000
```

Useful scripts:

```bash
pnpm dev
pnpm cli
pnpm db:migration:sqlite:run
pnpm db:migration:sqlite:generate
pnpm db:studio
pnpm package:new
pnpm lint
pnpm format:fix
pnpm test
pnpm test:ui
pnpm typecheck
pnpm build
```

Before claiming source changes are done, run the smallest meaningful gates:

```bash
pnpm lint
pnpm typecheck
pnpm test
```

Use `pnpm build` when build-level confidence is needed.

Docker build/run:

```bash
docker build -t homarr .
docker run -p 7575:7575 -e SECRET_ENCRYPTION_KEY='<secret>' homarr:latest
```

## Native integration implementation checklist

When adding a real Homarr integration in source, expect changes across several areas:

- integration definition, kind, and secret schema;
- integration class/client implementation;
- registration in integration creator/factory;
- test connection implementation;
- permissions/action model;
- docs page for the integration;
- supported widget/category mapping if widgets consume it.

Rules:

- implement the correct category interface for the widget family;
- read secrets server-side only;
- never pass API tokens to React/client;
- validate URL/secrets during test connection;
- return clear errors;
- handle self-signed certificates according to Homarr docs;
- include empty/error/loading states.

## Native widget implementation checklist

When adding/changing a native widget:

- verify supported integrations;
- define options with defaults;
- validate numeric/string options, often with zod;
- hide irrelevant options based on selected integration kind/category;
- handle preview/edit mode;
- do not assume `itemId` or `boardId` always exists in preview;
- handle `width`/`height` responsive behavior;
- support 0/1/N integrations where applicable;
- route data access through Homarr server/tRPC, not direct client requests to secret APIs;
- gate actions by permissions;
- keep UI accessible and usable in light/dark themes.

Common option types/patterns:

- text;
- switch;
- number;
- slider;
- select;
- multiSelect;
- multiText;
- location;
- app;
- dynamic/select-like inputs;
- conditional `shouldHide` behavior.

## Source-work safety

- Keep changes minimal and typed.
- Avoid touching unrelated widgets/integrations.
- Do not introduce client-side secret access.
- Preserve existing permission checks.
- Add/adjust tests when behavior changes.
- Verify empty/loading/error states manually or with tests.
