# Safe Payload Playbook — DETECTION ONLY

Every payload in this document is a **non-destructive detection probe**. They
are designed to confirm the presence of a vulnerability class WITHOUT
exfiltrating data, mutating server state, or causing denial of service.

## Guardrails (apply to ALL payloads below)

1. Only send payloads to in-scope targets (see safety_policy.md §2).
2. Route every request through the rate limiter (≤ 3 rps default).
3. L4 actions (write methods, internal SSRF sinks, privilege escalation)
   require human approval and are blocked in `safe_mode`.
4. Never include real secrets, real PII, or real production credentials in a
   payload. Use the marker `PTSKILLTEST` in payload content so responses can
   be unambiguously attributed to the test.
5. If a payload produces an unexpected destructive effect, STOP, log it, and
   abort the run.

## XSS (Reflected / Stored) — DETECTION

Goal: confirm unescaped reflection of a benign marker.

- Probe value: `PTSKILLTEST<xss>9a3f`
- Inject into every reflected parameter (query, path, fragment, JSON body
  field, form field).
- Detection signal: the exact string `PTSKILLTEST<xss>9a3f` OR the decoded
  form appears in the response body without HTML encoding of `<`, `>`.
- Do NOT execute script. Do NOT use `onerror`, `onload`, or event handlers
  that fetch external resources. Use a static marker only.
- Stored XSS: submit the marker via an input form, then fetch the page that
  renders the stored value; confirm reflection. Clean up the stored entry if
  the target provides a delete API (L4, requires approval).

## SQL Injection — DETECTION

Goal: confirm a SQL syntax error or boolean differential, WITHOUT extracting
data.

### Error-based

- Probe: `PTSKILLTEST'`  (single quote)
- Detection signal: response contains a DB-engine error signature
  (`SQL syntax`, `unterminated quoted string`, `ORA-`, `PG::SyntaxError`,
  `sqlite3.OperationalError`, etc.).

### Boolean-based differential

- Baseline request: `id=1`
- TRUE probe: `id=1 AND 1=1`
- FALSE probe: `id=1 AND 1=2`
- Detection signal: TRUE response matches baseline length/shape, FALSE
  response differs meaningfully (length delta beyond noise threshold, or a
  status/content marker differs). Record both responses as evidence.

### Time-based (capped)

- Probe: `id=1; SELECT pg_sleep(2) --`  (or engine equivalent)
- Threshold: response time ≥ baseline + 1.8s AND ≤ 3s (cap to avoid DoS).
- Only ONE time-based probe per parameter per run to limit load.

Never use `UNION SELECT` to extract real table data in detection mode. If
boolean/time confirms injection, mark `detected` and stop; do not enumerate.

## SSRF — DETECTION

Goal: confirm the server fetches a user-supplied URL, using an authorized
out-of-band sink. NEVER point the server at internal admin endpoints during
detection.

- Requires: a user-controlled callback sink declared in
  `ctx.config.ssrf_sink` (e.g., `https://oob.authorized.test/<run_id>`).
- Requires: human approval (L4) even in non-safe mode, because the server
  initiates an outbound request.
- Probe: set the suspect parameter (e.g., `url=`, `image=`, `webhook=`) to
  `https://oob.authorized.test/<run_id>/PTSKILLTEST`.
- Detection signal: a callback hit arrives at the sink within 30s containing
  the `<run_id>` marker.
- Do NOT request `127.0.0.1`, `169.254.169.254`, internal IPs, or cloud
  metadata endpoints in detection mode. Those are L4 and require explicit
  approval and a separate, documented test plan.

## IDOR / Access Control — DETECTION

Goal: confirm an object accessible by user A is also accessible by user B (or
unauthenticated) when it should not be.

- Requires: two test accounts (or one account + unauthenticated) provided in
  `ctx.credentials` for L3 testing.
- Method:
  1. As user A, identify an object id and capture the response (baseline 200
     with data).
  2. As user B (or unauthenticated), request the SAME object id.
  3. Detection signal: user B receives a 200 with user-A's data (status and
     content differential vs an expected 403/404).
- Use synthetic test objects created for the run when possible; do not probe
  arbitrary real user ids.
- Compare response bodies for data leakage of fields that should differ per
  user.

## Misconfiguration — DETECTION (L1–L2)

These are passive/safe checks; no payloads sent that mutate state.

