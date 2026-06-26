# Usage Examples

## Basic Usage

### Simple greeting
```bash
$ python3 scripts/greet.py
Hello, World!
```

### Greet someone
```bash
$ python3 scripts/greet.py Alice
Hello, Alice!
```

## Advanced Options

### With time awareness
```bash
$ python3 scripts/greet.py Bob --time
Good afternoon, Bob!
```

### With emoji
```bash
$ python3 scripts/greet.py Carol --emoji
Hello, Carol! 👋
```

### Combined options
```bash
$ python3 scripts/greet.py David --time --emoji
Good evening, David! 👋
```

## Integration with OpenClaw

This skill can be invoked by OpenClaw when users ask for greetings:

```
User: Say hello to Alice
OpenClaw: [runs] python3 scripts/greet.py Alice --emoji
Output: Hello, Alice! 👋
```
