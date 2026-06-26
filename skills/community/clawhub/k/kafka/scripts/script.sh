#!/usr/bin/env bash
###############################################################################
# Kafka CLI Helper
# A comprehensive Apache Kafka management tool for common operations.
#
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
#
# Requirements: Kafka CLI tools (kafka-topics.sh, kafka-console-producer.sh,
#               kafka-console-consumer.sh, kafka-consumer-groups.sh)
#
# Usage: script.sh <command> [arguments...]
#
# Commands:
#   topics                    List all topics
#   create-topic <name> [p]   Create topic with optional partitions (default: 1)
#   describe <topic>          Describe a topic in detail
#   produce <topic> <msg>     Produce a message to a topic
#   consume <topic> [count]   Consume messages from a topic
#   groups                    List all consumer groups
#   lag <group>               Show consumer group lag
#   config                    Show current Kafka connection config
#   status                    Check cluster/broker status
#   delete-topic <topic>      Delete a topic
#   partitions <topic> <n>    Increase partitions for a topic
#   offsets <topic>           Show topic offsets (earliest and latest)
#   help                      Show this help message
###############################################################################
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
DATA_DIR="${HOME}/.local/share/kafka-helper"
LOG_FILE="${DATA_DIR}/kafka-helper.log"

# Kafka connection defaults
KAFKA_BOOTSTRAP="${KAFKA_BOOTSTRAP:-localhost:9092}"
KAFKA_ZOOKEEPER="${KAFKA_ZOOKEEPER:-localhost:2181}"
KAFKA_HOME="${KAFKA_HOME:-}"
KAFKA_CONFIG_FILE="${KAFKA_CONFIG_FILE:-}"

BRAND="Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

###############################################################################
# Utility functions
###############################################################################

_init() {
    mkdir -p "$DATA_DIR"
    touch "$LOG_FILE"
}

_log() {
    local ts
    ts="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$ts] $*" >> "$LOG_FILE"
}

_info()  { echo -e "${GREEN}[✓]${NC} $*"; }
_warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
_error() { echo -e "${RED}[✗]${NC} $*" >&2; }
_header(){ echo -e "${BOLD}${CYAN}═══ $* ═══${NC}"; }

_find_kafka_bin() {
    local bin_name="$1"

    # 1. Check KAFKA_HOME/bin
    if [[ -n "$KAFKA_HOME" && -x "${KAFKA_HOME}/bin/${bin_name}" ]]; then
        echo "${KAFKA_HOME}/bin/${bin_name}"
        return 0
    fi

    # 2. Check PATH (works for packages, docker, brew etc.)
    if command -v "$bin_name" &>/dev/null; then
        command -v "$bin_name"
        return 0
    fi

    # 3. Check common install locations
    local search_dirs=(
        /opt/kafka/bin
        /usr/local/kafka/bin
        /opt/bitnami/kafka/bin
        /usr/share/kafka/bin
        /usr/lib/kafka/bin
    )
    for dir in "${search_dirs[@]}"; do
        if [[ -x "${dir}/${bin_name}" ]]; then
            echo "${dir}/${bin_name}"
            return 0
        fi
    done

    return 1
}

_check_kafka_tools() {
    local required_tools=("kafka-topics.sh" "kafka-console-producer.sh" "kafka-console-consumer.sh" "kafka-consumer-groups.sh")
    local missing=()

    for tool in "${required_tools[@]}"; do
        if ! _find_kafka_bin "$tool" &>/dev/null; then
            missing+=("$tool")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        _error "Missing Kafka CLI tools: ${missing[*]}"
        echo ""
        echo "Install options:"
        echo "  1. Download from https://kafka.apache.org/downloads"
        echo "  2. Set KAFKA_HOME to your Kafka installation directory"
        echo "  3. Ensure kafka-*.sh scripts are in your PATH"
        echo ""
        echo "  Example: export KAFKA_HOME=/opt/kafka"
        echo ""
        echo "For Docker: docker exec -it <kafka-container> kafka-topics.sh ..."
        exit 1
    fi
}

