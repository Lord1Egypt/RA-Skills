#!/bin/sh
# OpenXSys installer for macOS, Linux and Git Bash.
#
#   sh skills/open-x-sys/deps/install.sh [options]
#
# It installs the OpenXSys skill and the dependencies pinned in openxsys.lock.json.
# One install, one consent: it shows what it will do, asks once, then does it.
# Nothing is installed that fails verification. Nothing updates itself later.
#
# The lock file is read line by line (no JSON tool is required). The installer relies on
# these conventions in openxsys.lock.json: top-level keys are indented by two spaces,
# entry fields by six, each skill and each library file sits on one line, and each entry
# ends with its "review" line.

set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_SRC=$(dirname "$HERE")
LOCK="$HERE/openxsys.lock.json"
CLI_VERSION="1.8.1"

HOST=""; DIR=""; LANG_ED="en"; PROJECT=0; YES=0; CHECK=0; UNINSTALL=0
DEPS_ONLY=0; INCLUDE_PENDING=0; NO_LIBS=0; WITHOUT=" "

usage() {
  sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
  cat <<'EOF'

Options:
  --host <name>       claude-code | codex | agents   (default: detected)
  --dir <path>        install into this skills directory
  --lang zh-CN        install the complete Chinese edition as open-x-sys
  --project           install into the current project instead of the home directory
  --without <id>      leave out one dependency (id from the lock file); repeatable
  --no-libraries      skip offline copies of page libraries
  --deps-only         install dependencies for an already installed OpenXSys
  --include-pending   also install entries that are not yet approved (reviewers, testers)
  --yes               do not prompt
  --check             change nothing; report what is installed and what is missing
  --uninstall         remove OpenXSys; list the dependencies it installed
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --host) HOST="$2"; shift 2 ;;
    --dir) DIR="$2"; shift 2 ;;
    --lang) LANG_ED="$2"; shift 2 ;;
    --project) PROJECT=1; shift ;;
    --without) WITHOUT="$WITHOUT$2 "; shift 2 ;;
    --no-libraries) NO_LIBS=1; shift ;;
    --deps-only) DEPS_ONLY=1; shift ;;
    --include-pending) INCLUDE_PENDING=1; shift ;;
    --yes|-y) YES=1; shift ;;
    --check) CHECK=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

say()  { printf '%s\n' "$*"; }
warn() { printf '%s\n' "$*" >&2; }
have() { command -v "$1" >/dev/null 2>&1; }

ask() {
  # ask "question" -> 0 for yes. Without a terminal and without --yes the answer is no.
  if [ "$YES" -eq 1 ]; then return 0; fi
  if [ ! -r /dev/tty ]; then warn "No terminal to ask on; treating as 'no'. Pass --yes to proceed without prompts."; return 1; fi
  printf '%s [y/N] ' "$1" > /dev/tty
  read -r reply < /dev/tty || reply=""
  case "$reply" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

# ---------- where things are ----------

REPO=""
if [ -f "$SKILL_SRC/../../README.md" ] && [ -d "$SKILL_SRC/../../skills" ]; then
  REPO=$(CDPATH= cd -- "$SKILL_SRC/../.." && pwd)
fi

if [ -z "$DIR" ]; then
  if [ -z "$HOST" ]; then
    if [ -d "$HOME/.claude" ]; then HOST="claude-code"
    elif [ -d "$HOME/.codex" ]; then HOST="codex"
    else HOST="agents"; fi
  fi
  if [ "$PROJECT" -eq 1 ]; then BASE="$(pwd)"; else BASE="$HOME"; fi
  case "$HOST" in
    claude-code) DIR="$BASE/.claude/skills" ;;
    codex)       DIR="$BASE/.codex/skills" ;;
    agents)      DIR="$BASE/.agents/skills" ;;
    *) warn "Unknown host '$HOST'. Use claude-code, codex or agents, or pass --dir."; exit 2 ;;
  esac
else
  HOST="${HOST:-custom}"
fi
TARGET="$DIR/open-x-sys"
RECORD="$TARGET/deps/installed.json"

# ---------- runtimes ----------

