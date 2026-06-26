#!/usr/bin/env bash
# HTTPLint -- HTTP Misconfiguration Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Direct security vulnerability or data exposure
#   high     -- Significant HTTP misconfiguration requiring prompt fix
#   medium   -- Moderate concern that should be addressed
#   low      -- Best practice suggestion
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.

set -euo pipefail

# ===========================================================================
# HC -- HTTP Client (15 patterns: HC-001 to HC-015)
# Free tier
# ===========================================================================

declare -a HTTPLINT_HC_PATTERNS=(
  'fetch\([[:space:]]*["\x27]http://|critical|HC-001|HTTP fetch over plaintext connection|Use HTTPS for all fetch requests to prevent MITM attacks'
  'axios\.get\([[:space:]]*["\x27]http://|critical|HC-002|Axios GET over insecure HTTP|Use HTTPS URLs in all axios requests'
  'requests\.get\([[:space:]]*["\x27]http://|critical|HC-003|Python requests over insecure HTTP|Use HTTPS for all outbound HTTP requests'
  'verify[[:space:]]*=[[:space:]]*False|critical|HC-004|SSL verification disabled in Python requests|Enable SSL verification; use verify=True'
  'rejectUnauthorized[[:space:]]*:[[:space:]]*false|critical|HC-005|Node.js TLS verification disabled|Enable TLS certificate verification in production'
  'InsecureRequestWarning|high|HC-006|Suppressing insecure request warnings|Fix the underlying HTTPS issue instead of suppressing warnings'
  'timeout[[:space:]]*:[[:space:]]*0[[:space:]]*[,})]|high|HC-007|HTTP client timeout set to zero (infinite)|Set a reasonable timeout (e.g., 30 seconds) to prevent hanging connections'
  'fetch\([^)]*\)[[:space:]]*$|medium|HC-008|Fetch call without error handling or await|Use try/catch with await or .catch() for proper error handling'
  'HttpClient\(\)|medium|HC-009|HTTP client created without configuration|Configure timeout, retry, and connection pooling options'
  'curl[[:space:]].*-k|high|HC-010|Curl with insecure flag skipping SSL|Remove -k flag and fix certificate chain instead'
  'http\.request\(|medium|HC-011|Using raw http.request instead of https|Use https.request or a library with built-in TLS support'
  'new[[:space:]]+XMLHttpRequest|low|HC-012|Legacy XMLHttpRequest usage|Use fetch API or axios for modern HTTP client features'
  'proxy[[:space:]]*:[[:space:]]*["\x27]http://|high|HC-013|Proxy configured over insecure HTTP|Use HTTPS proxy to prevent credential interception'
  'setRequestHeader\([[:space:]]*["\x27]Authorization|medium|HC-014|Authorization header set in XHR without security review|Ensure tokens are stored securely and transmitted over HTTPS only'
  'followRedirects[[:space:]]*:[[:space:]]*true|low|HC-015|Following redirects may lead to open redirect vulnerabilities|Validate redirect destinations and limit redirect count'
)

# ===========================================================================
# HS -- HTTP Server (15 patterns: HS-001 to HS-015)
# Free tier
# ===========================================================================

declare -a HTTPLINT_HS_PATTERNS=(
  'Access-Control-Allow-Origin[[:space:]]*:[[:space:]]*\*|critical|HS-001|CORS wildcard allows any origin|Restrict Access-Control-Allow-Origin to specific trusted domains'
  'Access-Control-Allow-Credentials.*true.*Allow-Origin.*\*|critical|HS-002|CORS credentials with wildcard origin is a security vulnerability|Never combine credentials=true with wildcard origin'
  'app\.listen\([[:space:]]*[0-9]|medium|HS-003|Server listening on hardcoded port|Use environment variable for port configuration'
  'res\.send\([[:space:]]*500|medium|HS-004|Sending raw 500 status without proper error structure|Return structured error responses with appropriate detail level'
  'createServer\([[:space:]]*function|low|HS-005|Raw HTTP server without framework middleware|Consider using Express/Fastify for built-in security middleware'
  'X-Powered-By|medium|HS-006|X-Powered-By header leaks server technology|Remove or disable X-Powered-By header to reduce information exposure'
  'helmet|low|HS-007|Consider using Helmet.js for HTTP security headers|Add helmet() middleware for automatic security header configuration'
  'bodyParser\.json\(\)|low|HS-008|Body parser without size limit configuration|Set a limit option to prevent large payload attacks: json({ limit: "1mb" })'
  'express\.static\([[:space:]]*["\x27]\./|medium|HS-009|Serving static files from project root|Serve static files from a dedicated public directory with restricted access'
  'res\.redirect\([[:space:]]*req\.|high|HS-010|Redirect using unvalidated user input|Validate and whitelist redirect destinations to prevent open redirect'
  'app\.use\([[:space:]]*cors\(\)\)|high|HS-011|CORS enabled with default permissive settings|Configure CORS with specific origins, methods, and headers'
  'res\.header\([[:space:]]*["\x27]Set-Cookie|medium|HS-012|Manual cookie setting without security flags|Use cookie library with secure, httpOnly, and sameSite flags'
  'app\.disable\([[:space:]]*["\x27]etag|low|HS-013|ETag disabled reducing caching efficiency|Keep ETags enabled for proper cache validation'
  'res\.json\([[:space:]]*err|high|HS-014|Sending raw error object in response may leak internals|Return sanitized error messages without stack traces or internal details'
  'trust[[:space:]]*proxy|medium|HS-015|Trust proxy setting needs careful configuration|Set trust proxy to specific IP range, not true, to prevent IP spoofing'
)

