#!/usr/bin/env bash
set -euo pipefail

echo '== OpenClaw SaaS Builder preflight =='

echo
echo '-- Gemini CLI --'
if [ -x ./skills/gemini-cli/scripts/check_gemini.sh ]; then
  ./skills/gemini-cli/scripts/check_gemini.sh || true
else
  echo 'gemini-cli helper not found'
fi

echo
echo '-- GitHub CLI --'
if command -v gh >/dev/null 2>&1; then
  gh auth status || true
else
  echo 'gh not found'
fi

echo
echo '-- Vercel CLI --'
if command -v vercel >/dev/null 2>&1; then
  vercel --version || true
  vercel whoami || true
else
  echo 'vercel not found'
fi
