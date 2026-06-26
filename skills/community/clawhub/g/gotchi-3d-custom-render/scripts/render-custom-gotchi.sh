#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQUEST_PATH="${ROOT}/Requests/custom-request.json"
WEARABLE_INDEX_PATH="${ROOT}/references/wearables.tsv"
WEARABLE_DB_PATH="$(find "${ROOT}/unity/GotchiCustomRenderer/Library/PackageCache" -path '*/Runtime/Data/AavegotchiWearableDataBase.asset' -print -quit 2>/dev/null || true)"

slug="custom-gotchi"
haunt_id=1
collateral="ETH"
eye_shape="Mythical"
eye_color="High"
skin_id=0
background="arcade-purple"
pose="idle"
body=0
face=0
eyes=0
head=0
pet=0
hand_left=0
hand_right=0
preset=""
render_mode="hosted"
write_only=0
find_wearable_query=""

usage() {
  cat <<'EOF'
Usage:
  render-custom-gotchi.sh [options]

Core options:
  --preset NAME
  --slug NAME
  --haunt-id N
  --collateral NAME
  --eye-shape NAME
  --eye-color NAME
  --skin-id N
  --background VALUE
  --bg VALUE
  --pose NAME

Wearable options:
  --body VALUE
  --face VALUE
  --eyes VALUE
  --head VALUE
  --pet VALUE
  --hand-left VALUE
  --hand-right VALUE
  --left-hand VALUE
  --right-hand VALUE
  --slot SLOT=VALUE
  --wearables LIST

Helpers:
  --find-wearable QUERY
  --render-mode MODE
  --hosted-only
  --unity-only
  --print-presets
  --write-only
  --help

Render mode behavior:
  hosted  default; hosted Aavegotchi renderer only
  auto    hosted renderer first, local Unity fallback
  unity   local Unity renderer only

Examples:
  render-custom-gotchi.sh --find-wearable aagent
  render-custom-gotchi.sh --preset aagent-eth
  render-custom-gotchi.sh --preset blank-eth --background studio-cream --pose portrait
  render-custom-gotchi.sh --collateral ETH --eye-shape Mythical --slot head=56 --slot hand-right=58
  render-custom-gotchi.sh --body 'Aagent Shirt' --face 'Aagent Headset' --eyes 'Aagent Shades' --head 'Aagent Fedora Hat'
  render-custom-gotchi.sh --wearables 'head=56,hand-right=58' --bg gotchi-radio
  render-custom-gotchi.sh --preset aagent-eth --render-mode hosted
EOF
}

print_presets() {
  cat <<'EOF'
Available presets:
  blank-eth        ETH mythical blank gotchi with classic framing
  aagent-eth       ETH mythical gotchi with Aagent shirt + pistol
  portrait-eth     ETH mythical blank gotchi tuned for portrait framing

Background aliases:
  arcade-purple    -> #806AFB
  studio-cream     -> #F4EDE1
  slime-lime       -> #D8FF5E
  night-ink        -> #131722
  soft-sky         -> #D9F3FF
  gotchi-radio     -> #1DDA8D
  transparent      -> transparent

Pose aliases:
  idle             front-facing studio default
  portrait         tighter head/upper-body framing
  hero             slight three-quarter turn
  left             rotate left
  right            rotate right

Wearable values:
  Every wearable flag accepts either a numeric ID or a quoted wearable name.
  Example: --head 'Aagent Fedora Hat' --hand-right 'Aagent Pistol'
EOF
}

normalize_lookup_key() {
  printf '%s' "${1:-}" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+//g'
}

