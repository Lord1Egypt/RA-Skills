# Elixir HTTP Static Server

## Using :inets (Elixir 1.17+)

Elixir can leverage Erlang's built-in `:inets` module:

```bash
elixir --no-halt -e '
Application.start(:inets)
:inets.start(:httpd,
  port: 8000,
  server_root: ~c".",
  document_root: ~c".",
  server_name: ~c"httpd",
  mime_types: [
    {~c"html", ~c"text/html"},
    {~c"js", ~c"text/javascript"},
    {~c"css", ~c"text/css"},
    {~c"png", ~c"image/png"},
    {~c"jpg", ~c"image/jpeg"}
  ]
)
'
```

Features:
- Directory listing: No
- No hex dependencies needed
- Uses Erlang OTP under the hood
- Requires explicit MIME type configuration

## Using Plug (with Mix project)

For a more full-featured option within a Mix project:

```elixir
# In mix.exs, add {:plug_cowboy, "~> 2.0"}
# Then:
Mix.install([:plug_cowboy])

defmodule StaticServer do
  use Plug.Router
  plug Plug.Static, at: "/", from: "."
  plug :match
  plug :dispatch
  match _ do send_resp(conn, 404, "Not found") end
end

Plug.Cowboy.http(StaticServer, [], port: 8000)
Process.sleep(:infinity)
```

Run:

```bash
elixir static_server.exs
```

Features:
- Directory listing: No (add custom handler)
- Full Plug ecosystem
- Production-grade (Cowboy server)
