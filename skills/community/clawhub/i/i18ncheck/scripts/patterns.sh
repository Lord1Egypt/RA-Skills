#!/usr/bin/env bash
# I18nCheck -- Internationalization Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- i18n issues that will break localization completely
#   high     -- Issues that make translation difficult or incorrect
#   medium   -- Sub-optimal patterns that should be improved for i18n
#   low      -- Informational, minor i18n improvements possible
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, \b, etc.)
#
# Patterns cover 6 languages: JS/TS, Python, Java, Go, Ruby, PHP

set -euo pipefail

# ============================================================================
# 1. HARDCODED STRINGS (HS-001 through HS-015)
# ============================================================================

declare -a I18NCHECK_HS_PATTERNS=()

I18NCHECK_HS_PATTERNS+=(
  # --- HS-001: Hardcoded text in JSX/TSX elements ---
  # Matches: <h1>Welcome to our site</h1>, <p>Some text here</p>, <span>Hello</span>
  '<(h[1-6]|p|span|div|li|td|th|button|label|a|strong|em|b|i)>[[:space:]]*[A-Z][a-zA-Z ,.!?'"'"']{3,}[[:space:]]*<|critical|HS-001|Hardcoded text content in JSX/TSX element|Wrap with translation function: t("key") or <Trans i18nKey="key">'

  # --- HS-002: Hardcoded strings in alert/confirm/prompt ---
  # Matches: alert("Please enter..."), confirm("Are you sure?"), prompt("Enter name")
  '(alert|confirm|prompt)[[:space:]]*\([[:space:]]*"[A-Z][^"]{3,}"|critical|HS-002|Hardcoded string in alert()/confirm()/prompt() call|Replace with translated string: alert(t("message_key"))'

  # --- HS-003: Hardcoded placeholder attribute ---
  # Matches: placeholder="Enter your email", placeholder="Search..."
  'placeholder[[:space:]]*=[[:space:]]*"[A-Z][^"]{2,}"|high|HS-003|Hardcoded placeholder attribute text|Use translated placeholder: placeholder={t("input.placeholder")}'

  # --- HS-004: Hardcoded title attribute ---
  # Matches: title="Click here", title="More information"
  'title[[:space:]]*=[[:space:]]*"[A-Z][^"]{2,}"|high|HS-004|Hardcoded title attribute text|Use translated title: title={t("element.title")}'

  # --- HS-005: Hardcoded button/submit value ---
  # Matches: value="Submit", value="Cancel", value="OK"
  'value[[:space:]]*=[[:space:]]*"(Submit|Cancel|OK|Save|Delete|Edit|Update|Close|Next|Back|Previous|Continue|Confirm|Reset|Send|Search|Login|Sign [Uu]p|Sign [Ii]n|Register|Log [Oo]ut|Apply|Remove)"|high|HS-005|Hardcoded button/submit value text|Use translated value: value={t("button.submit")}'

  # --- HS-006: Hardcoded label text in HTML/JSX ---
  # Matches: <label>Email Address</label>, <label>Username</label>
  '<label[^>]*>[[:space:]]*[A-Z][a-zA-Z ]{2,}[[:space:]]*</label>|high|HS-006|Hardcoded label text in HTML/JSX element|Wrap label text with translation: <label>{t("form.email_label")}</label>'

  # --- HS-007: Hardcoded error message strings ---
  # Matches: "Error: Something went wrong", "Failed to load", "Invalid input"
  '(error|Error|ERROR)[[:space:]]*[:=][[:space:]]*"[A-Z][^"]{5,}"|high|HS-007|Hardcoded error message string in UI code|Use translated error messages: t("error.something_went_wrong")'

  # --- HS-008: Hardcoded tooltip/popover text ---
  # Matches: tooltip="Click to expand", data-tooltip="More info"
  '(tooltip|data-tooltip|data-tip|popover)[[:space:]]*=[[:space:]]*"[A-Z][^"]{3,}"|medium|HS-008|Hardcoded tooltip or popover text|Use translated tooltip: tooltip={t("tooltip.click_to_expand")}'

  # --- HS-009: Hardcoded option text in select ---
  # Matches: <option>Select an option</option>, <option value="1">First Choice</option>
  '<option[^>]*>[[:space:]]*[A-Z][a-zA-Z ]{2,}[[:space:]]*</option>|high|HS-009|Hardcoded option text in select element|Translate option text: <option>{t("select.first_choice")}</option>'

  # --- HS-010: Hardcoded heading text ---
  # Matches: <h1>Dashboard</h1>, <h2>Settings</h2>
  '<h[1-6][^>]*>[[:space:]]*[A-Z][a-zA-Z ]{2,}</h[1-6]>|high|HS-010|Hardcoded heading text content|Translate heading: <h1>{t("page.dashboard_title")}</h1>'

  # --- HS-011: Hardcoded paragraph text ---
  # Matches: <p>This is a description of the feature.</p>
  '<p[^>]*>[[:space:]]*[A-Z][a-zA-Z ,.:;!?'"'"']{10,}</p>|medium|HS-011|Hardcoded paragraph text content|Translate paragraph text: <p>{t("feature.description")}</p>'

  # --- HS-012: Hardcoded document.title assignment ---
  # Matches: document.title = "My App - Dashboard"
  'document\.title[[:space:]]*=[[:space:]]*"[^"]{3,}"|high|HS-012|Hardcoded string in document.title assignment|Use translated page title: document.title = t("page.title")'

  # --- HS-013: Hardcoded user-facing console messages ---
  # Matches: showMessage("Operation completed"), notify("Success!")
  '(showMessage|showNotification|showToast|notify|toast|snackbar|addToast|pushNotification)[[:space:]]*\([[:space:]]*"[A-Z][^"]{3,}"|medium|HS-013|Hardcoded text in user notification/toast call|Use translated notification: showToast(t("notification.success"))'

  # --- HS-014: Hardcoded strings in Python/Ruby/Java UI code ---
  # Matches: Label("Username"), JLabel("Password"), render("Error page")
  '(Label|JLabel|JButton|JMenuItem|setText|setTitle|setToolTipText|render_template|flash)[[:space:]]*\([[:space:]]*"[A-Z][^"]{3,}"|high|HS-014|Hardcoded string in Python/Ruby/Java UI framework call|Use translation function for UI text in server-side frameworks'

  # --- HS-015: Hardcoded notification/toast message ---
  # Matches: Toast.makeText(ctx, "Saved successfully", ...), QMessageBox.information(self, "Info", "Done")
  '(Toast\.makeText|QMessageBox\.|MessageBox\.Show|NSAlert|UIAlertController)[[:space:]]*\([^)]*"[A-Z][^"]{3,}"|medium|HS-015|Hardcoded notification/dialog message text|Wrap notification text with translation function'
)