wearable_index_stream() {
  if [[ -f "${WEARABLE_INDEX_PATH}" ]]; then
    cat "${WEARABLE_INDEX_PATH}"
    return
  fi

  if [[ -z "${WEARABLE_DB_PATH}" || ! -f "${WEARABLE_DB_PATH}" ]]; then
    echo "Wearable database not found. Expected ${WEARABLE_INDEX_PATH} or a Unity SDK package cache." >&2
    exit 1
  fi

  awk '
    /^  HeadWearables:/ {slot="head"; next}
    /^  BodyWearables:/ {slot="body"; next}
    /^  FaceWearables:/ {slot="face"; next}
    /^  EyeWearables:/ {slot="eyes"; next}
    /^  HandWearables:/ {slot="hand"; next}
    /^  PetWearables:/ {slot="pet"; next}
    /WearableID:/ {
      id=$3
      next
    }
    /WearableName:/ {
      name=$0
      sub(/^[[:space:]]*WearableName:[[:space:]]*/, "", name)
      print id "\t" slot "\t" name
    }
  ' "${WEARABLE_DB_PATH}"
}

print_wearable_matches() {
  local raw="${1:-}"
  local key=""
  local id=""
  local slot=""
  local name=""
  local name_key=""
  local found=0

  if [[ -z "$raw" ]]; then
    echo "Provide a search query. Example: --find-wearable aagent" >&2
    exit 1
  fi

  key="$(normalize_lookup_key "$raw")"
  printf 'Wearable matches for "%s"\n' "$raw"
  printf '%-6s %-8s %s\n' "ID" "SLOT" "NAME"

  while IFS=$'\t' read -r id slot name; do
    name_key="$(normalize_lookup_key "$name")"
    if [[ "$name_key" == *"$key"* || "$key" == *"$name_key"* ]]; then
      printf '%-6s %-8s %s\n' "$id" "$slot" "$name"
      found=1
    fi
  done < <(wearable_index_stream)

  if [[ "$found" -eq 0 ]]; then
    echo "No wearable matches found." >&2
    exit 1
  fi
}

resolve_wearable_id() {
  local raw="${1:-}"
  local key
  local id=""
  local name=""
  local name_key=""
  local match_count=0
  local first_match_id=""
  local first_match_name=""
  local suggestions=()

  if [[ -z "$raw" ]]; then
    echo "0"
    return
  fi

  if [[ "$raw" =~ ^[0-9]+$ ]]; then
    echo "$raw"
    return
  fi

  key="$(normalize_lookup_key "$raw")"
  case "$key" in
    ""|none|empty|blank|off|nil|null|default) echo "0"; return ;;
  esac

  while IFS=$'\t' read -r id _slot name; do
    name_key="$(normalize_lookup_key "$name")"
    if [[ "$name_key" == "$key" ]]; then
      echo "$id"
      return
    fi
    if [[ "$name_key" == *"$key"* || "$key" == *"$name_key"* ]]; then
      match_count=$((match_count + 1))
      if [[ -z "$first_match_id" ]]; then
        first_match_id="$id"
        first_match_name="$name"
      fi
      if [[ ${#suggestions[@]} -lt 8 ]]; then
        suggestions+=("${name} (${id})")
      fi
    fi
  done < <(wearable_index_stream)

  if [[ "$match_count" -eq 1 ]]; then
    echo "$first_match_id"
    return
  fi

  if [[ "$match_count" -gt 1 ]]; then
    echo "Ambiguous wearable name: ${raw}" >&2
    printf 'Matches:\n' >&2
    printf '  - %s\n' "${suggestions[@]}" >&2
    exit 1
  fi

  echo "Unknown wearable name: ${raw}" >&2
  exit 1
}

normalize_slot_name() {
  local raw="${1:-}"
  raw="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  raw="${raw//_/}"
  raw="${raw//-/}"
  raw="${raw// /}"
  case "$raw" in
    body|shirt|torso) echo "body" ;;
    face|mouth|mask) echo "face" ;;
    eyes|eyewear|glasses) echo "eyes" ;;
    head|hat|helmet|hair) echo "head" ;;
    pet|companion|backpet) echo "pet" ;;
    handleft|lefthand|left) echo "hand_left" ;;
    handright|righthand|right|weapon) echo "hand_right" ;;
    *)
      echo "Unknown slot: ${1}" >&2
      exit 1
      ;;
  esac
}

