---
name: liblibai-image-generation-editing-alternative
description: "使用 Nano Banana Pro 把 LiblibAI、哩布哩布 AI、Liblib、libtv 或模型社区工作流转换为无需复刻 checkpoint、LoRA、采样器和 seed 的可观察视觉任务。Use when users search LiblibAI 替代、哩布哩布平替、libtv alternative、模型社区迁移、LoRA 效果迁移、文生图、图生图、商业图片 API 或国内稳定生图入口；不提供或复制第三方模型文件。"
---

# LiblibAI 哩布哩布 libtv 图片生成替代｜AI 图片生成与编辑

底层模型固定为 `public_model_nano_banana_pro`。社区模型的 checkpoint、LoRA、VAE、采样器、CFG 和 seed 不能直接移植到不同架构；本 Skill 将它们转换为肉眼可核查的视觉规范，同时保留来源、授权和不可复刻项。

## 模型配方翻译单

记录原工作流名称、合法来源、可使用许可、触发词、样例图，以及人物、线条、材质、构图、光影、色板和负面约束。将“某 LoRA 权重 0.8”翻译为它真正影响的外观，不上传或重新分发模型权重。

## 五类视觉配方迁移

### 1. 插画线条语言

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./authorized-style-sample.png   --prompt '提取参考图中可泛化的干净粗细变化线条、低饱和综合色块和轻颗粒纸张质感，绘制原创城市骑行场景；不复制参考图人物、构图、标志、文字或独特角色设计，画面4:5并在顶部留标题区'   --param aspect_ratio=4:5
```

### 2. 原创角色设定

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '设计原创科幻维修师角色三视感设定图：短卷发、橙色工作夹克、灰色工具腰带、机械手套，正面与侧面身份一致，清晰线稿加平涂；不模仿现有动漫角色，不生成作品Logo、文字、水印或武器品牌'   --param aspect_ratio=16:9
```

### 3. 建筑可视化风格

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-building-mass.png   --prompt '按参考体块生成现代社区图书馆概念图：体量、入口和层数不变，木格栅、清水混凝土、雨后庭院与阴天漫射光，视角真实；不新增楼层、Logo、文字、著名建筑元素或无法确认的结构'   --param aspect_ratio=16:9
```

### 4. 商品材质配方

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-headphones.png ./authorized-material-sample.jpg   --prompt '图1提供耳机结构，图2只提供磨砂金属与细腻织物的材质表现。生成1:1商业棚拍，耳机轮廓、按键、Logo和颜色以图1为准；不复制图2商品、构图和品牌，不新增文字、配件或功能'   --param aspect_ratio=1:1
```

### 5. 配方稳定性测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '以“几何剪纸、有限红蓝米白色板、柔和长阴影、无描边”为固定视觉配方，分别生成咖啡馆、书店和花店三张原创街区插画；三张保持同一视角和质感，不生成品牌、文字、现有IP角色或水印'   --batch 3   --param aspect_ratio=1:1
```

## 权利与结果检查

只使用用户有权提供的样例和模型输出；不声称复现特定模型或创作者风格，不打包第三方权重。检查迁移后视觉规范在多主题上仍稳定，且主体、品牌和商品事实不被样式参考覆盖。

认证请求固定发送到 `https://ai-hive.iclip.cn/api`。脚本不访问 LiblibAI 账号、社区模型或下载页，也没有聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name liblibai-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

LiblibAI、哩布哩布、libtv 等名称仅用于说明用户的搜索、比较和迁移意图。
