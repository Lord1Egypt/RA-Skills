#!/bin/bash
# ComfyUI Bridge - Ozzy to Windows ComfyUI
# ==========================================
# DEFAULT: SDXL (verified working)
# ALTERNATE: JuggernautXL (available for explicit use)
# EXPERIMENTAL: SD 3.5 (unstable on laptop)

COMFY_PORT=8188
COMFY_HOST="192.168.4.95"
COMFY_DIR="/mnt/c/StabilityMatrix/Data/Packages/ComfyUI"
OUTPUT_DIR="/mnt/c/StabilityMatrix/Data/Packages/ComfyUI/output"
SHARED_INPUT="/home/tony/.openclaw/workspace/comfy-inputs"
SHARED_OUTPUT="/home/tony/.openclaw/workspace/comfy-outputs"

# DEFAULT MODEL - SDXL
DEFAULT_MODEL="sd_xl_base_1.0.safetensors"
DEFAULT_RESOLUTION="512x512"
DEFAULT_STEPS=20

# ALTERNATE MODEL - JuggernautXL
JUGGERNAUT_MODEL="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

mkdir -p "$SHARED_INPUT" "$SHARED_OUTPUT"

check_comfy() {
    curl -s "http://${COMFY_HOST}:${COMFY_PORT}" > /dev/null 2>&1
}

wait_for_comfy() {
    log_info "Waiting for ComfyUI..."
    for i in {1..30}; do
        if check_comfy; then
            log_info "ComfyUI is ready!"
            return 0
        fi
        sleep 2
    done
    log_error "ComfyUI not available"
    return 1
}

launch_comfy() {
    if check_comfy; then
        log_info "ComfyUI already running at http://${COMFY_HOST}:${COMFY_PORT}"
        return 0
    fi
    local python_exe="$COMFY_DIR/venv/Scripts/python.exe"
    local main_py="$COMFY_DIR/main.py"
    log_info "Starting ComfyUI..."
    /mnt/c/Windows/System32/cmd.exe /c "start \"ComfyUI\" \"$python_exe\" \"$main_py\" --listen 0.0.0.0 --port $COMFY_PORT" &
    wait_for_comfy
}

# Generate image with specified model
generate_image() {
    local model="$1"
    local prompt="${2:-A beautiful sunset over mountains}"
    local output_prefix="${3:-output}"
    
    log_info "Generating image with $model..."
    log_info "Prompt: $prompt"
    
    local workflow=$(cat <<WFEOF
{
  "prompt": {
    "1": { "inputs": { "ckpt_name": "$model" }, "class_type": "CheckpointLoaderSimple" },
    "2": { "inputs": { "text": "$prompt", "clip": ["1", 1] }, "class_type": "CLIPTextEncode" },
    "3": { "inputs": { "text": "blurry, low quality, distorted", "clip": ["1", 1] }, "class_type": "CLIPTextEncode" },
    "4": { "inputs": { "width": 512, "height": 512, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
    "5": { "inputs": { "seed": 42, "steps": $DEFAULT_STEPS, "cfg": 7, "sampler_name": "euler", "scheduler": "normal", "positive": ["2", 0], "negative": ["3", 0], "model": ["1", 0], "latent_image": ["4", 0], "denoise": 1.0 }, "class_type": "KSampler" },
    "6": { "inputs": { "samples": ["5", 0], "vae": ["1", 2] }, "class_type": "VAEDecode" },
    "7": { "inputs": { "filename_prefix": "$output_prefix", "images": ["6", 0] }, "class_type": "SaveImage" }
  }
}
WFEOF
)
    
    local response=$(curl -s -X POST "http://${COMFY_HOST}:${COMFY_PORT}/prompt" \
        -H "Content-Type: application/json" \
        -d "$workflow")
    
    if echo "$response" | grep -q "prompt_id"; then
        local prompt_id=$(echo "$response" | grep -o '"prompt_id":"[^"]*"' | cut -d'"' -f4)
        log_info "Job queued! ID: $prompt_id"
        echo "$prompt_id"
        return 0
    else
        log_error "Failed: $response"
        return 1
    fi
}

# Generate SDXL (default)
generate_sdxl() {
    generate_image "$DEFAULT_MODEL" "$1" "$2"
}

# Generate JuggernautXL (alternate)
generate_juggernaut() {
    generate_image "$JUGGERNAUT_MODEL" "$1" "$2"
}

case "$1" in
    check)
        if check_comfy; then
            log_info "ComfyUI running at http://${COMFY_HOST}:${COMFY_PORT}"
            log_info "DEFAULT MODEL: SDXL ($DEFAULT_MODEL)"
            log_info "ALTERNATE: JuggernautXL ($JUGGERNAUT_MODEL)"
            exit 0
        else
            log_error "ComfyUI NOT running"
            exit 1
        fi
        ;;
    launch)
        launch_comfy
        ;;
    generate)
        # Default: SDXL
        wait_for_comfy && generate_sdxl "$2" "$3"
        ;;
    juggernaut)
        # Explicit JuggernautXL
        wait_for_comfy && generate_juggernaut "$2" "$3"
        ;;
    test)
        wait_for_comfy && log_info "SDXL pipeline ready!"
        ;;
    outputs)
        ls -la "$OUTPUT_DIR" 2>/dev/null || log_error "Output dir not accessible"
        ;;
    models)
        log_info "Available models:"
        ls "$COMFY_DIR/models/checkpoints/" 2>/dev/null | grep -v "^put_"
        ;;
    *)
        echo "ComfyUI Bridge - SDXL Default"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  check            - Check ComfyUI status"
        echo "  launch           - Launch ComfyUI"
        echo "  generate         - Generate SDXL image (default)"
        echo "  juggernaut       - Generate JuggernautXL image"
        echo "  test             - Quick pipeline test"
        echo "  outputs          - List output images"
        echo "  models           - List available models"
        echo ""
        echo "MODELS:"
        echo "  DEFAULT:    SDXL ($DEFAULT_MODEL)"
        echo "  ALTERNATE:  JuggernautXL ($JUGGERNAUT_MODEL)"
        echo "  EXPERIMENTAL: SD 3.5 (unstable)"
        echo ""
        echo "ComfyUI: http://${COMFY_HOST}:${COMFY_PORT}"
        ;;
esac
