#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

assert_file_exists() {
    if [ ! -f "$1" ]; then
        echo "Expected file to exist: $1" >&2
        exit 1
    fi
}

assert_contains() {
    local file="$1"
    local expected="$2"
    if ! grep -Fq -- "$expected" "$file"; then
        echo "Expected $file to contain: $expected" >&2
        echo "Actual content:" >&2
        cat "$file" >&2
        exit 1
    fi
}

make_fake_pandoc() {
    local bin_dir="$1"
    mkdir -p "$bin_dir"
    cat > "$bin_dir/pandoc" <<'FAKE'
#!/usr/bin/env bash
set -euo pipefail
if [ "${1:-}" = "--version" ]; then
    echo "pandoc 3.1.0"
    exit 0
fi
if [ "${1:-}" = "--list-input-formats" ]; then
    printf 'markdown\nhtml\ndocx\n'
    exit 0
fi
if [ "${1:-}" = "--list-output-formats" ]; then
    printf 'html\ndocx\npdf\nepub\n'
    exit 0
fi
out=""
input=""
while [ "$#" -gt 0 ]; do
    case "$1" in
        -o|--output)
            out="$2"
            shift 2
            ;;
        -o*)
            out="${1#-o}"
            shift
            ;;
        --output=*)
            out="${1#--output=}"
            shift
            ;;
        --*)
            shift
            ;;
        -* )
            shift
            ;;
        *)
            if [ -z "$input" ]; then
                input="$1"
            fi
            shift
            ;;
    esac
done
if [ -z "$out" ]; then
    echo "missing output" >&2
    exit 2
fi
case "$(basename "$input")" in
    flaky.md)
        state="${PANDOC_FAKE_STATE}/flaky.attempts"
        attempts=0
        [ -f "$state" ] && attempts="$(cat "$state")"
        attempts=$((attempts + 1))
        echo "$attempts" > "$state"
        if [ "$attempts" -eq 1 ]; then
            echo "temporary pandoc failure" >&2
            exit 7
        fi
        ;;
    bad.md)
        echo "permanent pandoc failure" >&2
        exit 8
        ;;
esac
mkdir -p "$(dirname "$out")"
printf 'converted %s\n' "$input" > "$out"
FAKE
    chmod +x "$bin_dir/pandoc"
}

test_convert_help() {
    bash "$SKILL_DIR/scripts/convert.sh" --help > "$TMP_ROOT/convert_help.txt"
    assert_contains "$TMP_ROOT/convert_help.txt" "Usage: convert.sh"
}

test_validate_reports_missing_pandoc() {
    local empty_bin="$TMP_ROOT/empty-bin"
    mkdir -p "$empty_bin"
    set +e
    PATH="$empty_bin" /bin/bash "$SKILL_DIR/scripts/validate.sh" "$TMP_ROOT/input.md" -o "$TMP_ROOT/out.html" > "$TMP_ROOT/validate_missing.out" 2>&1
    local status=$?
    set -e
    if [ "$status" -eq 0 ]; then
        echo "Expected validate.sh to fail when pandoc is missing" >&2
        exit 1
    fi
    assert_contains "$TMP_ROOT/validate_missing.out" "pandoc is not installed"
    assert_contains "$TMP_ROOT/validate_missing.out" "install_pandoc.sh"
}

test_install_helper_dry_run_recommends_available_manager() {
    local bin_dir="$TMP_ROOT/fake-bin-install"
    mkdir -p "$bin_dir"
    cat > "$bin_dir/brew" <<'FAKEBREW'
#!/usr/bin/env bash
printf 'Homebrew 4.0.0\n'
FAKEBREW
    chmod +x "$bin_dir/brew"

    PATH="$bin_dir:/usr/bin:/bin" bash "$SKILL_DIR/scripts/install_pandoc.sh" > "$TMP_ROOT/install_dry_run.out" 2>&1
    assert_contains "$TMP_ROOT/install_dry_run.out" "Pandoc is not installed"
    assert_contains "$TMP_ROOT/install_dry_run.out" "brew install pandoc"
    assert_contains "$TMP_ROOT/install_dry_run.out" "Re-run with --yes"
}

test_install_helper_noops_when_pandoc_exists() {
    local bin_dir="$TMP_ROOT/fake-bin-installed"
    make_fake_pandoc "$bin_dir"
    PATH="$bin_dir:/usr/bin:/bin" PANDOC_FAKE_STATE="$TMP_ROOT" bash "$SKILL_DIR/scripts/install_pandoc.sh" > "$TMP_ROOT/install_noop.out" 2>&1
    assert_contains "$TMP_ROOT/install_noop.out" "Pandoc is already installed"
    assert_contains "$TMP_ROOT/install_noop.out" "pandoc 3.1.0"
}

test_convert_with_fake_pandoc() {
    local bin_dir="$TMP_ROOT/fake-bin-convert"
    make_fake_pandoc "$bin_dir"
    mkdir -p "$TMP_ROOT/single"
    printf '# Hello\n' > "$TMP_ROOT/single/input.md"
    PATH="$bin_dir:$PATH" PANDOC_FAKE_STATE="$TMP_ROOT" bash "$SKILL_DIR/scripts/convert.sh" "$TMP_ROOT/single/input.md" -o "$TMP_ROOT/single/out.html" --toc --metadata title=Hello > "$TMP_ROOT/convert.out" 2>&1
    assert_file_exists "$TMP_ROOT/single/out.html"
    assert_contains "$TMP_ROOT/convert.out" "Conversion successful"
}

test_batch_retries_and_reports_failures() {
    local bin_dir="$TMP_ROOT/fake-bin-batch"
    make_fake_pandoc "$bin_dir"
    mkdir -p "$TMP_ROOT/docs/sub"
    printf '# Good\n' > "$TMP_ROOT/docs/good.md"
    printf '# Flaky\n' > "$TMP_ROOT/docs/sub/flaky.md"
    printf '# Bad\n' > "$TMP_ROOT/docs/bad.md"

    set +e
    PATH="$bin_dir:$PATH" PANDOC_FAKE_STATE="$TMP_ROOT" python3 "$SKILL_DIR/scripts/batch_convert.py" "$TMP_ROOT/docs" --output-dir "$TMP_ROOT/out" --to html --retries 1 --retry-delay 0 --report "$TMP_ROOT/report.md" --json-report "$TMP_ROOT/report.json" > "$TMP_ROOT/batch.out" 2>&1
    local status=$?
    set -e
    if [ "$status" -eq 0 ]; then
        echo "Expected batch conversion to fail when one file permanently fails" >&2
        exit 1
    fi

    assert_file_exists "$TMP_ROOT/out/good.html"
    assert_file_exists "$TMP_ROOT/out/sub/flaky.html"
    assert_file_exists "$TMP_ROOT/report.md"
    assert_file_exists "$TMP_ROOT/report.json"
    assert_contains "$TMP_ROOT/batch.out" "[1/3]"
    assert_contains "$TMP_ROOT/batch.out" "Retry 1/1"
    assert_contains "$TMP_ROOT/batch.out" "Summary: 2 succeeded, 1 failed, 0 skipped"
    assert_contains "$TMP_ROOT/report.md" "bad.md"
    assert_contains "$TMP_ROOT/report.json" "\"failed\": 1"
}

test_convert_help
test_validate_reports_missing_pandoc
test_install_helper_dry_run_recommends_available_manager
test_install_helper_noops_when_pandoc_exists
test_convert_with_fake_pandoc
test_batch_retries_and_reports_failures

echo "All tests passed"
