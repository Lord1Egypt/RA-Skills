#!/bin/bash
# Docker container stats with formatted output

echo "Container Stats"
echo "==============="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
