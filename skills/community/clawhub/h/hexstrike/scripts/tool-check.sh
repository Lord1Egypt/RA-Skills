#!/usr/bin/env bash
# Check which security tools are available on this system
# Usage: bash tool-check.sh [category]
# Categories: all, network, web, crypto, pwn, forensics, rev, osint, cloud

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; NC='\033[0m'

check() {
  if command -v "$1" &>/dev/null; then
    printf "${GREEN}✓${NC} %-20s %s\n" "$1" "$(command -v "$1")"
    return 0
  else
    printf "${RED}✗${NC} %-20s not found\n" "$1"
    return 1
  fi
}

category="${1:-all}"
found=0; missing=0

check_tools() {
  local label="$1"; shift
  echo -e "\n${YELLOW}── $label ──${NC}"
  for tool in "$@"; do
    if check "$tool"; then ((found++)); else ((missing++)); fi
  done
}

if [[ "$category" == "all" || "$category" == "network" ]]; then
  check_tools "Network Scanning" nmap rustscan masscan autorecon
  check_tools "DNS & Subdomain" amass subfinder fierce dnsenum dnsrecon dig whois
  check_tools "SMB/Windows" enum4linux smbmap rpcclient nbtscan netexec evil-winrm
fi

if [[ "$category" == "all" || "$category" == "web" ]]; then
  check_tools "Web Discovery" gobuster feroxbuster ffuf dirsearch dirb
  check_tools "Web Scanning" nuclei nikto sqlmap dalfox wpscan wafw00f
  check_tools "Web Crawling" httpx katana whatweb
  check_tools "Parameters" arjun paramspider
fi

if [[ "$category" == "all" || "$category" == "crypto" ]]; then
  check_tools "Crypto/Cracking" hashcat john hash-identifier hashid openssl gpg
fi

if [[ "$category" == "all" || "$category" == "pwn" ]]; then
  check_tools "Binary Analysis" checksec file strings objdump readelf nm ldd ltrace strace
  check_tools "Exploitation" gdb radare2 ropper python3
fi

if [[ "$category" == "all" || "$category" == "forensics" ]]; then
  check_tools "Forensics" binwalk foremost exiftool steghide zsteg tshark tcpdump
  check_tools "Memory" volatility python3
fi

if [[ "$category" == "all" || "$category" == "rev" ]]; then
  check_tools "Reverse Engineering" ghidra r2 gdb objdump strings upx
fi

if [[ "$category" == "all" || "$category" == "osint" ]]; then
  check_tools "OSINT" sherlock theHarvester recon-ng shodan whois dig
fi

if [[ "$category" == "all" || "$category" == "cloud" ]]; then
  check_tools "Cloud Security" prowler trivy kube-hunter kube-bench checkov terrascan
  check_tools "SSL/TLS" testssl sslscan sslyze
fi

echo -e "\n${GREEN}Found: $found${NC} | ${RED}Missing: $missing${NC}"
