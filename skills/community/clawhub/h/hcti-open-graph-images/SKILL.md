---
name: hcti-open-graph-images
description: Create and implement HCTI dynamic Open Graph image configurations that render webpages or populate templates from page metadata. Use for persistent og:image and social-preview URLs, including webpage meta tags, HCTI templates, metadata mappings, proxies, or storage destinations. Do not use for a one-off social image.
metadata:
  openclaw:
    homepage: https://htmlcsstoimage.com
    requires:
      bins:
        - openclaw
---

# HCTI Dynamic Open Graph Images

Use the HCTI MCP tools to create the configuration and finish the website integration. A configuration is not complete until the website publishes its HCTI image URL and any page-specific rendering metadata.

Tool names may be prefixed by the client; select them by the suffixes below. Inspect each selected tool's current input schema instead of assuming an optional parameter exists.

## Connect with OAuth

Requires an HCTI account and available image credits. Rendering consumes the user's allowance and may incur service costs under their plan. Use the hosted MCP server at `https://mcp.hcti.io` with Streamable HTTP and browser-based OAuth. No HCTI API key environment variables are needed.

If HCTI tools are already available in the current client, use that connection. Otherwise, when setting up the integration in OpenClaw, inspect existing server entries with `openclaw mcp list`. For a new connection:

```bash
openclaw mcp add hcti --url https://mcp.hcti.io --transport streamable-http --auth oauth
openclaw mcp login hcti
```

Have the user complete browser authorization and choose their HCTI organization. Do not overwrite an existing `hcti` entry pointing elsewhere. For an existing correct connection, run `openclaw mcp login hcti` to authorize it. Check connectivity with `openclaw mcp doctor hcti --probe`, then ensure the current agent session exposes the HCTI tools before rendering. If it does not, reload the MCP connection or start a new session as supported by the client.

Installing this skill supplies instructions; it does not automatically register or authorize the MCP server. Use the client's OAuth credential storage, and never copy access tokens into skill files, shell commands, or chat. If the installed OpenClaw version lacks these MCP commands, consult its supported connection setup or update it before proceeding.

HTML, CSS, target URLs, template values, and rendering options are processed by the hosted HCTI service. See [HCTI MCP documentation](https://docs.htmlcsstoimage.com/integrations/mcp/) and [OpenClaw MCP setup](https://docs.openclaw.ai/cli/mcp/registry).

## Complete workflow

1. Choose the source website's HTTPS origin and a rendering mode.
2. Resolve any referenced template, proxy, or storage destination before creating the configuration.
3. Call `create_og_config` and retain both returned identifiers:
   - `id` manages the configuration with `get_og_config`, `update_og_config`, and `delete_og_config`.
   - `domain_id` belongs in the public image URL used by the website.
4. Read [references/webpage-integration.md](references/webpage-integration.md), then add the appropriate tags to every source page's server-rendered `<head>`.
5. Build each image URL as `https://hcti.io/v1/og/{domain_id}{pathname}`. The pathname must match the source page under the configuration's `base_url`.
6. Open the HCTI image URL directly and verify the rendered result before treating the integration as complete.

For example, a configuration whose `base_url` is `https://example.com` and whose returned `domain_id` is `DOMAIN_ID` maps:

```text
Source page: https://example.com/articles/product-launch
Image URL:   https://hcti.io/v1/og/DOMAIN_ID/articles/product-launch
```

The corresponding page tag is:

```html
<meta property="og:image" content="https://hcti.io/v1/og/DOMAIN_ID/articles/product-launch">
```

Do not substitute the configuration `id` for `domain_id`. Query strings do not identify a new image; change `hcti:content_version` when the same pathname needs a new render because otherwise-invisible content changed.

## Choose the rendering mode

### Page screenshot

Use `config_type: html_css` to render the source page itself.

- Set `extract_values: true` when individual pages will provide `hcti:*` rendering options.
- Put shared fallback behavior in `default_options`; extracted page values override those defaults.
- Use `hcti:selector` with a unique, stable selector such as `#social-card` when only one element should become the preview.
- Keep large shared CSS in the configuration's defaults. Use `hcti:css` only for page-specific overrides.

### Reusable template

Use `config_type: templated` to render an existing HCTI template with values extracted from each source page.

- If the user provides a template name instead of an ID, call `list_templates`, prefer a clear case-insensitive match, and ask when the match is ambiguous.
- Omit `template_version` to track the latest version; set it only when the user wants the configuration pinned to a particular version.
- Pages can publish values directly with `html:tv:{template_key}` tags.
- `template_values_mapping` can map a standard or custom metadata field into a template key. Each mapping must supply exactly one `meta_key` or `fallback`.
- Direct `html:tv:*` values override mapped values for the same template key.
- The `titles` fallback checks the document `<title>`, then `og:title`, then `twitter:title`. The `descriptions` fallback checks `description`, then `og:description`, then `twitter:description`.

## Connect supporting resources

- Use `list_proxies` or `get_proxy` to resolve an existing proxy when HCTI needs one to reach the source website.
- Use `list_storage_destinations` or `get_storage_destination` when rendered files should be delivered to external storage.
- Create or modify a proxy or storage destination only when the user explicitly requests that separate account change.
- Treat custom request headers as sensitive. Send them only to the source origin and explicitly allowed additional origins, and never repeat secret values in the response.

## Choose social sizing

- Prefer `post_process` when the user has no special requirement. HCTI performs one render per page and adapts it to recognized social-preview sizes afterward.
- Use `set_viewport` only when the content must render independently at each platform size. It can consume multiple renders per page.
- Use `no_optimization` when the original rendered dimensions must be preserved.

Do not publish fixed `og:image:width` or `og:image:height` values when the endpoint may return crawler-specific dimensions. They are appropriate only when the configuration always serves a known fixed size.

## Manage existing configurations

- Use `list_og_configs` to discover configurations and `get_og_config` to inspect one by ID.
- Before `update_og_config`, retrieve the current configuration unless the user supplied the complete desired state. The update replaces the complete configuration, so omitted optional settings are cleared or reset to defaults.
- Use `delete_og_config` only when the user explicitly asks to delete the exact identified configuration.
- `list_og_configs` includes disabled configurations and returns the newest first. Continue with `pagination.next_page_start` only when needed.

## Verify and troubleshoot

After creating or updating a configuration:

1. Confirm that the configuration is enabled and that its stored `base_url`, rendering mode, and referenced resource IDs are correct.
2. Confirm that the source page is publicly reachable over HTTPS and its metadata appears in the initial HTML `<head>`, not only after client-side JavaScript runs.
3. Open the constructed `https://hcti.io/v1/og/...` URL directly and inspect the returned image.
4. If the image is stale, check the configuration's refresh interval, the source page's cache headers or ETag, and `hcti:content_version` before changing the image URL.
5. Remember that social platforms can retain their own cache after the HCTI image changes.

For missing content, clipping, or timing problems, revise the relevant `hcti:*` fields using [references/webpage-integration.md](references/webpage-integration.md) and test the image URL again. Do not repeatedly create new configurations to troubleshoot a page-level metadata problem.

For an authorization failure, ask the user to reconnect HCTI and approve the permissions required for the intended organization. Do not retry a denied mutation until access changes.

After a successful operation, report the configuration name, management `id`, public `domain_id`, enabled state, rendering mode, refresh interval, and an example image URL for the configured origin. Do not claim the website integration is installed unless the relevant website files were actually changed.