# ===========================================================================
# CK -- Cookie & Session (15 patterns: CK-001 to CK-015)
# Pro tier
# ===========================================================================

declare -a HTTPLINT_CK_PATTERNS=(
  'Set-Cookie[^;]*[^Ss]ecure|critical|CK-001|Cookie set without Secure flag|Add Secure flag to prevent transmission over HTTP'
  'httpOnly[[:space:]]*:[[:space:]]*false|critical|CK-002|HttpOnly flag explicitly disabled on cookie|Set httpOnly: true to prevent JavaScript access to cookies'
  'sameSite[[:space:]]*:[[:space:]]*["\x27]none["\x27]|high|CK-003|SameSite=None allows cross-site cookie sending|Use SameSite=Strict or Lax unless cross-site is required with Secure flag'
  'document\.cookie[[:space:]]*=|critical|CK-004|Setting cookies via JavaScript is vulnerable to XSS|Use server-side Set-Cookie headers with httpOnly flag'
  'session\.cookie\.secure[[:space:]]*=[[:space:]]*false|critical|CK-005|Session cookie secure flag disabled|Enable secure flag for session cookies in production'
  'cookie-parser|low|CK-006|Cookie parser without signed cookies consideration|Use signed cookies to detect tampering'
  'maxAge[[:space:]]*:[[:space:]]*[0-9]{8,}|medium|CK-007|Cookie with very long expiration increases risk window|Set reasonable cookie expiration aligned with session policy'
  'session[[:space:]]*=[[:space:]]*req\.cookies|medium|CK-008|Using raw cookie value as session identifier|Use established session middleware with secure defaults'
  'express-session.*secret[[:space:]]*:[[:space:]]*["\x27][a-z]+["\x27]|high|CK-009|Weak or short session secret|Use a strong random secret of at least 32 characters'
  'localStorage\.setItem\([[:space:]]*["\x27]token|high|CK-010|Storing auth tokens in localStorage is XSS vulnerable|Store tokens in httpOnly cookies instead of localStorage'
  'sessionStorage\.setItem\([[:space:]]*["\x27]token|medium|CK-011|Auth token in sessionStorage vulnerable to XSS|Prefer httpOnly cookies for authentication tokens'
  'cookie\.domain[[:space:]]*=[[:space:]]*["\x27]\.|medium|CK-012|Cookie domain starts with dot allowing subdomain access|Be explicit about cookie domain to prevent subdomain attacks'
  'session\.regenerate|low|CK-013|Ensure session regeneration on privilege escalation|Call session.regenerate() after login to prevent session fixation'
  'connect\.sid|medium|CK-014|Default session cookie name reveals technology stack|Customize session cookie name to reduce information exposure'
  'cookieParser\([[:space:]]*\)|medium|CK-015|Cookie parser initialized without secret for signed cookies|Provide a secret to enable cookie signing and integrity checking'
)

# ===========================================================================
# CH -- Caching & Headers (15 patterns: CH-001 to CH-015)
# Pro tier
# ===========================================================================

