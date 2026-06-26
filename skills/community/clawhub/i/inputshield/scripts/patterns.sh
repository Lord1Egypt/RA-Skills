#!/usr/bin/env bash
# InputShield -- Vulnerability Detection Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# 90 patterns across 6 categories (15 each):
#   IV -- Input Validation (IV-001 to IV-015)
#   DS -- Deserialization  (DS-001 to DS-015)
#   RD -- ReDoS            (RD-001 to RD-015)
#   PT -- Path Traversal   (PT-001 to PT-015)
#   CI -- Command Injection(CI-001 to CI-015)
#   XS -- XSS / Output     (XS-001 to XS-015)
#
# Severity levels:
#   critical -- Directly exploitable, allows RCE, injection, or data exfiltration
#   high     -- Serious security risk requiring prompt remediation
#   medium   -- Potential vulnerability needing review and context
#   low      -- Informational, possible false positive, style issue
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \b, etc.)
# - Character classes use POSIX bracket expressions
# - Alternation uses | (pipe)
# - Grouping uses ( ) (parentheses)
# - Quantifiers: ?, *, +, {n,m}

set -euo pipefail

# ============================================================================
# 1. INPUT VALIDATION (IV-001 through IV-015)
#    Missing length checks, absent type validation, raw user input acceptance,
#    missing allowlist, absent boundary checks, and related issues.
# ============================================================================

declare -a INPUTSHIELD_IV_PATTERNS=()

INPUTSHIELD_IV_PATTERNS+=(
  # IV-001: Request body accessed directly without any validation or length check
  'req\.body\.[a-zA-Z_]+[[:space:]]*[^=!<>]|high|IV-001|Request body field accessed without validation|Validate req.body fields with a schema validator (Joi, Zod, express-validator) before use'

  # IV-002: Request query parameters used directly
  'req\.query\.[a-zA-Z_]+[[:space:]]*[^=!<>]|high|IV-002|Query parameter accessed without validation|Validate and sanitize query parameters before use; check types, length, and allowed values'

  # IV-003: Request params accessed without validation
  'req\.params\.[a-zA-Z_]+[[:space:]]*[^=!<>]|medium|IV-003|Route parameter accessed without validation|Validate route params with express-validator or a schema library'

  # IV-004: parseInt/parseFloat without radix or NaN check
  'parseInt[[:space:]]*\([^,)]*\)[[:space:]]*[^;]*[^N]|medium|IV-004|parseInt called without NaN check or radix parameter|Use parseInt(value, 10) and check for isNaN() before using the result'

  # IV-005: Direct use of request headers without validation
  'req\.headers\[[^]]*\]|medium|IV-005|Request header accessed directly without validation|Validate and sanitize request headers; never trust client-provided header values'

  # IV-006: User input directly used in array index
  '\[[[:space:]]*(req\.|request\.|params\.|query\.|body\.)|high|IV-006|User-controlled value used as array index without bounds checking|Validate array indices are within bounds before access; check for negative values'

  # IV-007: Type coercion without explicit check (==  instead of ===)
  '[^!=]=[[:space:]]*req\.(body|query|params)|medium|IV-007|User input assigned without type checking|Use strict equality (===) and explicit type validation for all user inputs'

  # IV-008: Missing Content-Type validation on file upload
  'upload|multer|formidable|busboy|multipart|medium|IV-008|File upload handler without visible Content-Type validation|Validate file MIME types, extensions, and sizes; use allowlists for accepted types'

  # IV-009: URL parameter used in redirect without validation
  'redirect[[:space:]]*\([[:space:]]*(req\.|request\.)|critical|IV-009|User input used directly in redirect without validation|Validate redirect URLs against an allowlist; never redirect to user-supplied URLs blindly'

  # IV-010: No length check on string input
  '(body|query|params)\.[a-zA-Z_]+\.length[[:space:]]*[^><!]|low|IV-010|String input accessed without length validation|Check .length against maximum bounds before processing string inputs'

  # IV-011: Django/Flask request data without validation
  'request\.(GET|POST|data|args|form|json)\[|high|IV-011|Web framework request data accessed without validation|Validate all request.GET/POST/data values with Django forms or marshmallow schemas'

  # IV-012: Spring @RequestParam without validation annotation
  '@RequestParam[[:space:]]*[^@]*[[:space:]]String[[:space:]]|medium|IV-012|Spring @RequestParam without @Valid or @Size annotation|Add @Valid, @Size, @Pattern annotations to validate request parameters'

  # IV-013: Express route without express-validator or Joi
  'app\.(get|post|put|delete|patch)[[:space:]]*\([[:space:]]*['"'"'"][^'"'"'"]*['"'"'"][[:space:]]*,[[:space:]]*\(?[[:space:]]*(req|ctx)|medium|IV-013|Express route handler without visible input validation middleware|Add express-validator or Joi validation middleware before the route handler'

  # IV-014: User input used in database query without parameterization
  '\.(find|findOne|findMany|where)\([[:space:]]*\{[^}]*(req\.|request\.)|high|IV-014|User input used directly in database query object|Use parameterized queries or ORM-level validation; never pass raw user input to queries'

  # IV-015: Missing CSRF token validation
  'csrf|csrfToken|_csrf|low|IV-015|CSRF token reference found -- verify CSRF protection is properly enforced|Ensure CSRF tokens are validated on all state-changing requests; use framework CSRF middleware'
)

