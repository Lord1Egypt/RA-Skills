#!/usr/bin/env bash
# ingest-photo.sh — add a photo to a Postflight photo library.
#
# Strips ALL metadata (GPS included) from a copy of the photo, files it
# in the library directory, and appends the manifest entry that makes it
# postable (see CONTENT.md "Photo library"). The skill never writes the
# manifest — this script and your editor are the only ways in.
#
# usage: ingest-photo.sh [options] <photo> "<one-line note>" <tag> [tag ...]
#        ingest-photo.sh [options] --note-file F <photo> <tag> [tag ...]
#   --dir DIR            library directory (default:
#                        <workspace>/postflight-state/media/photos);
#                        must not contain ".."
#   --location "..."     where it was taken (shown in the approval message)
#   --location-file F    read the location from a file instead (safe for
#                        untrusted text: nothing is shell-expanded)
#   --note-file F        read the note from a file instead of an argument
#   --taken YYYY-MM-DD   taken date, when the photo has no EXIF date
#   --name SLUG          filename slug (default: from the source filename)
#   --ext jpg|jpeg|png   extension, when the source file has none
#
# Works on macOS bash 3.2 and Linux bash 5. Requires exiftool.

set -euo pipefail

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
ok()  { printf '  ok: %s\n' "$*"; }

# The library must live where the agent reads it, which is one path now:
# <workspace>/postflight-state/media/photos, the same for a copy install, a
# --dev symlink, and a ClawHub install. There is deliberately no fallback to
# the folder this script sits in — that used to cover running from a
# checkout, and it would now file photos somewhere the agent never looks.
default_dir() {
  local workspace="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
  [[ -d "$workspace" ]] || die "no OpenClaw workspace at $workspace — set OPENCLAW_WORKSPACE, or pass --dir"
  printf '%s' "$workspace/postflight-state/media/photos"
}

# One-line YAML double-quoted scalar: escape backslashes and quotes,
# flatten newlines, carriage returns, and tabs to spaces.
yaml_escape() {
  printf '%s' "$1" | tr '\n\r\t' '   ' | sed 's/\\/\\\\/g; s/"/\\"/g'
}

slugify() {
  printf '%s' "$1" | tr -d '\n\r' | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]\{1,\}/-/g; s/^-//; s/-$//'
}

dir="" location="" taken="" note_file="" location_file="" name="" ext_opt=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)           dir="${2:?--dir needs a value}"; shift 2 ;;
    --location)      location="${2:?--location needs a value}"; shift 2 ;;
    --location-file) location_file="${2:?--location-file needs a value}"; shift 2 ;;
    --note-file)     note_file="${2:?--note-file needs a value}"; shift 2 ;;
    --taken)         taken="${2:?--taken needs a value}"; shift 2 ;;
    --name)          name="${2:?--name needs a value}"; shift 2 ;;
    --ext)           ext_opt="${2:?--ext needs a value}"; shift 2 ;;
    --*)             die "unknown option: $1" ;;
    *)               break ;;
  esac
