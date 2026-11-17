# obscura 0.2.6 CLI reference

Verbatim `--help` output, captured 2026-11-13 from the Homebrew 0.2.6 binary.
Regenerate with `scripts/smoke.sh --dump-help`; do not hand-edit.

## obscura

```
Obscura - A lightweight headless browser for web scraping and automation

Usage: obscura [OPTIONS] [COMMAND]

Commands:
  serve   
  fetch   
  scrape  
  mcp     
  help    Print this message or the help of the given subcommand(s)

Options:
  -v, --verbose                    
  -p, --port <PORT>                [default: 9222]
      --proxy <PROXY>              
      --stealth                    Enable stealth mode (consistent browser fingerprint, and with the `stealth` build feature, TLS impersonation plus tracker blocking). Global: applies to fetch, serve, scrape, and mcp
      --obey-robots                Respect robots.txt before navigating to an HTTP(S) URL. Global: applies to fetch and scrape
      --user-agent <USER_AGENT>    Override the User-Agent sent with every request. Global: applies to fetch, serve, scrape, and mcp. A subcommand-level --user-agent still wins where one exists
      --storage-dir <STORAGE_DIR>  
      --allow-private-network      Permit fetches to loopback, RFC1918, and link-local addresses. Default is to block them (SSRF fix from #4). Use this for local development against http://localhost:N or http://192.168.x.y. Equivalent to `OBSCURA_ALLOW_PRIVATE_NETWORK=1` but per-process and survives in command pipelines
      --v8-flags <FLAGS>           Pass raw flags to V8, in the same form V8/Chromium/Node accept (e.g. `"--max-old-space-size=4096 --max-semi-space-size=64 --expose-gc"`). Applied once at startup before any isolate is created
  -h, --help                       Print help
  -V, --version                    Print version
```

## obscura fetch