# ============================================================================
# 2. TRANSLATION KEYS (TK-001 through TK-015)
# ============================================================================

declare -a I18NCHECK_TK_PATTERNS=()

I18NCHECK_TK_PATTERNS+=(
  # --- TK-001: String literal missing t()/i18n() wrapper ---
  # Matches: return "Welcome back"; (in component-like context)
  'return[[:space:]]+"[A-Z][a-zA-Z ]{3,}"[[:space:]]*;|high|TK-001|String literal returned without translation wrapper|Wrap with t(): return t("welcome_back")'

  # --- TK-002: Untranslated aria-label ---
  # Matches: aria-label="Close dialog", aria-label="Open menu"
  'aria-label[[:space:]]*=[[:space:]]*"[A-Z][^"]{2,}"|high|TK-002|Untranslated aria-label attribute value|Use translated aria-label for accessibility: aria-label={t("aria.close_dialog")}'

  # --- TK-003: Untranslated aria-placeholder ---
  # Matches: aria-placeholder="Type to search"
  'aria-placeholder[[:space:]]*=[[:space:]]*"[A-Z][^"]{2,}"|high|TK-003|Untranslated aria-placeholder attribute|Translate aria-placeholder: aria-placeholder={t("aria.search_placeholder")}'

  # --- TK-004: Suspicious hardcoded English in i18n JSON ---
  # Matches: "key": "Some English text that should be translated"
  '"[a-z_.]+"[[:space:]]*:[[:space:]]*"[A-Z][a-zA-Z ]{15,}"|medium|TK-004|Suspiciously long English string in locale/translation file|Verify translation is not just English placeholder text'

  # --- TK-005: Duplicate translation key definitions ---
  # Matches: repeated "key_name": patterns in same context
  '"([a-z_]+)"[[:space:]]*:.*"([a-z_]+)"[[:space:]]*:|medium|TK-005|Possible duplicate translation key pattern|Check for duplicate keys in translation files; use unique keys'

  # --- TK-006: Inconsistent key naming (camelCase vs snake_case) ---
  # Matches: "loginButton": next to "logout_button":
  '"[a-z]+[A-Z][a-zA-Z]+"[[:space:]]*:[[:space:]]*"|medium|TK-006|CamelCase translation key (inconsistent with snake_case convention)|Use consistent key naming: prefer dot-separated or snake_case keys'

  # --- TK-007: Raw string in component prop ---
  # Matches: label="Username", message="Error occurred"
  '(label|message|text|description|header|footer|caption|subtitle|headline)[[:space:]]*=[[:space:]]*"[A-Z][^"]{3,}"|high|TK-007|Raw string passed to component prop expecting translation|Use translated prop value: label={t("form.username_label")}'

  # --- TK-008: Hardcoded string in gettext call (empty or English) ---
  # Matches: gettext(""), ngettext("item", "items", count)
  '(gettext|ngettext|pgettext|_)[[:space:]]*\([[:space:]]*""[[:space:]]*\)|medium|TK-008|Empty string in gettext/translation call|Provide a valid translation key string in gettext call'

  # --- TK-009: Missing i18n function in file with HTML strings ---
  # Matches: files with JSX/HTML that lack any i18n import
  'PLACEHOLDER_MISSING_I18N_IMPORT|medium|TK-009|File contains UI strings but has no i18n/translation import|Add translation import: import { t } from "i18next" or equivalent'

  # --- TK-010: Translation function with variable key ---
  # Matches: t(variableName), i18n.t(someKey)
  '(^|[^a-zA-Z])(t|i18n\.t|intl\.formatMessage|__)\([[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\)|medium|TK-010|Translation function called with variable key (harder to extract)|Use string literal keys for static extraction: t("literal.key")'

  # --- TK-011: Translation function with empty string ---
  # Matches: t(""), i18n.t("")
  '(t|i18n\.t|__|gettext)[[:space:]]*\([[:space:]]*"[[:space:]]*"[[:space:]]*\)|medium|TK-011|Translation function called with empty string|Provide a valid translation key'

  # --- TK-012: Untranslated alt text on images ---
  # Matches: alt="Company logo", alt="User avatar"
  'alt[[:space:]]*=[[:space:]]*"[A-Z][^"]{2,}"|high|TK-012|Untranslated alt text on image|Use translated alt text: alt={t("image.company_logo")}'

  # --- TK-013: Hardcoded validation messages ---
  # Matches: "This field is required", "Please enter a valid email"
  '(required|validate|validation)[[:space:]]*[:=][[:space:]]*"[A-Z][^"]{5,}"|medium|TK-013|Hardcoded string in validation message|Use translated validation messages from i18n system'

  # --- TK-014: Untranslated content in meta tags ---
  # Matches: <meta name="description" content="Our company provides..."
  'content[[:space:]]*=[[:space:]]*"[A-Z][a-zA-Z ,.]{15,}"|high|TK-014|Untranslated content in HTML meta tag|Translate meta tag content for SEO in target locales'

  # --- TK-015: Hardcoded display values for enums ---
  # Matches: "ACTIVE": "Active", STATUS_LABELS = { pending: "Pending" }
  '(LABELS|DISPLAY|STATUS|NAMES|TITLES)[[:space:]]*[\[{=].*"[A-Z][a-zA-Z ]{2,}"|medium|TK-015|Hardcoded display value for enum/constant|Use translation keys for enum display values: t("status.active")'
)

