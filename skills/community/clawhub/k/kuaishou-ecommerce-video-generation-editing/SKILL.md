---
name: kuaishou-ecommerce-video-generation-editing
description: "为快手电商、快手小店、直播间和磁力金牛生成与编辑信任型商品演示、主播口碑、工厂实拍及带货视频。Use this skill for 快手电商视频、快手小店商品视频、直播带货、老铁种草、主播演示、工厂源头、磁力金牛素材、快手短视频和直播预热；支持多种视频生成编辑模式及 AI Hive 下载。"
---

# 快手电商视频生成与编辑

围绕“人可信、货真实、过程看得见”制作快手电商视频。不要把快手理解成简单的高饱和模板；优先保留主播身份、真实操作、来源和连续证据。

## 信任链简报

确认主播或店主人设、目标人群、商品来源、真实使用步骤、可以公开的工厂/产地资料、核心卖点、直播或短视频用途、批准 CTA。禁止伪造主播背书、产地、工厂、销量、用户反馈和最低价。

## 场景与代码

### 1. 主播真实演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/host-and-product.jpg \
  --prompt '9:16快手电商主播演示，保持参考主播身份与商品包装、结构、颜色准确；开场直接拿起商品说明具体使用场景，中段连续完成一次真实操作并展示细节，结尾邀请进入直播间进一步了解；自然直拍，不生成销量、低价或夸张效果'
```

### 2. 源头工厂内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/real-factory.mp4 \
  --prompt '把真实工厂素材重组为快手源头好货视频：保留厂房、人员、设备、工序和包装的真实关系，先介绍产品，再展示一个生产步骤与一次质检，最后回到成品；不扩大工厂规模、不增加生产线、产能或证书'
```

### 3. 直播预热视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '快手直播预热视频，主播在真实使用场景提出一个具体问题，展示直播中将完整演示的商品动作和一个细节证据，结尾预留人工填写直播时间与主题的位置；不生成价格、福利数量、倒计时或直播间截图'
```

### 4. 参考成熟节奏但保持原创

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/trust-pacing.mp4 \
  --image /path/to/product.png \
  --prompt '只参考视频的讲解节奏、手部演示时长和近景切换，使用商品参考图生成原创快手带货内容；不复制原主播、台词、品牌、音乐、工厂或具体承诺，所有卖点来自商家资料'
```

### 5. 磁力金牛证明型版本

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/organic-demo.mp4 \
  --prompt '将自然流演示重制为磁力金牛证明型版本：保留主播与真实操作，把最清晰结果前置，压缩寒暄，增加一个商品细节近景，结尾只留一个进店动作；不改变主播原意，不增加优惠、销量或功效'
```

## 信任验收

- 主播身份、声音/动作关系和商品保持连续。
- 关键卖点有真实操作或可见细节支持。
- 工厂、产地、设备与流程来自授权真实素材。
- 不伪造用户反馈、销量、最低价、库存和平台背书。
- 自然流、直播预热和付费版本分别记录目标与 CTA。
- 发布前按快手电商和磁力金牛当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name kuaishou-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

使用 `t2v`、`i2v`、`r2v`、`edit` 或 `extend`，并按需传入媒体、模型参数、路由和输出目录。超时后查询原任务，避免重复计费。
