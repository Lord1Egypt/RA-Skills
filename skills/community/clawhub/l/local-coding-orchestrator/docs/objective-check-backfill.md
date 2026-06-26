# Objective check backfill

This document defines the next hardening step for automatic objective check updates.

## Goal

Use worker summaries and result artifacts to backfill some objective checks automatically.

## First useful signals

- if summary mentions read-only sandbox or missing repo, do not mark checks passed; prefer blocked interpretation
- if summary explicitly says build passed, set `build = passed`
- if summary explicitly says tests passed, set `tests = passed`
- if summary explicitly says review completed or review artifact exists, set `review = passed`
- if summary explicitly says a check remains pending, keep it pending

## Caution

Do not infer success from silence.
Only mark checks passed when the worker or artifact provides direct evidence.