# ============================================================================
# 3. DATE & NUMBER FORMATTING (DF-001 through DF-015)
# ============================================================================

declare -a I18NCHECK_DF_PATTERNS=()

I18NCHECK_DF_PATTERNS+=(
  # --- DF-001: toLocaleDateString without locale ---
  # Matches: .toLocaleDateString(), .toLocaleTimeString(), .toLocaleString()
  '\.toLocale(Date|Time|)String[[:space:]]*\([[:space:]]*\)|high|DF-001|toLocaleDateString() called without explicit locale parameter|Pass explicit locale: .toLocaleDateString("en-US") or use Intl.DateTimeFormat'

  # --- DF-002: Hardcoded date format MM/DD/YYYY or DD/MM/YYYY ---
  # Matches: "MM/DD/YYYY", "DD-MM-YYYY", "YYYY/MM/DD" as format strings
  '["'"'"'](MM[/-]DD[/-]YYYY|DD[/-]MM[/-]YYYY|YYYY[/-]MM[/-]DD|mm[/-]dd[/-]yyyy|dd[/-]mm[/-]yyyy)["'"'"']|high|DF-002|Hardcoded date format string (locale-dependent)|Use locale-aware date formatting: Intl.DateTimeFormat or equivalent'

  # --- DF-003: Manual number formatting with toFixed ---
  # Matches: .toFixed(2) in currency/display context
  '\.(toFixed|toPrecision)[[:space:]]*\([[:space:]]*[0-9]+[[:space:]]*\)|high|DF-003|Manual number formatting instead of Intl.NumberFormat|Use Intl.NumberFormat for locale-aware number display'

  # --- DF-004: Hardcoded currency symbols ---
  # Matches: "$" + price, "EUR " + amount, price + " USD"
  '["'"'"']([$]|EUR|GBP|JPY|CNY|USD|CAD|AUD)["'"'"'][[:space:]]*[+]|high|DF-004|Hardcoded currency symbol in display string|Use Intl.NumberFormat with style: "currency" for locale-aware currency display'

  # --- DF-005: Locale-dependent parseFloat/parseInt ---
  # Matches: parseFloat("1,234.56"), parseInt(userInput)
  'parse(Float|Int)[[:space:]]*\([[:space:]]*[a-zA-Z]|medium|DF-005|parseFloat/parseInt on user input (locale-dependent decimal separators)|Use locale-aware number parsing or Intl.NumberFormat for user input'

  # --- DF-006: Timezone-naive Date constructor ---
  # Matches: new Date(), Date.now(), new Date("2024-01-01")
  'new[[:space:]]+Date[[:space:]]*\([[:space:]]*("[0-9]{4}|'"'"'[0-9]{4}|\)|$)|high|DF-006|Timezone-naive Date construction|Use timezone-aware date library (date-fns-tz, luxon, Temporal) or pass timezone explicitly'

  # --- DF-007: Hardcoded decimal separator ---
  # Matches: value.replace(".", ","), split(".")[0]
  '\.(replace|split)[[:space:]]*\([[:space:]]*"[.,]"|medium|DF-007|Hardcoded decimal separator (period or comma)|Use Intl.NumberFormat for locale-correct decimal formatting'

  # --- DF-008: strftime/strptime without locale ---
  # Matches: strftime("%m/%d/%Y"), strptime(date_str, "%d-%m-%Y")
  'str[fp]time[[:space:]]*\([[:space:]]*"?%[mMdDyYHIpBba/.-]+|high|DF-008|strftime/strptime with hardcoded format (locale-dependent)|Use locale-aware date formatting: babel.dates.format_date() or equivalent'

  # --- DF-009: Hardcoded thousand separator ---
  # Matches: .replace(/(\d)((\d{3})+$)/, "$1,")
  'replace[[:space:]]*\(.*[0-9]{3}.*[",.]|medium|DF-009|Manual thousand separator insertion (locale-dependent)|Use Intl.NumberFormat for locale-correct number grouping'

  # --- DF-010: SimpleDateFormat without Locale (Java) ---
  # Matches: new SimpleDateFormat("MM/dd/yyyy")
  'new[[:space:]]+SimpleDateFormat[[:space:]]*\([[:space:]]*"[^"]*"[[:space:]]*\)|high|DF-010|SimpleDateFormat without explicit Locale parameter (Java)|Pass Locale: new SimpleDateFormat("dd/MM/yyyy", Locale.US)'

  # --- DF-011: Go time.Format with hardcoded layout ---
  # Matches: .Format("01/02/2006"), .Format("2006-01-02 15:04")
  '\.Format[[:space:]]*\([[:space:]]*"[0-9]{2}[/.-][0-9]{2}[/.-][0-9]{4}|medium|DF-011|Go time.Format with hardcoded US date layout|Use locale-appropriate format or accept format as parameter'

  # --- DF-012: Date.parse with string ---
  # Matches: Date.parse("January 1, 2024"), Date.parse(dateString)
  'Date\.parse[[:space:]]*\([[:space:]]*"[A-Z][a-zA-Z]+[[:space:]]+[0-9]|high|DF-012|Date.parse() with locale-dependent date string|Use ISO 8601 format or locale-aware date parsing'

  # --- DF-013: Hardcoded AM/PM ---
  # Matches: "AM", "PM" in time formatting context
  '(format|display|show|render)[^;]*["'"'"'](AM|PM|am|pm)["'"'"']|medium|DF-013|Hardcoded AM/PM time format assumption|Use Intl.DateTimeFormat with hour12 option for locale-correct time'

  # --- DF-014: Number.toFixed for currency ---
  # Matches: price.toFixed(2), amount.toFixed(2)
  '(price|cost|amount|total|fee|tax|balance|salary|payment)[^;]*\.toFixed[[:space:]]*\(|medium|DF-014|Number.toFixed() used for currency display|Use Intl.NumberFormat({style: "currency"}) for proper currency formatting'

  # --- DF-015: moment() without locale ---
  # Matches: moment().format("LL"), moment(date).format(
  'moment[[:space:]]*\([^)]*\)\.format[[:space:]]*\(|high|DF-015|moment().format() without locale configuration|Configure moment locale: moment.locale(userLocale) or migrate to date-fns/luxon'
)

