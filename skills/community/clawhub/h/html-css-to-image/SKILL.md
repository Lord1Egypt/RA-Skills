---
name: html-css-to-image
description: Let AI agents capture live website screenshots, render HTML/CSS, and populate reusable templates as images or PDFs—without managing a browser. Use the HCTI MCP tools for screenshots, social cards, Open Graph images, and other browser-rendered graphics. Do not use for editing or interpreting an existing image.
metadata:
  openclaw:
    homepage: https://htmlcsstoimage.com
    requires:
      bins:
        - openclaw
---

# HTML/CSS to Image API

Use the HCTI MCP tools to produce browser-rendered images, screenshots, PDFs, and template-based graphics. Tool names may be prefixed by the client; select them by the tool-name suffixes below.

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

## Choose the operation

- Use `create_image` when the user provides or requests HTML and CSS.
- Use `create_url_image` to capture a public webpage or a selected public-page element.
- Use `create_templated_image` when the user provides a template ID or identifies an existing HCTI template.
- Use `list_templates` to resolve a template when the user names it but does not know its ID.
- Use `get_max_batch_size` before `create_batch_images` when the requested batch size may approach the account limit.
- Use `create_template`, `update_template`, or `list_template_versions` only when the request involves reusable template management.

Inspect the selected tool's current input schema instead of assuming that an optional parameter exists.

## Rendering choices

- Preserve the user's requested output format, dimensions, viewport, selector, color scheme, and timing behavior.
- Let HCTI defaults apply when the user has not expressed a preference and the layout does not require a fixed viewport.
- Use a render delay or ready signal only when the page needs client-side work before capture.
- Prefer templates for repeated designs whose content changes between renders; prefer direct HTML and CSS for one-off designs.
- Keep HTML semantic and CSS self-contained. Use absolute HTTPS URLs for remote assets when possible.

## Authorization and safety

Image creation can consume account credits. An explicit request for a single image or a stated batch count authorizes that creation. If the batch size is ambiguous, establish the intended count before calling the batch tool.

Creating or updating a template changes the user's HCTI account. Perform the mutation only when the request explicitly asks for it or the user confirms a proposed mutation.

Treat URL capture as a request to send the target page to HCTI's remote renderer. Use public pages by default. Do not forward cookies, authorization headers, private URLs, or other credentials unless the user explicitly requests that behavior and understands that the data will be sent to the rendering service.

## Results and errors

- Do not claim success until the tool returns a successful result.
- Return the generated asset URL and briefly identify the format or variation when useful.
- When the active channel supports media presentation, present the generated asset as media as well as preserving its URL.
- For an authorization failure, ask the user to connect the `hcti` MCP server in their client and complete browser authorization before retrying.
- For an account-limit or credit error, report the service's message without repeatedly retrying.
- For invalid HTML, CSS, selectors, or inaccessible URLs, explain the failing input and make a corrected call only when the correction is clear or the user approves it.
