#!/bin/sh
# persona-import.sh — Import a .persona bundle into a workspace.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Defaults
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_PATH="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
FORCE=false
BUNDLE_FILE=""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

usage() {
    cat << 'EOF'
Usage: persona-import.sh BUNDLE_FILE [OPTIONS]

Import a .persona bundle into a workspace.

Options:
  --workspace PATH    Target workspace directory (supports any workspace-* path)
  --config PATH       Config file path
  --force             Overwrite existing files without prompting
  -h, --help          Show this help

Cross-workspace example:
  persona-import.sh pepper.persona --workspace ~/.openclaw/workspace-new
EOF
}

confirm_overwrite() {
    file="$1"
    if [ "$FORCE" = "true" ]; then
        return 0
    fi
    if [ -f "$file" ]; then
        printf "${YELLOW}  File exists: %s. Overwrite? (y/n)${NC} > " "$file"
        read -r answer
        case "$answer" in
            [yY]*) return 0 ;;
            *) return 1 ;;
        esac
    fi
    return 0
}

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --workspace) shift; WORKSPACE="$1" ;;
        --config) shift; CONFIG_PATH="$1" ;;
        --force) FORCE=true ;;
        -h|--help) usage; exit 0 ;;
        -*)
            printf "${RED}Unknown option: $1${NC}\n"
            usage; exit 1 ;;
        *)
            if [ -z "$BUNDLE_FILE" ]; then
                BUNDLE_FILE="$1"
            else
                printf "${RED}Unexpected argument: $1${NC}\n"
                usage; exit 1
            fi
            ;;
    esac
    shift
done

if [ -z "$BUNDLE_FILE" ]; then
    printf "${RED}Error: No bundle file specified.${NC}\n"
    usage
    exit 1
fi

if [ ! -f "$BUNDLE_FILE" ]; then
    printf "${RED}Error: File not found: $BUNDLE_FILE${NC}\n"
    exit 1
fi

printf "${BOLD}${CYAN}📦 Importing persona from ${BUNDLE_FILE}...${NC}\n\n"

# Read manifest
python3 -c "
import json, zipfile, sys
with zipfile.ZipFile('$BUNDLE_FILE', 'r') as zf:
    manifest = json.loads(zf.read('manifest.json'))
    p = manifest.get('persona', {})
    print(f\"  Persona: {p.get('name', '?')} {p.get('emoji', '')}\")
    print(f\"  Archetype: {p.get('archetype', '?')}\")
    print(f\"  Exported: {manifest.get('exportDate', '?')}\")
    prov = manifest.get('providers', {})
    print(f\"  Voice: {prov.get('voice', 'none')}\")
    print(f\"  Image: {prov.get('image', 'none')}\")
    if manifest.get('includesMemory'):
        print('  Includes: memory data')
"

printf "\n"

if [ "$FORCE" != "true" ]; then
    printf "${CYAN}  Import to workspace: $WORKSPACE${NC}\n"
    printf "  Proceed? (y/n) > "
    read -r answer
    case "$answer" in
        [yY]*) ;;
        *) printf "Cancelled.\n"; exit 0 ;;
    esac
    printf "\n"
fi

python3 -c "
import json
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import merge_config

bundle_path = '$BUNDLE_FILE'
workspace = Path('$WORKSPACE')
config_path = '$CONFIG_PATH'
force = $( [ "$FORCE" = "true" ] && echo "True" || echo "False" )

workspace.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(bundle_path, 'r') as zf:
    names = zf.namelist()

    # Extract workspace files
    for name in names:
        if name.startswith('workspace/'):
            rel = name[len('workspace/'):]
            if not rel:
                continue
            target = workspace / rel
            if target.exists() and not force:
                print(f'  Skipped (exists): {rel}')
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))
            print(f'  Imported: {rel}')

    # Extract memory files
    for name in names:
        if name.startswith('memory/'):
            rel = name[len('memory/'):]
            if not rel:
                continue
            target = workspace / 'memory' / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not force:
                print(f'  Skipped (exists): memory/{rel}')
                continue
            target.write_bytes(zf.read(name))
            print(f'  Imported: memory/{rel}')

    # Extract reference image
    if 'assets/reference.png' in names:
        target = workspace / 'persona-reference.png'
        if not target.exists() or force:
            target.write_bytes(zf.read('assets/reference.png'))
            print('  Imported: persona-reference.png')

    # Merge persona config
    if 'config/persona.json' in names:
        persona_config = json.loads(zf.read('config/persona.json'))
        merge_config({'persona': persona_config}, config_path)
        print('  Merged: persona config into openclaw.json')

    # Merge TTS config
    if 'config/tts.json' in names:
        tts_config = json.loads(zf.read('config/tts.json'))
        merge_config({'messages': {'tts': tts_config}}, config_path)
        print('  Merged: TTS config into openclaw.json')

print()
"

printf "${GREEN}✅ Import complete!${NC}\n\n"
printf "${BOLD}Next steps:${NC}\n"
printf "  • Review imported files in ${WORKSPACE}\n"
printf "  • Add any required API keys to openclaw.json\n"
printf "  • Run ${CYAN}openclaw gateway restart${NC} to apply changes\n"