# ============================================================================
# 2. DESERIALIZATION (DS-001 through DS-015)
#    Unsafe deserialization, unvalidated parsing, and unmarshaling risks.
# ============================================================================

declare -a INPUTSHIELD_DS_PATTERNS=()

INPUTSHIELD_DS_PATTERNS+=(
  # DS-001: JSON.parse without try-catch
  'JSON\.parse[[:space:]]*\([[:space:]]*(req\.|request\.|body|input|data|params|args)|critical|DS-001|JSON.parse on untrusted input without error handling|Wrap JSON.parse in try-catch; validate the parsed structure against a schema'

  # DS-002: Python pickle.loads on potentially untrusted data
  'pickle\.(loads|load)[[:space:]]*\(|critical|DS-002|pickle.loads/load used -- unsafe deserialization of untrusted data|Never use pickle on untrusted data; use json.loads() or a safe serialization format'

  # DS-003: yaml.load without SafeLoader
  'yaml\.load[[:space:]]*\([^)]*\)[[:space:]]*$|critical|DS-003|yaml.load called without Loader=SafeLoader -- allows arbitrary code execution|Use yaml.safe_load() or yaml.load(data, Loader=yaml.SafeLoader)'

  # DS-004: Java ObjectInputStream -- deserialization from stream
  'ObjectInputStream[[:space:]]*\(|critical|DS-004|Java ObjectInputStream used -- vulnerable to deserialization attacks|Use allowlist-based deserialization (ObjectInputFilter) or switch to JSON/protobuf'

  # DS-005: PHP unserialize on user input
  'unserialize[[:space:]]*\([[:space:]]*\$_(GET|POST|REQUEST|COOKIE)|critical|DS-005|PHP unserialize on user-supplied input -- allows object injection|Never unserialize user input; use json_decode() instead'

  # DS-006: Ruby Marshal.load without filtering
  'Marshal\.(load|restore)[[:space:]]*\(|high|DS-006|Ruby Marshal.load used -- unsafe deserialization|Use JSON.parse or a safe serialization format; avoid Marshal on untrusted data'

  # DS-007: .NET BinaryFormatter deserialization
  'BinaryFormatter|high|DS-007|.NET BinaryFormatter detected -- vulnerable to deserialization attacks|Use System.Text.Json or DataContractSerializer with known types only'

  # DS-008: Java XMLDecoder usage
  'XMLDecoder[[:space:]]*\(|high|DS-008|Java XMLDecoder used -- vulnerable to XML deserialization attacks|Use a safe XML parser (JAXB with known types) instead of XMLDecoder'

  # DS-009: XML external entity processing enabled
  'FEATURE_EXTERNAL_GENERAL_ENTITIES|setExpandEntityReferences|resolveExternalEntities|high|DS-009|XML external entity processing may be enabled|Disable external entity processing; set FEATURE_EXTERNAL_GENERAL_ENTITIES to false'

  # DS-010: Unvalidated XML parsing (DOMParser, etree)
  'DOMParser|lxml\.etree\.parse|xml\.etree\.ElementTree\.parse|medium|DS-010|XML parsing without visible entity restriction|Disable DTD processing and external entities in XML parser configuration'

  # DS-011: Unsafe object spread/destructuring from external source
  'Object\.assign[[:space:]]*\([[:space:]]*\{\}[[:space:]]*,[[:space:]]*(req\.|request\.|body|input)|high|DS-011|Object.assign merging untrusted external data into object|Validate and allowlist properties before merging user data; avoid prototype pollution'

  # DS-012: Java readObject override without validation
  'readObject[[:space:]]*\([[:space:]]*ObjectInputStream|high|DS-012|Custom readObject without visible input validation|Implement ObjectInputFilter; validate deserialized object fields before use'

  # DS-013: Go gob.Decode from untrusted source
  'gob\.(NewDecoder|Decode)[[:space:]]*\(|medium|DS-013|Go gob.Decode used -- may accept untrusted data|Validate the source of gob-encoded data; prefer JSON for untrusted inputs'

  # DS-014: Python jsonpickle or dill deserialization
  '(jsonpickle|dill)\.(decode|loads|load)[[:space:]]*\(|critical|DS-014|jsonpickle/dill deserialization used -- allows arbitrary code execution|Use json.loads() instead; jsonpickle and dill are unsafe for untrusted data'

  # DS-015: Unsafe msgpack/protobuf without schema
  'msgpack\.unpack(b)?[[:space:]]*\(|medium|DS-015|MessagePack deserialization without visible schema validation|Define and enforce a schema for deserialized data; validate all fields after unpacking'
)

