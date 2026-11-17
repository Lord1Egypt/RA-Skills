# API 文档自动生成：以代码为唯一真相源

## 一、问题与目标

大型项目中 API 文档和代码脱节是常态——接口改了，文档忘了更新；文档写对了，代码却走样了。根本原因只有一个：**文档和代码是两份独立维护的东西**。

本技术方案解决的核心问题是：**如何让 API 文档天然与代码保持同步，且维护成本趋近于零。**

方案只有一条规则：**代码是唯一真相源**。文档不手写，从代码自动提取。代码动了，重跑生成脚本即可。

---

## 二、机制拆解

### 2.1 信息来源

代码中天然包含三类 API 元信息：

| 信息来源 | 内容 | Python 提取方式 |
|----------|------|----------------|
| 类型注解（Type Hints） | 参数名、参数类型、默认值、返回类型 | `inspect.signature()` |
| 文档字符串（Docstring） | 类/函数/方法的说明文字 | `obj.__doc__` |
| Pydantic Field | 字段描述、约束、默认值 | `model.model_fields` |
| 枚举（Enum） | 枚举名、成员值 | `list(enum)` |
| 模块导出（`__all__`） | 哪些符号对外可见 | `module.__all__` |

这些信息全部在源码里，不需要额外标注，也不需要维护一份平行描述。

### 2.2 生成流程

```
源码（.py 文件）
   │
   │  import + inspect 反射
   ▼
遍历所有模块
   │
   ├─ 对每个类：提取类名 + docstring + 构造方法签名 + 方法列表
   ├─ 对每个函数：提取函数名 + docstring + 完整签名
   ├─ 对每个枚举：提取枚举名 + 成员名 + 成员值
   └─ 对 Pydantic 模型：提取字段名 + 类型 + Field 描述 + 默认值
   │
   ▼
按模块路径组织
   │
   ▼
Markdown 文档输出
   ├─ api_reference.md         完整 API 参考，含签名
   ├─ api_class_reference.md    类名速查表（符号→模块）
   └─ api_enums.md              全部枚举类型汇总
```

### 2.3 核心提取逻辑（伪代码）

```python
import inspect, enum, importlib
from pydantic import BaseModel

def extract_module(module):
    results = []
    for name in module.__all__:
        obj = getattr(module, name, None)
        if obj is None:
            continue
        if isinstance(obj, type) and issubclass(obj, enum.Enum):
            results.append(extract_enum(obj))
        elif isinstance(obj, type) and issubclass(obj, BaseModel):
            results.append(extract_pydantic_model(obj))
        elif isinstance(obj, type):
            results.append(extract_class(obj))
        elif callable(obj):
            results.append(extract_function(obj))
    return results

def extract_class(cls):
    sig = inspect.signature(cls.__init__)
    methods = [m for m in dir(cls) if not m.startswith("_")]
    return {
        "name": cls.__name__,
        "doc": cls.__doc__,
        "constructor": str(sig),
        "methods": [
            {"name": m, "signature": str(inspect.signature(getattr(cls, m)))}
            for m in methods
        ],
    }

def extract_enum(e):
    return {
        "name": e.__name__,
        "members": [(m.name, m.value) for m in e],
    }
```

### 2.4 真实项目中的文档结构

本项目产出的三份自动文档各有明确职责：

**`api_reference.md`** — 完整 API 参考
- 按模块路径分层组织（`scripts.cognitive.*`、`scripts.infra.*` 等）
- 每个类展示：docstring 描述、构造方法签名、全部公开方法签名
- 参数类型、默认值、返回类型全部从源码提取
- 枚举额外展示所有成员及值

**`api_class_reference.md`** — 类名速查表
- 一张大表，列：符号名 / 类型（类/函数/枚举/常量）/ 真实模块路径 / 职责说明
- 用于快速查找某个符号从哪个模块导入

**`api_enums.md`** — 枚举类型汇总
- 按模块分组列出全部枚举
- 每个枚举含：成员名、成员值、说明
- 部分枚举额外标注建议策略、权重等业务信息（来自源码注释）

三份文档均由同一脚本生成，保证互不矛盾。

---

## 三、防漂移机制

只靠"生成脚本存在"还不够，必须有机制保证生成物确实对应代码真实状态。本项目通过两层防护实现：

### 3.1 契约门禁测试

`tests/test_api_contract.py` 在 CI 中运行，覆盖五类历史缺陷：

| 缺陷类型 | 测试用例 | 防什么 |
|----------|----------|--------|
| `__all__` 声明但不可访问 | `test_all_exports_accessible` | 声明导出了但 import 失败 |
| 文档声称的方法名不存在 | `test_core_methods_exist` | 文档写了 `prepare()` 但代码里是 `prepare_context()` |
| 枚举成员漂移 | `test_enum_members_complete` | 枚举新增了值但文档/测试没更新 |
| 双定义遮蔽 | `test_consent_status_single_source` | 同一符号在两个模块定义了，导入时后一个覆盖前一个 |
| 类型兼容性 | `test_store_memory_accepts_string_bucket` | 枚举入参只接受 Enum 对象不接受字符串，导致 `.value` 崩溃 |