_kafka_topics() {
    local bin
    bin="$(_find_kafka_bin "kafka-topics.sh")"
    local cmd=("$bin" --bootstrap-server "$KAFKA_BOOTSTRAP")
    if [[ -n "$KAFKA_CONFIG_FILE" && -f "$KAFKA_CONFIG_FILE" ]]; then
        cmd+=(--command-config "$KAFKA_CONFIG_FILE")
    fi
    "${cmd[@]}" "$@"
}

_kafka_producer() {
    local bin
    bin="$(_find_kafka_bin "kafka-console-producer.sh")"
    local cmd=("$bin" --bootstrap-server "$KAFKA_BOOTSTRAP")
    if [[ -n "$KAFKA_CONFIG_FILE" && -f "$KAFKA_CONFIG_FILE" ]]; then
        cmd+=(--producer.config "$KAFKA_CONFIG_FILE")
    fi
    "${cmd[@]}" "$@"
}

_kafka_consumer() {
    local bin
    bin="$(_find_kafka_bin "kafka-console-consumer.sh")"
    local cmd=("$bin" --bootstrap-server "$KAFKA_BOOTSTRAP")
    if [[ -n "$KAFKA_CONFIG_FILE" && -f "$KAFKA_CONFIG_FILE" ]]; then
        cmd+=(--consumer.config "$KAFKA_CONFIG_FILE")
    fi
    "${cmd[@]}" "$@"
}

_kafka_groups() {
    local bin
    bin="$(_find_kafka_bin "kafka-consumer-groups.sh")"
    local cmd=("$bin" --bootstrap-server "$KAFKA_BOOTSTRAP")
    if [[ -n "$KAFKA_CONFIG_FILE" && -f "$KAFKA_CONFIG_FILE" ]]; then
        cmd+=(--command-config "$KAFKA_CONFIG_FILE")
    fi
    "${cmd[@]}" "$@"
}

_kafka_configs() {
    local bin
    bin="$(_find_kafka_bin "kafka-configs.sh")" 2>/dev/null || true
    if [[ -z "$bin" ]]; then
        _error "kafka-configs.sh not found"
        return 1
    fi
    local cmd=("$bin" --bootstrap-server "$KAFKA_BOOTSTRAP")
    if [[ -n "$KAFKA_CONFIG_FILE" && -f "$KAFKA_CONFIG_FILE" ]]; then
        cmd+=(--command-config "$KAFKA_CONFIG_FILE")
    fi
    "${cmd[@]}" "$@"
}

###############################################################################
# Command implementations
###############################################################################

cmd_topics() {
    _header "Kafka Topics"
    echo -e "${BLUE}Broker:${NC} $KAFKA_BOOTSTRAP"
    echo ""

    local topics_output
    topics_output="$(_kafka_topics --list 2>&1)"
    if [[ -z "$topics_output" ]]; then
        echo "(no topics found)"
        return 0
    fi

    local count
    count="$(echo "$topics_output" | wc -l)"
    echo -e "${BOLD}Found:${NC} $count topic(s)"
    echo ""

    # Get partition counts for each topic
    echo "$topics_output" | while IFS= read -r topic; do
        [[ -z "$topic" ]] && continue
        local partitions
        partitions="$(_kafka_topics --describe --topic "$topic" 2>/dev/null | grep -c 'Partition:' || echo '?')"
        printf "  %-50s  partitions: %s\n" "$topic" "$partitions"
    done

    _log "TOPICS: count=$count"
}

cmd_create_topic() {
    local name="${1:?Usage: $SCRIPT_NAME create-topic <name> [partitions] [replication-factor]}"
    local partitions="${2:-1}"
    local replication="${3:-1}"

    _header "Create Topic"
    echo -e "${BLUE}Name:${NC}        $name"
    echo -e "${BLUE}Partitions:${NC}  $partitions"
    echo -e "${BLUE}Replication:${NC} $replication"
    echo ""

    local output
    output="$(_kafka_topics --create \
        --topic "$name" \
        --partitions "$partitions" \
        --replication-factor "$replication" 2>&1)" || {
        _error "Failed to create topic: $output"
        _log "CREATE-TOPIC: name=$name FAILED: $output"
        return 1
    }

    _info "Topic '$name' created successfully"
    _log "CREATE-TOPIC: name=$name partitions=$partitions replication=$replication"
}

