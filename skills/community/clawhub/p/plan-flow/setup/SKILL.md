---
name: setup
description: Analyze project structure and create Plan-Flow configuration
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Setup

Analyze the current repository and generate Plan-Flow configuration files.

## What It Does

1. Scans project structure to detect languages and frameworks
2. Creates the `flow/` directory structure
3. Identifies existing patterns in the codebase
4. Generates initial configuration

## Usage

```
/setup [path]
```

**Arguments:**
- `path` (optional): Directory to analyze. Defaults to current directory.

## Output

Creates the following structure:

```
flow/
├── archive/           # Completed/abandoned plans
├── contracts/         # Integration contracts
├── discovery/         # Discovery documents
├── plans/             # Active implementation plans
├── references/        # Reference materials
├── reviewed-code/     # Code review documents
└── reviewed-pr/       # PR review documents
```

## Example

```
/setup
```

**Output:**
```
Setup Complete!

Analyzed: /path/to/project
Files found: 156
Languages detected: TypeScript, JavaScript
Frameworks detected: Next.js, Jest

Created Directories:
- flow/discovery/
- flow/plans/
- flow/contracts/
- flow/references/
- flow/archive/

Next Steps:
1. Create .plan-flow.yml with your AI API key
2. Run /discovery to gather requirements for a feature
3. Run /create-plan to create an implementation plan
```

## Next Command

After setup, run `/discovery` to start gathering requirements for a new feature.
