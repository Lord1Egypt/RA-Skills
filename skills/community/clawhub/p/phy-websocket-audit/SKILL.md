---
name: WebSocket Audit
description: WebSocket security auditor. Scans source code for 10 WebSocket-specific vulnerabilities — plaintext ws:// connections, missing Origin header validation (CSWSH — Cross-Site WebSocket Hijacking), no authentication before accept, missing message size limits, no rate limiting, unauthenticated client broadcasts, reflected message relay (XSS-over-WS), error stack trace leaks, insecure subprotocol negotiation, and missing heartbeat/timeout configuration. Supports Node.js (ws, Socket.IO), Python (websockets, FastAPI, Django Channels), Go (gorilla/websocket), Java (Spring WebSocket), Ruby (ActionCable). Zero external dependencies. Zero competitors on ClawHub.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - websocket
  - security
  - owasp
  - real-time
  - backend
  - developer-tools
  - static-analysis
---

# phy-websocket-audit

**WebSocket security auditor** — catches the 10 most dangerous WebSocket vulnerabilities that standard OWASP scanners miss because WebSocket connections upgrade from HTTP and bypass most traditional security controls.

WebSocket attacks are under-appreciated: there is no SameSite cookie protection, no CORS pre-flight (only an Origin header that developers frequently forget to validate), and no automatic authentication check on upgrade. A single missing `if req.headers["Origin"] not in ALLOWED_ORIGINS` line is enough for any website to hijack your WebSocket connections.

## What It Detects

| ID | Vulnerability | Severity | CWE |
|----|---------------|----------|-----|
| WS001 | Plaintext `ws://` instead of `wss://` | HIGH | CWE-319 |
| WS002 | Missing Origin header validation (CSWSH) | CRITICAL | CWE-346 |
| WS003 | No authentication before WebSocket accept | CRITICAL | CWE-306 |
| WS004 | No message size limit (DoS via large payload) | HIGH | CWE-400 |
| WS005 | No per-connection message rate limit | MEDIUM | CWE-770 |
| WS006 | Unauthenticated broadcast to all connected clients | HIGH | CWE-862 |
| WS007 | Message relay without sanitization (reflected XSS-over-WS) | HIGH | CWE-79 |
| WS008 | Error details / stack trace sent over WebSocket | MEDIUM | CWE-209 |
| WS009 | Insecure subprotocol negotiation (wildcard or no validation) | MEDIUM | CWE-295 |
| WS010 | No heartbeat / connection timeout (zombie connections) | LOW | CWE-400 |

## Trigger Phrases

```
/phy-websocket-audit
Audit my WebSocket code for security vulnerabilities
```

```
/phy-websocket-audit
Check src/realtime/ for WebSocket security issues
```

```
/phy-websocket-audit
Is my Socket.IO server vulnerable to cross-site WebSocket hijacking?
```

---

## Implementation

When invoked, run the following Python analysis. Accept `--root` (default `.`) and optional `--ci` flag.

