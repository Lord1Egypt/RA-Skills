#!/usr/bin/env python3
import json, subprocess, sys
r = subprocess.run(["docker","ps","--format","{{.Names}}"], capture_output=True, text=True)
print(json.dumps({"containers": r.stdout.strip().split("\n") if r.stdout.strip() else []}))
