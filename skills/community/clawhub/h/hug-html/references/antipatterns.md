# 反模式手册

本文档列出 hug-html 技能的常见反模式及正确做法。

---

## 反模式列表

### ❌ 错误：在 SKILL.md 中粘贴大段代码

**问题**：SKILL.md 应保持 ≤230 行，大段代码会导致文件臃肿，违反 R-17 渐进式加载规范。

**正确做法**：将代码移到 `scripts/` 目录，在 SKILL.md 中描述调用方式。

```markdown
❌ 错误示例：
```python
def generate_template():
    # ... 50行代码 ...
```

✅ 正确示例：
调用 `scripts/template_generator.py --output <path> --type <promo|product|tech|flow>`
```

---

### ❌ 错误：使用相对路径 `./scripts/grid_builder.py`

**问题**：相对路径在不同工作目录下会解析错误，导致脚本找不到。

**正确做法**：使用相对路径（如 `scripts/grid_builder.py`），skill-standardization 审计工具会自动拼接安装目录。

```markdown
❌ 错误：python "C:/Users/.../scripts/template_generator.py"
✅ 正确：python scripts/template_generator.py --output ../.standardization/hug-html/data/output/result.html
```

---

### ❌ 错误：在 SKILL.md 中写"详见脚本注释"

**问题**：用户无法看到脚本注释，且脚本注释容易过时。

**正确做法**：将详细说明写入 `references/guide.md`，SKILL.md 只写必要信息。

---

### ❌ 错误：产出物路径指向安装目录

**问题**：`artifact_paths` 应指向数据目录（`../.standardization/hug-html/data/output/`），而非安装目录下的 `data/output/`。

**正确做法**：

在 `SKILL.md` frontmatter 中：
```yaml
artifact_paths: ["../.standardization/hug-html/data/output/"]
```

在脚本中：
```python
from pathlib import Path
output_dir = Path(__file__).parent.parent.parent / ".standardization" / "hug-html" / "data" / "output"
```

---

### ❌ 错误：模块名拼写错误

**问题**：`SKILL.md` 或 `references/` 中引用的模块名与实际文件名不一致，导致用户调用失败。

**正确做法**：每次提及脚本名时，用绝对路径验证文件是否存在。

```
✅ 正确：python "C:/Users/sm001/.workbuddy/skills/hug-html/scripts/template_generator.py" --help
```

---

### ❌ 错误：术语不一致

**问题**：同一概念混用多个术语（如"配置"/"配置"、"填充内容"/"填内容"），增加理解成本。

**正确做法**：全文统一术语。

| 概念 | 统一术语 | 错误术语 |
|------|----------|----------|
| configuration | 配置 | 配置、setting |
| fill content | 填充内容 | 填内容、填入 |
| module | 模块 | 组件、component |
| preset | 预设 | 预置、preset |
| update | 更新 | 更新、modify |

---

## 检查清单

- [ ] SKILL.md ≤ 230 行？
- [ ] 无大段代码（>10行）直接在 SKILL.md 中？
- [ ] 所有路径均为相对路径？
- [ ] 无"详见脚本注释"等推卸责任的描述？
- [ ] `artifact_paths` 指向数据目录而非安装目录？
- [ ] 所有脚本名拼写正确且文件存在？
- [ ] 术语全文统一？

---

> 本文档遵循 R-18 反模式引用规范，由 `skill-standardization v2.38.6` 生成。
