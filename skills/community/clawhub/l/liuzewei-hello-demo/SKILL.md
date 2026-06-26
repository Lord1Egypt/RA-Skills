# Hello Demo Skill

A simple greeting skill for OpenClaw that provides friendly greetings with time awareness.

## Installation

```bash
skillhub install hello-demo
```

Or install from file:
```bash
skillhub install --file hello-demo.skill
```

## Usage

### Basic greeting
```bash
python3 scripts/greet.py [name]
```

### With options
```bash
python3 scripts/greet.py Alice --time --emoji
```

## Features

- 👋 Friendly greetings
- 🕐 Time-aware (morning/afternoon/evening)
- 😊 Emoji support
- 🌍 Multi-language ready

## Examples

```bash
$ python3 scripts/greet.py
Hello, World!

$ python3 scripts/greet.py Alice --time
Good afternoon, Alice!

$ python3 scripts/greet.py Bob --emoji
Hello, Bob! 👋
```

## Author

Created by liuzewei1990 as a demo for OpenClaw skill development.
