#!/bin/bash
set -e

# ==============================================================================
# leio-sdlc Test Runner
# Provides a self-documenting CLI for running Mock/E2E tests against SDLC CUJs.
# ==============================================================================

print_help() {
    echo "🦞 leio-sdlc Test Runner CLI"
    echo ""
    echo "Usage: ./run_sdlc_tests.sh [OPTIONS]"
    echo ""
    echo "Description:"
    echo "  Executes Agentic Unit Tests (Mock Tests) for the LEIO SDLC skill."
    echo "  These tests use SDLC_TEST_MODE to intercept LLM tool calls safely."
    echo ""
    echo "Options:"
    echo "  --all       Run all Critical User Journey (CUJ) tests (1 through 5)"
    echo "  --cuj <N>   Run a specific CUJ test (1, 2, 3, 4, or 5)"
    echo "  -h, --help  Show this help message and exit"
    echo ""
    echo "Examples:"
    echo "  ./run_sdlc_tests.sh --all"
    echo "  ./run_sdlc_tests.sh --cuj 3"
}

run_cuj() {
    local cuj_num=$1
    local script_path="scripts/test_cuj_${cuj_num}_mock.sh"
    
    if [ ! -f "$script_path" ]; then
        echo "❌ Error: Test script $script_path not found."
        exit 1
    fi
    
    echo "======================================"
    echo "▶️  STARTING: CUJ-${cuj_num} Mock Test"
    echo "======================================"
    bash "$script_path"
    echo -e "✅ CUJ-${cuj_num} PASSED\n"
}

# Require at least one argument
if [ $# -eq 0 ]; then
    print_help
    exit 0
fi

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --all)
            for i in {1..5}; do
                run_cuj "$i"
            done
            exit 0
            ;;
        --cuj)
            if [[ -n "$2" && "$2" =~ ^[1-5]$ ]]; then
                run_cuj "$2"
                exit 0
            else
                echo "❌ Error: --cuj requires a number between 1 and 5."
                exit 1
            fi
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo "❌ Unknown parameter passed: $1"
            echo "Run with --help for usage instructions."
            exit 1
            ;;
    esac
    shift
done