cmd_describe() {
    local topic="${1:?Usage: $SCRIPT_NAME describe <topic>}"

    _header "Topic: $topic"

    local output
    output="$(_kafka_topics --describe --topic "$topic" 2>&1)" || {
        _error "Failed to describe topic: $output"
        return 1
    }

    if [[ -z "$output" ]]; then
        _warn "Topic '$topic' not found"
        return 1
    fi

    # Parse and display topic info
    local topic_line
    topic_line="$(echo "$output" | head -1)"
    echo -e "${BOLD}Configuration:${NC}"
    echo "  $topic_line"
    echo ""

    # Display partition details
    local partition_lines
    partition_lines="$(echo "$output" | tail -n +2)"
    if [[ -n "$partition_lines" ]]; then
        local part_count
        part_count="$(echo "$partition_lines" | wc -l)"
        echo -e "${BOLD}Partitions:${NC} $part_count"
        echo ""
        printf "  ${BOLD}%-12s %-10s %-20s %-20s %-10s${NC}\n" "Partition" "Leader" "Replicas" "ISR" "Offline"

        echo "$partition_lines" | while IFS= read -r line; do
            local part leader replicas isr
            part="$(echo "$line" | grep -oP 'Partition:\s*\K[0-9]+' || echo '?')"
            leader="$(echo "$line" | grep -oP 'Leader:\s*\K[0-9]+' || echo '?')"
            replicas="$(echo "$line" | grep -oP 'Replicas:\s*\K[0-9,]+' || echo '?')"
            isr="$(echo "$line" | grep -oP 'Isr:\s*\K[0-9,]+' || echo '?')"
            printf "  %-12s %-10s %-20s %-20s\n" "$part" "$leader" "$replicas" "$isr"
        done
    fi

    # Try to get topic configs
    echo ""
    echo -e "${BOLD}Topic Configs:${NC}"
    _kafka_configs --entity-type topics --entity-name "$topic" --describe 2>/dev/null | tail -n +1 || echo "  (unable to retrieve configs)"

    _log "DESCRIBE: topic=$topic"
}

cmd_produce() {
    local topic="${1:?Usage: $SCRIPT_NAME produce <topic> <message> [key]}"
    local message="${2:?Usage: $SCRIPT_NAME produce <topic> <message> [key]}"
    local key="${3:-}"

    _header "Produce Message"

    local payload="$message"
    local extra_args=()

    if [[ -n "$key" ]]; then
        payload="${key}:${message}"
        extra_args+=(--property "parse.key=true" --property "key.separator=:")
        echo -e "${BLUE}Key:${NC}   $key"
    fi

    echo -e "${BLUE}Topic:${NC} $topic"
    echo -e "${BLUE}Size:${NC}  ${#message} bytes"

    echo "$payload" | _kafka_producer --topic "$topic" "${extra_args[@]}" 2>&1 || {
        _error "Failed to produce message"
        _log "PRODUCE: topic=$topic FAILED"
        return 1
    }

    _info "Message sent to '$topic'"
    _log "PRODUCE: topic=$topic size=${#message}"
}

cmd_consume() {
    local topic="${1:?Usage: $SCRIPT_NAME consume <topic> [count] [from-beginning]}"
    local count="${2:-10}"
    local from_beginning="${3:-true}"

    _header "Consume Messages from: $topic"
    echo -e "${BLUE}Max messages:${NC} $count"
    echo ""

    local args=(--topic "$topic" --max-messages "$count" --property "print.timestamp=true" --property "print.key=true")

    if [[ "$from_beginning" == "true" || "$from_beginning" == "beginning" ]]; then
        args+=(--from-beginning)
        echo -e "${YELLOW}Reading from beginning...${NC}"
    else
        echo -e "${YELLOW}Reading new messages (Ctrl+C to stop)...${NC}"
    fi

    echo ""
    local msg_count=0
    _kafka_consumer "${args[@]}" 2>/dev/null | while IFS= read -r line; do
        (( msg_count++ ))
        echo -e "  ${GREEN}[$msg_count]${NC} $line"
    done

    _log "CONSUME: topic=$topic count=$count"
}

