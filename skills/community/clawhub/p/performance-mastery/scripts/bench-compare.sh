#!/bin/bash
# bench-compare.sh — 基准测试对比工具
# 运行两组基准并对比差异
#
# 用法:
#   bash bench-compare.sh --help
#   bash bench-compare.sh --baseline "sleep 0.1" --candidate "sleep 0.05" --runs 10
#   bash bench-compare.sh --go-bench ./...
#   bash bench-compare.sh --command "curl -s http://localhost:8080" --runs 50

set -euo pipefail

RUNS=10
MODE=""
BASELINE_CMD=""
CANDIDATE_CMD=""
GO_PKG=""
NON_INTERACTIVE=false

usage() {
    cat <<EOF
bench-compare.sh — 基准测试对比工具

用法:
  1) 对比两个命令:
     bash bench-compare.sh --baseline "CMD_A" --candidate "CMD_B" --runs N

  2) Go 基准测试对比 (需要 benchstat):
     bash bench-compare.sh --go-bench ./... --runs N

  3) 单命令多次运行统计:
     bash bench-compare.sh --command "CMD" --runs N

选项:
  --baseline CMD   基线命令
  --candidate CMD  对比命令
  --command CMD    单命令模式
  --go-bench PKG   Go 基准测试包路径
  --runs N         运行次数 (默认 10)
  --non-interactive  非交互模式，跳过所有确认提示（适用于 CI/CD）
  --help           显示帮助
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --baseline)   BASELINE_CMD="$2"; MODE="compare"; shift 2 ;;
        --candidate)  CANDIDATE_CMD="$2"; shift 2 ;;
        --command)    BASELINE_CMD="$2"; MODE="single"; shift 2 ;;
        --go-bench)   GO_PKG="$2"; MODE="go"; shift 2 ;;
        --runs)       RUNS="$2"; shift 2 ;;
        --non-interactive) NON_INTERACTIVE=true; shift ;;
        --help|-h)    usage ;;
        *)            echo "未知参数: $1"; usage ;;
    esac
done

# --- 参数校验 ---
if [ "$MODE" = "compare" ] && [ -z "$CANDIDATE_CMD" ]; then
    echo "错误: --baseline 必须配合 --candidate 使用" >&2
    exit 1
fi
if ! [[ "$RUNS" =~ ^[0-9]+$ ]] || [ "$RUNS" -lt 1 ]; then
    echo "错误: --runs 必须是正整数" >&2
    exit 1
fi

confirm_commands() {
    echo "即将执行的命令:" >&2
    for arg in "$@"; do
        echo "  $arg" >&2
    done
    echo "" >&2
    # 非交互模式（管道/重定向）跳过确认
    if [ "$NON_INTERACTIVE" = true ]; then
        echo "(非交互模式，跳过确认)" >&2
    elif [ -t 0 ]; then
        echo "按 Enter 继续，Ctrl+C 取消..." >&2
        read -r
    fi
}

run_timed() {
    local cmd="$1"
    local n="$2"
    local label="$3"
    local times=()

    echo "运行 $label ($n 次)..." >&2
    for i in $(seq 1 "$n"); do
        start=$(date +%s%N)
        bash -c "$cmd" > /dev/null 2>&1
        end=$(date +%s%N)
        elapsed=$(( (end - start) / 1000000 ))  # ms
        times+=("$elapsed")
        printf "\r  进度: %d/%d" "$i" "$n" >&2
    done
    echo "" >&2

    # 计算统计
    IFS=$'\n' sorted=($(sort -n <<<"${times[*]}")); unset IFS
    total=0
    for t in "${times[@]}"; do total=$((total + t)); done
    avg=$((total / n))
    min="${sorted[0]}"
    max="${sorted[$((n-1))]}"
    p50_idx=$(( n / 2 ))
    p99_idx=$(( n * 99 / 100 ))
    p50="${sorted[$p50_idx]}"
    p99="${sorted[$p99_idx]}"

    # 小样本量时 p99 没有统计意义，添加提示
    local p99_display
    if [ "$n" -lt 100 ]; then
        p99_display="${p99}ms*"
    else
        p99_display="${p99}ms"
    fi

    printf "  %-12s avg=%dms  min=%dms  p50=%dms  p99=%s  max=%dms\n" \
        "$label:" "$avg" "$min" "$p50" "$p99_display" "$max" >&2
    if [ "$n" -lt 100 ]; then
        echo "  (* p99 样本量不足 100，仅供参考)" >&2
    fi
    echo "$avg"
}

case "$MODE" in
    compare)
        echo "=========================================="
        echo " 基准对比 ($RUNS 次运行)"
        echo "=========================================="
        confirm_commands "Baseline:  $BASELINE_CMD" "Candidate: $CANDIDATE_CMD"
        avg_a=$(run_timed "$BASELINE_CMD" "$RUNS" "Baseline")
        avg_b=$(run_timed "$CANDIDATE_CMD" "$RUNS" "Candidate")
        echo ""
        if [ "$avg_a" -gt "$avg_b" ] && [ "$avg_a" -gt 0 ]; then
            speedup=$(echo "scale=2; $avg_a / $avg_b" | bc 2>/dev/null || echo "N/A")
            echo "结果: Candidate 快 ${speedup}x"
        elif [ "$avg_b" -gt "$avg_a" ] && [ "$avg_b" -gt 0 ]; then
            slowdown=$(echo "scale=2; $avg_b / $avg_a" | bc 2>/dev/null || echo "N/A")
            echo "结果: Candidate 慢 ${slowdown}x"
        else
            echo "结果: 无明显差异"
        fi
        ;;
    single)
        echo "=========================================="
        echo " 单命令基准 ($RUNS 次运行)"
        echo "=========================================="
        confirm_commands "Command: $BASELINE_CMD"
        run_timed "$BASELINE_CMD" "$RUNS" "Command"
        ;;
    go)
        if ! command -v benchstat &>/dev/null; then
            echo "安装 benchstat: go install golang.org/x/perf/cmd/benchstat@latest"
            exit 1
        fi
        echo "=========================================="
        echo " Go 基准测试对比"
        echo "=========================================="
        echo "步骤 1: 运行基线基准..."
        go test -bench=. -benchmem -count="$RUNS" "$GO_PKG" > "${TMPDIR:-/tmp}/bench-old.txt" 2>&1
        echo "保存到 ${TMPDIR:-/tmp}/bench-old.txt"
        echo ""
        echo "现在请做你的优化，然后按 Enter 运行对比基准..."
        if [ "$NON_INTERACTIVE" = true ]; then
            echo "(非交互模式，直接继续)" >&2
        else
            read -r
        fi
        echo "步骤 2: 运行对比基准..."
        go test -bench=. -benchmem -count="$RUNS" "$GO_PKG" > "${TMPDIR:-/tmp}/bench-new.txt" 2>&1
        echo ""
        echo "步骤 3: benchstat 对比结果:"
        echo "=========================================="
        benchstat "${TMPDIR:-/tmp}/bench-old.txt" "${TMPDIR:-/tmp}/bench-new.txt"
        ;;
    *)
        echo "请指定模式。运行 --help 查看用法。"
        exit 1
        ;;
esac
