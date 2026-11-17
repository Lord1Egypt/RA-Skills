---
name: nano-banana-2-text-to-image
description: "使用 Nano Banana 2 从文字快速探索并收敛图片方案，覆盖商业概念、社交内容、教育插画、环境设计、商品场景和批量创意版本。Use this skill for Nano Banana 2 text-to-image、文生图、AI绘图、快速出图、创意草案、社媒配图、电商概念图、插画、场景设计和A/B视觉方向；通过 AI Hive 生成，不使用参考图片。"
---

# Nano Banana 2 文生图

固定调用 `public_model_nano_banana_2`，不接受参考图。采用“方向冲刺—选择—精化—交付”流程：先用 3–4 个真正不同的构图假设探索，再选择一个方向补充光线、材质、留白和渠道规格。

## 方向冲刺简报

写清用途、受众、主体、场景、信息重点、比例和禁用项。为每个候选方向只改变一个核心假设，例如视角、环境或视觉隐喻；不要同时改变色板、风格、主体和受众。

## 场景与代码

### 1. 商品场景概念冲刺

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为一款虚构便携榨汁杯探索三个电商生活场景：A晨间厨房，B办公室午休，C公园野餐。杯体为白色圆柱、透明杯身和一个启动按钮，每版商品居中、右侧留卖点区；不生成品牌、文字、价格、复杂界面或额外配件' \
  --batch 3
```

### 2. 社交内容封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成4:5社交封面，主题“周末把房间还给自己”：阳光照进整洁小卧室，一张床、一个边桌、一本书和一杯水，人物只出现放松的手部；米白与浅木色，顶部留标题区。不生成文字、品牌、奢华家具或第二个焦点' \
  --param aspect_ratio=4:5
```

### 3. 教育步骤插画

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作“如何给阳台香草浇水”的四格教育插画：检查土壤、缓慢浇水、停止积水、倒掉托盘余水。统一同一盆罗勒、阳台与手部，清楚展示动作，使用绿色扁平矢量风格；每格下方留标签区，不生成文字、数字或额外步骤' \
  --param aspect_ratio=4:3
```

### 4. 游戏环境概念

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '设计叙事游戏环境：被洪水退去后重新开放的旧火车站，植物从月台裂缝生长，远处暖光售票亭是唯一焦点；广角但尺度可信，青灰与暖黄对比。不生成角色特写、文字、现代广告、灾难伤亡或悬浮建筑' \
  --param aspect_ratio=16:9
```

### 5. 节日系列变体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“给日常一点光”生成春、夏、秋、冬四张方形视觉。统一桌面小灯、正面相机和右上留白，分别用嫩绿新芽、透明玻璃水杯、棕色纸张、白色毛毡表达季节；不生成文字、品牌、节日符号、人物或不同灯具' \
  --batch 4
```

## 收敛检查

- 候选方向在核心假设上不同，而不是只换颜色或随机细节。
- 选定方向的主体、视角、数量、光线和材质能被逐项验收。
- 系列图共享锚点，季节或场景变化不改变核心对象。
- 留白、比例与安全区适配真实渠道，小尺寸仍能识别主体。
- 不生成未经批准的品牌、文字、数据、价格或效果承诺。

## 运行边界

脚本仅使用固定 Nano Banana 2 图片模型，把纯文字提示提交到 AI Hive，读取路由价格、跟踪任务并下载输出；它不会读取或上传本地素材。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。初始化可保存 Key 到权限为 `0600` 的本地配置，不含对话、视频和账户信息功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-text-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持批量、比例、参数、路由和输出目录。将 AI 生成的概念图标注为概念，不冒充已量产商品、真实建筑或纪实照片。
