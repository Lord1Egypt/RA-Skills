#!/usr/bin/env bash
# LogSentry -- Logging Quality Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Immediate security risk (sensitive data exposure, injection)
#   high     -- Significant quality/security problem requiring prompt attention
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   SL (Structured Logging)    -- 15 patterns (SL-001 to SL-015)
#   LL (Log Levels)            -- 15 patterns (LL-001 to LL-015)
#   SD (Sensitive Data)        -- 15 patterns (SD-001 to SD-015)
#   LI (Log Injection)         -- 15 patterns (LI-001 to LI-015)
#   CI (Correlation & Context) -- 15 patterns (CI-001 to CI-015)
#   OB (Observability)         -- 15 patterns (OB-001 to OB-015)

set -euo pipefail

# ============================================================================
# 1. STRUCTURED LOGGING (SL-001 through SL-015)
#    Detects missing structured logging, print/println instead of loggers,
#    string concatenation in log messages, missing log context/fields.
# ============================================================================

declare -a LOGSENTRY_SL_PATTERNS=()

LOGSENTRY_SL_PATTERNS+=(
  # SL-001: Java System.out.println used instead of logger
  'System\.out\.print(ln)?\(|high|SL-001|System.out.println used instead of structured logger|Replace with SLF4J/Log4j logger call (e.g., logger.info(...)) for structured output'

  # SL-002: Java System.err.println used instead of logger
  'System\.err\.print(ln)?\(|high|SL-002|System.err.println used instead of structured logger|Replace with logger.error(...) for structured error output'

  # SL-003: console.log used in production code (JS/TS)
  'console\.log\(|medium|SL-003|console.log used instead of structured logger|Replace with a structured logger (winston, pino, bunyan) for production code'

  # SL-004: console.error used in production code (JS/TS)
  'console\.error\(|medium|SL-004|console.error used instead of structured logger|Replace with logger.error(...) from a structured logging library'

  # SL-005: String concatenation in Java/JS logger.info call
  'logger\.info\([[:space:]]*"[^"]*"[[:space:]]*\+|high|SL-005|String concatenation in logger.info() instead of parameterized message|Use parameterized logging: logger.info("User {} logged in", userId)'

  # SL-006: String concatenation in logger.error call
  'logger\.error\([[:space:]]*"[^"]*"[[:space:]]*\+|high|SL-006|String concatenation in logger.error() instead of parameterized message|Use parameterized logging: logger.error("Failed for user {}", userId, ex)'

  # SL-007: String concatenation in logger.debug call
  'logger\.debug\([[:space:]]*"[^"]*"[[:space:]]*\+|high|SL-007|String concatenation in logger.debug() instead of parameterized message|Use parameterized logging: logger.debug("Processing item {}", itemId)'

  # SL-008: String concatenation in logger.warn call
  'logger\.warn\([[:space:]]*"[^"]*"[[:space:]]*\+|high|SL-008|String concatenation in logger.warn() instead of parameterized message|Use parameterized logging: logger.warn("Slow query {} ms", duration)'

  # SL-009: Python f-string in logging call
  'logging\.info\([[:space:]]*f"|high|SL-009|Python f-string in logging.info() causes unnecessary string interpolation|Use lazy formatting: logging.info("User %s logged in", user_id)'

  # SL-010: Python f-string in logging.error call
  'logging\.error\([[:space:]]*f"|high|SL-010|Python f-string in logging.error() causes unnecessary string interpolation|Use lazy formatting: logging.error("Failed: %s", error_msg)'

  # SL-011: Python f-string in logging.warning call
  'logging\.warning\([[:space:]]*f"|high|SL-011|Python f-string in logging.warning() causes unnecessary interpolation|Use lazy formatting: logging.warning("Slow query: %s ms", duration)'

  # SL-012: Go fmt.Println used instead of structured logger
  'fmt\.Println\(|medium|SL-012|Go fmt.Println used instead of structured logger|Replace with zap, zerolog, or logrus for structured production logging'

  # SL-013: Go fmt.Printf used instead of structured logger
  'fmt\.Printf\(|medium|SL-013|Go fmt.Printf used instead of structured logger|Replace with zap.Logger or zerolog with structured fields'

  # SL-014: C# Console.WriteLine used instead of ILogger
  'Console\.WriteLine\(|medium|SL-014|C# Console.WriteLine used instead of ILogger|Replace with ILogger injection and Serilog or NLog for structured logging'

  # SL-015: Ruby puts used for logging
  'puts[[:space:]]+"[[:space:]]*[A-Z]{3,8}[[:space:]:]|medium|SL-015|Ruby puts used with log-level prefix instead of Logger|Replace with Rails.logger or Ruby Logger class for structured output'
)

