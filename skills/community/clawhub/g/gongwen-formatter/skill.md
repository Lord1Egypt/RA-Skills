---
slug: gongwen-formatter
name: gongwen-formatter
displayName: Gongwen Formatter 公文格式转换
name_cn: 公文格式转换
version: 1.1.9
author: EdwardWason
license: MIT
homepage: https://github.com/EdwardWason/official-doc
description: 公文格式转换 — 将 Markdown 转换为符合 GB/T 9704-2012 党政机关公文格式的 Word 文件。可选能力：远程图片下载（仅 http/https/data:image，可通过 download_images=False 关闭）。Do NOT：不做文体识别、不添加红头/版记/落款、不做内容审核。
summary: 将 Markdown 转换为符合 GB/T 9704-2012 标准的党政机关公文格式 Word 文件。
allowed-tools:
  - filesystem (write .docx output)
  - net.http (GET image download, http/https only, toggleable via download_images=False)
triggers:
  - 公文格式转换
  - 转换公文格式
---

# 📄 official-doc - 公文格式转换

## 技能信息

### 基本信息
| 属性 | 说明 |
|------|------|
| **名称** | official-doc |
| **中文名称** | 公文格式转换 |
| **版本** | 1.1.9 |
| **作者** | EdwardWason |
| **许可证** | MIT |
| **主页** | https://github.com/EdwardWason/official-doc |

### 触发词
- **公文格式转换**
- **转换公文格式**

### 功能描述
将 Markdown 文档转换为符合 **GB/T 9704-2012** 党政机关公文格式的 Word 文档。专注排版格式转换，不添加红头、版记、落款等公文装饰要素。

### 适用场景
- AI Agent 生成公文格式报告
- 定时任务自动生成工作简报、周报、月报
- Markdown 文档批量转换为标准公文格式
- 行业研报格式标准化输出

### Do NOT（超出范围）
- ❌ **不做文体识别**：不区分通知/通报/报告/请示等公文文种，统一按 Markdown 结构转换
- ❌ **不添加公文装饰要素**：不生成红头、版记、落款、签发人、密级标识等
- ❌ **不做内容审核**：不审查内容合规性、不校验公文要素完整性
- ❌ **不做双向转换**：仅支持 Markdown → Word 单向，不支持 Word → Markdown 反向
- ❌ **不读取本地敏感文件**：不读取 memory/profile/credentials 等任何用户数据

### v1.1.0 新增功能
- 引入 markdown-it-py 解析器，支持多行段落、嵌套列表
- `#` 标题智能判断：单个视为大标题（居中不加序号），多个视为一级标题（加序号）
- 首行缩进精确对齐国标（640 twips = 2个三号汉字宽度）
- 新增表格、图片、超链接、代码块、嵌套列表支持
- 加粗文本自动转为楷体加粗，斜体文本自动转为楷体

### v1.1.2 安全升级（响应 ClawHub SkillSpector 审计）
- `download_image()` 增加 URL scheme 白名单（仅 `http://`/`https://`/`data:image`），防止 SSRF
- `md_to_docx()` 新增 `download_images=True` 参数，受限网络环境可设为 `False` 完全关闭网络请求
- `_handle_standalone_image()` 关闭图片下载时以 `[图片: alt]` 文字占位替代
- `requirements.txt` 改用 `~=` 兼容版本锁定（python-docx~=1.1.0、markdown-it-py~=3.0.0）
- README 中英文版增加 "图片下载网络请求说明 / Network Access Disclosure" 用户警告段落

### v1.1.3 修复（响应 v1.1.2 后 SkillSpector 二次审计）
- 修复 v1.1.2 漏改：README/skill.md/skill.json 中残留的 `>=` 全部改为 `~=`（依赖版本一致性）
- frontmatter 增加 `allowed-tools` 字段，声明 filesystem（写 .docx）和 net.http（图片下载，可关闭）两项权限
- 7 项 findings 中：2 项真实漏改（本次修复）、3 项 stale（已修复但被重复扫描，本次通过 allowed-tools 增强声明）、2 项过度修改（保留现有设计，不采纳）

