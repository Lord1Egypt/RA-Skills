#!/bin/bash
######################################################### 
# deploy.sh
# vLLM LLMs Deployment General Script.
# Usage: [ENV VARIABLES] ./$0 <model_name> <model_org>
#########################################################

set -e

# ========== Default configuration, modifiable via parameters ==========
MODEL_NAME="${1:-Qwen3.5-0.8B}"
MODEL_ORG="${MODEL_ORG:-Qwen}"

# ========== Default configuration, modifiable via environment variables ==========
PORT="${PORT:-8000}"
GPU_COUNT="${GPU_COUNT:-1}"
ENV_NAME="${ENV_NAME:-vllm}"
PROXY="${PROXY:-http://proxyaddress:port}"
MODEL_BASE_PATH="${MODEL_BASE_PATH:-/home/work/models}"

# ========== Set network proxy ==========
export https_proxy="${PROXY}"
export http_proxy="${PROXY}"

# ========== Define colors ==========
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# ========== Help Information ==========
show_help() {
    echo "Usage: [ENV VARIABLES] $0 <model_name> <model_org> "
    echo ""
    echo "Examples:"
    echo "  PORT=8001 \\"
    echo "  GPU_COUNT=4 \\"
    echo "  $0 Qwen3.5-0.8B Qwen"
    echo ""
    echo "Environment Variables:"
    echo "  ENV_NAME        conda env name (default: vllm)"
    echo "  PORT            Service port (default: 8000)"
    echo "  GPU_COUNT       GPU parallel count (default: 1)"
    echo "  PROXY           Proxy address (default: http://proxyaddress:port)"
    echo "  MODEL_BASE_PATH Model storage path (default: /home/work/models)"
    exit 0
}

print_env_info() {
    local var_names=(
        "MODEL_NAME"
        "MODEL_ORG"
        "ENV_NAME"
        "PORT"
        "GPU_COUNT"
        "PROXY"
        "MODEL_BASE_PATH"
    )

    for var in "${var_names[@]}"; do
        local var_value="${!var}"
        printf "  %-16s %s\n" "$var:" "$var_value"
    done
}

# ========== Init conda ==========
init_conda() {
    local CONDA_INIT="$HOME/miniconda3/etc/profile.d/conda.sh"
    if [ -f "$CONDA_INIT" ]; then
        . "$CONDA_INIT"
        log_info "conda init success..."
    else
        log_error "conda initialization script does not exist: $CONDA_INIT"
        exit 1
    fi
}

# ========== Check environment ==========
check_environment() {
    log_step "Checking deployment environment..."

    # Check conda environment
    if ! conda env list | grep -q "^${ENV_NAME} "; then
        log_warn "conda environment '${ENV_NAME}' does not exist, creating..."
        conda create -n ${ENV_NAME} python=3.11 -y
        conda activate ${ENV_NAME}
        log_info "installing vLLM and ModelScope in environment: ${ENV_NAME}..."
        pip install vllm modelscope
    else
        log_info "Using existing environment: ${ENV_NAME}"
        conda activate ${ENV_NAME}
    fi

    # Check port
    if netstat -tlnp 2>/dev/null | grep -q ":${PORT} "; then
        log_warn "Port ${PORT} is already in use"
        local NEW_PORT=$((PORT + 1))
        log_info "Automatically switching to port: ${NEW_PORT}"
        PORT=${NEW_PORT}
    fi
}

# ========== Download the models ==========
download_model() {
    local MODEL_PATH="${MODEL_BASE_PATH}/${MODEL_NAME}"

    log_step " downloading model..."

    if [ -f "${MODEL_PATH}/config.json" ]; then
        log_info "Model already exists: ${MODEL_PATH} avoiding issues caused by incomplete model file downloads..."
        modelscope download \
            --model ${MODEL_ORG}/${MODEL_NAME} \
            --local_dir ${MODEL_PATH}
        return 0
    fi

    log_info "Creating model directory: ${MODEL_PATH}"
    mkdir -p ${MODEL_PATH}

    log_info "Downloading model from ModelScope: ${MODEL_ORG}/${MODEL_NAME}"
    log_info "This may take a long time, please wait..."
    modelscope download \
        --model ${MODEL_ORG}/${MODEL_NAME} \
        --local_dir ${MODEL_PATH}

    if [ ! -f "${MODEL_PATH}/config.json" ]; then
        log_error "Model download failed"
        exit 1
    fi

    log_info "✅ Model download completed"
}

# ========== start service ==========
start_service() {
    local MODEL_PATH="${MODEL_BASE_PATH}/${MODEL_NAME}"

    log_step "Starting vLLM service..."

    echo ""
    log_info "============================================"
    log_info "Model: ${MODEL_NAME}"
    log_info "Path: ${MODEL_PATH}"
    log_info "Port: ${PORT}"
    log_info "GPU Count: ${GPU_COUNT}"
    log_info "Access: http://localhost:${PORT}"
    log_info "============================================"
    log_info "Press Ctrl+C to stop the service..."
    echo ""

    vllm serve ${MODEL_PATH} \
        --tensor-parallel-size ${GPU_COUNT} \
        --gpu-memory-utilization 0.9 \
        --host 0.0.0.0 \
        --port ${PORT}
}

# ========== deploy model ==========
deploy_model() {
    log_info "🐵 deploying model: ${MODEL_NAME}"
    echo ""

    init_conda
    check_environment
    download_model
    start_service
}

main() {
    MODEL_NAME=$1

    if [ $# -eq 0 ]; then
        show_help
    elif [ $# -eq 1 ]; then
        MODEL_NAME=$1
    elif [ $# -eq 2 ]; then
        MODEL_ORG=$2
    else
        echo "params error..."
    fi

    print_env_info

    deploy_model
}

main "$@"