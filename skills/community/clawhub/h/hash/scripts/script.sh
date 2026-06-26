#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# hash — Hash & Checksum Tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
###############################################################################

BRAND="Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
DATA_DIR="${HOME}/.local/share/hash"
HISTORY_FILE="${DATA_DIR}/history.log"

mkdir -p "${DATA_DIR}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
die()  { echo "ERROR: $*" >&2; exit 1; }
info() { echo "▸ $*"; }

usage() {
  cat <<'EOF'
hash — Hash & Checksum Tool

USAGE
  script.sh <command> [arguments...]

COMMANDS
  md5    <file_or_text>           Compute MD5 hash
  sha1   <file_or_text>           Compute SHA-1 hash
  sha256 <file_or_text>           Compute SHA-256 hash
  sha512 <file_or_text>           Compute SHA-512 hash
  verify <file> <expected_hash>   Verify a file against a known hash
  compare <file1> <file2>         Compare hashes of two files
  batch  <directory> [algo]       Hash every file in a directory (default: sha256)
  check  <hashfile>               Verify hashes listed in a checksum file
  history                         Show recent hash operations

EOF
  echo "${BRAND}"
}

# Detect the best available tool for a given algorithm
hash_file() {
  local algo="$1" file="$2"
  case "${algo}" in
    md5)
      if command -v md5sum &>/dev/null; then
        md5sum "$file" | awk '{print $1}'
      elif command -v openssl &>/dev/null; then
        openssl dgst -md5 "$file" | awk '{print $NF}'
      else
        die "No md5sum or openssl found"
      fi
      ;;
    sha1)
      if command -v sha1sum &>/dev/null; then
        sha1sum "$file" | awk '{print $1}'
      elif command -v openssl &>/dev/null; then
        openssl dgst -sha1 "$file" | awk '{print $NF}'
      else
        die "No sha1sum or openssl found"
      fi
      ;;
    sha256)
      if command -v sha256sum &>/dev/null; then
        sha256sum "$file" | awk '{print $1}'
      elif command -v openssl &>/dev/null; then
        openssl dgst -sha256 "$file" | awk '{print $NF}'
      else
        die "No sha256sum or openssl found"
      fi
      ;;
    sha512)
      if command -v sha512sum &>/dev/null; then
        sha512sum "$file" | awk '{print $1}'
      elif command -v openssl &>/dev/null; then
        openssl dgst -sha512 "$file" | awk '{print $NF}'
      else
        die "No sha512sum or openssl found"
      fi
      ;;
    *)
      die "Unsupported algorithm: ${algo}"
      ;;
  esac
}

# Hash a string by piping through the same tools
hash_string() {
  local algo="$1" text="$2"
  case "${algo}" in
    md5)
      printf '%s' "$text" | md5sum 2>/dev/null | awk '{print $1}' \
        || printf '%s' "$text" | openssl dgst -md5 | awk '{print $NF}'
      ;;
    sha1)
      printf '%s' "$text" | sha1sum 2>/dev/null | awk '{print $1}' \
        || printf '%s' "$text" | openssl dgst -sha1 | awk '{print $NF}'
      ;;
    sha256)
      printf '%s' "$text" | sha256sum 2>/dev/null | awk '{print $1}' \
        || printf '%s' "$text" | openssl dgst -sha256 | awk '{print $NF}'
      ;;
    sha512)
      printf '%s' "$text" | sha512sum 2>/dev/null | awk '{print $1}' \
        || printf '%s' "$text" | openssl dgst -sha512 | awk '{print $NF}'
      ;;
    *) die "Unsupported algorithm: ${algo}" ;;
  esac
}

# Auto-detect hash algorithm from length
detect_algo() {
  local hash="$1"
  local len=${#hash}
  case "${len}" in
    32)  echo "md5" ;;
    40)  echo "sha1" ;;
    64)  echo "sha256" ;;
    128) echo "sha512" ;;
    *)   echo "unknown" ;;
  esac
}

log_operation() {
  local op="$1" detail="$2"
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') ${op} ${detail}" >> "${HISTORY_FILE}"
}

