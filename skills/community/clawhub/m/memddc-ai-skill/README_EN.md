# memddc-ai-skill

> [中文版本](README.md)

## One-Line Summary

MemDDC = Code checkup (init) → Record snapshot → AI doctor fast diagnosis

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Project Scan** | Auto-scan full codebase on first use, generate docs |
| **Three-Tier Index** | metadata/index/context structure, fast file positioning |
| **Relation Mapping** | entity→mapper→service→controller→view, lookup by ID |
| **DDD Constraints** | Modifications must conform to domain model and contracts |
| **VCS Analysis** | Auto-analyze Git commit patterns, understand team collaboration |
| **Token Savings** | 53% Token reduction measured in complex business modifications |

## Trigger Keywords

```
MemDDC, Load memory constraints for modification, Iterate according to DDD contract, memddc-init, memddc-update, memddc-sync
```

## Workflow

### 1. Initialization (memddc-init)

Scan project → Generate docs → Build mem-snapshot.json (three-tier index + relations)

### 2. Code Modification

Read mem-snapshot.json → Query index to locate files → Modify with DDD constraints → Sync docs

### 3. Incremental Sync (memddc-sync)

git diff → Analyze change scope → Precisely update affected docs → Update snapshot

## mem-snapshot.json Structure

```json
{
  "metadata": { "name": "RuoYi-Vue", "version": "1.0", "tech": "Java+Spring Boot" },
  "index": {
    "entities": { "SysDept": { "path": ".../SysDept.java", "module": "system" } },
    "relations": {
      "SysDept": {
        "entity": ".../SysDept.java",
        "mapper": ".../SysDeptMapper.xml",
        "service": ".../SysDeptServiceImpl.java",
        "controller": ".../SysDeptController.java",
        "views": [".../dept/index.vue"]
      }
    }
  },
  "context": {
    "patterns": ["treeBuild", "pagination", "crudApi"],
    "codeStyle": { "returnType": "AjaxResult", "annotation": "@RestController" }
  }
}
```

## Measured Results

Tested on RuoYi-Vue full-stack project:

| Scenario | With MemDDC | Without | Savings |
|----------|-------------|---------|---------|
| Project description | ~49,000 token | ~77,000 token | **36%** |
| Business modification | ~18,000 token | ~38,000 token | **53%** |
| Conversation rounds | 4 rounds | 6-10 rounds | **60%** |

## Directory Structure

```
project/
├── .memddc/
│   ├── mem-snapshot.json       # Three-tier index snapshot
│   ├── vcs-log-analysis.md    # VCS log analysis
│   ├── file-tree-analysis.md  # File structure analysis
│   └── docs/                  # Project documents
│       ├── architecture.md
│       ├── ddd-model.md
│       └── api.md
└── [Project Source]
```

## Use Cases

- **Team Collaboration**: Unified docs, new members get up to speed quickly
- **Complex Architecture**: DDD constraints, prevent reckless modifications
- **Legacy Systems**: Complete docs for refactoring
- **Long-term Maintenance**: Record decision history, understand design intent

## Tech Stack Support

| Language/Framework | Doc Generation | DDD Modeling | Memory Compression |
|--------------------|----------------|--------------|-------------------|
| Java/Spring | ✅ | ✅ | ✅ |
| Python/Django | ✅ | ✅ | ✅ |
| Go/Gin | ✅ | ✅ | ✅ |
| Vue/React | ✅ | ⚠️ | ✅ |

## Versions

- **v1.0.2** (current): Three-tier index + Relation mapping + VCS analysis
- **v1.0.1**: Team collaboration + Smart triggers

## Links

- GitHub: <https://github.com/qihao123/memddc-ai-skill>
- Email: <qihoo2017@gmail.com>
