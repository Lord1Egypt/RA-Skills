## 技能文档

### 基本信息
- 技能名: `notebook-builder`
- 创建人: @beauren
- 版本: v1.1.0
- 许可证: MIT
- 更新时间: 2026-03-06

### 适用场景
- 分段式创建教学 Jupyter Notebook（避免一次性生成过大内容导致截断）
- 修改、维护已有的 .ipynb 文件（增删改查 cell）
- 生成带有哈希判题系统的编程练习 notebook（答案不以明文存储）
- 将本地图片以 base64 编码嵌入 notebook 的 Markdown 或 Code cell
- 合并多个 notebook 文件为一个完整课件
- 将 notebook 导出为纯 Python 脚本 (.py)
- 自动生成目录、Cell 标签分组、Cell 重排序
- 创建结构化的技术教程、学习笔记、课程课件

### 前置条件
- Python 3.6+
- 无第三方依赖（仅使用 json, base64, hashlib, pathlib 等标准库）

### 使用示例
```
"帮我分段生成一个 PyTorch 教学 notebook，包含讲解、实验代码和判题"
"修改现有 notebook，在第 5 个 cell 后插入一段新内容"
"给这个 notebook 加上带判题功能的考核部分"
"把这张图片嵌入到 notebook 的 Markdown cell 中"
"把这 3 个 notebook 合并成一个"
"把这个 notebook 导出为 .py 文件"
"给这个长 notebook 加一个目录"
```

### 注意事项
⚠️ 图片 base64 嵌入会显著增大 .ipynb 文件体积，建议压缩图片后再嵌入
⚠️ 判题哈希不可逆但可见，适合教学场景而非高安全性考试
⚠️ 分段生成时每段追加后都应保存，防止进度丢失


### 已知问题
- [ ] 暂不支持从 URL 远程加载图片嵌入
- [ ] 判题系统仅支持精确匹配，暂不支持模糊匹配或数值容差

### 相关技能
- `pdf`: 如需将 notebook 导出为 PDF 可配合使用
