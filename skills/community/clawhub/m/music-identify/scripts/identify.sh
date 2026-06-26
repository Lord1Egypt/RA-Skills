#!/usr/bin/env bash
set -euo pipefail

audio_path="${1:-}"
if [[ -z "$audio_path" ]]; then
  echo '{"status":"error","message":"missing audio file path"}'
  exit 2
fi

if [[ ! -f "$audio_path" ]]; then
  echo '{"status":"error","message":"audio file not found"}'
  exit 2
fi

api_key_file="${AUDD_API_KEY_FILE:-$HOME/.config/audd/api_key}"
if [[ ! -f "$api_key_file" ]]; then
  echo '{"status":"error","message":"missing api key"}'
  exit 2
fi

api_key="$(tr -d '\n' < "$api_key_file" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
if [[ -z "$api_key" ]]; then
  echo '{"status":"error","message":"empty api key"}'
  exit 2
fi

response="$(curl -sS -F "file=@${audio_path}" -F "api_token=${api_key}" -F "return=spotify" https://api.audd.io/ || true)"

if [[ -z "$response" ]]; then
  echo '{"status":"error","message":"empty api response"}'
  exit 2
fi

status="$(echo "$response" | jq -r '.status // empty' 2>/dev/null || true)"
if [[ -z "$status" ]]; then
  echo '{"status":"error","message":"invalid api response"}'
  exit 2
fi

if [[ "$status" == "error" ]]; then
  message="$(echo "$response" | jq -r '.error.error_message // .error // "api error"' 2>/dev/null || true)"
  if [[ -z "$message" ]]; then
    message="api error"
  fi
  printf '{"status":"error","message":%s}\n' "$(jq -Rn --arg msg "$message" '$msg')"
  exit 2
fi

result_is_null="$(echo "$response" | jq -r '.result == null' 2>/dev/null || true)"
if [[ "$result_is_null" == "true" ]]; then
  echo '{"status":"not_found"}'
  exit 1
fi

title="$(echo "$response" | jq -r '.result.title // empty')"
artist="$(echo "$response" | jq -r '.result.artist // empty')"
album="$(echo "$response" | jq -r '.result.album // empty')"
spotify_url="$(echo "$response" | jq -r '.result.spotify.external_urls.spotify // empty')"

if [[ -z "$title" && -z "$artist" ]]; then
  echo '{"status":"not_found"}'
  exit 1
fi

jq -n --arg title "$title" --arg artist "$artist" --arg album "$album" --arg spotify_url "$spotify_url" \
  '{status:"found",title:$title,artist:$artist,album:$album,spotify_url:$spotify_url}'
exit 0