# ============================================================================
# 3. REDOS -- Regular Expression Denial of Service (RD-001 through RD-015)
#    Catastrophic backtracking, nested quantifiers, exponential patterns.
# ============================================================================

declare -a INPUTSHIELD_RD_PATTERNS=()

INPUTSHIELD_RD_PATTERNS+=(
  # RD-001: Nested quantifiers -- (a+)+ pattern
  '\([^)]*[+*][[:space:]]*\)[+*]|high|RD-001|Nested quantifiers detected -- potential catastrophic backtracking|Refactor regex to avoid nested quantifiers; use atomic groups or possessive quantifiers'

  # RD-002: Star-of-star pattern -- (.*)*
  '\(\.\*\)\*|high|RD-002|Star-of-star regex pattern -- exponential backtracking risk|Remove the outer quantifier or anchor the inner pattern'

  # RD-003: Overlapping alternation with quantifier -- (a|a)*
  '\([^)]*\|[^)]*\)[*+]|medium|RD-003|Alternation under quantifier -- may cause excessive backtracking|Ensure alternation branches are mutually exclusive; simplify overlapping patterns'

  # RD-004: Quantified group with optional elements -- (a?b+)*
  '\([^)]*[?][^)]*[+*][^)]*\)[*+]|high|RD-004|Quantified group with optional elements -- backtracking risk|Simplify the regex; make inner elements non-optional or remove outer quantifier'

  # RD-005: Nested repetition with dot -- (.+)+
  '\(\.[+*]\)[+*]|high|RD-005|Nested repetition with wildcard dot -- severe ReDoS risk|Replace with a specific character class; avoid nested quantifiers on wildcards'

  # RD-006: Unbounded repetition in lookahead
  '\(\?[=!][^)]*[+*]\)|medium|RD-006|Unbounded repetition inside lookahead -- may cause excessive matching|Limit repetition in lookaheads; use bounded quantifiers {n,m}'

  # RD-007: new RegExp with user input
  'new RegExp[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|params|input|user|data|args)|critical|RD-007|User input used to construct regex -- ReDoS and injection risk|Never build regex from user input; use allowlisted patterns or escape special characters'

  # RD-008: Python re.compile with variable (potential user input)
  're\.(compile|match|search|findall)[[:space:]]*\([[:space:]]*[a-z_]+[[:space:]]*[,)]|medium|RD-008|Regex compiled from variable -- verify input is not user-controlled|Ensure regex patterns are constants; never compile regexes from user-supplied strings'

  # RD-009: Repetition on complex character class -- [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+
  '\[[^\]]{10,}\][+*]\.\*|medium|RD-009|Complex character class with repetition followed by wildcard|Anchor regex and limit repetition; avoid .* after quantified character classes'

  # RD-010: Email validation regex (commonly vulnerable)
  '[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}|low|RD-010|Hand-written email validation regex -- often vulnerable to ReDoS|Use a well-tested email validation library instead of custom regex'

  # RD-011: URL validation regex with nested groups
  'https?://[^[:space:]]*\([^)]*[+*]\)|medium|RD-011|URL validation regex with nested quantified groups|Use a URL parsing library (new URL(), urllib.parse) instead of regex for URL validation'

  # RD-012: Repeated backreference -- (.+)\1+
  '\([^)]+\)\\\\1[+*]|medium|RD-012|Quantified backreference -- can cause exponential matching|Avoid quantified backreferences; redesign the matching logic'

  # RD-013: Greedy quantifier on alternation
  '\([^)]+\|[^)]+\)\{[0-9]*,\}|medium|RD-013|Alternation with unbounded repetition -- backtracking risk|Use bounded repetition {n,m} instead of unbounded; ensure branches do not overlap'

  # RD-014: Regex used in user-facing validation without timeout
  '(validateEmail|validateUrl|validateInput|isValid)[[:space:]]*.*new RegExp|high|RD-014|User-facing validation using dynamic RegExp -- ReDoS risk|Use pre-compiled constant regexes with bounded quantifiers; add regex timeout'

  # RD-015: Ruby Regexp.new with variable
  'Regexp\.new[[:space:]]*\([[:space:]]*[a-z_]|high|RD-015|Ruby Regexp.new constructed from variable -- potential ReDoS|Use constant regex patterns; escape user input with Regexp.escape() if dynamic regex is unavoidable'
)