# ============================================================================
# 4. RTL & LAYOUT (RL-001 through RL-015)
# ============================================================================

declare -a I18NCHECK_RL_PATTERNS=()

I18NCHECK_RL_PATTERNS+=(
  # --- RL-001: Missing dir attribute on html ---
  # Matches: <html> or <html lang="en"> without dir
  '<html[^>]*>[[:space:]]*$|high|RL-001|HTML element may be missing dir attribute for RTL support|Add dir attribute: <html dir="ltr" lang="en"> or set dynamically'

  # --- RL-002: Hardcoded text-align: left ---
  # Matches: text-align: left; text-align:left
  'text-align[[:space:]]*:[[:space:]]*left|high|RL-002|Hardcoded text-align: left (breaks in RTL layouts)|Use text-align: start for automatic RTL support, or use logical properties'

  # --- RL-003: Hardcoded text-align: right ---
  # Matches: text-align: right; text-align:right
  'text-align[[:space:]]*:[[:space:]]*right|high|RL-003|Hardcoded text-align: right (breaks in RTL layouts)|Use text-align: end for automatic RTL support, or use logical properties'

  # --- RL-004: float: left ---
  # Matches: float: left;
  'float[[:space:]]*:[[:space:]]*left|medium|RL-004|float: left without logical alternative|Use float: inline-start or flexbox/grid for RTL-compatible layouts'

  # --- RL-005: float: right ---
  # Matches: float: right;
  'float[[:space:]]*:[[:space:]]*right|medium|RL-005|float: right without logical alternative|Use float: inline-end or flexbox/grid for RTL-compatible layouts'

  # --- RL-006: margin-left/margin-right instead of margin-inline ---
  # Matches: margin-left: 16px; margin-right: 8px
  'margin-(left|right)[[:space:]]*:|high|RL-006|margin-left/margin-right instead of logical margin-inline-start/end|Use margin-inline-start/margin-inline-end for RTL support'

  # --- RL-007: padding-left/padding-right instead of padding-inline ---
  # Matches: padding-left: 16px; padding-right: 8px
  'padding-(left|right)[[:space:]]*:|high|RL-007|padding-left/padding-right instead of logical padding-inline-start/end|Use padding-inline-start/padding-inline-end for RTL support'

  # --- RL-008: border-left/border-right instead of logical ---
  # Matches: border-left: 1px solid; border-right: none
  'border-(left|right)[[:space:]]*:|medium|RL-008|border-left/border-right instead of logical border-inline-start/end|Use border-inline-start/border-inline-end for RTL support'

  # --- RL-009: Missing lang attribute on html ---
  # Matches: <html> without lang, <html dir="ltr">
  '<html[[:space:]]*>|high|RL-009|Missing lang attribute on html element|Add lang attribute: <html lang="en"> for accessibility and i18n'

  # --- RL-010: CSS left/right positioning ---
  # Matches: left: 16px; right: 0;
  '[^a-z-](left|right)[[:space:]]*:[[:space:]]*[0-9]+|medium|RL-010|Directional left/right CSS position (not RTL-safe)|Use inset-inline-start/inset-inline-end for RTL-compatible positioning'

  # --- RL-011: Hardcoded text direction ltr ---
  # Matches: direction: ltr;
  'direction[[:space:]]*:[[:space:]]*ltr|medium|RL-011|Hardcoded text direction: ltr in CSS|Set direction dynamically based on locale, or remove if not needed'

  # --- RL-012: text-indent with direction assumption ---
  # Matches: text-indent: 20px; text-indent: 2em
  'text-indent[[:space:]]*:[[:space:]]*[0-9]+|high|RL-012|text-indent with fixed direction assumption|Use logical properties or set text-indent direction-aware for RTL'

  # --- RL-013: CSS transform translateX with directional value ---
  # Matches: transform: translateX(100px); transform: translateX(-50%)
  'translateX[[:space:]]*\([[:space:]]*-?[0-9]+|medium|RL-013|CSS translateX with directional value (not RTL-safe)|Use logical transform or flip translateX value for RTL layouts'

  # --- RL-014: Directional arrow/chevron icon ---
  # Matches: arrow-left, chevron-right, ArrowLeft, ChevronRight
  '(arrow|chevron|caret)[_-]?(left|right|Left|Right)|high|RL-014|Directional icon/arrow that needs RTL flip|Use CSS transform: scaleX(-1) in RTL or swap icon programmatically'

  # --- RL-015: CSS flexbox/grid direction assumption ---
  # Matches: flex-direction: row; (without RTL consideration in context)
  'flex-direction[[:space:]]*:[[:space:]]*row-reverse|medium|RL-015|flex-direction: row-reverse may need adjustment for RTL|Verify flex-direction works correctly in both LTR and RTL contexts'
)

