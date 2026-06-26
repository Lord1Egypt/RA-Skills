# 📄 Official Doc - 公文格式转换

🇨🇳 中文文档 | 🇺🇸 [English](README.md)

将 Markdown 文档转换为符合 **GB/T 9704-2012** 党政机关公文格式的 Word 文档。专注排版格式转换，不添加红头、版记、落款等公文装饰要素。

---

## ⚠️ 重要说明

本工具仅提供格式排版功能，不负责内容审核。请确保使用本工具生成的公文内容符合相关规定和要求。

---

## ✨ 功能特点

| 功能 | 描述 |
|------|------|
| 🚀 **一键转换** | Markdown 转 Word 公文格式，简单易用 |
| 📋 **标准遵循** | 严格按照 GB/T 9704-2012 党政机关公文格式标准 |
| 🤖 **多智能体兼容** | 支持 OpenClaw、Hermes Agent、Claude Code 等 AI 智能体 |
| 🔄 **双重输出** | 一份内容，同时生成 Markdown（供机器读）和 Word（供人读） |
| 📊 **自动化支持** | 支持定时任务自动生成简报、周报、月报 |
| 📦 **易于集成** | 提供标准 Python API，便于其他系统集成 |

---

## 🆕 v1.1.0 新特性

- 引入 **markdown-it-py** 解析器，支持多行段落、嵌套列表
- `#` 标题智能判断：单个视为大标题（居中不加序号），多个视为一级标题（加序号）
- 首行缩进精确对齐国标（640 twips = 2个三号汉字宽度）
- 新增表格、图片、超链接、代码块、嵌套列表支持
- **加粗文本**自动转为黑体，*斜体文本*自动转为楷体

---

## 🚀 快速开始

### 环境要求

| 组件 | 要求 |
|------|------|
| 操作系统 | Windows 10/11、Linux、macOS |
| Python | 3.8+（支持 3.11 / 3.12 / 3.13） |
| 依赖 | python-docx >= 1.1.0, markdown-it-py >= 3.0.0 |

### 安装方法

**方式一：使用 pip 安装**
```bash
pip install python-docx>=1.1.0 markdown-it-py>=3.0.0
```

**方式二：克隆仓库**
```bash
git clone https://github.com/EdwardWason/official-doc.git
cd official-doc
pip install -r requirements.txt
```

### 使用示例

```python
from official_doc import md_to_docx

# Markdown 内容
md_content = """# 工作简报

## 一、上周工作总结

本周完成了系统升级任务，主要包括：

### （一）主要工作
1. 完成服务器部署
2. 完成数据迁移
3. 完成测试验证

### （二）存在问题
部分功能需要进一步优化。

### （三）下周计划
继续推进优化工作。
"""

# 转换为公文格式
success = md_to_docx(md_content, "工作简报_公文格式.docx")
print("转换成功" if success else "转换失败")
```

---

## 📋 公文格式规范（GB/T 9704-2012）

### 页面设置

| 设置项 | 规范值 |
|--------|--------|
| 纸张尺寸 | A4 (210mm × 297mm) |
| 上边距 | 3.7cm |
| 下边距 | 3.5cm |
| 左边距 | 2.8cm |
| 右边距 | 2.6cm |
| 行间距 | 固定值 26 磅 |
| 首行缩进 | 2字符（640 twips） |

### 字体规范

| 元素 | Markdown 标记 | 字体 | 字号 |
|------|--------------|------|------|
| 大标题 | `#`（单个） | 方正小标宋简体 | 二号 |
| 一级标题 | `##` / `#`（多个） | 黑体 | 三号 |
| 二级标题 | `###` | 楷体_GB2312 | 三号 |
| 三级标题 | `####` | 仿宋_GB2312 | 三号 |
| 正文 | 普通文本 | 仿宋_GB2312 | 三号 |
| 页码 | - | 宋体 | 四号 |

### 标题编号规则

