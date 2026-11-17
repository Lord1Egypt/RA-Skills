# Redirects & Rewrites

## return vs rewrite (the default and the exception)

- `return 301 https://example.com$request_uri;` is the default tool: cheapest, clearest, no regex engine.
- `rewrite` only when the URL must be TRANSFORMED with captures: `rewrite ^/old/(.*)$ /new/$1 permanent;`.
- Query strings behave differently: `rewrite` appends the original query automatically (kill it with a trailing `?` on the replacement); `return 301 /new` does NOT — append `$is_args$args` explicitly if you need it.

## Status Codes (method and cache semantics)

| Code | Cache | Method preserved | Use |
|---|---|---|---|
| 301 | Cached aggressively by browsers, effectively forever | No — POST may become GET | Permanent moves, AFTER verification |
| 302 | Not cached | No | Temporary, and the rollout stage of every 301 |
| 307 | Not cached | Yes — POST stays POST with body | Temporary redirect of API/form endpoints |
| 308 | Cached | Yes | Permanent move of endpoints that receive POST |

- Rollout ramp: ship 302 → verify with `curl -sI` (shows `Location` without following) → switch to 301. A wrong 301 lives in visitors' browser caches with no way to purge; that is why the ramp exists.
- "I fixed the redirect but my browser still loops" = cached 301. Test in curl or a private window; the config is probably already correct.
- Redirecting POST endpoints with 301/302 silently drops the body — the classic "webhook works direct, fails through the redirect". Use 307/308.

## rewrite Flags

- `last` — stop this rewrite set, re-enter location matching with the new URI. More than 10 cycles = `rewrite or internal redirection cycle` error 500.
- `break` — stop rewriting, stay in the CURRENT location and process the request here. The right flag inside a location that also has `proxy_pass`/`root`.
- `redirect` (302) / `permanent` (301) — external redirect; the client sees the new URL.
- No flag, in `server` context: processing continues to location matching with the rewritten URI — fine; no flag inside a `location`: the rewrite set re-runs, easy to loop.

## Canonical Host (www ↔ apex, http → https)

Separate server blocks beat conditionals — the match happens at server selection, zero per-request logic:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://example.com$request_uri;
}
server {
    listen 443 ssl;
    server_name www.example.com;
    # cert must cover www — SAN rules in ssl.md
    return 301 https://example.com$request_uri;
}
server {
    listen 443 ssl;
    server_name example.com;
    # the real site
}
```

Behind a CDN/LB that terminates TLS, the http→https decision must read `X-Forwarded-Proto`, not `$scheme` — the loop and its fix are in `ssl.md`.

## The Port-Leak Redirect (containers and nonstandard ports)

nginx auto-issues a 301 when a directory is requested without its trailing slash, and builds that URL from the port it LISTENS on. nginx on 8080 behind an LB on 443 → the redirect sends users to `https://host:8080/path/`.

- Fix: `absolute_redirect off;` (nginx >=1.11.8, emits relative `Location`) or `port_in_redirect off;` if you only need the port dropped.
- Same class of bug from the backend's own redirects through a proxy → `proxy_redirect` maps upstream `Location` headers; default `proxy_redirect default` handles the simple `proxy_pass` case only.

## Bulk Redirects (the map pattern)

A location block per legacy URL dies at scale; `map` is O(1) at thousands of entries:

```nginx
map $request_uri $redirect_to {
    default              "";
    /old-pricing         /pricing;
    /blog/2019-post      /blog/updated-post;
    ~^/docs/v1/(?<p>.*)$ /docs/v2/$p;
}
server {
    if ($redirect_to) { return 301 $redirect_to; }
    ...
}
```

- `$request_uri` includes the query string — entries with query params must match it or use `$uri` as the map source (then re-append `$is_args$args`).
- Big lists: `include /etc/nginx/redirects.map;` inside the map block; the file is regeneratable from a CMS export.
- `server`-level `if` with only `return` inside is the safe use of `if` (`semantics.md` for why everything else isn't).

## Trailing Slashes & Merges

- `merge_slashes on` (default) collapses `//` before location matching — turn it off only if URLs legitimately embed encoded slashes, and re-audit regex locations if you do.
- Enforcing a no-trailing-slash canon: `rewrite ^/(.*)/$ /$1 permanent;` — but exclude the root (`location = /` matches first) and remember directories will re-add it via the auto-redirect above.

## Diagnosis

`curl -sIL -o /dev/null -w '%{url_effective} %{num_redirects}\n' <url>` — follows the chain and counts hops. More than 2 hops on a canonical URL (http→https→www-strip should be collapsible to one) wastes a round trip per visit; collapse the chain into single-jump rules per entry point.
