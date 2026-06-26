---
name: hello_world
description: Use when the user asks for a hello, a greeting, says hi, or wants to test that the hello-world plugin is loaded.
---

# Hello World

A minimal demo skill paired with the `hello-world` OpenClaw plugin.

## When to use

Trigger when the user asks for a greeting, says "hello", "hi", "say hi to <name>", or asks to test the hello-world plugin.

## How to use

Call the `hello` tool registered by the `hello-world` plugin:

- If the user mentions a name, pass it as the `name` parameter.
- Otherwise omit `name` and let the tool default to "world".
- Return the tool's text output directly without rephrasing.
