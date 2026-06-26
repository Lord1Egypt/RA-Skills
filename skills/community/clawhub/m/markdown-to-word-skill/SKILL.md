# Markdown转Word技能

## 描述
使用Python的`python-docx`、`markdown`、`beautifulsoup4`库将Markdown文件转换为格式良好的Word文档。支持标题、段落、列表、表格、代码块、图片等Markdown元素的转换。

## 激活条件
当用户需要将Markdown文件转换为Word文档时激活此技能。

## 技能目录结构
```
markdown-to-word-skill/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 详细文档
├── requirements.txt            # Python依赖
├── install.sh                  # 安装脚本
├── quick_start.sh              # 快速开始脚本
├── scripts/
│   ├── md2docx.py              # 主转换脚本
│   ├── md2docx_batch.py        # 批量转换脚本
│   ├── md2docx_with_images.py  # 带图片转换脚本
│   └── template_processor.py   # 模板处理器
├── templates/
│   ├── academic.docx           # 学术论文模板
│   ├── business.docx           # 商业报告模板
│   └── technical.docx          # 技术文档模板
├── examples/
│   ├── sample.md               # 示例Markdown文件
│   ├── sample_output.docx      # 示例输出
│   └── test_images/            # 测试图片目录
└── config/
    └── styles.json             # 样式配置
```

## 核心功能

### 1. 基础转换
- 将Markdown文件转换为Word文档
- 支持所有基本Markdown语法
- 保持文档结构和格式

### 2. 高级功能
- **图片处理**：自动插入图片并调整大小
- **表格转换**：将Markdown表格转换为Word表格
- **代码块**：保留代码格式和语法高亮
- **数学公式**：支持LaTeX数学公式
- **自定义样式**：应用预定义或自定义样式

### 3. 批量处理
- 批量转换多个Markdown文件
- 支持文件夹递归处理
- 生成进度报告

### 4. 模板系统
- 使用预定义模板（学术、商业、技术）
- 自定义模板支持
- 自动应用样式

## 依赖安装

### Python依赖
```bash
pip install python-docx markdown beautifulsoup4 pillow
```

### 系统依赖（可选）
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip python3-venv

# macOS
brew install python3
```

## 使用方法

### 1. 基本转换
```bash
python scripts/md2docx.py --input sample.md --output sample.docx
```

### 2. 使用模板
```bash
python scripts/md2docx.py --input sample.md --output sample.docx --template templates/academic.docx
```

### 3. 批量转换
```bash
python scripts/md2docx_batch.py --input-dir ./markdown_files --output-dir ./word_docs
```

### 4. 带图片转换
```bash
python scripts/md2docx_with_images.py --input sample.md --output sample.docx --image-dir ./images
```

## 脚本说明

### md2docx.py - 主转换脚本
```python
"""
Markdown转Word主转换脚本
支持：
- 标题（H1-H6）
- 段落和文本格式（粗体、斜体、删除线）
- 列表（有序、无序）
- 表格
- 代码块
- 引用块
- 水平线
- 图片
- 链接
"""

# 基本用法
python md2docx.py --input input.md --output output.docx

# 高级选项
python md2docx.py --input input.md --output output.docx \
  --template academic.docx \
  --style-title "Title" \
  --style-heading1 "Heading 1" \
  --style-heading2 "Heading 2" \
  --style-paragraph "Normal" \
  --style-code "Code" \
  --style-quote "Quote"
```

### md2docx_batch.py - 批量转换脚本
```python
"""
批量转换脚本
支持：
- 批量处理文件夹中的所有Markdown文件
- 递归处理子文件夹
- 保持目录结构
- 生成转换报告
"""

# 基本用法
python md2docx_batch.py --input-dir ./docs --output-dir ./word_docs

# 高级选项
python md2docx_batch.py --input-dir ./docs --output-dir ./word_docs \
  --recursive \
  --template technical.docx \
  --report report.json \
  --skip-existing
