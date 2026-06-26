#!/usr/bin/env bash
# SkillBoss API Hub CLI — PPT / Presentation Generation
# Generate presentations, documents, and social posts via SkillBoss API Hub

set -euo pipefail

API_BASE="https://api.heybossai.com/v1"

# Check for API key
if [[ -z "${SKILLBOSS_API_KEY:-}" ]]; then
    echo "Error: SKILLBOSS_API_KEY environment variable not set" >&2
    exit 1
fi

usage() {
    cat << 'EOF'
Usage: gamma.sh <command> [options]

Commands:
  generate <content>    Generate a new presentation/document/social post
  help                 Show this help

Generate Options:
  --format <type>       presentation|document|social (default: presentation)
  --cards <num>         Number of cards/slides (default: 10)
  --instructions <str>  Additional styling instructions
  --amount <type>       concise|detailed (default: detailed)
  --tone <str>          e.g., "professional", "casual"
  --audience <str>      e.g., "investors", "developers"
  --image-source <type> aiGenerated|web|none (default: aiGenerated)
  --image-style <type>  illustration|photo (default: illustration)
  --dimensions <type>   fluid|16x9|4x3|1x1|4x5|9x16 (default: fluid)
  --wait                (no-op: SkillBoss API Hub is synchronous)

Examples:
  gamma.sh generate "AI automation trends" --wait
  gamma.sh generate "$(cat content.md)" --format presentation --cards 12 --wait
EOF
}

# API request helper — routes all calls through SkillBoss /v1/pilot
api_pilot() {
    local body="$1"
    curl -s \
        -X POST \
        -H "Authorization: Bearer ${SKILLBOSS_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$body" \
        "${API_BASE}/pilot"
}

# Generate command
cmd_generate() {
    local content=""
    local format="presentation"
    local cards=10
    local instructions=""
    local amount="detailed"
    local tone=""
    local audience=""
    local image_source="aiGenerated"
    local image_style="illustration"
    local dimensions="fluid"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --format)
                format="$2"
                shift 2
                ;;
            --cards)
                cards="$2"
                shift 2
                ;;
            --instructions)
                instructions="$2"
                shift 2
                ;;
            --amount)
                amount="$2"
                shift 2
                ;;
            --tone)
                tone="$2"
                shift 2
                ;;
            --audience)
                audience="$2"
                shift 2
                ;;
            --image-source)
                image_source="$2"
                shift 2
                ;;
            --image-style)
                image_style="$2"
                shift 2
                ;;
            --dimensions)
                dimensions="$2"
                shift 2
                ;;
            --wait)
                # SkillBoss API Hub is synchronous — --wait is accepted for compatibility
                shift
                ;;
            -*)
                echo "Unknown option: $1" >&2
                exit 1
                ;;
            *)
                if [[ -z "$content" ]]; then
                    content="$1"
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$content" ]]; then
        echo "Error: Content is required" >&2
        echo "Usage: gamma.sh generate <content> [options]" >&2
        exit 1
    fi

    # Build inputs JSON
    local json_content
    json_content=$(printf '%s' "$content" | jq -Rs .)

    local inputs
    inputs=$(jq -n \
        --argjson inputText "$json_content" \
        --arg format "$format" \
        --argjson numCards "$cards" \
        --arg amount "$amount" \
        --arg imageSource "$image_source" \
        --arg imageStyle "$image_style" \
        --arg dimensions "$dimensions" \
        '{
            inputText: $inputText,
            textMode: "generate",
            format: $format,
            numCards: $numCards,
            textOptions: {
                amount: $amount
            },
            imageOptions: {
                source: $imageSource,
                style: $imageStyle
            },
            cardOptions: {
                dimensions: $dimensions
            }
        }')

    # Add optional fields
    if [[ -n "$instructions" ]]; then
        inputs=$(echo "$inputs" | jq --arg v "$instructions" '. + {additionalInstructions: $v}')
    fi
    if [[ -n "$tone" ]]; then
        inputs=$(echo "$inputs" | jq --arg v "$tone" '.textOptions.tone = $v')
    fi
    if [[ -n "$audience" ]]; then
        inputs=$(echo "$inputs" | jq --arg v "$audience" '.textOptions.audience = $v')
    fi

    # Wrap as SkillBoss /v1/pilot request
    local pilot_body
    pilot_body=$(jq -n --argjson inputs "$inputs" '{type: "ppt", inputs: $inputs, prefer: "balanced"}')

    # Make request — SkillBoss returns synchronously
    local response
    response=$(api_pilot "$pilot_body")

    local url
    url=$(echo "$response" | jq -r '.result.gammaUrl // empty')

    if [[ -z "$url" ]]; then
        echo "Error creating presentation:" >&2
        echo "$response" >&2
        exit 1
    fi

    echo "Generation complete!"
    echo "URL: $url"
}

# Main
case "${1:-help}" in
    generate)
        shift
        cmd_generate "$@"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo "Unknown command: $1" >&2
        usage
        exit 1
        ;;
esac
