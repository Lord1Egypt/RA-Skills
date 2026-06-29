# PIC Residual Guard

PIC Residual Guard is an OpenClaw skill for review-first action checks.

Generated agent output is a candidate, not verified work.

## What it does

Before external-effect actions, this skill asks the agent to create an action proposal, list evidence, list missing evidence, record a rollback path, classify risk, and avoid treating proposed work as verified work.

External-effect actions include shell commands, file writes, network requests, email or message sending, calendar edits, package installs, skill installs, repository mutations, persistent memory writes, credential handling, browser automation, payments, purchases, and irreversible transactions.

## Safety boundary

This skill does not execute proposed actions.
This skill does not run commands from action proposals.
This skill does not clone or install PIC automatically.
This skill does not prove correctness, real ASI, external-world truth, or action safety.
This skill does not replace OpenClaw sandboxing, approvals, allowlists, or tool policy.

## Optional PIC integration

PIC-backed mode is optional and user-configured in the full GitHub repository.
The ClawHub skill itself is safe to use in skill-only advisory mode.

Repository:
https://github.com/kadubon/pic-openclaw-skill
