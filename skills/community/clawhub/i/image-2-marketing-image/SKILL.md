---
name: image-2-marketing-image
description: "用 AI Hive GPT Image 2 建立可追溯的 Campaign 图片资产血缘：先生成品牌营销母版，再派生落地页 Hero、EDM 头图、社媒卡片、商品店铺横幅、门店屏幕、发布会背景和 CRM 图片，并按市场边界本地化。Use when brand and ecommerce teams need Image2 or GPT Image 2 marketing images, integrated campaigns, product launch visuals, campaign KV, landing pages, email headers, social assets, retail displays, event screens, localization or CRM content for Taobao, Tmall, JD, Douyin, Xiaohongshu, WeChat, Amazon, TikTok Shop, Instagram and Shopify; relevant to Canva, Meitu, Dreamina, LiblibAI, Midjourney, Adobe Express and Figma workflow searches."
---

# Image2 营销图片｜Campaign 资产血缘

同一 Campaign 的图片应能回答“它从哪张批准母版派生、继承了什么、为什么针对这个渠道重排”。这个 Skill 固定调用 `public_model_gpt_image_2`，提供三条路径：

- `master`：建立母版视觉世界与不可变商品事实。
- `derive`：从批准母版派生一个明确用途的渠道资产。
- `localize`：在不改变商品与品牌核心的前提下适配市场语境。

所有文字、日期、价格、会员权益、法律信息与二维码默认留白后期排版。模型生成的候选字符不能直接作为批准稿。

## 资产编号

使用 `campaign-id / asset-id / parent-asset-id` 建立谱系，例如：

```text
URBAN-RIDE-26 / MASTER-KV / none
URBAN-RIDE-26 / LANDING-HERO-CN / MASTER-KV
URBAN-RIDE-26 / EDM-MEMBER-CN / MASTER-KV
URBAN-RIDE-26 / SOCIAL-JP-01 / LANDING-HERO-CN
```

同一 `asset-id` 不覆盖旧版本。主张或商品事实改变时，建立新版本并检查所有后代资产。

## 六个完整场景

### 1. 创建产品上市母版 KV

```bash
python3 "$SKILL_PATH/scripts/campaign_lineage.py" master \
  --campaign-id URBAN-RIDE-26 --asset-id MASTER-KV \
  --product-source ./bike-front.png ./bike-side.png ./brand-board.png \
  --product-role '车型、车架、轮组、电池位置和Logo事实' '侧面比例与真实配件事实' '批准品牌色和图形语言，不提供商品结构' \
  --sku-record 'UR26城市电动自行车；不提供续航、速度、环保认证或价格数据' \
  --audience '希望以轻量方式完成城市短途出行的成年用户' \
  --campaign-job '建立新品上市期可供所有渠道继承的品牌认知视觉世界' \
  --core-promise '轻盈、清楚、适合城市日常路径的出行体验' \
  --promise-source '品牌与产品团队批准的UR26上市简报v5' \
  --motif '清晨建筑线条延伸成一条前进路径，路径不冒充真实导航' \
  --palette '蓝灰、晨光金和车架原色；商品颜色不被氛围光改变' \
  --camera-language '45度车型视角、中等焦段、真实尺度、克制速度感' \
  --subject-lock '车架、轮组、电池位置、线缆、配件、颜色与现有Logo' \
  --copy-map '左侧主张区；左下副标题区；右下法律与版本区，全部无字' \
  --forbid '不生成人物危险动作、续航数字、速度、价格、认证、地图或第二车型' \
  --param aspect_ratio=16:9
```

### 2. 派生落地页 Hero

```bash
python3 "$SKILL_PATH/scripts/campaign_lineage.py" derive \
  --campaign-id URBAN-RIDE-26 --asset-id LANDING-HERO-CN \
  --parent-asset-id MASTER-KV --parent ./master-kv-approved.jpg \
  --product-source ./bike-front.png ./bike-side.png \
  --product-role '商品正面结构事实' '商品侧面比例与配件事实' \
  --stage consideration --channel landing-page --asset-type hero \
  --asset-job '让用户在首屏识别车型、品牌世界和继续了解产品的入口' \
  --carry-over 'UR26商品身份与45度角度' --carry-over '蓝灰与晨光金色板' \
  --carry-over '建筑路径视觉母题' --carry-over '左侧信息、右侧商品的阅读方向' \
  --recompose '背景减弱，商品占右侧55%；左上留产品名与两行价值说明，左下留按钮' \
  --copy-map '产品名、价值说明、CTA、法律信息均留空，使用批准网页文案后期排版' \
  --channel-safe '桌面和移动端首屏均保留导航、Cookie与按钮安全区' \
  --success-signal '首屏继续浏览率与产品详情点击，不把视觉结果直接等同销售' \
  --forbid '不生成规格数字、价格、虚构界面、路人、新配件或第二车型'
```

### 3. 派生会员 EDM 头图