GIT_OK=0; have git && GIT_OK=1
NODE_V=""; NODE_OK=0
if have node; then
  NODE_V=$(node --version 2>/dev/null | sed 's/^v//')
  major=${NODE_V%%.*}; rest=${NODE_V#*.}; minor=${rest%%.*}
  if [ "$major" -gt 22 ] 2>/dev/null || { [ "$major" -eq 22 ] 2>/dev/null && [ "$minor" -ge 20 ] 2>/dev/null; }; then NODE_OK=1; fi
fi
PY=""; PY_V=""
for c in python3 python; do
  if have "$c" && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$c"; PY_V=$("$c" -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])'); break
  fi
done
FETCH=""; have curl && FETCH="curl"; [ -z "$FETCH" ] && have wget && FETCH="wget"

sha256_of() {
  if have sha256sum; then sha256sum "$1" | awk '{print $1}'
  elif have shasum; then shasum -a 256 "$1" | awk '{print $1}'
  elif have openssl; then openssl dgst -sha256 "$1" | awk '{print $NF}'
  else echo ""; fi
}

# ---------- read the lock file ----------

[ -f "$LOCK" ] || { warn "Lock file not found: $LOCK"; exit 1; }

RECORDS=$(awk '
function val(line, key,    re, s) {
  re = "\"" key "\"[ ]*:[ ]*\""
  if (match(line, re)) { s = substr(line, RSTART + RLENGTH); sub(/".*/, "", s); return s }
  return ""
}
/^  "skills": \[/    { section = "skills"; next }
/^  "libraries": \[/ { section = "libraries"; next }
/^  \]/              { section = ""; next }
section == "skills" {
  if ($0 ~ /^      "id":/)         { id = val($0, "id"); n = 0; req = "" }
  if ($0 ~ /^      "url":/)        url = val($0, "url")
  if ($0 ~ /^      "commit":/)     commit = val($0, "commit")
  if ($0 ~ /^      "capability":/) cap = val($0, "capability")
  if ($0 ~ /^      "requires":/)   { req = $0; sub(/.*\[/, "", req); sub(/\].*/, "", req); gsub(/[" ]/, "", req) }
  if ($0 ~ /"name":/ && $0 ~ /"tree":/) { n++; nm[n] = val($0, "name"); pa[n] = val($0, "path"); tr[n] = val($0, "tree") }
  if ($0 ~ /^      "review":/) {
    st = val($0, "status")
    for (i = 1; i <= n; i++) print "skill\t" id "\t" url "\t" commit "\t" nm[i] "\t" pa[i] "\t" tr[i] "\t" st "\t" cap "\t" req
  }
}
section == "libraries" {
  if ($0 ~ /^      "id":/) { id = val($0, "id"); pkg = val($0, "package"); ver = val($0, "version"); n = 0 }
  if ($0 ~ /"path":/ && $0 ~ /"sha256":/) { n++; pa[n] = val($0, "path"); sh[n] = val($0, "sha256") }
  if ($0 ~ /^      "review":/) {
    st = val($0, "status")
    for (i = 1; i <= n; i++) print "lib\t" id "\t" pkg "\t" ver "\t" pa[i] "\t" sh[i] "\t" st
  }
}' "$LOCK")

[ -n "$RECORDS" ] || { warn "Could not read any dependency from $LOCK."; exit 1; }
TAB=$(printf '\t')

wanted() {
  # wanted <id> <status> -> 0 if this entry should be installed
  case "$WITHOUT" in *" $1 "*) return 1 ;; esac
  [ "$2" = "approved" ] && return 0
  [ "$INCLUDE_PENDING" -eq 1 ] && return 0
  return 1
}

# ---------- show ----------

show_plan() {
  say "OpenXSys installer"
  say ""
  say "  Skills directory : $DIR  (host: $HOST)"
  if [ "$DEPS_ONLY" -eq 0 ]; then
    if [ -n "$REPO" ]; then say "  OpenXSys edition : $LANG_ED, with the Playground"; else say "  OpenXSys edition : (not in a repository checkout; dependencies only)"; fi
  fi
  say ""
  say "  Runtimes"
  if [ "$GIT_OK" -eq 1 ]; then say "    git      present"; else say "    git      MISSING  (needed to fetch pinned skills)"; fi
  if [ "$NODE_OK" -eq 1 ]; then say "    Node.js  $NODE_V"
  elif [ -n "$NODE_V" ]; then say "    Node.js  $NODE_V  (22.20 or later adds: video with Remotion, the skills CLI)"
  else say "    Node.js  missing  (adds: video with Remotion, the skills CLI)"; fi
  if [ -n "$PY" ]; then say "    Python   $PY_V"; else say "    Python   missing  (adds: Manim animation; scripts in the document skills)"; fi
  say ""
  say "  Skills (each fetched at its pinned commit and verified by git tree id)"
  printf '%s\n' "$RECORDS" | while IFS="$TAB" read -r kind id url commit name path tree status cap req; do
    [ "$kind" = "skill" ] || continue
    if wanted "$id" "$status"; then mark="install"; else mark="skip   "; fi
    printf '    %s  %-26s %-9s %s\n' "$mark" "$name" "$status" "$url@$(printf '%s' "$commit" | cut -c1-12)"
  done
  say ""
  say "  Page libraries (offline copies, each file verified by SHA-256)"
  printf '%s\n' "$RECORDS" | while IFS="$TAB" read -r kind id pkg ver path sha status; do
    [ "$kind" = "lib" ] || continue
    if [ "$NO_LIBS" -eq 0 ] && wanted "$id" "$status"; then mark="install"; else mark="skip   "; fi
    printf '    %s  %-26s %-9s %s\n' "$mark" "$pkg@$ver" "$status" "$path"
  done
  say ""
  say "  Licenses and conditions (full text: deps/DEPENDENCIES.md)"
  say "    - Remotion is free for individuals and small teams; companies above a team-size"
  say "      threshold need a paid company license: https://remotion.dev/license"
  say "    - Anthropic's document skills (pptx, docx, pdf, xlsx) carry their own license terms."
  say "    - GSAP is free to use under its own standard license (not an OSI license)."
  say "    - D3 (ISC); Scrollama, KaTeX, Mermaid, Three.js (MIT); MapLibre GL JS (BSD-3-Clause)."
  say "    - The skills CLI is run at version $CLI_VERSION with its telemetry turned off."
  say ""
  if [ "$INCLUDE_PENDING" -eq 1 ]; then
    say "  --include-pending is set: entries marked 'pending' have NOT been reviewed."
    say "  Their pins and checksums are real, but nobody has yet read the pinned content in full."
    say ""
  else
    say "  Entries marked 'pending' are candidates awaiting review and are skipped."
    say ""
  fi
}

# ---------- check ----------

if [ "$CHECK" -eq 1 ]; then
  show_plan
  if [ -f "$TARGET/SKILL.md" ]; then say "  OpenXSys is installed at $TARGET"; else say "  OpenXSys is not installed at $TARGET"; fi
  if [ -f "$RECORD" ]; then say "  Install record: $RECORD"; fi
  printf '%s\n' "$RECORDS" | while IFS="$TAB" read -r kind id url commit name rest; do
    [ "$kind" = "skill" ] || continue
    if [ -f "$DIR/$name/SKILL.md" ]; then say "    present  $name"; else say "    absent   $name"; fi
  done
  exit 0
fi

# ---------- uninstall ----------

if [ "$UNINSTALL" -eq 1 ]; then
  if [ ! -e "$TARGET" ]; then say "OpenXSys is not installed at $TARGET."; exit 0; fi
  say "This removes $TARGET."
  say "Your systems (~/.openxsys/ and any <project>/.openxsys/) are yours and are not touched."
  if [ -f "$RECORD" ]; then
    say "Dependencies this installer added (remove each yourself if you no longer want it):"
    grep '"name"' "$RECORD" | sed 's/.*"name": *"\([^"]*\)".*/    \1/' | while read -r n; do
      say "    $n   ->   rm -rf \"$DIR/$n\"   (or: npx skills remove $n -g)"
    done
  fi
  if ask "Remove OpenXSys now?"; then
    if [ -L "$TARGET" ]; then rm -f "$TARGET"; else rm -rf "$TARGET"; fi
    say "Removed. If you added the OpenXSys line to your host instructions, remove that line too."
  else
    say "Nothing was removed."
  fi
  exit 0
fi

# ---------- consent ----------

show_plan
if ! ask "Install as shown?"; then say "Nothing was installed."; exit 0; fi

INSTALLED_SKILLS=""; INSTALLED_LIBS=""; SKIPPED=""
note_skip() { SKIPPED="$SKIPPED
    $1"; }

# ---------- 1. OpenXSys itself ----------

if [ "$DEPS_ONLY" -eq 0 ] && [ -n "$REPO" ]; then
  case "$LANG_ED" in
    en) SRC="$REPO/skills/open-x-sys" ;;
    zh-CN|zh) SRC="$REPO/skills/open-x-sys.zh-CN" ;;
    *) warn "Unknown edition '$LANG_ED' (use en or zh-CN)."; exit 2 ;;
  esac
  [ -f "$SRC/SKILL.md" ] || { warn "Edition not found: $SRC"; exit 1; }
  mkdir -p "$DIR"
  if [ -L "$TARGET" ]; then
    say "  $TARGET is a link (a development setup). Left as it is."
  else
    if [ -e "$TARGET" ]; then
      if ask "  $TARGET already exists. Replace it with this version?"; then
        if [ -d "$TARGET/display/lib" ]; then mv "$TARGET/display/lib" "$DIR/.openxsys-lib-keep"; fi
        rm -rf "$TARGET"
      else
        say "  Kept the existing install."; SRC=""
      fi
    fi
    if [ -n "$SRC" ]; then
      cp -R "$SRC" "$TARGET"
      # the installers, lock file and scripts are the same in every edition
      mkdir -p "$TARGET/deps"
      cp "$HERE/openxsys.lock.json" "$HERE/install.sh" "$HERE/install.ps1" "$TARGET/deps/" 2>/dev/null || true
      if [ -d "$DIR/.openxsys-lib-keep" ]; then mkdir -p "$TARGET/display"; mv "$DIR/.openxsys-lib-keep" "$TARGET/display/lib"; fi
      if [ -d "$REPO/playground" ]; then rm -rf "$TARGET/playground"; cp -R "$REPO/playground" "$TARGET/playground"; fi
      say "  Installed OpenXSys ($LANG_ED) at $TARGET"
    fi
  fi
elif [ "$DEPS_ONLY" -eq 0 ]; then
  say "  Not in a repository checkout: skipping the OpenXSys skill itself."
fi

# ---------- 2. pinned skills ----------

CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/openxsys/pins"
export DISABLE_TELEMETRY=1 DO_NOT_TRACK=1

install_skill() {
  # install_skill id url commit name path tree
  _id="$1"; _url="$2"; _commit="$3"; _name="$4"; _path="$5"; _tree="$6"
  if [ -e "$DIR/$_name" ]; then
    say "  $_name is already present in $DIR. Left as it is (it is yours)."
    return 0
  fi
  if [ "$GIT_OK" -ne 1 ]; then note_skip "$_name: git is not installed"; return 0; fi
  _c="$CACHE/$_commit"
  if [ ! -d "$_c/.git" ]; then
    mkdir -p "$_c"; git init -q "$_c"
    if ! git -C "$_c" fetch -q --depth 1 "$_url" "$_commit" 2>/dev/null; then
      rm -rf "$_c"; note_skip "$_name: could not fetch $_url at $_commit"; return 0
    fi
  fi
  _got=$(git -C "$_c" rev-parse FETCH_HEAD 2>/dev/null || echo "")
  if [ "$_got" != "$_commit" ]; then note_skip "$_name: fetched commit $_got is not the pinned $_commit"; return 0; fi
  _gt=$(git -C "$_c" rev-parse "$_commit:$_path" 2>/dev/null || echo "")
  if [ "$_gt" != "$_tree" ]; then note_skip "$_name: tree id $_gt does not match the lock file ($_tree). NOT installed"; return 0; fi
  git -C "$_c" checkout -q "$_commit" -- "$_path"
  _done=0
  if [ "$NODE_OK" -eq 1 ] && { [ "$HOST" = "claude-code" ] || [ "$HOST" = "codex" ]; } && [ "$PROJECT" -eq 0 ] && have npx; then
    if npx --yes "skills@$CLI_VERSION" add "$_c" --skill "$_name" -g -a "$HOST" -y --copy >/dev/null 2>&1 && [ -f "$DIR/$_name/SKILL.md" ]; then
      _done=1; _how="skills CLI $CLI_VERSION"
    fi
  fi
  if [ "$_done" -eq 0 ]; then
    mkdir -p "$DIR"; cp -R "$_c/$_path" "$DIR/$_name"; _how="copied"
  fi
  say "  Installed $_name  ($_how; verified tree $(printf '%s' "$_tree" | cut -c1-12))"
  INSTALLED_SKILLS="$INSTALLED_SKILLS
    { \"name\": \"$_name\", \"id\": \"$_id\", \"commit\": \"$_commit\", \"tree\": \"$_tree\", \"how\": \"$_how\" },"
}

SKILL_LINES=$(printf '%s\n' "$RECORDS" | grep "^skill$TAB" || true)
OLD_IFS=$IFS
IFS='
'
for line in $SKILL_LINES; do
  IFS="$TAB"; set -- $line; IFS='
'
  # $1 kind  $2 id  $3 url  $4 commit  $5 name  $6 path  $7 tree  $8 status
  if wanted "$2" "$8"; then install_skill "$2" "$3" "$4" "$5" "$6" "$7"; fi
done
IFS=$OLD_IFS

# ---------- 3. offline copies of page libraries ----------

install_lib() {
  # install_lib id package version path sha256
  _dest="$TARGET/display/lib/$2@$3/$4"
  if [ -f "$_dest" ] && [ "$(sha256_of "$_dest")" = "$5" ]; then return 0; fi
  if [ -z "$FETCH" ]; then note_skip "$2@$3/$4: neither curl nor wget is installed"; return 0; fi
  mkdir -p "$(dirname "$_dest")"
  _url="https://cdn.jsdelivr.net/npm/$2@$3/$4"
  if [ "$FETCH" = "curl" ]; then curl -fsSL "$_url" -o "$_dest.part" || { rm -f "$_dest.part"; note_skip "$2@$3/$4: download failed"; return 0; }
  else wget -q "$_url" -O "$_dest.part" || { rm -f "$_dest.part"; note_skip "$2@$3/$4: download failed"; return 0; }; fi
  _sum=$(sha256_of "$_dest.part")
  if [ -z "$_sum" ]; then rm -f "$_dest.part"; note_skip "$2@$3/$4: no SHA-256 tool (sha256sum, shasum or openssl) to verify it"; return 0; fi
  if [ "$_sum" != "$5" ]; then rm -f "$_dest.part"; note_skip "$2@$3/$4: SHA-256 $_sum does not match the lock file. NOT installed"; return 0; fi
  mv "$_dest.part" "$_dest"
  say "  Library $2@$3/$4  (verified)"
  INSTALLED_LIBS="$INSTALLED_LIBS
    { \"package\": \"$2\", \"version\": \"$3\", \"path\": \"$4\", \"sha256\": \"$5\" },"
}

if [ "$NO_LIBS" -eq 0 ] && [ -d "$TARGET" ]; then
  LIB_LINES=$(printf '%s\n' "$RECORDS" | grep "^lib$TAB" || true)
  IFS='
'
  for line in $LIB_LINES; do
    IFS="$TAB"; set -- $line; IFS='
'
    # $1 kind  $2 id  $3 package  $4 version  $5 path  $6 sha256  $7 status
    if wanted "$2" "$7"; then install_lib "$2" "$3" "$4" "$5" "$6"; fi
  done
  IFS=$OLD_IFS
fi

# ---------- 4. the install record ----------

if [ -d "$TARGET/deps" ] && [ ! -L "$TARGET" ]; then
  {
    printf '{\n'
    printf '  "openxsys": "0.0.1-alpha.1",\n'
    printf '  "installed": "%s",\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf '  "host": "%s",\n' "$HOST"
    printf '  "skillsDirectory": "%s",\n' "$DIR"
    printf '  "edition": "%s",\n' "$LANG_ED"
    printf '  "runtimes": { "git": %s, "node": "%s", "python": "%s" },\n' "$([ "$GIT_OK" -eq 1 ] && echo true || echo false)" "$NODE_V" "$PY_V"
    printf '  "skills": [%s\n  ],\n' "$(printf '%s' "$INSTALLED_SKILLS" | sed '$ s/,$//')"
    printf '  "libraries": [%s\n  ]\n' "$(printf '%s' "$INSTALLED_LIBS" | sed '$ s/,$//')"
    printf '}\n'
  } > "$RECORD"
fi

# ---------- 5. summary, and what is missing ----------

say ""
say "Done."
[ -f "$RECORD" ] && say "  Install record: $RECORD"
if [ -n "$SKIPPED" ]; then say "  Not installed:$SKIPPED"; fi
if [ "$NODE_OK" -ne 1 ]; then
  say "  Without Node.js 22.20 or later you still get full interactive pages and static cards."
  say "  Node.js would add short video clips. Install it from https://nodejs.org/"
  if have brew && ask "  Install Node.js now with 'brew install node'?"; then brew install node || warn "  brew install node failed."; fi
fi
if [ -z "$PY" ]; then
  say "  Python 3.10 or later would add Manim concept animation and the document skills' scripts: https://www.python.org/downloads/"
fi
say ""
say "Next: open your agent and say   Open a system for ___.   or   Open the playground."