### v1.1.4 格式修复（对齐公文规范）
- **加粗句（`**text**`）修复**：由"黑体不加粗"改为"楷体_GB2312 加粗"——符合公文段首"一是/二是"句式标准格式
- **三级标题（`###`）修复**：由"楷体不加粗"改为"楷体_GB2312 加粗"——符合 GB/T 9704 二级标题（（一））楷体加粗规范
- 黑体标题（`#`/`##`）、正文仿宋、斜体楷体等保持不变

### v1.1.8 格式增强（间隔号序号规范化为公文标准序号）
- **「一 · 源头」→「一、源头」**：识别到间隔号体例时自动改写为公文标准序号，
  `##` →「一、」（阿拉伯数字自动转中文数字），`###` →「（五）」
- 结构性标题（「结语 ·」「附一 ·」）保持原样不套序号

### v1.1.7 格式修复（序号去重扩展·间隔号体例）
- **间隔号序号去重**：新增「一 · 源头」「1 · 标题」间隔号体例识别，
  以及「结语 ·」「附一 ·」结构性标题识别，避免自动编号与原文序号重复
- 涌现写作交付成稿常用间隔号体例，此前会产生「二、一·源头」这类重复序号

### v1.1.6 格式修复（段落按源码行拆分）
- **连续非空行不再合并**：连续的非空行（软换行 `softbreak`）还原为独立段落，
  解决"甲方：/住所：/法定代表人："这类一行一要素文本被挤在同一段的问题
- 拆分后的每段独立应用两端对齐 + 固定行距 + 首行缩进 2 字（640 twips）
- 本版一并纳入此前仅写入代码 docstring 的 v1.1.5 标题层级重定义（`#` 大标题 / `##` 一级标题 / `###` 楷体加粗 / `####` 仿宋加粗 + 序号去重）

---

## 权限声明

本技能执行过程中涉及的系统能力（用户须知）：

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| **网络访问** | ✅ 仅 http/https 图片下载 | 默认开启；可通过 `download_images=False` 关闭；URL scheme 白名单防止 SSRF |
| **文件读写** | ✅ 仅写入输出 .docx 和临时图片缓存 | 临时图片下载后立即 `os.unlink` 删除；不读取用户其他文件 |
| **环境变量** | ❌ 不读取 | 不依赖任何环境变量，无凭证收集 |
| **subprocess 调用** | ❌ 不调用 | 纯 Python 实现，不执行 shell 命令 |
| **外部 API 调用** | ❌ 不调用 | 不向任何外部 API 推送数据 |

**最小权限原则**：本技能仅做 Markdown→Word 格式转换，不涉及任何外部数据上传、凭证收集或子进程调用。

---

## 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `md_content` | string | ✅ | Markdown 格式的文本内容 |
| `output_path` | string | ✅ | 输出 Word 文件路径（.docx） |
| `download_images` | bool | ❌ | 是否下载远程图片并嵌入 Word，默认 `True`；受限网络环境设为 `False` 跳过网络请求 |

---

## 输出结果

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 转换是否成功 |
| `output_path` | string | 输出文件路径 |

---

## 使用示例

### 基本使用
```python
from official_doc import md_to_docx

md_content = """# 工作简报

## 一、上周工作总结

本周完成了系统升级任务。

### （一）主要工作
1. 服务器部署
2. 数据迁移
3. 测试验证

### （二）下周计划
继续推进优化工作。
"""

success = md_to_docx(md_content, "工作简报_公文格式.docx")
print("转换成功" if success else "转换失败")
```