# ============================================================================
# 4. PATH TRAVERSAL (PT-001 through PT-015)
#    Directory traversal, unsanitized file paths, file inclusion attacks.
# ============================================================================

declare -a INPUTSHIELD_PT_PATTERNS=()

INPUTSHIELD_PT_PATTERNS+=(
  # PT-001: Direct ../ in file path operations
  '\.\.[/\\]|high|PT-001|Path traversal sequence ../ detected in code|Sanitize file paths with path.resolve() and verify they stay within allowed directories'

  # PT-002: Path concatenation with user input (Node.js)
  'path\.(join|resolve)[[:space:]]*\([^)]*req\.(body|query|params)|critical|PT-002|User input used in path.join/resolve -- path traversal risk|Validate the resolved path starts with the intended base directory; reject ../ sequences'

  # PT-003: fs operations with user-controlled paths (Node.js)
  'fs\.(readFile|writeFile|readFileSync|writeFileSync|createReadStream|unlink|access|stat|open|appendFile)[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|params|input|filename)|critical|PT-003|File system operation with user-controlled path|Validate and sanitize file paths; use allowlists for accessible directories'

  # PT-004: Python open() with variable filename
  'open[[:space:]]*\([[:space:]]*(request\.|filename|filepath|file_path|user_file|upload|f")|high|PT-004|Python open() with potentially user-controlled filename|Validate file paths against an allowlist of permitted directories; reject path traversal characters'

  # PT-005: PHP file_get_contents with user input
  'file_get_contents[[:space:]]*\([[:space:]]*\$_(GET|POST|REQUEST)|critical|PT-005|PHP file_get_contents with user-supplied path -- local file inclusion|Validate paths against an allowlist; never pass user input directly to file operations'

  # PT-006: PHP include/require with variable
  '(include|require)(_once)?[[:space:]]*\([[:space:]]*\$|critical|PT-006|PHP include/require with variable path -- remote file inclusion risk|Use allowlisted paths for includes; never include files based on user input'

  # PT-007: URL-encoded path traversal patterns
  '%2e%2e[/%5c]|%252e%252e|%c0%ae|high|PT-007|URL-encoded path traversal sequence detected|Decode and normalize paths before validation; check for traversal after decoding'

  # PT-008: Express static file serving with user input
  'express\.static[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|path\.join.*req)|high|PT-008|Express static middleware with user-influenced path|Use fixed directory for express.static; never construct the path from user input'

  # PT-009: Archive extraction without path validation (zip slip)
  '(extractAll|extract)[[:space:]]*\([^)]*\)|medium|PT-009|Archive extraction without visible path validation -- zip slip risk|Validate extracted file paths stay within the target directory; reject entries with ../'

  # PT-010: User-controlled file serving
  '(sendFile|download|pipe)[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|params|filepath)|critical|PT-010|File serving endpoint with user-controlled path|Validate file paths against an allowlist; use path.resolve() and verify the resolved path is within bounds'

  # PT-011: Java file operations with user input
  'new File[[:space:]]*\([[:space:]]*(request\.|getParameter|req\.|param)|critical|PT-011|Java File object created from user input|Sanitize paths with Path.normalize(); validate against allowed base directory using startsWith()'

  # PT-012: Python os.path.join with user input
  'os\.path\.join[[:space:]]*\([^)]*request\.|os\.path\.join[[:space:]]*\([^)]*filename|high|PT-012|os.path.join with user-controlled segment -- path traversal risk|Validate the joined path with os.path.realpath() and verify it starts with the allowed base'

  # PT-013: User input in template file path
  'render[[:space:]]*\([[:space:]]*(req\.|request\.|body\.|query\.|params\.)|high|PT-013|Template rendering with user-controlled template path|Use a fixed set of template names; never pass user input as a template path'

  # PT-014: Symlink following without validation
  'fs\.realpath|os\.readlink|Files\.readSymbolicLink|medium|PT-014|Symlink resolution used -- verify target is within allowed directory|After resolving symlinks, validate the target path is within the allowed directory tree'

  # PT-015: Null byte injection in file path
  '%00|\\x00|\\0[^-9]|medium|PT-015|Potential null byte injection in file path|Strip null bytes from file paths; reject paths containing null characters'
)