# Format file size for display
human_size() {
  local bytes="$1"
  if (( bytes >= 1073741824 )); then
    echo "$(awk "BEGIN{printf \"%.2f\", $bytes/1073741824}") GB"
  elif (( bytes >= 1048576 )); then
    echo "$(awk "BEGIN{printf \"%.2f\", $bytes/1048576}") MB"
  elif (( bytes >= 1024 )); then
    echo "$(awk "BEGIN{printf \"%.2f\", $bytes/1024}") KB"
  else
    echo "${bytes} B"
  fi
}

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
cmd_hash() {
  local algo="$1"
  shift
  [[ $# -lt 1 ]] && die "Usage: ${algo} <file_or_text>"
  local input="$1"

  if [[ -f "${input}" ]]; then
    local size
    size=$(stat -c%s "$input" 2>/dev/null || stat -f%z "$input" 2>/dev/null || echo "?")
    local h
    h=$(hash_file "${algo}" "${input}")
    echo "Algorithm : ${algo^^}"
    echo "File      : ${input}"
    echo "Size      : $(human_size "${size}")"
    echo "Hash      : ${h}"
    log_operation "${algo}" "file=${input} hash=${h}"
  else
    local h
    h=$(hash_string "${algo}" "${input}")
    echo "Algorithm : ${algo^^}"
    echo "Input     : ${input}"
    echo "Hash      : ${h}"
    log_operation "${algo}" "text hash=${h}"
  fi
}

cmd_verify() {
  [[ $# -lt 2 ]] && die "Usage: verify <file> <expected_hash>"
  local file="$1" expected="$2"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  # Normalize to lowercase
  expected=$(echo "${expected}" | tr '[:upper:]' '[:lower:]')

  local algo
  algo=$(detect_algo "${expected}")
  [[ "${algo}" == "unknown" ]] && die "Cannot detect algorithm from hash length (${#expected} chars). Supported: 32=md5, 40=sha1, 64=sha256, 128=sha512"

  info "Detected algorithm: ${algo^^} (from hash length)"
  local actual
  actual=$(hash_file "${algo}" "${file}")

  echo "File     : ${file}"
  echo "Algorithm: ${algo^^}"
  echo "Expected : ${expected}"
  echo "Actual   : ${actual}"
  echo ""

  if [[ "${actual}" == "${expected}" ]]; then
    echo "✅ MATCH — File integrity verified"
    log_operation "verify" "file=${file} algo=${algo} result=MATCH"
  else
    echo "❌ MISMATCH — File may be corrupted or tampered with"
    log_operation "verify" "file=${file} algo=${algo} result=MISMATCH"
    exit 1
  fi
}

cmd_compare() {
  [[ $# -lt 2 ]] && die "Usage: compare <file1> <file2>"
  local f1="$1" f2="$2"
  [[ -f "${f1}" ]] || die "File not found: ${f1}"
  [[ -f "${f2}" ]] || die "File not found: ${f2}"

  echo "Comparing files with multiple algorithms..."
  echo ""
  printf "%-8s | %-64s | %-64s | %s\n" "ALGO" "FILE 1" "FILE 2" "MATCH"
  printf "%-8s-+-%-64s-+-%-64s-+-%s\n" "--------" "----------------------------------------------------------------" "----------------------------------------------------------------" "-----"

  local all_match=true
  for algo in md5 sha1 sha256; do
    local h1 h2 match_str
    h1=$(hash_file "${algo}" "${f1}")
    h2=$(hash_file "${algo}" "${f2}")
    if [[ "${h1}" == "${h2}" ]]; then
      match_str="  ✅"
    else
      match_str="  ❌"
      all_match=false
    fi
    printf "%-8s | %-64s | %-64s | %s\n" "${algo^^}" "${h1}" "${h2}" "${match_str}"
  done

  echo ""
  if ${all_match}; then
    echo "✅ Files are identical (all hashes match)"
  else
    echo "❌ Files differ"
  fi
  log_operation "compare" "f1=${f1} f2=${f2} identical=${all_match}"
}

cmd_batch() {
  [[ $# -lt 1 ]] && die "Usage: batch <directory> [algo]"
  local dir="$1"
  local algo="${2:-sha256}"
  [[ -d "${dir}" ]] || die "Directory not found: ${dir}"

  info "Hashing all files in ${dir} with ${algo^^}..."
  echo ""

  local count=0 total_size=0
  local manifest="${DATA_DIR}/batch_$(date +%Y%m%d_%H%M%S).txt"

  while IFS= read -r -d '' file; do
    local h size
    h=$(hash_file "${algo}" "${file}")
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo 0)
    total_size=$((total_size + size))
    count=$((count + 1))
    echo "${h}  ${file}"
    echo "${h}  ${file}" >> "${manifest}"
  done < <(find "${dir}" -type f -print0 | sort -z)

  echo ""
  info "Files hashed : ${count}"
  info "Total size   : $(human_size ${total_size})"
  info "Algorithm    : ${algo^^}"
  info "Manifest saved: ${manifest}"
  log_operation "batch" "dir=${dir} algo=${algo} files=${count}"
}

cmd_check() {
  [[ $# -lt 1 ]] && die "Usage: check <hashfile>"
  local hashfile="$1"
  [[ -f "${hashfile}" ]] || die "Hash file not found: ${hashfile}"

  info "Verifying checksums from ${hashfile}..."
  echo ""

  local total=0 passed=0 failed=0 missing=0

  while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "${line}" || "${line}" == \#* ]] && continue

    local expected_hash file_path
    expected_hash=$(echo "${line}" | awk '{print $1}')
    file_path=$(echo "${line}" | sed 's/^[^ ]* *\*\?//')

    total=$((total + 1))

    if [[ ! -f "${file_path}" ]]; then
      echo "⚠️  MISSING  ${file_path}"
      missing=$((missing + 1))
      continue
    fi

    local algo
    algo=$(detect_algo "${expected_hash}")
    if [[ "${algo}" == "unknown" ]]; then
      echo "⚠️  UNKNOWN  ${file_path} (can't detect algo from hash length)"
      failed=$((failed + 1))
      continue
    fi

    local actual
    actual=$(hash_file "${algo}" "${file_path}")
    if [[ "${actual}" == "${expected_hash}" ]]; then
      echo "✅ OK       ${file_path}"
      passed=$((passed + 1))
    else
      echo "❌ FAILED   ${file_path}"
      failed=$((failed + 1))
    fi
  done < "${hashfile}"

  echo ""
  echo "────────────────────────────────────"
  echo "Total: ${total} | Passed: ${passed} | Failed: ${failed} | Missing: ${missing}"
  if [[ ${failed} -eq 0 && ${missing} -eq 0 ]]; then
    echo "✅ All checksums verified successfully"
  else
    echo "❌ Some checksums failed or files were missing"
    exit 1
  fi
  log_operation "check" "hashfile=${hashfile} total=${total} passed=${passed} failed=${failed}"
}

cmd_history() {
  if [[ ! -f "${HISTORY_FILE}" || ! -s "${HISTORY_FILE}" ]]; then
    echo "No hash operations recorded yet."
    return
  fi
  info "Recent hash operations:"
  echo ""
  tail -20 "${HISTORY_FILE}" | while IFS= read -r line; do
    echo "  ${line}"
  done
  echo ""
  local total
  total=$(wc -l < "${HISTORY_FILE}")
  echo "(${total} total operations)"
}

# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------
main() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 0
  fi

  local cmd="$1"
  shift

  case "${cmd}" in
    md5|sha1|sha256|sha512)
      cmd_hash "${cmd}" "$@"
      ;;
    verify)
      cmd_verify "$@"
      ;;
    compare)
      cmd_compare "$@"
      ;;
    batch)
      cmd_batch "$@"
      ;;
    check)
      cmd_check "$@"
      ;;
    history)
      cmd_history
      ;;
    help|--help|-h)
      usage
      ;;
    *)
      die "Unknown command: ${cmd}. Run with 'help' for usage."
      ;;
  esac
}

main "$@"