cmd_groups() {
    _header "Consumer Groups"
    echo -e "${BLUE}Broker:${NC} $KAFKA_BOOTSTRAP"
    echo ""

    local output
    output="$(_kafka_groups --list 2>&1)"

    if [[ -z "$output" ]]; then
        echo "(no consumer groups found)"
        return 0
    fi

    local count
    count="$(echo "$output" | wc -l)"
    echo -e "${BOLD}Found:${NC} $count group(s)"
    echo ""

    echo "$output" | while IFS= read -r group; do
        [[ -z "$group" ]] && continue
        # Try to get group state
        local state
        state="$(_kafka_groups --describe --group "$group" 2>/dev/null | head -1 || echo '')"
        printf "  %-50s\n" "$group"
    done

    _log "GROUPS: count=$count"
}

cmd_lag() {
    local group="${1:?Usage: $SCRIPT_NAME lag <consumer-group>}"

    _header "Consumer Group Lag: $group"

    local output
    output="$(_kafka_groups --describe --group "$group" 2>&1)" || {
        _error "Failed to get lag for group: $group"
        _error "$output"
        return 1
    }

    if echo "$output" | grep -qi "does not exist"; then
        _warn "Consumer group '$group' does not exist"
        return 1
    fi

    echo "$output"
    echo ""

    # Calculate total lag
    local total_lag=0
    while IFS= read -r line; do
        local lag_val
        lag_val="$(echo "$line" | awk '{print $6}')" 2>/dev/null || continue
        if [[ "$lag_val" =~ ^[0-9]+$ ]]; then
            total_lag=$(( total_lag + lag_val ))
        fi
    done <<< "$output"

    echo ""
    if [[ "$total_lag" -gt 0 ]]; then
        echo -e "  ${BOLD}Total Lag:${NC} ${RED}${total_lag}${NC} messages behind"
    else
        echo -e "  ${BOLD}Total Lag:${NC} ${GREEN}0${NC} (caught up)"
    fi

    _log "LAG: group=$group total_lag=$total_lag"
}

cmd_config() {
    _header "Kafka Configuration"
    echo ""
    echo -e "  ${BOLD}Bootstrap Servers:${NC}  $KAFKA_BOOTSTRAP"
    echo -e "  ${BOLD}Zookeeper:${NC}          $KAFKA_ZOOKEEPER"
    echo -e "  ${BOLD}KAFKA_HOME:${NC}         ${KAFKA_HOME:-<not set>}"
    echo -e "  ${BOLD}Config File:${NC}        ${KAFKA_CONFIG_FILE:-<not set>}"
    echo ""

    echo -e "${BOLD}Available Tools:${NC}"
    local tools=("kafka-topics.sh" "kafka-console-producer.sh" "kafka-console-consumer.sh" "kafka-consumer-groups.sh" "kafka-configs.sh" "kafka-broker-api-versions.sh")
    for tool in "${tools[@]}"; do
        local path
        if path="$(_find_kafka_bin "$tool" 2>/dev/null)"; then
            echo -e "  ${GREEN}✓${NC} $tool → $path"
        else
            echo -e "  ${RED}✗${NC} $tool (not found)"
        fi
    done

    echo ""
    echo -e "${BOLD}Environment Variables:${NC}"
    echo "  KAFKA_BOOTSTRAP    Bootstrap servers (default: localhost:9092)"
    echo "  KAFKA_ZOOKEEPER    Zookeeper address (default: localhost:2181)"
    echo "  KAFKA_HOME         Kafka installation directory"
    echo "  KAFKA_CONFIG_FILE  Client config file (for auth/SSL)"

    _log "CONFIG: displayed"
}

