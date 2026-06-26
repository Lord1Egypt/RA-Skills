# Erlang HTTP Static Server

## inets (built-in)

```bash
erl -s inets -eval 'inets:start(httpd,[{server_name,"NAME"},{document_root, "."},{server_root, "."},{port, 8000},{mime_types,[{"html","text/html"},{"htm","text/html"},{"js","text/javascript"},{"css","text/css"},{"gif","image/gif"},{"jpg","image/jpeg"},{"jpeg","image/jpeg"},{"png","image/png"}]}]).'
```

Features:
- Directory listing: No
- Built into OTP (no install needed)
- Supports custom MIME types
- Configurable via Erlang terms

Custom bind address (add to options):

```erlang
{bind_address, {0,0,0,0}}
```

Note: The `inets` httpd is part of Erlang/OTP and requires no external dependencies. The MIME types must be explicitly configured as shown above.
