# Breach checks

Use breach checks only in a defensive context.

## Purpose
Check whether an email address appears in known public breach datasets.

## Recommended provider
Use Have I Been Pwned (HIBP) with an API key.

## What to return
If a breach check is enabled and an email is provided, return:
- whether breaches were found
- breach names
- breach dates when available
- exposed data classes when available

## Safety rule
Treat breach checks as defensive exposure checking, not harassment tooling.
Do not frame the result as permission to target the person.
