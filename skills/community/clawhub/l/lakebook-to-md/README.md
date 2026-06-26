# Lakebook to Markdown + Excel

将语雀导出的 `.lakebook` 文件转换为 Markdown + Excel 文件夹，保留原始文档目录树结构。

> 基于 [PZh101/YuqueExportToMarkdown](https://github.com/PZh101/YuqueExportToMarkdown) 项目扩展开发，修复了多项 bug，新增多种格式支持。

## ✨ 核心特性

- 📝 **富文本文档** → Markdown
- 📊 **数据库表格** → 同时输出 Markdown + Excel (.xlsx)
- 📎 **附件自动下载** 并记录成功/失败状态
- 📋 **自动生成转换报告** 详细列出需要手动处理的内容

## 功能特性

### 支持的文档格式

| 语雀格式 | 类型 | 说明 | 输出 |
|---|---|---|---|
| `lake` | Doc | 富文本文档 | Markdown (.md) |
| `laketable` | Table | 数据库式表格 | **Markdown + Excel (.xlsx)** |
| `lakesheet` | Sheet | 电子表格（zlib 压缩） | Markdown 表格 |

### 支持的卡片类型

| 卡片 | 输出 | 备注 |
|---|---|---|
| `codeblock` | 带语言标注的 fenced code block | |
| `image` | 下载后 `![]()` 语法 | 自动下载并记录状态 |
| `hr` | `---` 分割线 | |
| `label` | 内联标签文本 | |
| `math` | LaTeX 公式 + 图片 | |
| `file` | 附件链接 | |
| `bookmarkInline` | `> **[标题](URL)** — 来源` | |
| `bookmarklink` | `[标题](URL)` | |
| `localdoc` | 附件自动下载 + 链接 | **记录下载成功/失败状态** |
| `lockedtext` | 加密内容占位提示 | |
| `yuque` | 跨文档引用链接 | |

### 转换报告

每次转换自动生成 `转换报告.md`，包含：

1. **总体统计** - 文档数量、类型分布
2. **成功转换的文档** - 列出所有成功转换的文件
3. **转换失败的文档** - 列出失败原因
4. **图片下载统计** - 成功/失败的图片
5. **附件下载统计** - 成功/失败的附件
6. **过期链接** - 无法下载的资源
7. **需要手动处理的内容** - 汇总需要人工介入的项目

## 安装

### 方式一：pip 安装

```bash
pip install git+https://github.com/luhuiwang/lakebook-to-md.git
```

### 方式二：克隆使用

```bash
git clone https://github.com/luhuiwang/lakebook-to-md.git
cd lakebook-to-md/scripts
pip install -r requirements.txt
```

### 方式三：AionUi Skill

将本仓库克隆到 AionUi 的 skills 目录：

```bash
git clone https://github.com/luhuiwang/lakebook-to-md.git \
  ~/.config/AionUi/config/skills/lakebook-to-md
```

## 使用方法

### 命令行

```bash
# 基本转换
python scripts/startup.py -l 你的导出文件.lakebook -o 输出文件夹

# 或者 pip 安装后直接使用
lakebook2md -l your.lakebook -o output
```

### 可选参数

| 参数 | 说明 |
|---|---|
| `-l` | `.lakebook` 文件路径 |
| `-i` | 已解压的 `meta.json` 路径（二选一） |
| `-o` | 输出文件夹（必填） |
| `-d False` | 禁用图片下载（更快） |
| `-s` | 跳过已下载的资源 |

### Python 调用

```python
import sys
sys.path.insert(0, "lakebook-to-md/scripts")
from lake.lake_setup import start_convert

start_convert(
    meta=None,
    lake_book="your.lakebook",
    output="output_folder",
    download_image_of_in=True,
    skip_existing=False
)
```

## 输出结构

```
output_folder/
├── 转换报告.md          # 转换统计报告
├── 笔记本名称/
│   ├── 文档1.md
│   ├── 文档1.xlsx       # laketable 同时生成 Excel
│   ├── 文档1.assert/    # 图片/附件目录
│   │   ├── image1.png
│   │   └── attachment.pdf
│   └── 子目录/
│       └── 文档2.md
```

## 相比原项目的改进

基于 [PZh101/YuqueExportToMarkdown](https://github.com/PZh101/YuqueExportToMarkdown) 的扩展修复：

| 问题 | 修复 |
|---|---|
| 标题含 `/` 导致路径嵌套重复 | 替换 `/` 为 `_`，使用 `os.path.join` |
| `laketable` 表格文档输出为空 | 解析 `body` 列定义 + `table_records` 记录数据 |
| `lakesheet` 电子表格输出为空 | zlib 解压 `body_draft`，解析压缩数据 |
| `lakesheet` 公式单元格显示原始 JSON | 提取公式计算值 `value` 字段 |
| `bookmarkInline` 卡片不渲染 | 新增支持，输出为引用块链接 |
| `localdoc` 附件卡片不渲染 | 新增支持，自动下载并记录状态 |
| `bookmarklink` 卡片不渲染 | 新增支持，输出为 Markdown 链接 |
| `lockedtext` 加密内容输出为空 | 输出占位提示符 |
| Windows 路径分隔符不兼容 | 统一使用 `os.path.join` + `os.path.sep` |
| `select` 类型列显示 ID 而非文本 | 解析 options 映射，输出显示值 |
| 仅输出 Markdown | 新增 Excel 输出支持 |
| 无转换统计 | 新增详细转换报告 |

## 项目结构

```
lakebook-to-md/
├── SKILL.md              # AionUi 技能定义
├── README.md             # 本文件
├── LICENSE               # Apache-2.0
├── pyproject.toml        # Python 打包配置
├── .gitignore
└── scripts/
    ├── startup.py        # 入口脚本（自动安装依赖）
    ├── requirements.txt
    └── lake/
        ├── __init__.py
        ├── lake_setup.py       # 主转换逻辑 + laketable/lakesheet 解析 + 报告生成
        ├── lake_handle.py      # HTML/ASL 解析器 + 所有卡片类型处理
        ├── lake_reader.py      # lakebook 解包
        └── failure_result_parser.py
```

## 依赖

- `beautifulsoup4>=4.12.0` — HTML/ASL 解析
- `PyYAML>=6.0` — 元数据解析
- `Requests>=2.31.0` — 图片/附件下载
- `openpyxl>=3.1.0` — Excel 文件生成

## 关键实现说明

### laketable 转 Excel

- 自动解析 `select`/`multi_select` 类型的选项值（ID → 显示文本）
- 数字类型列自动转换为数值格式
- 日期类型列提取可读文本
- 自动调整列宽

### lakesheet 解码

`lakesheet` 格式使用 zlib 压缩存储在 `body_draft` 字段中：

```python
sheet_bytes = sheet_raw.encode("latin-1")
decompressed = zlib.decompress(sheet_bytes)
sheets = json.loads(decompressed)
```

### 公式单元格

`lakesheet` 中 `{'class': 'formula', 'value': ...}` 类型的单元格使用计算后的 `value` 渲染，而非原始 JSON。

### 加密内容

`lockedtext` 卡片使用 AES-256-GCM 客户端加密，密钥**不在** lakebook 导出中。如需访问，请在语雀 App 中解锁后重新导出。

## 限制

- 加密的 `lockedtext` 内容无法解密（密钥不在导出中）
- `lakesheet` 合并表头在 Markdown 中拆分显示（Markdown 不支持单元格合并）
- OSS 附件下载链接有过期时间，建议尽快转换
- 不支持语雀内部跨知识库引用
- 幻灯片文档暂不支持转换为 PPT 格式

## 致谢

- 原始项目：[PZh101/YuqueExportToMarkdown](https://github.com/PZh101/YuqueExportToMarkdown)

## License

Apache-2.0 — 详见 [LICENSE](LICENSE) 文件
