# 📄 official-doc - 公文格式转换

## 技能信息

### 基本信息
| 属性 | 说明 |
|------|------|
| **名称** | official-doc |
| **中文名称** | 公文格式转换 |
| **版本** | 1.1.0 |
| **作者** | EdwardWason |
| **许可证** | MIT |
| **主页** | https://github.com/EdwardWason/official-doc |

### 功能描述
将 Markdown 文档转换为符合 **GB/T 9704-2012** 党政机关公文格式的 Word 文档。专注排版格式转换，不添加红头、版记、落款等公文装饰要素。

### 适用场景
- AI Agent 生成公文格式报告
- 定时任务自动生成工作简报、周报、月报
- Markdown 文档批量转换为标准公文格式
- 行业研报格式标准化输出

### v1.1.0 新增功能
- 引入 markdown-it-py 解析器，支持多行段落、嵌套列表
- `#` 标题智能判断：单个视为大标题（居中不加序号），多个视为一级标题（加序号）
- 首行缩进精确对齐国标（640 twips = 2个三号汉字宽度）
- 新增表格、图片、超链接、代码块、嵌套列表支持
- 加粗文本自动转为黑体，斜体文本自动转为楷体

---

## 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `md_content` | string | ✅ | Markdown 格式的文本内容 |
| `output_path` | string | ✅ | 输出 Word 文件路径（.docx） |

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
| 三级标题 | `###` | 楷体_GB2312 | 三号 |
| 四级标题 | `####` | 仿宋_GB2312 | 三号 |
| 正文 | 普通文本 | 仿宋_GB2312 | 三号 |
| 加粗文本 | `**text**` | 黑体 | 三号 |
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
| 加粗 `**text**` | 黑体 |
| 斜体 `*text*` | 楷体 |
| 代码块 ` ``` ` | 仿宋小四号 |
| 水平线 `---` | 忽略 |

---

## 依赖要求

| 依赖 | 版本 |
|------|------|
| Python | >= 3.8 |
| python-docx | >= 1.1.0 |
| markdown-it-py | >= 3.0.0 |

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