apply_slot_assignment() {
  local assignment="${1:?missing assignment}"
  local slot="${assignment%%=*}"
  local value="${assignment#*=}"
  if [[ "$assignment" != *=* ]] || [[ -z "$slot" ]] || [[ -z "$value" ]]; then
    echo "Invalid slot assignment: $assignment" >&2
    exit 1
  fi

  slot="$(normalize_slot_name "$slot")"
  value="$(resolve_wearable_id "$value")"
  case "$slot" in
    body) body="$value" ;;
    face) face="$value" ;;
    eyes) eyes="$value" ;;
    head) head="$value" ;;
    pet) pet="$value" ;;
    hand_left) hand_left="$value" ;;
    hand_right) hand_right="$value" ;;
  esac
}

apply_preset() {
  local name="${1:-}"
  local key
  key="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"
  case "$key" in
    "" ) ;;
    blank-eth|blank_eth|eth-blank)
      slug="blank-eth"
      collateral="ETH"
      eye_shape="Mythical"
      eye_color="High"
      skin_id=0
      background="arcade-purple"
      pose="idle"
      body=0
      face=0
      eyes=0
      head=0
      pet=0
      hand_left=0
      hand_right=0
      ;;
    aagent-eth|aagent_eth|aagent)
      slug="aagent-eth"
      collateral="ETH"
      eye_shape="Mythical"
      eye_color="High"
      skin_id=0
      background="arcade-purple"
      pose="hero"
      body=0
      face=0
      eyes=0
      head=56
      pet=0
      hand_left=0
      hand_right=58
      ;;
    portrait-eth|portrait_eth|portrait)
      slug="portrait-eth"
      collateral="ETH"
      eye_shape="Mythical"
      eye_color="High"
      skin_id=0
      background="studio-cream"
      pose="portrait"
      body=0
      face=0
      eyes=0
      head=0
      pet=0
      hand_left=0
      hand_right=0
      ;;
    *)
      echo "Unknown preset: $name" >&2
      print_presets >&2
      exit 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --preset) preset="$2"; apply_preset "$preset"; shift 2 ;;
    --slug) slug="$2"; shift 2 ;;
    --haunt-id) haunt_id="$2"; shift 2 ;;
    --collateral) collateral="$2"; shift 2 ;;
    --eye-shape) eye_shape="$2"; shift 2 ;;
    --eye-color) eye_color="$2"; shift 2 ;;
    --skin-id) skin_id="$2"; shift 2 ;;
    --background|--bg) background="$2"; shift 2 ;;
    --pose) pose="$2"; shift 2 ;;
    --body|--body-wearable) body="$(resolve_wearable_id "$2")"; shift 2 ;;
    --face|--face-wearable) face="$(resolve_wearable_id "$2")"; shift 2 ;;
    --eyes|--eyes-wearable) eyes="$(resolve_wearable_id "$2")"; shift 2 ;;
    --head|--head-wearable) head="$(resolve_wearable_id "$2")"; shift 2 ;;
    --pet) pet="$(resolve_wearable_id "$2")"; shift 2 ;;
    --hand-left|--left-hand) hand_left="$(resolve_wearable_id "$2")"; shift 2 ;;
    --hand-right|--right-hand) hand_right="$(resolve_wearable_id "$2")"; shift 2 ;;
    --slot) apply_slot_assignment "$2"; shift 2 ;;
    --wearables)
      IFS=',' read -r -a slot_pairs <<< "$2"
      for slot_pair in "${slot_pairs[@]}"; do
        apply_slot_assignment "$slot_pair"
      done
      shift 2
      ;;
    --find-wearable) find_wearable_query="$2"; shift 2 ;;
    --render-mode) render_mode="$2"; shift 2 ;;
    --hosted-only) render_mode="hosted"; shift ;;
    --unity-only) render_mode="unity"; shift ;;
    --print-presets) print_presets; exit 0 ;;
    --write-only) write_only=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -n "$find_wearable_query" ]]; then
  print_wearable_matches "$find_wearable_query"
  exit 0
