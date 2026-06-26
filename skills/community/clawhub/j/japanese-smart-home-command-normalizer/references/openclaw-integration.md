# OpenClaw integration notes

## audio-router

A thin integration path is:

1. normalize transcript with `normalizeText()`
2. classify with `classify()`
3. if `intent` exists and `needsConfirmation` is false, run the fastpath
4. otherwise defer to the main agent or ask for confirmation

## Why keep it thin

The hook should not own a giant Japanese regex table forever.
The normalizer skill should own domain vocabulary and confidence logic.
The hook should mostly route, execute, and record state.

## Current practical split

- this skill: transcript normalization, slot extraction, confidence
- device-control skill: actual API execution
- hook: glue layer and runtime messaging