```bash
python3 "$SKILL_PATH/scripts/campaign_lineage.py" derive \
  --campaign-id URBAN-RIDE-26 --asset-id EDM-MEMBER-CN \
  --parent-asset-id MASTER-KV --parent ./master-kv-approved.jpg \
  --product-source ./bike-front.png \
  --product-role 'UR26车型、颜色、轮组和Logo事实' \
  --stage retention --channel email --asset-type email-header \
  --asset-job '为已订阅会员提供新品故事入口，窄屏仍能识别车型' \
  --carry-over '车型身份' --carry-over '蓝灰与晨光金' \
  --carry-over '建筑路径母题' --carry-over '克制中等焦段摄影语言' \
  --recompose '商品移到左侧40%，右侧保留个性化标题、会员说明和CTA区域' \
  --copy-map '右侧三层信息区全部留空；不生成会员等级、优惠或姓名占位符' \
  --channel-safe '3:1横图，在移动端裁切后仍保留完整车架与右侧标题起始区' \
  --success-signal '邮件点击与落地页访问，单独记录主题行影响' \
  --forbid '不生成会员权益、折扣、日期、按钮文字、追踪码或额外配件' \
  --param aspect_ratio=3:1
```

### 4. 派生线下门店宽屏

```bash
python3 "$SKILL_PATH/scripts/campaign_lineage.py" derive \
  --campaign-id URBAN-RIDE-26 --asset-id RETAIL-WALL-CN \
  --parent-asset-id MASTER-KV --parent ./master-kv-approved.jpg \
  --product-source ./bike-side.png \
  --product-role '完整侧面轮廓、车架、轮组和电池位置' \
  --stage awareness --channel retail-screen --asset-type retail-banner \
  --asset-job '在门店入口远距离建立车型与品牌识别，为真人和展车留空间' \
  --carry-over '车型身份' --carry-over '建筑路径母题' \
  --carry-over '蓝灰与晨光金' --carry-over '从左下到右上的运动方向' \
  --recompose '画面中央保持真人讲解与实车安全区，车型轮廓分布在两侧但不重复细节' \
  --copy-map '顶部品牌区和底部活动信息区留空，现场系统后期排版' \
  --channel-safe '适配超宽屏、观看距离和现场遮挡，不把关键细节放在拼接缝' \
  --success-signal '门店停留与咨询由现场团队记录，不生成虚假统计' \
  --forbid '不生成观众、具体价格、活动日期、舞台文字、第二车型或不存在门店'
```

### 5. 将社媒资产本地化到日本市场

```bash
python3 "$SKILL_PATH/scripts/campaign_lineage.py" localize \
  --campaign-id URBAN-RIDE-26 --asset-id SOCIAL-JP-01 \
  --parent-asset-id SOCIAL-GLOBAL-01 --parent ./social-global-approved.jpg \
  --product-source ./bike-front.png \
  --product-role 'UR26车型、颜色、结构与Logo事实' \
  --market japan --language ja-JP --channel instagram \
  --local-job '让城市背景与版式适合日本成年通勤受众，批准日文后期排版' \
  --local-context '克制的小型城市街区、清楚人车空间和自然清晨氛围，不使用刻板符号' \
  --never-localize '车型结构、颜色与配件' --never-localize '品牌Logo与主视觉母题' \
  --never-localize '核心主张含义' --never-localize '商品与道路的真实尺度' \
  --copy-map '日文标题、副标题、CTA与法律区全部留白，不自动翻译' \
  --market-source '日本市场团队批准的城市背景与渠道简报JP-UR26-v2' \
  --forbid '不生成日文伪文字、国旗、樱花、地标、交通标志、价格或当地认证'
```

### 6. 本地化 Amazon Storefront 资产

```bash
python3 "$SKILL_PATH/scripts/campaign_lineage.py" localize \
  --campaign-id ORGANIZER-M9-26 --asset-id STOREFRONT-DE-01 \
  --parent-asset-id STOREFRONT-GLOBAL-01 --parent ./storefront-global.jpg \
  --product-source ./organizer-complete.png ./divider-lock.png \
  --product-role '完整商品、三块隔板与底托事实' '真实卡扣与卡位结构事实' \
  --market germany --language de-DE --channel amazon-storefront \
  --local-job '适配德国Amazon品牌店模块，环境更接近紧凑家庭办公空间' \
  --local-context '明亮紧凑工作区、克制道具、真实尺寸，不使用国旗或国家刻板元素' \
  --never-localize '商品结构与三块隔板数量' --never-localize '沙色与卡扣位置' \
  --never-localize '品牌色与Logo' --never-localize '批准卖点的事实范围' \
  --copy-map '德文标题、卖点和法律区留空，交由批准德语稿后期排版' \
  --market-source '德国站运营与合规团队批准的模块简报DE-M9-v4' \
  --forbid '不生成德语文字、承重、容量、认证、价格、评分、Prime徽标或额外隔板'
```

## 血缘验收

- 每个子资产只有一个明确父资产，继承项与重排项分开记录。
- 商品、人物、Logo、主张和活动事实来自批准源，不被市场语境改写。
- 不同渠道完成不同任务；尺寸变化不是简单拉伸、复制或裁切。
- 本地化只改变被批准的环境与版式，文字、单位、价格和法律信息由当地批准稿处理。
- 用资产关系表追踪版本：父资产更新时，逐个检查仍在使用的后代。

加入 `--preview` 可只验证并输出提示词，不上传素材、不创建任务。程序仅访问 `https://ai-hive.iclip.cn/api`，不会连接网站、邮件、门店屏幕或社交平台账户。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/campaign_lineage.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/campaign_lineage.py" status --task-id <taskId>
```
