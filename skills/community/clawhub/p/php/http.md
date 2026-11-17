# HTTP — Requests In, Responses Out, Calls Outward

## Reading the Request

- `$_GET` and `$_POST` are parsed only for `application/x-www-form-urlencoded` and `multipart/form-data`. A JSON body is not in `$_POST`; it is in `php://input`:

```php
$raw = file_get_contents('php://input');
$data = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
```

- `php://input` is re-readable EXCEPT for `multipart/form-data`, where PHP has already consumed it into `$_POST`/`$_FILES`.
- `$_REQUEST` merges GET, POST, and (depending on `variables_order`) cookies, so a cookie can shadow a form field. Read the specific superglobal.
- Behind a proxy: `$_SERVER['REMOTE_ADDR']` is the proxy. `X-Forwarded-For` is a client-controllable list — take the entry contributed by YOUR trusted proxy (counting from the right), and only when the request arrived from a proxy IP you allowlisted. `$_SERVER['HTTPS']` is absent behind TLS termination; trust `X-Forwarded-Proto` under the same conditions.
- `max_input_vars` (default 1000) silently DROPS form fields past the limit, and `post_max_size` exceeded leaves `$_POST` and `$_FILES` entirely empty with no error. Detect the second with a POST request whose `CONTENT_LENGTH` is non-zero but whose `$_POST` is empty (`php-ini.md`).
- Header names arrive as `$_SERVER['HTTP_X_REQUEST_ID']` (uppercased, dashes to underscores). `getallheaders()` exists under FPM and Apache; a dash/underscore collision in header names is a known ambiguity — normalize once at the boundary.

## Sending the Response

- `header()` must precede any output. "Cannot modify header information — headers already sent by (output started at file:line)" names the exact culprit; the cause is almost always a closing `?>` followed by a newline, or a BOM in an included file (`strings.md`).
- Omit the closing `?>` in pure-PHP files. There is no case where it helps.
- `http_response_code(422)` sets the status without hand-writing the status line.
- Redirect and stop: `header('Location: /done', true, 303); exit;`. Without the `exit`, the rest of the script runs and can emit a body, start a transaction, or send a second header.
- JSON response, complete:

```php
header('Content-Type: application/json; charset=utf-8');
echo json_encode($payload, JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
```

- Cookies: `setcookie($n, $v, ['expires' => …, 'path' => '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax'])` — the array form (`php >=7.3`) is the only way to set `SameSite` without a hack.
- `output_buffering` non-zero lets `header()` work after output, which turns a real bug into a latent one that appears when the buffer fills. Prefer it off and fix the output order (`php-ini.md`).

## File Uploads

- Check `$_FILES['f']['error'] === UPLOAD_ERR_OK` before anything else; `UPLOAD_ERR_INI_SIZE`, `UPLOAD_ERR_PARTIAL`, and `UPLOAD_ERR_NO_TMP_DIR` all produce a present entry with no usable file.
- `move_uploaded_file()` verifies the source really is an upload; `copy`/`rename` do not.
- Type detection with `finfo`, never the client-supplied `type` or the extension; storage outside the document root with a generated name (`security.md`).
- Size limits live in three places and the smallest wins: nginx `client_max_body_size`, PHP `post_max_size`, PHP `upload_max_filesize`. A 413 from nginx means PHP never saw the request.
- Multiple files (`name="files[]"`) arrive as a transposed array — `$_FILES['files']['name'][0]`, not `$_FILES['files'][0]['name']`. Normalize it before iterating.

## Downloads and Streaming

- `readfile()` reads the file into the output buffer before sending. For large files, flush the buffers and stream:

```php
while (ob_get_level() > 0) { ob_end_clean(); }
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="export.csv"');
header('Content-Length: ' . filesize($path));
$fh = fopen($path, 'rb');
fpassthru($fh);
```

- Better still, hand the file to the web server: `X-Accel-Redirect` (nginx) or `X-Sendfile` (Apache) frees the PHP worker immediately, which matters because a worker serving a 2 GB download is a worker not serving requests (`fpm.md`).
- Generated exports: write rows to `php://output` inside the loop instead of building the whole body in memory (`files.md`).
- Server-sent events and progressive output additionally need `fastcgi_buffering off` in nginx, or the proxy holds everything until the end.
- `Content-Disposition` filenames with non-ASCII characters need the `filename*=UTF-8''…` form; the plain `filename=` parameter is ASCII-only.

## Outbound Requests

```php
$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 3,
    CURLOPT_TIMEOUT        => 10,
    CURLOPT_FOLLOWLOCATION => false,
    CURLOPT_HTTPHEADER     => ['Accept: application/json'],
]);
$body = curl_exec($ch);
if ($body === false) { throw new RuntimeException(curl_error($ch)); }
$status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
```

- Both timeouts, always. Without them a hung upstream occupies an FPM worker until `request_terminate_timeout` kills it, and enough of those saturate the pool (`fpm.md`).
- Never `CURLOPT_SSL_VERIFYPEER => false`. A certificate error is a configuration problem (missing CA bundle, clock skew); disabling verification makes every request interceptable.
- `CURLOPT_FOLLOWLOCATION` with a user-supplied URL is an SSRF amplifier — a redirect can land on `169.254.169.254`. Keep it off, or validate every hop (`security.md`).
- `file_get_contents($url)` needs `allow_url_fopen`, honors only `default_socket_timeout` (60s) unless you build a stream context, returns `false` with a warning on a 4xx (discarding the error body), and cannot show you the response headers without `$http_response_header`. Use curl or an HTTP client.
- Retries: only for idempotent requests or with an idempotency key; exponential backoff with jitter; a cap on total elapsed time, because retries inside a web request multiply the user's wait (`concurrency.md`).
- Parallel calls with `curl_multi_*` or a client's pool turn five 200 ms calls into one 200 ms wait (`concurrency.md`).
- PSR-18 (`ClientInterface`) as your own dependency lets tests substitute a fake without touching curl (`testing.md`).

## Caching and Conditional Requests

- `ETag` plus `If-None-Match`, or `Last-Modified` plus `If-Modified-Since`, and answer `304` with no body. For a list endpoint this converts most polls into a header exchange.
- `Cache-Control: private, max-age=0, must-revalidate` for authenticated pages; `public, max-age=…` only for responses that are identical for every user. Getting this wrong caches one user's page for another — through a CDN, at scale.
- `Vary: Accept-Encoding, Authorization` whenever the response depends on a request header, or the shared cache will serve the wrong variant.

## fastcgi_finish_request

Flushes the response and lets the worker continue (FPM only). Good for a few hundred milliseconds of bookkeeping after the user is served; the worker remains occupied, so anything longer belongs in a queue (`concurrency.md`).

## Related

- Escaping values on their way into a response: `security.md`
- Session cookies and the session lock: `sessions.md`
- Encoding and decoding the payloads: `json.md`