done
case "$dir" in *..*) die "--dir must not contain '..'" ;; esac
[[ -z "$name" || "$name" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "--name must be a lowercase slug"
if [[ -n "$note_file" ]]; then
  [[ -f "$note_file" ]] || die "no such note file: $note_file"
  note="$(cat "$note_file")"
  [[ $# -ge 2 ]] || die 'usage: ingest-photo.sh [options] --note-file F <photo> <tag> [tag ...]'
  photo="$1"
  shift 1
else
  [[ $# -ge 3 ]] || die 'usage: ingest-photo.sh [options] <photo> "<note>" <tag> [tag ...]'
  photo="$1" note="$2"
  shift 2
fi
if [[ -n "$location_file" ]]; then
  [[ -z "$location" ]] || die "pass --location or --location-file, not both"
  [[ -f "$location_file" ]] || die "no such location file: $location_file"
  location="$(cat "$location_file")"
fi
case "$photo" in -*) photo="./$photo" ;; esac

command -v exiftool >/dev/null \
  || die "exiftool required (macOS: brew install exiftool · Debian/Ubuntu: apt install libimage-exiftool-perl)"
[[ -f "$photo" ]] || die "no such file: $photo"
[[ -n "${note// /}" ]] || die "the note is the caption seed — it cannot be empty"

if [[ "$(basename "$photo")" == *.* ]]; then
  ext="$(printf '%s' "${photo##*.}" | tr '[:upper:]' '[:lower:]')"
else
  ext="$(printf '%s' "$ext_opt" | tr '[:upper:]' '[:lower:]')"
  [[ -n "$ext" ]] || die "source file has no extension — pass --ext jpg|jpeg|png"
fi
case "$ext" in
  jpg|jpeg|png) ;;
  heic) die "X does not take HEIC — convert it first (macOS: sips -s format jpeg <file> --out out.jpg)" ;;
  *)    die "unsupported extension .$ext (jpg, jpeg, png)" ;;
esac

size="$(wc -c < "$photo" | tr -d ' ')"
max=$((5 * 1024 * 1024))
[[ "$size" -le "$max" ]] \
  || die "$((size / 1024 / 1024)) MB is over X's 5 MB image cap — resize it first (macOS: sips -Z 2048 <file>)"

tags=()
for t in "$@"; do
  t="$(printf '%s' "$t" | tr '[:upper:]' '[:lower:]')"
  [[ "$t" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "tag '$t' — lowercase letters, digits, dashes only"
  tags+=("$t")
done

if [[ -z "$taken" ]]; then
  taken="$(exiftool -s3 -d %Y-%m-%d -DateTimeOriginal "$photo" 2>/dev/null || true)"
  [[ -n "$taken" ]] || die "photo has no EXIF date — pass --taken YYYY-MM-DD"
fi
[[ "$taken" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "taken date must be YYYY-MM-DD, got: $taken"

[[ -n "$dir" ]] || dir="$(default_dir)"
mkdir -p "$dir"

base="$(basename "$photo")"
if [[ -n "$name" ]]; then
  slug="$name"
else
  slug="$(slugify "${base%.*}")"
fi
[[ -n "$slug" ]] || slug="photo"
dest="$taken-$slug.$ext"
if [[ -e "$dir/$dest" ]]; then
  n=2
  while [[ -e "$dir/$taken-$slug-$n.$ext" ]]; do
    n=$((n + 1))
    [[ $n -le 9 ]] || die "too many copies of $taken-$slug — rename the source file"
  done
  dest="$taken-$slug-$n.$ext"
fi

cp "$photo" "$dir/$dest"
if ! strip_out="$(exiftool -all= -overwrite_original "$dir/$dest" 2>&1)"; then
  rm -f "$dir/$dest"
  die "exiftool could not rewrite $base (${strip_out##*$'\n'}) — not adding it"
fi
# The verify must fail closed: an exiftool error here is NOT a clean scan.
if ! gps="$(exiftool -s3 -gps:all -XMP:Location -IPTC:Sub-location -City "$dir/$dest" 2>&1)"; then
  rm -f "$dir/$dest"
  die "could not verify the metadata strip ($gps) — not adding the photo"
fi
if [[ -n "$gps" ]]; then
  rm -f "$dir/$dest"
  die "location metadata survived the strip — not adding the photo"
fi
ok "EXIF stripped, filed as $dest"

tag_list=""
for t in "${tags[@]}"; do
  tag_list="${tag_list:+$tag_list, }\"$t\""
done

manifest="$dir/manifest.yaml"
if [[ ! -f "$manifest" ]]; then
  printf '# postflight photo library — one entry per postable photo.\n' > "$manifest"
  printf '# Maintained by ingest-photo.sh and your editor; the skill only reads it.\n' >> "$manifest"
fi
{
  printf -- '- file: %s\n' "$dest"
  printf '  tags: [%s]\n' "$tag_list"
  [[ -n "$location" ]] && printf '  location: "%s"\n' "$(yaml_escape "$location")"
  printf '  note: "%s"\n' "$(yaml_escape "$note")"
  printf '  taken: %s\n' "$taken"
} >> "$manifest"
ok "manifest entry appended to $manifest"

printf '\nPostable once the pillar'\''s cooldowns allow it (never same-day).\n'
printf 'Reminder: home-adjacent spots stay out of the library entirely.\n'
