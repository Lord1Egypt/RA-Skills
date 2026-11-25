# Connect to Open Agent Guide

Read this when configuring MCP, installing the CLI, or choosing authentication.

## MCP server (read-only except feedback)

Connect an MCP client to `$OAG_BASE_URL/mcp` with Streamable HTTP. The endpoint
has no persistent sessions or server push.

Catalog reads work anonymously. For higher rate limits, use a personal `oag_`
API token or connect through OAuth with the `mcp:read` scope. OAuth requires
interactive consent and an email-verified account. OAuth credentials work only
at `/mcp`; they cannot authorize direct REST calls, A2A, catalog submissions,
reviews, or account management. Both authentication methods support the
`submit_feedback` tool.

The tools are:

- `search_products`: filter products by search text and structured constraints.
- `get_product`: read a product by `product`, with score and evidence.
- `get_product_coverage`: read coverage gaps for `product` before contributing.
- `list_categories`: look up category slugs.
- `list_jobs_to_be_done`: look up job-to-be-done slugs.
- `list_capabilities`: look up capability slugs.
- `list_compliance_certifications`: look up compliance certification slugs.
- `submit_feedback`: report a service problem with authentication.

Use `expand` on `search_products` or `get_product` to include related records.
Use `search`, `page_size`, and `cursor` for searches and pagination. Read the
[MCP setup guide](https://www.openagentguide.com/mcp/guide.md) for connection
instructions. Catalog submissions use the HTTP API or the CLI.

## CLI installation

Supported platforms are macOS and Linux with Python 3.12, 3.13, 3.14, or 3.15.
Install the public package from PyPI:

```sh
uv tool install open-agent-guide
uv tool upgrade open-agent-guide
```

For library use, run `uv add open-agent-guide`. Alternatively, install the
library and CLI with `pip install open-agent-guide` and upgrade with
`pip install --upgrade open-agent-guide`. The package is MIT-licensed. Windows
and standalone executables are not supported.

## Configuration reference

| Variable       | Use                                             | Default                          |
| -------------- | ----------------------------------------------- | -------------------------------- |
| `OAG_TOKEN`    | Authenticated operations and higher read limits | Unset; reads work anonymously    |
| `OAG_BASE_URL` | CLI and HTTP destination                        | `https://www.openagentguide.com` |

This bundle contains instructions and a JSON example. It includes no executable
scripts. MCP runs at the hosted endpoint. The separately installed CLI runs in
the user's environment under the host's permissions.