declare -a HTTPLINT_CH_PATTERNS=(
  'Cache-Control[[:space:]]*:[[:space:]]*no-cache|low|CH-001|no-cache still allows storage; use no-store for sensitive data|Use Cache-Control: no-store for truly sensitive responses'
  'Pragma[[:space:]]*:[[:space:]]*no-cache|low|CH-002|Pragma is HTTP/1.0 only; prefer Cache-Control|Use Cache-Control header for proper cache management'
  'Content-Type[[:space:]]*:[[:space:]]*text/html[^;]|medium|CH-003|Content-Type without charset may cause encoding issues|Include charset=utf-8 in Content-Type header'
  'X-Frame-Options|low|CH-004|X-Frame-Options is deprecated; use CSP frame-ancestors|Migrate to Content-Security-Policy frame-ancestors directive'
  'Strict-Transport-Security|low|CH-005|HSTS header check -- ensure it is present and configured|Set HSTS with max-age of at least 31536000 and includeSubDomains'
  'X-Content-Type-Options[[:space:]]*:[[:space:]]*nosniff|low|CH-006|Good: X-Content-Type-Options nosniff is set|Keep X-Content-Type-Options: nosniff to prevent MIME sniffing'
  'Content-Security-Policy|low|CH-007|CSP header check -- ensure a strict policy is defined|Define restrictive CSP that limits script sources and prevents XSS'
  'max-age[[:space:]]*=[[:space:]]*0|medium|CH-008|Cache max-age=0 forces revalidation on every request|Set appropriate max-age for static assets to improve performance'
  'Vary[[:space:]]*:[[:space:]]*\*|medium|CH-009|Vary: * prevents all caching|Use specific Vary header values like Accept, Accept-Encoding'
  'ETag[[:space:]]*:[[:space:]]*W/|low|CH-010|Weak ETags are fine for most use cases|Weak ETags are acceptable; use strong ETags only if byte-range accuracy needed'
  'Expires[[:space:]]*:[[:space:]]*-1|low|CH-011|Expires: -1 is non-standard for disabling cache|Use Cache-Control: no-store instead of Expires: -1'
  'res\.set\([[:space:]]*["\x27]Cache-Control|low|CH-012|Manual cache header management -- consider middleware|Use cache-control middleware for consistent cache policy'
  'cdn[[:space:]]*=[[:space:]]*["\x27]http://|high|CH-013|CDN configured over insecure HTTP|Use HTTPS for CDN resources to ensure integrity and security'
  'X-XSS-Protection[[:space:]]*:[[:space:]]*0|medium|CH-014|XSS Protection header disabled|Remove X-XSS-Protection entirely; rely on CSP instead'
  'Referrer-Policy|low|CH-015|Check Referrer-Policy is set appropriately|Set Referrer-Policy to strict-origin-when-cross-origin or no-referrer'
)

# ===========================================================================
# RH -- Request Handling (15 patterns: RH-001 to RH-015)
# Team tier
# ===========================================================================

declare -a HTTPLINT_RH_PATTERNS=(
  'req\.body\.[[:alnum:]]+[[:space:]]*[^=!<>]|medium|RH-001|Using request body fields without validation|Validate and sanitize all request body inputs before use'
  'req\.query\.[[:alnum:]]|medium|RH-002|Using query parameters without validation|Validate and sanitize query parameters before processing'
  'req\.params\.[[:alnum:]]|medium|RH-003|Using route parameters without validation|Validate route parameters with type checks and bounds'
  'parseInt\([[:space:]]*req\.|medium|RH-004|Parsing request input without radix or error handling|Use parseInt with radix 10 and validate NaN results'
  'JSON\.parse\([[:space:]]*req\.|high|RH-005|Parsing request data without try/catch|Wrap JSON.parse in try/catch for malformed input handling'
  'eval\([[:space:]]*req\.|critical|RH-006|Evaluating user input is a code injection vulnerability|Never eval user input; use safe parsing alternatives'
  'req\.headers\.[[:alnum:]]|low|RH-007|Accessing headers without case normalization|Normalize header names to lowercase for consistency'
  'multer\([[:space:]]*{|low|RH-008|File upload middleware needs size and type limits|Configure fileSize limit and fileFilter in multer options'
  'req\.ip|low|RH-009|Client IP may be spoofed behind proxies|Use req.ip with trust proxy configured, or validate X-Forwarded-For'
  'Content-Length[^:]|medium|RH-010|Check Content-Length handling for request smuggling|Validate Content-Length matches actual body size'
  'Transfer-Encoding|medium|RH-011|Transfer-Encoding needs careful handling to prevent smuggling|Ensure consistent Transfer-Encoding handling between proxy and server'
  'req\.url|low|RH-012|Raw URL access without parsing or sanitization|Use URL parsing library to safely extract path and parameters'
  'res\.redirect\([[:space:]]*301|low|RH-013|Permanent redirect (301) is cached by browsers permanently|Use 302 or 307 for temporary redirects; reserve 301 for truly permanent moves'
  'encodeURIComponent\([[:space:]]*req\.|low|RH-014|Encoding user input before use -- good practice|Continue encoding user inputs in URLs and HTML contexts'
  'req\.rawBody|medium|RH-015|Raw body access without size validation|Enforce body size limits before processing raw request bodies'
)

