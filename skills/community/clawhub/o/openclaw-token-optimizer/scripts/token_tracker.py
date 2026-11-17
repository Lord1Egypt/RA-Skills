#!/usr/bin/env python3
"""v4 migration shim: legacy behavior removed; explicit v4 arguments required."""
import sys
from optimizer import main
if __name__ == '__main__':
    sys.argv.insert(1, 'budget')
    sys.exit(main())
