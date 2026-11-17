#!/bin/sh

set -eu

API_URL='https://longxia.cool/api/scans'
USER_AGENT='longxia-scan-skill/1.0.0'

usage() {
  printf '%s\n' \
    'Usage:' \
    '  scan.sh scan <public-github-url>' \
    '  scan.sh report <scan-id>'
}

fail() {
  printf 'longxia-scan: %s\n' "$1" >&2
  exit 2
}

require_curl() {
  command -v curl >/dev/null 2>&1 ||
    fail 'curl is required but was not found.'
}

scan_url() {
  github_url=$1

  case "$github_url" in
    https://github.com/*) ;;
    *) fail 'only public https://github.com URLs are supported.' ;;
  esac

  [ "${#github_url}" -le 500 ] ||
    fail 'the GitHub URL must be 500 characters or fewer.'

  case "$github_url" in
    *[![:print:]]* | *'"'* | *'\'*)
      fail 'the GitHub URL contains unsupported characters.'
      ;;
  esac

  printf '{"url":"%s"}' "$github_url" |
    curl \
      --fail-with-body \
      --silent \
      --show-error \
      --connect-timeout 10 \
      --max-time 60 \
      --request POST \
      --header 'Accept: application/json' \
      --header 'Content-Type: application/json' \
      --header "User-Agent: $USER_AGENT" \
      --data-binary @- \
      "$API_URL"
}

read_report() {
  scan_id=$1

  [ "${#scan_id}" -eq 36 ] ||
    fail 'the scan ID must be a 36-character UUID.'
  case "$scan_id" in
    *[!0-9a-fA-F-]*)
      fail 'the scan ID must be a UUID.'
      ;;
  esac

  curl \
    --fail-with-body \
    --silent \
    --show-error \
    --connect-timeout 10 \
    --max-time 30 \
    --header 'Accept: application/json' \
    --header "User-Agent: $USER_AGENT" \
    "$API_URL/$scan_id"
}

require_curl

command_name=${1:-}
case "$command_name" in
  scan)
    [ "$#" -eq 2 ] || {
      usage >&2
      exit 2
    }
    scan_url "$2"
    ;;
  report)
    [ "$#" -eq 2 ] || {
      usage >&2
      exit 2
    }
    read_report "$2"
    ;;
  -h | --help | help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
