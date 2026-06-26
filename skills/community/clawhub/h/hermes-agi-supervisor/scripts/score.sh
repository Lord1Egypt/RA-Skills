#!/bin/bash
# hermes-agi-supervisor: 积分计算脚本
# 用法: ./score.sh <task_id> <completed_count> <failed_count>

TASK_ID="$1"
COMPLETED="$2"
FAILED="$3"

SCORE=$((COMPLETED * 10 - FAILED * 5))

if [ $COMPLETED -ge 3 ] && [ $FAILED -eq 0 ]; then
  STATUS="excellent"
  BONUS=20
elif [ $COMPLETED -ge 2 ] && [ $FAILED -le 1 ]; then
  STATUS="good"
  BONUS=10
elif [ $COMPLETED -ge 1 ]; then
  STATUS="partial"
  BONUS=0
else
  STATUS="failed"
  BONUS=0
fi

TOTAL=$((SCORE + BONUS))

echo "{\"task_id\": \"$TASK_ID\", \"base_score\": $SCORE, \"bonus\": $BONUS, \"total\": $TOTAL, \"status\": \"$STATUS\"}"
