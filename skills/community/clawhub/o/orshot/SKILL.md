---
name: orshot
description: "Automate video, PDF and image generation from templates and social media posting. Image generation, PDF generation and video generation from your templates with the Orshot API, over the hosted Orshot MCP server (OAuth, no key) or REST. Use to generate images, OG images, social media posts, carousels, thumbnails, ad creatives, banners, certificates, invoices and PDF documents from a template, render video with animations and audio, resize one design to every social format, batch render personalized images, take tweet screenshots and website screenshots, and schedule and post renders to Instagram, LinkedIn, X, TikTok, Facebook, Pinterest, Threads, Bluesky, Reddit, YouTube, Telegram, Snapchat and Google Business. Load for any Orshot task; it carries the gotchas (parameterId keys, page1@ prefixes, async video) that otherwise break renders."
homepage: https://orshot.com/agents/openclaw
license: MIT-0
metadata:
  author: Orshot
  version: "1.4.0"
  openclaw:
    emoji: "🖼️"
    homepage: https://orshot.com/agents/openclaw
    primaryEnv: ORSHOT_API_KEY
    requires:
      env: []
      bins: []
    envVars:
      - name: ORSHOT_API_KEY
        required: false
        description: Orshot API key from Workspace Settings > API Keys. Only needed for REST. Not needed when the agent connects through the hosted MCP server with OAuth.
---

# Orshot: automate video, PDF and image generation from templates and social media posting

Orshot is an API for automated image, PDF and video generation from templates. Design a template once in the Orshot studio (or import it from Canva or Figma), then render it with new text, images and video on every call, and post the result to connected social accounts in the same request. Rendering is deterministic: the same template plus the same data gives the same output every time.

- Docs: https://orshot.com/docs (append `.md` to any docs URL for markdown)
- Hosted MCP server: `https://mcp.orshot.com/mcp` (100+ `orshot_*` tools)
- REST base: `https://api.orshot.com/v1`
- Free plan: 100 credits a month, no credit card.

## Connect first (MCP, no key to paste)

The hosted MCP server is the fastest route and the only one that returns inline previews, visual post cards and design checks. Add it, log in with the user's Orshot account in the browser, and every tool below works.

```bash
openclaw mcp add orshot --url https://mcp.orshot.com/mcp --transport streamable-http --auth oauth
openclaw mcp login orshot
```

No Orshot account yet? The login page offers signup; the free plan starts with 100 credits a month. Claude Code: `claude mcp add --transport http orshot https://mcp.orshot.com/mcp`. Cursor, Windsurf, VS Code, Codex and ChatGPT take the same URL as a remote MCP server.

Confirm with `orshot_get_account`. It returns the profile, workspaces and credits. If it says the subscription is inactive or a plan limit is hit, that is a billing state, not an auth error: point the user to their workspace billing page at https://orshot.com/pricing and stop retrying.

**Headless fallback: REST with an API key.** Only when the agent cannot run MCP (a cron job, a server-side script, n8n).

```bash
export ORSHOT_API_KEY=...   # Workspace Settings > API Keys
curl -s https://api.orshot.com/v1/me -H "Authorization: Bearer $ORSHOT_API_KEY"
```

Do not proceed until one of the two works.

## What you can do with it

Each line names the MCP tool first and the REST route second.