这些测试不依赖生成的文档，直接校验代码行为。文档可以错，但代码行为不能错。

### 3.2 文档头声明

每份自动生成的文档顶部都有一段声明：

> 本文档由 `generate-api-docs.py` 自动生成，以代码为唯一真相源。人工修改会被下次生成覆盖。若需更新 API 描述，请修改代码 docstring 后重新生成。

这段声明有两个作用：一是告诉维护者不要直接改文档；二是规定了更新 API 描述的正确流程——改代码 docstring，而不是改文档。

---

## 四、推广到任意 Python 项目

### 4.1 前置条件

1. **项目使用类型注解**：函数和类必须有类型标注，否则提取出的签名信息不完整
2. **项目使用 `__all__` 控制导出**：每个模块声明对外公开的符号
3. **类/函数有 docstring**：至少写一句说明，否则文档会缺失描述
4. **Pydantic 或 dataclass**：结构化配置类使用 Pydantic `BaseModel` + `Field(description=...)`，字段描述自动提取

如果项目满足以上四点，直接套用即可。如果不满足，需要补充这些标注。

### 4.2 实施步骤

**第一步：规范源码**

```python
# 每个模块末尾声明 __all__
__all__ = ["MyClass", "MyFunction", "MyEnum"]

class MyConfig(BaseModel):
    """配置类说明"""
    timeout: float = Field(default=5.0, ge=1, le=30, description="超时秒数")
    retries: int = Field(default=3, ge=0, le=10, description="重试次数")

class MyEnum(str, Enum):
    """枚举说明"""
    VALUE_A = "a"
    VALUE_B = "b"

class MyClass:
    """类说明"""
    def __init__(self, config: MyConfig | None = None):
        ...

    def do_something(self, x: int, y: str = "default") -> bool:
        """方法说明"""
        ...
```

**第二步：编写生成脚本**

```python
#!/usr/bin/env python3
"""generate-api-docs.py — 从源码自动生成 API 文档"""

import importlib, inspect, enum, sys
from pathlib import Path
from pydantic import BaseModel

def generate(package_name: str, output_dir: str):
    pkg = importlib.import_module(package_name)
    doc = f"# {package_name} API 参考\n\n> 自动生成，以代码为唯一真相源\n"
    # 遍历 __all__ → 反射提取 → 写入 Markdown
    # ...（详见伪代码 2.3）...
    Path(output_dir, "api_reference.md").write_text(doc)

if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2])
```

**第三步：集成到工作流**

```bash
# 本地生成
python generate-api-docs.py scripts docs/references

# CI 中增加门禁
python -m pytest tests/test_api_contract.py
python generate-api-docs.py scripts docs/references
git diff --exit-code docs/references/
```

`git diff --exit-code` 确保文档和代码在同一个提交里同步。

### 4.3 关键原则

1. **不要手写文档**：写 docstring，跑生成器。docstring 是代码的一部分，随代码一起 review。
2. **签名是自动提取的，不要手调**：改签名改代码，不碰文档。
3. **文档差异就是代码差异**：CI 中 `git diff` 有输出说明代码改了但没重跑生成器。
4. **枚举和类型定义是 API 契约**：改动枚举值、类型注解属于破坏性变更，需要评审。

---

## 五、非 Python 项目的适配

| 语言 | 等效机制 | 可用工具 |
|------|----------|----------|
| TypeScript/JavaScript | JSDoc + `tsc --emitDeclarationOnly` | TypeDoc、api-extractor |
| Java | Javadoc 注解 | Javadoc、Dokka |
| Go | 注释 + 导出符号 | godoc |
| Rust | `///` 文档注释 | rustdoc |
| C# | XML 文档注释 | DocFX |

核心思路不变：**语言内置的注释/注解系统 + 自动生成器 + CI 门禁**。

---

## 六、成本与收益

| 维度 | 传统手写文档 | 本方案 |
|------|------------|--------|
| 初始投入 | 低（但很快过时） | 中（需补类型注解和 docstring） |
| 持续维护 | 每次改 API 要手动更新文档 | 重跑一次脚本 |
| 漂移概率 | 高 | 零（代码即文档） |
| 新人上手 | 需要判断文档是否最新 | 直接信任文档 |
| CI 覆盖 | 通常无文档测试 | 契约测试自动拦截漂移 |

适合所有有对外 API 的中型以上项目。

---

## 七、常见问题

**Q：docstring 不够详细怎么办？**

A：文档的详细信息来自代码本身。函数名 + 类型签名已经表达了大部分信息。docstring 只需一句话说明用途。确实需要详细说明时，补充到 docstring，重跑即可。

**Q：私有方法/内部类也会出现在文档里吗？**

A：不会。`__all__` 只列出对外公开的符号，生成器只处理 `__all__` 中的对象。用 `__all__` 控制边界。

**Q：生成脚本找不到怎么办？**

A：脚本本身是通用工具，按第二节伪代码实现即可。关键依赖是 Python 标准库的 `inspect` 模块，无需额外安装。

**Q：文档生成后格式乱了怎么办？**

A：不要手写格式化。在生成脚本里固定模板，或接入 Markdown 格式化器（如 `markdownlint`）作为 CI 检查。
