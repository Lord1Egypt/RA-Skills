#!/bin/bash
# Check M-flow Memory status
CONTAINER_NAME="mflow-memory"

if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${CONTAINER_NAME}$"; then
    PORT=$(docker port "$CONTAINER_NAME" 8000 2>/dev/null | head -1 | cut -d: -f2)
    HEALTH=$(curl -sf "http://localhost:$PORT/health" 2>/dev/null || echo "unreachable")
    echo "M-flow Memory: RUNNING (port $PORT)"
    echo "Health: $HEALTH"
    echo "Logs:   docker logs $CONTAINER_NAME --tail 10"
elif docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q "^${CONTAINER_NAME}$"; then
    echo "M-flow Memory: STOPPED"
    echo "Start:  docker start $CONTAINER_NAME"
else
    echo "M-flow Memory: NOT INSTALLED"
    echo "Setup:  bash scripts/setup.sh"
fi
