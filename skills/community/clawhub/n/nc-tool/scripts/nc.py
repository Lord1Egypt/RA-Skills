#!/usr/bin/env python3
"""Nc Tool - Netcat-like."""
import socket, sys
if len(sys.argv) != 3:
    print("Usage: nc.py <host> <port>")
    sys.exit(1)
try:
    s = socket.socket()
    s.connect((sys.argv[1], int(sys.argv[2])))
    print(f"Connected to {sys.argv[1]}:{sys.argv[2]}")
    s.close()
except Exception as e: print(f"Error: {e}")