# ============================================================================
# 5. COMMAND INJECTION (CI-001 through CI-015)
#    Shell execution with user input, eval, exec, template injection.
# ============================================================================

declare -a INPUTSHIELD_CI_PATTERNS=()

INPUTSHIELD_CI_PATTERNS+=(
  # CI-001: Node.js child_process.exec with user input
  'child_process\.(exec|execSync)[[:space:]]*\([[:space:]]*[`'"'"'"][^`'"'"'"]*\$\{|critical|CI-001|child_process.exec with template literal interpolation -- command injection|Use child_process.execFile or spawn with argument arrays; never interpolate user input into shell commands'

  # CI-002: Node.js child_process.exec with string concatenation
  '(exec|execSync)[[:space:]]*\([[:space:]]*[a-zA-Z_]*[[:space:]]*\+|critical|CI-002|exec/execSync with string concatenation -- command injection risk|Use execFile() or spawn() with argument arrays instead of shell string construction'

  # CI-003: Python os.system with variable
  'os\.system[[:space:]]*\([[:space:]]*(f['"'"'"]|[a-z_]+[[:space:]]*\+)|critical|CI-003|Python os.system with dynamic string -- command injection|Use subprocess.run() with a list of arguments and shell=False'

  # CI-004: Python os.popen with variable
  'os\.popen[[:space:]]*\([[:space:]]*(f['"'"'"]|[a-z_]+)|critical|CI-004|Python os.popen with dynamic string -- command injection|Use subprocess.run() with argument list and shell=False; capture output with subprocess.PIPE'

  # CI-005: Python subprocess with shell=True
  'subprocess\.(call|run|Popen|check_output|check_call)[[:space:]]*\([^)]*shell[[:space:]]*=[[:space:]]*True|critical|CI-005|subprocess called with shell=True -- command injection risk|Use shell=False (default) and pass arguments as a list; avoid shell=True with any user input'

  # CI-006: JavaScript eval() usage
  'eval[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|params|input|user|data|args)|critical|CI-006|eval() called with user-controlled input -- arbitrary code execution|Never use eval with user input; use JSON.parse for data or a safe expression evaluator'

  # CI-007: PHP exec/system/passthru/shell_exec
  '(exec|system|passthru|shell_exec|popen|proc_open)[[:space:]]*\([[:space:]]*\$|critical|CI-007|PHP shell execution function with variable argument -- command injection|Use escapeshellarg/escapeshellcmd; prefer library functions over shell commands'

  # CI-008: Ruby backtick or system with interpolation
  '`[^`]*#\{|system[[:space:]]*\([[:space:]]*"|critical|CI-008|Ruby shell execution with string interpolation -- command injection|Use Open3.capture3 or Shellwords.escape; pass arguments as arrays to system()'

  # CI-009: Generic eval() with variable (non-user-input specific)
  '[^a-zA-Z_]eval[[:space:]]*\([[:space:]]*[a-zA-Z_]+[[:space:]]*[,)]|high|CI-009|eval() called with variable argument -- potential code injection|Avoid eval entirely; use safe alternatives like JSON.parse, template engines, or sandboxed evaluation'

  # CI-010: Server-side template injection (SSTI)
  '(render_template_string|Template|Environment)[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|input|user)|critical|CI-010|Server-side template injection -- user input in template rendering|Never pass user input as template content; use template variables with auto-escaping enabled'

  # CI-011: SQL query string concatenation (non-parameterized)
  '(SELECT|INSERT|UPDATE|DELETE|DROP)[[:space:]]+.*[[:space:]]*\+[[:space:]]*[a-z_]+|critical|CI-011|SQL query built with string concatenation -- SQL injection|Use parameterized queries or prepared statements; never concatenate user input into SQL'

  # CI-012: LDAP query with user input
  'ldap[._](search|filter|query)[^;]*\+[[:space:]]*[a-z_]+|high|CI-012|LDAP query built with string concatenation -- LDAP injection|Use parameterized LDAP queries or escape special LDAP characters in user input'

  # CI-013: SSI injection via user input in HTML
  '<!--#(include|exec|echo|config)[[:space:]]|medium|CI-013|Server-Side Include directive detected -- verify input is not user-controlled|Disable SSI processing or ensure no user input reaches SSI directives'

  # CI-014: Expression Language injection (Java EL, SpEL)
  '\$\{[^}]*(request\.|param\.|header\.|cookie\.)|high|CI-014|Expression Language with request data -- EL injection risk|Use fixed expressions; never include user input in EL expressions; sanitize with OWASP encoder'

  # CI-015: Runtime.exec or ProcessBuilder with user input (Java)
  '(Runtime\.getRuntime\(\)\.exec|ProcessBuilder)[[:space:]]*\([[:space:]]*(request\.|getParameter|req\.|param)|critical|CI-015|Java Runtime.exec/ProcessBuilder with user input -- command injection|Pass arguments as a String array; validate and sanitize all command components'
)

