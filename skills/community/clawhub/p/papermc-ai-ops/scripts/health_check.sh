#!/bin/bash
# PaperMC Health Check Script
# Monitors server health across multiple dimensions

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration - Update these paths
SERVER_DIR="/path/to/your/papermc-server"  # CHANGE THIS
LOG_DIR="${SERVER_DIR}/logs"
BACKUP_DIR="${SERVER_DIR}/backup"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================"
echo "PaperMC Health Check - ${TIMESTAMP}"
echo "========================================"
echo ""

cd "${SERVER_DIR}" || exit 1

# Check 1: Service Status
echo "[1/6] Checking service status..."
# Replace with your service check command
if systemctl is-active --quiet paper-mc.service 2>/dev/null; then
    echo -e "${GREEN}✓ Service is running${NC}"
    SERVICE_STATUS="OK"
else
    echo -e "${RED}✗ Service is NOT running${NC}"
    SERVICE_STATUS="FAIL"
fi
echo ""

# Check 2: Recent Logs
echo "[2/6] Checking recent logs..."
# Adjust log checking method as needed
ERROR_COUNT=0
if [ -f "${LOG_DIR}/latest.log" ]; then
    ERROR_COUNT=$(grep -i "error\|exception\|severe" "${LOG_DIR}/latest.log" | tail -50 | wc -l)
fi

if [ "${ERROR_COUNT}" -eq 0 ]; then
    echo -e "${GREEN}✓ No recent errors${NC}"
    LOG_STATUS="OK"
else
    echo -e "${YELLOW}⚠ Found ${ERROR_COUNT} error(s)${NC}"
    LOG_STATUS="WARN"
fi
echo ""

# Check 3: Plugin Count
echo "[3/6] Checking plugins..."
PLUGIN_COUNT=0
if [ -d "${SERVER_DIR}/plugins" ]; then
    PLUGIN_COUNT=$(ls -1 "${SERVER_DIR}/plugins"/*.jar 2>/dev/null | wc -l)
fi
echo -e "${GREEN}✓ ${PLUGIN_COUNT} plugins found${NC}"
PLUGIN_STATUS="OK"
echo ""

# Check 4: Backup Status
echo "[4/6] Checking backups..."
if [ -d "${BACKUP_DIR}" ] && [ "$(ls -A ${BACKUP_DIR}/*.tar.gz 2>/dev/null)" ]; then
    LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/*.tar.gz 2>/dev/null | head -1)
    BACKUP_TIME=$(stat -c %Y "${LATEST_BACKUP}" 2>/dev/null || echo "0")
    CURRENT_TIME=$(date +%s)
    AGE_HOURS=$(( (CURRENT_TIME - BACKUP_TIME) / 3600 ))
    
    if [ "${AGE_HOURS}" -lt 24 ]; then
        echo -e "${GREEN}✓ Latest backup: ${AGE_HOURS}h ago${NC}"
        BACKUP_STATUS="OK"
    else
        echo -e "${YELLOW}⚠ Backup is ${AGE_HOURS}h old${NC}"
        BACKUP_STATUS="WARN"
    fi
else
    echo -e "${RED}✗ No backups found${NC}"
    BACKUP_STATUS="FAIL"
fi
echo ""

# Check 5: Disk Space
echo "[5/6] Checking disk space..."
DISK_USAGE=$(df -h "${SERVER_DIR}" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "${DISK_USAGE}" -lt 80 ]; then
    echo -e "${GREEN}✓ Disk usage: ${DISK_USAGE}%${NC}"
    DISK_STATUS="OK"
else
    echo -e "${YELLOW}⚠ Disk usage high: ${DISK_USAGE}%${NC}"
    DISK_STATUS="WARN"
fi
echo ""

# Check 6: Memory
echo "[6/6] Checking memory..."
if pgrep -f "papermc.jar" > /dev/null; then
    echo -e "${GREEN}✓ Java process running${NC}"
    MEM_STATUS="OK"
else
    echo -e "${RED}✗ Java process not found${NC}"
    MEM_STATUS="FAIL"
fi
echo ""

# Summary
echo "========================================"
echo "Health Check Summary"
echo "========================================"
echo "Service:  ${SERVICE_STATUS}"
echo "Logs:     ${LOG_STATUS}"
echo "Plugins:  ${PLUGIN_STATUS}"
echo "Backups:  ${BACKUP_STATUS}"
echo "Disk:     ${DISK_STATUS}"
echo "Memory:   ${MEM_STATUS}"
echo ""

if [ "${SERVICE_STATUS}" = "OK" ] && [ "${BACKUP_STATUS}" != "FAIL" ]; then
    echo -e "${GREEN}Overall: HEALTHY${NC}"
    exit 0
else
    echo -e "${RED}Overall: ISSUES DETECTED${NC}"
    exit 1
fi
