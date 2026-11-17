#!/usr/bin/env bash
# keyguard.test.sh — where OFOX_API_KEY is allowed to go, and what the two
# escape hatches are not allowed to do.
#
# Three guards are under test, each exercised by constructing the input it
# exists to refuse rather than by watching a good input pass:
#
#   R2  OFOX_API_BASE_URL must be https (loopback excepted) and must say out
#       loud which host is about to receive the key. This script has no
#       polling URL — every request it makes is built from API_BASE and no URL
#       from a response body is ever fetched — so the sibling video script's
#       R1 has no counterpart here, and that absence is asserted below rather
#       than assumed.
#   R3  --extra-json is merged last and wins over the flags, so a key that has
#       a flag is refused; an explicitly EMPTY value is refused too, instead
#       of being indistinguishable from the flag not being passed.
#   R4  --extra-form is a passthrough into curl's -F, where a value starting
#       '@' uploads that local file and one starting '<' sends that local
#       file's contents. `--extra-form "mask=@$HOME/.ssh/id_rsa"` was a
#       working file exfiltration primitive; ordinary key=value pairs are
#       untouched.
#
# Free by construction: every rejection happens before the one billable call,
# and the accepted cases stop at --dry-run or die on an unroutable base.
#
# Run: bash references/test/keyguard.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-image.sh"

if [ ! -f "$TARGET" ]; then
  echo "FATAL: cannot find ofox-image.sh at $TARGET" >&2
  exit 1
fi

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
export XDG_CACHE_HOME="$WORK/cache"

# Not a credential — the script only checks that OFOX_API_KEY is non-empty.
# Through a variable, and a plain dictionary word, because a key-shaped literal
# assigned straight to OFOX_API_KEY is what tripped ClawHub's static scan.
PLACEHOLDER=placeholder
export OFOX_API_KEY="$PLACEHOLDER"
# Loopback, so the override is legal, and port 1 is not listening anywhere.
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"

# A real PNG header is all the input-format check needs; nothing here looks at
# the picture.
IMG="$WORK/in.png"
printf '\211PNG\r\n\032\n' >"$IMG"
# A file that must never leave this machine. Its content is what an --extra-form
# exfiltration would put in the request body.
SECRET="$WORK/secret.txt"
printf 'a-file-the-user-never-asked-to-upload\n' >"$SECRET"

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "${2:-}"
  FAIL=$((FAIL + 1))
}

gen() { bash "$TARGET" generate --prompt x --quality low --dry-run --out-dir "$WORK/out" "$@" 2>&1; }
edt() { bash "$TARGET" edit --image "$IMG" --prompt x --dry-run --out-dir "$WORK/out" "$@" 2>&1; }

mkdir -p "$WORK/out"

# ---------------------------------------------------------------------------
# R2 — OFOX_API_BASE_URL
#
# `check` makes no network call, which makes it the right probe: the startup
# guard is what is under test, not any request.
# ---------------------------------------------------------------------------

echo "=== R2: OFOX_API_BASE_URL is validated and announced ==="

base_case() {
  # base_case DESC WANT_EXIT WANT_PATTERN -- BASE_VALUE ("" means unset)
  local desc="$1" want_code="$2" want="$3" value="$5"
  local out code
  if [ -z "$value" ]; then
    out=$(env -u OFOX_API_BASE_URL bash "$TARGET" check 2>&1)
  else
    out=$(OFOX_API_BASE_URL="$value" bash "$TARGET" check 2>&1)
  fi
  code=$?
  if [ "$code" -ne "$want_code" ]; then
    fail "$desc" "expected exit $want_code, got $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    return
  fi
  if [ -n "$want" ] && ! printf '%s' "$out" | grep -q -- "$want"; then
    fail "$desc" "exit $want_code as expected, but nothing mentioned '$want': $(printf '%s' "$out" | head -3 | tr '\n' ' ')"
    return
  fi
  pass "$desc"
}

base_case "a plaintext non-loopback base is refused" 2 "not https://" -- \
  "http://staging.example.com/v1"
base_case "the refusal says why: the key rides in a header on every request" 2 "Authorization" -- \
  "http://staging.example.com/v1"
base_case "a value that is not a URL at all is refused" 2 "not an http:// or https:// URL" -- \
  "staging.example.com"
base_case "a non-http scheme is refused" 2 "not an http:// or https:// URL" -- \
  "ftp://staging.example.com/v1"
base_case "https to another host is allowed" 0 "" -- \
  "https://staging.example.com/v1"
