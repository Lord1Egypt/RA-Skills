#!/bin/bash
# leio-sdlc standard pre-commit hook
# Part of PRD-1012: Enforce SDLC via Git Pre-Commit Hook

if [ "$SDLC_ORCHESTRATOR_RUNNING" != "1" ]; then
    echo "ERROR: SDLC Violation! Direct commits are forbidden. You must use orchestrator.py."
    exit 1
fi

exit 0
