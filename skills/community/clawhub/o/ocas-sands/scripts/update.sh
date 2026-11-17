#!/bin/bash
cd "$(dirname "$0")/.."
git reset --hard HEAD 2>/dev/null
git clean -fd 2>/dev/null
git pull 2>/dev/null
