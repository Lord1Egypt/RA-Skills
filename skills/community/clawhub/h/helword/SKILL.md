---
name: helword
description: A simple hello world skill that demonstrates basic skill structure. When users ask for a greeting, it responds with a friendly hello message.
triggers:
  - pattern: "hello|hi|hey|greeting|say hi"
    description: "Detect greeting requests"
  - pattern: "who are you|about yourself|introduce"
    description: "Detect self-introduction requests"
auto_invoke: true
examples:
  - "Say hello"
  - "Hi there"
  - "Hello world"
  - "Who are you"
---

# Hello World Skill

A simple skill that demonstrates the basic structure of an OpenClaw skill. This skill responds with a friendly greeting when users ask for one.

## Usage

When the user asks for a greeting or introduces themselves, this skill will respond with a friendly message.

## Examples

- User: "Say hello" → Skill: "Hello from your custom skill!"
- User: "Hi there" → Skill: "Hello from your custom skill!"
- User: "Who are you" → Skill: "Hello from your custom skill!"
- User: "Hello world" → Skill: "Hello from your custom skill!"
- User: "Introduce yourself" → Skill: "Hello from your custom skill!"

## Implementation

This skill uses the built-in `echo` tool to output the greeting message.

## For Developers

This skill serves as a template for creating new skills. To create your own skill:

1. Create a new folder in your skills directory
2. Add a `SKILL.md` file with proper metadata
3. Implement your skill logic
4. Publish using `clawhub publish <path>`
