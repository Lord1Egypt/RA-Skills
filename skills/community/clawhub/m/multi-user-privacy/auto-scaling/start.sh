#!/bin/bash

# Session Auto-Scaler Management Script
# Usage: ./start.sh [start|stop|status|restart|log]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "$1" in
  start)
    echo "Starting Session Auto-Scaler..."
    node start-autoscaler.js start
    ;;
  stop)
    echo "Stopping Session Auto-Scaler..."
    node start-autoscaler.js stop
    ;;
  status)
    node start-autoscaler.js status
    ;;
  restart)
    echo "Restarting Session Auto-Scaler..."
    node start-autoscaler.js restart
    ;;
  log)
    echo "Tailing logs (Ctrl+C to stop)..."
    tail -f logs/autoscaler.log
    ;;
  demo)
    echo "Running demo..."
    node demo-autoscaler.js
    ;;
  *)
    echo "Usage: $0 {start|stop|status|restart|log|demo}"
    echo ""
    echo "Commands:"
    echo "  start   - Start the auto-scaler service"
    echo "  stop    - Stop the auto-scaler service"
    echo "  status  - Show service status"
    echo "  restart - Restart the service"
    echo "  log     - View live logs"
    echo "  demo    - Run demo script"
    exit 1
    ;;
esac
