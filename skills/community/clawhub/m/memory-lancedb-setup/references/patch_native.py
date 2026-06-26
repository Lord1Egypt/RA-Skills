#!/usr/bin/env python3
"""
Patch LanceDB native.js on Apple Silicon (arm64) macOS.

Problem: native.js tries darwin-x64 first, uses `break` after catch,
so arm64 is never reached even when the arm64 package is installed.

Fix: move `break` inside the try block so x64 failure falls through to arm64.
"""

import sys
from pathlib import Path

NATIVE_JS = Path("/usr/local/lib/node_modules/openclaw/extensions/memory-lancedb/node_modules/@lancedb/lancedb/dist/native.js")

OLD = """            case 'x64':
                localFileExisted = existsSync(join(__dirname, 'lancedb.darwin-x64.node'));
                try {
                    if (localFileExisted) {
                        nativeBinding = require('./lancedb.darwin-x64.node');
                    }
                    else {
                        nativeBinding = require('@lancedb/lancedb-darwin-x64');
                    }
                }
                catch (e) {
                    loadError = e;
                }
                break;"""

NEW = """            case 'x64':
                localFileExisted = existsSync(join(__dirname, 'lancedb.darwin-x64.node'));
                try {
                    if (localFileExisted) {
                        nativeBinding = require('./lancedb.darwin-x64.node');
                    }
                    else {
                        nativeBinding = require('@lancedb/lancedb-darwin-x64');
                    }
                    break;
                }
                catch (e) {
                    loadError = e;
                    // fall through to arm64"""

def main():
    if not NATIVE_JS.exists():
        print(f"ERROR: {NATIVE_JS} not found. Is memory-lancedb installed?")
        sys.exit(1)

    content = NATIVE_JS.read_text()

    if NEW.strip() in content:
        print("Already patched, nothing to do.")
        return

    if OLD not in content:
        print("ERROR: Expected snippet not found. LanceDB version may have changed.")
        print("Manual patch needed — check native.js and move `break` inside try block for x64 case.")
        sys.exit(1)

    patched = content.replace(OLD, NEW)
    NATIVE_JS.write_text(patched)
    print("Patched successfully. Run: openclaw gateway restart")

if __name__ == "__main__":
    main()
