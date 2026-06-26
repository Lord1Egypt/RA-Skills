#!/bin/bash
# glm-swarm cleanup: 완료된 swarm 작업 디렉토리 정리
# Usage: cleanup.sh <task-id>   — 특정 task 정리
#        cleanup.sh --all       — 1시간 이상 된 전부 정리
#        cleanup.sh --list      — 현재 swarm 디렉토리 목록

set -e

SWARM_BASE="/tmp/swarm"

case "${1}" in
  --all)
    if [ -d "${SWARM_BASE}" ]; then
      find "${SWARM_BASE}" -maxdepth 1 -mindepth 1 -type d -mmin +60 -exec rm -rf {} +
      echo "Cleaned swarm dirs older than 1 hour"
    fi
    ;;
  --list)
    if [ -d "${SWARM_BASE}" ]; then
      ls -lt "${SWARM_BASE}/" 2>/dev/null || echo "No swarm dirs"
    else
      echo "No swarm dirs"
    fi
    ;;
  "")
    echo "Usage: cleanup.sh <task-id> | --all | --list"
    exit 1
    ;;
  *)
    TASK_DIR="${SWARM_BASE}/${1}"
    if [ -d "${TASK_DIR}" ]; then
      rm -rf "${TASK_DIR}"
      echo "Cleaned ${TASK_DIR}"
    else
      echo "Not found: ${TASK_DIR}"
      exit 1
    fi
    ;;
esac
