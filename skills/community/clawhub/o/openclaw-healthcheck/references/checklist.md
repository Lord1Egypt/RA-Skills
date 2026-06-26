# OpenClaw Healthcheck Checklist

## Core categories
1. Runtime health
2. Network exposure
3. Config hygiene
4. Browser surface / session attach risk
5. Recent error signals
6. Update / version hygiene

## High-risk findings
- gateway not running when expected
- unexpected public listeners
- weak or missing auth-related settings
- browser attach / relay exposed without clear user intent
- repeated recent runtime failures
- stale deployment with known operator issues

## Example recommendation patterns
- restrict listen address / exposure
- rotate high-privilege keys after accidental disclosure
- enable narrower auth / safer attach path
- add recovery / backup verification
- review cron jobs with exact owners and receipts