# ===========================================================================
# ER -- Error & Response (15 patterns: ER-001 to ER-015)
# Team tier
# ===========================================================================

declare -a HTTPLINT_ER_PATTERNS=(
  'stack[[:space:]]*:[[:space:]]*err\.|critical|ER-001|Stack trace exposed in HTTP response|Never include stack traces in production responses'
  'res\.status\(200\)\.json\([[:space:]]*{[[:space:]]*error|high|ER-002|Returning 200 status for error responses|Use appropriate 4xx/5xx status codes for error responses'
  'res\.send\([[:space:]]*err\.message|high|ER-003|Sending raw error message to client|Return generic error messages; log details server-side'
  'res\.status\(500\)\.send\([[:space:]]*["\x27]Internal|medium|ER-004|Generic 500 error without correlation ID|Include a request ID in error responses for debugging'
  'catch\([[:space:]]*e\)[[:space:]]*{[[:space:]]*}|critical|ER-005|Empty catch block silently swallows errors|Log or handle errors in catch blocks; never swallow silently'
  'console\.error\([[:space:]]*e\)|low|ER-006|Using console.error for server error logging|Use structured logger (winston, pino) instead of console for production'
  'res\.sendStatus\(200\)|low|ER-007|sendStatus returns status text as body; may confuse clients|Use res.status(200).json() for structured responses'
  'next\([[:space:]]*err\)|low|ER-008|Error forwarded to Express error handler -- good pattern|Ensure a centralized error handler middleware is configured'
  'process\.exit\([[:space:]]*1\)|high|ER-009|Process exit on error kills all connections abruptly|Use graceful shutdown with connection draining'
  'res\.json\([[:space:]]*null\)|medium|ER-010|Responding with null body is ambiguous|Return an empty object or appropriate error response'
  'throw[[:space:]]+new[[:space:]]+Error\([[:space:]]*req\.|high|ER-011|Throwing error with user input may expose data in logs|Sanitize user input before including in error messages'
  'res\.set\([[:space:]]*["\x27]Content-Type["\x27].*text/plain|low|ER-012|Text/plain content-type for API response|Use application/json for API responses for proper client parsing'
  'res\.status\(404\)\.send\([[:space:]]*["\x27]Not[[:space:]]*Found|low|ER-013|Generic 404 response without helpful context|Include available resource suggestions or documentation link'
  'unhandledRejection|medium|ER-014|Unhandled promise rejection handler needed|Add process.on unhandledRejection handler for graceful error management'
  'res\.writeHead\([[:space:]]*200|low|ER-015|Using writeHead instead of response helpers|Use framework response methods for consistent header management'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
httplint_pattern_count() {
  local count=0
  count=$((count + ${#HTTPLINT_HC_PATTERNS[@]}))
  count=$((count + ${#HTTPLINT_HS_PATTERNS[@]}))
  count=$((count + ${#HTTPLINT_CK_PATTERNS[@]}))
  count=$((count + ${#HTTPLINT_CH_PATTERNS[@]}))
  count=$((count + ${#HTTPLINT_RH_PATTERNS[@]}))
  count=$((count + ${#HTTPLINT_ER_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
httplint_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_httplint_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_httplint_patterns_for_category() {
  local category="$1"
  case "$category" in
    HC|hc) echo "HTTPLINT_HC_PATTERNS" ;;
    HS|hs) echo "HTTPLINT_HS_PATTERNS" ;;
    CK|ck) echo "HTTPLINT_CK_PATTERNS" ;;
    CH|ch) echo "HTTPLINT_CH_PATTERNS" ;;
    RH|rh) echo "HTTPLINT_RH_PATTERNS" ;;
    ER|er) echo "HTTPLINT_ER_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_httplint_category_label() {
  local category="$1"
  case "$category" in
    HC|hc) echo "HTTP Client" ;;
    HS|hs) echo "HTTP Server" ;;
    CK|ck) echo "Cookie & Session" ;;
    CH|ch) echo "Caching & Headers" ;;
    RH|rh) echo "Request Handling" ;;
    ER|er) echo "Error & Response" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_httplint_categories() {
  echo "HC HS CK CH RH ER"
}

# Get categories available for a given tier level
# free=0 -> HC, HS (30 patterns)
# pro=1  -> HC, HS, CK, CH (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_httplint_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "HC HS CK CH RH ER"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "HC HS CK CH"
  else
    echo "HC HS"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
httplint_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in HC HS CK CH RH ER; do
      httplint_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_httplint_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_httplint_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_httplint_category() {
  local category="$1"
  case "$category" in
    HC|hc|HS|hs|CK|ck|CH|ch|RH|rh|ER|er) return 0 ;;
    *) return 1 ;;
  esac
}
