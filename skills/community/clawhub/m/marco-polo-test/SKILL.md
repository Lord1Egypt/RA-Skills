---
name: marco-polo-test
description: A simple zero‑dependency, environment‑agnostic, and side‑effect‑free skill that helps users test if their OpenClaw instances can load skills correctly.
---

# Marco Polo Test Skill

## Purpose

This skill provides a minimal but verifiable interaction pattern to confirm that OpenClaw correctly loads and invokes skills. It is designed to be completely safe, stateless, and free of external dependencies.

## Core Behavior

When a user's message contains the word **"marco"** (case‑insensitive, as a standalone word or part of a sentence), the skill responds with **polo**


## Usage Examples

| User input | Skill response |
|------------|----------------|
| `marco` | `polo` |
| `Marco!` | `polo` |
| `Hello, marco!` | `Hello! 👋 How can I help you today? polo` |

## Testing Workflow

1. **Load the skill** – Place this `SKILL.md` in the appropriate OpenClaw skills directory.
2. **Start an OpenClaw instance** – Ensure skills are enabled.
3. **Send a message containing "marco"** – For example, type `marco` or `Hey, marco!`.
4. **Verify the response** – The instance should reply with something including `polo`.

If the instance does not respond with `polo`, the skill is not being loaded or triggered correctly.