# ============================================================================
# 5. STRING CONCATENATION (SC-001 through SC-015)
# ============================================================================

declare -a I18NCHECK_SC_PATTERNS=()

I18NCHECK_SC_PATTERNS+=(
  # --- SC-001: String concatenation in translated message ---
  # Matches: t("Hello ") + name, __("Welcome ") + userName
  '(t|__|gettext|i18n\.t|intl\.formatMessage)[[:space:]]*\([[:space:]]*"[^"]*"[[:space:]]*\)[[:space:]]*[+]|critical|SC-001|String concatenation with translated message|Use interpolation: t("hello_name", { name: userName })'

  # --- SC-002: Template literal in translation call ---
  # Matches: t(`Hello ${name}`), i18n.t(`Welcome ${user}`)
  '(t|__|gettext|i18n\.t)[[:space:]]*\([[:space:]]*`[^`]*\$\{|high|SC-002|Template literal interpolation inside translation call|Use i18n interpolation: t("hello_name", { name }) instead of template literals'

  # --- SC-003: Printf-style formatting without i18n ---
  # Matches: sprintf("Hello %s, you have %d items", name, count)
  'sprintf[[:space:]]*\([[:space:]]*"[^"]*%[sdf][^"]*"|high|SC-003|Printf-style format string without i18n library|Use i18n-aware formatting: t("message", { name, count })'

  # --- SC-004: Concatenated string fragments for UI ---
  # Matches: "You have " + count + " items in your cart"
  '"[A-Z][a-zA-Z ]*"[[:space:]]*[+][[:space:]]*[a-zA-Z_]+[[:space:]]*[+][[:space:]]*"[a-zA-Z ]+"|critical|SC-004|Word order assumption in concatenated translation string|Use interpolation with named placeholders: t("cart_items", { count })'

  # --- SC-005: Plural with simple if/else ---
  # Matches: count === 1 ? "item" : "items", n == 1 ? "file" : "files"
  '[=!]=+[[:space:]]*1[[:space:]]*\?[[:space:]]*"[a-zA-Z]+("[[:space:]]*:[[:space:]]*"|'"'"'[[:space:]]*:[[:space:]]*'"'"')"?[a-zA-Z]+s"|high|SC-005|Simple if/else pluralization (incorrect for many languages)|Use i18n plural rules: t("item", { count }) with ICU MessageFormat or equivalent'

  # --- SC-006: Gender assumption in strings ---
  # Matches: "his"/"her" or "he"/"she" in conditional string building
  '(gender|sex)[^;]*\?[[:space:]]*"(he|she|his|her|him)"|high|SC-006|Gender assumption in string construction (many languages have more forms)|Use gender-neutral ICU MessageFormat: {gender, select, male {he} female {she} other {they}}'

  # --- SC-007: Number-to-string concatenation ---
  # Matches: count + " items", price + " dollars"
  '[a-zA-Z_]+(count|num|total|amount|quantity|price)[a-zA-Z_]*[[:space:]]*[+][[:space:]]*"[[:space:]][a-zA-Z]+"|medium|SC-007|Number-to-string concatenation for display|Use Intl.NumberFormat and translation interpolation'

  # --- SC-008: Conditional string building ---
  # Matches: (isActive ? "Active" : "Inactive"), (enabled ? "On" : "Off")
  '\?[[:space:]]*"[A-Z][a-zA-Z]+"[[:space:]]*:[[:space:]]*"[A-Z][a-zA-Z]+"|high|SC-008|Conditional string building for UI messages|Use translation keys for each state: t(isActive ? "status.active" : "status.inactive")'

  # --- SC-009: Array join for sentence ---
  # Matches: names.join(", "), items.join(" and ")
  '\.join[[:space:]]*\([[:space:]]*"[, ]+(&|and|or|und|et|y|e)[, ]*"|medium|SC-009|Array.join() with hardcoded conjunction for sentence construction|Use Intl.ListFormat for locale-aware list formatting'

  # --- SC-010: String replace for dynamic values ---
  # Matches: message.replace("{name}", userName), text.replace("%s", value)
  '(message|text|label|title|description)[^;]*\.replace[[:space:]]*\([[:space:]]*["'"'"'][{%][^"'"'"']*["'"'"']|high|SC-010|String.replace() for dynamic values in translated text|Use i18n interpolation instead of manual string replacement'

  # --- SC-011: Sentence fragment concatenation ---
  # Matches: "The " + type + " has been " + action + "."
  '"[Tt]he[[:space:]]+"[[:space:]]*[+][[:space:]]*[a-zA-Z_]+[[:space:]]*[+][[:space:]]*"[[:space:]][a-zA-Z ]+"|critical|SC-011|Sentence fragments concatenated across variables|Use single translation key with interpolation: t("item_action", { type, action })'

  # --- SC-012: Ordinal formatting without i18n ---
  # Matches: num + "st", num + "nd", num + "rd", num + "th"
  '[a-zA-Z_]+[[:space:]]*[+][[:space:]]*"(st|nd|rd|th)"|medium|SC-012|Ordinal number formatting without i18n|Use Intl.PluralRules with ordinal type or i18n ordinal formatting'

  # --- SC-013: Possessive form with apostrophe-s ---
  # Matches: name + "'s profile", user + "'s settings"
  '[a-zA-Z_]+[[:space:]]*[+][[:space:]]*"'"'"'s[[:space:]]|high|SC-013|Possessive form with English apostrophe-s assumption|Use interpolation: t("users_profile", { name }) -- possessives vary by language'

  # --- SC-014: List formatting without Intl.ListFormat ---
  # Matches: items.join(", ") + " and " + lastItem
  '\.join[[:space:]]*\([[:space:]]*",[[:space:]]*"[[:space:]]*\)[[:space:]]*[+][[:space:]]*"[[:space:]]+(and|or)|medium|SC-014|Manual list formatting without Intl.ListFormat|Use Intl.ListFormat for locale-aware list conjunction'

  # --- SC-015: Relative time via concatenation ---
  # Matches: diff + " days ago", count + " minutes left"
  '[a-zA-Z_]+[[:space:]]*[+][[:space:]]*"[[:space:]]+(days?|hours?|minutes?|seconds?|weeks?|months?|years?)[[:space:]]+(ago|left|remaining|from now)"|high|SC-015|Relative time expressed via string concatenation|Use Intl.RelativeTimeFormat for locale-aware relative time display'
)