cmd_status() {
    _header "Kafka Cluster Status"
    echo -e "${BLUE}Broker:${NC} $KAFKA_BOOTSTRAP"
    echo ""

    # Check broker connectivity by listing topics
    echo -e "${BOLD}Connectivity:${NC}"
    local start_ms
    start_ms="$(date +%s%3N)"
    if _kafka_topics --list &>/dev/null; then
        local end_ms
        end_ms="$(date +%s%3N)"
        local latency=$(( end_ms - start_ms ))
        _info "Connected to broker ($latency ms)"
    else
        _error "Cannot connect to broker at $KAFKA_BOOTSTRAP"
        return 1
    fi

    # Topic count
    local topics
    topics="$(_kafka_topics --list 2>/dev/null)"
    local topic_count
    if [[ -n "$topics" ]]; then
        topic_count="$(echo "$topics" | wc -l)"
    else
        topic_count=0
    fi
    echo -e "  ${BOLD}Topics:${NC}           $topic_count"

    # Consumer group count
    local groups
    groups="$(_kafka_groups --list 2>/dev/null)"
    local group_count
    if [[ -n "$groups" ]]; then
        group_count="$(echo "$groups" | wc -l)"
    else
        group_count=0
    fi
    echo -e "  ${BOLD}Consumer Groups:${NC}  $group_count"

    # Try to get broker info via kafka-broker-api-versions
    local api_bin
    if api_bin="$(_find_kafka_bin "kafka-broker-api-versions.sh" 2>/dev/null)"; then
        echo ""
        echo -e "${BOLD}Broker Details:${NC}"
        local api_output
        api_output="$("$api_bin" --bootstrap-server "$KAFKA_BOOTSTRAP" 2>/dev/null | head -5)" || true
        if [[ -n "$api_output" ]]; then
            echo "$api_output" | while IFS= read -r line; do
                echo "  $line"
            done
        fi
    fi

    # Show under-replicated partitions
    echo ""
    echo -e "${BOLD}Under-replicated Partitions:${NC}"
    local urp
    urp="$(_kafka_topics --describe --under-replicated-partitions 2>/dev/null)" || true
    if [[ -z "$urp" ]]; then
        echo -e "  ${GREEN}None${NC} — all partitions are fully replicated"
    else
        echo -e "  ${RED}WARNING:${NC}"
        echo "$urp" | while IFS= read -r line; do
            echo "    $line"
        done
    fi

    _log "STATUS: topics=$topic_count groups=$group_count"
}

cmd_delete_topic() {
    local topic="${1:?Usage: $SCRIPT_NAME delete-topic <topic>}"

    _warn "This will permanently delete topic '$topic'"
    read -rp "Type the topic name to confirm: " confirm
    if [[ "$confirm" != "$topic" ]]; then
        _warn "Aborted."
        return 0
    fi

    local output
    output="$(_kafka_topics --delete --topic "$topic" 2>&1)" || {
        _error "Failed to delete topic: $output"
        return 1
    }
    _info "Topic '$topic' deleted (may take a moment to propagate)"
    _log "DELETE-TOPIC: topic=$topic"
}

cmd_partitions() {
    local topic="${1:?Usage: $SCRIPT_NAME partitions <topic> <new-count>}"
    local new_count="${2:?Usage: $SCRIPT_NAME partitions <topic> <new-count>}"

    _warn "Increasing partitions for '$topic' to $new_count (cannot be undone)"
    local output
    output="$(_kafka_topics --alter --topic "$topic" --partitions "$new_count" 2>&1)" || {
        _error "Failed to alter partitions: $output"
        return 1
    }
    _info "Partitions for '$topic' set to $new_count"
    _log "PARTITIONS: topic=$topic new_count=$new_count"
}

