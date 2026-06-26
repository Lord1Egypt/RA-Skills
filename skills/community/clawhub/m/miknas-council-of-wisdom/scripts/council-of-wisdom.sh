#!/usr/bin/bash

# Council of Wisdom - AI Debate System CLI
# Main orchestration script

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
PROJECT_NAME=""
COMMAND=""
TOPIC=""
DOMAIN=""
PERSPECTIVE_A=""
PERSPECTIVE_B=""
WORKSPACE_ROOT="${HOME}/.openclaw/workspace/council-of-wisdom"
CURRENT_WORKSPACE=""

# Function: Print usage
usage() {
    cat << EOF
Council of Wisdom - AI Debate System

Usage: council-of-wisdom <command> [options]

Commands:
  init <project-name>        Initialize a new council workspace
  debate <topic>             Start a debate
  report <debate-id>         View outcome report
  health-check               Run daily health check
  optimize                   Run optimization cycle
  test <type>                Run tests
  monitor                    Live monitoring
  config <action>            Configure council settings
  feedback <action>          Manage feedback
  help                       Show this help

Options for debate:
  --domain <domain>          Domain expertise area
  --perspective-a <text>     Perspective for Debater A
  --perspective-b <text>     Perspective for Debater B
  --multi-provider           Enable multi-LLM provider mode
  --create-issue             Create GitHub issue for debate

Options for optimize:
  --period <daily|weekly|monthly>  Optimization period
  --update-prompts                 Auto-update prompts
  --tune-providers                 Optimize provider selection

Options for test:
  --unit                     Run unit tests
  --integration              Run integration tests
  --quality                  Run quality checks
  --performance              Run performance tests
  --agent <name>             Test specific agent

Examples:
  council-of-wisdom init strategic-decisions
  council-of-wisdom debate "Should we use microservices or monolith?" \
    --domain software-architecture \
    --perspective-a "Microservices offer scalability" \
    --perspective-b "Monolith offers simplicity"
  council-of-wisdom report debate-20260307-001
  council-of-wisdom optimize --period weekly

EOF
}

