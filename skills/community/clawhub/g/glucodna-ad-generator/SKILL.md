# GlucoDNA 广告图生成器

生成 GlucoDNA 基因护肾的中文广告图片，包含产品图。

## 触发词
- "生成GlucoDNA广告"
- "GlucoDNA 广告图"
- "glucodna ad"

## 前置依赖
- Gemini API Key（配置于 TOOLS.md 或环境变量）
- Python 包: `pip install google-genai requests`

## 工作流
1. 读取 `knowledge/products/GlucoDNA.md` 获取产品信息
2. 用 Gemini 3 Pro 生成 1024×1024 广告图
3. 保存到桌面

## 关键代码
```python
python3 workspace/skills/glucodna-ad-skill/generate.py
```
