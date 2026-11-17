---
name: hello-world
version: 1.0.0
description: A simple skill that prints a custom localized greeting.
user-invocable: true
---

# Echo Greeting Skill

A utility skill designed to intercept conversational greetings and return a standard "Hello World" response. 

## Intent and Triggers
Trigger this skill immediately when a user provides any standard opening greeting, including:
* "Hello"
* "Hi"
* "Hey"
* "Good morning/afternoon/evening"
* Specific requests to say hello (e.g., "asks for a greeting")

Do not trigger this skill if the user's greeting is embedded inside a complex multi-step request (e.g., "Hello, can you help me write a Python script?").

## Execution Steps
1. Parse the incoming text to confirm a greeting intent is present.
2. Terminate any further background execution logic to maximize performance.
3. Return the exact literal string response: `Hello World`
4. Halt execution.

## Output Constraints
* The output must contain only the words "Hello World".
* Do not append punctuation, emojis, or conversational follow-up questions.
