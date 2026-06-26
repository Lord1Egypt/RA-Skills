# Contributing to LobsterOps

Thank you for your interest in contributing to LobsterOps! This guide will help you get started.

## Development Setup

```bash
git clone https://github.com/noeldelisle/LobsterOps.git
cd LobsterOps
npm install
npm test
```

## Project Structure

```
LobsterOps/
├── SKILL.md                    # OpenClaw skill definition
├── index.js                    # Package entry point (exports)
├── src/
│   ├── core/
│   │   ├── LobsterOps.js      # Main observability class
│   │   ├── PIIFilter.js        # PII detection and redaction
│   │   ├── Exporter.js         # Export to JSON/CSV/Markdown
│   │   ├── DebugConsole.js     # Time-travel debug console
│   │   ├── Analytics.js        # Behavioral analytics
│   │   ├── AlertManager.js     # Alerting and anomaly detection
│   │   └── OpenClawInstrumentation.js  # OpenClaw integration hooks
│   └── storage/
│       ├── StorageAdapter.js   # Abstract base class
│       ├── StorageFactory.js   # Factory for storage backends
│       ├── JsonFileStorage.js  # JSON file backend
│       ├── MemoryStorage.js    # In-memory backend
│       ├── SQLiteStorage.js    # SQLite backend
│       └── SupabaseStorage.js  # Supabase cloud backend
└── tests/
    └── LobsterOps.test.js      # Test suite
```

## Running Tests

```bash
npm test              # Run full test suite
npm run test:watch    # Run tests in watch mode
```

## Adding a Storage Backend

1. Create a new class extending `StorageAdapter` in `src/storage/`
2. Implement all required methods: `init`, `saveEvent`, `queryEvents`, `getEventById`, `updateEvent`, `deleteEvents`, `cleanupOld`, `getStats`, `close`
3. Register it in `StorageFactory.js`
4. Export it from `index.js`
5. Add tests

## Code Style

- Use CommonJS (`require`/`module.exports`) - not ESM
- Keep dependencies minimal
- All async methods should return Promises
- Include JSDoc comments on public methods

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request with a clear description

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
