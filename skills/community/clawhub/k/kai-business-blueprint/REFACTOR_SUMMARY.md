# 目录重构总结（2026-04-25）

## 问题分析

原目录结构存在**命名混乱**，导致双重身份冲突：

### Python 包视角
```
business_blueprint/
├── specs/__init__.py    ← Python代码模块（导出规格构建器）
├── specs/*.md           ← 文档混在代码目录 ❌
└── templates/           ← JSON模板数据 ✅
```

**问题**：`specs/` 名称误导，看起来是"文档目录"，实际是Python代码模块。

### Skill 视角
```
references/              ← Skill外部文档 ✅
SKILL.md                 ← Skill定义 ✅
```

**问题**：包内文档（实体定义、分类规则）没有明确的存放位置。

---

## 重构方案

### 核心原则

1. **Python包约束优先**：代码模块和数据必须在包内（`Path(__file__).parent` 加载）
2. **语义清晰**：目录名称反映真实用途
3. **职责分离**：代码、文档、数据独立目录

### 新目录结构

```
business_blueprint/              # Python包（pyproject.toml定义）
├── renderers/                   # Python导出规格构建器（原specs）
│   ├── __init__.py              # build_svg_spec(), build_drawio_spec()等
│   └── __pycache__/             # 编译缓存
├── docs/                        # 包内文档（新目录）
│   ├── entities-schema.md       # 实体定义（capabilities, actors等）
│   └── systems-schema.md        # Systems分类规则（category: layer vs service）
├── templates/                   # JSON模板数据（保留）
│   ├── common/seed.json         # 基础模板 + 字段示例
│   ├── finance/seed.json        # 金融行业hints
│   ├── manufacturing/seed.json  # 制造行业hints
│   └── retail/seed.json         # 零售行业hints
├── assets/                      # 静态资源（HTML模板）
└── *.py                         # 核心代码（export_svg.py, cli.py等）

references/                       # Skill外部文档（标准目录）
├── blueprint-schema.md          # 已存在
├── implementation-plan.md       # 已存在
└── ...

SKILL.md                          # Skill路由层（指向docs + templates）
```

---

## 文件改动

| 文件 | 改动类型 | 内容 |
|------|---------|------|
| `business_blueprint/specs/` | 重命名 | → `business_blueprint/renderers/` |
| `business_blueprint/specs/*.md` | 移动 | → `business_blueprint/docs/` |
| `SKILL.md` | 更新引用 | `specs/entities-schema.md` → `docs/entities-schema.md` |
| `export_drawio.py` | 更新import | `from .specs` → `from .renderers` |
| `export_excalidraw.py` | 更新import | `from .specs` → `from .renderers` |

---

## 职责分工

| 目录 | 作用 | 内容类型 | 调用者 |
|------|------|---------|--------|
| `renderers/` | 导出规格构建器 | Python代码 | export_*.py |
| `docs/` | 包内文档 | Markdown文档 | SKILL.md（路由） |
| `templates/` | 数据模板 | JSON文件 | generate.py（`Path(__file__).parent`） |
| `references/` | Skill文档 | 设计文档 | AI Agent阅读 |

**关键区别**：
- `docs/` = 包内文档（实体定义，AI生成blueprint时参考）
- `references/` = Skill文档（设计规范，人类阅读）

---

## 验证结果

### 功能测试
```bash
python3 -m pytest tests/ -x
# 173 passed, 1 skipped ✅
```

### 导出测试
```python
from business_blueprint.export_html import export_html_viewer
export_html_viewer(blueprint, output_path)
# ✅ 成功导出 29.7 KB HTML viewer
```

### 路径引用
```markdown
# SKILL.md
- See `business_blueprint/docs/entities-schema.md` for field definitions ✅
- See `business_blueprint/docs/systems-schema.md` for category rules ✅
- See `business_blueprint/templates/common/seed.json` for examples ✅
```

---

## 对比标准Skill目录

### 标准Skill结构
```
skill-name/
├── references/         # 文档
├── scripts/            # 可执行脚本（可选）
└── SKILL.md            # Skill定义
```

### 本Skill特殊之处

**Python包身份**（强制约束）：
- 必须有 `business_blueprint/` 目录（pyproject.toml定义）
- 必须有 `__init__.py`（包标识）
- 必须用 `Path(__file__).parent` 加载包内资源

**双重身份解决方案**：
- 包内代码 → `business_blueprint/*.py` + `renderers/`
- 包内文档 → `business_blueprint/docs/`
- 包内数据 → `business_blueprint/templates/`
- Skill文档 → `references/`（标准目录）

---

## 后续维护建议

### 添加新导出格式
1. 在 `business_blueprint/export_{format}.py` 实现导出函数
2. 从 `renderers` import规格构建器（如需要）
3. 更新 `cli.py` 添加 `--format {format}` 支持

### 添加新实体定义
1. 在 `business_blueprint/docs/entities-schema.md` 添加字段说明
2. 在 `business_blueprint/templates/common/seed.json` 添加示例字段
3. 在 `SKILL.md` 保持路由引用（不写实体逻辑）

### 添加新行业模板
1. 在 `business_blueprint/templates/{industry}/seed.json` 添加 `industryHints.checklist`
2. 在 `generate.py` 的 `_VALID_INDUSTRIES` 添加行业名
3. 更新 `SKILL.md` 行业选择表

---

## 命名规范

### 目录命名
- **renderers** = 导出渲染器（代码）
- **docs** = 包内文档（Markdown）
- **templates** = 数据模板（JSON）
- **references** = Skill文档（设计规范）

### 避免
- ❌ `specs/` （名称误导：看起来像文档，实际是代码）
- ❌ 文档混在代码目录（`specs/*.md`）
- ❌ 代码模块使用文档类名称

---

## Git提交记录

```bash
git add -A
git commit -m "refactor: rename specs → renderers, move docs to docs/

- business_blueprint/specs/ → business_blueprint/renderers/ (Python module)
- business_blueprint/specs/*.md → business_blueprint/docs/ (documentation)
- Update import paths in export_drawio.py, export_excalidraw.py
- Update SKILL.md references to docs/

All tests pass (173 passed, 1 skipped)
"
```

---

## 相关文档

- `business_blueprint/docs/entities-schema.md` - 实体定义
- `business_blueprint/docs/systems-schema.md` - Systems分类规则
- `references/blueprint-schema.md` - Blueprint JSON schema参考
- `SKILL.md` - Skill路由层

---

**重构日期**: 2026-04-25
**验证状态**: ✅ 全部通过
**影响范围**: 目录结构、import路径、文档引用