| 层级 | 判断条件 | 格式示例 |
|------|----------|----------|
| 大标题 | 文档中仅一个 `#` | 公文标题（居中，不加序号） |
| 一级标题 | `##` 或多个 `#` | 一、章节名称 |
| 二级标题 | `###` | （一）小节名称 |
| 三级标题 | `####` | 1. 项目名称 |

### 支持的 Markdown 元素

| 元素 | Markdown 语法 | 说明 |
|------|--------------|------|
| 标题 | `#` `##` `###` `####` | 智能标题判断 |
| 段落 | 普通文本 | 支持多行段落 |
| 有序列表 | `1. 2. 3.` | 支持嵌套列表 |
| 无序列表 | `- - -` | 支持嵌套列表 |
| 表格 | `\| 列 \| 列 \|` | 完整表格支持 |
| 图片 | `![alt](url)` | 行内图片 |
| 超链接 | `[文本](url)` | 超链接 |
| 加粗 | `**文本**` | 自动转为黑体 |
| 斜体 | `*文本*` | 自动转为楷体 |
| 代码块 | `` ```代码``` `` | 等宽字体格式 |
| 分隔线 | `---` | 页面分隔 |

---

## 🔧 AI Agent 集成指南

### OpenClaw 集成

```python
from official_doc import md_to_docx
from openclaw import Skill

class OfficialDocSkill(Skill):
    name = "official-doc"
    description = "公文格式转换 - 将 Markdown 转为党政机关公文格式"

    def execute(self, md_content, output_path=None):
        if output_path is None:
            output_path = "output_公文格式.docx"

        success = md_to_docx(md_content, output_path)

        return {
            "success": success,
            "output_path": output_path,
            "message": "公文格式转换完成" if success else "转换失败"
        }
```

### Hermes Agent 集成

```python
# 调用示例
from hermes import Agent

agent = Agent()
result = agent.run_skill(
    skill="official-doc",
    md_content=report_content,
    output_path="weekly_report.docx"
)
```

### 定时任务配置

```python
import schedule
import time
from official_doc import md_to_docx

def generate_daily_report():
    content = generate_report_content()
    today = time.strftime("%Y-%m-%d")
    md_to_docx(content, f"工作简报_{today}_公文格式.docx")

# 每周一至周五 9:00 自动执行
schedule.every().monday.at("09:00").do(generate_daily_report)
schedule.every().tuesday.at("09:00").do(generate_daily_report)
schedule.every().wednesday.at("09:00").do(generate_daily_report)
schedule.every().thursday.at("09:00").do(generate_daily_report)
schedule.every().friday.at("09:00").do(generate_daily_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📁 项目结构

```
official-doc/
├── src/                      # 源代码目录
│   ├── __init__.py          # 包初始化
│   └── md2docx.py           # 核心转换模块
├── skill.json               # AI Agent 技能配置
├── setup.py                 # 安装配置
├── requirements.txt         # 依赖清单
├── README.md                # 英文文档
├── README_CN.md             # 中文文档
├── CHANGELOG.md             # 更新日志
├── LICENSE                  # MIT 许可证
└── .gitignore               # Git 忽略配置
```

---

## 🧪 测试验证

```bash
# 创建测试脚本
cat > test_official_doc.py << 'EOF'
from official_doc import md_to_docx

def test_basic_conversion():
    md_content = """# 测试文档

## 一、测试标题

这是一个测试段落。

### （一）二级标题

1. 列表项一
2. 列表项二

**加粗文本** 测试。
"""
    success = md_to_docx(md_content, 'test_output.docx')
    assert success == True
    print("✓ 基本转换测试通过")

if __name__ == "__main__":
    test_basic_conversion()
    print("\n✅ 所有测试通过！")
EOF

# 运行测试
python test_official_doc.py
```

---

## 📜 许可证

MIT License

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📞 联系方式

- **GitHub**: [https://github.com/EdwardWason/official-doc](https://github.com/EdwardWason/official-doc)
- **Issues**: [https://github.com/EdwardWason/official-doc/issues](https://github.com/EdwardWason/official-doc/issues)

---

*Built with ❤️ for LLM + AI Agent 生态*