# ============================================================================
# 2. LOG LEVELS (LL-001 through LL-015)
#    Detects incorrect log level usage, debug in production paths, missing
#    error-level for exceptions, inconsistent level patterns.
# ============================================================================

declare -a LOGSENTRY_LL_PATTERNS=()

LOGSENTRY_LL_PATTERNS+=(
  # LL-001: Error/exception logged at debug level
  'logger\.debug\(.*[Ee]rror|high|LL-001|Error condition logged at debug level instead of error|Raise log level to error for error conditions: logger.error("...", error)'

  # LL-002: Exception logged at debug level
  'logger\.debug\(.*[Ee]xception|high|LL-002|Exception logged at debug level instead of error|Log exceptions at error level: logger.error("Operation failed", exception)'

  # LL-003: Exception/stack trace logged at info level
  'logger\.info\(.*[Ee]xception|high|LL-003|Exception logged at info level instead of error|Log exceptions at error level: logger.error("Operation failed", exception)'

  # LL-004: Payment/billing event at debug level
  'logger\.debug\(.*[Pp]ayment|medium|LL-004|Payment event logged at debug level|Raise to info or higher for audit trail: logger.info("Payment processed")'

  # LL-005: Authentication event at debug level
  'logger\.debug\(.*[Aa]uthenticat|medium|LL-005|Authentication event logged at debug level|Raise to info for security audit trail: logger.info("User authenticated")'

  # LL-006: Security access denial at info level
  'logger\.info\(.*[Uu]nauthorized|high|LL-006|Unauthorized access logged at info level instead of warn/error|Log security denials at warn or error: logger.warn("Unauthorized access attempt")'

  # LL-007: Access denied logged at debug level
  'logger\.debug\(.*[Aa]ccess[[:space:]]denied|high|LL-007|Access denied event logged at debug level|Log security events at warn or error level for alerting'

  # LL-008: Fatal/critical used for recoverable condition
  'logger\.fatal\(.*[Rr]etry|medium|LL-008|Fatal level used for retryable condition|Use warn or error for recoverable situations; reserve fatal for unrecoverable crashes'

  # LL-009: Database error at warn instead of error
  'logger\.warn\(.*[Dd]atabase[[:space:]]error|medium|LL-009|Database error logged at warn level instead of error|Log database errors at error level: logger.error("Database query failed")'

  # LL-010: Timeout event logged at info or debug level
  'logger\.info\(.*[Tt]imeout|medium|LL-010|Timeout event logged at info level instead of warn/error|Log timeouts at warn or error level for operational alerting'

  # LL-011: Connection error at info
  'logger\.info\(.*[Cc]onnection[[:space:]]refused|medium|LL-011|Connection refused logged at info level|Log connection errors at warn or error for operational alerting'

  # LL-012: Configuration error at debug
  'logger\.debug\(.*[Cc]onfig.*error|medium|LL-012|Configuration error logged at debug level|Log configuration errors at warn or error level'

  # LL-013: Deprecation warning at trace/debug
  'logger\.debug\(.*[Dd]eprecat|low|LL-013|Deprecation notice logged at debug level|Log deprecation warnings at warn level for visibility'

  # LL-014: Startup event at debug level
  'logger\.debug\(.*[Ss]erver[[:space:]]start|low|LL-014|Server startup logged at debug level|Log lifecycle events at info level for operational visibility'

  # LL-015: Shutdown event at debug level
  'logger\.debug\(.*[Ss]hutdown|low|LL-015|Shutdown event logged at debug level|Log lifecycle events at info level for operational visibility'
)

# ============================================================================
# 3. SENSITIVE DATA (SD-001 through SD-015)
#    Detects passwords, tokens, PII, credit cards, SSNs, emails in log
#    output, logging full request bodies, and other sensitive data exposure.
# ============================================================================