```

### md2docx_with_images.py - 带图片转换脚本
```python
"""
带图片处理的转换脚本
支持：
- 自动查找并插入图片
- 图片大小调整
- 图片居中/对齐
- 图片标题
- 相对路径支持
"""

# 基本用法
python md2docx_with_images.py --input article.md --output article.docx --image-dir ./images

# 高级选项
python md2docx_with_images.py --input article.md --output article.docx \
  --image-dir ./images \
  --image-width 500 \
  --image-height 300 \
  --image-quality 85 \
  --add-captions
```

## 支持的Markdown元素

### 1. 标题
```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 2. 文本格式
```markdown
**粗体文本**
*斜体文本*
~~删除线文本~~
```

### 3. 列表
```markdown
- 无序列表项1
- 无序列表项2

1. 有序列表项1
2. 有序列表项2
```

### 4. 表格
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |
```

### 5. 代码块
````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### 6. 图片
```markdown
![图片描述](image.jpg)
```

### 7. 链接
```markdown
[链接文本](https://example.com)
```

### 8. 引用
```markdown
> 这是一段引用文字
> 可以有多行
```

### 9. 水平线
```markdown
---
```

## 样式配置

### 默认样式映射
```json
{
  "h1": "Heading 1",
  "h2": "Heading 2", 
  "h3": "Heading 3",
  "h4": "Heading 4",
  "h5": "Heading 5",
  "h6": "Heading 6",
  "p": "Normal",
  "code": "Code",
  "quote": "Quote",
  "table": "Table Grid",
  "image": "Image Caption"
}
```

### 自定义样式
创建 `config/styles.json`：
```json
{
  "styles": {
    "title": "自定义标题",
    "heading1": "自定义标题1",
    "heading2": "自定义标题2",
    "paragraph": "自定义段落",
    "code": "代码样式",
    "quote": "引用样式"
  },
  "font": {
    "title": {"name": "微软雅黑", "size": 24, "bold": true},
    "heading1": {"name": "微软雅黑", "size": 18, "bold": true},
    "paragraph": {"name": "宋体", "size": 12}
  },
  "colors": {
    "title": "2E74B5",
    "heading1": "2E74B5",
    "code_background": "F2F2F2"
  }
}
```

## 模板系统

### 预定义模板
1. **academic.docx** - 学术论文模板
   - 符合学术论文格式
   - 包含摘要、关键词、参考文献
   - 支持章节编号

2. **business.docx** - 商业报告模板
   - 专业商业风格
   - 包含公司Logo、页眉页脚
   - 图表和表格样式

3. **technical.docx** - 技术文档模板
   - 代码友好格式
   - 技术图表支持
   - API文档样式

### 创建自定义模板
1. 在Word中创建模板文档
2. 定义样式（标题、段落、代码等）
3. 保存为 `.docx` 文件到 `templates/` 目录
4. 使用 `--template` 参数指定

## 安装脚本

### install.sh
```bash
#!/bin/bash
# Markdown转Word技能安装脚本

echo "安装Markdown转Word技能..."

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
pip install python-docx markdown beautifulsoup4 pillow

# 创建必要目录
mkdir -p templates examples test_images config

echo "✅ 安装完成！"
echo "激活虚拟环境：source venv/bin/activate"
echo "运行测试：python scripts/md2docx.py --input examples/sample.md --output examples/sample_output.docx"
```

### quick_start.sh
```bash
#!/bin/bash
# 快速开始脚本

echo "Markdown转Word技能快速开始..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -q python-docx markdown beautifulsoup4 pillow

# 运行示例
echo "运行示例转换..."
python scripts/md2docx.py --input examples/sample.md --output examples/sample_output.docx

if [ $? -eq 0 ]; then
    echo "✅ 示例转换成功！"
    echo "输出文件：examples/sample_output.docx"
else
    echo "❌ 转换失败，请检查错误信息"
fi
```

## 示例文件

### sample.md
```markdown
# 示例文档

这是一个Markdown转Word的示例文档。

## 章节1：介绍

这是第一章节的内容。**粗体文本**和*斜体文本*都可以正常转换。

### 子章节1.1

这是一个子章节。

## 章节2：列表示例

### 无序列表
- 项目1
- 项目2
  - 子项目2.1
  - 子项目2.2
- 项目3

### 有序列表
1. 第一步
2. 第二步
3. 第三步

## 章节3：表格示例

| 姓名 | 年龄 | 职业 |
|------|------|------|
| 张三 | 25   | 工程师 |
| 李四 | 30   | 设计师 |
| 王五 | 28   | 产品经理 |

## 章节4：代码示例

```python
def calculate_sum(a, b):
    """计算两个数的和"""
    return a + b

result = calculate_sum(10, 20)
print(f"结果: {result}")
```

## 章节5：引用示例

> 这是引用内容
> 可以有多行
> 
> — 引用来源

## 章节6：图片示例

![示例图片](test_images/sample.jpg)

---

文档结束。
```

## 故障排除

### 常见问题

#### 1. 缺少依赖
```
ModuleNotFoundError: No module named 'docx'
```
**解决方案**：
```bash
pip install python-docx
```

#### 2. 图片路径错误
```
FileNotFoundError: [Errno 2] No such file or directory: 'image.jpg'
```
**解决方案**：
- 使用绝对路径
- 使用 `--image-dir` 参数指定图片目录
- 确保图片文件存在

#### 3. 样式不存在
```
KeyError: 'Heading 1'
```
**解决方案**：
- 检查模板文件中的样式名称
- 使用 `--list-styles` 查看可用样式
- 创建自定义样式配置

#### 4. 编码问题
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```
**解决方案**：
```bash
python md2docx.py --input input.md --output output.docx --encoding utf-8-sig
```

### 调试模式
```bash
python md2docx.py --input input.md --output output.docx --debug
```

## 在OpenClaw中的使用

### 作为独立技能
```bash
# 转换单个文件
exec("cd /path/to/markdown-to-word-skill && python scripts/md2docx.py --input document.md --output document.docx")

# 批量转换
exec("cd /path/to/markdown-to-word-skill && python scripts/md2docx_batch.py --input-dir ./docs --output-dir ./word_docs")
```

### 在技能中集成
```python
def convert_markdown_to_word(md_file, docx_file, template=None):
    """转换Markdown到Word"""
    import subprocess
    
    cmd = ["python", "scripts/md2docx.py", "--input", md_file, "--output", docx_file]
    
    if template:
        cmd.extend(["--template", template])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"success": True, "output": docx_file}
    else:
        return {"success": False, "error": result.stderr}
```

## 性能优化

### 1. 批量处理优化
- 使用多进程处理大文件
- 内存优化
- 缓存已解析的模板

### 2. 图片处理优化
- 图片压缩
- 缩略图生成
- 并行处理

### 3. 样式缓存
- 缓存样式定义
- 减少重复操作
- 提高转换速度

## 扩展功能

### 1. 自定义转换器
```python
from md2docx import MarkdownToDocx

class CustomConverter(MarkdownToDocx):
    def convert_custom_element(self, element):
        """处理自定义Markdown元素"""
        pass
```

### 2. 插件系统
```python
# 创建插件
class ImagePlugin:
    def process(self, converter, element):
        """处理图片元素"""
        pass

# 注册插件
converter.register_plugin(ImagePlugin())
```

### 3. Web API
```python
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    md_content = request.form['markdown']
    # 转换逻辑
    return send_file('output.docx')
```

## 更新日志

### v1.0.0 (2026-03-02)
- 初始版本发布
- 支持基本Markdown元素转换
- 添加图片处理功能
- 实现批量转换
- 添加模板系统

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证
MIT License

## 联系方式
- 问题反馈：创建GitHub Issue
- 功能建议：提交Pull Request
- 文档改进：编辑README.md

---

**技能创建时间**：2026-03-02 10:12 GMT+8
**创建者**：OpenClaw AI Assistant
**版本**：1.0.0