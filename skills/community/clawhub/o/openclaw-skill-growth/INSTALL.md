# Install

## 1. Clone the repository

```bash
git clone https://github.com/Shuai-DaiDai/openclaw-skill-growth.git
cd openclaw-skill-growth
```

## 2. Install dependencies

```bash
npm install
```

## 3. Build and test

```bash
npm run build
npm run test
```

## 4. Run common commands

### Generate a report

```bash
npm run report
```

### Simulate guarded apply without writing

```bash
npm run demo:dry-run
```

### Run apply against demo fixtures

```bash
npm run demo:apply
```

## 5. Use on your own skills

Replace the demo skill directory and run log path with your own inputs, for example:

```bash
node dist/cli.js report \
  --skills-dir ./path/to/skills \
  --runs-file ./path/to/runs.jsonl \
  --out-dir ./output \
  --config ./examples/config.json
```