declare -a LOGSENTRY_SD_PATTERNS=()

LOGSENTRY_SD_PATTERNS+=(
  # SD-001: Password value logged via logger
  'logger\.[a-z]+\(.*[Pp]assword[[:space:]]*[:=]|critical|SD-001|Password value being written to log output|Never log password values; remove password from log statement entirely'

  # SD-002: API key/token logged
  'logger\.[a-z]+\(.*api[_-]?[Kk]ey[[:space:]]*[:=]|critical|SD-002|API key value being written to log output|Never log API keys; mask or omit from log statements'

  # SD-003: Authorization header logged
  'logger\.[a-z]+\(.*[Aa]uthoriz|critical|SD-003|Authorization header being written to log output|Never log authorization headers; they contain bearer tokens or credentials'

  # SD-004: Credit card number pattern in log
  'logger\.[a-z]+\(.*[0-9]{4}[[:space:]-][0-9]{4}[[:space:]-][0-9]{4}[[:space:]-][0-9]{4}|critical|SD-004|Credit card number pattern detected in log statement|Never log credit card numbers; mask all but last 4 digits at most'

  # SD-005: SSN pattern in log
  'logger\.[a-z]+\(.*[0-9]{3}-[0-9]{2}-[0-9]{4}|critical|SD-005|Social Security Number pattern detected in log statement|Never log SSNs; completely remove from all log output'

  # SD-006: Email address logged
  'logger\.[a-z]+\(.*[Ee]mail[[:space:]]*[:=]|high|SD-006|Email address being written to log output|Mask or hash email addresses in logs to protect PII'

  # SD-007: Full request body logged
  'logger\.[a-z]+\(.*req(uest)?\.body|high|SD-007|Full HTTP request body being logged (may contain PII or secrets)|Log only necessary fields from request body; never log entire body in production'

  # SD-008: Full response body logged
  'logger\.[a-z]+\(.*res(ponse)?\.body|medium|SD-008|Full HTTP response body being logged|Log only status codes and metadata, not full response bodies'

  # SD-009: Session ID/cookie logged
  'logger\.[a-z]+\(.*[Ss]ession[_-]?[Ii]d|high|SD-009|Session ID value being logged|Never log session IDs; they enable session hijacking if exposed'

  # SD-010: Access token in log
  'logger\.[a-z]+\(.*[Aa]ccess[_-]?[Tt]oken|critical|SD-010|Access token being written to log output|Never log access tokens; mask or omit from log statements'

  # SD-011: Private key material in log
  'logger\.[a-z]+\(.*[Pp]rivate[_-]?[Kk]ey|critical|SD-011|Private key reference being written to log output|Never log key material; completely remove from all log output'

  # SD-012: Secret key in log
  'logger\.[a-z]+\(.*[Ss]ecret[_-]?[Kk]ey|critical|SD-012|Secret key being written to log output|Never log secret keys; completely remove from all log output'

  # SD-013: Connection string in log
  'logger\.[a-z]+\(.*[Cc]onnection[_-]?[Ss]tring|high|SD-013|Database connection string being logged (may contain credentials)|Sanitize connection strings before logging; remove embedded credentials'

  # SD-014: Phone number in log
  'logger\.[a-z]+\(.*[Pp]hone[[:space:]]*[:=]|high|SD-014|Phone number being logged|Mask phone numbers in logs to protect PII'

  # SD-015: JSON.stringify of full object in log (may contain secrets)
  'logger\.[a-z]+\(.*JSON\.stringify\(|high|SD-015|JSON.stringify of entire object in log (may expose sensitive fields)|Log only specific fields; use a safe serializer that strips sensitive keys'
)

# ============================================================================
# 4. LOG INJECTION (LI-001 through LI-015)
#    Detects unsanitized user input in logs, newline injection, CRLF in
#    log messages, format string vulnerabilities in logging.
# ============================================================================

declare -a LOGSENTRY_LI_PATTERNS=()