```python
#!/usr/bin/env python3
"""
phy-websocket-audit — WebSocket security vulnerability scanner
Detects WS001–WS010 in Node.js, Python, Go, Java, Ruby
Zero external dependencies.
"""
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────

SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', 'vendor', '.venv', 'venv',
    'dist', 'build', '.next', 'coverage', 'test', 'tests', 'spec',
    '__tests__', 'e2e', 'fixtures', 'mocks',
}

SEVERITY_ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
SEVERITY_EMOJI = {'CRITICAL': '💀', 'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🔵'}

CI_MODE = '--ci' in sys.argv
MIN_SEVERITY = next(
    (sys.argv[sys.argv.index('--min-severity') + 1]
     for _ in ['x'] if '--min-severity' in sys.argv),
    'LOW'
)

SOURCE_EXTENSIONS = {'.js', '.ts', '.mjs', '.cjs', '.jsx', '.tsx',
                     '.py', '.go', '.java', '.kt', '.rb'}


# ─────────────────────────────────────────────────────
# Data model
# ─────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    file: str
    line: int
    severity: str
    description: str
    matched_text: str
    fix: str
    cwe: str
    framework: str = ''


# ─────────────────────────────────────────────────────
# File walker
# ─────────────────────────────────────────────────────

def walk_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            try:
                content = fpath.read_text(errors='ignore')
                # Only process files that contain WebSocket-related code
                if not _is_ws_file(content):
                    continue
                yield fpath, content
            except Exception:
                continue


def _is_ws_file(content: str) -> bool:
    """Quick filter: only scan files that actually use WebSockets."""
    markers = [
        'WebSocket', 'websocket', 'socket.io', 'ws.on', 'wss.on',
        'ws://', 'wss://', 'gorilla/websocket', 'nhooyr.io/websocket',
        'fastapi.websocket', 'ActionCable', 'consumer_registered',
        'WebsocketConsumer', 'AsyncWebsocketConsumer', 'channel_layer',
        'spring.websocket', '@ServerEndpoint', 'TextWebSocketHandler',
        'require("ws")', "require('ws')", 'from websockets',
        'import WebSocket',
    ]
    return any(m in content for m in markers)


def _detect_framework(content: str, ext: str) -> str:
    if ext in ('.js', '.ts', '.mjs', '.cjs', '.jsx', '.tsx'):
        if 'socket.io' in content or 'require("socket.io")' in content:
            return 'socket.io'
        if 'require("ws")' in content or "require('ws')" in content or 'new WebSocketServer' in content:
            return 'ws'
        return 'node-ws'
    if ext == '.py':
        if 'websockets' in content:
            return 'websockets'
        if 'fastapi' in content.lower() or 'WebSocket' in content:
            return 'fastapi'
        if 'channels' in content or 'WebsocketConsumer' in content:
            return 'django-channels'
        return 'python-ws'
    if ext == '.go':
        if 'gorilla/websocket' in content:
            return 'gorilla/websocket'
        return 'go-ws'
    if ext in ('.java', '.kt'):
        return 'spring-websocket'
    if ext == '.rb':
        return 'actioncable'
    return 'unknown'


# ─────────────────────────────────────────────────────
# Helper: proximity guard check
# ─────────────────────────────────────────────────────

def has_guard_nearby(lines: list[str], line_idx: int,
                     guard_patterns: list[re.Pattern],
                     window: int = 30) -> bool:
    start = max(0, line_idx - window)
    end = min(len(lines), line_idx + window)
    window_text = '\n'.join(lines[start:end])
    return any(p.search(window_text) for p in guard_patterns)


# ─────────────────────────────────────────────────────
# WS001 — Plaintext ws:// URL
# ─────────────────────────────────────────────────────

WS_PLAINTEXT_RE = re.compile(r"""['"](ws://[^'"]+)['"]""")
WS_PLAINTEXT_ALLOW = re.compile(
    r'localhost|127\.0\.0\.1|::1|0\.0\.0\.0|test|dev|local|example\.com',
    re.IGNORECASE
)


def check_ws001_plaintext(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        m = WS_PLAINTEXT_RE.search(line)
        if not m:
            continue
        url = m.group(1)
        if WS_PLAINTEXT_ALLOW.search(url):
            continue  # localhost/dev is OK
        findings.append(Finding(
            check_id='WS001',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=f'Plaintext WebSocket URL: `{url}`. All messages sent in cleartext.',
            matched_text=line.strip()[:120],
            fix='Change ws:// to wss:// and ensure your server has a valid TLS certificate.',
            cwe='CWE-319',
            framework=framework,
        ))
    return findings


# ─────────────────────────────────────────────────────
# WS002 — Missing Origin header validation (CSWSH)
# ─────────────────────────────────────────────────────

# Patterns that indicate a WebSocket upgrade handler
WS_UPGRADE_RE = re.compile(
    r"""on\s*\(\s*['"](?:connection|upgrade)['"]|
        async\s+websocket\s*\(|
        @WebSocket|
        wss?\.on\s*\(\s*['"]connection['"]|
        func\s+\w*[Hh]andler|func\s+\w*[Ww]ebsocket|
        upgrader\.Upgrade|
        def\s+(?:connect|websocket_connect|ws_connect)|
        WebSocket\s+ws\s*=\s*await|
        socket\s*=\s*await\s+websocket\.accept""",
    re.VERBOSE | re.IGNORECASE
)

# Patterns that indicate Origin is being checked
ORIGIN_CHECK_RE = re.compile(
    r"""[Oo]rigin|ORIGIN|
        req\.headers\[.origin|
        request\.headers\.get\s*\(\s*['"]origin['"]|
        r\.Header\.Get\s*\(\s*"Origin"|
        checkOrigin|check_origin|
        ALLOWED_ORIGINS|allowed_origins|
        upgrader\.CheckOrigin""",
    re.VERBOSE
)


def check_ws002_origin(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not WS_UPGRADE_RE.search(line):
            continue
        # Check within ±40 lines for Origin validation
        if has_guard_nearby(lines, i, [ORIGIN_CHECK_RE], window=40):
            continue
        findings.append(Finding(
            check_id='WS002',
            file=str(fpath),
            line=i + 1,
            severity='CRITICAL',
            description=(
                'WebSocket upgrade handler without Origin header validation. '
                'Any website can open a WebSocket connection to your server using the visiting user\'s cookies '
                '(Cross-Site WebSocket Hijacking — CSWSH).'
            ),
            matched_text=line.strip()[:120],
            fix=_ws002_fix(framework),
            cwe='CWE-346',
            framework=framework,
        ))
    return findings


def _ws002_fix(framework: str) -> str:
    fixes = {
        'ws': (
            'const wss = new WebSocketServer({\n'
            '  verifyClient: ({ origin }, cb) => {\n'
            '    const allowed = ["https://yourdomain.com"];\n'
            '    cb(allowed.includes(origin), 403, "Forbidden");\n'
            '  }\n'
            '});'
        ),
        'socket.io': (
            'const io = new Server(server, {\n'
            '  cors: { origin: ["https://yourdomain.com"], credentials: true }\n'
            '});'
        ),
        'fastapi': (
            '@app.websocket("/ws")\n'
            'async def websocket_endpoint(websocket: WebSocket):\n'
            '    origin = websocket.headers.get("origin")\n'
            '    if origin not in ALLOWED_ORIGINS:\n'
            '        await websocket.close(code=1008)\n'
            '        return\n'
            '    await websocket.accept()'
        ),
        'gorilla/websocket': (
            'upgrader := websocket.Upgrader{\n'
            '    CheckOrigin: func(r *http.Request) bool {\n'
            '        origin := r.Header.Get("Origin")\n'
            '        return origin == "https://yourdomain.com"\n'
            '    },\n'
            '}'
        ),
        'django-channels': (
            'class MyConsumer(WebsocketConsumer):\n'
            '    def connect(self):\n'
            '        origin = self.scope["headers"].get(b"origin", b"").decode()\n'
            '        if origin not in settings.ALLOWED_WS_ORIGINS:\n'
            '            self.close()\n'
            '            return\n'
            '        self.accept()'
        ),
    }
    return fixes.get(framework, (
        'Validate the Origin header before accepting the WebSocket connection. '
        'Reject connections from origins not in your allowlist. '
        'Never use a wildcard allowlist for authenticated endpoints.'
    ))


# ─────────────────────────────────────────────────────
# WS003 — No authentication before accept
# ─────────────────────────────────────────────────────

# Patterns indicating auth check (token, session, user)
AUTH_CHECK_RE = re.compile(
    r"""[Jj][Ww][Tt]|bearer|Bearer|token|Token|
        session|Session|cookie|Cookie|
        authenticate|authorize|auth|Auth|
        verify\w*[Tt]oken|decode\w*[Tt]oken|
        getCurrentUser|get_current_user|
        req\.user|request\.user|c\.Locals\("user"|
        scope\[.user|scope\[.session""",
    re.VERBOSE
)

WS_ACCEPT_RE = re.compile(
    r"""websocket\.accept\s*\(\)|
        ws\.accept\s*\(\)|
        await\s+websocket\.accept|
        self\.accept\s*\(\)|
        conn,\s*_\s*=\s*upgrader\.Upgrade""",
    re.VERBOSE | re.IGNORECASE
)


def check_ws003_auth(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not WS_ACCEPT_RE.search(line):
            continue
        if has_guard_nearby(lines, i, [AUTH_CHECK_RE], window=30):
            continue
        findings.append(Finding(
            check_id='WS003',
            file=str(fpath),
            line=i + 1,
            severity='CRITICAL',
            description=(
                'WebSocket accepted without authentication check. '
                'Any unauthenticated client can connect and receive data.'
            ),
            matched_text=line.strip()[:120],
            fix=_ws003_fix(framework),
            cwe='CWE-306',
            framework=framework,
        ))
    return findings


def _ws003_fix(framework: str) -> str:
    fixes = {
        'fastapi': (
            'async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):\n'
            '    user = await verify_token(token)  # validate JWT/session\n'
            '    if not user:\n'
            '        await websocket.close(code=1008, reason="Unauthorized")\n'
            '        return\n'
            '    await websocket.accept()'
        ),
        'ws': (
            '// Check auth in the HTTP upgrade request:\n'
            'server.on("upgrade", (req, socket, head) => {\n'
            '    const token = new URLSearchParams(req.url.split("?")[1]).get("token");\n'
            '    if (!verifyToken(token)) { socket.destroy(); return; }\n'
            '    wss.handleUpgrade(req, socket, head, ws => wss.emit("connection", ws, req));\n'
            '});'
        ),
        'gorilla/websocket': (
            'func wsHandler(w http.ResponseWriter, r *http.Request) {\n'
            '    token := r.URL.Query().Get("token")\n'
            '    if _, err := validateJWT(token); err != nil {\n'
            '        http.Error(w, "Unauthorized", http.StatusUnauthorized)\n'
            '        return\n'
            '    }\n'
            '    conn, _ := upgrader.Upgrade(w, r, nil)\n'
            '    // ...\n'
            '}'
        ),
    }
    return fixes.get(framework, (
        'Validate authentication (JWT, session cookie, API key) in the HTTP upgrade request '
        'BEFORE calling accept(). Query parameters or Authorization headers are common patterns. '
        'Close the connection with code 1008 (Policy Violation) for unauthenticated requests.'
    ))


# ─────────────────────────────────────────────────────
# WS004 — No message size limit
# ─────────────────────────────────────────────────────

WS_SERVER_INIT_RE = re.compile(
    r"""new\s+WebSocketServer\s*\(|
        new\s+Server\s*\(.*socket|
        websockets\.serve\s*\(|
        websockets\.connect\s*\(|
        upgrader\s*:?=\s*websocket\.Upgrader|
        @ServerEndpoint|TextWebSocketHandler""",
    re.VERBOSE | re.IGNORECASE
)

SIZE_LIMIT_RE = re.compile(
    r"""maxPayload|max_size|max_message_size|
        ReadLimit|ReadBufferSize|WriteBufferSize|
        maxMessageSize|MAX_MESSAGE|
        setMaxTextMessageBufferSize|setMaxBinaryMessageBufferSize""",
    re.IGNORECASE | re.VERBOSE
)


def check_ws004_size_limit(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not WS_SERVER_INIT_RE.search(line):
            continue
        if has_guard_nearby(lines, i, [SIZE_LIMIT_RE], window=20):
            continue
        findings.append(Finding(
            check_id='WS004',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=(
                'WebSocket server initialized without message size limit. '
                'A single client can send a multi-GB message to exhaust server memory.'
            ),
            matched_text=line.strip()[:120],
            fix=_ws004_fix(framework),
            cwe='CWE-400',
            framework=framework,
        ))
    return findings


def _ws004_fix(framework: str) -> str:
    fixes = {
        'ws': 'new WebSocketServer({ maxPayload: 1024 * 1024 })  // 1MB limit',
        'fastapi': (
            '# In websockets library:\n'
            'async with websockets.serve(handler, host, port, max_size=1_000_000):  # 1MB'
        ),
        'gorilla/websocket': (
            'upgrader := websocket.Upgrader{}\n'
            '// After upgrade:\n'
            'conn.SetReadLimit(1 * 1024 * 1024)  // 1MB'
        ),
        'spring-websocket': (
            '@Bean\n'
            'public WebSocketHandler wsHandler() {\n'
            '    // In AbstractWebSocketHandler, override handleMessage\n'
            '    // and check message.getPayloadLength() < MAX_SIZE\n'
            '}'
        ),
    }
    return fixes.get(framework, 'Set a maximum message size (e.g., 1MB) on the WebSocket server configuration.')


# ─────────────────────────────────────────────────────
# WS005 — No per-connection message rate limit
# ─────────────────────────────────────────────────────

WS_MESSAGE_HANDLER_RE = re.compile(
    r"""\.on\s*\(\s*['"]message['"]|
        async\s+def\s+receive\s*\(|
        func\s+\w*[Mm]essage\s*\(|
        def\s+receive\s*\(self|
        receive_text\s*\(\)|receive_json\s*\(\)|receive_bytes""",
    re.VERBOSE | re.IGNORECASE
)

RATE_LIMIT_RE = re.compile(
    r"""rate.?limit|rateLimit|RateLimit|
        throttl|Throttl|
        message.?count|messageCount|msg_count|
        token.?bucket|leaky.?bucket|
        setInterval.*count|clearTimeout""",
    re.VERBOSE | re.IGNORECASE
)


def check_ws005_rate_limit(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not WS_MESSAGE_HANDLER_RE.search(line):
            continue
        if has_guard_nearby(lines, i, [RATE_LIMIT_RE], window=30):
            continue
        findings.append(Finding(
            check_id='WS005',
            file=str(fpath),
            line=i + 1,
            severity='MEDIUM',
            description=(
                'WebSocket message handler has no rate limiting. '
                'A single client can flood the server with thousands of messages per second.'
            ),
            matched_text=line.strip()[:120],
            fix=(
                '// Track message count per connection (Node.js example):\n'
                'const clients = new Map(); // ws -> { count, resetAt }\n'
                'ws.on("message", (data) => {\n'
                '    const state = clients.get(ws) || { count: 0, resetAt: Date.now() + 1000 };\n'
                '    if (Date.now() > state.resetAt) { state.count = 0; state.resetAt = Date.now() + 1000; }\n'
                '    if (++state.count > 100) { ws.close(1008, "Rate limit exceeded"); return; }\n'
                '    clients.set(ws, state);\n'
                '    // process message\n'
                '});'
            ),
            cwe='CWE-770',
            framework=framework,
        ))
    return findings


# ─────────────────────────────────────────────────────
# WS006 — Unauthenticated broadcast to all clients
# ─────────────────────────────────────────────────────

BROADCAST_RE = re.compile(
    r"""wss\.clients\.forEach|
        io\.emit\s*\(|
        io\.to\s*\(.*\)\.emit|
        self\.channel_layer\.group_send|
        group_send\s*\(|
        ActionCable\.server\.broadcast""",
    re.VERBOSE | re.IGNORECASE
)

BROADCAST_AUTH_RE = re.compile(
    r"""user|User|admin|Admin|role|Role|
        permission|Permission|authorize|authenticated|
        isAuthenticated|is_authenticated|
        req\.user|request\.user|scope\[.user""",
    re.IGNORECASE
)


def check_ws006_broadcast(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not BROADCAST_RE.search(line):
            continue
        if has_guard_nearby(lines, i, [BROADCAST_AUTH_RE], window=15):
            continue
        findings.append(Finding(
            check_id='WS006',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=(
                'Broadcast to all WebSocket clients without permission check. '
                'Private data may be sent to unauthenticated or unauthorized connections.'
            ),
            matched_text=line.strip()[:120],
            fix=(
                '// Filter clients before broadcasting:\n'
                'wss.clients.forEach(client => {\n'
                '    if (client.readyState === WebSocket.OPEN && client.userId) {\n'
                '        client.send(data); // only send to authenticated clients\n'
                '    }\n'
                '});'
            ),
            cwe='CWE-862',
            framework=framework,
        ))
    return findings


# ─────────────────────────────────────────────────────
# WS007 — Message relay without sanitization (XSS-over-WS)
# ─────────────────────────────────────────────────────

WS_RELAY_RE = re.compile(
    r"""\.on\s*\(\s*['"]message['"].*(?:ws|client|socket)\.send|
        receive.*\n.*send|
        msg\s*=.*\n.*broadcast""",
    re.DOTALL | re.IGNORECASE
)

WS_SEND_FROM_RECV_RE = re.compile(
    r"""ws\.send\s*\(.*(?:data|message|msg|payload)\s*\)|
        client\.send\s*\(.*(?:data|message|msg)\s*\)|
        socket\.emit\s*\(.*(?:data|message|msg)\s*\)|
        websocket\.send_text\s*\(.*(?:data|message|msg)""",
    re.IGNORECASE
)

SANITIZE_RE = re.compile(
    r"""sanitize|escape|htmlspecialchars|encodeHTML|DOMPurify|
        bleach\.clean|html\.escape|validator\.escape|
        strip_tags|purify|xss""",
    re.IGNORECASE
)


def check_ws007_relay(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')

    in_message_handler = False
    handler_start = 0
    handler_indent = 0

    for i, line in enumerate(lines):
        # Detect entering a message handler
        if WS_MESSAGE_HANDLER_RE.search(line):
            in_message_handler = True
            handler_start = i
            handler_indent = len(line) - len(line.lstrip())

        if not in_message_handler:
            continue

        # Check if we're still in the same handler scope (rough indentation check)
        if i > handler_start + 1:
            stripped = line.strip()
            if stripped and not stripped.startswith(('//','#')):
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= handler_indent and i > handler_start + 2:
                    in_message_handler = False
                    continue

        # Look for send/relay of received data
        if WS_SEND_FROM_RECV_RE.search(line):
            # Check if there's any sanitization nearby
            window_start = max(0, i - 10)
            window_text = '\n'.join(lines[window_start:i + 5])
            if not SANITIZE_RE.search(window_text):
                findings.append(Finding(
                    check_id='WS007',
                    file=str(fpath),
                    line=i + 1,
                    severity='HIGH',
                    description=(
                        'WebSocket message relayed to client(s) without sanitization. '
                        'Malicious clients can inject XSS payloads that execute in other clients\' browsers '
                        'when the message is rendered as HTML.'
                    ),
                    matched_text=line.strip()[:120],
                    fix=(
                        '// Always sanitize before relaying messages:\n'
                        'const clean = DOMPurify.sanitize(data.toString());\n'
                        'wss.clients.forEach(c => c.readyState === 1 && c.send(clean));\n'
                        '// Or use a JSON envelope that clients render as text, not HTML:\n'
                        'ws.send(JSON.stringify({ type: "message", text: data.toString() }));'
                    ),
                    cwe='CWE-79',
                    framework=framework,
                ))

    return findings


# ─────────────────────────────────────────────────────
# WS008 — Error details leaked over WebSocket
# ─────────────────────────────────────────────────────

WS_ERROR_LEAK_RE = re.compile(
    r"""(?:ws|socket|websocket|client)\.send\s*\(.*
        (?:err\.message|err\.stack|error\.message|error\.stack|
           str\(e\)|str\(err\)|traceback|exception\.message|
           e\.getMessage\(\)|e\.getStackTrace)""",
    re.VERBOSE | re.IGNORECASE
)


def check_ws008_error_leak(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if WS_ERROR_LEAK_RE.search(line):
            findings.append(Finding(
                check_id='WS008',
                file=str(fpath),
                line=i + 1,
                severity='MEDIUM',
                description=(
                    'Error details or stack trace sent over WebSocket to the client. '
                    'Exposes internal structure, file paths, and library versions to attackers.'
                ),
                matched_text=line.strip()[:120],
                fix=(
                    '// Send generic error to client, log details server-side:\n'
                    'ws.send(JSON.stringify({ error: "Internal server error", code: "E500" }));\n'
                    'console.error("WS error:", err);  // server-side only'
                ),
                cwe='CWE-209',
                framework=framework,
            ))
    return findings


# ─────────────────────────────────────────────────────
# WS009 — Insecure subprotocol negotiation
# ─────────────────────────────────────────────────────

# Accepting all subprotocols (wildcard accept)
WS_SUBPROTOCOL_ACCEPT_RE = re.compile(
    r"""protocols\s*[=:]\s*\[\s*\*|
        acceptedSubprotocol\s*=\s*req\.headers\[|
        Sec-WebSocket-Protocol.*req\.headers|
        subprotocols\s*=\s*client\.|
        header.*Sec-WebSocket-Protocol.*=.*request\.header""",
    re.IGNORECASE | re.VERBOSE
)

WS_SUBPROTOCOL_VALIDATE_RE = re.compile(
    r"""SUPPORTED_PROTOCOLS|supported_protocols|allowedProtocols|
        includes\s*\(\s*(?:protocol|subprotocol)|
        in\s+PROTOCOLS|protocol\s*==|protocol\s*in\s*\[""",
    re.IGNORECASE
)


def check_ws009_subprotocol(fpath: Path, content: str, framework: str) -> list[Finding]:
    findings = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if WS_SUBPROTOCOL_ACCEPT_RE.search(line):
            if not has_guard_nearby(lines, i, [WS_SUBPROTOCOL_VALIDATE_RE], window=10):
                findings.append(Finding(
                    check_id='WS009',
                    file=str(fpath),
                    line=i + 1,
                    severity='MEDIUM',
                    description=(
                        'WebSocket subprotocol echoed back without validation. '
                        'Clients can negotiate arbitrary subprotocols, bypassing protocol-level security constraints.'
                    ),
                    matched_text=line.strip()[:120],
                    fix=(
                        'const SUPPORTED_PROTOCOLS = ["v1.chat", "v2.chat"];\n'
                        'const requested = req.headers["sec-websocket-protocol"]?.split(",").map(s => s.trim());\n'
                        'const protocol = requested?.find(p => SUPPORTED_PROTOCOLS.includes(p));\n'
                        'if (!protocol) { socket.destroy(); return; }\n'
                        '// Pass protocol to handleUpgrade'
                    ),
                    cwe='CWE-295',
                    framework=framework,
                ))
    return findings


# ─────────────────────────────────────────────────────
# WS010 — No heartbeat / connection timeout
# ─────────────────────────────────────────────────────

HEARTBEAT_RE = re.compile(
    r"""ping|pong|heartbeat|keepalive|keep.alive|
        setInterval.*ping|setTimeout.*close|
        ping_interval|ping_timeout|
        isAlive|is_alive|
        conn\.SetPingHandler|conn\.SetPongHandler|
        ws\.ping\s*\(|wss\.ping""",
    re.IGNORECASE | re.VERBOSE
)


def check_ws010_heartbeat(fpath: Path, content: str, framework: str) -> list[Finding]:
    """Only flag if there's clearly a persistent WS server without heartbeat."""
    findings = []
    lines = content.split('\n')

    # Look for server initialization without heartbeat
    for i, line in enumerate(lines):
        if WS_SERVER_INIT_RE.search(line):
            # Check entire file for heartbeat
            if not HEARTBEAT_RE.search(content):
                findings.append(Finding(
                    check_id='WS010',
                    file=str(fpath),
                    line=i + 1,
                    severity='LOW',
                    description=(
                        'WebSocket server has no ping/pong heartbeat mechanism. '
                        'Dead connections accumulate as zombie sockets, leaking memory and file descriptors.'
                    ),
                    matched_text=line.strip()[:120],
                    fix=(
                        '// Node.js ws heartbeat pattern:\n'
                        'function heartbeat() { this.isAlive = true; }\n'
                        'wss.on("connection", ws => {\n'
                        '    ws.isAlive = true;\n'
                        '    ws.on("pong", heartbeat);\n'
                        '});\n'
                        'setInterval(() => {\n'
                        '    wss.clients.forEach(ws => {\n'
                        '        if (!ws.isAlive) return ws.terminate();\n'
                        '        ws.isAlive = false;\n'
                        '        ws.ping();\n'
                        '    });\n'
                        '}, 30000);'
                    ),
                    cwe='CWE-400',
                    framework=framework,
                ))
            break  # One finding per file for WS010

    return findings


# ─────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────

CHECKS = [
    check_ws001_plaintext,
    check_ws002_origin,
    check_ws003_auth,
    check_ws004_size_limit,
    check_ws005_rate_limit,
    check_ws006_broadcast,
    check_ws007_relay,
    check_ws008_error_leak,
    check_ws009_subprotocol,
    check_ws010_heartbeat,
]


def deduplicate(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple] = set()
    result = []
    for f in findings:
        key = (f.check_id, f.file, f.line)
        if key not in seen:
            seen.add(key)
            result.append(f)
    return result


def run_audit(root: Path) -> int:
    print(f"\n🔍  phy-websocket-audit — scanning {root}\n{'─'*60}")

    all_findings: list[Finding] = []

    severity_threshold = SEVERITY_ORDER.get(MIN_SEVERITY, 3)

    for fpath, content in walk_files(root):
        framework = _detect_framework(content, fpath.suffix.lower())
        for check in CHECKS:
            try:
                results = check(fpath, content, framework)
                all_findings.extend(results)
            except Exception:
                pass

    all_findings = deduplicate(all_findings)
    all_findings = [f for f in all_findings
                    if SEVERITY_ORDER.get(f.severity, 3) <= severity_threshold]
    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 3), f.file, f.line))

    if not all_findings:
        print("✅  No WebSocket security issues found.")
        return 0

    critical = sum(1 for f in all_findings if f.severity == 'CRITICAL')
    high = sum(1 for f in all_findings if f.severity == 'HIGH')
    med = sum(1 for f in all_findings if f.severity == 'MEDIUM')
    low = sum(1 for f in all_findings if f.severity == 'LOW')

    print(f"Found {len(all_findings)} issue(s): "
          f"💀 CRITICAL={critical}  🔴 HIGH={high}  🟡 MEDIUM={med}  🔵 LOW={low}\n")

    current_severity = None
    for f in all_findings:
        if f.severity != current_severity:
            current_severity = f.severity
            emoji = SEVERITY_EMOJI.get(f.severity, '⚪')
            print(f"\n{emoji} {f.severity} — {f.check_id}\n{'─'*50}")

        print(f"\n[{f.check_id}] {f.file}:{f.line}  ({f.framework})")
        print(f"  {f.cwe}: {f.description}")
        print(f"  Matched: {f.matched_text}")
        print(f"  Fix:")
        for fix_line in f.fix.split('\n'):
            print(f"    {fix_line}")

    print(f"\n{'═'*60}")
    print(f"SUMMARY: {critical} CRITICAL, {high} HIGH, {med} MEDIUM, {low} LOW")
    print(f"\nCI fail-gate (fails on CRITICAL or HIGH):")
    print(f"  python websocket_audit.py --root . --ci --min-severity HIGH")

    if CI_MODE and (critical + high) > 0:
        print(f"\n[CI] Exit 1 — {critical + high} CRITICAL/HIGH findings.")
        return 1
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='WebSocket security auditor')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--ci', action='store_true', help='Exit 1 on CRITICAL or HIGH')
    parser.add_argument('--min-severity', choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                        default='LOW')
    args = parser.parse_args()
    CI_MODE = args.ci
    MIN_SEVERITY = args.min_severity
    sys.exit(run_audit(Path(args.root)))
```

