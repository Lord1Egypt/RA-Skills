#!/bin/bash
# Mermaid CLI Batch Export Script
# Simple wrapper for batch exporting Mermaid diagrams

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
FORMAT="png"
THEME="default"
OUTPUT_DIR="exports"
SCALE="1.0"
BACKGROUND="transparent"
VERBOSE="false"

# Help function
show_help() {
    cat << EOF
Mermaid CLI Batch Export Script

Usage: $0 [options] [input_files...]

Options:
  -h, --help            Show this help message
  -f, --format FORMAT   Output format: png, svg, pdf (default: png)
  -t, --theme THEME     Mermaid theme (default: default)
  -d, --output-dir DIR  Output directory (default: exports)
  -s, --scale SCALE     Scale factor (default: 1.0)
  -b, --background COLOR Background color (default: transparent)
  -v, --verbose         Verbose output
  --mermaid-cmd CMD     mermaid-cli command (default: mmdc or npx mmdc)

Examples:
  # Export all .mmd files to PNG
  $0 *.mmd
  
  # Export to SVG with dark theme
  $0 -f svg -t dark *.mmd
  
  # Export with custom output directory
  $0 -d diagrams *.mmd
  
  # Export with high resolution
  $0 -s 2.0 *.mmd
  
  # Export specific files
  $0 flowchart.mmd sequence.mmd
  
  # Use npx if mmdc not installed globally
  $0 --mermaid-cmd "npx mmdc" *.mmd

Supported themes: default, forest, dark, neutral
EOF
}

# Parse arguments
INPUT_FILES=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -t|--theme)
            THEME="$2"
            shift 2
            ;;
        -d|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -s|--scale)
            SCALE="$2"
            shift 2
            ;;
        -b|--background)
            BACKGROUND="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="true"
            shift
            ;;
        --mermaid-cmd)
            MERMAID_CMD="$2"
            shift 2
            ;;
        -*)
            echo -e "${RED}Error: Unknown option $1${NC}" >&2
            show_help
            exit 1
            ;;
        *)
            INPUT_FILES+=("$1")
            shift
            ;;
    esac
done

# Check for mermaid-cli
find_mermaid_cli() {
    if command -v mmdc &> /dev/null; then
        echo "mmdc"
    elif command -v npx &> /dev/null; then
        echo "npx mmdc"
    else
        echo ""
    fi
}

# Set mermaid command
if [ -z "${MERMAID_CMD:-}" ]; then
    MERMAID_CMD=$(find_mermaid_cli)
    if [ -z "$MERMAID_CMD" ]; then
        echo -e "${RED}Error: mermaid-cli not found${NC}" >&2
        echo "Install with: npm install -g @mermaid-js/mermaid-cli" >&2
        echo "Or use: npx @mermaid-js/mermaid-cli" >&2
        exit 1
    fi
fi

# Check input files
if [ ${#INPUT_FILES[@]} -eq 0 ]; then
    # No files specified, use all .mmd files in current directory
    INPUT_FILES=(*.mmd)
    if [ ${#INPUT_FILES[@]} -eq 0 ] || [ "${INPUT_FILES[0]}" = "*.mmd" ]; then
        echo -e "${YELLOW}No .mmd files found in current directory${NC}" >&2
        show_help
        exit 1
    fi
fi

# Validate format
case "$FORMAT" in
    png|svg|pdf)
        # Valid format
        ;;
    *)
        echo -e "${RED}Error: Invalid format '$FORMAT'. Must be png, svg, or pdf${NC}" >&2
        exit 1
        ;;
esac

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Export function
export_diagram() {
    local input_file="$1"
    local output_file="$2"
    
    if [ "$VERBOSE" = "true" ]; then
        echo -e "${BLUE}Exporting: $input_file -> $output_file${NC}"
    fi
    
    # Build command
    local cmd="$MERMAID_CMD"
    cmd+=" -i \"$input_file\""
    cmd+=" -o \"$output_file\""
    cmd+=" -t \"$THEME\""
    cmd+=" -b \"$BACKGROUND\""
    cmd+=" -s \"$SCALE\""
    
    # For PDF, we need Puppeteer config
    if [ "$FORMAT" = "pdf" ]; then
        local config_file="$(mktemp)"
        cat > "$config_file" << EOF
{
  "args": ["--no-sandbox", "--disable-setuid-sandbox"],
  "headless": "new"
}
EOF
        cmd+=" -p \"$config_file\""
    fi
    
    # Run command
    if eval "$cmd" 2>/dev/null; then
        if [ "$VERBOSE" = "true" ]; then
            echo -e "${GREEN}✓ Success: $output_file${NC}"
        fi
        return 0
    else
        echo -e "${RED}✗ Failed: $input_file${NC}" >&2
        return 1
    fi
    
    # Clean up
    if [ "$FORMAT" = "pdf" ] && [ -f "$config_file" ]; then
        rm -f "$config_file"
    fi
}

# Start batch export
echo -e "${BLUE}Starting batch export...${NC}"
echo -e "Format: $FORMAT, Theme: $THEME, Output: $OUTPUT_DIR/"
echo -e "Files to process: ${#INPUT_FILES[@]}"
echo ""

success_count=0
total_count=${#INPUT_FILES[@]}

for i in "${!INPUT_FILES[@]}"; do
    input_file="${INPUT_FILES[$i]}"
    
    if [ ! -f "$input_file" ]; then
        echo -e "${YELLOW}Warning: File not found: $input_file${NC}" >&2
        continue
    fi
    
    # Generate output filename
    filename=$(basename "$input_file" .mmd)
    output_file="$OUTPUT_DIR/${filename}.$FORMAT"
    
    # Show progress
    if [ "$VERBOSE" = "false" ]; then
        printf "[%3d/%3d] %s -> %s\n" \
            $((i + 1)) \
            $total_count \
            "$(basename "$input_file")" \
            "$(basename "$output_file")"
    fi
    
    # Export
    if export_diagram "$input_file" "$output_file"; then
        success_count=$((success_count + 1))
    fi
done

# Summary
echo ""
echo -e "${BLUE}Export Summary${NC}"
echo "==============="
echo -e "Total files:   $total_count"
echo -e "Successful:    ${GREEN}$success_count${NC}"
echo -e "Failed:        $((total_count - success_count))"
echo -e "Output folder: $OUTPUT_DIR/"

if [ $success_count -eq $total_count ]; then
    echo -e "${GREEN}✓ All exports successful!${NC}"
    exit 0
elif [ $success_count -gt 0 ]; then
    echo -e "${YELLOW}⚠ Some exports failed${NC}"
    exit 1
else
    echo -e "${RED}✗ All exports failed${NC}"
    exit 1
fi