LOGSENTRY_LI_PATTERNS+=(
  # LI-001: Direct request parameter in log message
  'logger\.[a-z]+\(.*req\.param\[|critical|LI-001|User-controlled request parameter directly in log statement (injection risk)|Sanitize all user input before logging; strip newlines and control characters'

  # LI-002: Request query value logged directly
  'logger\.[a-z]+\(.*req\.query\[|critical|LI-002|User-controlled query parameter directly in log statement (injection risk)|Sanitize query parameters before logging; strip control characters'

  # LI-003: Request header value logged directly
  'logger\.[a-z]+\(.*req(uest)?\.headers?\[|high|LI-003|HTTP header value logged directly without sanitization|Sanitize header values before logging; headers can contain injection payloads'

  # LI-004: Request body field logged with concatenation
  'logger\.[a-z]+\(.*"[[:space:]]*\+[[:space:]]*req\.body|high|LI-004|Request body value concatenated into log message|Use parameterized logging for request data; sanitize before logging'

  # LI-005: User agent logged without sanitization
  'logger\.[a-z]+\(.*[Uu]ser[_-]?[Aa]gent|medium|LI-005|User-Agent header logged (user-controlled input, injection risk)|Sanitize User-Agent before logging; it is user-controlled'

  # LI-006: Format string with request data
  'String\.format\(.*req|high|LI-006|String.format used with request data (format string injection risk)|Use parameterized logging instead of String.format with user data'

  # LI-007: Newline literal in log message construction
  'logger\.[a-z]+\(.*\\\\n.*\+|high|LI-007|Newline character in log message with concatenation (log forging risk)|Remove literal newlines from log messages; use structured fields for multiline data'

  # LI-008: Carriage return in log construction
  'logger\.[a-z]+\(.*\\\\r|critical|LI-008|Carriage return in log message (CRLF injection / log forging)|Strip carriage returns from all logged values to prevent log forging attacks'

  # LI-009: getParameter value in log (Java)
  'logger\.[a-z]+\(.*getParameter\(|high|LI-009|Request parameter from getParameter() logged directly (injection risk)|Sanitize getParameter() values before logging to prevent log injection'

  # LI-010: Python os.environ value in log
  'logging\.[a-z]+\(.*os\.environ|medium|LI-010|Environment variable value logged directly (may contain user-controlled content)|Validate and sanitize environment values before logging'

  # LI-011: Command line argument in log
  'logger\.[a-z]+\(.*argv|medium|LI-011|Command-line argument value logged directly|Sanitize CLI arguments before logging to prevent log injection'

  # LI-012: Exception message concatenated into log
  'logger\.[a-z]+\(.*\+[[:space:]]*[a-zA-Z_]*[Ee]x(ception)?\.getMessage|medium|LI-012|Exception message concatenated into log (may contain user input)|Use structured logging for exceptions; pass exception as parameter not via concat'

  # LI-013: Search query or regex input logged
  'logger\.[a-z]+\(.*[Ss]earch[_-]?[Qq]uery|low|LI-013|Search query logged (user-controlled input)|Sanitize search queries before logging to prevent log injection'

  # LI-014: Filename from user input in log
  'logger\.[a-z]+\(.*[Ff]ile[Nn]ame[[:space:]]*[:=]|medium|LI-014|User-provided filename logged directly (path traversal or injection risk)|Sanitize filenames before logging; strip path separators and control characters'

  # LI-015: Form data logged via POST parameter
  'logger\.[a-z]+\(.*POST\[|high|LI-015|POST form data logged directly without sanitization|Sanitize and validate form data before logging'
)

# ============================================================================
# 5. CORRELATION & CONTEXT (CI-001 through CI-015)
#    Detects missing request IDs, trace IDs, correlation IDs, structured
#    context, and inconsistent timestamp formats.
# ============================================================================

declare -a LOGSENTRY_CI_PATTERNS=()

