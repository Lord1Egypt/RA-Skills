# Course Templates

Pre-built course profiles for quick onboarding. Use when the user has not yet uploaded materials or described their course in detail.

## Usage

In agent shell:
```bash
python scripts/course_templates.py list           # show all templates
python scripts/course_templates.py show "math-analysis"  # preview template
python scripts/course_templates.py apply "math-analysis"  # save as snapshot
python scripts/course_templates.py apply "data-structures" --active  # save and set active
```

In plain chat or RAG notebook:
```
告诉我你的课程，我可以用内置模板快速开始。可用模板：
- 高等数学
- 大学物理 / 普通物理
- 程序设计（C/C++）
- 数字电路与逻辑设计
- 马克思主义基本原理
- 数据结构与算法
- 线性代数
- 计算机网络
- 操作系统
```

## Available Templates

| Key | Course | Subject |
|-----|--------|---------|
| `advanced-math` | 高等数学 | mathematics |
| `physics` | 大学物理 / 普通物理 | physics |
| `programming-c-cpp` | 程序设计（C/C++） | programming |
| `digital-logic` | 数字电路与逻辑设计 | engineering |
| `marxism-basic-principles` | 马克思主义基本原理 | politics |
| `data-structures` | 数据结构与算法 | programming |
| `math-analysis` | 数学分析 / 高等数学 | mathematics |
| `linear-algebra` | 线性代数 | mathematics |
| `computer-networks` | 计算机网络 | computer science |
| `operating-system` | 操作系统 | computer science |
| `university-physics` | 大学物理 | physics |

## Adding Templates

Templates are defined in `scripts/course_templates.py` as a `TEMPLATES` dict. Each template has:

- `name`: course display name
- `subject_family`: maps to `subject-adaptation.md` discipline
- `assessment`: exam format
- `level`: default level (usually "shaky" for new setup)
- `environment`: agent-shell / rag-notebook / notes-app / plain-chat / unknown
- `notes`: additional guidance text

The snapshot output includes a `from template "<key>"` tag in the `Last action` field. Use `unknown` environment by default for broad templates; let `references/environment-adaptation.md` set the final environment after capability detection.