```
Usage: obscura fetch [OPTIONS] [URL]

Arguments:
  [URL]
          

Options:
      --dump <DUMP>
          Possible values:
          - html
          - text
          - links
          - markdown
          - original: Stream the raw HTTP response body verbatim (binary-safe). Bypasses the browser/JS layer — useful for fetching images, JSON, JS, CSS, or any non-HTML resource (cf. issue #117)
          - assets:   One JSON object per line listing every sub-resource URL the rendered page references (script src, link href, img src, iframe src, media sources, embed/object data). Lets callers replay the asset graph with their own HTTP client when they need the originals alongside the page (cf. issue 124)
          - cookies:  Dump all cookies in the browser jar as a JSON array, including HttpOnly cookies that are inaccessible via document.cookie. Useful for extracting session tokens set by anti-bot challenges

  -v, --verbose
          

      --file <FILE>
          Read newline-delimited URLs from a file (one per line; blank lines and lines starting with `#` are skipped). Use `-` for stdin. Enables batch mode: every URL is fetched raw (--dump original) and one JSON status line is printed per URL. For rendered/DOM batch output use `scrape` instead (issue #349)

      --concurrency <CONCURRENCY>
          Number of URLs fetched concurrently in batch mode. Ignored without --file
          
          [default: 1]

      --selector <SELECTOR>
          

      --wait <WAIT>
          Maximum adaptive post-load settle time in seconds. When supplied explicitly, this is a fixed delay; the default is a 5-second cap that returns once the page is quiescent

      --timeout <TIMEOUT>
          [default: 30]

      --proxy <PROXY>
          

      --wait-until <WAIT_UNTIL>
          [default: load]

      --stealth
          Enable stealth mode (consistent browser fingerprint, and with the `stealth` build feature, TLS impersonation plus tracker blocking). Global: applies to fetch, serve, scrape, and mcp

      --user-agent <USER_AGENT>
          

  -e, --eval <EVAL>
          

      --obey-robots
          Respect robots.txt before navigating to an HTTP(S) URL. Global: applies to fetch and scrape

  -o, --output <OUTPUT>
          

  -q, --quiet
          

      --allow-private-network
          Permit fetches to loopback, RFC1918, and link-local addresses. Default is to block them (SSRF fix from #4). Use this for local development against http://localhost:N or http://192.168.x.y. Equivalent to `OBSCURA_ALLOW_PRIVATE_NETWORK=1` but per-process and survives in command pipelines

      --storage-dir <STORAGE_DIR>
          

  -s, --screenshot <FILE>
          Capture the settled page as a PNG. Requires the `render` feature

  -h, --help
          Print help (see a summary with '-h')
```

## obscura scrape

```
Usage: obscura scrape [OPTIONS] [URLS]...

Arguments:
  [URLS]...  

Options:
  -e, --eval <EVAL>                
  -v, --verbose                    
      --concurrency <CONCURRENCY>  [default: 10]
      --format <FORMAT>            [default: json]
      --timeout <TIMEOUT>          [default: 60]
  -q, --quiet                      
      --proxy <PROXY>              
      --stealth                    Enable stealth mode (consistent browser fingerprint, and with the `stealth` build feature, TLS impersonation plus tracker blocking). Global: applies to fetch, serve, scrape, and mcp
      --obey-robots                Respect robots.txt before navigating to an HTTP(S) URL. Global: applies to fetch and scrape
      --user-agent <USER_AGENT>    Override the User-Agent sent with every request. Global: applies to fetch, serve, scrape, and mcp. A subcommand-level --user-agent still wins where one exists
      --allow-private-network      Permit fetches to loopback, RFC1918, and link-local addresses. Default is to block them (SSRF fix from #4). Use this for local development against http://localhost:N or http://192.168.x.y. Equivalent to `OBSCURA_ALLOW_PRIVATE_NETWORK=1` but per-process and survives in command pipelines
  -h, --help                       Print help
```

## obscura serve

```
Usage: obscura serve [OPTIONS]

Options:
  -p, --port <PORT>
          [default: 9222]
  -v, --verbose
          
      --host <HOST>
          [default: 127.0.0.1]
      --proxy <PROXY>
          
      --user-agent <USER_AGENT>
          
      --workers <WORKERS>
          [default: 1]
      --max-connections <MAX_CONNECTIONS>
          Maximum live CDP connections. Each connection runs on its own OS thread with its own V8 isolates, so this bounds the server's thread and memory footprint. Connections beyond the limit are refused with a 503 rather than queued. With --workers N the limit applies to each worker process, so the server-wide maximum is N times this value [default: 128]
      --worker-max-connections <N>
          Recycle a worker after it has served this many CDP connections (/json discovery requests do not count). Needs --workers > 1. The worker drains and a replacement takes its place; off by default
      --stealth
          Enable stealth mode (consistent browser fingerprint, and with the `stealth` build feature, TLS impersonation plus tracker blocking). Global: applies to fetch, serve, scrape, and mcp
      --worker-max-rss <MB>
          Recycle a worker whose resident memory exceeds this many MB, sampled every 2s from /proc (Linux only). Needs --workers > 1
      --obey-robots
          Respect robots.txt before navigating to an HTTP(S) URL. Global: applies to fetch and scrape
      --worker-max-age <SECS>
          Recycle a worker after it has run this many seconds. Needs --workers > 1
      --worker-drain-timeout <SECS>
          Seconds a replaced worker may keep serving its live connections before it is killed [default: 120]
      --ready-file <PATH>
          Atomically publish the bound address after V8 initialization
      --allow-file-access
          Allow CDP clients to navigate to file:// URLs. Off by default so a CDP connection cannot read arbitrary local files. Enable only when serving local HTML for testing and the port is on a trusted network
      --allow-private-network
          Permit fetches to loopback, RFC1918, and link-local addresses. Default is to block them (SSRF fix from #4). Use this for local development against http://localhost:N or http://192.168.x.y. Equivalent to `OBSCURA_ALLOW_PRIVATE_NETWORK=1` but per-process and survives in command pipelines
      --storage-dir <STORAGE_DIR>
          
      --font-dir <DIR>
          Recursively load TTF, TTC, OTF, and OTC files from this directory. Repeat for multiple directories. Requires a render-enabled build
      --quiet
          Suppress all logs (same as on `fetch`). Useful when scraping pages that flood the console with per-page script warnings (issue #264)
  -h, --help
          Print help
```

## obscura mcp

```
Usage: obscura mcp [OPTIONS]

Options:
      --font-dir <DIR>           Recursively load additional font files before the first render
  -v, --verbose                  
      --http                     
      --host <HOST>              [default: 127.0.0.1]
      --port <PORT>              [default: 3000]
      --proxy <PROXY>            
      --user-agent <USER_AGENT>  
      --stealth                  Enable stealth mode (consistent browser fingerprint, and with the `stealth` build feature, TLS impersonation plus tracker blocking). Global: applies to fetch, serve, scrape, and mcp
      --obey-robots              Respect robots.txt before navigating to an HTTP(S) URL. Global: applies to fetch and scrape
      --allow-private-network    Permit fetches to loopback, RFC1918, and link-local addresses. Default is to block them (SSRF fix from #4). Use this for local development against http://localhost:N or http://192.168.x.y. Equivalent to `OBSCURA_ALLOW_PRIVATE_NETWORK=1` but per-process and survives in command pipelines
  -h, --help                     Print help
```