LOGSENTRY_CI_PATTERNS+=(
  # CI-001: Logger call with plain string and no structured context
  'logger\.info\([[:space:]]*"[A-Za-z ]+"\)|low|CI-001|Logger.info call with plain string and no structured context fields|Add structured fields: logger.info("msg", { key: value }) for searchability'

  # CI-002: Logger.debug with plain string and no context
  'logger\.debug\([[:space:]]*"[A-Za-z ]+"\)|low|CI-002|Logger.debug call with plain string and no structured context fields|Add structured fields: logger.debug("msg", { requestId, userId })'

  # CI-003: Logger.error with plain string and no context
  'logger\.error\([[:space:]]*"[A-Za-z ]+"\)|low|CI-003|Logger.error call with plain string and no structured context fields|Add structured fields: logger.error("msg", { error, requestId })'

  # CI-004: Logger.warn with plain string and no context
  'logger\.warn\([[:space:]]*"[A-Za-z ]+"\)|low|CI-004|Logger.warn call with plain string and no structured context fields|Add structured fields: logger.warn("msg", { key: value })'

  # CI-005: Python logging without extra context dict
  'logging\.info\([[:space:]]*"[^%]*"[[:space:]]*\)|low|CI-005|Python logging.info without extra context or format args|Add extra context: logging.info("msg", extra={"key": value})'

  # CI-006: Python logging.error without extra context
  'logging\.error\([[:space:]]*"[^%]*"[[:space:]]*\)|low|CI-006|Python logging.error without extra context or format args|Add extra context: logging.error("msg", extra={"requestId": req_id})'

  # CI-007: Go standard log.Println (no structured fields)
  'log\.Println\(|medium|CI-007|Go standard log.Println used (no structured fields support)|Use zap or zerolog with structured fields for correlation support'

  # CI-008: Go standard log.Printf (no structured fields)
  'log\.Printf\(|medium|CI-008|Go standard log.Printf used (no structured fields support)|Use zap or zerolog with structured fields for correlation support'

  # CI-009: Manual timestamp prepended to log message
  'logger\.[a-z]+\([[:space:]]*".*"[[:space:]]*\+[[:space:]]*new Date|low|CI-009|Manual timestamp prepended to log message instead of using logger timestamp|Let the logging framework handle timestamps via its configuration'

  # CI-010: Non-ISO timestamp format in log (toString)
  'new Date\(\)\.toString\(\).*logger|medium|CI-010|Non-ISO timestamp format used near logging (toString)|Use ISO 8601 format (toISOString()) for consistent, parseable timestamps'

  # CI-011: Date.now used in log string
  'logger\.[a-z]+\(.*Date\.now\(\)|low|CI-011|Date.now() used in log string (millisecond timestamp, not human-readable)|Use ISO 8601 formatted timestamps for log messages'

  # CI-012: Java logger without MDC for processing events
  'logger\.info\([[:space:]]*"Processing[^"]*"[[:space:]]*\)|low|CI-012|Logger call for processing event without MDC or structured context|Add MDC context: MDC.put("requestId", id) before logging processing events'

  # CI-013: Logger call for "Handling" event without context
  'logger\.info\([[:space:]]*"Handling[^"]*"[[:space:]]*\)|low|CI-013|Logger call for handling event without structured context|Add structured context to handler logs for request traceability'

  # CI-014: Logger call for "Received" event without context
  'logger\.info\([[:space:]]*"Received[^"]*"[[:space:]]*\)|low|CI-014|Logger call for received event without structured context|Include message ID and source in received event logs'

  # CI-015: Hardcoded timestamp pattern in log message code
  '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}.*logger\.|low|CI-015|Hardcoded timestamp pattern near logging call (possible duplicate timestamp)|Rely on logging framework for timestamps; remove manual timestamp from message'
)

# ============================================================================
# 6. OBSERVABILITY (OB-001 through OB-015)
#    Detects missing metrics emission, no health check logging, missing
#    audit trail events, and absent error rate tracking.
# ============================================================================

declare -a LOGSENTRY_OB_PATTERNS=()

