---
name: image-recognize
description: 百度AI识别图片中的物体、场景、文字等内容，需要用户提供本地图片或网络图片，支持Base64编码。支持（题目，文字，图片人脸，植物，动物，表情，素材，商品，玩具，景点，通用识别等）内容识别。用于通用图片内容分类识别，不负责图片生成或编辑
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 图片识别

基于百度AI的通用图片识别能力，可识别多种场景下的图片内容。当用户要求识别图片主体、分类标签、场景内容时触发使用，

## 前置条件，获取api_key
1. 从对话上下文中提取（用户曾提及或粘贴过）
2. 读取环境变量 `BAIDU_API_KEY`
3. 以上均无 → **询问用户**：「请提供千帆 API Key（格式：bce-v3/ALTAK-...）」

## 🎯 功能特点
- **多场景识别**：支持景点、动物、植物、商品、表情、人脸、文字等
- **多种输入格式**：本地图片、网络图片、Base64编码
- **简单易用**：只需一个图片参数，返回识别结果
- **不适用场景**：不适用于图片编辑、OCR精确提取、目标检测定位、身份核验、人脸比对、医学影像分析等

## 📋 使用方法

### 基本参数
- `--image`：图片路径/URL/Base64（必需）,图片大小不能超过4MB，最好控制在1MB以下，否则可能出现识别失败。
- `--similar_count`：返回相似图数量（可选，默认3）

### 使用示例
```bash
# 本地图片
python3 scripts/image_recognize.py --image "/path/to/local/image.jpg"

# 网络图片
python3 scripts/image_recognize.py --image "https://example.com/image.jpg"

# Base64编码
python3 scripts/image_recognize.py --image "base64编码字符串"

# 指定相似图数量
python3 scripts/image_recognize.py --image "/path/to/image.jpg" --similar_count 5
```

## ⚙️ 配置要求
- **Python 3**：需要安装python3
- **百度API Key**：需要在OpenClaw配置中设置BAIDU_API_KEY环境变量

## 📝 输出说明
返回MARKDOWN格式的识别结果，包含：
- 识别结果描述
- 置信度评分
- 相似图片（如启用）
- 分类标签

### 示例输出
```markdown
# 图片识别结果:

## 识别结果: 威尔士柯基
**类型**: 动物
**置信度**: 1(高)

### 简要描述
威尔士柯基个子矮小，骨量适中，胸深。整个身体的侧面轮廓的比例是长度远大于高度。尾巴位置非常低，而且象狐狸尾巴。给人的整体印象是：漂亮、有力的小型犬，速度和耐力都非常好，聪明，结构坚固，但不粗糙。

### 识别摘要
==**威尔士柯基犬是中小型犬，体格结实，体长大于身高，头部似狐狸，耳朵直立，四肢粗短，拥有浑圆臀部，毛色多样，彭布罗克柯基多断尾，卡迪根柯基则有长尾巴**==[1][2][3][4]。

### 详细信息

### 参考资源

1. [威尔士柯基犬](https://baike.baidu.com/item/威尔士柯基犬/84385)
2. [卡迪根威尔士柯基犬](https://baike.baidu.com/item/卡迪根威尔士柯基犬/625957)

```
