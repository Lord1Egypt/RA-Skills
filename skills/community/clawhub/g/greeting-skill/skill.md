---
name: greeting-skill
emoji: 👋
description: A friendly greeting skill that provides personalized and time-based greetings
version: 1.0.0
author: orlyjamie
tags:
  - utility
  - social
triggers:
  - greet
  - hello
  - hi
  - good morning
  - good afternoon
  - good evening
metadata:
  openclaw:
    requires:
      kind: node
      package: typescript
---

# Greeting Skill

A simple skill that provides friendly personalized greetings. Supports both random generic greetings and time-based contextual greetings.

## Tools

### greet
Generates a random friendly greeting for a user

**Parameters:**
- `name` (string, required): The name of the person to greet

**Returns:** A random greeting string

**Example:**
> User: greet Alice
> Agent: Hello, Alice! Hope you're having a great day! 👋

### getTimeBasedGreeting
Generates a greeting appropriate for the current time of day

**Parameters:**
- `name` (string, required): The name of the person to greet

**Returns:** A time-appropriate greeting (morning/afternoon/evening)

**Example:**
> User: greet Bob (at 10 AM)
> Agent: Good morning, Bob!