base_case "and it names the host that will receive the key" 0 "staging.example.com" -- \
  "https://staging.example.com/v1"
base_case "plaintext IS allowed on loopback (local test servers)" 0 "" -- \
  "http://127.0.0.1:1/v1"
base_case "plaintext IS allowed on localhost by name" 0 "localhost" -- \
  "http://localhost:8080/v1"

out=$(env -u OFOX_API_BASE_URL bash "$TARGET" check 2>&1)
if printf '%s' "$out" | grep -q 'OFOX_API_BASE_URL'; then
  fail "an unset OFOX_API_BASE_URL must say nothing" "$(printf '%s' "$out" | head -1)"
else
  pass "no override, no notice (the warning stays worth reading)"
fi

out=$(OFOX_API_BASE_URL="https://staging.example.com/v1" bash "$TARGET" check 2>/dev/null)
if printf '%s' "$out" | grep -q 'OFOX_API_BASE_URL'; then
  fail "the override notice must go to stderr" "it appeared on stdout"
else
  pass "the override notice goes to stderr, not into the stdout contract"
fi

# The claim this suite's header makes about R1 having no counterpart here is
# checked, not asserted in prose: every credentialed request must be built
# from API_BASE.
auth_lines=$(grep -c 'Authorization: Bearer' "$TARGET")
api_base_posts=$(grep -c '\-X POST "$API_BASE/' "$TARGET")
if [ "$auth_lines" -eq 2 ] && [ "$api_base_posts" -eq 2 ]; then
  pass "both authenticated requests are still posted to \$API_BASE, none to a response URL"
else
  fail "the set of authenticated requests changed" \
    "$auth_lines Authorization headers, $api_base_posts posts to \$API_BASE — if a URL now comes from a response, it needs the video script's origin check"
fi

# ---------------------------------------------------------------------------
# R4 — --extra-form
# ---------------------------------------------------------------------------

echo
echo "=== R4: --extra-form cannot be turned into a file picker ==="

form_reject() {
  # form_reject DESC VALUE
  local desc="$1" value="$2" out code
  out=$(edt --extra-form "$value")
  code=$?
  if [ "$code" -ne 1 ]; then
    fail "$desc" "expected exit 1, got $code: $(printf '%s' "$out" | grep -i error | head -1)"
    return
  fi
  if ! printf '%s' "$out" | grep -qi 'filesystem instruction'; then
    fail "$desc" "rejected, but not for the stated reason: $(printf '%s' "$out" | grep -i error | head -1)"
    return
  fi
  pass "$desc"
}

form_reject "an '@path' value (curl would upload that file) is refused" "mask=@$SECRET"
form_reject "a '<path' value (curl would send that file's contents) is refused" "mask=<$SECRET"
form_reject "a relative @path is refused too" "mask=@secret.txt"
form_reject "@ with no path is still refused" "mask=@"
form_reject "an unrelated field name does not exempt it" "anything=@$SECRET"

# The concrete thing this prevents: the field never reaches the assembled
# form, so curl is never handed the '@path' that would upload it.
#
# Deliberately NOT asserted here: that the file's content is absent from the
# output. It is absent whether or not this guard exists — a dry run prints
# field NAMES only and sends nothing — so that assertion could not fail and
# would read as coverage it does not have.
out=$(edt --extra-form "mask=@$SECRET")
if printf '%s' "$out" | grep -q '^FORM_FIELDS'; then
  fail "the request form was assembled anyway" "$(printf '%s' "$out" | grep '^FORM_FIELDS')"
else
  pass "the refusal happens before the multipart form is assembled"
fi

echo
echo "=== R4: ordinary --extra-form pairs are untouched ==="
out=$(edt --extra-form "mask=plain-value")
if [ $? -eq 0 ] && printf '%s' "$out" | grep -q '^FORM_FIELDS.* mask$'; then
  pass "a plain key=value still reaches the form"
else
  fail "a plain --extra-form pair must keep working" "$(printf '%s' "$out" | grep -E '^FORM_FIELDS|ERROR' | head -1)"
fi
for v in "k=user@example.com" "k=a<b" "k=" "k=https://example.com/x.png"; do
  out=$(edt --extra-form "$v")
  if [ $? -eq 0 ]; then
    pass "accepted: --extra-form '$v'"
  else
    fail "this must not be refused: --extra-form '$v'" "$(printf '%s' "$out" | grep -i error | head -1)"
  fi
done
# The script's own uploads are built from --image/--image-url, not from
# --extra-form, so they must be unaffected by the rule above.
out=$(edt)
if [ $? -eq 0 ] && printf '%s' "$out" | grep -q '^FORM_FIELDS image '; then
  pass "the script's own image upload (-F image=@PATH) still happens"
