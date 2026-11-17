---
name: nano-banana-2-background-replace
description: "使用 Nano Banana 2 把同一授权主体迁移到不同渠道背景，并用背景版本表控制平台、场景、光线、安全区与禁止暗示。Use this skill for Nano Banana 2 background replacement、图片换背景、商品抠图、白底转场景、多渠道背景、淘宝京东抖音小红书亚马逊 TikTok Shop Shopify 产品图和广告图；通过 AI Hive 编辑指定图片。"
---

# Nano Banana 2 图片换背景

固定使用 `public_model_nano_banana_2`，必须提供原图。围绕同一主体建立“背景版本表”，每个版本只改变环境与渠道构图，主体身份、商品事实和拍摄视角保持一致。

## 背景版本表

为每个版本记录渠道、比例、环境、地面材质、地平线、主光方向、色温、景深、文案安全区、允许道具和禁止暗示。先确认原图是否具备可用边缘和光线；主体需要换角度、换姿势或重做结构时，不应伪装成单纯换背景。

## 场景与代码

### 1. 白底到品牌色棚拍

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-headphones-white.png \
  --prompt '只把白底替换为深蓝到靛青的品牌色渐变棚拍背景，耳机外形、耳罩、头梁、按键、接口、Logo和真实颜色不变；延续原图右侧主光，生成柔和底部阴影与细窄轮廓光，不添加文字、霓虹、人物或第二副耳机' \
  --param aspect_ratio=4:5
```

### 2. Amazon 白底版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-tool-scene.jpg \
  --prompt '从场景照中保留参考电动螺丝刀及已确认标配批头，替换为纯白背景；产品结构、颜色、Logo、按键和配件数量不变，商品完整居中、自然轻阴影，不保留工作台、手、木屑、文字、尺寸线或非标配工具' \
  --param aspect_ratio=1:1
```

### 3. 抖音电商厨房版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-blender.png \
  --prompt '保持料理机杯体、底座、旋钮、刻度、Logo和相机角度，只把背景迁移到明亮家庭厨房台面；顶部与底部保留UI安全区，补充与左侧窗光一致的阴影和台面反射，不生成主播、文字、价格、飞溅食物或不存在的配件' \
  --param aspect_ratio=4:5
```

### 4. 小红书生活方式版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-notebook.png \
  --prompt '把参考笔记本迁移到清晨咖啡馆木桌，保持封面材质、装订、尺寸比例、Logo和原相机角度；背景轻微虚化，旁边只放一支无品牌铅笔，顶部留标题区，不生成咖啡品牌、人物脸、文字、价格或第二本笔记本' \
  --param aspect_ratio=3:4
```

### 5. 户外耐用感版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-case.png \
  --prompt '保持参考防护箱的尺寸、锁扣、提手、轮廓和标识，只替换为阴天户外岩石地面；匹配原图相机高度，增加合理接触阴影和少量环境反射，不添加跌落、浸水、军用标识、性能等级、人物或额外装备' \
  --param aspect_ratio=16:9
```

## 版本验收

1. 将各渠道版本叠加对比，主体轮廓与内部结构没有漂移。
2. 背景地平线、尺度和透视匹配原相机，不悬浮、不穿插。
3. 新光线只解释环境，不改写商品颜色或人物身份。
4. 安全区与裁切适配渠道，平台规则按发布当天重新核对。
5. 环境不得暗示未经证实的耐用性、地点、合作或使用效果。

## 助手边界

工具只读取并上传命令中指定的参考图，固定调用 Nano Banana 2 图片模型，查询价格、创建任务并保存结果。携带 Key 的请求只发送到 `https://ai-hive.iclip.cn/api`；不接受自定义接口，也没有聊天、视频、钱包或账户查询命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-background-replace
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

渠道名称用于描述使用环境，不表示官方合作；人物、室内空间和品牌素材应先获得授权。
