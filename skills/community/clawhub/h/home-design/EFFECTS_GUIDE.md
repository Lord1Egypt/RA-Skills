# 效果图生成使用指南

本指南介绍如何使用 AI 生成装修房间效果图。

---

## 🎯 功能概述

本技能支持生成以下房间的效果图：

- ✅ 客厅
- ✅ 卧室
- ✅ 儿童房
- ✅ 书房
- ✅ 餐厅
- ✅ 厨房
- ✅ 卫生间
- ✅ 玄关

支持的装修风格：
- 现代简约、北欧风格、新中式、轻奢风格
- 日式风格、美式风格、工业风格、法式风格

---

## 📋 使用流程

### 步骤 1：生成提示词

```bash
cd ~/.openclaw/skills/home-design

python scripts/generate_room_prompts.py \
  --style "现代简约" \
  --living-room "8.6㎡" \
  --bedroom "14.3㎡" \
  --kids-room "10.1㎡" \
  --study "4.9㎡" \
  --dining "9.4㎡" \
  --kitchen "5.5㎡" \
  --bathroom "2.4㎡" \
  --entrance "3㎡" \
  --output /tmp/prompts.json
```

输出：`prompts.json` 包含所有房间的 AI 绘画提示词。

### 步骤 2：选择 AI 后端

#### 选项 A：本地 Stable Diffusion（推荐）

**优点**：
- 免费、无限制
- 可自定义模型
- 生成速度快

**要求**：
- 安装 Stable Diffusion WebUI
- 显卡推荐：NVIDIA 8GB+ VRAM

**配置**：
```json
{
  "url": "http://127.0.0.1:7860"
}
```

**启动 SD WebUI**：
```bash
cd stable-diffusion-webui
./webui.sh  # Linux/Mac
webui.bat   # Windows
```

#### 选项 B：DALL-E 3 API

**优点**：
- 质量高
- 无需本地部署

**缺点**：
- 付费（约 $0.04/张）
- 需要 OpenAI API Key

**配置**：
```json
{
  "api_key": "sk-xxx"
}
```

#### 选项 C：LiblibAI (哩布哩布)

**优点**：
- 国内访问快
- 有免费额度
- 模型丰富

**缺点**：
- 需要注册账号

**配置**：
```json
{
  "api_key": "your_api_key",
  "model_id": "realisticVisionV60B1_v51VAE"
}
```

### 步骤 3：生成效果图

```bash
python scripts/generate_effect.py \
  --prompts /tmp/prompts.json \
  --output /tmp/effects \
  --backend sd_webui \
  --config sd_config.json \
  --rooms 客厅 卧室 儿童房 书房
```

**参数说明**：
- `--prompts`: 提示词 JSON 文件
- `--output`: 输出目录
- `--backend`: AI 后端 (sd_webui/dalle3/liblib)
- `--config`: API 配置文件
- `--rooms`: 可选，指定要生成的房间

### 步骤 4：查看结果

生成完成后，输出目录包含：
- `客厅_20260321_013000.png` - 效果图文件
- `generation_report.json` - 生成报告

---

## 🎨 提示词优化

### 高质量提示词要素

```text
professional interior design photography of a [房间]
style: [风格关键词]
size: [房间尺寸]
color scheme: [配色方案]
materials: [材料]
furniture: [家具]
decor: [装饰]
features: [特色]
lighting: [灯光]
photorealistic, 8k resolution
architectural digest style
professional lighting
interior design magazine quality
wide angle view
depth of field
natural lighting
highly detailed
```

### 负面提示词

```text
blurry, low quality, distorted, deformed, ugly, 
bad anatomy, disfigured, poorly drawn, 
bad proportions, cluttered, messy, 
dark, poorly lit, amateur, low resolution
```

### 风格关键词参考

| 风格 | 关键词 |
|------|--------|
| 现代简约 | modern minimalist, clean lines, uncluttered, functional |
| 北欧风格 | nordic, scandinavian, cozy, hygge, bright |
| 新中式 | new chinese, oriental, zen, elegant, traditional modern |
| 轻奢风格 | light luxury, elegant, sophisticated, refined |
| 日式风格 | japanese, zen, minimalist, natural, serene |
| 美式风格 | american, comfortable, warm, traditional, cozy |
| 工业风格 | industrial, urban, raw, edgy, loft |
| 法式风格 | french, romantic, elegant, ornate, charming |

