# 参考文献辅助脚本核心逻辑

> 以下为两个常用辅助脚本的核心逻辑提取。当项目中存在这些脚本时优先直接调用；不存在时，可参考以下逻辑临时编写等效代码或由 LLM 直接处理。

## 一、analyze_bib.py — BibTeX 分析与引用交叉验证

### 核心功能
1. 解析 .bib 文件提取条目元数据（key, type, title, author, year, journal, line_number）
2. 重复检测：精确 key 匹配 + 标题模糊匹配（阈值 85%）
3. 问题 key 检测（空格、非 ASCII、LaTeX 特殊字符）
4. 从 .tex 提取 `\cite{...}` 引用键，支持多键展开
5. 交叉验证：unused entries + missing references

### 关键正则表达式

```python
# 解析 BibTeX 条目
entry_pattern = r'@(\w+)\{([^,]+),'

# 提取 title 字段
title_pattern = r'title\s*=\s*[{"]([^"}]+)[}"]'

# 提取 LaTeX 引用（含可选参数）
cite_pattern = r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}'
```

### 标题相似度比较

```python
from difflib import SequenceMatcher

def normalize_title(title):
    """去除特殊字符、转小写、合并空白"""
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    return ' '.join(title.split())

def title_similarity(t1, t2):
    return SequenceMatcher(None, normalize_title(t1), normalize_title(t2)).ratio()

# 阈值 > 0.85 判定为疑似重复
```

### 调用方式

```bash
# 在项目目录下运行（需要 Ref.bib 和 main.tex 在同目录）
python analyze_bib.py
```

输出包含：重复 key、相似标题、未使用条目、缺失引用的详细报告。

---

## 二、nameTranslate.py — 期刊名标准化

### 核心功能
1. 从 IEEEfull.bib 加载 IEEE 期刊全名 → 宏命令映射（约 400+ 条）
2. 扫描 Ref.bib 中硬编码的 `journal = {全名}` 字段
3. 精确匹配 → 直接替换为宏
4. 模糊匹配（cutoff=0.8）→ 近似替换
5. 未匹配 → 报告警告

### 关键正则表达式

```python
# 解析 IEEEfull.bib 的 @STRING 定义
string_pattern = r'@STRING\s*\{\s*(\S+)\s*=\s*(?:"([^"]+)"|\{([^}]+)\})\s*\}'

# 匹配 Ref.bib 中的 journal 字段（花括号包围）
journal_pattern = r'journal\s*=\s*{([^}]+)}'
```

### 替换逻辑

```python
from difflib import get_close_matches

# 1. 精确匹配
if journal_name in full_name_dict:
    macro = full_name_dict[journal_name]
    # journal = {IEEE Trans. Wireless Commun.} → journal = IEEE_J_WCOM

# 2. 模糊匹配（精确失败时）
close = get_close_matches(journal_name, full_name_dict.keys(), n=1, cutoff=0.8)
if close:
    macro = full_name_dict[close[0]]
```

### 调用方式

```bash
# 需要 IEEEfull.bib 和 ref.bib（注意文件名大小写）
python nameTranslate.py
```

### 注意事项
- 脚本默认读取 `ref.bib`（小写），实际项目可能用 `Ref.bib`（大写），需确认
- 已使用 IEEE 宏的条目（如 `journal = IEEE_J_WCOM`，无花括号）不会被匹配，不受影响
- 替换后建议人工确认，模糊匹配可能有误判

---

## 三、LLM 直接处理 vs 脚本处理的决策

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| 期刊名识别（<10条） | LLM | 常见期刊已在训练数据中 |
| 期刊名批量替换（>10条） | 脚本 | 系统性、无遗漏 |
| 重复检测（全文件） | 脚本 | O(n²) 比较，代码更可靠 |
| 单条 DOI 验证 | LLM + WebSearch | 需要网络能力 |
| 批量格式检查 | 两者结合 | 脚本扫描 + LLM 判断边界情况 |
| 新增条目生成 | LLM | 需要理解语义和规范 |