---

## Example Output

```
🔍  phy-websocket-audit — scanning /home/user/chat-app
────────────────────────────────────────────────────────────
Found 5 issue(s): 💀 CRITICAL=2  🔴 HIGH=1  🟡 MEDIUM=2  🔵 LOW=0

💀 CRITICAL — WS002
──────────────────────────────────────────────────────

[WS002] src/server/wsServer.js:14  (ws)
  CWE-346: WebSocket upgrade handler without Origin header validation.
           Any website can open a WebSocket connection using the user's cookies (CSWSH).
  Matched: wss.on('connection', (ws, req) => {
  Fix:
    const wss = new WebSocketServer({
      verifyClient: ({ origin }, cb) => {
        const allowed = ["https://yourdomain.com"];
        cb(allowed.includes(origin), 403, "Forbidden");
      }
    });

💀 CRITICAL — WS003
──────────────────────────────────────────────────────

[WS003] src/server/wsServer.js:14  (ws)
  CWE-306: WebSocket accepted without authentication check.
           Any unauthenticated client can connect and receive data.
  Matched: wss.on('connection', (ws, req) => {
  Fix:
    server.on("upgrade", (req, socket, head) => {
        const token = new URLSearchParams(req.url.split("?")[1]).get("token");
        if (!verifyToken(token)) { socket.destroy(); return; }
        wss.handleUpgrade(req, socket, head, ws => wss.emit("connection", ws, req));
    });

🔴 HIGH — WS004
──────────────────────────────────────────────────────

[WS004] src/server/wsServer.js:3  (ws)
  CWE-400: WebSocket server initialized without message size limit.
  Matched: const wss = new WebSocketServer({ port: 8080 })
  Fix:
    new WebSocketServer({ maxPayload: 1024 * 1024 })  // 1MB limit

════════════════════════════════════════════════════════════
SUMMARY: 2 CRITICAL, 1 HIGH, 2 MEDIUM, 0 LOW

CI fail-gate (fails on CRITICAL or HIGH):
  python websocket_audit.py --root . --ci --min-severity HIGH
```

