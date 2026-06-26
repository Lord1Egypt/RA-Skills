#!/bin/bash
#
# Build or update llama.cpp from source with configurable backend
# Usage: ./build_llamacpp.sh [options]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
BUILD_DIR="${HOME}/Repo/llama.cpp"
BACKEND="vulkan"
UPDATE=false
CLEAN=false
JOBS=$(nproc)

# Usage
usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -d <dir>     Build directory (default: ~/Repo/llama.cpp)"
    echo "  -b <backend> Backend: vulkan, cuda, rocm, cpu (default: vulkan)"
    echo "  -u           Update to latest version from upstream"
    echo "  -c           Clean build (remove existing build directory)"
    echo "  -j <jobs>    Parallel jobs for make (default: $(nproc))"
    echo "  -v           Show current version and exit"
    echo "  -h           Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 -v                              # Show current version"
    echo "  $0 -u -b vulkan                    # Update and build with Vulkan"
    echo "  $0 -b cuda -d /custom/path         # Build with CUDA in custom dir"
    echo "  $0 -c -b rocm                      # Clean build with ROCm"
    exit 0
}

# Get current version from git
get_version() {
    if [ -d "$BUILD_DIR/.git" ]; then
        cd "$BUILD_DIR"
        local commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        local date=$(git log -1 --format=%cd --date=short 2>/dev/null || echo "unknown")
        local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        echo "Branch: $branch"
        echo "Commit: $commit"
        echo "Date: $date"
        
        # Check if behind upstream
        git fetch origin --quiet 2>/dev/null || true
        local behind=$(git rev-list HEAD..origin/master --count 2>/dev/null || echo "0")
        if [ "$behind" -gt 0 ]; then
            echo -e "${YELLOW}⚡ Behind upstream by $behind commits${NC}"
        else
            echo -e "${GREEN}✓ Up to date with upstream${NC}"
        fi
    else
        echo "Not a git repository or not cloned yet"
    fi
}

# Show current version info
show_version() {
    echo -e "${BLUE}=== llama.cpp Version Info ===${NC}"
    echo "Build directory: $BUILD_DIR"
    
    if [ ! -d "$BUILD_DIR" ]; then
        echo -e "${YELLOW}⚠ Not installed${NC}"
        echo "Run: $0 -u (to clone and build)"
        return
    fi
    
    get_version
    
    # Check for binary
    if [ -x "$BUILD_DIR/build/bin/llama-bench" ]; then
        echo ""
        echo -e "${GREEN}✓ llama-bench found${NC}"
        echo "Path: $BUILD_DIR/build/bin/llama-bench"
        
        # Show available backends
        echo ""
        echo "Available backends:"
        ls -la "$BUILD_DIR/build/bin/" | grep -E "libggml-(cuda|hip|vulkan|cpu)" || echo "  (check build directory for backend libraries)"
    else
        echo -e "${RED}✗ llama-bench not found${NC}"
        echo "Run: $0 (to build)"
    fi
}

# Clone or update repository
update_repo() {
    if [ -d "$BUILD_DIR/.git" ]; then
        echo -e "${BLUE}Updating existing repository...${NC}"
        cd "$BUILD_DIR"
        git fetch origin
        git pull origin master
    else
        echo -e "${BLUE}Cloning llama.cpp from GitHub...${NC}"
        mkdir -p "$(dirname "$BUILD_DIR")"
        git clone https://github.com/ggerganov/llama.cpp.git "$BUILD_DIR"
        cd "$BUILD_DIR"
    fi
    
    echo -e "${GREEN}✓ Repository ready${NC}"
}

# Clean build directory
clean_build() {
    if [ -d "$BUILD_DIR/build" ]; then
        echo -e "${YELLOW}Cleaning build directory...${NC}"
        rm -rf "$BUILD_DIR/build"
        echo -e "${GREEN}✓ Build directory cleaned${NC}"
    fi
}

# Build with selected backend
build() {
    echo ""
    echo -e "${BLUE}=== Building llama.cpp ===${NC}"
    echo "Backend: $BACKEND"
    echo "Jobs: $JOBS"
    echo ""
    
    cd "$BUILD_DIR"
    mkdir -p build
    cd build
    
    case "$BACKEND" in
        cuda)
            echo "Configuring for CUDA..."
            cmake .. -DLLAMA_CUDA=ON -DLLAMA_BUILD_TESTS=OFF
            ;;
        rocm)
            echo "Configuring for ROCm..."
            cmake .. -DLLAMA_HIPBLAS=ON -DLLAMA_BUILD_TESTS=OFF
            ;;
        vulkan)
            echo "Configuring for Vulkan..."
            cmake .. -DLLAMA_VULKAN=ON -DLLAMA_BUILD_TESTS=OFF
            ;;
        cpu)
            echo "Configuring for CPU only..."
            cmake .. -DLLAMA_BUILD_TESTS=OFF
            ;;
        *)
            echo -e "${RED}Unknown backend: $BACKEND${NC}"
            exit 1
            ;;
    esac
    
    echo ""
    echo "Building..."
    cmake --build . --config Release -j "$JOBS"
    
    echo ""
    echo -e "${GREEN}✓ Build complete!${NC}"
    echo "llama-bench: $BUILD_DIR/build/bin/llama-bench"
}

# Main
while getopts "d:b:ucj:vh" opt; do
    case $opt in
        d) BUILD_DIR="$OPTARG" ;;
        b) BACKEND="$OPTARG" ;;
        u) UPDATE=true ;;
        c) CLEAN=true ;;
        j) JOBS="$OPTARG" ;;
        v) show_version; exit 0 ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Show version info first
show_version
echo ""

# If only showing version, exit
if [ "$UPDATE" = false ] && [ "$CLEAN" = false ] && [ -x "$BUILD_DIR/build/bin/llama-bench" ]; then
    echo "llama.cpp is already built. Use -u to update or -c for clean build."
    exit 0
fi

# Interactive mode if update flag not set
if [ "$UPDATE" = false ] && [ -d "$BUILD_DIR/.git" ]; then
    read -p "Update to latest version from GitHub? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        UPDATE=true
    fi
fi

# Interactive backend selection if not specified
if [ "$BACKEND" = "vulkan" ] && [ "$UPDATE" = true ]; then
    echo ""
    echo "Select backend:"
    echo "  1) Vulkan (cross-platform GPU, recommended for AMD)"
    echo "  2) CUDA (NVIDIA GPUs)"
    echo "  3) ROCm (AMD GPUs)"
    echo "  4) CPU only"
    read -p "Choice [1-4]: " -n 1 -r
    echo
    case $REPLY in
        1) BACKEND="vulkan" ;;
        2) BACKEND="cuda" ;;
        3) BACKEND="rocm" ;;
        4) BACKEND="cpu" ;;
        *) echo "Invalid choice, using Vulkan"; BACKEND="vulkan" ;;
    esac
fi

# Execute
if [ "$UPDATE" = true ]; then
    update_repo
fi

if [ "$CLEAN" = true ]; then
    clean_build
fi

# Build if needed
if [ "$UPDATE" = true ] || [ "$CLEAN" = true ] || [ ! -x "$BUILD_DIR/build/bin/llama-bench" ]; then
    build
    echo ""
    show_version
fi
