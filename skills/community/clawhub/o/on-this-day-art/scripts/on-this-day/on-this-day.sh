#!/bin/bash
#
# On This Day - Historical Event Image Generator
# Fetches events from Wikipedia and generates SDXL images
#

set -e

# Config
API_HOST="${COMFY_HOST:-192.168.4.95}"
API_PORT=8188
OUTPUT_DIR="/mnt/c/StabilityMatrix/Data/Images/Text2Img"
MEMORY_FILE="/home/tony/.openclaw/workspace/memory/on-this-day-runs.jsonl"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1" >&2; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Get today's date in Wikipedia format
get_today() {
    date "+%m/%d"
}

# Fetch events from Wikipedia
fetch_events() {
    local date_param="$1"
    local url="https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/${date_param}"
    
    log_info "Fetching events for ${date_param}..."
    
    curl -s -L "$url" | python3 << 'PYEOF'
import json, sys, random
data = json.load(sys.stdin)
events = data.get('events', [])

# Score and rank events
scored = []
for e in events:
    score = 0
    text = e.get('text', '')
    year = e.get('year', 0)
    
    # Skip if no year
    if not year:
        continue
    
    # Skip births/deaths
    if e.get('type') in ['birth', 'death']:
        continue
    
    # Skip vague events
    vague_words = ['established', 'founded', 'opened', 'born', 'died', 'elected', 'appointed']
    if any(w in text.lower() for w in vague_words) and len(text) < 30:
        continue
    
    # Prefer major categories
    major_keywords = ['war', 'battle', 'disaster', 'attack', 'explosion', 'crash', 'landing', 'moon', 'speech', 'assassination', 'revolution', '发明', 'discovery', 'first']
    if any(k in text.lower() for k in major_keywords):
        score += 10
    
    # Prefer events with specific locations
    if e.get('pages') and len(e['pages']) > 0:
        page = e['pages'][0]
        if page.get('thumbnail'):
            score += 5
        if page.get('extract'):
            score += 3
    
    # Recency bonus (major 20th-21st century events)
    if 1900 <= year <= 2025:
        score += 5
    elif 1800 <= year < 1900:
        score += 2
    
    # Strong visual potential keywords
    visual_keywords = ['ship', 'airplane', 'plane', 'train', 'city', 'building', 'soldiers', 'crowd', 'president', 'king', 'queen', 'rocket', 'space', 'moon', 'explosion', 'fire', 'flood', 'earthquake']
    if any(k in text.lower() for k in visual_keywords):
        score += 8
    
    scored.append({
        'text': text,
        'year': year,
        'score': score,
        'pages': e.get('pages', [])
    })

# Sort by score and return top candidates
scored.sort(key=lambda x: x['score'], reverse=True)
top = scored[:10]

for e in top:
    # Extract coordinates if available
    coords = ""
    if e.get('pages') and len(e['pages']) > 0:
        page = e['pages'][0]
        if page.get('coordinates'):
            coords = f"{page['coordinates']['lat']},{page['coordinates']['lon']}"
    print(f\"{e['year']}|{e['score']}|{e['text']}|{coords}\")
" 2>/dev/null || echo ""
}

# Get event details
get_event_details() {
    local year_text="$1"
    local pages="$2"
    
    echo "$pages" | python3 -c "
import json, sys
pages = json.load(sys.stdin)
if pages:
    p = pages[0]
    print(p.get('extract', '')[:500])
    if p.get('coordinates'):
        print(f\"COORDS: {p['coordinates']['lat']},{p['coordinates']['lon']}\")
" 2>/dev/null || echo ""
}

# Generate SDXL prompt for the scene
generate_prompt() {
    local event_text="$1"
    local year="$2"
    local details="$3"
    
    # Use AI to construct the scene prompt
    echo "$event_text|$year|$details" | python3 -c "
import json, sys
line = sys.stdin.read().strip()
if '|' in line:
    parts = line.split('|')
    event_text = parts[0] if len(parts) > 0 else ''
    year = parts[1] if len(parts) > 1 else ''
else:
    event_text = line
    year = ''

# Simple prompt construction (can be enhanced with LLM)
# Scene: 10 seconds before the event
scene_prompts = {
    'war': 'Military troops positioned before battle, tense atmosphere, foggy dawn, 1910s or {} era style, cinematic composition'.format(year),
    'attack': 'Peaceful city street moments before attack, civilians going about day, tense foreshadowing, historical accuracy, dramatic lighting'.format(year),
    'explosion': 'Industrial facility moments before explosion, workers unaware, steam and machinery, dramatic sky, early 20th century industrial setting'.format(year),
    'disaster': 'Coastal city before tsunami, boats in harbor, normal activity, beautiful sky, peaceful scene about to change'.format(year),
    'landing': 'Lunar surface moments before landing, astronauts preparing descent module, Earth visible in black sky, tense mission control'.format(year),
    'moon': 'Astronaut on moon surface moments before historic step, boot about to touch lunar regolith, Earth rising, tension and wonder'.format(year),
    'speech': 'Crowd gathered before famous speech, podium prepared, leader approaching microphone, dramatic stage lighting'.format(year),
    'ship': 'Ship sailing toward iceberg, crew on deck unaware, foggy Atlantic ocean, early 1912 style, dramatic maritime scene'.format(year),
    'plane': 'Airplane on runway before takeoff, passengers boarding, sunny day, 1960s or {} era airport setting'.format(year),
    'fire': 'Theater before fire, audience arriving, ornate interior, decorated proscenium, moments before disaster'.format(year),
}

# Default fallback
default = f'Historical scene depicting moments before {event_text}, cinematic composition, dramatic lighting, {year} era architecture and attire, photorealistic, detailed environment'

# Find matching keyword
prompt = default
for key, val in scene_prompts.items():
    if key in event_text.lower():
        prompt = val
        break

print(prompt)
PYEOF
}

# Generate image via ComfyUI
generate_image() {
    local prompt="$1"
    local output_prefix="on-this-day"
    
    log_info "Generating image with prompt: ${prompt:0:50}..."
    
    local workflow=$(cat <<WFEOF
{
  "prompt": {
    "1": { "inputs": { "ckpt_name": "sd_xl_base_1.0.safetensors" }, "class_type": "CheckpointLoaderSimple" },
    "2": { "inputs": { "text": "$prompt", "clip": ["1", 1] }, "class_type": "CLIPTextEncode" },
    "3": { "inputs": { "text": "blurry, low quality, distorted, modern, anachronistic, watermark, text, signature", "clip": ["1", 1] }, "class_type": "CLIPTextEncode" },
    "4": { "inputs": { "width": 512, "height": 512, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
    "5": { "inputs": { "seed": 42, "steps": 25, "cfg": 7, "sampler_name": "euler", "scheduler": "normal", "positive": ["2", 0], "negative": ["3", 0], "model": ["1", 0], "latent_image": ["4", 0], "denoise": 1.0 }, "class_type": "KSampler" },
    "6": { "inputs": { "samples": ["5", 0], "vae": ["1", 2] }, "class_type": "VAEDecode" },
    "7": { "inputs": { "filename_prefix": "$output_prefix", "images": ["6", 0] }, "class_type": "SaveImage" }
  }
}
WFEOF
)
    
    local response=$(curl -s -X POST "http://${API_HOST}:${API_PORT}/prompt" \
        -H "Content-Type: application/json" \
        -d "$workflow")
    
    if echo "$response" | grep -q "prompt_id"; then
        local prompt_id=$(echo "$response" | grep -o '"prompt_id":"[^"]*"' | cut -d'"' -f4)
        log_info "Job queued: $prompt_id"
        echo "$prompt_id"
        return 0
    else
        log_error "Failed to queue: $response"
        return 1
    fi
}

# Wait for generation
wait_for_generation() {
    local prompt_id="$1"
    local max_wait=120
    local waited=0
    
    log_info "Waiting for generation..."
    
    while [ $waited -lt $max_wait ]; do
        sleep 5
        waited=$((waited + 5))
        
        # Check if output exists
        local output=$(ls -t "${OUTPUT_DIR}/on-this-day"*.png 2>/dev/null | head -1)
        if [ -n "$output" ]; then
            log_info "Image generated: $output"
            echo "$output"
            return 0
        fi
    done
    
    log_error "Timeout waiting for generation"
    return 1
}

# Log to memory
log_run() {
    local date="$1"
    local event="$2"
    local location="$3"
    local prompt="$4"
    local image_path="$5"
    local status="$6"
    
    mkdir -p "$(dirname "$MEMORY_FILE")"
    echo "{\"date\": \"$date\", \"event\": \"$event\", \"location\": \"$location\", \"prompt\": \"$prompt\", \"image\": \"$image_path\", \"status\": \"$status\", \"timestamp\": \"$(date -Iseconds)\"}" >> "$MEMORY_FILE"
}

# Main run
run_on_this_day() {
    local test_date="${1:-$(get_today)}"
    local test_event="${2:-}"
    
    log_info "=== On This Day Workflow ==="
    log_info "Date: $test_date"
    
    # Check ComfyUI
    if ! curl -s "http://${API_HOST}:${API_PORT}/" > /dev/null 2>&1; then
        log_error "ComfyUI not available"
        echo "FAIL: ComfyUI not running"
        return 1
    fi
    
    # If test event provided, use it
    if [ -n "$test_event" ]; then
        event_text="$test_event"
        year="2024"
        score=100
    else
        # Fetch events
        events=$(fetch_events "$test_date")
        if [ -z "$events" ]; then
            log_error "No events found"
            echo "FAIL: No events found"
            return 1
        fi
        
        # Get top event
        top_event=$(echo "$events" | head -1)
        event_text=$(echo "$top_event" | cut -d'|' -f3)
        year=$(echo "$top_event" | cut -d'|' -f1)
        score=$(echo "$top_event" | cut -d'|' -f2)
        coordinates=$(echo "$top_event" | cut -d'|' -f4)
    fi
    
    log_info "Selected: $event_text ($year)"
    
    # Extract location from event (simple heuristic)
    location=""
    case "$event_text" in
        *"Boston"*) location="Boston, Massachusetts" ;;
        *"New York"*) location="New York City, New York" ;;
        *"Washington"*) location="Washington, D.C." ;;
        *"London"*) location="London, England" ;;
        *"Paris"*) location="Paris, France" ;;
        *"Moon"*) location="Sea of Tranquility, Moon" ;;
        *"Hiroshima"*) location="Hiroshima, Japan" ;;
        *"Nagasaki"*) location="Nagasaki, Japan" ;;
        *"Berlin"*) location="Berlin, Germany" ;;
        *"Moscow"*) location="Moscow, Russia" ;;
        *"Tokyo"*) location="Tokyo, Japan" ;;
        *"Pearl Harbor"*) location="Pearl Harbor, Hawaii" ;;
        *"Dallas"*) location="Dallas, Texas" ;;
        *"Cape Canaveral"*) location="Cape Canaveral, Florida" ;;
        *"Hudson"*) location="Hudson River, New York" ;;
        *"Hungary"*|"Katalin Novák"*) location="Budapest, Hungary" ;;
        *"Gandhi"*|"India"*) location="India" ;;
        *"France"*|"French"*) location="France" ;;
        *"Long Beach"*) location="Long Beach, California" ;;
        *"Cuba"*) location="Cuba" ;;
    esac
    
    # If no location found but we have coordinates, use them
    if [ -z "$location" ] || [ "$location" = "$year" ]; then
        if [ -n "$coordinates" ] && [ "$coordinates" != "" ]; then
            location="$coordinates"
        else
            location="$year"
        fi
    fi
    
    # Generate prompt
    prompt=$(generate_prompt "$event_text" "$year" "")
    
    # Generate image
    prompt_id=$(generate_image "$prompt")
    if [ $? -ne 0 ]; then
        echo "FAIL: Image generation failed"
        return 1
    fi
    
    # Wait for result
    image_path=$(wait_for_generation "$prompt_id")
    if [ $? -ne 0 ] || [ -z "$image_path" ]; then
        echo "FAIL: Generation timeout"
        return 1
    fi
    
    # Log the run
    log_run "$test_date" "$event_text" "$location" "$prompt" "$image_path" "success"
    
    # Output for Discord
    echo "=== GENERATED ==="
    echo "DATE: $test_date"
    echo "LOCATION: $location"
    echo "IMAGE: $image_path"
    echo "================="
    
    return 0
}

# Run
case "${1:-run}" in
    run)
        run_on_this_day "$2" "$3"
        ;;
    test)
        # Quick test without full flow
        log_info "Testing event fetch..."
        fetch_events "$(get_today)"
        ;;
    check)
        if curl -s "http://${API_HOST}:${API_PORT}/" > /dev/null 2>&1; then
            log_info "ComfyUI is ready"
            exit 0
        else
            log_error "ComfyUI not available"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {run|test|check} [date] [event]"
        ;;
esac