LOGSENTRY_OB_PATTERNS+=(
  # OB-001: Error handler logs but no metric counter
  'catch.*logger\.error\(|medium|OB-001|Error handler logs error but does not emit error count metric|Add error counter metric emission alongside error logging'

  # OB-002: Exception catch with only console.error (no metrics)
  'catch.*console\.error\(|medium|OB-002|Exception caught with console.error but no metric emission|Add structured error logging with error classification and metrics'

  # OB-003: Authentication function without audit logging
  'authenticate.*return[[:space:]]|medium|OB-003|Authentication function without audit log event|Add audit logging for all authentication attempts (success and failure)'

  # OB-004: Login handler without logging
  'login.*return[[:space:]]|medium|OB-004|Login handler without audit log event|Log all login attempts with outcome for security audit trail'

  # OB-005: Authorization check without logging
  'checkPermission.*return[[:space:]]|medium|OB-005|Authorization check without audit log event|Log authorization decisions for security audit trail'

  # OB-006: Delete operation without audit log
  'delete.*\{[^}]*return|low|OB-006|Data deletion operation without audit trail logging|Add audit logging before and after data deletion operations'

  # OB-007: Retry logic log without attempt number
  'retry.*logger\.debug\([[:space:]]*"|low|OB-007|Retry logic logs without including attempt number or max retries|Include attempt number and max retries in retry log messages'

  # OB-008: Circuit breaker state change reference
  'circuitBreaker\.open|medium|OB-008|Circuit breaker state change without explicit state logging|Log circuit breaker state transitions with current state and metrics'

  # OB-009: Rate limiter triggered without logging
  'rateLimi.*return|low|OB-009|Rate limiter triggered without logging the event|Log rate limit hits with client identifier for monitoring and alerting'

  # OB-010: Health check endpoint without logging
  'healthz.*res\.send|low|OB-010|Health check endpoint without logging health status|Add structured logging to health checks for monitoring visibility'

  # OB-011: Health check with json response but no logging
  'health.*res\.json\(|low|OB-011|Health check response without logging|Log health check results for monitoring dashboard integration'

  # OB-012: Migration operation without logging
  'migrate.*\{.*return|low|OB-012|Migration operation without audit logging|Log migration start, completion, and any errors for operational awareness'

  # OB-013: Background job without duration logging
  'worker\.process\(.*\{|low|OB-013|Background job handler without execution duration logging|Add start time tracking and log total job duration on completion'

  # OB-014: API response without status logging
  'res\.send\(.*\)[[:space:]]*;[[:space:]]*$|low|OB-014|API response sent without logging the response status code|Log response status code and latency for API observability'

  # OB-015: WebSocket event without connection tracking
  'ws\.on\([[:space:]]*["\x27]connection|low|OB-015|WebSocket connection event without connection tracking log|Log WebSocket connection lifecycle events with connection IDs'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
logsentry_pattern_count() {
  local count=0
  count=$((count + ${#LOGSENTRY_SL_PATTERNS[@]}))
  count=$((count + ${#LOGSENTRY_LL_PATTERNS[@]}))
  count=$((count + ${#LOGSENTRY_SD_PATTERNS[@]}))
  count=$((count + ${#LOGSENTRY_LI_PATTERNS[@]}))
  count=$((count + ${#LOGSENTRY_CI_PATTERNS[@]}))
  count=$((count + ${#LOGSENTRY_OB_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
logsentry_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_logsentry_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_logsentry_patterns_for_category() {
  local category="$1"
  case "$category" in
    SL|sl) echo "LOGSENTRY_SL_PATTERNS" ;;
    LL|ll) echo "LOGSENTRY_LL_PATTERNS" ;;
    SD|sd) echo "LOGSENTRY_SD_PATTERNS" ;;
    LI|li) echo "LOGSENTRY_LI_PATTERNS" ;;
    CI|ci) echo "LOGSENTRY_CI_PATTERNS" ;;
    OB|ob) echo "LOGSENTRY_OB_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_logsentry_category_label() {
  local category="$1"
  case "$category" in
    SL|sl) echo "Structured Logging" ;;
    LL|ll) echo "Log Levels" ;;
    SD|sd) echo "Sensitive Data" ;;
    LI|li) echo "Log Injection" ;;
    CI|ci) echo "Correlation & Context" ;;
    OB|ob) echo "Observability" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_logsentry_categories() {
  echo "SL LL SD LI CI OB"
}

# Get categories available for a given tier level
# free=0 -> SL, LL (30 patterns)
# pro=1  -> SL, LL, SD, LI (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_logsentry_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "SL LL SD LI CI OB"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "SL LL SD LI"
  else
    echo "SL LL"
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
logsentry_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in SL LL SD LI CI OB; do
      logsentry_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_logsentry_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_logsentry_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_logsentry_category() {
  local category="$1"
  case "$category" in
    SL|sl|LL|ll|SD|sd|LI|li|CI|ci|OB|ob) return 0 ;;
    *) return 1 ;;
  esac
}