cmd_offsets() {
    local topic="${1:?Usage: $SCRIPT_NAME offsets <topic>}"

    _header "Offsets for: $topic"

    local get_offsets_bin
    if get_offsets_bin="$(_find_kafka_bin "kafka-get-offsets.sh" 2>/dev/null)"; then
        echo -e "${BOLD}Earliest:${NC}"
        "$get_offsets_bin" --bootstrap-server "$KAFKA_BOOTSTRAP" --topic "$topic" --time -2 2>/dev/null | while IFS= read -r line; do
            echo "  $line"
        done
        echo ""
        echo -e "${BOLD}Latest:${NC}"
        "$get_offsets_bin" --bootstrap-server "$KAFKA_BOOTSTRAP" --topic "$topic" --time -1 2>/dev/null | while IFS= read -r line; do
            echo "  $line"
        done
    else
        # Fallback: use kafka-run-class
        local run_class_bin
        if run_class_bin="$(_find_kafka_bin "kafka-run-class.sh" 2>/dev/null)"; then
            echo -e "${BOLD}Earliest offsets:${NC}"
            "$run_class_bin" kafka.tools.GetOffsetShell --broker-list "$KAFKA_BOOTSTRAP" --topic "$topic" --time -2 2>/dev/null || echo "  (unable to retrieve)"
            echo ""
            echo -e "${BOLD}Latest offsets:${NC}"
            "$run_class_bin" kafka.tools.GetOffsetShell --broker-list "$KAFKA_BOOTSTRAP" --topic "$topic" --time -1 2>/dev/null || echo "  (unable to retrieve)"
        else
            _warn "Neither kafka-get-offsets.sh nor kafka-run-class.sh found"
            echo "  Showing topic description instead:"
            _kafka_topics --describe --topic "$topic" 2>/dev/null
        fi
    fi

    _log "OFFSETS: topic=$topic"
}

cmd_help() {
    cat <<EOF

${BOLD}Kafka CLI Helper${NC}
${BRAND}

${BOLD}Usage:${NC} $SCRIPT_NAME <command> [arguments...]

${BOLD}Connection:${NC}
  Set environment variables to configure connection:
    KAFKA_BOOTSTRAP    Bootstrap servers (default: localhost:9092)
    KAFKA_ZOOKEEPER    Zookeeper address (default: localhost:2181)
    KAFKA_HOME         Kafka installation directory
    KAFKA_CONFIG_FILE  Client config file (for SASL/SSL auth)

${BOLD}Commands:${NC}
  topics                           List all topics with partition counts
  create-topic <name> [p] [r]     Create topic (partitions, replication factor)
  describe <topic>                 Detailed topic description
  produce <topic> <msg> [key]     Produce a message (optional key)
  consume <topic> [count] [from]  Consume messages (default: 10, from-beginning)
  groups                           List all consumer groups
  lag <group>                      Show consumer group lag
  config                           Show connection config and available tools
  status                           Cluster health and status check
  delete-topic <topic>            Delete a topic (with confirmation)
  partitions <topic> <count>      Increase topic partitions
  offsets <topic>                  Show earliest/latest offsets
  help                             Show this help message

${BOLD}Requirements:${NC}
  Kafka CLI tools must be installed. Set KAFKA_HOME or ensure tools are in PATH.

${BOLD}Examples:${NC}
  $SCRIPT_NAME topics
  $SCRIPT_NAME create-topic my-events 6 3
  $SCRIPT_NAME produce my-events "hello world"
  $SCRIPT_NAME consume my-events 5
  $SCRIPT_NAME lag my-consumer-group
  KAFKA_BOOTSTRAP=broker1:9092 $SCRIPT_NAME status

EOF
}

###############################################################################
# Main dispatcher
###############################################################################

main() {
    _init

    local cmd="${1:-help}"
    shift 2>/dev/null || true

    case "$cmd" in
        topics)          _check_kafka_tools; cmd_topics "$@" ;;
        create-topic)    _check_kafka_tools; cmd_create_topic "$@" ;;
        describe)        _check_kafka_tools; cmd_describe "$@" ;;
        produce)         _check_kafka_tools; cmd_produce "$@" ;;
        consume)         _check_kafka_tools; cmd_consume "$@" ;;
        groups)          _check_kafka_tools; cmd_groups "$@" ;;
        lag)             _check_kafka_tools; cmd_lag "$@" ;;
        config)          cmd_config "$@" ;;
        status)          _check_kafka_tools; cmd_status "$@" ;;
        delete-topic)    _check_kafka_tools; cmd_delete_topic "$@" ;;
        partitions)      _check_kafka_tools; cmd_partitions "$@" ;;
        offsets)         _check_kafka_tools; cmd_offsets "$@" ;;
        help|--help|-h)  cmd_help ;;
        *)
            _error "Unknown command: $cmd"
            echo "Run '$SCRIPT_NAME help' for usage."
            exit 1
            ;;
    esac
}

main "$@"
