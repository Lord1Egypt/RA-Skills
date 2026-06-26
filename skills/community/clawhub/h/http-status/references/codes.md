# HTTP Status Codes — Complete Reference

Sources: RFC 7231, RFC 7235, RFC 4918 (WebDAV), RFC 6585, RFC 7538, RFC 8297, RFC 8470, Nginx docs, Cloudflare docs

---

## 1xx — Informational

| Code | Name | Meaning | Source |
|------|------|---------|--------|
| 100 | Continue | Server received request headers; client should proceed to send body | RFC 7231 |
| 101 | Switching Protocols | Server agrees to switch protocols (e.g. HTTP→WebSocket) | RFC 7231 |
| 102 | Processing | Server received and is processing; no response available yet (WebDAV) | RFC 2518 |
| 103 | Early Hints | Preload headers sent before final response | RFC 8297 |

---

## 2xx — Success

| Code | Name | Meaning | Common use |
|------|------|---------|------------|
| 200 | OK | Standard success | GET, POST, PUT responses |
| 201 | Created | Resource was created | POST that creates a resource |
| 202 | Accepted | Request accepted but not yet processed | Async jobs, queues |
| 203 | Non-Authoritative Information | Returned meta-information from a third party, not origin server | Proxies |
| 204 | No Content | Success, no body to return | DELETE, PUT with no return body |
| 205 | Reset Content | Client should reset its document view | Form submission reset |
| 206 | Partial Content | Partial GET response (range requests) | Video streaming, download resume |
| 207 | Multi-Status | Multiple status codes in body (WebDAV) | WebDAV batch operations |
| 208 | Already Reported | Members already enumerated (WebDAV) | WebDAV |
| 226 | IM Used | Response is result of instance-manipulations | Delta encoding (rare) |

---

## 3xx — Redirection

| Code | Name | Meaning | Notes |
|------|------|---------|-------|
| 300 | Multiple Choices | Multiple options for the resource | Rarely used |
| 301 | Moved Permanently | Resource has moved permanently; update bookmarks | Method may change to GET |
| 302 | Found | Resource temporarily at different URI | Method may change to GET |
| 303 | See Other | Redirect to another URI using GET | After POST/PUT/DELETE |
| 304 | Not Modified | Cached version is still valid | Conditional GET with ETag/If-Modified-Since |
| 305 | Use Proxy | Resource must be accessed through proxy | Deprecated |
| 307 | Temporary Redirect | Same as 302 but method must not change | Preserves POST method |
| 308 | Permanent Redirect | Same as 301 but method must not change | Preserves POST method |

---

## 4xx — Client Errors

| Code | Name | Meaning | Common causes & fixes |
|------|------|---------|----------------------|
| 400 | Bad Request | Server cannot process malformed request | Syntax error, invalid JSON, missing required field |
| 401 | Unauthorized | Authentication required / failed | Missing/expired token; re-authenticate |
| 402 | Payment Required | Reserved; used by some APIs for billing | Upgrade plan or add payment method |
| 403 | Forbidden | Authenticated but not authorized | Wrong role/permission; contact admin |
| 404 | Not Found | Resource does not exist | Wrong URL, resource deleted, wrong ID |
| 405 | Method Not Allowed | HTTP method not supported for this endpoint | Check API docs for allowed methods |
| 406 | Not Acceptable | Server can't produce response matching Accept headers | Adjust Accept header |
| 407 | Proxy Authentication Required | Proxy requires authentication | Configure proxy credentials |
| 408 | Request Timeout | Server timed out waiting for request | Retry; check network latency |
| 409 | Conflict | Request conflicts with current state | Concurrent update conflict, duplicate key |
| 410 | Gone | Resource permanently removed | Don't retry; remove from index |
| 411 | Length Required | Content-Length header required | Add Content-Length header |
| 412 | Precondition Failed | Precondition in headers evaluated to false | Check If-Match / If-Unmodified-Since |
| 413 | Content Too Large | Request body exceeds server limit | Reduce payload size or upload in chunks |
| 414 | URI Too Long | Request URI too long | Shorten URL or use POST with body |
| 415 | Unsupported Media Type | Content-Type not supported | Change Content-Type header |
| 416 | Range Not Satisfiable | Range header cannot be satisfied | Check file size, fix Range header |
| 417 | Expectation Failed | Expect header cannot be met | Remove Expect header |
| 418 | I'm a teapot | Easter egg from RFC 2324 (Hyper Text Coffee Pot Control Protocol) | Real RFC; used as an Easter egg |
| 421 | Misdirected Request | Request directed at server unable to respond | TLS certificate mismatch |
| 422 | Unprocessable Content | Request well-formed but semantically invalid | Validation errors (e.g. invalid email format) |
| 423 | Locked | Resource is locked (WebDAV) | WebDAV lock contention |
| 424 | Failed Dependency | Previous request failed (WebDAV) | WebDAV |
| 425 | Too Early | Replay attack risk; won't process early data | TLS 1.3 early data |
| 426 | Upgrade Required | Client must upgrade protocol | Server requires TLS or different HTTP version |
| 428 | Precondition Required | Origin server requires conditional request | Add If-Match header to prevent lost updates |
| 429 | Too Many Requests | Rate limit exceeded | Back off; respect Retry-After header |
| 431 | Request Header Fields Too Large | Header fields too large | Reduce cookie size or header count |
| 451 | Unavailable For Legal Reasons | Resource unavailable for legal reasons | Government/court order; content removed |

