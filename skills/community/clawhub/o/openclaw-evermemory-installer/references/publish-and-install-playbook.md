# EverMemory Install/Publish Playbook

## 1. Install Plugin (OpenClaw)

Local path install:

```bash
openclaw plugins install /path/to/evermemory --link
openclaw plugins enable evermemory
openclaw config set plugins.slots.memory evermemory
openclaw gateway restart
openclaw plugins info evermemory
```

From npm:

```bash
openclaw plugins install your-scope/evermemory@0.0.1
openclaw plugins enable evermemory
openclaw config set plugins.slots.memory evermemory
openclaw gateway restart
```

## 2. Publish Skill (ClawHub)

```bash
clawhub login
clawhub whoami
clawhub publish skills/openclaw-evermemory-installer \
  --slug openclaw-evermemory-installer \
  --name "OpenClaw EverMemory Installer" \
  --version 0.1.0 \
  --changelog "Initial release"
```

## 3. Publish Plugin (npm)

Preconditions:
- `package.json` must not be `private: true`
- `npm whoami` succeeds
- release gates pass

```bash
npm run teams:release
npm run release:pack
npm publish --access public --tag latest
```

## 4. Quality Gates (mandatory)

```bash
npm run teams:dev
npm run teams:release
npm run test:recall:benchmark
```

Benchmark hard gate: `>= 0.90`  
Freeze target: `>= 0.95`