else
  fail "the R4 rule wounded the real upload path" "$(printf '%s' "$out" | grep -E '^FORM_FIELDS|ERROR' | head -1)"
fi
out=$(bash "$TARGET" edit --image-url "https://example.com/a.png" --prompt x \
  --dry-run --out-dir "$WORK/out" 2>&1)
if [ $? -eq 0 ] && printf '%s' "$out" | grep -q '^FORM_FIELDS image_url '; then
  pass "and so does the -F image_url=<TEMPFILE form of it"
else
  fail "the image_url path broke" "$(printf '%s' "$out" | grep -E '^FORM_FIELDS|ERROR' | head -1)"
fi
# Pre-existing --extra-form rules must still hold.
out=$(edt --extra-form "novalue")
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'KEY=VALUE'; then
  pass "a value with no '=' is still rejected as before"
else
  fail "the KEY=VALUE check regressed" "$(printf '%s' "$out" | grep -i error | head -1)"
fi
out=$(edt --extra-form "model=other")
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'collides'; then
  pass "a field that has a flag is still rejected as before"
else
  fail "the collision check regressed" "$(printf '%s' "$out" | grep -i error | head -1)"
fi

# ---------------------------------------------------------------------------
# R3, on the edit path: --extra-form must not override a priced or validated
# field either
#
# The list of colliding keys was image/image_url/model/prompt, while the same
# function also sets quality, size, n, output_format and background from flags.
# A duplicate multipart part skips that flag's validation and is appended AFTER
# print_edit_estimate has run, so `--extra-form "n=10"` printed `N 1`, quoted
# one image, and asked the server for ten.
#
# The list under test is EXTRACTED from the script's own form builders rather
# than retyped here. Retyping it would make this a second hardcoded copy that
# agrees with the first by construction — the shape falsifiable-gates.md calls
# "the check and the code share one wrong premise", which is precisely how the
# missing five survived review. A new `form+=(--form-string "x=$x")` with no
# entry in the guard turns this red with no edit to this file.
# ---------------------------------------------------------------------------

echo
echo "=== R3(edit): every field the form builder sets from a flag is refused ==="

form_owned=$(grep -oE 'form\+=\((-F|--form-string) "[a-z_]+=' "$TARGET" \
  | sed -E 's/.*"([a-z_]+)=/\1/' | sort -u)
owned_count=$(printf '%s\n' "$form_owned" | grep -c .)
# An extractor that quietly matches nothing would make every loop below
# vacuous and this whole section green, so the count is asserted first.
if [ "$owned_count" -eq 9 ]; then
  pass "the form builder sets 9 fields from flags: $(printf '%s' "$form_owned" | tr '\n' ' ')"
else
  fail "the extraction found $owned_count field(s), expected 9" \
    "either a flag was added/removed (update this number and the guard) or the grep stopped matching: $(printf '%s' "$form_owned" | tr '\n' ' ')"
fi

for k in $form_owned; do
  out=$(edt --extra-form "$k=whatever")
  code=$?
  if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'collides'; then
    pass "--extra-form '$k=...' is refused; the flag owns that field"
  else
    fail "--extra-form '$k=...' reached the form" \
      "exit $code — this field is set from a flag, validated there and priced before the form is assembled: $(printf '%s' "$out" | grep -E '^FORM_FIELDS|ERROR' | head -1)"
  fi
done

# The money assertion, in the units of the promise rather than on a proxy for
# it: `n` multiplies the bill. Asserting "exit 1" alone would stay green if the
# refusal moved below print_edit_estimate, which is where the damage is — the
# user approves the quote, not the exit code. So assert that no quote was
# printed at all for a request the script will not send.
out=$(edt --extra-form "n=10")
if printf '%s' "$out" | grep -q 'Estimated cost:'; then
  fail "a cost was quoted for a request that was then refused" \
    "$(printf '%s' "$out" | grep 'Estimated cost:' | head -1)"
elif printf '%s' "$out" | grep -q '^N '; then
  fail "the refused request still reported an image count" \
    "$(printf '%s' "$out" | grep '^N ' | head -1)"
else
  pass "no estimate and no N line for a refused '--extra-form n=10' — the guard is above the quote, not below it"
fi