---

## 💡 使用技巧

### 1. 批量生成

生成所有房间：
```bash
python scripts/generate_effect.py \
  --prompts prompts.json \
  --output ./effects \
  --backend sd_webui
```

生成指定房间：
```bash
python scripts/generate_effect.py \
  --prompts prompts.json \
  --output ./effects \
  --backend sd_webui \
  --rooms 客厅 卧室 儿童房
```

### 2. 调整参数

编辑提示词 JSON 文件中的参数：
```json
{
  "parameters": {
    "width": 1024,
    "height": 768,
    "steps": 30,
    "cfg_scale": 7,
    "seed": -1
  }
}
```

- `width/height`: 分辨率（建议 1024×768 或 1280×960）
- `steps`: 步数（20-40，越高细节越好但越慢）
- `cfg_scale`: 提示词相关性（5-9，推荐 7）
- `seed`: 随机种子（-1 为随机）

### 3. 模型选择

**推荐模型**：
- `realisticVisionV60B1_v51VAE` - 写实风格
- `architectureRealistic_v20` - 建筑室内
- `interiorDesign_v10` - 室内设计专用

### 4. 使用 ControlNet（高级）

如果有户型图，可以使用 ControlNet 精确控制布局：

```bash
# 需要 SD WebUI 安装 ControlNet 扩展
# 在 WebUI 中启用 ControlNet
# 上传户型图作为参考
```

---

## 🔧 故障排除

### 问题 1：SD WebUI 连接失败

**检查**：
```bash
curl http://127.0.0.1:7860/sdapi/v1/cmd-flags
```

**解决**：
- 确保 SD WebUI 正在运行
- 检查端口是否正确（默认 7860）
- 检查防火墙设置

### 问题 2：生成图像质量差

**解决**：
- 增加 steps 到 30-40
- 使用更好的模型（如 realisticVision）
- 优化提示词，增加细节描述
- 调整 cfg_scale 到 7-8

### 问题 3：生成速度慢

**解决**：
- 降低分辨率（如 768×576）
- 减少 steps（20-25）
- 使用 SDXL Turbo 等快速模型
- 升级显卡

### 问题 4：API Key 无效

**解决**：
- 检查 API Key 是否正确
- 检查账户余额
- 确认 API 权限

---

##  成本估算

### Stable Diffusion（本地）
- 软件：免费
- 电费：约 0.5 元/小时
- 生成 8 个房间：约 10-20 分钟
- **总成本**：约 1-2 元

### DALL-E 3
- 单价：$0.04/张（1024×768）
- 8 个房间：$0.32 ≈ 2.3 元
- **总成本**：约 2-3 元

### LiblibAI
- 免费额度：每日约 10-20 张
- 8 个房间：在免费额度内
- **总成本**：免费

---

## 🎓 在线工具（无需安装）

如果不想安装 SD WebUI，可使用以下在线工具：

1. **LiblibAI** (哩布哩布): https://www.liblib.ai/
   - 注册送积分
   - 中文界面
   - 模型丰富

2. **吐司 TusiArt**: https://tusiart.com/
   - 免费额度
   - 简单易用

3. **SeaArt**: https://www.seaart.ai/
   - 免费使用
   - 功能丰富

4. **Leonardo.ai**: https://leonardo.ai/
   - 每日 150 免费积分
   - 高质量

**使用方法**：
1. 复制提示词 JSON 中的 `positive_prompt`
2. 粘贴到在线工具的 Prompt 框
3. 设置参数（分辨率、步数等）
4. 点击生成

---

## 📝 示例输出

生成报告示例 (`generation_report.json`):

```json
[
  {
    "room": "客厅",
    "style": "现代简约",
    "success": true,
    "filepath": "/tmp/effects/客厅_20260321_013000.png",
    "message": "生成成功"
  },
  {
    "room": "卧室",
    "style": "现代简约",
    "success": true,
    "filepath": "/tmp/effects/卧室_20260321_013015.png",
    "message": "生成成功"
  }
]
```

---

## 🚀 下一步

生成效果图后，可以：

1. **查看效果** - 在输出目录查看 PNG 文件
2. **调整优化** - 根据效果调整提示词重新生成
3. **导出报告** - 将效果图整合到设计方案中
4. **分享展示** - 发送给业主或施工方参考

---

**最后更新**: 2026-03-21  
**版本**: v1.0
