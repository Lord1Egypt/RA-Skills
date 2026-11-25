---
name: orshot
description: "Image, PDF and video generation from Orshot templates, through the hosted MCP server (OAuth, no API key) or the REST API. Covers connecting, finding a template and its parameter keys, render options (formats, sizes, Smart Resize, batch, async), dynamic image URLs, utility templates (tweet and website screenshots, charts, mockups), posting a render to connected social accounts, wiring it into n8n, Make, Zapier or cron, and the gotchas that break renders (parameterId keys, page1@ prefixes, public image URLs). Use when: \"render my Orshot template\", \"connect Orshot to Claude\", \"call the Orshot API\", \"my modification is ignored\", \"automate this render in n8n\", \"screenshot this tweet\", \"move from Bannerbear to Orshot\". One job end to end: load its skill (orshot-blog-images, orshot-pdf-generator, orshot-video-generator, orshot-ad-creative, orshot-carousel, orshot-youtube-thumbnail, orshot-social-media-content or orshot-social-media-scheduler). NOT for template design craft (use orshot-design)."
homepage: https://orshot.com/agents/skills
license: MIT
metadata:
  author: Orshot
  version: "1.6.2"
  openclaw:
    emoji: "🖼️"
    homepage: https://orshot.com/agents/skills
    primaryEnv: ORSHOT_API_KEY
    requires:
      env: []
      bins: []
    envVars:
      - name: ORSHOT_API_KEY
        required: false
        description: Orshot API key from Workspace Settings > API Keys. Only needed for REST. Not needed when the agent connects through the hosted MCP server with OAuth.
---

# Orshot: generate images, PDFs and videos from templates through the API

Orshot is an API for automated image, PDF and video generation from templates. A template is designed once (in the Orshot studio, imported, or built by an agent), then rendered with new data on every call. The output can be posted to connected social accounts in the same request.

This skill is the flow: which tool or endpoint to call, in what order, and what to check. Parameters, allowed values, limits and response fields live in the docs. Every docs page is readable as markdown at `https://orshot.com/docs/<path>.md`; the docs map at the end lists the pages for each job.

- MCP server: `https://mcp.orshot.com/full`
- REST base: `https://api.orshot.com/v1`

Three things hold in every flow below:

- No API key over the hosted MCP server. It signs in with OAuth. A key is only for cron jobs, servers and n8n.
- The credit cost comes first. Say it before a bulk render.
- Nothing is posted, run or deleted without the user's yes.

## One job end to end? Load its skill

This skill is Orshot itself: connecting, rendering and the gotchas. A whole job has its own skill with the flow and worked examples:

| The job | Skill |
| --- | --- |
| Featured images and OG images for blog posts, in-article images | `orshot-blog-images` |
| Invoices, certificates, reports and other PDFs from rows of data | `orshot-pdf-generator` |
| Reels, Shorts, product and listing videos, animated charts and brand films | `orshot-video-generator` |
| Ads in every Meta, Google and LinkedIn size, A/B variants | `orshot-ad-creative` |
| TikTok, Instagram and LinkedIn carousels | `orshot-carousel` |
| YouTube thumbnails | `orshot-youtube-thumbnail` |
| On-brand social posts and stories | `orshot-social-media-content` |
| Scheduling, posting and analytics across platforms | `orshot-social-media-scheduler` |
| Designing or refining a template | `orshot-design` |

## Connect first

The hosted MCP server is the fastest route and the only one that returns inline previews and design checks.

```bash
# OpenClaw
openclaw mcp add orshot --url https://mcp.orshot.com/full --transport streamable-http --auth oauth
openclaw mcp login orshot

# Claude Code
claude mcp add orshot --transport http https://mcp.orshot.com/full
```

Other clients: https://orshot.com/docs/integrations/mcp-server.md

Confirm with `orshot_get_account`. It returns the plan, credits and which features the plan includes (video, workflows, embed). If it reports an inactive subscription or a used-up limit, that is a billing state, not an auth error. Send the user to https://orshot.com/pricing and stop retrying.

**Headless fallback: REST with an API key.** Use it only when the agent cannot run MCP (a cron job, a server script, n8n). Read the key from the environment.

```bash
curl -s https://api.orshot.com/v1/me -H "Authorization: Bearer $ORSHOT_API_KEY"
```

Do not go on until one of the two works.

## Core workflow

