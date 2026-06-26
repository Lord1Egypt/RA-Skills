# md2docx 技能

## 描述
将Markdown文件转换为Word文档（.docx格式），采用两阶段转换方案：
1. Pandoc转换Markdown为Word文档
2. python-docx后处理设置字体和表格边框
支持完整的Markdown语法包括标题、列表、表格、代码块等。

## 功能
- 转换Markdown到Word文档（两阶段处理）
- 保持格式完整性
- 支持所有标准Markdown语法
- 自动设置中文字体（Microsoft YaHei/SimSun）
- 自动添加表格边框
- 可自定义输出样式

## 使用方法
```
python tools/md2docx.py input.md output.docx
```

或者

```python
from tools.md2docx import convert_md_to_docx
convert_md_to_docx('input.md', 'output.docx')
```

## 参数
- `input_file`: 输入的Markdown文件路径
- `output_file`: 输出的Word文档路径
- `template`: (可选) Word模板文件路径
- `reference_docx`: (可选) 参考文档以设置样式

## 特性
- 支持H1-H6标题层级
- 支持有序和无序列表
- 支持表格渲染（自动添加边框）
- 支持代码块高亮
- 支持引用块
- 支持图片插入
- 支持链接和强调文本
- 中文字体优化（Microsoft YaHei/SimSun）
- 表格边框自动设置

## 依赖
- Pandoc (>= 2.0)
- python-docx (>= 1.2.0)

## 版本
1.0.6

## 更新日志 (Changelog)
### v1.0.6（2026-03-26）
- 代码规范化：完整 docstring + 类型注解 + PEP 8 规范
- 错误提示优化：友好的错误信息 + 解决建议
- 测试完善：增加测试用例 + 边界测试
- 字体修复：中文字体自动设置优化
- 表格边框优化：自动添加表格边框

### v1.0.5
- 引入两阶段转换方案：Pandoc + python-docx后处理
- 添加中文字体设置（Microsoft YaHei/SimSun）
- 添加表格边框自动设置功能
- 修复了文档样式问题
- 优化了Word文档输出格式

### v1.0.0
- 初始版本发布
- 基础Markdown到Word转换功能

## 注意事项
- 确保系统已安装Pandoc (>= 2.0)
- 输入文件必须为UTF-8编码
- 支持的Markdown语法：标题、列表、表格、代码块、引用、链接、强调等
- 对于复杂的文档样式，建议使用自定义Word模板