- Default credentials: probe known login endpoints with a SMALL, bounded set
  (`admin/admin`, `admin/password`) ONLY against in-scope staging/dev targets
  with human approval. Stop on first success; do not enumerate.
- Verbose headers: inspect response headers for `Server`, `X-Powered-By`,
  `X-AspNet-Version`, etc. Flag versions with known CVEs.
- Missing security headers: flag absence of `Strict-Transport-Security`,
  `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors`,
  `Content-Security-Policy`.
- Exposed admin panels: GET common paths (`/admin`, `/wp-admin`,
  `/.git/config`, `/.env`, `/server-status`) at low rate; flag 200/401/403
  that reveal existence. Never attempt to read `.env` contents — flag
  existence only and mark `safe_poc` true based on status code.
- Directory listing: flag responses where an `Index of /` page is returned.
- TLS misconfig: note expired/self-signed/weak-cipher certs during recon.

## LOW Severity — DETECTION (L1–L2)

These are defense-in-depth / information-disclosure checks. Non-destructive,
read-only.

### Information Disclosure (`info_leak`)

- Verbose error pages: trigger an error (e.g., `?id=abc` where numeric
  expected, malformed JSON body) and inspect for stack traces, file paths,
  framework version banners, SQL fragments.
- Backup/source files: GET `/<path>.bak`, `/<path>.old`, `/<path>.swp`,
  `/<path>~`, `/.DS_Store`, `/web.config.bak`, `/backup.sql` at low rate.
  Flag any 200 with non-trivial size (>512 bytes) as candidate.
- Source map exposure: GET `/static/js/main.js.map`, `/app.js.map`; flag 200
  responses (reveals client-side source structure).
- Comments leakage: grep response HTML/JS for `TODO`, `FIXME`, internal host
  names, email addresses, API keys patterns (`AKIA[0-9A-Z]{16}`,
  `ghp_[a-zA-Z0-9]{36}`, `-----BEGIN`).
- Detection signal: response contains a sensitive pattern OR a 200 on a
  backup/source-map path. `safe_poc` = true (read-only).

### Open Redirect (`open_redirect`)

- Probe parameter names commonly used for redirects: `next`, `url`, `redirect`,
  `return`, `returnUrl`, `goto`, `target`, `dest`, `continue`.
- Probe values (use an authorized external host declared in
  `ctx.config.redirect_sink`, default `https://oob.authorized.test`):
  - `?next=https://oob.authorized.test/PTSKILLTEST`
  - `?next=//oob.authorized.test/PTSKILLTEST` (protocol-relative)
  - `?next=/\/oob.authorized.test/PTSKILLTEST` (backslash bypass)
- Detection signal: server returns a 3xx with `Location` containing the sink,
  OR renders a meta-refresh / JS redirect to the sink. Do NOT follow the
  redirect during detection.
- `safe_poc` = true (no state change; user must click).

### CSRF — weak token / missing (`csrf`)

- Identify state-changing endpoints (POST/PUT/DELETE) discovered in recon.
- For each, check:
  1. Presence of a CSRF token parameter / header (`csrf`, `csrf_token`,
     `X-CSRF-Token`, `authenticity_token`).
  2. If a token exists, send the request with the token REMOVED and with the
     token BLANK. If the request still succeeds (200/302 to success page),
     flag weak/missing CSRF validation.
  3. If no token at all AND the endpoint relies solely on a session cookie
     (no `SameSite=Strict/Lax` on the cookie), flag missing CSRF protection.
- Detection signal: state-changing request succeeds without valid token.
- IMPORTANT: only test against synthetic test objects created for the run; do
  not mutate real data. Mark `safe_poc` = true if a synthetic object was used
  and cleaned up.

## MEDIUM Severity — DETECTION (L2–L3)

### Path Traversal — read-only (`path_traversal`)

- Probe parameter names: `file`, `path`, `page`, `template`, `download`,
  `doc`, `image`, `static`.
- Probe values (sequence, stop on first hit):
  - `../../../../etc/passwd` (unix)
  - `..\..\..\..\windows\win.ini` (windows)
  - `....//....//....//etc/passwd` (filter bypass)
  - `%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd` (encoded)
- Detection signal: response contains `root:x:0:0:` (unix) or
  `[fonts]`/`[extensions]` (windows win.ini), OR response size/shape differs
  significantly from a benign baseline request.