1. **Connect** (above).
2. **Find the template.** `orshot_list_studio_templates` (search by name or tags) or `GET /v1/studio/templates/all`. No template yet? Browse `orshot_list_library_templates`, or design one with the `orshot-design` skill.
3. **Read its keys.** `orshot_get_studio_template_modifications` or `GET /v1/studio/templates/:id`. Never guess a key.
4. **Render.** `orshot_render_template` or `POST /v1/studio/render`.
5. **Deliver or post.** Show the output URL. To post it, pass the URL to `orshot_publish_social_post` (over REST, `publish` on the render also works; see Social posting).
6. **Automate.** Put the call into what the user already runs. Playbook: `references/recurring-automation.md`.
7. **Verify.** `orshot_list_workspace_logs` or `GET /v1/workspace/logs` shows the render and the `source` that made it. Show the output before calling it done.

## Safety rules

- **Confirm before anything leaves the workspace.** Publishing a post, running a workflow (it spends credits and can deliver or post) and deleting a template, workflow or brand asset need an explicit yes. Say what will go where, and when.
- **Default social posts to drafts.** "Prepare", "draft" and "let me look first" mean a draft. A draft reaches nobody until it is published.
- **Show the cost before bulk work.** Renders spend credits and AI modifications spend AI credits ([credits-usage](https://orshot.com/docs/definitions/credits-usage.md)). Say so before a loop of hundreds of renders.
- **Never paste the API key into chat, files or URLs.** Prefer MCP, which has no key.
- **Do not delete anything to "clean up" on your own.**

## Gotchas (read before rendering)

1. **Modifications key by `parameterId`, not layer name.** If a value is ignored, the key is wrong. Fetch the keys instead of guessing.
2. **Multi-page templates need a `pageN@` prefix on every content key** (`"page1@title"`, `"page2@title"`). A bare content key reaches no page; the response carries a warning. A bare dotted style key (`"title.fontSize"`) applies to every page that has that layer. [multi-page-images](https://orshot.com/docs/image-generation/multi-page-images.md)
3. **Studio template ids are numbers; library template ids are slugs** (`"website-screenshot"`). [template-id](https://orshot.com/docs/definitions/template-id.md)
4. **MCP and REST shape the render call differently.** Over MCP, output options are flat arguments of `orshot_render_template` (`format`, `scale`, `includePages`, `size`, `extraSizes`, `background`, `videoOptions`). Over REST they sit inside the `response` object. Posting over MCP is its own tool, `orshot_publish_social_post`.
5. **Long renders must not block.** Over MCP pass `background: true`, then collect with `orshot_get_render_job`. Over REST add `mode: "async"` to `response`, then poll or use a webhook ([async-render-start](https://orshot.com/docs/api-reference/async-render-start.md)). Any template can render as video; the plan must include video.
6. **Image and video URLs in modifications must be public.** The renderer fetches them server side; localhost, expired signed URLs and login-gated URLs fail.
7. **The response shape depends on the page count.** Read the Response section of [render-from-studio-template](https://orshot.com/docs/api-reference/render-from-studio-template.md) before writing code that reads it.
8. **On `429`, back off** for the `Retry-After` seconds.
9. **Publish by account id, never by platform name.** Two accounts on one platform have different ids. Media rules differ per platform: check [social-posting-guidelines](https://orshot.com/docs/publish/social-posting-guidelines.md) before posting. A PDF render posts only to LinkedIn.

## Worked example: one design, several sizes

Prompt: "Render the launch template as an OG image and an Instagram story, title 'We just shipped'."

1. `orshot_list_studio_templates` with `search: "launch"`. One match: id `123`.
2. `orshot_get_studio_template_modifications` with `templateId: 123`. Keys: `title`, `hero_image`.
3. `orshot_render_template`:

```json
{
  "templateId": 123,
  "modifications": { "title": "We just shipped" },
  "format": "png",
  "size": "og-image",
  "extraSizes": ["instagram-story"]
}
```

4. Check: the result lists every output URL and each extra size. A per-size `error` means that one size failed; the others are fine. Show the user every link.

The same render over REST:

```js
await fetch("https://api.orshot.com/v1/studio/render", {
  method: "POST",
  headers: { "Content-Type": "application/json", Authorization: `Bearer ${process.env.ORSHOT_API_KEY}` },
  body: JSON.stringify({
    templateId: 123,
    modifications: { title: "We just shipped" },
    response: { type: "url", format: "png", size: "og-image", extraSizes: ["instagram-story"] },
  }),
});
```

Preset names and size rules: [render-from-studio-template, Smart Resize](https://orshot.com/docs/api-reference/render-from-studio-template.md).

## Worked example: render and hold as a draft post

Prompt: "Render this week's quote card and put it on LinkedIn as a draft."

1. `orshot_list_social_accounts`. Pick the LinkedIn account id, say `3`. An empty list means no account is connected yet; a person connects one in the dashboard ([connect-account](https://orshot.com/docs/publish/connect-account.md)), the API cannot. A draft or scheduled post can still be saved with `platforms` instead of `accounts`; once an account on that platform is connected, add it with `orshot_update_social_post` and send the post. Publishing now needs an account.
2. `orshot_render_template` with the modifications. It returns the image URL.
3. `orshot_publish_social_post` with `mediaUrls: [that URL]`, `accounts: [3]`, `content` and `status: "draft"`. Check the result per account.
4. After the user approves: `orshot_publish_social_draft`. To change it first: `orshot_update_social_post`.

Over REST, the render `publish` object reads `isDraft` and `schedule.scheduledFor` for timing, not `status` ([publish-from-api](https://orshot.com/docs/publish/publish-from-api.md)). To post a file that already exists, use `orshot_publish_social_post` or `POST /v1/social/publish`. Scheduling, analytics and best time to post: the `orshot-social-media-scheduler` skill.

## Other jobs

- **Utility templates** (tweet and website screenshots, bar and comparison charts, app store screenshots, phone mockups, background removal): `orshot_render_library_template` or `POST /v1/generate/:renderType`.
- **Many variants of one template** (a list of names, a set of products): `orshot_batch_render_template`, or loop the REST render. A full invoice or certificate run: `orshot-pdf-generator`.
- **Stable image URLs** for OG tags, emails and embeds: `orshot_create_dynamic_url`. OG images for a whole blog or site: `orshot-blog-images`.
- **Brand assets**: `orshot_get_brand_kit`, `orshot_import_brand_website`.
- **Folders and workspaces**: `orshot_list_template_folders`, `orshot_set_active_workspace`.
- **Coming from another tool**: `references/migration.md`.
- **Recurring jobs** (n8n, Make, Zapier, Pipedream, cron, Orshot Workflows): `references/recurring-automation.md`.

## Docs map

| Job | Docs page |
| --- | --- |
| Render a studio template: body, response object, Smart Resize, PDF, video, publish | https://orshot.com/docs/api-reference/render-from-studio-template.md |
| Render a library (utility) template | https://orshot.com/docs/api-reference/render-from-template.md |
| What modification values can be | https://orshot.com/docs/definitions/modifications.md |
| Style overrides with dot keys | https://orshot.com/docs/orshot-studio/style-parameters.md |
| AI-generated values (`.prompt`) | https://orshot.com/docs/dynamic-parameters/prompt.md |
| Output formats and response types | https://orshot.com/docs/definitions/response-format.md, https://orshot.com/docs/definitions/response-type.md |
| Long renders as jobs | https://orshot.com/docs/api-reference/async-render-start.md |
| Video options, audio, captions | https://orshot.com/docs/video-generation/video-options.md, https://orshot.com/docs/video-generation/adding-subtitles.md |
| PDF options | https://orshot.com/docs/pdf-generation/pdf-options.md |
| Plan a design: the formats brands run for the job, palette, type | `orshot_plan_design` (brief, `job`, size), then `orshot_get_design_spec` for the craft, the packs, the film schema, the layout grammar and the format references |
| Template JSON (pages, elements, styles, animation) | `orshot_get_design_spec` topic `template-json`, https://orshot.com/docs/definitions/template-json.md |
| Create or update templates over REST (Enterprise) | https://orshot.com/docs/api-reference/enterprise-template-create.md |
| List and read templates | https://orshot.com/docs/api-reference/studio-templates-list.md, https://orshot.com/docs/api-reference/studio-template-get.md |
| Dynamic URLs | https://orshot.com/docs/integrations/dynamic-urls.md |
| Signed render URLs (REST) | https://orshot.com/docs/api-reference/generate-signed-url.md |
| Social posting | https://orshot.com/docs/publish/publish-from-api.md, https://orshot.com/docs/api-reference/social-publish.md |
| Social add-on pricing | https://orshot.com/docs/publish/pricing.md |
| Credits | https://orshot.com/docs/definitions/credits-usage.md |
| Errors | https://orshot.com/docs/error-reference.md |
| Workspace logs and `source` values | https://orshot.com/docs/api-reference/workspace-logs.md |
| Workflows over REST | https://orshot.com/docs/api-reference/workflow-create.md |
| n8n, Make, Zapier, Pipedream and other integrations | https://orshot.com/docs/integrations/index.md |
| SDKs (Node, Python, PHP, Ruby) | https://orshot.com/docs/sdks/index.md |
| Importing templates | https://orshot.com/docs/importing-templates/index.md |
| White-label editor embed | https://orshot.com/docs/orshot-embed/introduction.md |
| Third-party apps with OAuth | https://orshot.com/docs/developers/oauth-overview.md |
| MCP setup and tool list | https://orshot.com/docs/integrations/mcp-server.md |

The MCP server also serves `orshot://formats` (output formats and size presets).
