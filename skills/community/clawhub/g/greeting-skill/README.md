# Greeting Skill for Clawd Bot

A simple, friendly greeting skill that provides personalized greetings for users of the Clawd personal AI assistant.

## Features

- Random generic greetings
- Time-based contextual greetings (morning/afternoon/evening)
- Fully compatible with OpenClaw skill specification

## Installation

```bash
npx clawhub install greeting-skill
```

## Usage

The skill responds to natural language triggers like "greet", "hello", "hi", "good morning", etc. You can also call the tools directly:

### Random greeting
```
greet [name]
```

### Time-based greeting
```
time-greet [name]
```

## Development

### Prerequisites
- Node.js 18+
- TypeScript 5+
- @openclaw/core

### Build
```bash
npm run build
```

### Watch mode
```bash
npm run dev
```

### Type check
```bash
npm run typecheck
```

### Test
```bash
npm test
```

## License

MIT
