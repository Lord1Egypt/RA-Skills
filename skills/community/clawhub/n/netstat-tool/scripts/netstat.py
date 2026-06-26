#!/usr/bin/env python3
"""Netstat Tool - Network stats."""
import subprocess
subprocess.run(['netstat', '-tuln'])
