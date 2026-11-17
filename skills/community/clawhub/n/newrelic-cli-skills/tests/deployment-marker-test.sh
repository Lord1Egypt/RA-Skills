#!/bin/bash

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
HELPER="$REPO_ROOT/scripts/deployment-marker.sh"
TEST_TMP=$(mktemp -d "${TMPDIR:-/tmp}/deployment-marker-test.XXXXXX")

cleanup() {
  rm -rf "$TEST_TMP"
}

trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

FAKE_BIN="$TEST_TMP/bin"
INVOCATION_FILE="$TEST_TMP/invoked"
mkdir -p "$FAKE_BIN"
export INVOCATION_FILE

cat > "$FAKE_BIN/newrelic" <<'EOF'
#!/bin/bash
set -eu

: > "$INVOCATION_FILE"

if [ "$#" -ne 11 ] ||
   [ "$1" != "apm" ] ||
   [ "$2" != "deployment" ] ||
   [ "$3" != "create" ] ||
   [ "$4" != "--applicationId" ] ||
   [ "$5" != "$EXPECTED_APP_ID" ] ||
   [ "$6" != "--revision" ] ||
   [ "$7" != "$EXPECTED_REVISION" ] ||
   [ "$8" != "--description" ] ||
   [ "$9" != "$EXPECTED_DESCRIPTION" ] ||
   [ "${10}" != "--user" ] ||
   [ "${11}" != "$EXPECTED_USER" ]; then
  printf '%s\n' "deployment-marker.sh did not preserve the expected argv" >&2
  exit 64
fi
EOF
chmod +x "$FAKE_BIN/newrelic"

fail() {
  printf 'not ok - %s\n' "$1" >&2
  exit 1
}

pass() {
  printf 'ok - %s\n' "$1"
}

assert_rejected() {
  name=$1
  app_id=$2
  revision=$3
  description=$4
  user=$5

  rm -f "$INVOCATION_FILE"
  set +e
  PATH="$FAKE_BIN:$PATH" NEW_RELIC_API_KEY=test-key \
    "$HELPER" "$app_id" "$revision" "$description" "$user" \
    >"$TEST_TMP/output" 2>&1
  status=$?
  set -e

  [ "$status" -ne 0 ] || fail "$name: input was accepted"
  [ ! -e "$INVOCATION_FILE" ] || fail "$name: newrelic was invoked"
  pass "$name"
}

assert_forwarded() {
  name=$1
  app_id=$2
  revision=$3
  description=$4
  user=$5
  expected_revision=$6
  expected_description=$7
  expected_user=$8

  export EXPECTED_APP_ID=$app_id
  export EXPECTED_REVISION=$expected_revision
  export EXPECTED_DESCRIPTION=$expected_description
  export EXPECTED_USER=$expected_user
  rm -f "$INVOCATION_FILE"

  PATH="$FAKE_BIN:$PATH" NEW_RELIC_API_KEY=test-key \
    "$HELPER" "$app_id" "$revision" "$description" "$user" \
    >"$TEST_TMP/output" 2>&1 || fail "$name: helper failed"

  [ -e "$INVOCATION_FILE" ] || fail "$name: newrelic was not invoked"
  pass "$name"
}

BELL_VALUE=$(printf 'rev\007injected')
ESC_VALUE=$(printf 'description\033injected')
DEL_VALUE=$(printf 'user\177injected')

assert_rejected "rejects a nonnumeric application ID" "12x34" "rev" "description" "user"
assert_rejected "rejects non-whitespace controls in revision" "1234" "$BELL_VALUE" "description" "user"
assert_rejected "rejects non-whitespace controls in description" "1234" "rev" "$ESC_VALUE" "user"
assert_rejected "rejects non-whitespace controls in user" "1234" "rev" "description" "$DEL_VALUE"

MULTILINE_REVISION=$(printf 'rev\ninjected')
TABBED_DESCRIPTION=$(printf 'description\tinjected')
RETURNED_USER=$(printf 'user\rinjected')
assert_forwarded \
  "normalizes tabs and line breaks" \
  "1234" \
  "$MULTILINE_REVISION" \
  "$TABBED_DESCRIPTION" \
  "$RETURNED_USER" \
  "rev injected" \
  "description injected" \
  "user injected"

SENTINEL="$TEST_TMP/metacharacters-executed"
export SENTINEL
REVISION='rev; touch "$SENTINEL"'
DESCRIPTION='$(touch "$SENTINEL") `touch "$SENTINEL"`'
USER='deploy-bot && touch "$SENTINEL"'
rm -f "$SENTINEL"
assert_forwarded \
  "forwards shell metacharacters as literal argv" \
  "1234" \
  "$REVISION" \
  "$DESCRIPTION" \
  "$USER" \
  "$REVISION" \
  "$DESCRIPTION" \
  "$USER"

[ ! -e "$SENTINEL" ] || fail "literal metacharacter forwarding: shell syntax was executed"
