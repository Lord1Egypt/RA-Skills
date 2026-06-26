#!/bin/bash
# Restart MuseStream server on port 5001 (default)

pkill -f musestream_server.py 2>/dev/null && echo "Stopped existing server" || echo "No server running"
sleep 1

cd "$(dirname "$0")"
nohup python3 musestream_server.py > /tmp/musestream.log 2>&1 &
echo "Started musestream_server.py (PID $!)"
echo "Logs: tail -f /tmp/musestream.log"
