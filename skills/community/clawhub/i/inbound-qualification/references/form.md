# The form on the site

The tool's public form takes submissions; the site renders the form with its own markup and
submits through `@cargo-ai/form-sdk`, headless. This is the wiring, in the website app
(`infra/website-building/apps/website/` when the site came from `website-building`).

## 1. Copy the site files and add the SDK

| From                               | To, in the app                  |
| ---------------------------------- | ------------------------------- |
| `site/components/inbound-form.tsx` | `components/inbound-form.tsx`   |
| `site/app/contact/page.tsx`        | `app/contact/page.tsx`          |

```sh
npm install @cargo-ai/form-sdk --prefix infra/website-building/apps/website
```

Then link `/contact/` from the site's header or call to action, and add it to `app/sitemap.ts`.
The page uses `pageMetadata` from `lib/site.ts` and the app's `Button`, both from
`website-building`; in another app, point those imports at its equivalents.

## 2. Hand the tool to the app

In the app's `defineApp` (`infra/website-building/apps/website.ts`):

```ts
import { inboundForm } from "../../inbound-qualification/tools/inbound-form";

env: {
  NEXT_PUBLIC_CARGO_FORM: inboundForm.uuid,
},
```

The tool's uuid is public: the form API accepts submissions only from `allowedOrigins`. Without
the env var the component renders nothing, so a build without it ships no form.

## 3. Set the origin

`publicForm.allowedOrigins` in `infra/tools/inbound-form.ts` is the site's canonical origin,
exactly: `https://www.example.com`, no trailing slash, no path. `https://example.com` and a preview
URL are different origins and are refused with 403. Add `http://localhost:3000` only while
testing locally, and remove it before the release.

## How a submission is checked

In order, each one refusing the request:

1. **Origin**: not in `allowedOrigins`, 403.
2. **Honeypot**: a hidden field the SDK injects; a bot that fills it is dropped.
3. **Time-trap**: submitted sooner than `minFillMillis` after the SDK loaded. The site loads it once
   the page has hydrated, so the timer starts when the form becomes usable.
4. **Rate limit**: ten submissions a minute per address, always on.
5. **CAPTCHA**, only with the `turnstile` variation.
6. **The workflow's own check**: a personal email domain is refused before any paid call.

## Privacy

- The SDK reads the page's UTMs, `page_url` and `referrer` into memory when it loads, and sets its
  first-party `cargo_anon_id` cookie only when a visitor submits (neither under Global Privacy
  Control or Do Not Track). A visitor who never submits leaves with no cookie.
- A submission is personal data the person chose to send. It is used for their request; marketing
  email only when they ticked the box, recorded as `marketing_consent`.
- Add a "Contact form" section to the privacy page: what the form collects, that the company is
  looked up from the email domain, where the record goes (the workspace's contacts, a Slack
  channel), how long it is kept, and how to ask for it to be removed. Never generate the legal
  text.

## How long the page waits

The form submits in async mode: the API accepts the submission at once and the SDK polls the run.
A run usually takes well under 30 seconds, most of it the company lookup, but a slow lookup or a
busy queue can take minutes. `pollTimeoutMs: 30_000` in `components/inbound-form.tsx` is how long
the visitor waits for the booking link; after that they get the thank-you. The run still finishes,
so the account, the contact and the Slack post land late, never lost. Raise it only if a qualified
visitor missing the link on the page costs more than a longer wait.

## The SDK's own render mode

The workflow's input schema is the form's field list, so the hidden `utm_*`, `page_url` and
`referrer` fields are in it. In headless mode the site sets them; the SDK's `render` mode would show
them as visible inputs. Keep headless, or move those fields out of the schema before switching.

## Checking it

1. Open `/contact/` in a private window: the SDK loads after hydration (one schema request) and
   no `cargo_anon_id` cookie is set.
2. Wait a few seconds before submitting: a submission sooner than `minFillMillis` is refused.
3. Submit with a personal email: "Please use your work email", and no run spends credits.
4. Submit with a work email: the answer shows, the account and contact appear in the models, the
   Slack channel gets one message.
5. From another origin (a preview URL), the submission is refused.
