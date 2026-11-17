#!/usr/bin/env python3
"""Vulnerability Detector — severity-tiered detection engine (v3.0.0).

Implements the LOW / MEDIUM / HIGH / CRITICAL detection logic defined in
references/payload_playbook.md and references/advanced_payload_playbook.md.
Produces CANDIDATE findings (status=detected); the finding_validator.py
promotes them to validated/FP at the VALIDATION state.

This module is deterministic and side-effect free w.r.t. the network: it takes
recon results + a `probe` callable (provided by the agent via ctx.tools) and
emits candidate findings. The agent is responsible for routing every probe
through scope_guard + rate_limiter.

v3.0.0 EXPANSION: 22 → 38 vulnerability types. Adds:
  - NOSQL injection (MongoDB $ne/$gt/$regex operators)
  - LDAP injection (&)(|)(*) filter bypass
  - CRLF injection / HTTP response splitting
  - GraphQL introspection + injection
  - CORS misconfiguration (wildcard origin, null origin bypass)
  - Subdomain takeover (dangling DNS/CNAME)
  - Host header injection (password reset poisoning)
  - Web cache poisoning + cache deception
  - Race condition / TOCTOU
  - HTTP request smuggling (CL.TE / TE.CL)
  - Prototype pollution (client-side + server-side)
  - JWT deep analysis (kid injection, jku/x5u hijacking)
  - OAuth/OIDC misconfiguration
  - WebSocket hijacking (CSWSH)
  - Mass assignment
  - Email header injection
  - Session fixation
  - Dependency confusion

Usage (CLI emits the detection plan for a given assets set):
  python vuln_detector.py --assets assets.json --tier all
  python vuln_detector.py --assets assets.json --tier low,medium
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json

# ---- type → baseline severity (single source of truth) ----------------------
SEVERITY_BY_TYPE: dict[str, str] = {
    # low
    "info_leak": "low",
    "open_redirect": "low",
    "csrf": "low",
    "misconfig": "low",
    "graphql_introspection": "low",    # v3: GraphQL introspection disclosure
    "directory_listing": "low",         # v3: directory listing standalone
    # medium
    "path_traversal": "medium",
    "xxe": "medium",
    "ssti": "medium",
    "deserialization": "medium",
    "command_injection": "medium",
    "xss": "medium",
    "weak_credential": "medium",
    "component_exposure": "medium",
    "captcha_bypass": "medium",
    "crlf_injection": "medium",         # v3: CRLF / HTTP response splitting
    "cors_misconfig": "medium",         # v3: CORS misconfiguration
    "subdomain_takeover": "medium",     # v3: dangling DNS
    "host_header_injection": "medium",  # v3: host header poisoning
    "websocket_hijacking": "medium",    # v3: CSWSH
    "session_fixation": "medium",       # v3: session fixation
    "email_injection": "medium",        # v3: email header injection
    # high
    "sqli": "high",
    "ssrf": "high",
    "idor": "high",
    "file_upload": "high",
    "logic_flaw": "high",
    "nosql_injection": "high",          # v3: MongoDB/NoSQL injection
    "ldap_injection": "high",           # v3: LDAP injection
    "graphql_injection": "high",        # v3: GraphQL batching/DOS/injection
    "cache_poisoning": "high",          # v3: web cache poisoning
    "race_condition": "high",           # v3: TOCTOU / race condition
    "prototype_pollution": "high",      # v3: client/server prototype pollution
    "jwt_deep_analysis": "high",        # v3: extended JWT attacks
    "oauth_misconfig": "high",          # v3: OAuth flow misconfig
    "mass_assignment": "high",          # v3: auto-binding / mass assignment
    "dependency_confusion": "high",     # v3: supply chain dependency confusion
    # critical
    "rce": "critical",
    "auth_bypass": "critical",
    "priv_esc": "critical",
    "data_exposure": "critical",
    "http_smuggling": "critical",       # v3: HTTP request smuggling
}

TIER_ORDER = ["low", "medium", "high", "critical"]


@dataclass
class DetectionRule:
    """Declarative description of one detection probe.

    v5.1 fields:
      auto_verifiable — the candidate finding can be verified end-to-end by
        scripts/auto_verifier.py WITHOUT manual intervention (HTTP replay +
        deterministic signal matching, or pure local analysis).
      verification_method — how the auto-verification is performed:
        "http_probe"   : single replayed HTTP request, signal in response
        "timing_probe" : replayed request, signal = response-time delta
        "header_inspect": signal from response headers only
        "local_analysis": no network; signal computed from existing evidence
        ""             : requires manual/OOB/multi-account verification
    """

    type: str
    severity: str
    tier: str
    risk_level: str
    target_param_hints: list
    probe_description: str
    detection_signal: str
    safe_poc: bool = True
    requires_credentials: bool = False
    requires_human_approval: bool = False
    blocked_in_safe_mode: bool = False
    auto_verifiable: bool = False
    verification_method: str = ""


# =============================================================================
# LOW tier
# =============================================================================
LOW_RULES = [
    DetectionRule(
        type="info_leak", severity="low", tier="low", risk_level="L1",
        target_param_hints=["id", "file", "page"],
        probe_description="GET /<path>.bak, .old, .swp, .map; grep responses for AKIA/ghp_/BEGIN PRIVATE KEY/email patterns",
        detection_signal="200 on backup path OR sensitive pattern in response body",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="open_redirect", severity="low", tier="low", risk_level="L2",
        target_param_hints=["next", "url", "redirect", "return", "returnUrl", "goto", "target", "dest", "continue"],
        probe_description="Set redirect param to https://oob.authorized.test/PTSKILLTEST (and //, /\\ variants)",
        detection_signal="3xx Location or meta-refresh/JS redirect points to the authorized sink",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="csrf", severity="low", tier="low", risk_level="L2",
        target_param_hints=["<state-changing POST/PUT/DELETE endpoints>"],
        probe_description="Replay state-changing request with CSRF token removed and blanked; check SameSite cookie attr",
        detection_signal="Request succeeds (200/302) without valid token AND cookie lacks SameSite=Strict/Lax",
        requires_credentials=True,
    ),
    DetectionRule(
        type="misconfig", severity="low", tier="low", risk_level="L1",
        target_param_hints=["<root of each endpoint>"],
        probe_description="Inspect headers: missing HSTS/CSP/X-Frame-Options/X-Content-Type-Options; present X-Powered-By/Server version",
        detection_signal="Any required security header absent OR verbose version header present",
        auto_verifiable=True, verification_method="header_inspect",
    ),
    DetectionRule(
        type="component_exposure", severity="medium", tier="low", risk_level="L1",
        target_param_hints=["<root of each target>"],
        probe_description=(
            "Probe known component admin/leak paths at low rate: "
            "/actuator, /actuator/env, /actuator/heapdump, /actuator/mappings, /actuator/configprops, /actuator/jolokia; "
            "/druid/index.html, /druid/login.html, /druid/sql.html; "
            "/swagger-ui.html, /swagger-ui/index.html, /v2/api-docs, /v3/api-docs, /swagger-resources; "
            "/controller.ashx?action=catchimage (UEditor); /api-docs"
        ),
        detection_signal=(
            "200 on /actuator/env (env vars) OR /actuator/heapdump (binary dump) OR "
            "/druid/index.html (monitor page) OR /swagger-ui.html (API docs) OR "
            "response contains swagger JSON / actuator JSON / druid SQL monitor"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="info_leak", severity="low", tier="low", risk_level="L1",
        target_param_hints=["<root of each target>"],
        probe_description="Probe source-leak paths: /.git/config, /.svn/entries, /.DS_Store, /.env, /WEB-INF/web.xml, /WEB-INF/classes/, /crossdomain.xml, /phpinfo.php",
        detection_signal="200 on git/svn config path OR .env content OR WEB-INF web.xml OR phpinfo page",
        auto_verifiable=True, verification_method="http_probe",
    ),
    # v3 NEW: GraphQL introspection disclosure
    DetectionRule(
        type="graphql_introspection", severity="low", tier="low", risk_level="L1",
        target_param_hints=["/graphql", "/gql", "/api/graphql", "/v1/graphql"],
        probe_description=(
            "Send GraphQL introspection query to discover full API schema: "
            "POST with {__schema{types{name,fields{name,args{name,type{name}}}}}} "
            "OR GET /graphql?sdl for schema SDL"
        ),
        detection_signal=(
            "200 response with JSON containing __schema/types introspection data "
            "OR schema SDL with type definitions"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    # v3 NEW: Directory listing standalone
    DetectionRule(
        type="directory_listing", severity="low", tier="low", risk_level="L1",
        target_param_hints=["/uploads/", "/static/", "/backup/", "/logs/", "/temp/"],
        probe_description="GET common directories; check for Index of / and directory listing patterns",
        detection_signal="Response contains 'Index of /' or 'Parent Directory' or lists file/dir entries",
        auto_verifiable=True, verification_method="http_probe",
    ),
]

# =============================================================================
# MEDIUM tier
# =============================================================================
MEDIUM_RULES = [
    DetectionRule(
        type="xss", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["q", "search", "name", "msg", "comment", "title", "description"],
        probe_description="Inject PTSKILLTEST<xss>9a3f into reflected params (query/path/body)",
        detection_signal="Marker reflected unescaped (raw < > ) in response body",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="path_traversal", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["file", "path", "page", "template", "download", "doc", "image", "static"],
        probe_description="Inject ../../../../etc/passwd (unix) or ..\\..\\..\\..\\windows\\win.ini (windows) / encoded / filter-bypass variants; agent selects payload per target OS fingerprint",
        detection_signal="Response contains root:x:0:0: (unix target) or [fonts]/[extensions] (windows target) OR significant delta from baseline",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="xxe", severity="medium", tier="medium", risk_level="L3",
        target_param_hints=["<XML-accepting endpoints>"],
        probe_description="POST XML with <!ENTITY x SYSTEM https://oob.authorized.test/PTSKILLTEST-xxe>",
        detection_signal="OOB callback hit within 30s OR parser error mentions the sink URL",
    ),
    DetectionRule(
        type="ssti", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["q", "name", "template", "msg"],
        probe_description="Inject PTSKILLTEST{{7*7}} / ${7*7} / <%=7*7%> / #set($x=7*7)$x",
        detection_signal="Response contains '49' AND marker prefix; arithmetic evaluated (not literal reflection)",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="deserialization", severity="medium", tier="medium", risk_level="L3",
        target_param_hints=["<octet-stream endpoints>"],
        probe_description="Send innocuous serialized object (Java HashMap/PHP obj) then malformed blob; observe parser errors",
        detection_signal="500 error with framework-specific deserialization stack trace (InvalidClassException/unserialize/pickle.loads)",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="command_injection", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["host", "ip", "ping", "cmd", "exec", "name", "file"],
        probe_description="Time-based only: ;sleep 3 # / |sleep 3 / $(sleep 3) — ONE per param per run, capped 4s",
        detection_signal="Response time >= baseline + 2.5s AND <= 4s",
        auto_verifiable=True, verification_method="timing_probe",
    ),
    DetectionRule(
        type="weak_credential", severity="medium", tier="medium", risk_level="L3",
        target_param_hints=["login", "username", "user", "account", "password", "passwd", "pwd"],
        probe_description=(
            "Bounded default-credential probe against login endpoints (staging/dev ONLY, human-approved): "
            "admin/123456, admin/admin, admin/admin123, admin/password, admin/111111, admin/12345678, "
            "root/root, root/123456, test/test, guest/guest; "
            "Edu pattern: 学号/学号后6位, 工号/工号a; "
            "Stop on first success; max 10 attempts per endpoint"
        ),
        detection_signal=(
            "Login response indicates success (302 to dashboard / 200 with token / JSON {code:0,success:true}) "
            "using a default credential"
        ),
        requires_human_approval=True,
    ),
    DetectionRule(
        type="captcha_bypass", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["captcha", "code", "verifyCode", "vcode", "checkCode", "imgCode"],
        probe_description=(
            "Test captcha bypass modes: (1) empty captcha value; (2) remove captcha param entirely; "
            "(3) fixed/generic value '123456' (同济万能验证码案例); (4) reuse same captcha code multiple times; "
            "(5) 4-digit captcha brute-force feasibility check; "
            "(6) intercept & flip response {success:false->true, error_code:1->0}"
        ),
        detection_signal=(
            "Request succeeds with empty/missing/fixed captcha OR same captcha reusable OR "
            "response tamper bypass accepted (login/state-change succeeds)"
        ),
    ),
    # ---- v3 NEW: CRLF injection / HTTP response splitting -------------------
    DetectionRule(
        type="crlf_injection", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["redirect", "url", "return", "next", "language", "locale", "lang"],
        probe_description=(
            "Inject CRLF sequences into URL parameters to test HTTP response splitting: "
            "%0d%0aSet-Cookie:PTSKILLTEST=crlf / %0d%0a%0d%0a<script> / "
            "\\r\\nX-PTSKILLTEST: injected"
        ),
        detection_signal=(
            "Response contains injected header (Set-Cookie: PTSKILLTEST=crlf) OR "
            "reflected CRLF in response body before content-type"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    # ---- v3 NEW: CORS misconfiguration --------------------------------------
    DetectionRule(
        type="cors_misconfig", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["<all API endpoints>"],
        probe_description=(
            "Test CORS misconfiguration: (1) send Origin: null — check Access-Control-Allow-Origin: null; "
            "(2) send Origin: https://attacker.evil.test — check if reflected; "
            "(3) send Origin: https://target.test.attacker.evil.test — check suffix bypass; "
            "(4) check Access-Control-Allow-Credentials: true with wildcard origin"
        ),
        detection_signal=(
            "ACAO: null with credentials OR ACAO reflects attacker origin OR "
            "wildcard ACAO with credentials OR suffix-based origin bypass"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    # ---- v3 NEW: Subdomain takeover -----------------------------------------
    DetectionRule(
        type="subdomain_takeover", severity="medium", tier="medium", risk_level="L1",
        target_param_hints=["<all discovered subdomains>"],
        probe_description=(
            "Check CNAME records for dangling DNS pointers to cloud services: "
            "AWS CloudFront/S3, Azure, GitHub Pages, Heroku, Netlify, Shopify, "
            "Fastly, Zendesk, etc. Detect NXDOMAIN or 404 with service-specific error pages"
        ),
        detection_signal=(
            "CNAME points to cloud service (cloudfront.net/s3.amazonaws.com/azurewebsites.net/etc.) AND "
            "target returns NXDOMAIN or 404 with service-branded error page"
        ),
    ),
    # ---- v3 NEW: Host header injection --------------------------------------
    DetectionRule(
        type="host_header_injection", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["password-reset", "forgot", "reset", "link", "magic"],
        probe_description=(
            "Test host header poisoning: (1) set Host: attacker.evil.test — check if reflected in links/redirects; "
            "(2) set X-Forwarded-Host: attacker.evil.test — check password reset link poisoning; "
            "(3) set X-Forwarded-For / X-Real-IP to test IP spoofing"
        ),
        detection_signal=(
            "Response links/redirects contain attacker-controlled host OR "
            "password reset link uses injected host header"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    # ---- v3 NEW: WebSocket hijacking (CSWSH) ---------------------------------
    DetectionRule(
        type="websocket_hijacking", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["<WebSocket endpoints (ws:// or wss://)>"],
        probe_description=(
            "Test WebSocket security: (1) check Origin header validation on WS handshake; "
            "(2) send Origin: null — cross-site WebSocket hijacking; "
            "(3) check for missing authentication on WS endpoint; "
            "(4) test for plaintext ws:// instead of wss://"
        ),
        detection_signal=(
            "WS handshake succeeds with null/mismatched Origin OR "
            "WS endpoint accepts unauthenticated connections OR ws:// in production"
        ),
    ),
    # ---- v3 NEW: Session fixation -------------------------------------------
    DetectionRule(
        type="session_fixation", severity="medium", tier="medium", risk_level="L3",
        target_param_hints=["PHPSESSID", "JSESSIONID", "session", "sid", "token"],
        probe_description=(
            "Test session fixation: (1) obtain a session ID before login, check if same ID persists after login; "
            "(2) inject session ID via URL parameter (?PHPSESSID=attacker); "
            "(3) inject session ID via cookie before authentication"
        ),
        detection_signal=(
            "Session ID unchanged after login (pre-login token == post-login token) OR "
            "URL-based session ID accepted"
        ),
        requires_credentials=True,
    ),
    # ---- v3 NEW: Email header injection -------------------------------------
    DetectionRule(
        type="email_injection", severity="medium", tier="medium", risk_level="L2",
        target_param_hints=["email", "to", "from", "subject", "body", "contact", "feedback"],
        probe_description=(
            "Test email header injection: inject \\r\\nBcc: / \\r\\nCc: / \\r\\nContent-Type: "
            "into email fields to test SMTP header injection. "
            "Detect via response differences (error message, timing) or OOB."
        ),
        detection_signal=(
            "Response differs from baseline (error message mentions SMTP/mail) OR "
            "OOB email received at authorized sink"
        ),
    ),
]

# =============================================================================
# HIGH tier
# =============================================================================
HIGH_RULES = [
    DetectionRule(
        type="xss", severity="high", tier="high", risk_level="L3",
        target_param_hints=["comment", "bio", "message", "profile"],
        probe_description="Submit marker via write endpoint; render as a DIFFERENT test account; confirm cross-user reflection",
        detection_signal="Stored marker reflected unescaped to a second account's view",
        requires_credentials=True,
    ),
    DetectionRule(
        type="sqli", severity="high", tier="high", risk_level="L2",
        target_param_hints=["id", "q", "search", "user", "name", "filter"],
        probe_description="Error-based (PTSKILLTEST') + boolean differential (AND 1=1 vs AND 1=2) + capped time-based (pg_sleep 2)",
        detection_signal="DB error signature OR boolean differential OR time delta >= 1.8s",
        auto_verifiable=True, verification_method="http_probe",
    ),
    DetectionRule(
        type="ssrf", severity="high", tier="high", risk_level="L4",
        target_param_hints=["url", "image", "webhook", "callback", "fetch"],
        probe_description="Set url param to https://oob.authorized.test/<run_id>/PTSKILLTEST; await callback",
        detection_signal="OOB callback hit within 30s",
        requires_human_approval=True,
        blocked_in_safe_mode=True,
    ),
    DetectionRule(
        type="idor", severity="high", tier="high", risk_level="L3",
        target_param_hints=["id", "user_id", "account", "doc_id", "order", "applyId", "student_uuid", "studentId", "userId", "qxid", "secode", "uid"],
        probe_description=(
            "As user A capture object; as user B/unauth request SAME object id; "
            "ALSO test sequential ID enumeration (id+1, id-1) and UUID predictability; "
            "覆盖水平越权(id/userId/applyId/student_uuid) + 交叉越权(qxid/secode)"
        ),
        detection_signal="User B receives 200 with user-A's data (expected 403/404) OR sequential ID returns different user's data",
        requires_credentials=True,
    ),
    DetectionRule(
        type="file_upload", severity="high", tier="high", risk_level="L3",
        target_param_hints=["upload", "file", "avatar", "image", "attachment", "doc", "img"],
        probe_description=(
            "DETECTION ONLY (no real webshell): "
            "(1) Upload a benign .txt marker file 'PTSKILLTEST-upload-9a3f' — confirm it is stored & accessible; "
            "(2) Test extension bypass: .jpg.php, .phtml, .phar, .asp;jpg, .html, .svg (XSS carrier); "
            "(3) Test Content-Type manipulation: image/jpeg header + .php body; "
            "(4) Test double-extension: file.jpg.html (同济案例); "
            "(5) Test UEditor action=catchimage with remote URL pointing to authorized sink; "
            "(6) Test Content-Disposition double-write bypass (南开安全狗案例). "
            "Flag if uploaded file is accessible AND executable OR if non-image extension accepted"
        ),
        detection_signal=(
            "Uploaded marker file accessible at known path OR executable extension (.php/.asp/.jsp) accepted & served OR "
            "SVG with script accessible OR UEditor catchimage fetches remote URL"
        ),
        requires_credentials=True,
    ),
    DetectionRule(
        type="logic_flaw", severity="high", tier="high", risk_level="L3",
        target_param_hints=["price", "amount", "count", "role", "type", "level", "status", "is_admin", "is_vip", "balance", "score", "orderId", "step"],
        probe_description=(
            "Business-logic flaw DETECTION (non-destructive, synthetic test objects only): "
            "(1) Response tampering: intercept response, flip error_code:1->0, success:false->true, role:user->admin, Message:0->1; "
            "(2) Parameter tampering: modify price/amount to negative or 0, modify quantity to large number; "
            "(3) Step skip: directly access step3 URL bypassing step1/step2; "
            "(4) SMS/verification bombing: probe /sendPasswordCode or /sendSms endpoint — check rate limit; "
            "(5) Replay: replay a state-changing request N times; "
            "(6) Negative value: amount=-1, count=-100"
        ),
        detection_signal=(
            "Tampered response accepted OR negative/zero price accepted OR "
            "step-skip grants access OR SMS endpoint has no rate limit (>5/min) OR replay applies N times OR "
            "negative amount reverses balance"
        ),
        requires_credentials=True,
    ),
    # ---- v3 NEW: NoSQL injection (MongoDB) -----------------------------------
    DetectionRule(
        type="nosql_injection", severity="high", tier="high", risk_level="L2",
        target_param_hints=["id", "user", "username", "email", "search", "q", "filter"],
        probe_description=(
            "Test NoSQL injection (MongoDB): "
            "(1) $ne bypass: {'$ne': null} → bypass auth/query filters; "
            "(2) $regex blind: {'$regex': '^admin'} → enumerate users; "
            "(3) $gt timing: {'$gt': ''} → compare response size/timing; "
            "(4) $where JS injection: {$where: 'sleep(3000)'}"
        ),
        detection_signal=(
            "Response differs from baseline (JSON injection accepted) OR "
            "$regex enumeration reveals data OR $where timing delta >= 2.5s"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    # ---- v3 NEW: LDAP injection ---------------------------------------------
    DetectionRule(
        type="ldap_injection", severity="high", tier="high", risk_level="L2",
        target_param_hints=["user", "username", "name", "search", "filter", "query"],
        probe_description=(
            "Test LDAP injection: (1) *)(& → bypass AND filter; (2) *)(|(uid=* → OR filter; "
            "(3) *)(uid=*))(|(uid=* → multi-filter; (4) *)(|(password=* → password enumeration; "
            "(5) time-based: *)(objectClass=*&sleep(3) → timing test"
        ),
        detection_signal=(
            "LDAP filter bypass succeeds (auth/login works with injected filter) OR "
            "LDAP error message in response (LDAPException/NamingException) OR "
            "time-based LDAP injection confirmed"
        ),
        auto_verifiable=True, verification_method="http_probe",
    ),
    # ---- v3 NEW: GraphQL injection ------------------------------------------
    DetectionRule(
        type="graphql_injection", severity="high", tier="high", risk_level="L2",
        target_param_hints=["/graphql", "/gql", "/api/graphql"],
        probe_description=(
            "Test GraphQL injection: (1) batching attack — send multiple queries in one request; "
            "(2) alias-based rate limit bypass — use aliases to repeat the same query; "
            "(3) depth/circular query — test if nested queries cause DOS; "
            "(4) field suggestion — send malformed query to leak field names; "
            "(5) SQL injection via GraphQL arguments"
        ),
        detection_signal=(
            "Batching accepted (multiple queries resolved) OR "
            "alias-based rate limit bypass works OR deep recursive query accepted OR "
            "field suggestions reveal schema OR SQL injection in GraphQL args"
        ),
    ),
    # ---- v3 NEW: Web cache poisoning ----------------------------------------
    DetectionRule(
        type="cache_poisoning", severity="high", tier="high", risk_level="L3",
        target_param_hints=["X-Forwarded-Host", "X-Forwarded-Scheme", "X-Forwarded-Port", "Origin", "Host"],
        probe_description=(
            "Test web cache poisoning: (1) inject X-Forwarded-Host → check if reflected in cached response; "
            "(2) unkeyed header injection — add X-PTSKILLTEST: cache-test → check if cached; "
            "(3) cache deception — GET /profile.css → check if cached; "
            "(4) fat GET — POST with body to cached endpoint"
        ),
        detection_signal=(
            "Injected header value reflected in cached response OR "
            "unkeyed header cached and served to other users OR "
            "cache deception: authenticated page cached as static resource"
        ),
    ),
    # ---- v3 NEW: Race condition / TOCTOU ------------------------------------
    DetectionRule(
        type="race_condition", severity="high", tier="high", risk_level="L3",
        target_param_hints=["coupon", "redeem", "withdraw", "transfer", "order", "checkout"],
        probe_description=(
            "Test race condition (TOCTOU): (1) send multiple concurrent requests to same endpoint; "
            "(2) test coupon/voucher double-use — send 2+ requests simultaneously; "
            "(3) test balance withdrawal — send concurrent withdrawal requests; "
            "(4) test file upload — concurrent uploads to same filename"
        ),
        detection_signal=(
            "Duplicate action accepted (coupon used twice, balance withdrawn twice) OR "
            "race condition causes inconsistent state"
        ),
        requires_credentials=True,
    ),
    # ---- v3 NEW: Prototype pollution -----------------------------------------
    DetectionRule(
        type="prototype_pollution", severity="high", tier="high", risk_level="L2",
        target_param_hints=["__proto__", "constructor", "prototype", "q", "filter", "params"],
        probe_description=(
            "Test prototype pollution: (1) client-side: ?__proto__[polluted]=PTSKILLTEST; "
            "(2) server-side: POST JSON with {__proto__:{polluted:PTSKILLTEST}}; "
            "(3) constructor.prototype injection: {constructor:{prototype:{polluted:PTSKILLTEST}}}; "
            "(4) merge/deep-extend function abuse"
        ),
        detection_signal=(
            "Polluted property reflected in response OR "
            "DOM mutation observed via browser OR "
            "server-side pollution changes behavior (status change, error difference)"
        ),
    ),
    # ---- v3 NEW: JWT deep analysis ------------------------------------------
    DetectionRule(
        type="jwt_deep_analysis", severity="high", tier="high", risk_level="L3",
        target_param_hints=["Authorization", "Bearer", "token", "jwt", "access_token"],
        probe_description=(
            "Extended JWT analysis: (1) kid injection — ../../../../etc/passwd; "
            "(2) jku/x5u header injection — point to attacker-controlled JWKS; "
            "(3) algorithms confusion: RS256→HS256 with public key; "
            "(4) empty signature / none algorithm; (5) weak HMAC secret brute-force; "
            "(6) exp/nbf/iat manipulation; (7) audience/sub claim confusion"
        ),
        detection_signal=(
            "JWT accepted with modified algorithm (alg:none/HS256 with pubkey) OR "
            "kid injection succeeds OR jku/x5u hijacking works OR "
            "expired/exp-manipulated token accepted"
        ),
        requires_credentials=True,
    ),
    # ---- v3 NEW: OAuth misconfiguration -------------------------------------
    DetectionRule(
        type="oauth_misconfig", severity="high", tier="high", risk_level="L3",
        target_param_hints=["redirect_uri", "client_id", "state", "code", "response_type", "scope"],
        probe_description=(
            "Test OAuth 2.0 misconfiguration: (1) open redirect in redirect_uri; "
            "(2) CSRF in state parameter (missing/invalid); "
            "(3) authorization code replay; (4) PKCE missing; "
            "(5) implicit flow token leakage; (6) scope upgrade"
        ),
        detection_signal=(
            "redirect_uri accepts attacker-controlled value OR "
            "state parameter missing/not validated OR "
            "authorization code reusable OR PKCE not enforced"
        ),
    ),
    # ---- v3 NEW: Mass assignment --------------------------------------------
    DetectionRule(
        type="mass_assignment", severity="high", tier="high", risk_level="L3",
        target_param_hints=["profile", "user", "account", "register", "settings", "update"],
        probe_description=(
            "Test mass assignment (auto-binding): (1) add is_admin=true to user update; "
            "(2) add role=admin / role_id=1 to registration; (3) add balance=999999 to profile; "
            "(4) add verified=true / email_verified=true; (5) add plan=enterprise to subscription"
        ),
        detection_signal=(
            "Extra parameter accepted (is_admin/role/balance/verified/plan) "
            "and value reflected in subsequent GET or login response"
        ),
        requires_credentials=True,
    ),
    # ---- v3 NEW: Dependency confusion ---------------------------------------
    DetectionRule(
        type="dependency_confusion", severity="high", tier="high", risk_level="L1",
        target_param_hints=["package.json", "composer.json", "requirements.txt", "Pipfile", "Gemfile", "pom.xml"],
        probe_description=(
            "Supply chain dependency confusion: (1) check for exposed package.json/Pipfile/composer.json; "
            "(2) identify internal packages with no public registry entry; "
            "(3) check if npm/pip/composer registry allows scoped packages without verification"
        ),
        detection_signal=(
            "Internal package name found in dependency manifest AND "
            "package not registered on public registry OR scoped package configurable"
        ),
    ),
]

# =============================================================================
# CRITICAL tier
# =============================================================================
CRITICAL_RULES = [
    DetectionRule(
        type="rce", severity="critical", tier="critical", risk_level="L4",
        target_param_hints=["<confirmed command_injection/ssti/deserialization surfaces>"],
        probe_description="Second independent time-based/arithmetic probe to confirm code-exec context (NO data exfil)",
        detection_signal="Second independent probe succeeds; no data exfiltrated",
        requires_human_approval=True,
        blocked_in_safe_mode=True,
    ),
    DetectionRule(
        type="auth_bypass", severity="critical", tier="critical", risk_level="L3",
        target_param_hints=["login", "auth", "token", "reset"],
        probe_description="Default-cred (bounded, approved) / JWT alg:none+kid traversal / reset-token predictability",
        detection_signal="Unauthenticated or wrong-identity request accepted as authenticated/different identity",
        requires_human_approval=True,
    ),
    DetectionRule(
        type="priv_esc", severity="critical", tier="critical", risk_level="L3",
        target_param_hints=["role", "admin", "isAdmin", "user_type"],
        probe_description="As low-priv user call admin endpoints; flip role claim in JWT/cookie (alg:none if key unknown)",
        detection_signal="Low-priv user gets 200 on admin endpoint OR role flip accepted",
        requires_credentials=True,
        requires_human_approval=True,
    ),
    DetectionRule(
        type="data_exposure", severity="critical", tier="critical", risk_level="L2",
        target_param_hints=["<any validated finding exposing response body>"],
        probe_description="Regex-count PII in confirmed-finding responses: >=10 emails OR phone/SSN/card OR password/secret/api_key fields",
        detection_signal="PII count thresholds exceeded — UPGRADES an existing finding to critical",
        auto_verifiable=True, verification_method="local_analysis",
    ),
    # ---- v3 NEW: HTTP request smuggling -------------------------------------
    DetectionRule(
        type="http_smuggling", severity="critical", tier="critical", risk_level="L4",
        target_param_hints=["<all endpoints behind proxy/CDN>"],
        probe_description=(
            "Test HTTP request smuggling: (1) CL.TE: Content-Length + Transfer-Encoding mismatch; "
            "(2) TE.CL: Transfer-Encoding first, Content-Length second; "
            "(3) TE.TE: obfuscated Transfer-Encoding (\\r\\n, 0x0d, chunked0); "
            "(4) detect via time differential: send slow POST + smuggled request"
        ),
        detection_signal=(
            "Time differential observed (smuggled request processed) OR "
            "response queue poisoning (different user's response received) OR "
            "400/500 from smuggled request"
        ),
        requires_human_approval=True,
        blocked_in_safe_mode=True,
    ),
]

TIER_RULES = {
    "low": LOW_RULES,
    "medium": MEDIUM_RULES,
    "high": HIGH_RULES,
    "critical": CRITICAL_RULES,
}


def candidate_finding(rule, target, evidence_hint=""):
    """Build a candidate Finding (status=detected) from a rule + target.

    v5.1: each candidate carries `auto_verifiable` / `verification_method`
    so the VALIDATION state (scripts/auto_verifier.py) knows which findings
    can be closed-loop verified without manual intervention.
    """
    return {
        "id": "",
        "type": rule.type,
        "severity": rule.severity,
        "tier": rule.tier,
        "target": target,
        "status": "detected",
        "confidence": 0.5,
        "evidence": {
            "request": evidence_hint,
            "response": "",
            "timestamp": "",
            "tool": "",
        },
        "reproducible": False,
        "safe_poc": rule.safe_poc,
        "risk_level": rule.risk_level,
        "requires_human_approval": rule.requires_human_approval,
        "blocked_in_safe_mode": rule.blocked_in_safe_mode,
        "detection_signal": rule.detection_signal,
        "auto_verifiable": rule.auto_verifiable,
        "verification_method": rule.verification_method,
        "requires_credentials": rule.requires_credentials,
    }


def _extract_targets(assets):
    """Robustly extract probe targets from the recon assets object.

    Accepts endpoints as dicts ({'url': ...}) or plain strings; filters out
    empty/invalid entries. Falls back to scope domains (as https URLs) when
    no endpoints were discovered, so the plan is never silently empty.
    """
    targets: list[str] = []
    for e in assets.get("endpoints", []) or []:
        if isinstance(e, dict):
            url = str(e.get("url", "") or "").strip()
        else:
            url = str(e or "").strip()
        if url:
            targets.append(url)
    if not targets:
        for d in assets.get("domains", []) or []:
            d = str(d or "").strip()
            if d:
                if "://" not in d:
                    d = "https://" + d
                targets.append(d)
    # Dedup while preserving order (a probe per duplicated URL is wasted budget)
    seen: set[str] = set()
    deduped: list[str] = []
    for t in targets:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


def build_plan(assets, tiers, safe_mode=True, include_l4=False, max_per_type=None):
    """Return the ordered list of candidate probes to run for the given tiers.

    Args:
        assets: recon output (domains, ips, endpoints).
        tiers: subset of TIER_ORDER to include.
        safe_mode: when True, rules marked blocked_in_safe_mode are EXCLUDED.
        include_l4: when True (and safe_mode is False), include L4 rules.
        max_per_type: v5.1 — cap candidates per vulnerability type (int > 0).
            Prevents plan explosion when recon returns many endpoints
            ("计划生成多" problem). None = unlimited (backward compatible).
    """
    if max_per_type is not None and (not isinstance(max_per_type, int) or max_per_type < 1):
        raise ValueError("max_per_type must be a positive integer or None")

    targets = _extract_targets(assets)
    plan = []
    per_type_count: dict[str, int] = {}
    for tier in (t for t in TIER_ORDER if t in tiers):
        for rule in TIER_RULES[tier]:
            if safe_mode and rule.blocked_in_safe_mode:
                continue
            if rule.risk_level == "L4" and not include_l4:
                continue
            for t in targets:
                if max_per_type is not None:
                    key = f"{rule.type}@{rule.tier}"
                    if per_type_count.get(key, 0) >= max_per_type:
                        break
                    per_type_count[key] = per_type_count.get(key, 0) + 1
                plan.append(candidate_finding(rule, t, rule.probe_description))
    return plan


def classify_data_exposure(response_body):
    """Check whether a response body triggers data_exposure (critical upgrade).

    Returns (triggered, score). score = sum of matched category flags.
    """
    score = 0
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response_body)
    if len(emails) >= 10:
        score += 3
    phones = re.findall(r"\b(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b", response_body)
    if len(phones) >= 5:
        score += 2
    ssn = re.findall(r"\b\d{3}-\d{2}-\d{4}\b", response_body)
    if ssn:
        score += 3
    cards = re.findall(r"\b(?:\d[ -]*?){13,16}\b", response_body)
    if cards:
        score += 3
    secret_keys = re.findall(r'(?i)["\'](password|secret|api_key|apikey|token|access_key)["\']\s*[:=]\s*["\'][^"\']{4,}', response_body)
    if secret_keys:
        score += 3
    return (score >= 3, score)


def main():
    ap = argparse.ArgumentParser(description="Severity-tiered vulnerability detection plan generator (v3.0)")
    ap.add_argument("--assets", required=True, help="Assets JSON (recon output) path or '-'")
    ap.add_argument("--tier", default="all", help="Comma-separated tiers: low,medium,high,critical or 'all'")
    ap.add_argument("--safe-mode", action="store_true", default=True, help="Honor safe_mode (default ON)")
    ap.add_argument("--no-safe-mode", dest="safe_mode", action="store_false", help="Disable safe_mode")
    ap.add_argument("--include-l4", action="store_true", default=False,
                    help="Include L4 rules (SSRF, RCE, destructive). Requires --no-safe-mode for execution.")
    ap.add_argument("--max-per-type", type=int, default=None,
                    help="v5.1: cap candidate probes per vulnerability type (prevents plan explosion)")
    args = ap.parse_args()

    if args.tier.strip().lower() == "all":
        tiers = list(TIER_ORDER)
    else:
        tiers, invalid = [], []
        for tok in args.tier.split(","):
            tok_norm = tok.strip().lower()
            if tok_norm in TIER_ORDER:
                tiers.append(tok_norm)
            elif tok_norm:
                invalid.append(tok.strip())
        if invalid:
            print(f"vuln_detector: invalid tier(s) {', '.join(invalid)!r}; "
                  f"valid tiers: {', '.join(TIER_ORDER)}", file=sys.stderr)
            return 2
        # Dedup preserving order
        tiers = list(dict.fromkeys(tiers))
    if not tiers:
        print(f"vuln_detector: invalid tier '{args.tier}'", file=sys.stderr)
        return 2

    if args.max_per_type is not None and args.max_per_type < 1:
        print("vuln_detector: --max-per-type must be >= 1", file=sys.stderr)
        return 2

    try:
        assets = load_json(args.assets)
    except (OSError, json.JSONDecodeError) as e:
        print(f"vuln_detector: cannot load assets: {e}", file=sys.stderr)
        return 2
    if not isinstance(assets, dict):
        print("vuln_detector: assets JSON must be an object", file=sys.stderr)
        return 2

    try:
        plan = build_plan(assets, tiers, args.safe_mode, args.include_l4,
                          max_per_type=args.max_per_type)
    except ValueError as e:
        print(f"vuln_detector: {e}", file=sys.stderr)
        return 2
    for i, item in enumerate(plan, 1):
        item["id"] = f"finding-{i:03d}"
    auto_verifiable_count = sum(1 for p in plan if p.get("auto_verifiable"))
    print(dump_json({
        "tier": tiers,
        "safe_mode": args.safe_mode,
        "include_l4": args.include_l4,
        "plan_count": len(plan),
        "auto_verifiable_count": auto_verifiable_count,
        "auto_verifiable_ratio": round(auto_verifiable_count / len(plan), 2) if plan else 0.0,
        "plan": plan,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())