# And the must-not-fire side: a name that merely CONTAINS an owned field is a
# different field and still passes. Precision beats coverage.
for v in "n_hint=2" "mask_hint=none" "size_note=big" "background_music=off"; do
  out=$(edt --extra-form "$v")
  if [ $? -eq 0 ]; then
    pass "accepted: --extra-form '$v' (not an owned field name)"
  else
    fail "this must not be refused: --extra-form '$v'" "$(printf '%s' "$out" | grep -i error | head -1)"
  fi
done

# ---------------------------------------------------------------------------
# R4, the half that is not behind --extra-form
#
# Refusing '@' in --extra-form closes the escape hatch and nothing else. curl
# applies the same two prefixes to EVERY -F value, including one that arrived
# as free text through --prompt, which a user may legitimately open with '@'
# ("@golden hour, ...") or '<'. So the fields this script sets literally go
# through --form-string.
#
# Asserted in the property's own units — what CURL does with the argument
# vector this script builds — not on the spelling of the vector. The run below
# hands the captured arguments to the real curl binary, pointed at a closed
# loopback port, with a prompt naming a file that does not exist:
#
#   -F            -> exit 26, "Failed to open/read local data", before connecting
#   --form-string -> exit 7, "couldn't connect", the value never read as a path
#
# So reverting the fix turns this red with no edit here, and it stays honest if
# the flag is ever spelled differently.
# ---------------------------------------------------------------------------

echo
echo "=== R4: a --prompt that opens with '@' is a prompt, not a file read ==="

cat > "$WORK/capture.sh" <<'EOF'
set -u
# Log only the edits request; the catalog fetch shares this stub.
curl() {
  case " $* " in
    *"/images/edits"*) printf '%s\n' "$@" > "$ARGLOG" ;;
  esac
  return 1
}
export -f curl
bash "$TARGET" edit "$@"
EOF

capture_edit_args() {
  : > "$WORK/curl.args"
  ARGLOG="$WORK/curl.args" TARGET="$TARGET" \
    bash "$WORK/capture.sh" --image "$IMG" --out-dir "$WORK/out" "$@" >/dev/null 2>&1
  [ -s "$WORK/curl.args" ]
}

replay_curl_rc() {
  # Replay the captured argument vector through the real curl. API_BASE is the
  # unroutable loopback set at the top of this file, so nothing is ever sent.
  local args=() line
  while IFS= read -r line; do args+=("$line"); done < "$WORK/curl.args"
  command curl --connect-timeout 2 "${args[@]}" >/dev/null 2>&1
  printf '%s' "$?"
}

MISSING="$WORK/no-such-file-$$.txt"
rm -f "$MISSING"

if capture_edit_args --prompt "@$MISSING"; then
  rc="$(replay_curl_rc)"
  if [ "$rc" = "26" ]; then
    fail "curl read the prompt as a file path" \
      "exit 26 is curl's 'Failed to open/read local data' — the prompt became an upload"
  elif [ "$rc" = "7" ]; then
    pass "a '@path' prompt reaches curl as a literal value (connect failure, not a file read)"
  else
    fail "the replay did not reach the connect stage" "curl exit $rc"
  fi
else
  fail "could not capture the edit request's curl arguments" "no /images/edits call was made"
fi

# The same for '<', curl's other filesystem prefix.
if capture_edit_args --prompt "<$MISSING"; then
  rc="$(replay_curl_rc)"
  if [ "$rc" = "7" ]; then
    pass "a '<path' prompt reaches curl as a literal value too"
  else
    fail "a '<path' prompt was not sent literally" "curl exit $rc (26 = read as a file)"
  fi
fi

# Control, so the two cases above are not both green for some unrelated reason:
# with the SAME replay machinery, an -F value that names a missing file really
# does produce 26. Without this, "exit 7" could mean the guard works or that
# curl never applies the prefix at all.
rc_control=$(command curl --connect-timeout 2 -F "prompt=@$MISSING" \
  "$OFOX_API_BASE_URL/images/edits" >/dev/null 2>&1; printf '%s' "$?")
if [ "$rc_control" = "26" ]; then
  pass "control: the same value under -F IS read as a file (exit 26), so 7 means something"
else
  fail "the control did not reproduce the defect" \
    "expected curl exit 26 from -F with a missing file, got $rc_control"
fi

# And an ordinary prompt still travels, with the field names unchanged.
out=$(edt --prompt "an ordinary prompt")
if [ $? -eq 0 ] && printf '%s' "$out" | grep -q '^FORM_FIELDS image model prompt'; then
  pass "--form-string did not disturb the FORM_FIELDS contract"
else
  fail "the dry-run field list changed shape" "$(printf '%s' "$out" | grep -E '^FORM_FIELDS|ERROR' | head -1)"