- **Render any template with your data**: OG images, ad creatives, certificates, invoices, carousels, reels. `orshot_render_template` or `POST /v1/studio/render`.
- **Create and refine studio templates from a brief**, with inline previews and design checks. `orshot_create_template_design`, `orshot_update_template_design`, `orshot_patch_template_elements` (read `orshot://template-design-spec` first; the `orshot-social-media-content` skill holds the craft rules).
- **Render true video**: per-element animations and transitions, soundtracks from the brand kit, free motion previews before a paid render. Same render tool with `format: "mp4"`.
- **Start with ready-made utility templates**: tweet screenshots, website screenshots, bar and comparison charts, app store screenshots, phone mockups, background removal. `orshot_render_library_template` or `POST /v1/generate/:renderType`.
- **Resize one design to every social format in one call** (Smart Resize). `size` and `extraSizes` on the render.
- **Batch render personalized variations**, like certificates for a list of names. `orshot_batch_render_template`.
- **Stay on brand**: colors, fonts, images, videos and audio from the brand kit. `orshot_get_brand_kit`, `orshot_import_brand_website`.
- **Organize**: folders, template sharing, switching between client workspaces. `orshot_list_template_folders`, `orshot_set_active_workspace`.
- **Mint signed dynamic URLs** for OG images and embeds. `orshot_create_dynamic_url` or `POST /v1/signed-url/create`.
- **Draft, schedule and publish social media posts**, learn the best time to post from the user's own engagement data, read reach and engagement analytics. `orshot_publish_social_post`, `orshot_get_best_time_to_post`, `orshot_get_social_analytics`. The `orshot-social-media-scheduler` skill carries the full loop.
- **Build and run automation workflows** that keep producing content on a schedule. `orshot_create_workflow`, `orshot_run_workflow`.

Example prompts that map straight onto these tools:

- "Render the launch template as an OG image with the title 'We just shipped'"
- "Create an Instagram post template with a headline, subtitle and product image"
- "Resize my launch design for Instagram story, square and OG in one call"
- "Generate certificates for this list of 40 names as PDFs"
- "Screenshot this tweet" / "Capture orshot.com as an image" / "Make a bar chart from these numbers"
- "Post this render to Instagram at the best time and show me how last week's posts performed"

## Core workflow

1. **Connect** (above).
2. **Find the template.** `orshot_list_studio_templates` (search by name and tags) or `GET /v1/studio/templates/all?page=1&limit=10`. No template yet? Use the 2,000+ library templates (`orshot_list_library_templates`) or design one with `orshot_create_template_design`.
3. **Read its parameters.** `orshot_get_studio_template_modifications` or `GET /v1/studio/templates/:id`. Modifications key by `parameterId`, never by layer name. Never guess keys.
4. **Render.** `orshot_render_template` with `modifications`, or `POST /v1/studio/render` with `response: { type: "url", format: "png" }`.
5. **Deliver or post.** Show the user the output URL. Add `publish` to post it to social in the same call.
6. **Automate.** Put the call into the n8n, Make, Zapier or cron the user already runs, or build an Orshot Workflow.
7. **Verify.** `orshot_list_workspace_logs` or `GET /v1/workspace/logs` shows the render and its `source`. Show the output before calling it done.

## Safety rules for agents

- **Confirm before anything leaves the workspace.** Publishing a social post, running a workflow (it spends credits and can deliver or post) and deleting a template, workflow or brand asset need an explicit go-ahead. Say what will be posted, where, and when.
- **Default social posts to drafts.** "Prepare", "draft", "let me look first" mean `status: "draft"`. A draft reaches nobody until it is published.
- **Show cost before bulk work.** Renders spend credits, `.prompt` modifications spend AI credits, and each connected social account is a paid add-on. Say so before a loop of hundreds of renders.
- **Never paste the API key into chat, files or URLs.** Read it from the environment. Prefer MCP, which has no key at all.
- **Do not delete anything to "clean up" on your own.**

## Common gotchas (read before rendering)