- Read-only: do NOT attempt to read secrets (`/etc/shadow`, `.env`,
  `id_rsa`). Flag existence of traversal capability only; deeper reads are L4.
- `safe_poc` = true.

### XXE — DETECTION (`xxe`)

- Applicable to endpoints accepting XML (`Content-Type: application/xml`,
  `text/xml`), discovered via recon or by probing JSON→XML content negotiation.
- Probe (entity expansion to an authorized sink, NOT file exfiltration):
  ```xml
  <?xml version="1.0"?>
  <!DOCTYPE r [<!ENTITY x SYSTEM "https://oob.authorized.test/PTSKILLTEST-xxe">]>
  <r>&x;</r>
  ```
- Detection signal: callback hit at the sink within 30s containing
  `PTSKILLTEST-xxe`. Alternatively, error-based: if the parser echoes the
  entity resolution error mentioning the sink URL, flag as confirmed.
- NEVER use `file://`, `expect://`, or `php://` schemes in detection. Those
  are L4 (local file read) and require approval.
- `safe_poc` = true (OOB to authorized sink only).

### SSTI — reflection-only (`ssti`)

- Probe template syntax into reflected parameters and inspect the rendered
  output (NOT for code execution):
  - Jinja2: `{{7*7}}` → look for `49`
  - Twig: `{{7*'7'}}` → look for `49`
  - Freemarker: `${7*7}` → look for `49`
  - ERB: `<%= 7*7 %>` → look for `49`
  - Velocity: `#set($x=7*7)$x` → look for `49`
- Probe value should carry the marker: `PTSKILLTEST{{7*7}}`
- Detection signal: response contains the arithmetic result (`49`) AND the
  marker prefix. Distinguish from literal reflection (input `{{7*7}}` echoed
  unchanged = NOT SSTI).
- Do NOT probe for RCE gadgets (`__class__`, `os.popen`, `freemarker.template.utility.Execute`).
  Those escalate to L4; flag SSTI presence and stop.
- `safe_poc` = true.

### Deserialization — probe-only (`deserialization`)

- Identify endpoints accepting serialized formats: `application/octet-stream`
  with Java (`rO0AB`), .NET (`AAEAAAD/////`), PHP (`O:N:"..."`), Python
  (`gASV`/pickle) magic bytes in recon or via content-type probing.
- Detection (NON-exploiting):
  - Send a syntactically-valid but semantically-innocuous serialized object
    of the detected framework (e.g., a Java HashMap, a PHP object with no
    __wakeup side effects).
  - Send a deliberately malformed serialized blob.
  - Detection signal: a 500 error with a stack trace revealing the
    deserialization framework AND that user input reaches the deserializer
    (e.g., `java.io.InvalidClassException`, `unserialize()`, `pickle.loads`).
- NEVER send gadget-chain payloads (ysoserial, PHPGGC). Those are L4 RCE.
- `safe_poc` = true (capability confirmed, no exploitation).

### Command Injection — probe (`command_injection`)

- Probe parameter names: `host`, `ip`, `ping`, `cmd`, `exec`, `name`, `file`.
- Probe values (time-based, capped, NON-output):
  - `;sleep 3 #`
  - `|sleep 3`
  - `` `sleep 3` ``
  - `$(sleep 3)`
- Baseline timing first; a clean parameter should return in <1s.
- Detection signal: response time ≥ baseline + 2.5s AND ≤ 4s (cap to avoid
  DoS). Only ONE time-based probe per parameter per run.
- Do NOT use output-bearing payloads (`;id`, `;cat /etc/passwd`,
  `$(whoami)`). Those are L4 (data exfiltration). Flag presence and stop.
- `safe_poc` = true (time-based only).

## HIGH Severity — DETECTION (L3, L4 gated)

### Stored XSS (`xss` stored → high)

- Same marker technique as reflected XSS, but submit via a write endpoint
  (comment, profile bio, message) then render the read endpoint.
- If the stored marker persists across sessions AND reflects unescaped to
  OTHER users, severity = high (cross-user).
- Detection signal: marker appears unescaped on a page viewed by a different
  test account.
- Cleanup: delete the stored test entry (L4, requires approval).

### RCE — capability confirmation (`rce`)

- ONLY after `command_injection`, `ssti`, or `deserialization` is already
  validated at medium; this is an L4 escalation requiring human approval and
  disabled in `safe_mode`.
