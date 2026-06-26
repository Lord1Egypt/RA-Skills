# Kazakh-Convert - 哈萨克文转换技能

> **版本**: 2.0 (OpenClaw 适配版)  
> **创建**: 2026-04-05  
> **来源**: D:\PROJECT\WEB\kazakh-convert  
> **功能**: 哈萨克文在西里尔文和阿拉伯文之间双向转换

---

## 📋 技能描述

哈萨克文转换工具，支持在**西里尔文**（哈萨克斯坦官方文字）和**阿拉伯文**（中国哈萨克族传统文字）之间相互转换。

**核心功能:**
- ✅ 西里尔文 → 阿拉伯文
- ✅ 阿拉伯文 → 西里尔文
- ✅ 词库管理（添加/删除/查询自定义词汇）
- ✅ 文件批量转换
- ✅ 语法自动修正

---

## 🎯 触发规则

### 自动触发
当用户消息包含以下关键词时自动调用此技能：

```yaml
triggers:
  - "哈萨克文转换"
  - "西里尔文转阿拉伯文"
  - "阿拉伯文转西里尔文"
  - "kazakh convert"
  - "kazakh-convert"
  - "转成阿拉伯文"
  - "转成西里尔文"
  - "哈萨克语转换"
```

### 手动调用
```bash
# 直接调用技能
kazakh-convert convert --mode cyrillic --text "Қазақ тілі"
```

---

## 🛠️ 工具定义

### 转换工具 (convert)

**功能**: 执行哈萨克文转换

**参数:**
- `--mode` (必需): 转换模式
  - `cyrillic`: 西里尔文转阿拉伯文
  - `arabic`: 阿拉伯文转西里尔文
- `--text, -t`: 直接输入文本（与 `--input` 二选一）
- `--input, -i`: 输入文件路径（与 `--text` 二选一）
- `--output, -o`: 输出文件路径（可选，默认输出到终端）
- `--dict, -d`: 用户词库文件路径（默认：`skills/kazakh-convert/user.dic`）

**示例:**
```bash
# 西里尔文转阿拉伯文
kazakh-convert convert --mode cyrillic --text "Сәлем, қалың қалай?"

# 阿拉伯文转西里尔文
kazakh-convert convert --mode arabic --text "سەلەم، قالىڭ قالاي؟"

# 从文件读取并输出到文件
kazakh-convert convert --mode cyrillic --input input.txt --output output.txt
```

---

### 词库管理工具 (dict)

**功能**: 管理自定义词库

**子命令:**

#### 列出词库
```bash
kazakh-convert dict list --section arabic
kazakh-convert dict list --section cyrillic
```

#### 添加词条
```bash
# 添加到阿拉伯文词库（用于西里尔文转阿拉伯文后的修正）
kazakh-convert dict add --section arabic --key "тест" --value "تست"

# 添加到西里尔文词库（用于阿拉伯文转西里尔文后的修正）
kazakh-convert dict add --section cyrillic --key "көмсөмөл" --value "комсомол"
```

#### 删除词条
```bash
kazakh-convert dict delete --section arabic --key "тест"
```

---

## 📁 文件结构

```
skills/kazakh-convert/
├── SKILL.md          # 技能定义（本文件）
├── kazConvert.py     # 转换脚本
├── user.dic          # 用户词库
├── README.md         # 详细文档（可选）
└── scripts/          # 辅助脚本（可选）
    └── convert.bat   # Windows 批处理快捷方式
```

---

## 🔧 执行脚本

### Python 脚本调用

```python
import sys
sys.path.insert(0, 'skills/kazakh-convert')
from kazConvert import convert_text, load_user_dict

# 加载词库
user_dict = load_user_dict('skills/kazakh-convert/user.dic')

# 西里尔文转阿拉伯文
result = convert_text("Қазақ тілі", 'cyrillic', user_dict)
print(result)

# 阿拉伯文转西里尔文
result = convert_text("قازاق ءتىلى", 'arabic', user_dict)
print(result)
```

### 命令行调用

```powershell
# 设置 UTF-8 编码
$env:PYTHONIOENCODING="utf-8"

# 执行转换
python skills/kazakh-convert/kazConvert.py convert --mode cyrillic --text "Сәлем"
```

---

## 📝 使用场景

### 场景 1: 日常对话转换
```
用户: "把这句话转成阿拉伯文：Сәлем, қалың қалай?"
伽马: 调用 kazakh-convert → 返回 "سەلەم، قالىڭ قالاي؟"
```

### 场景 2: 文件批量转换
```
用户: "把这个哈萨克语文档转成阿拉伯文"
伽马: 
  1. 读取文件内容
  2. 调用 kazakh-convert convert --mode cyrillic --input file.txt --output output.txt
  3. 返回转换后的文件路径
```

### 场景 3: 词库管理
```
用户: "添加一个词，'تەكس' 转成 'تەكست'"
用户：转换错误 تەكس应该是تەكست
伽马: 调用 kazakh-convert dict add --section arabic --key "تەكس" --value "تەكست"
```

---

## ⚠️ 注意事项

1. **UTF-8 编码**: 所有文件操作必须使用 UTF-8 编码
2. **词库优先级**: 用户词库优先于内置映射表
3. **长词优先**: 转换时优先匹配较长的词语
4. **语法修正**: 转换后自动应用语法规则修正

---

## 🧪 测试用例

```bash
# 测试 1: 基本西里尔文转阿拉伯文
python kazConvert.py A "сэнің атың кім болады?"
# 预期输出：سەنىڭ اتىڭ كىم بولادى؟

# 测试 2: 基本阿拉伯文转西里尔文
python kazConvert.py C "سەنىڭ اتىڭ كىم بولادى؟"
# 预期输出：сенің атың кім болады?

# 测试 3: 2.0 版本命令
python kazConvert.py convert --mode cyrillic --text "Қазақ тілі"
# 预期输出：قازاق ءتىلى

# 测试 4: 词库管理
python kazConvert.py dict list --section arabic
```

---

## 📚 参考资料

- 原版项目：D:\PROJECT\WEB\kazakh-convert
- 哈萨克文西里尔字母：33 个字母（9 个特有：ә, і, ү, ө, ң, ғ, ұ, қ, һ）
- 哈萨克文阿拉伯字母：32 个字母（基于波斯 - 阿拉伯字母表）

---

## 🔄 版本历史

- **2.0** (2026-04-05): OpenClaw 技能适配版
  - 添加 SKILL.md 触发规则
  - 集成到 OpenClaw 技能系统
  - 支持自动触发和手动调用

- **2.0** (原版): Python 命令行工具
  - 词库管理功能
  - 文件输入输出
  - 兼容 1.0 语法

- **1.0** (原版): Web 应用版本

---

*最后更新：2026-04-05*