1. **Modifications key by `parameterId`, not layer name.** If a value is ignored, the key is wrong. Fetch the template instead of guessing.
2. **Multi-page templates need a `pageN@` prefix.** `"page1@title"`, `"page2@title"`. A bare `"title"` only hits page 1.
3. **Studio `templateId` is an integer; utility `templateId` is a string** (`/v1/generate/:renderType` takes a slug like `"website-screenshot"`).
4. **Video output does not need video layers.** `format: "mp4"`, `"webm"` or `"gif"` renders any template. Long video renders must use `response.mode: "async"` and poll `orshot_get_render_job` or `GET /v1/studio/render-jobs/:id`, or the client times out.
5. **Image and video URLs in modifications must be public.** The renderer fetches them server side; `localhost`, expired signed URLs and auth-gated URLs fail.
6. **Style overrides use dot notation on the parameterId:** `"title.fontSize": "48px"`.
7. **Response shape differs by page count.** One page: `data` is an object (`data.content`). Multi-page: `data` is an array of `{ page, content }`.
8. **`base64` and `binary` do not combine.** `binary` streams one file.
9. **Credits and AI credits are separate.** `.prompt` modifications spend AI credits on top.
10. **On `429`, back off** using `Retry-After`.
11. **PDFs cannot be posted to social.** Images cannot go to TikTok or YouTube (video only). Video cannot go to Google Business.
12. **Social account ids are numbers.** Two accounts on the same platform have different ids. Always publish by id, never by platform name.
13. **Social publishing is a paid add-on.** Free plan workspaces cannot connect accounts. Publishing itself spends no extra credits.

## Rendering essentials

Full field reference: `references/render-configuration.md` and `references/api-reference.md`.

```js
await fetch("https://api.orshot.com/v1/studio/render", {
  method: "POST",
  headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
  body: JSON.stringify({
    templateId: 123,
    modifications: {
      title: "Launch day",             // text
      hero_image: "https://.../a.png", // image url
      "title.fontSize": "56px",        // style override
      "page2@title": "Slide two",      // multi-page
    },
    response: { type: "url", format: "png", size: "instagram-story",
                extraSizes: ["1080x1080", "1200x630"] },
  }),
});
```

The same object is the input of `orshot_render_template` over MCP.

- `format`: `png`, `jpg`, `webp`, `pdf`, `mp4`, `webm`, `gif`.
- `size` renders the design at another preset or `WIDTHxHEIGHT`; `extraSizes` adds more copies in one call (Smart Resize). Presets: `orshot://formats`.
- `response.mode: "async"` returns a job; poll it or pass `webhook_url`. Use it for video.
- Many variants at once: `orshot_batch_render_template`, or loop the render call over REST.
- Signed URLs: `POST /v1/signed-url/create` for a render URL you can embed without exposing the key.

SDKs for headless use: `npm install orshot@0.3.1`, `pip install orshot==0.2.0`, `composer require rishimohan/orshot:0.2.0`, `gem install orshot -v 0.2.0`.

```js
import { Orshot } from "orshot";
const orshot = new Orshot(apiKey); // read from your environment
const res = await orshot.renderFromTemplate({
  templateId: "open-graph-image-1",
  modifications: { title: "Hello World" },
  responseType: "url",
  responseFormat: "png",
});
```

## Social posting (the short version)

Orshot posts renders to 13+ platforms: X, Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Bluesky, Threads, Telegram, Snapchat, Google Business. The `orshot-social-media-scheduler` skill carries scheduling, drafts, analytics and best time; this is the core.

1. **Accounts.** `orshot_list_social_accounts` or `GET /v1/social/accounts?include_health=true`. Accounts are connected by a human in the dashboard (Workspace > Socials > Accounts); the API cannot connect one. An empty list means send the user there.
2. **Render and post in one call.** Add `publish` to the render:

```js
publish: {
  accounts: [1, 3],
  content: "Caption, max 5000 chars",
  status: "draft",                       // "published" (default) | "draft" | "scheduled"
  // scheduled_for: "2026-11-01T14:00:00Z", timezone: "America/New_York",
  platformOptions: { "3": { firstComment: "https://orshot.com" } },
  tiktokSettings: { autoAddMusic: true }, // TikTok photo carousels
}
```

Multi-page templates post as a carousel automatically. The response carries `publish[]` with per-account `status`, `url` and `error`. A failed publish never blocks the render.

