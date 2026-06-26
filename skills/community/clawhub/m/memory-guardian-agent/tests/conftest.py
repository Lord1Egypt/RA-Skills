"""Pytest conftest — add scripts/ and subpackages to sys.path."""

import os
import sys

# Add the project root so we can import scripts/* and mg_* subpackages
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")

for p in (ROOT, SCRIPTS):
    if p not in sys.path:
        sys.path.insert(0, p)
