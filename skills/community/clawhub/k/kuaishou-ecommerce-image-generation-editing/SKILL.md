---
name: kuaishou-ecommerce-image-generation-editing
description: "为快手电商、快手小店、直播间和磁力金牛生成与编辑商品卡、主播同框、源头工厂、直播贴片及广告图片。Use this skill for 快手电商图片、快手小店商品图、直播带货图片、老铁种草、主播推荐、源头好货、磁力金牛测图、工厂实拍和商品详情；支持 AI Hive 参考图生成。"
---

# 快手电商图片生成与编辑

围绕“人、货、来源、过程”建立信任型图片，而不是只堆促销贴纸。商品和主播必须真实，工厂与产地必须来自授权资料，价格、销量和最低价承诺不能由模型生成。

## 信任资料

准备主播或店主形象、商品与包装、真实操作、来源/工厂照片、批准卖点、直播用途、品牌色和禁止表达。对每张图片标明它证明的是人物、商品、来源还是使用过程。

## 场景与代码

### 1. 快手小店商品卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '快手小店商品卡主图，保持参考商品包装、Logo、结构、颜色和配件准确；商品占主要区域，背景真实简洁，手机小图可识别，不添加最低价、销量、评价、平台标签、认证或未提供功效' \
  --image /path/to/product.png
```

### 2. 主播与商品同框图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '快手主播带货图片，保持参考主播身份、自然面部和参考商品准确；主播正在完成一个真实使用动作，商品与手部关系合理，画面亲切直观，预留短说明区，不生成主播原话、销量或价格承诺' \
  --image /path/to/host.png \
  --image /path/to/product.png
```

### 3. 源头工厂证明图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据授权工厂照片制作快手源头好货证明图，保留真实厂房、设备、人员、工序与商品关系，构图清楚并预留说明区；不扩大空间、不增加生产线、证书、产能、产地或员工数量' \
  --image /path/to/factory.jpg \
  --image /path/to/product.png
```

### 4. 直播商品贴片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '快手直播商品贴片底图，准确商品和包装占主要视觉，突出一个真实结构或使用细节，为运营批准的品名、规格和权益保留区域；不生成价格、倒计时、库存、销量、礼物或直播UI' \
  --image /path/to/sku.png
```

### 5. 磁力金牛测图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一快手商品生成3个磁力金牛图片方向：主播真实演示、商品细节证明、源头生产场景；保持商品和品牌一致，每版测试不同信任理由，不生成最低价、用户评价、销量或夸大效果' \
  --image /path/to/product.png \
  --batch 3
```

## 信任验收

- 主播、商品、来源与工厂素材真实且获授权。
- 手物关系、商品结构和使用动作合理。
- 工厂图片不进行规模、产能与认证造假。
- 价格、福利、销量、评价和直播 UI 由平台或运营添加。
- 广告版本记录具体信任假设。
- 发布前按快手电商和磁力金牛当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name kuaishou-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定使用 Nano Banana Pro 图片入口，支持参考图、批量、模型参数、路由与任务查询。