- Permitted probe (time-based only, same caps as command injection):
  - On a confirmed SSTI: `{{''.__class__.__mro__[1].__subclasses__()}}` is
    FORBIDDEN. Use only `{{7*7}}`-class arithmetic which is already done at
    medium. RCE confirmation here = a second, DIFFERENT arithmetic gadget
    succeeding (e.g., `{{7*'7'}}` yielding `49` in Twig) to confirm template
    context = code context.
  - On confirmed command injection: do NOT run `id`/`whoami`. Confirm via a
    SECOND independent time-based payload to rule out false positive.
- If safe_mode, RCE probe is BLOCKED; the medium finding is reported as the
  terminal finding and `execution_log` notes "RCE escalation skipped
  (safe_mode)".
- `safe_poc` = true only if no data was exfiltrated and no persistent change
  made.

### Auth Bypass (`auth_bypass`)

- Requires two test accounts (L3) or one account + unauthenticated.
- Methods:
  1. **Default/weak credential**: only against explicitly approved staging
     targets; bounded set (`admin/admin`, `admin/password`); stop on first
     success.
  2. **JWT manipulation**: if the app uses JWT, decode the token; test
     `alg:none`, `alg:HS256` with `kid` path traversal (read-only signal:
     error message change), key confusion (RS256→HS256 with public key).
     Flag if a manipulated token is accepted (verified by hitting `/me` and
     getting a different identity).
  3. **Password reset token predictability**: request a reset for a test
     account; inspect the token for sequential/time-based predictability. Do
     NOT use the token; flag the weakness.
- Detection signal: an unauthenticated or wrong-identity request is accepted
  as an authenticated/different-identity session.
- `safe_poc` = true if no real account was compromised (synthetic accounts
  only).

### Privilege Escalation (`priv_esc`)

- Requires two test accounts with DIFFERENT roles (e.g., `user` and `admin`)
  provided in `ctx.credentials`.
- Horizontal: already covered by `idor`.
- Vertical: as the low-privilege user, attempt to call admin-only endpoints
  discovered in recon (`/admin/users`, `/admin/config`). Detection signal:
  low-priv user receives 200 with admin data instead of 403.
- Role manipulation: if the app carries a role claim in JWT/cookie, test
  flipping `role:user` → `role:admin` (re-sign only if key known; otherwise
  test `alg:none`). Flag if accepted.
- `safe_poc` = true if synthetic accounts only.

### Data Exposure — bulk / PII (`data_exposure`)

- Triggered when a validated finding (sqli, idor, path_traversal, ssrf)
  exposes a response containing PII patterns at scale:
  - ≥10 email addresses, OR
  - phone/SSN/credit-card number patterns, OR
  - keys named `password`, `secret`, `api_key`, `token` with non-empty values.
- Detection signal: regex match counts exceed thresholds above.
- This is a classification UPGRADE on top of an existing validated finding;
  it raises severity to critical and adds a `data_exposure` finding linked
  via attack path.
- `safe_poc` = true if detection used only marker responses and did not
  harvest real user records (synthetic data only, or aggregate counts).

## Payload hygiene checklist (run before each ACTIVE_TESTING iteration)

- [ ] Target in scope (re-checked at request time).
- [ ] Payload contains the `PTSKILLTEST` marker.
- [ ] Payload contains no real secrets/PII.
- [ ] Payload is non-destructive (no DROP, DELETE, write unless L4-approved).
- [ ] Request routed through rate limiter.
- [ ] LLM (if used) only suggests payloads; does not auto-execute L4.

---

## NEW — 组件未授权访问检测 (`component_exposure`) — DETECTION (L1)

> 来源：152 份真实 SRC 报告统计。Actuator 信息泄露为企业 SRC ⭐⭐⭐⭐ 高频项。

Goal: detect exposed admin/monitor/API-doc endpoints of common components without
reading sensitive data. Non-destructive GET-only probes.

### Spring Boot Actuator
- Probe paths: `/actuator`, `/actuator/env`, `/actuator/heapdump`,
  `/actuator/mappings`, `/actuator/configprops`, `/actuator/beans`,
  `/actuator/jolokia`
- Detection signal: 200 response with JSON containing `"propertySources"` (env),
  or binary octet-stream (heapdump), or `"contexts"` (mappings).
