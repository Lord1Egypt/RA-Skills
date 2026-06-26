#!/bin/sh
# persona-export.sh — Export persona to a portable .persona zip bundle.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Defaults
CONFIG_PATH="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
BUNDLE_NAME=""
INCLUDE_MEMORY=false
INCLUDE_VOICE=false

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

usage() {
    cat << 'EOF'
Usage: persona-export.sh [OPTIONS]

Export the current persona to a portable .persona bundle.

Options:
  --name NAME              Bundle filename (default: derived from persona name)
  --include-memory         Include MEMORY.md and memory/ directory
  --include-voice-config   Include voice settings (NOT API keys)
  --config PATH            Config file path
  --workspace PATH         Workspace directory (supports workspace-* pattern)
  --output-dir DIR         Directory for the output bundle (default: current dir)
  -h, --help               Show this help
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        --name) shift; BUNDLE_NAME="$1" ;;
        --include-memory) INCLUDE_MEMORY=true ;;
        --include-voice-config) INCLUDE_VOICE=true ;;
        --config) shift; CONFIG_PATH="$1" ;;
        --workspace) shift; WORKSPACE="$1" ;;
        -h|--help) usage; exit 0 ;;
        *) printf "${RED}Unknown option: $1${NC}\n"; usage; exit 1 ;;
    esac
    shift
done

# Determine bundle name from persona config if not specified
if [ -z "$BUNDLE_NAME" ]; then
    BUNDLE_NAME=$(python3 -c "
import json
try:
    with open('$CONFIG_PATH', 'r') as f:
        config = json.load(f)
    name = config.get('persona', {}).get('name', 'persona')
    print(name.lower().replace(' ', '-'))
except Exception:
    print('persona')
")
fi

OUTPUT_FILE="${BUNDLE_NAME}.persona"

printf "${BOLD}${CYAN}📦 Exporting persona to ${OUTPUT_FILE}...${NC}\n\n"

python3 -c "
import json
import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import read_config, extract_persona_config_no_secrets

workspace = Path('$WORKSPACE')
config_path = '$CONFIG_PATH'
output_file = '$OUTPUT_FILE'
include_memory = $( [ "$INCLUDE_MEMORY" = "true" ] && echo "True" || echo "False" )
include_voice = $( [ "$INCLUDE_VOICE" = "true" ] && echo "True" || echo "False" )

config = read_config(config_path)
persona = config.get('persona', {})

# Build manifest
manifest = {
    'version': '1.0',
    'engine': 'ai-persona-engine',
    'exportDate': datetime.now().isoformat(),
    'persona': {
        'name': persona.get('name', 'Unknown'),
        'emoji': persona.get('emoji', ''),
        'archetype': persona.get('personality', {}).get('archetype', 'custom'),
    },
    'providers': {
        'voice': persona.get('voice', {}).get('provider', 'none'),
        'image': persona.get('image', {}).get('provider', 'none'),
    },
    'includesMemory': include_memory,
}

with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Manifest
    zf.writestr('manifest.json', json.dumps(manifest, indent=2))

    # Workspace files
    workspace_files = ['SOUL.md', 'USER.md', 'IDENTITY.md', 'AGENTS.md', 'HEARTBEAT.md']
    if include_memory:
        workspace_files.append('MEMORY.md')

    for fname in workspace_files:
        fpath = workspace / fname
        if fpath.exists():
            zf.write(str(fpath), f'workspace/{fname}')
            print(f'  Added: workspace/{fname}')

    # Persona config (no secrets)
    persona_clean = extract_persona_config_no_secrets(config_path)
    zf.writestr('config/persona.json', json.dumps(persona_clean, indent=2))
    print('  Added: config/persona.json')

    # TTS config (no API keys)
    if include_voice:
        tts = config.get('messages', {}).get('tts', {})
        # Strip secrets
        tts_clean = json.loads(json.dumps(tts))
        for key in list(tts_clean.keys()):
            if isinstance(tts_clean[key], dict):
                for k in list(tts_clean[key].keys()):
                    if 'key' in k.lower() or 'secret' in k.lower() or 'token' in k.lower():
                        del tts_clean[key][k]
        zf.writestr('config/tts.json', json.dumps(tts_clean, indent=2))
        print('  Added: config/tts.json')

    # Reference image
    ref_image = persona.get('image', {}).get('referenceImage', '')
    if ref_image:
        ref_path = Path(os.path.expanduser(ref_image))
        if ref_path.exists():
            zf.write(str(ref_path), 'assets/reference.png')
            print('  Added: assets/reference.png')

    # Memory directory
    if include_memory:
        memory_dir = workspace / 'memory'
        if memory_dir.exists():
            for md_file in sorted(memory_dir.glob('*.md')):
                arcname = f'memory/{md_file.name}'
                zf.write(str(md_file), arcname)
                print(f'  Added: {arcname}')

print()
print(f'Bundle saved: {output_file}')
"

if [ "$INCLUDE_MEMORY" = "true" ]; then
    printf "\n${YELLOW}⚠️  Memory included. This bundle may contain personal information.${NC}\n"
fi

printf "\n${GREEN}✅ Export complete: ${OUTPUT_FILE}${NC}\n"
