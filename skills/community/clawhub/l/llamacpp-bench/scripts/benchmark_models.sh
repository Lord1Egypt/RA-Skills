#!/bin/bash
#
# Benchmark multiple GGUF models using llama-bench
# Usage: ./benchmark_models.sh [-o output_dir] model1.gguf [model2.gguf ...]
#

set -e

# Default values
OUTPUT_DIR="./benchmark_results"
LLAMA_BENCH=""
PROMPT_SIZES="512,1024,2048"
GEN_SIZES="128,256"
GPU_LAYERS=99

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to find llama-bench
find_llama_bench() {
    # Check common locations
    local paths=(
        "/DATA/Benchmark/llama.cpp/build/bin/llama-bench"
        "$HOME/Repo/llama.cpp/build/bin/llama-bench"
        "$HOME/lab/build/bin/llama-bench"
        "$HOME/Repo/ollama/llm/llama.cpp/build/linux/x86_64/rocm_v5/examples/llama-bench"
        "/usr/local/bin/llama-bench"
    )
    
    for path in "${paths[@]}"; do
        if [ -x "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    
    # Try to find it
    local found=$(find ~ /DATA 2>/dev/null | grep -E "llama-bench$" | head -1)
    if [ -n "$found" ] && [ -x "$found" ]; then
        echo "$found"
        return 0
    fi
    
    return 1
}

# Function to print usage
usage() {
    echo "Usage: $0 [-o output_dir] [-p prompt_sizes] [-n gen_sizes] [-g gpu_layers] model1.gguf [model2.gguf ...]"
    echo ""
    echo "Options:"
    echo "  -o    Output directory for results (default: ./benchmark_results)"
    echo "  -p    Prompt sizes to test (default: 512,1024,2048)"
    echo "  -n    Generation sizes to test (default: 128,256)"
    echo "  -g    GPU layers to offload (default: 99)"
    echo "  -h    Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -o ./results /DATA/GGUF/gemma-4-*.gguf"
    exit 1
}

# Parse arguments
while getopts "o:p:n:g:h" opt; do
    case $opt in
        o) OUTPUT_DIR="$OPTARG" ;;
        p) PROMPT_SIZES="$OPTARG" ;;
        n) GEN_SIZES="$OPTARG" ;;
        g) GPU_LAYERS="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

shift $((OPTIND-1))

# Check if models were provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No model files provided${NC}"
    usage
fi

# Find llama-bench
LLAMA_BENCH=$(find_llama_bench)
if [ -z "$LLAMA_BENCH" ]; then
    echo -e "${RED}Error: Could not find llama-bench executable${NC}"
    echo "Please ensure llama.cpp is built or provide the path to llama-bench"
    exit 1
fi

echo -e "${GREEN}Using llama-bench: $LLAMA_BENCH${NC}"

# Create output directory
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_FILE="$OUTPUT_DIR/benchmark_${TIMESTAMP}.md"

# Write header to results file
cat > "$RESULTS_FILE" << EOF
# llama.cpp Benchmark Results

**Date:** $(date)  
**llama-bench:** $LLAMA_BENCH  
**Prompt Sizes:** $PROMPT_SIZES  
**Generation Sizes:** $GEN_SIZES  
**GPU Layers:** $GPU_LAYERS

---

EOF

echo ""
echo -e "${GREEN}Starting benchmarks...${NC}"
echo "Results will be saved to: $RESULTS_FILE"
echo ""

# Benchmark each model
for model in "$@"; do
    if [ ! -f "$model" ]; then
        echo -e "${YELLOW}Warning: Model not found: $model${NC}"
        continue
    fi
    
    model_name=$(basename "$model" .gguf)
    echo -e "${GREEN}Benchmarking: $model_name${NC}"
    
    # Run benchmark
    echo "Running: $LLAMA_BENCH -m $model -p $PROMPT_SIZES -n $GEN_SIZES -ngl $GPU_LAYERS"
    
    # Append to results file
    echo "## $model_name" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo "\`\`\`" >> "$RESULTS_FILE"
    
    if $LLAMA_BENCH -m "$model" -p "$PROMPT_SIZES" -n "$GEN_SIZES" -ngl "$GPU_LAYERS" 2>&1 >> "$RESULTS_FILE"; then
        echo -e "${GREEN}✓ Completed: $model_name${NC}"
    else
        echo -e "${RED}✗ Failed: $model_name${NC}"
        echo "ERROR: Benchmark failed" >> "$RESULTS_FILE"
    fi
    
    echo "\`\`\`" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo "---" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    
    echo ""
done

echo -e "${GREEN}All benchmarks completed!${NC}"
echo "Results saved to: $RESULTS_FILE"