---

## 5xx — Server Errors

| Code | Name | Meaning | Common causes & fixes |
|------|------|---------|----------------------|
| 500 | Internal Server Error | Generic server-side error | Server bug; check server logs; retry after a moment |
| 501 | Not Implemented | Server doesn't support this functionality | Feature not implemented; check API docs |
| 502 | Bad Gateway | Upstream server returned invalid response | Upstream service down; retry with backoff |
| 503 | Service Unavailable | Server temporarily unavailable | Overloaded or maintenance; retry with Retry-After |
| 504 | Gateway Timeout | Upstream server didn't respond in time | Slow upstream; retry; increase timeout if configurable |
| 505 | HTTP Version Not Supported | HTTP version not supported | Use HTTP/1.1 or HTTP/2 |
| 506 | Variant Also Negotiates | Content negotiation loop | Server misconfiguration |
| 507 | Insufficient Storage | Server out of storage (WebDAV) | Free up server storage |
| 508 | Loop Detected | Infinite loop detected (WebDAV) | WebDAV |
| 510 | Not Extended | Further extensions required | Server requires request extension |
| 511 | Network Authentication Required | Client must authenticate to access network | Captive portal (hotel/airport WiFi) |

---

## Nginx Unofficial Codes

| Code | Name | Meaning |
|------|------|---------|
| 444 | No Response | Nginx closes connection without sending response (blocks malicious requests) |
| 494 | Request Header Too Large | Header too large (pre-494 Nginx) |
| 495 | SSL Certificate Error | Client SSL cert error |
| 496 | SSL Certificate Required | Client cert required but not provided |
| 497 | HTTP Request Sent to HTTPS Port | HTTP request sent to HTTPS-only port |
| 499 | Client Closed Request | Client closed connection before server responded (common with slow APIs) |

---

## Cloudflare Codes

| Code | Name | Meaning |
|------|------|---------|
| 520 | Web Server Returns Unknown Error | Origin returned empty/unexpected response |
| 521 | Web Server Is Down | Origin refused Cloudflare connection |
| 522 | Connection Timed Out | Cloudflare TCP handshake with origin timed out |
| 523 | Origin Is Unreachable | Cloudflare cannot reach origin (DNS failure, routing issue) |
| 524 | A Timeout Occurred | Cloudflare connected but origin didn't respond within 100s |
| 525 | SSL Handshake Failed | Cloudflare–origin SSL handshake failed |
| 526 | Invalid SSL Certificate | Origin's SSL cert is invalid |
| 527 | Railgun Error | Railgun connection error (deprecated) |
| 530 | Origin DNS Error | Cloudflare cannot resolve origin hostname |

---

## AWS Elastic Load Balancer Codes

| Code | Meaning |
|------|---------|
| 000 | ELB: idle timeout exceeded before connection established |
| 460 | Client closed connection before ELB could send response |
| 463 | X-Forwarded-For header with >30 IPs |
| 464 | Incompatible protocol in target group |
| 561 | Unauthorized (from identity provider) |

---

## Common Unofficial / Informal Codes

| Code | Name | Used by |
|------|------|---------|
| 419 | Page Expired | Laravel (CSRF token expired) |
| 420 | Method Failure / Enhance Your Calm | Spring (method failure); Twitter (rate limit, deprecated) |
| 430 | Request Header Fields Too Large | Shopify |
| 450 | Blocked by Windows Parental Controls | Microsoft |
| 498 | Invalid Token | Esri/ArcGIS |
| 509 | Bandwidth Limit Exceeded | cPanel/WHM hosting |
| 529 | Site Overloaded | Qualys / Shopify |
| 598 | Network Read Timeout Error | Informal proxy code |
| 599 | Network Connect Timeout Error | Informal proxy code |

---

## Quick Decision Guide

### API debugging checklist

```
Got 4xx? → Your request has a problem:
  400 → Fix syntax / body format
  401 → Authenticate / refresh token
  403 → Check permissions
  404 → Verify URL and resource ID
  405 → Check allowed HTTP methods
  409 → Handle concurrent update conflict
  422 → Fix validation errors
  429 → Add rate limiting / backoff

Got 5xx? → Server has a problem:
  500 → Check server logs; transient — retry once
  502 → Upstream down; wait and retry
  503 → Server overloaded; respect Retry-After
  504 → Timeout; increase client timeout or retry
  Cloudflare 5xx → Check origin server health
```

### Safe to retry?

```
✅ Retry (with exponential backoff):  408, 429, 500, 502, 503, 504
⚠️  Retry carefully (idempotent only):  409, 423
❌ Don't retry without fixing:        400, 401, 403, 404, 405, 410, 422
```