# ============================================================================
# 6. XSS / OUTPUT ENCODING (XS-001 through XS-015)
#    Cross-site scripting, unsanitized output, missing encoding.
# ============================================================================

declare -a INPUTSHIELD_XS_PATTERNS=()

INPUTSHIELD_XS_PATTERNS+=(
  # XS-001: innerHTML assignment with variable
  '\.innerHTML[[:space:]]*=[[:space:]]*[^'"'"'"]|critical|XS-001|innerHTML assigned from variable -- XSS risk|Use textContent instead of innerHTML; if HTML is needed, sanitize with DOMPurify'

  # XS-002: React dangerouslySetInnerHTML
  'dangerouslySetInnerHTML|critical|XS-002|dangerouslySetInnerHTML used -- potential XSS vulnerability|Sanitize HTML content with DOMPurify before passing to dangerouslySetInnerHTML'

  # XS-003: document.write with variable
  'document\.write[[:space:]]*\([[:space:]]*[^'"'"'"]|critical|XS-003|document.write called with variable -- XSS risk|Avoid document.write entirely; use safe DOM APIs (textContent, createElement)'

  # XS-004: jQuery .html() with variable
  '\.(html|append|prepend|after|before|replaceWith)[[:space:]]*\([[:space:]]*[a-zA-Z_$]|high|XS-004|jQuery DOM manipulation with variable -- potential XSS|Use .text() for text content; sanitize with DOMPurify before .html() if HTML is needed'

  # XS-005: Vue v-html directive
  'v-html[[:space:]]*=[[:space:]]*"|high|XS-005|Vue v-html directive used -- renders raw HTML, XSS risk|Use v-text for text content; sanitize data with DOMPurify before v-html binding'

  # XS-006: Angular [innerHTML] binding
  '\[innerHTML\][[:space:]]*=|high|XS-006|Angular innerHTML binding -- potential XSS if not sanitized|Use Angular DomSanitizer.sanitize() or bypassSecurityTrustHtml() only with trusted content'

  # XS-007: Unescaped template output (Jinja2 |safe, ERB <%=, Handlebars {{{)
  '\|[[:space:]]*safe[[:space:]]*\}|<%=[[:space:]]|high|XS-007|Unescaped template output detected -- raw HTML rendering|Use auto-escaping templates; only mark content as safe after sanitization'

  # XS-008: Express res.send with unsanitized user input
  'res\.(send|write|end)[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|params|input|user)|critical|XS-008|Response body contains unsanitized user input -- reflected XSS|Encode output before sending; use a templating engine with auto-escaping'

  # XS-009: Server template rendering with user data in HTML context
  'res\.render[[:space:]]*\([^)]*req\.(body|query|params)|high|XS-009|Template rendered with user input -- ensure template engine auto-escapes|Verify the template engine has auto-escaping enabled; manually escape variables in HTML context'

  # XS-010: Missing Content-Security-Policy header
  'helmet|Content-Security-Policy|csp|low|XS-010|Content-Security-Policy reference found -- verify CSP is properly configured|Implement a strict CSP header; use nonce-based or hash-based policies for inline scripts'

  # XS-011: JSONP callback with user-controlled function name
  'callback[[:space:]]*=[[:space:]]*(req\.|request\.|query\.)|high|XS-011|JSONP callback from user input -- XSS via callback injection|Validate callback names against a strict pattern (alphanumeric only); prefer CORS over JSONP'

  # XS-012: Response header injection
  'res\.setHeader[[:space:]]*\([^,]*,[[:space:]]*(req\.|request\.|body|query|params)|high|XS-012|User input in response header -- header injection risk|Validate and sanitize header values; reject values containing newlines (CRLF injection)'

  # XS-013: Direct DOM manipulation with user string
  '(createElement|createTextNode|setAttribute)[[:space:]]*\([[:space:]]*(req\.|request\.|body|query|input|user)|medium|XS-013|DOM manipulation with potentially unsanitized user input|Validate and sanitize all values before DOM manipulation; use textContent for text'

  # XS-014: CSS injection via style attribute
  'style[[:space:]]*=[[:space:]]*(req\.|request\.|body|query|params|input|user)|medium|XS-014|User input in style attribute -- CSS injection risk|Validate CSS values against an allowlist; never interpolate user input into style attributes'

  # XS-015: Open redirect via unvalidated URL
  '(window\.)?location[[:space:]]*=[[:space:]]*(req\.|request\.|body|query|params|input|url|redirect)|critical|XS-015|Open redirect -- user input assigned to location/window.location|Validate redirect URLs against an allowlist of trusted domains; use relative paths only'
)