### 含表格和图片
```python
from official_doc import md_to_docx

md_content = """# 项目进度表

## 工作进展

| 项目名称 | 负责人 | 进度 | 备注 |
|----------|--------|------|------|
| A项目 | 张三 | 80% | 正常 |
| B项目 | 李四 | 60% | 需加速 |

![架构图](https://example.com/arch.png)

详细说明请参考[官方文档](https://example.com)。
"""

md_to_docx(md_content, "进度表_公文格式.docx")
```

### AI Agent 集成
```python
from official_doc import md_to_docx

class OfficialDocSkill:
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

### 定时任务
```python
import schedule
import time
from official_doc import md_to_docx

def generate_report():
    content = generate_report_content()
    today = time.strftime("%Y-%m-%d")
    md_to_docx(content, f"工作简报_{today}_公文格式.docx")

schedule.every().monday.at("09:00").do(generate_report)
```

---

## 格式规范

### 页面设置
| 设置项 | 规范值 |
|--------|--------|
| 上边距 | 3.7cm |
| 下边距 | 3.5cm |
| 左边距 | 2.8cm |
| 右边距 | 2.6cm |
| 行间距 | 固定值 26 磅 |
| 首行缩进 | 2字符（640 twips） |

### 字体设置
| 元素 | Markdown | 字体 | 字号 |
|------|----------|------|------|
| 大标题（单个#） | `#` | 方正小标宋简体 | 二号 |
| 一级标题（多个#） | `#` | 黑体 | 三号 |
| 二级标题 | `##` | 黑体 | 三号 |
| 三级标题 | `###` | 楷体_GB2312 加粗 | 三号 |
| 四级标题 | `####` | 仿宋_GB2312 | 三号 |
| 正文 | 普通文本 | 仿宋_GB2312 | 三号 |
| 加粗文本 | `**text**` | 楷体_GB2312 加粗 | 三号 |
| 斜体文本 | `*text*` | 楷体_GB2312 | 三号 |
| 链接 | `[text](url)` | 仿宋_GB2312 蓝色下划线 | 三号 |
| 表格表头 | `| 表头 |` | 黑体 | 三号 |
| 表格内容 | `| 内容 |` | 仿宋_GB2312 | 三号 |
| 代码块 | ` ``` ` | 仿宋_GB2312 | 小四号 |
| 页码 | - | 宋体 | 四号 |

### 标题编号规则
| 层级 | 格式示例 | 说明 |
|------|----------|------|
| 大标题 | 公文标题 | 单个#标题居中，不加序号 |
| 一级标题 | 一、章节名称 | 多个#标题自动加序号 |
| 二级标题 | 一、章节名称 | ## 标题自动加序号 |
| 三级标题 | （一）小节名称 | ### 标题加中文括号序号 |
| 四级标题 | 正文格式 | #### 标题不加序号 |

### 支持的 Markdown 元素
| 元素 | 转换效果 |
|------|----------|
| 标题 `# / ## / ### / ####` | 智能层级判断 + 自动编号 |
| 段落 | 正文仿宋三号，首行缩进2字符 |
| 有序列表 `1. 2. 3.` | 自动编号，支持嵌套 |
| 无序列表 `- / *` | 圆点标记，支持嵌套 |
| 表格 `| ... |` | Word表格，表头黑体 |
| 图片 `![alt](url)` | 居中图片 + 图注 |
| 链接 `[text](url)` | 蓝色下划线超链接 |
| 加粗 `**text**` | 楷体加粗 |
| 斜体 `*text*` | 楷体 |
| 代码块 ` ``` ` | 仿宋小四号 |
| 水平线 `---` | 忽略 |

---

## 依赖要求

| 依赖 | 版本 |
|------|------|
| Python | >= 3.8 |
| python-docx | ~= 1.1.0 |
| markdown-it-py | ~= 3.0.0 |

---

## 支持平台

- ✅ Windows 10/11
- ✅ Linux
- ✅ macOS

---

## 项目链接

- GitHub: https://github.com/EdwardWason/official-doc
- Release: https://github.com/EdwardWason/official-doc/releases
- README: https://github.com/EdwardWason/official-doc/blob/main/README.md
