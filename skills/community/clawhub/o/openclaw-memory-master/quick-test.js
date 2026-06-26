{
  "name": "openclaw-memory-master",
  "version": "4.3.0",
  "description": "AI Memory System with LLM Wiki",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "node test/run-tests.js",
    "test:quick": "ts-node test/comprehensive.test.ts",
    "build": "tsc --outDir dist --module commonjs --target es2020 --lib es2020,dom --esModuleInterop --resolveJsonModule --declaration src/**/*.ts test/**/*.ts",
    "dev": "ts-node src/index.ts"
  },
  "keywords": [
    "memory",
    "ai",
    "agent",
    "openclaw"
  ],
  "author": "Ghost and Jake",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/cp3d1455926-svg/openclaw-memory.git"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "ts-node": "^10.9.0"
  }
}