- `/actuator/env` may expose DB credentials, API keys — flag existence only;
  do NOT parse or exfiltrate values. Mark `safe_poc = true` (read-only GET).
- `/actuator/heapdump` — flag 200 + large Content-Length; do NOT download the
  full dump. A HEAD request suffices for detection.

### Druid Monitor
- Probe paths: `/druid/index.html`, `/druid/login.html`, `/druid/sql.html`,
  `/druid/datasource.html`, `/druid/wall.html`
- Detection signal: 200 with HTML containing `Druid Stat Index` or
  `Druid SQL Monitor` — indicates unauth monitor access.
- Default credentials (`admin/admin` for `/druid/login.html`) → delegate to
  `weak_credential` rule below.

### Swagger / OpenAPI
- Probe paths: `/swagger-ui.html`, `/swagger-ui/index.html`, `/v2/api-docs`,
  `/v3/api-docs`, `/swagger-resources`, `/swagger.json`
- Detection signal: 200 with JSON containing `"swagger"` or `"openapi"` key,
  or HTML containing `Swagger UI`.
- Flag as `component_exposure`: reveals full API surface for further attack
  enumeration. Do NOT auto-fuzz discovered endpoints without explicit approval.

### UEditor (中国高校/企业高频)
- Probe paths: `/controller.ashx?action=catchimage`,
  `/ueditor/controller.ashx?action=catchimage`
- Detection signal: endpoint responds to `action=catchimage` with a JSON
  structure containing `"url"` — indicates SSRF-via-upload capability.
- Do NOT actually fetch a remote shell. Point `source[]` at the authorized
  sink `https://oob.authorized.test/PTSKILLTEST-ueditor` and detect the
  callback. This overlaps with `file_upload` detection (see below).

## NEW — 弱口令/默认凭据检测 (`weak_credential`) — DETECTION (L3)

> 来源：Edu 高校 SRC ⭐⭐⭐⭐⭐（最高频，30+ 案例）；企业 SRC ⭐⭐⭐。
> `admin/123456` 是高校系统最常见的弱口令。

Goal: confirm a login endpoint accepts a default/weak credential. Bounded,
human-approved, staging/dev ONLY.

- **Bounded credential set** (max 10 attempts per endpoint, stop on first success):

| 场景 | 凭据组合 |
|------|---------|
| 通用 admin | `admin/123456`, `admin/admin`, `admin/admin123`, `admin/password`, `admin/111111`, `admin/12345678` |
| 通用 root | `root/root`, `root/123456`, `root/password` |
| 测试账号 | `test/test`, `guest/guest`, `user/user` |
| Edu 学号 | `学号/学号后6位`, `学号/学号`, `学号/123456` |
| Edu 工号 | `工号/工号a`, `工号/工号`, `工号/123456` |
| 数据库/中间件 | `admin/admin` (Druid), `admin/admin` (Tomcat manager) |

- Detection signal: login response indicates success — 302 redirect to
  dashboard, 200 with `{code:0, success:true, token:...}`, or a session
  cookie issued. Record the credential that worked.
- **Safety**: stop immediately on first success. Do NOT enumerate further.
  Do NOT access any data beyond the login confirmation. Mark `safe_poc = true`
  only if no data was read post-login.
- Requires: `requires_human_approval = true` (brute-force is L4-adjacent;
  even bounded sets need approval).

## NEW — 验证码绕过检测 (`captcha_bypass`) — DETECTION (L2)

> 来源：Edu 高校 SRC ⭐（同济大学万能验证码、上海交大 4 位爆破、广东东软返回包篡改）。

Goal: confirm a captcha-protected endpoint accepts requests without valid
captcha verification.

| 绕过模式 | 探测方法 | 检测信号 |
|---------|---------|---------|
| 空值绕过 | 提交空 captcha 字段 `captcha=` | 请求成功（登录/状态变更生效） |
| 删除参数 | 完全移除 captcha 参数 | 请求成功 |
| 固定万能码 | `captcha=123456`（同济案例） | 请求成功 |
| 验证码复用 | 同一 captcha 连续提交 3 次 | 第 2/3 次仍成功 |
| 4 位爆破可行性 | 检查 4 位数字 captcha 是否有锁定/频率限制 | 无锁定 + 1001 次内可穷举 |
| 返回包篡改 | 拦截响应，翻转 `success:false→true` / `error_code:1→0` | 篡改后请求被接受 |