# ============================================================================
# 6. ENCODING & LOCALE (EN-001 through EN-015)
# ============================================================================

declare -a I18NCHECK_EN_PATTERNS=()

I18NCHECK_EN_PATTERNS+=(
  # --- EN-001: Non-UTF-8 charset in HTML ---
  # Matches: charset="iso-8859-1", charset="windows-1252", charset="ascii"
  'charset[[:space:]]*=[[:space:]]*"?(iso-8859|windows-125[0-9]|ascii|latin|shift[_-]?jis|euc|gb2312|big5)|high|EN-001|Non-UTF-8 charset declaration in HTML|Use UTF-8: <meta charset="UTF-8"> for universal character support'

  # --- EN-002: Locale-dependent toLowerCase (Turkish I problem) ---
  # Matches: .toLowerCase() without locale, .toUpperCase() without locale
  '\.(toLowerCase|toUpperCase)[[:space:]]*\([[:space:]]*\)|high|EN-002|Locale-dependent toLowerCase/toUpperCase (Turkish I problem)|Use .toLocaleLowerCase(locale) or String.prototype.localeCompare for locale-safe case conversion'

  # --- EN-003: ASCII-only regex for name validation ---
  # Matches: /^[a-zA-Z]+$/, /^[a-z ]+$/i (rejects international names)
  '/\^?\[a-zA-Z[[:space:],_.@-]*\][+*]\$?/|medium|EN-003|ASCII-only regex pattern for name/text validation|Use Unicode-aware patterns or remove character restrictions for international names'

  # --- EN-004: Hardcoded locale identifier ---
  # Matches: "en-US", "en_US", locale = "en", language = "en"
  '(locale|language|lang)[[:space:]]*[:=][[:space:]]*["'"'"'](en|en-US|en_US|en-GB)["'"'"']|medium|EN-004|Hardcoded locale identifier string|Use dynamic locale detection: navigator.language, Accept-Language header, or user preference'

  # --- EN-005: Missing Unicode normalization ---
  # Matches: str1 === str2 (string comparison without normalize)
  'PLACEHOLDER_MISSING_NORMALIZE|medium|EN-005|String comparison without Unicode normalization|Use String.prototype.normalize() before comparing: str.normalize("NFC")'

  # --- EN-006: Byte-level string length on multi-byte text ---
  # Matches: strlen(), len(), .length for truncation
  '(strlen|mb_strlen|len|\.length)[[:space:]]*[><=!]+[[:space:]]*[0-9]+|high|EN-006|Byte-level string length check on potentially multi-byte text|Use grapheme-aware length: Intl.Segmenter, mb_strlen, or grapheme_strlen'

  # --- EN-007: strcmp without locale collation ---
  # Matches: strcmp(a, b), strcasecmp(a, b)
  '(strcmp|strcasecmp|strcoll)[[:space:]]*\(|medium|EN-007|strcmp/strcasecmp without locale-aware collation|Use locale-aware comparison: Intl.Collator, strcoll, or localeCompare'

  # --- EN-008: Hardcoded encoding in file operations ---
  # Matches: open(file, encoding="ascii"), fopen with "r" mode, Charset.forName("US-ASCII")
  '(encoding|charset|Charset\.forName)[[:space:]]*[:=(][[:space:]]*"?(ascii|us-ascii|iso-8859|latin|ANSI)|medium|EN-008|Hardcoded non-Unicode character encoding in file operations|Use UTF-8 encoding for all file operations'

  # --- EN-009: ASCII character class in regex validation ---
  # Matches: [a-z], [A-Z], [a-zA-Z0-9] for user input validation
  '\[[a-zA-Z]-[a-zA-Z]\][[:space:]]*(for|match|test|replace|validate)|low|EN-009|ASCII-only character class in regex validation|Consider Unicode character classes or broader patterns for international input'

  # --- EN-010: String.length for display truncation ---
  # Matches: text.substring(0, 100), str.slice(0, maxLen), text[:50]
  '\.(substring|slice|substr)[[:space:]]*\([[:space:]]*0[[:space:]]*,[[:space:]]*[0-9]+|medium|EN-010|String.substring/slice for display truncation (multi-byte unsafe)|Use Intl.Segmenter for grapheme-safe text truncation'

  # --- EN-011: Locale-dependent sort comparison ---
  # Matches: array.sort(), list.sort(), names.sort()
  '\.(sort)[[:space:]]*\([[:space:]]*\)|medium|EN-011|Default sort without locale-aware comparator|Use localeCompare or Intl.Collator: array.sort((a,b) => a.localeCompare(b, locale))'

  # --- EN-012: Hardcoded separator in number validation ---
  # Matches: /^\d{1,3}(,\d{3})*(\.\d+)?$/ for number parsing
  '[/]["'"'"'][^/]*[,.].*[0-9]{3}|low|EN-012|Hardcoded thousands/decimal separators in number validation regex|Accept locale-dependent separators or use Intl.NumberFormat for parsing'

  # --- EN-013: Non-locale-aware string sort ---
  # Matches: .sort((a, b) => a > b), .sort((a, b) => a < b)
  '\.sort[[:space:]]*\([[:space:]]*\([[:space:]]*[a-z],[[:space:]]*[a-z][[:space:]]*\)[[:space:]]*=>[[:space:]]*[a-z][[:space:]]*[><]|medium|EN-013|String sort using > or < comparison (not locale-aware)|Use localeCompare: .sort((a, b) => a.localeCompare(b, locale))'

  # --- EN-014: Fixed-width character assumption ---
  # Matches: str.padStart(10), str.padEnd(20), "-".repeat(width)
  '\.(padStart|padEnd)[[:space:]]*\([[:space:]]*[0-9]+|medium|EN-014|Fixed-width character display assumption (CJK/emoji vary)|Consider variable-width characters when padding for display'

  # --- EN-015: Missing BOM handling ---
  # Matches: fs.readFileSync without BOM stripping, open() without BOM handling
  'PLACEHOLDER_MISSING_BOM_HANDLING|low|EN-015|File read without BOM (Byte Order Mark) handling|Strip BOM on read: str.replace(/^\\uFEFF/, "") or use encoding that handles BOM'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
i18ncheck_pattern_count() {
  local count=0
  count=$((count + ${#I18NCHECK_HS_PATTERNS[@]}))
  count=$((count + ${#I18NCHECK_TK_PATTERNS[@]}))
  count=$((count + ${#I18NCHECK_DF_PATTERNS[@]}))
  count=$((count + ${#I18NCHECK_RL_PATTERNS[@]}))
  count=$((count + ${#I18NCHECK_SC_PATTERNS[@]}))
  count=$((count + ${#I18NCHECK_EN_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
i18ncheck_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    HS) _patterns_ref=I18NCHECK_HS_PATTERNS ;;
    TK) _patterns_ref=I18NCHECK_TK_PATTERNS ;;
    DF) _patterns_ref=I18NCHECK_DF_PATTERNS ;;
    RL) _patterns_ref=I18NCHECK_RL_PATTERNS ;;
    SC) _patterns_ref=I18NCHECK_SC_PATTERNS ;;
    EN) _patterns_ref=I18NCHECK_EN_PATTERNS ;;
    all)
      i18ncheck_list_patterns "HS"
      i18ncheck_list_patterns "TK"
      i18ncheck_list_patterns "DF"
      i18ncheck_list_patterns "RL"
      i18ncheck_list_patterns "SC"
      i18ncheck_list_patterns "EN"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a category
get_i18ncheck_patterns_for_category() {
  local category="$1"
  case "$category" in
    hs) echo "I18NCHECK_HS_PATTERNS" ;;
    tk) echo "I18NCHECK_TK_PATTERNS" ;;
    df) echo "I18NCHECK_DF_PATTERNS" ;;
    rl) echo "I18NCHECK_RL_PATTERNS" ;;
    sc) echo "I18NCHECK_SC_PATTERNS" ;;
    en) echo "I18NCHECK_EN_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# All category names for iteration
get_all_i18ncheck_categories() {
  echo "hs tk df rl sc en"
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
