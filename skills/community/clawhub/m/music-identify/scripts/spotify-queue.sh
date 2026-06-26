#!/usr/bin/env bash
set -euo pipefail

# Queue a track to Spotify or check playback state
# Usage: spotify-queue.sh queue <spotify_uri>
#        spotify-queue.sh status

TOKEN_FILE="$HOME/.config/spotify/tokens.json"
CREDS_FILE="$HOME/.config/spotify/credentials.json"

if [[ ! -f "$TOKEN_FILE" ]]; then
  echo '{"status":"error","message":"not authenticated. run spotify-auth.py first"}'
  exit 2
fi

if [[ ! -f "$CREDS_FILE" ]]; then
  echo '{"status":"error","message":"missing credentials file"}'
  exit 2
fi

# Read tokens
access_token=$(jq -r '.access_token' "$TOKEN_FILE")
refresh_token=$(jq -r '.refresh_token' "$TOKEN_FILE")
client_id=$(jq -r '.client_id' "$CREDS_FILE")
client_secret=$(jq -r '.client_secret' "$CREDS_FILE")

# Try a request; if 401, refresh token
try_refresh() {
  local response
  response=$(curl -sS -X POST "https://accounts.spotify.com/api/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=refresh_token&refresh_token=${refresh_token}&client_id=${client_id}&client_secret=${client_secret}")

  local new_access
  new_access=$(echo "$response" | jq -r '.access_token // empty')
  if [[ -z "$new_access" ]]; then
    echo '{"status":"error","message":"token refresh failed"}'
    exit 2
  fi

  # Update token file (preserve refresh_token if not returned)
  local new_refresh
  new_refresh=$(echo "$response" | jq -r '.refresh_token // empty')
  if [[ -z "$new_refresh" ]]; then
    new_refresh="$refresh_token"
  fi

  jq --arg at "$new_access" --arg rt "$new_refresh" \
    '. + {access_token: $at, refresh_token: $rt}' "$TOKEN_FILE" > "${TOKEN_FILE}.tmp" \
    && mv "${TOKEN_FILE}.tmp" "$TOKEN_FILE"

  access_token="$new_access"
}

spotify_api() {
  local method="$1"
  local url="$2"
  local data="${3:-}"
  local http_code body

  if [[ -n "$data" ]]; then
    response=$(curl -sS -w "\n%{http_code}" -X "$method" "$url" \
      -H "Authorization: Bearer ${access_token}" \
      -H "Content-Type: application/json" \
      -d "$data")
  else
    response=$(curl -sS -w "\n%{http_code}" -X "$method" "$url" \
      -H "Authorization: Bearer ${access_token}")
  fi

  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "401" ]]; then
    try_refresh
    # Retry
    if [[ -n "$data" ]]; then
      response=$(curl -sS -w "\n%{http_code}" -X "$method" "$url" \
        -H "Authorization: Bearer ${access_token}" \
        -H "Content-Type: application/json" \
        -d "$data")
    else
      response=$(curl -sS -w "\n%{http_code}" -X "$method" "$url" \
        -H "Authorization: Bearer ${access_token}")
    fi
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
  fi

  echo "$http_code"
  echo "$body"
}

action="${1:-}"

case "$action" in
  queue)
    spotify_uri="${2:-}"
    if [[ -z "$spotify_uri" ]]; then
      echo '{"status":"error","message":"missing spotify URI"}'
      exit 1
    fi

    encoded_uri=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${spotify_uri}', safe=''))")
    result=$(spotify_api POST "https://api.spotify.com/v1/me/player/queue?uri=${encoded_uri}")
    code=$(echo "$result" | head -1)
    body=$(echo "$result" | tail -n +2)

    if [[ "$code" == "204" || "$code" == "200" ]]; then
      echo '{"status":"queued","uri":"'"$spotify_uri"'"}'
      exit 0
    elif [[ "$code" == "404" ]]; then
      echo '{"status":"no_device","message":"no active Spotify session found"}'
      exit 1
    else
      msg=$(echo "$body" | jq -r '.error.message // "unknown error"' 2>/dev/null || echo "unknown error")
      echo '{"status":"error","message":"'"$msg"'"}'
      exit 1
    fi
    ;;

  status)
    result=$(spotify_api GET "https://api.spotify.com/v1/me/player")
    code=$(echo "$result" | head -1)
    body=$(echo "$result" | tail -n +2)

    if [[ "$code" == "200" ]]; then
      is_playing=$(echo "$body" | jq -r '.is_playing')
      device=$(echo "$body" | jq -r '.device.name // "unknown"')
      track=$(echo "$body" | jq -r '.item.name // "nothing"')
      artist=$(echo "$body" | jq -r '.item.artists[0].name // "unknown"')
      echo '{"status":"active","is_playing":'"$is_playing"',"device":"'"$device"'","track":"'"$track"'","artist":"'"$artist"'"}'
      exit 0
    elif [[ "$code" == "204" ]]; then
      echo '{"status":"no_device","message":"no active Spotify session"}'
      exit 1
    else
      echo '{"status":"error","message":"could not check playback"}'
      exit 1
    fi
    ;;

  *)
    echo '{"status":"error","message":"usage: spotify-queue.sh queue <uri> | status"}'
    exit 2
    ;;
esac