fi

# ---------------------------------------------------------------------------
# R3 — --extra-json
# ---------------------------------------------------------------------------

echo
echo "=== R3: an explicitly empty --extra-json is an error, not 'not passed' ==="
out=$(gen --extra-json "")
code=$?
if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'empty value'; then
  pass "--extra-json '' is rejected before anything is sent"
else
  fail "an empty --extra-json must not be treated as 'flag not passed'" \
    "exit $code: $(printf '%s' "$out" | grep -i error | head -1)"
fi

echo
echo "=== R3: omitting the flag behaves byte-for-byte as it always did ==="
payload_of() {
  bash "$TARGET" generate --prompt x --quality low --size 1024x1024 --dry-run \
    --out-dir "$WORK/out" --model openai/gpt-image-2 "$@" 2>/dev/null |
    grep -E '^(STATUS|MODEL|QUALITY|SIZE|N) '
}
omitted="$(payload_of)"
empty_obj="$(payload_of --extra-json '{}')"
if [ -n "$omitted" ] && [ "$omitted" = "$empty_obj" ]; then
  pass "no --extra-json produces the same request as --extra-json '{}'"
else
  fail "the omitted path changed" "omitted='$omitted' vs '{}'='$empty_obj'"
fi

echo
echo "=== R3: a key that has a flag cannot be smuggled in through the hatch ==="
clash_case() {
  local json="$1" want="$2" out code
  out=$(gen --extra-json "$json")
  code=$?
  if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -q -- "$want"; then
    pass "rejected: $json"
  else
    fail "should be rejected: $json" "exit $code: $(printf '%s' "$out" | grep -i error | head -1)"
  fi
}
clash_case '{"model":"openai/gpt-image-2"}' 'model'
clash_case '{"prompt":"something else"}' 'prompt'
clash_case '{"quality":"high"}' 'quality'
clash_case '{"size":"1792x1024"}' 'size'
clash_case '{"n":10}' 'n'
clash_case '{"output_format":"webp"}' 'output_format'
clash_case '{"background":"transparent"}' 'background'
clash_case '{"quality":"high","size":"1792x1024"}' 'quality, size'
# The reason the rule exists: a high/1792x1024 body behind a low/default quote
# is 26x the price. Assert no estimate was printed for the wrong request.
out=$(gen --extra-json '{"quality":"high","size":"1792x1024"}')
if ! printf '%s' "$out" | grep -qi 'estimated'; then
  pass "the clash is caught before a price is quoted for the wrong request"
else
  fail "a quote was printed for parameters the body would have overridden" \
    "$(printf '%s' "$out" | grep -i estimated | head -1)"
fi

echo
echo "=== R3: everything without a flag still passes through ==="
out=$(gen --extra-json '{"extra_body":{"provider":{"type":"openai"}}}')
if [ $? -eq 0 ] && printf '%s' "$out" | grep -q '^STATUS dry_run$'; then
  pass "the documented extra_body.provider.type passthrough still works"
else
  fail "the documented passthrough broke" "$(printf '%s' "$out" | grep -i error | head -1)"
fi
out=$(gen --extra-json '{"some_field_with_no_flag":"v"}')
if [ $? -eq 0 ]; then
  pass "a field with no flag is still merged without complaint"
else
  fail "an unflagged field must still pass through" "$(printf '%s' "$out" | grep -i error | head -1)"
fi

echo
echo "=== R3: the pre-existing --extra-json rules still hold ==="
out=$(gen --extra-json '{nope}')
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'not valid JSON'; then
  pass "invalid JSON is still reported as invalid JSON"
else
  fail "the JSON check regressed" "$(printf '%s' "$out" | grep -i error | head -1)"
fi
out=$(gen --extra-json '{"input_images":["https://example.com/a.png"]}')
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'out of scope'; then
  pass "input_images is still out of scope"
else
  fail "the input_images check regressed" "$(printf '%s' "$out" | grep -i error | head -1)"
fi
out=$(gen --extra-json '{"stream":true}')
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'streamed'; then
  pass "stream:true is still refused"
else
  fail "the stream check regressed" "$(printf '%s' "$out" | grep -i error | head -1)"
fi
for bad in '[1,2]' '"text"' '42' 'null' 'false'; do
  out=$(gen --extra-json "$bad")
  if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'must be a JSON object'; then
    pass "refused a non-object --extra-json: $bad"
  else
    fail "a non-object --extra-json must be refused: $bad" \
      "$(printf '%s' "$out" | grep -i error | head -1)"
  fi
done

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