# ============================================================================
# Utility Functions
# ============================================================================

# All category codes for iteration
INPUTSHIELD_CATEGORIES="IV DS RD PT CI XS"

# Category labels
get_category_label() {
  local code="$1"
  case "$code" in
    IV) echo "Input Validation" ;;
    DS) echo "Deserialization" ;;
    RD) echo "ReDoS" ;;
    PT) echo "Path Traversal" ;;
    CI) echo "Command Injection" ;;
    XS) echo "XSS / Output Encoding" ;;
    *)  echo "$code" ;;
  esac
}

# Get the array variable name for a category
get_inputshield_patterns_for_category() {
  local category="$1"
  case "$category" in
    IV) echo "INPUTSHIELD_IV_PATTERNS" ;;
    DS) echo "INPUTSHIELD_DS_PATTERNS" ;;
    RD) echo "INPUTSHIELD_RD_PATTERNS" ;;
    PT) echo "INPUTSHIELD_PT_PATTERNS" ;;
    CI) echo "INPUTSHIELD_CI_PATTERNS" ;;
    XS) echo "INPUTSHIELD_XS_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# Get total pattern count across all categories
inputshield_pattern_count() {
  local count=0
  count=$((count + ${#INPUTSHIELD_IV_PATTERNS[@]}))
  count=$((count + ${#INPUTSHIELD_DS_PATTERNS[@]}))
  count=$((count + ${#INPUTSHIELD_RD_PATTERNS[@]}))
  count=$((count + ${#INPUTSHIELD_PT_PATTERNS[@]}))
  count=$((count + ${#INPUTSHIELD_CI_PATTERNS[@]}))
  count=$((count + ${#INPUTSHIELD_XS_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
inputshield_category_count() {
  local category="$1"
  local arr_name
  arr_name=$(get_inputshield_patterns_for_category "$category")
  if [[ -z "$arr_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$arr_name"
  echo "${#_ref[@]}"
}

# List patterns for a category with optional limit (for tier-based access)
inputshield_list_patterns() {
  local filter_category="${1:-all}"
  local limit="${2:-0}"  # 0 = no limit

  if [[ "$filter_category" == "all" ]]; then
    for cat in $INPUTSHIELD_CATEGORIES; do
      inputshield_list_patterns "$cat" "$limit"
    done
    return
  fi

  local arr_name
  arr_name=$(get_inputshield_patterns_for_category "$filter_category")
  if [[ -z "$arr_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _pref="$arr_name"
  local idx=0

  for entry in "${_pref[@]}"; do
    if [[ $limit -gt 0 && $idx -ge $limit ]]; then
      break
    fi
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
    idx=$((idx + 1))
  done
}

# Get patterns for a category with tier-based limit.
# Returns pattern entries (one per line) up to the tier limit.
get_tier_limited_patterns() {
  local category="$1"
  local per_category_limit="${2:-5}"

  local arr_name
  arr_name=$(get_inputshield_patterns_for_category "$category")
  if [[ -z "$arr_name" ]]; then
    return
  fi

  local -n _pref="$arr_name"
  local idx=0

  for entry in "${_pref[@]}"; do
    if [[ $idx -ge $per_category_limit ]]; then
      break
    fi
    echo "$entry"
    idx=$((idx + 1))
  done
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