---

## Why WebSocket Security Is Unique

WebSockets bypass the two main browser security mechanisms that protect HTTP APIs:

1. **No CORS pre-flight** — The browser sends a WebSocket upgrade request *without* checking CORS headers first. The `Origin` header is included, but only the *server* can enforce it — there's no automatic browser rejection.

2. **No SameSite protection for WebSockets** — `SameSite=Strict` cookies are sent with WebSocket upgrade requests on same-site navigations. A user visiting a malicious page on a different domain can trigger a WebSocket connection to your server with the user's cookies attached.

Result: a missing Origin check is a CSRF equivalent for WebSockets, and most developers don't know it.

---

## Supported Frameworks

| Language | Frameworks Detected |
|----------|-------------------|
| Node.js / TypeScript | `ws`, `Socket.IO`, raw `http.Server` |
| Python | `websockets`, `FastAPI WebSocket`, `Django Channels` |
| Go | `gorilla/websocket`, `nhooyr/websocket` |
| Java / Kotlin | Spring WebSocket, `@ServerEndpoint` |
| Ruby | ActionCable |

---

## Relationship to Other phy- Security Skills

| Skill | Protocol / Layer |
|-------|-----------------|
| `phy-websocket-audit` (this) | WebSocket (real-time, full-duplex) |
| `phy-cors-audit` | HTTP CORS headers (REST APIs) |
| `phy-security-headers` | HTTP response headers |
| `phy-ssrf-audit` | Server-side outbound HTTP requests |
| `phy-jwt-auth-audit` | Authentication token security |
| `phy-path-traversal-audit` | File system access via HTTP |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