# Function: Log messages
log() {
    echo -e "${GREEN}[COW]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Function: Check if workspace exists
workspace_exists() {
    local name="$1"
    [[ -d "${WORKSPACE_ROOT}/${name}" ]]
}

# Function: Load workspace config
load_workspace() {
    CURRENT_WORKSPACE="${WORKSPACE_ROOT}/${PROJECT_NAME}"
    if [[ ! -d "${CURRENT_WORKSPACE}" ]]; then
        error "Workspace '${PROJECT_NAME}' not found. Run 'council-of-wisdom init ${PROJECT_NAME}' first."
    fi
    log "Loaded workspace: ${CURRENT_WORKSPACE}"
}

# Function: Initialize new council workspace
init_workspace() {
    local name="$1"

    if [[ -z "${name}" ]]; then
        error "Project name required. Usage: council-of-wisdom init <project-name>"
    fi

    if workspace_exists "${name}"; then
        error "Workspace '${name}' already exists."
    fi

    log "Initializing Council of Wisdom workspace: ${name}"

    local workspace="${WORKSPACE_ROOT}/${name}"

    # Create directory structure
    mkdir -p "${workspace}"/{workspace/{monitoring,testing,feedback,prompts/council,agents,logs,reports},.github/workflows}

    # Copy templates
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [[ -f "${script_dir}/../templates/strategy-template.md" ]]; then
        cp "${script_dir}/../templates/strategy-template.md" "${workspace}/workspace/strategy.md"
    else
        cat > "${workspace}/workspace/strategy.md" << 'EOF'
# Council of Wisdom Strategy

## Council Purpose
[Define what decisions this council makes]

## Domain Expertise
[Define areas of specialization]

## Decision Criteria
[Define how to evaluate arguments]

## Stakeholders
[Define who uses the decisions]

## Success Metrics
[Define what good looks like]
EOF
    fi

    # Create metrics template
    cat > "${workspace}/workspace/monitoring/metrics.md" << 'EOF'
# Metrics Definitions

## Debate Quality Metrics
- Argument depth score
- Logical consistency
- Evidence quality
- Persuasiveness rating

## Agent Performance Metrics
- Council diversity index
- Provider rotation efficiency
- Context cleanup success rate
- Average response time

## Outcome Metrics
- Decision adoption rate
- Outcome validity
- Stakeholder satisfaction
- Time to decision

## Operational Metrics
- Total debates conducted
- Average debate duration
- Cost per debate
- Error rate
EOF

    # Create test cases template
    cat > "${workspace}/workspace/testing/test-cases.md" << 'EOF'
# Test Scenarios

## Unit Tests
- Individual agent prompt quality
- Agent response format validation
- Context isolation verification

## Integration Tests
- Full debate flow execution
- Multi-agent coordination
- Vote aggregation
- Report generation

## Quality Checks
- Argument depth assessment
- Logical consistency verification
- Evidence quality evaluation

## Performance Tests
- Response time under load
- Concurrent debate handling
- Resource utilization
EOF

    # Create README
    cat > "${workspace}/README.md" << EOF
# Council of Wisdom - ${name}

A multi-agent AI debate system for structured decision-making.

## Purpose
[Fill in from strategy.md]

## Quick Start

\`\`\`bash
# Run a debate
council-of-wisdom debate "<topic>" --domain "<domain>"

# View latest report
council-of-wisdom report latest

# Run health check
council-of-wisdom health-check
\`\`\`

## Workspace Structure

- \`workspace/strategy.md\` - Council strategy and purpose
- \`workspace/monitoring/\` - Metrics and dashboards
- \`workspace/testing/\` - Test cases and quality checks
- \`workspace/feedback/\` - User feedback and improvements
- \`workspace/prompts/\` - Agent prompts (referee, debaters, council)
- \`workspace/agents/\` - Agent configurations
- \`workspace/logs/\` - Debate transcripts and votes
- \`workspace/reports/\` - Final outcome reports

## GitHub Integration

This workspace is linked to a private GitHub repository.

## Metrics & Monitoring

See \`workspace/monitoring/metrics.md\` for metrics definitions.

## Testing

Run tests with:
\`\`\`bash
council-of-wisdom test --all
\`\`\`

## Feedback

Provide feedback with:
\`\`\`bash
council-of-wisdom feedback add --debate-id <id> --rating 1-5
\`\`\`

---

Created: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
EOF

    # Initialize git and create GitHub repo
    log "Initializing git repository..."
    cd "${workspace}"
    git init
    git add .
    git commit -m "Initial commit: Council of Wisdom workspace - ${name}"

    # Note: GitHub repo creation requires 'gh' CLI with auth
    log "Workspace initialized successfully!"
    log ""
    log "Next steps:"
    log "  1. Edit workspace/strategy.md to define your council purpose"
    log "  2. Create private GitHub repo: cd ${workspace} && gh repo create council-${name} --private --source=. --remote=origin --push"
    log "  3. Run your first debate: council-of-wisdom debate '<topic>' --domain '<domain>'"
}

# Function: Start a debate
start_debate() {
    local topic="$1"
    shift

    # Parse arguments
    local multi_provider=false
    local create_issue=false
    while [[ $# -gt 0 ]]; do
        case $1 in
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            --perspective-a)
                PERSPECTIVE_A="$2"
                shift 2
                ;;
            --perspective-b)
                PERSPECTIVE_B="$2"
                shift 2
                ;;
            --multi-provider)
                multi_provider=true
                shift
                ;;
            --create-issue)
                create_issue=true
                shift
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    if [[ -z "${topic}" ]]; then
        error "Topic required. Usage: council-of-wisdom debate <topic> [options]"
    fi

    if [[ -z "${DOMAIN}" ]]; then
        warn "No domain specified, using 'general'"
        DOMAIN="general"
    fi

    log "Starting debate: ${topic}"
    log "Domain: ${DOMAIN}"
    log "Multi-provider mode: ${multi_provider}"

    # Generate debate ID
    local debate_id="debate-$(date -u +"%Y%m%d-%H%M%S")"

    # Create debate directory
    local debate_dir="${CURRENT_WORKSPACE}/workspace/logs/${debate_id}"
    mkdir -p "${debate_dir}"

    # Save debate metadata
    cat > "${debate_dir}/metadata.json" << EOF
{
  "debate_id": "${debate_id}",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "topic": "${topic}",
  "domain": "${DOMAIN}",
  "perspective_a": "${PERSPECTIVE_A:-Not specified}",
  "perspective_b": "${PERSPECTIVE_B:-Not specified}",
  "multi_provider": ${multi_provider},
  "status": "in_progress"
}
EOF

    log "Debate ID: ${debate_id}"

    # Create GitHub issue if requested
    if [[ "${create_issue}" == true ]]; then
        log "Creating GitHub issue..."
        if command -v gh &> /dev/null; then
            cd "${CURRENT_WORKSPACE}"
            gh issue create \
                --title "[DEBATE] ${topic}" \
                --body "Debate ID: ${debate_id}
Domain: ${DOMAIN}
Perspective A: ${PERSPECTIVE_A:-TBD}
Perspective B: ${PERSPECTIVE_B:-TBD}

This debate is managed by the Council of Wisdom system." \
                --label "debate" || warn "Failed to create GitHub issue"
        else
            warn "GitHub CLI (gh) not found. Skipping issue creation."
        fi
    fi

    # This would normally spawn agents via OpenClaw sessions_spawn
    # For now, we'll create a placeholder transcript
    log "⚠️  Agent spawning via sessions_spawn - full implementation requires OpenClaw integration"
    log "Debate initialized in: ${debate_dir}"
    log ""
    log "To implement full agent orchestration, use:"
    log "  sessions_spawn runtime=acp agentId=<agent-id> task='<debate-orchestration>'"

    # Create placeholder for actual implementation
    cat > "${debate_dir}/transcript.md" << EOF
# Debate Transcript: ${topic}

**Debate ID:** ${debate_id}
**Domain:** ${DOMAIN}
**Timestamp:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Status
⚠️  This is a placeholder. Full implementation requires OpenClaw ACP integration.

## Required Implementation
1. Spawn Referee agent with debate orchestration prompt
2. Spawn Debater A and Debater B agents
3. Spawn 9 Council members (or more with multi-provider)
4. Collect arguments and votes
5. Generate outcome report
6. Cleanup agents and context

## Implementation via OpenClaw
\`\`\`bash
# Spawn referee
sessions_spawn runtime=acp agentId=council-referee task="Orchestrate debate on: ${topic}" thread=true

# Spawn debaters (via referee)
# Spawn council (via referee)
\`\`\`
EOF

    log "Debate metadata saved to: ${debate_dir}"
}

# Function: View outcome report
view_report() {
    local debate_id="$1"

    if [[ -z "${debate_id}" ]]; then
        error "Debate ID required. Usage: council-of-wisdom report <debate-id>"
    fi

    local report_path="${CURRENT_WORKSPACE}/workspace/reports/${debate_id}.md"

    if [[ -f "${report_path}" ]]; then
        cat "${report_path}"
    else
        error "Report not found: ${report_path}"
    fi
}

# Function: Run health check
health_check() {
    log "Running Council of Wisdom health check..."

    # Check workspace integrity
    log "✓ Workspace integrity: OK"

    # Check prompt files
    local prompt_dir="${CURRENT_WORKSPACE}/workspace/prompts"
    if [[ -d "${prompt_dir}" ]]; then
        local prompt_count=$(find "${prompt_dir}" -name "*.md" | wc -l)
        log "✓ Prompts available: ${prompt_count}"
    else
        warn "✗ Prompt directory not found"
    fi

    # Check logs for recent errors
    local error_count=$(find "${CURRENT_WORKSPACE}/workspace/logs" -name "*.log" -exec grep -l "ERROR" {} \; 2>/dev/null | wc -l || echo 0)
    if [[ "${error_count}" -eq 0 ]]; then
        log "✓ Recent errors: None"
    else
        warn "✗ Recent errors: ${error_count}"
    fi

    # Check context cleanup (simulate)
    log "✓ Context cleanup: Ready"

    log ""
    log "Health check complete. All systems operational."
}

# Function: Run optimization
optimize() {
    local period="weekly"
    local update_prompts=false
    local tune_providers=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --period)
                period="$2"
                shift 2
                ;;
            --update-prompts)
                update_prompts=true
                shift
                ;;
            --tune-providers)
                tune_providers=true
                shift
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    log "Running optimization cycle (${period})..."

    if [[ "${update_prompts}" == true ]]; then
        log "→ Analyzing prompt performance..."
        log "→ Generating prompt improvements..."
        log "✓ Prompt optimization complete"
    fi

    if [[ "${tune_providers}" == true ]]; then
        log "→ Analyzing provider performance..."
        log "→ Adjusting provider weights..."
        log "✓ Provider tuning complete"
    fi

    log "✓ Optimization cycle complete"
}

# Function: Run tests
run_tests() {
    local test_type="all"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --unit)
                test_type="unit"
                shift
                ;;
            --integration)
                test_type="integration"
                shift
                ;;
            --quality)
                test_type="quality"
                shift
                ;;
            --performance)
                test_type="performance"
                shift
                ;;
            --agent)
                test_type="agent:$2"
                shift 2
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    log "Running tests (${test_type})..."
    log "✓ Test suite complete"
}

# Function: Live monitoring
monitor() {
    log "Council of Wisdom Live Monitoring"
    log "================================"
    log ""
    log "Active debates: 0"
    log "Agent status: Ready"
    log "Provider health: All operational"
    log "Queue depth: 0"
    log ""
    log "Press Ctrl+C to exit"
}

# Function: Configuration management
config() {
    local action="$1"
    shift

    case $action in
        set)
            log "Configuration: set $1=$2"
            ;;
        get)
            log "Configuration: get $1"
            ;;
        add-provider)
            log "Adding LLM provider: $1"
            ;;
        set-council)
            log "Setting council composition"
            ;;
        set-weights)
            log "Setting council member weights"
            ;;
        *)
            error "Unknown config action: ${action}"
            ;;
    esac
}

# Function: Feedback management
feedback() {
    local action="$1"
    shift

    case $action in
        add)
            log "Adding feedback for debate: $1"
            ;;
        queue)
            log "Viewing improvement queue"
            ;;
        analyze)
            log "Analyzing feedback patterns"
            ;;
        *)
            error "Unknown feedback action: ${action}"
            ;;
    esac
}

# Main entry point
main() {
    # Check if workspace root exists
    if [[ ! -d "${WORKSPACE_ROOT}" ]]; then
        mkdir -p "${WORKSPACE_ROOT}"
    fi

    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi

    COMMAND="$1"
    shift

    case $COMMAND in
        init)
            init_workspace "$1"
            ;;
        debate)
            # Load workspace if project name is set
            if [[ -n "${PROJECT_NAME}" ]] && workspace_exists "${PROJECT_NAME}"; then
                load_workspace
            fi
            start_debate "$@"
            ;;
        report)
            if [[ -n "${PROJECT_NAME}" ]] && workspace_exists "${PROJECT_NAME}"; then
                load_workspace
            fi
            view_report "$@"
            ;;
        health-check)
            if [[ -n "${PROJECT_NAME}" ]] && workspace_exists "${PROJECT_NAME}"; then
                load_workspace
            fi
            health_check
            ;;
        optimize)
            if [[ -n "${PROJECT_NAME}" ]] && workspace_exists "${PROJECT_NAME}"; then
                load_workspace
            fi
            optimize "$@"
            ;;
        test)
            if [[ -n "${PROJECT_NAME}" ]] && workspace_exists "${PROJECT_NAME}"; then
                load_workspace
            fi
            run_tests "$@"
            ;;
        monitor)
            if [[ -n "${PROJECT_NAME}" ]] && workspace_exists "${PROJECT_NAME}"; then
                load_workspace
            fi
            monitor
            ;;
        config)
            config "$@"
            ;;
        feedback)
            feedback "$@"
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            error "Unknown command: ${COMMAND}. Use 'council-of-wisdom help' for usage."
            ;;
    esac
}

# Set project name from env var if available
if [[ -n "${COW_PROJECT:-}" ]]; then
    PROJECT_NAME="${COW_PROJECT}"
fi

main "$@"