- Detection signal: any bypass mode results in the protected action succeeding.
- `safe_poc = true` only if using synthetic test accounts and no real
  state-change occurred (use a test login that logs out immediately).

## NEW — 文件上传漏洞检测 (`file_upload`) — DETECTION (L3)

> 来源：Edu 高校 SRC ⭐⭐⭐；企业 SRC ⭐⭐⭐。
> UEditor 是高校 GetShell 主力组件。

Goal: confirm an upload endpoint accepts and serves a file that should be
rejected, WITHOUT uploading a real webshell.

- **Step 1 — benign marker upload**:
  - Upload `PTSKILLTEST-upload-9a3f.txt` (plain text, harmless).
  - Detection signal: file accessible at a predictable URL
    (`/uploads/PTSKILLTEST-upload-9a3f.txt`) → confirms storage works.

- **Step 2 — extension bypass detection** (test each, flag if accepted):
  - `.jpg.php` (double extension, Apache)
  - `.phtml`, `.phar`, `.php5` (PHP alt extensions)
  - `.asp;.jpg` (IIS semicolon bypass)
  - `.html`, `.svg` (XSS carrier — SVG with `<script>`)
  - `file.jpg.html` (同济大学双后缀案例)
  - Detection signal: uploaded file served with executable MIME OR
    `.html/.svg` accessible (stored XSS vector).

- **Step 3 — Content-Type manipulation**:
  - Send `Content-Type: image/jpeg` header but filename `test.php`.
  - Detection signal: server stores as `.php` (backend trusts header over
    extension).

- **Step 4 — UEditor catchimage (SSRF via upload)**:
  - POST `source[]=https://oob.authorized.test/PTSKILLTEST-ueditor` to
    `/controller.ashx?action=catchimage`.
  - Detection signal: OOB callback received → SSRF confirmed.

- **Step 5 — Content-Disposition bypass**（南开大学安全狗案例，DETECTION ONLY）:
  - Send request with doubled `Content-Disposition` header. Do NOT upload
    a real shell — just detect if the WAF accepts the malformed header
    (response 200 + file stored).
  - Detection signal: 200 with file stored despite malformed header.

- `safe_poc = true` only if NO real webshell was uploaded and NO remote
  code executed. All uploaded test files MUST be cleaned up post-detection
  (L4, requires approval).

## NEW — 逻辑漏洞检测 (`logic_flaw`) — DETECTION (L3)

> 来源：Edu 高校 SRC ⭐⭐⭐⭐（广东东软返回包篡改、上海交大 role 翻转、清华短信轰炸、广西大学附属中学步骤跳过）。
> 企业 SRC ⭐⭐⭐⭐。

Goal: detect business-logic flaws via non-destructive parameter/response
tampering. ALL tests use synthetic test objects created for the run.

### 返回包篡改绕过 (Response Tampering)
- Intercept login/verification response, flip fields:
  - `error_code: 1 → 0`（广东东软案例）
  - `success: false → true`
  - `role: user → admin`（上海交大案例）
  - `Message: 0 → 1`
- Detection signal: tampered response accepted — subsequent request to a
  protected endpoint succeeds.

### 参数篡改 (Parameter Tampering — 价格/数量)
- Modify `price`, `amount`, `count` to negative or zero values.
- Modify `quantity` to very large number.
- Detection signal: order/transaction accepted with invalid value
  (e.g., `price=-100` increases balance, `amount=0` free purchase).

### 步骤跳过 (Step Skip)
- Directly access step3 URL without completing step1/step2.
- Detection signal: step3 action succeeds without prerequisites
  （广西大学附属中学案例：特定 URL 免账号进后台）.

### 短信/验证码轰炸 (SMS/OTP Bombing)
- Probe `/sendPasswordCode`, `/sendSms`, `/getVerifyCode` endpoints.
- Send 6 requests within 60 seconds to the same test phone number.
- Detection signal: all 6 requests return success (no rate limit)
  （清华大学案例）。
- `safe_poc = true` only if using a test phone number owned by the tester.

### 重放攻击 (Replay)
- Capture a state-changing request, replay it N times (e.g., 3x).
- Detection signal: action applied N times (idempotency missing) —
  e.g., balance incremented 3x, 3x withdrawal.

- `safe_poc = true` only if all tests used synthetic objects and any
  state changes were reversed/cleaned up.
