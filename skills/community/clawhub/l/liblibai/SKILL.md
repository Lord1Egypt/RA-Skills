---
name: liblibai
description: 使用 LiblibAI API 生成 AI 图像。支持文生图、图生图、Ultra 模型、ComfyUI 工作流和文件上传，适合创意设计、内容创作和视觉项目。
license: MIT
allowed-tools:
  - Read
  - Write
  - Exec
  - WebFetch
  - AskUserQuestion
metadata:
  clawdbot:
    emoji: 🎨
    requires:
      bins: [node, npm]
    install:
      - id: npm
        kind: npm
        pkg: liblibai
        label: 安装 liblibai npm 包
config:
  - name: LIBLIBAI_ACCESS_KEY
    description: LiblibAI API AccessKey（在 https://liblibai.com 账户设置中获取）
    required: true
    example: "AFP8cs3Ip4KsQJr7tmUcWA"
  - name: LIBLIBAI_SECRET_KEY
    description: LiblibAI API SecretKey（与 AccessKey 配对）
    required: true
  - name: LIBLIBAI_BASE_URL
    description: API 端点 URL（默认: https://openapi.liblibai.cloud）
    default: https://openapi.liblibai.cloud
    optional: true

---

# LiblibAI Skill - AI 图像生成

强大的 AI 图像生成工具，基于 LiblibAI（星流）平台。适用于：

- 🎨 **创意设计**：概念图、角色设计、场景插画
- 📱 **内容创作**：社媒配图、文章插图、营销素材
- 🔬 **视觉实验**：风格转换、图像重绘、ControlNet 控制
- 🛠️ **工作流集成**：与其他 OpenClaw 技能组合（如 web_search 找灵感，humanizer 优化提示词）

---

## 快速开始

### 1. 获取 API 凭据