3. **Post an existing media URL.** `orshot_publish_social_post` or `POST /v1/social/publish` with `media_urls`.
4. **Held posts.** `orshot_list_social_posts`, `orshot_get_social_post` (visual card), `orshot_update_social_post`, `orshot_publish_social_draft`, `orshot_discard_social_post`. REST: `GET|PATCH|DELETE /v1/social/posts/:id`, `POST /v1/social/posts/:id/publish`.
5. **Analytics and best time.** `orshot_get_social_analytics`, `orshot_get_social_analytics_daily`, `orshot_get_social_followers`, `orshot_get_best_time_to_post`. REST: `GET /v1/social/analytics`, `/daily`, `/accounts`, `/insights`.

## Common recipes

**OG image on every deploy**

```js
response: { type: "url", format: "png", size: "og-image" }
// <meta property="og:image" content={data.content} />
```

**Bulk from a CSV (certificates, invoices, badges):** `orshot_batch_render_template` with one modifications set per row and `format: "pdf"`, or loop `POST /v1/studio/render`.

**Weekly social graphic, posted as a draft for review:** render with `publish.status: "draft"`, then `orshot_publish_social_draft` after the user approves.

**One design, every size:** `extraSizes: ["1080x1920", "1080x1080", "1200x630"]`.

**TikTok, Instagram or LinkedIn carousel:** see the `orshot-carousel` skill.

**Recurring pipeline:** `references/recurring-automation.md`. Check the workspace logs for the `source` the user already runs (n8n, Make, Zapier, SDK) and add to that; offer Orshot Workflows only when they run nothing yet.

## Reference files

Read these on demand; they are not loaded by default.

| File | When |
| --- | --- |
| `references/api-reference.md` | every REST endpoint: render, templates, signed URLs, brand assets, dynamic URLs, folders, workflows |
| `references/render-configuration.md` | modification types, video options, async jobs, animations, audio, Smart Resize, response types, credits |
| `references/template-design-spec.md` | element schema for creating or editing templates via API |
| `references/recurring-automation.md` | n8n, Make, Zapier, Pipedream, cron and Orshot Workflows playbook |
| `references/integrations-and-errors.md` | integration list, error codes, best practices |
| `references/oauth-developer-apps.md` | building a third-party app on Orshot with OAuth |
| `references/embed.md` | white-label editor embed (iframe, React, Vue) |
| `references/migration.md` | moving from Bannerbear, Placid, Templated, Creatomate or similar |

Any docs page is available as markdown: `https://orshot.com/docs/<path>.md`. The MCP server also serves `orshot://template-design-spec` and `orshot://formats`.

## Quick reference

```bash
# connect
openclaw mcp add orshot --url https://mcp.orshot.com/mcp --transport streamable-http --auth oauth && openclaw mcp login orshot
curl -s https://api.orshot.com/v1/me -H "Authorization: Bearer $ORSHOT_API_KEY"   # REST check

# templates
GET  /v1/studio/templates/all?page=1&limit=20   # list                 orshot_list_studio_templates
GET  /v1/studio/templates/:id                   # modification keys    orshot_get_studio_template_modifications

# render
POST /v1/studio/render                          # { templateId, modifications, response, publish? }   orshot_render_template
POST /v1/generate/:renderType                   # utility templates    orshot_render_library_template
GET  /v1/studio/render-jobs/:id                 # async (video) jobs   orshot_get_render_job
POST /v1/signed-url/create                      # embeddable URL       orshot_create_dynamic_url

# social
GET    /v1/social/accounts?include_health=true  # orshot_list_social_accounts
POST   /v1/social/publish                       # orshot_publish_social_post
GET    /v1/social/posts?status=draft            # orshot_list_social_posts
PATCH  /v1/social/posts/:id                     # orshot_update_social_post
POST   /v1/social/posts/:id/publish             # orshot_publish_social_draft
GET    /v1/social/analytics | /daily | /accounts | /insights

# automation
GET  /v1/workspace/logs?limit=100               # orshot_list_workspace_logs
POST /v1/workflows  /:id/run                    # orshot_run_workflow (confirm before run)
```

Links: https://orshot.com/agents/openclaw, https://orshot.com/docs, https://orshot.com/docs/api-reference, https://orshot.com/pricing, https://orshot.com/templates