fi

mkdir -p "${ROOT}/Requests" "${ROOT}/Renders"

normalized_slug="$(printf '%s' "$slug" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9_-]+/-/g; s/^-+//; s/-+$//')"
if [[ -z "$normalized_slug" ]]; then
  normalized_slug="custom-gotchi"
fi

background_key="$(printf '%s' "$background" | tr '[:upper:]' '[:lower:]')"
case "$background_key" in
  arcade-purple) normalized_background="#806AFB" ;;
  studio-cream) normalized_background="#F4EDE1" ;;
  slime-lime) normalized_background="#D8FF5E" ;;
  night-ink) normalized_background="#131722" ;;
  soft-sky) normalized_background="#D9F3FF" ;;
  gotchi-radio) normalized_background="#1DDA8D" ;;
  transparent) normalized_background="transparent" ;;
  *) normalized_background="$background" ;;
esac

pose_key="$(printf '%s' "$pose" | tr '[:upper:]' '[:lower:]')"
case "$pose_key" in
  front|classic|idle) normalized_pose="idle" ;;
  portrait) normalized_pose="portrait" ;;
  hero) normalized_pose="hero" ;;
  left) normalized_pose="left" ;;
  right) normalized_pose="right" ;;
  *) normalized_pose="$pose" ;;
esac

jq -n \
  --arg slug "$normalized_slug" \
  --arg root "$ROOT" \
  --arg collateral "$collateral" \
  --arg eye_shape "$eye_shape" \
  --arg eye_color "$eye_color" \
  --arg background "$normalized_background" \
  --arg pose "$normalized_pose" \
  --argjson haunt_id "$haunt_id" \
  --argjson skin_id "$skin_id" \
  --argjson body "$body" \
  --argjson face "$face" \
  --argjson eyes "$eyes" \
  --argjson head "$head" \
  --argjson pet "$pet" \
  --argjson hand_left "$hand_left" \
  --argjson hand_right "$hand_right" \
  '
  {
    haunt_id: $haunt_id,
    collateral: $collateral,
    eye_shape: $eye_shape,
    eye_color: $eye_color,
    skin_id: $skin_id,
    background: $background,
    pose: $pose,
    wearables: {
      body: $body,
      face: $face,
      eyes: $eyes,
      head: $head,
      pet: $pet,
      hand_left: $hand_left,
      hand_right: $hand_right
    },
    output: {
      slug: $slug,
      full_png: ($root + "/Renders/" + $slug + "-full.png"),
      headshot_png: ($root + "/Renders/" + $slug + "-headshot.png"),
      manifest_json: ($root + "/Renders/" + $slug + "-manifest.json")
    }
  }
  ' > "$REQUEST_PATH"

printf 'Wrote %s\n' "$REQUEST_PATH"

if [[ "$write_only" == "1" ]]; then
  exit 0
fi

case "$render_mode" in
  auto)
    if node "${ROOT}/scripts/render-hosted-custom.mjs" --input-json "$REQUEST_PATH" --quiet-fail; then
      exit 0
    fi
    echo "Hosted renderer unavailable for this request, falling back to local Unity renderer." >&2
    bash "${ROOT}/scripts/run-unity-render.sh" "$REQUEST_PATH"
    ;;
  hosted)
    node "${ROOT}/scripts/render-hosted-custom.mjs" --input-json "$REQUEST_PATH"
    ;;
  unity)
    bash "${ROOT}/scripts/run-unity-render.sh" "$REQUEST_PATH"
    ;;
  *)
    echo "Unknown render mode: $render_mode" >&2
    exit 1
    ;;
esac
