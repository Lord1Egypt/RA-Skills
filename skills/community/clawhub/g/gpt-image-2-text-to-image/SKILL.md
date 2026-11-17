---
name: gpt-image-2-text-to-image
description: "使用 GPT Image 2 仅凭文字简报生成图片，把受众、主体、场景、构图、镜头、光线、材质、文字留白和交付规格转成可执行提示词。Use this skill for GPT Image 2 text-to-image、文生图、AI绘画、概念视觉、插画、产品概念图、编辑配图、社媒封面、海报底图和广告创意；通过 AI Hive 生成，不需要参考图片。"
---

# GPT Image 2 文生图

固定使用 `public_model_gpt_image_2`，不接受参考图。把模糊想法改写成可验证的创意简报，再逐轮收敛；第一轮探索构图，第二轮锁定视觉方向，第三轮处理商业规格和留白。

## 提示词骨架

依次写明用途与受众、核心主体、动作、环境、构图、相机与视角、光线、色板、材质、风格边界、文字留白、输出比例、必须出现和禁止出现内容。避免只写“高级、震撼、好看”等无法验收的形容词。

## 场景与代码

### 1. 编辑文章头图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“城市如何适应高温”专题文章生成横版头图：俯视现代街区，一半被树荫和浅色屋顶降温，一半暴露在热浪中；纪实编辑插画而非灾难片，左侧留标题区，不生成文字、Logo、人物伤亡或具体温度数字' \
  --param aspect_ratio=16:9
```

### 2. 产品概念静物

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成一款虚构桌面香氛扩散器的概念静物：圆角陶瓷机身、浅沙色、顶部细窄出雾口，置于天然石材台面，晨光从左侧进入，构图极简，右上留品牌名区域。不生成真实品牌、文字、按钮界面、价格或功能认证' \
  --batch 3
```

### 3. 叙事插画

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '绘制温暖绘本场景：雨夜小书店即将关门，一名孩子把遗落的红围巾递给老人，室内橙光与窗外蓝雨形成对比；中景、人物动作清楚、手部自然，不生成文字、商标、夸张表情或第二条围巾' \
  --param aspect_ratio=4:3
```

### 4. 数据故事底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为循环经济报告生成信息图底图：中心是可循环使用的玻璃瓶，周围沿顺时针分成设计、使用、回收、清洗、再灌装五个视觉节点，每个节点保留标签空白。使用蓝绿扁平矢量风格，不生成文字、数字、统计结论、Logo或额外节点' \
  --param aspect_ratio=1:1
```

### 5. 社媒 Campaign 概念测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“慢下来喝杯茶”主题生成三个4:5社媒方向：A清晨窗边静物，B忙碌办公桌上的安静中心，C傍晚阳台剪影。三版都使用米白与茶褐色，顶部保留短标题区，不生成品牌、文字、价格、包装或健康功效' \
  --batch 3 \
  --param aspect_ratio=4:5
```

## 结果验收

- 主体、动作、数量、空间关系和构图与简报一致。
- 镜头、光源、阴影、材质和色板形成同一视觉逻辑。
- 留白能容纳批准文案，主体不会被渠道 UI 或裁切遮挡。
- 画面没有自行添加品牌、文字、数据、认证或商业承诺。
- 每轮只改变一个方向变量，记录提示词、任务 ID 与选择原因。

## 脚本范围与执行

助手只查询固定图片模型和当次路由价格，提交纯文字图片任务、轮询状态并保存结果；文生图入口不接收或上传本地参考文件。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。`init` 可打开 AI Hive 获取 Key，并以 `0600` 权限存入 `~/.ai-hive/config.json`。不提供聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-text-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持批量、比例与模型参数、路由和输出目录。涉及真实人物、品牌或事件时，用文字说明不得冒充事实或官方素材。