访问 [LiblibAI](https://liblibai.com)：
1. 注册/登录账户
2. 进入「API 管理」或「开发者设置」
3. 创建 AccessKey 和 SecretKey
4. 设置环境变量（推荐）：

```bash
export LIBLIBAI_ACCESS_KEY="your-access-key"
export LIBLIBAI_SECRET_KEY="your-secret-key"
```

或通过 OpenClaw 配置系统设置。

### 2. 基本生成

```bash
# 生成一张 1024x1024 的小狗图片
./skills/liblibai/bin/cli.js text2img -p "一只可爱的小狗，真实照片风格，高清" -W 1024 -H 1024 -s 20

# 查看结果（成功后输出图片 URL）
# 复制 URL 到浏览器即可查看
```

---

## 核心功能

### 文生图 (text2img)

从文本生成图像，支持完整参数控制。

**常用参数：**
```
-p, --prompt <text>        正向提示词（必需）
-n, --negative-prompt <text>  负向提示词（如 "ugly, blurry"）
-W, --width <1024>         图像宽度（建议 512-1536）
-H, --height <1024>        图像高度
-s, --steps <20>           采样步数（10-50，越高越精细）
-c, --cfg-scale <7>        提示词引导系数（1-20）
--sampler <15>             采样方法 ID（15=DPMSolver）
--seed <-1>                随机种子（-1=随机）
-i, --img-count <1>        生成数量（1-4）
-t, --template-uuid <uuid> 参数模板 ID（在 LiblibAI 平台预设）
```

**示例：**
```bash
# 生成插画风格头像
./bin/cli.js text2img -p "anime portrait, 1girl, colorful hair, detailed eyes" -W 768 -H 1024 -s 30 -c 8

# 使用预设模板（需要先在平台创建）
./bin/cli.js text2img -p " landscapes" -t "your-template-uuid"
```

### 图生图 (img2img)

基于现有图像重绘或风格转换。

**特有参数：**
```
-S, --source-image <url|path>  源图 URL 或本地路径（支持自动上传）
-d, --denoising-strength <0.75> 重绘幅度 (0-1, 越高变化越大)
--resize-mode <0>            缩放模式 (0=拉伸, 1=裁剪, 2=填充)
--mask-image <url>           蒙版图（用于局部重绘）
--mask-mode <0>              蒙版模式
--inpaint-area <0|1>         重绘区域 (0=全图, 1=仅蒙版)
```

**示例：**
```bash
# 将照片转为油画风格（自动上传本地文件）
./bin/cli.js img2img -p "oil painting style, Van Gogh" -S ./photo.jpg -d 0.65

# 局部重绘（需要配合蒙版）
./bin/cli.js img2img -p "add a hat" -S original.png --mask-image mask.png --inpaint-area 1
```

### Ultra 模型 (text2img-ultra / img2img-ultra)

更高品质的生成，支持 ControlNet。

**特有参数：**
```
-a, --aspect-ratio <portrait|landscape|square> 宽高比
--controlnet-type <depth|canny|...> ControlNet 类型
--controlnet-image <url>              ControlNet 参考图
```

**示例：**
```bash
# Ultra 文生图 + ControlNet
./bin/cli.js text2img-ultra -p "masterpiece, 1girl" -a portrait --controlnet-type depth --controlnet-image ref.jpg
```

### 文件上传 (upload)

上传本地图片供后续使用。

```bash
# 简单上传
./bin/cli.js upload ./my-image.png

# 自定义文件名
./bin/cli.js upload ./photo.jpg -n "reference"
```

返回的 URL 可用于 img2img 或 ControlNet。

### 异步任务管理

对于耗时较长的任务（ Ultra 模型、复杂工作流）：

```bash
# 提交任务（返回 UUID）
UUID=$(./bin/cli.js submit text2img -p "complex scene")

# 检查状态
./bin/cli.js status $UUID

# 等待完成（自动轮询）
./bin/cli.js wait $UUID --interval 5000 --timeout 600000
```

---

## 典型工作流示例

### 工作流 1：概念设计迭代

```bash
# 1. 生成多个版本的草图（不同种子）
for seed in {1..5}; do
  ./bin/cli.js text2img -p "character design, fantasy warrior" --seed $seed -W 512 -H 512 -s 15
done

# 2. 选择最佳的一张进行风格重绘
./bin/cli.js img2img -p "watercolor painting" -S best-sketch.png -d 0.7

# 3. Ultra 提升细节
./bin/cli.js text2img-ultra -p "high detail, refined" -a portrait --controlnet-type depth -S refined.png
```

### 工作流 2：批量生成营销配图

```bash
# 使用脚本循环生成
for product in "咖啡杯" "笔记本" "耳机"; do
  ./bin/cli.js text2img -p "$product on white background, product photography" -W 1024 -H 1024 -s 25 &
done
wait
```

---

## 故障排除

### 认证失败
```
Error: LiblibAI credentials not found
```
**解决**：确保环境变量已设置。测试：
```bash
echo $LIBLIBAI_ACCESS_KEY
echo $LIBLIBAI_SECRET_KEY
```
如果为空，请在 ~/.zshrc 或当前 shell 中 export。

### 速率限制
返回 429 错误。
**解决**：添加延迟（sleep 2-3 秒）或减少生成频率。

### 模板 UUID 问题
某些高级功能需要平台预设的模板 UUID。
**解决**：登录 LiblibAI 网页版，在「模板」或「工作流」中创建并获取 ID。

### 文件上传失败
```
Error: File size exceeds limit
```
**解决**：确保文件 < 10MB，格式为 PNG/JPG/JPEG/WebP。

### 网络超时
中国用户可能需要代理访问 international API。
**解决**：设置 `LIBLIBAI_BASE_URL` 为国内镜像（如有），或使用稳定网络。

---

## 与其他技能集成

### 结合 web_search 获取灵感
```bash
# 搜索当前流行设计风格
web_search "2025 UI design trends"

# 用搜索结果作为提示词
./bin/cli.js text2img -p "modern UI design, dark theme, glassmorphism" -W 1280 -H 720
```

### 结合 humanizer 优化提示词
```bash
# 用 humanizer 润色提示词，使结果更自然
# 先在聊天中让 humanizer 优化描述，再传入 text2img
```

### 在自动化工作流中使用
```bash
# 示例：生成配图并写入 MEMORY.md
URL=$(./bin/cli.js text2img -p "workflow diagram" -W 1200 -H 600 | grep -o 'https://[^"]*png')
echo "今日生成的流程图: $URL" >> memory/$(date +%Y-%m-%d).md
```

---

## 成本与积分

- **消耗**：每次生成消耗 2-5 积分（取决于分辨率、步数、模型）
- **查询余额**：运行任意命令后，输出中的 `accountBalance` 显示剩余积分
- **充值**：在 LiblibAI 平台充值增加积分

**建议**：先用小分辨率（512x512）测试提示词，再放大生成以节省积分。

---

## 参数参考表

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| prompt | string | **必需** | 正向提示词，描述你想生成的图像 |
| negativePrompt | string | - | 负向提示词，排除不想要的元素 |
| width/height | number | 768/1024 | 图像尺寸（建议 512 的倍数） |
| steps | number | 20 | 采样步数，质量与速度平衡 |
| cfgScale | number | 7 | 提示词遵循度 |
| sampler | number | 15 | 采样器 ID（15=DPMSolver++） |
| seed | number | -1 | 随机种子（固定种子可复现结果） |
| imgCount | number | 1 | 生成数量（1-4） |
| templateUuid | string | - | 预设模板 ID（平台创建） |

---

## 提示词技巧

- **使用逗号分隔**：`"cat, cute, photorealistic, 8k"`
- **权重语法**：`"(masterpiece:1.2)"` 提升权重
- **负面提示词**：始终添加 `"ugly, blurry, low quality, watermark"`
- **风格引用**：`"by Greg Rutkowski"`、`"Studio Ghibli style"`
- **质量词**：`"masterpiece, best quality, highres, 8k"`

---

## 技术细节

- **SDK**: 使用官方 `liblibai` npm 包（v0.0.11）
- **API**: 兼容 OpenAI DALL-E 风格接口
- **超时**: 默认 5 分钟，可通过 `--timeout` 调整
- **轮询间隔**: 默认 3 秒检查状态

---

## 版本历史

**v1.0.0** (2026-03-13)
- 初始发布
- 完整 CLI 支持（text2img, img2img, upload, status, wait）
- 优化输出格式（清晰图片链接）
- 环境变量配置

---

## 相关链接

- [LiblibAI 官网](https://liblibai.com)
- [API 文档](https://liblibai.feishu.cn/wiki/UAMVw67NcifQHukf8fpccgS5n6d)
- [npm 包](https://www.npmjs.com/package/liblibai)
- [ClawHub skill 页面](https://clawhub.ai/skill/liblibai)（发布后）

---

## 许可

MIT License - 自由使用、修改和分发。

---

*最后更新: 2026-03-13 · 上海*
