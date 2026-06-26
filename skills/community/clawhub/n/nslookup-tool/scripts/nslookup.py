#!/usr/bin/env python3
import socket, sys
if len(sys.argv) < 2: print("Usage: nslookup.py <host>"); sys.exit(1)
print(socket.gethostbyname(sys.argv[1]))
