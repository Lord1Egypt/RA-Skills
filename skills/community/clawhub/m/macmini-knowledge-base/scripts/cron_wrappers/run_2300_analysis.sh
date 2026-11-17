#!/bin/bash
# 23:00 知识库分析 —— 确定性执行 + 真实统计输出
#
# 背景：2026-11-03 / 11-04 连续两晚 cron status=ok，实际产出 200 份全是
#       「【分析失败】name 'clean_noise' is not defined」，而 payload 只输出
#       「run_analysis完成」→ 面板绿灯骗人，没人察觉。
# 本脚本跑完后解析 run_analysis.py 输出的 [STATS] 行，输出真实成功/失败/队列数；
# 连续多轮成功数为 0 时升级告警措辞；脚本崩溃时明确报异常，绝不伪装成功。
#
# 退出码约定（与「面板状态 = 真实健康度」对齐）：
#   0  本轮有产出（可能有部分文件失败，已留在重试队列）
#   1  脚本崩溃 / 无统计行 / 本轮成功数为 0
#
# 自测：PARSE_ONLY=<输出文件> 时只解析不执行
set -uo pipefail

WS=/Users/home/.openclaw/workspace
SCRIPT="$WS/knowledge/.analysis/run_analysis.py"
STATE="${ZERO_STATE:-$WS/knowledge/.analysis/.zero_run_counter}"
CORPUS_STATE="${CORPUS_STATE:-$WS/knowledge/.analysis/.corpus_count}"

if [[ -n "${PARSE_ONLY:-}" ]]; then
    OUT="$(cat "$PARSE_ONLY" 2>/dev/null)"; rc=0
else
    OUT="$(python3 "$SCRIPT" 2>&1)"; rc=$?
fi

STATS="$(printf '%s\n' "$OUT" | grep -E '^\[STATS\]' | tail -1)"
SUCCESS="$(printf '%s' "$STATS" | sed -n 's/.*success=\([0-9]*\).*/\1/p')"
FAILURE="$(printf '%s' "$STATS" | sed -n 's/.*failure=\([0-9]*\).*/\1/p')"
QUEUE="$(printf '%s' "$STATS" | sed -n 's/.*queue=\([0-9]*\).*/\1/p')"

if [[ -z "$STATS" ]]; then
    printf '🔴 知识库分析异常：脚本未产出 [STATS] 统计行（exit=%s）\n' "$rc"
    printf -- '--- 末尾输出 ---\n'
    printf '%s\n' "$OUT" | tail -15
    exit 1
fi

[ -z "$SUCCESS" ] && SUCCESS=0
[ -z "$FAILURE" ] && FAILURE=0
[ -z "$QUEUE" ] && QUEUE=0

# ── 语料库规模哨兵（必须先算：idle 分支也要用它，且不得跳过）────────
# 2026-11-05 事故：knowledge/知识库/ 整个目录被移到 macOS 系统废纸篓，
#   869 个文件从分析流水线视野中消失，cron 仍报「ok」→ 绿灯骗人。
# 2026-11-06 修正：原先这段在 idle 分支之后 → 队列为空时整段被跳过，
#   而「队列为空」恰恰是最可能出现静默删目录的场景 → 防线反而失效。
CORPUS="$(find "$WS/knowledge" -type d -name '.analysis' -prune -o -type f -print 2>/dev/null | wc -l | tr -d ' ')"
case "$CORPUS" in ''|*[!0-9]*) CORPUS=0 ;; esac
PREV_CORPUS=0
if [ -f "$CORPUS_STATE" ]; then PREV_CORPUS="$(cat "$CORPUS_STATE" 2>/dev/null || echo 0)"; fi
case "$PREV_CORPUS" in ''|*[!0-9]*) PREV_CORPUS=0 ;; esac
THRESHOLD=0
if [ "$PREV_CORPUS" -gt 0 ]; then THRESHOLD=$((PREV_CORPUS * 80 / 100)); fi

corpus_drop_warning() {
    if [ "$THRESHOLD" -gt 0 ] && [ "$CORPUS" -lt "$THRESHOLD" ]; then
        printf '🔴 语料库规模骤降：%s → %s（下降 %s 份，超过 20%% 阈值）\n' \
               "$PREV_CORPUS" "$CORPUS" "$((PREV_CORPUS - CORPUS))"
        printf '   请立即检查 knowledge/ 目录是否被误删/移动（可用 .trash/ 或系统废纸篓恢复）\n'
    fi
    echo "$CORPUS" > "$CORPUS_STATE"
}

if [ "$SUCCESS" -eq 0 ]; then
    # ── 区分「队列空闲」与「流水线故障」────────────────────────
    # 2026-11-06 修正：原先 SUCCESS=0 一律记 streak + exit 1，
    #   导致「无新文档、队列已空」这种健康空闲态被误判为故障、面板变红。
    #   判据：队列为空 且 本轮无失败 → 空闲（正常）；否则才是故障。
    if [ "$QUEUE" -eq 0 ] && [ "$FAILURE" -eq 0 ]; then
        echo 0 > "$STATE"
        printf '✅ 知识库分析：无新文档待处理（队列已空，流水线空闲）｜语料 %s 份\n' "$CORPUS"
        corpus_drop_warning      # 空闲态也要执行规模哨兵（静默删目录恰在此刻发生）
        exit 0
    fi
    PREV=0
    if [ -f "$STATE" ]; then PREV="$(cat "$STATE" 2>/dev/null || echo 0)"; fi
    case "$PREV" in ''|*[!0-9]*) PREV=0 ;; esac
    STREAK=$((PREV + 1))
    echo "$STREAK" > "$STATE"
    printf '⚠️ 知识库分析：本轮成功 0 份（失败 %s）｜队列剩余 %s\n' "$FAILURE" "$QUEUE"
    if [ "$STREAK" -ge 2 ]; then
        printf '🔴 已连续 %s 轮产出为 0 —— 流水线很可能已断，请立即检查\n' "$STREAK"
    fi
    printf -- '--- 末尾输出 ---\n'
    printf '%s\n' "$OUT" | tail -15
    exit 1
fi

echo 0 > "$STATE"

printf '📊 知识库分析完成：成功 %s 份 / 失败 %s 份｜队列剩余 %s\n' "$SUCCESS" "$FAILURE" "$QUEUE"
if [ "$FAILURE" -gt 0 ]; then
    printf '⚠️ 有 %s 份提取失败（已留在重试队列，连续失败 3 次自动隔离）\n' "$FAILURE"
fi

corpus_drop_warning
exit 0
