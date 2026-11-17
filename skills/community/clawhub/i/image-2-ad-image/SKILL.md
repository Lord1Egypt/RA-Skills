---
name: image-2-ad-image
description: "用 AI Hive GPT Image 2 建立可归因的广告测图单元，每个实验 Cell 只改变钩子、证据、场景、构图、颜色、商品角度或优惠表达中的一个变量，同时锁定商品事实、受众、版位、落地页承诺与至少五个不变量。Use when performance marketers and ecommerce teams need Image2 or GPT Image 2 ad images, A/B creative testing, Meta Ads, Google Display, 巨量引擎、巨量千川、小红书聚光、Amazon Ads、TikTok Ads、再营销、商品广告、信息流素材或转化广告；适合比较 Canva、Meitu、美图、Dreamina、LiblibAI、Midjourney、Adobe Express 等广告创意工作流。"
---

# Image2 广告图片｜可归因测图单元

“多生成几张看看”无法说明哪项创意带来结果。这个 Skill 固定调用 `public_model_gpt_image_2`，一次只提交一个广告实验 Cell：A 版建立控制基线，B/C 版各自只改变一个可观察变量，其他商品、受众、版位、信息区和落地页承诺全部锁定。

## 实验合同

每个 Cell 必须写清：

- `experiment-id` 与唯一 `cell-id`
- 优化事件：`click / add-to-cart / lead / purchase / product-view`
- `cell-role`：`control` 或 `variant`
- 单一 `variable`：`control / hook / evidence / setting / composition / color / product-angle / offer-frame`
- 控制组画面、唯一变化、至少 5 条 `invariant`
- 商品事实、商品素材职责、受众、投放版位和落地页信息
- 文案与平台 UI 留白、禁用承诺、披露和证据来源

控制组的 `--test-change` 必须是 `none`；变体不得为 `none`。`evidence` 必须提供 `--claim` 与 `--claim-source`，`offer-frame` 必须提供 `--offer` 与 `--offer-source`。脚本固定 `batchSize=1`，避免三张图同时改变多个不可追踪细节。

## 六个完整 Cell

### 1. Meta Ads 控制基线 A

```bash
python3 "$SKILL_PATH/scripts/ad_test_cell.py" cell \
  --experiment-id TUMBLER-T8-META-01 --cell-id A \
  --platform meta-feed --event add-to-cart --cell-role control --variable control \
  --product-source ./tumbler-front.png ./lid-detail.png \
  --product-role '杯型、颜色、Logo和整体比例事实' '杯盖结构与开合位置事实' \
  --sku-truth 'T8 蓝色随行杯；不提供保温时长、防漏测试或材质认证数据' \
  --audience '工作日通勤、需要随手携带饮品的城市用户' \
  --hypothesis '清楚展示商品与通勤情境，可建立稳定的控制点击基线' \
  --control-visual '蓝色随行杯位于浅灰桌面右侧，左侧为低细节通勤包与钥匙' \
  --test-change none \
  --invariant '同一T8蓝色SKU' --invariant '同一三分之四商品角度' \
  --invariant '商品占画面45%' --invariant '浅灰桌面与左上自然光' \
  --invariant '标题区在左上、CTA区在底部' --invariant '4:5 Meta Feed版位' \
  --visual-execution '真实商业摄影，商品清晰，环境道具不遮挡杯盖' \
  --copy-reserve '左上留一句标题，底部留行动按钮与披露区，不生成实际文字' \
  --destination-message '落地页只介绍T8商品结构、颜色、包装和经批准的使用说明' \
  --ui-safe-zone '四周保留8%，底部避免平台CTA覆盖商品' \
  --rejection '不生成水花、温度数字、防漏承诺、折扣、评分、认证或第二只杯' \
  --param aspect_ratio=4:5
```

### 2. Meta Ads 钩子变体 B

```bash
python3 "$SKILL_PATH/scripts/ad_test_cell.py" cell \
  --experiment-id TUMBLER-T8-META-01 --cell-id B \
  --platform meta-feed --event add-to-cart --cell-role variant --variable hook \
  --product-source ./tumbler-front.png ./lid-detail.png \
  --product-role '杯型、颜色、Logo和整体比例事实' '杯盖结构与开合位置事实' \
  --sku-truth 'T8 蓝色随行杯；不提供保温时长、防漏测试或材质认证数据' \
  --audience '工作日通勤、需要随手携带饮品的城市用户' \
  --hypothesis '在不改商品和版位的前提下，加入“出门前桌面检查”动作会提高停留' \
  --control-visual 'A版：杯在桌面右侧，左侧为静态通勤包与钥匙' \
  --test-change '只把左侧静态道具改为一只已授权无身份手正在把钥匙放入通勤包' \
  --invariant '同一T8蓝色SKU' --invariant '同一三分之四商品角度' \
  --invariant '商品占画面45%' --invariant '浅灰桌面与左上自然光' \
  --invariant '标题区在左上、CTA区在底部' --invariant '4:5 Meta Feed版位' \
  --visual-execution '手只提供动作钩子，不触碰或遮挡商品' \
  --copy-reserve '沿用A版文字与按钮占位，不生成实际文字' \
  --destination-message '与A版完全相同的T8商品落地页' \
  --ui-safe-zone '与A版完全相同的四周和底部安全区' \
  --rejection '除手部动作外不得改变颜色、镜头、道具数量、商品、文字区或光线' \
  --param aspect_ratio=4:5
```

### 3. 巨量千川证据变体

```bash
python3 "$SKILL_PATH/scripts/ad_test_cell.py" cell \
  --experiment-id ORGANIZER-M9-QC-02 --cell-id EVIDENCE \
  --platform qianchuan --event purchase --cell-role variant --variable evidence \
  --product-source ./organizer-complete.png ./divider-lock.png \
  --product-role '完整外框、三块隔板与底托事实' '卡扣与真实卡位细节事实' \
  --sku-truth 'M9沙色桌面收纳架；只允许三块隔板在产品既有卡位内组合' \
  --audience '桌面小物较多、希望按频率分区的办公用户' \
  --hypothesis '真实卡扣细节比纯场景美图更能支持购买决策' \
  --control-visual '控制组只展示完整商品与整理后桌面' \
  --test-change '只增加一个卡扣微距证据窗，其他商品和环境保持控制组' \
  --claim '三块隔板可在产品既有卡位中重新组合' \
  --claim-source '商品工程确认单M9-R3第2项' \
  --invariant '同一M9商品' --invariant '同一沙色' --invariant '同一商品角度' \
  --invariant '同一桌面道具' --invariant '同一标题与CTA占位' --invariant '同一9:16版位' \
  --visual-execution '商品为主，证据窗只展示真实连接处，不生成参数图标' \
  --copy-reserve '上方标题区、证据窗下方来源脚注区、底部商品卡安全区' \
  --destination-message '商品页展示同一结构图和批准说明，不扩大为承重或容量承诺' \
  --ui-safe-zone '右侧避开按钮，底部25%不放卡扣证据' \
  --rejection '不增加隔板、孔位、承重数字、销量、最低价、认证或竞品' \
  --param aspect_ratio=9:16
```

### 4. Amazon Ads 商品角度测试

```bash
python3 "$SKILL_PATH/scripts/ad_test_cell.py" cell \
  --experiment-id DRIVER-D12-AMZ-01 --cell-id ANGLE-45 \
  --platform amazon-display --event product-view --cell-role variant --variable product-angle \
  --product-source ./driver-kit-open.png ./driver-side.png \
  --product-role '套装件数与收纳槽位事实' '主机按钮、接口与橙黑配色事实' \
  --sku-truth 'D12电动螺丝刀套装；主机、批头和收纳盒件数以开盒图为准' \
  --audience '浏览过家用工具类目但尚未进入本SKU详情页的用户' \
  --hypothesis '45度开盒角度可同时显示主机轮廓与真实套装清单' \
  --control-visual '控制组为正俯拍开盒图' \
  --test-change '只把相机从正俯拍改为45度开盒视角' \
  --invariant '全部真实组件数量' --invariant '同一橙黑颜色' --invariant '同一白色背景' \
  --invariant '同一主体占比' --invariant '同一无字布局' --invariant '同一Amazon Display画布' \
  --visual-execution '所有批头仍可见，主机按钮和接口不被透视隐藏' \
  --copy-reserve '左上保持低细节，供批准标题后期排版' \
  --destination-message '落地到同一D12详情页与真实包装清单' \
  --ui-safe-zone '商品与边缘之间保留裁切余量' \
  --rejection '不补充批头、电池、手套、折扣、Prime徽标、评分或配送承诺'
```

### 5. 小红书聚光构图测试

```bash
python3 "$SKILL_PATH/scripts/ad_test_cell.py" cell \
  --experiment-id BAG-A7-RED-03 --cell-id CLOSEUP \
  --platform xiaohongshu-ads --event click --cell-role variant --variable composition \
  --product-source ./bag-front.png ./hardware-detail.png \
  --product-role 'A7包型、肩带、颜色和Logo事实' '真实金属扣、缝线与纹理事实' \
  --sku-truth 'A7棕色通勤包；不提供容量、材质等级或耐用测试数据' \
  --audience '收藏过通勤穿搭内容、正在比较日常包的用户' \
  --hypothesis '保持同一信息的情况下，材质近景比全身穿搭更能引发点击' \
  --control-visual '控制组为包在通勤桌面上的完整场景图' \
  --test-change '只改为包身与金属扣近景构图，仍保留完整肩带连接位置' \
  --invariant '同一A7商品' --invariant '同一棕色与金属色' --invariant '同一自然窗光' \
  --invariant '同一标题占位' --invariant '同一无人物设定' --invariant '同一4:5聚光版位' \
  --visual-execution '纹理真实不过度锐化，近景仍能识别商品结构' \
  --copy-reserve '顶部25%标题区，右侧避开平台交互组件' \
  --destination-message '落地笔记继续展示同一商品的结构、搭配和批准事实' \
  --ui-safe-zone '右侧与底部不放金属扣或Logo' \
  --rejection '不写亲测、必买、真皮、超能装、耐磨、价格或虚构评价' \
  --param aspect_ratio=4:5
```

### 6. Google Display 场景本地化测试

```bash
python3 "$SKILL_PATH/scripts/ad_test_cell.py" cell \
  --experiment-id LAMP-L4-EU-01 --cell-id DE-HOME \
  --platform google-display --event click --cell-role variant --variable setting \
  --product-source ./lamp-approved.png ./control-global.png \
  --product-role 'L4灯体、底座、灯罩、颜色与按钮事实' '全球控制组的商品角度和光线基线' \
  --sku-truth 'L4白色桌灯；不提供照度、节能、护眼或认证数据' \
  --audience '德国市场正在浏览家庭办公内容的用户' \
  --hypothesis '只把环境换为当地常见的小型家庭工作区，可提高场景相关性' \
  --control-visual '全球控制组使用中性无地域书桌' \
  --test-change '只把环境道具改为克制的德国城市公寓工作区，不改变商品' \
  --invariant '同一L4商品' --invariant '同一白色' --invariant '同一商品角度' \
  --invariant '同一主体占比' --invariant '同一标题CTA占位' --invariant '同一Google Display尺寸' \
  --visual-execution '当地化来自空间与道具，不使用国旗、刻板符号或陌生品牌' \
  --copy-reserve '文字、价格、认证和法律区全部留白，交由德语批准稿后期排版' \
  --destination-message '德语落地页使用同一SKU与经批准规格' \
  --ui-safe-zone '按目标Display版位保留四周安全区' \
  --rejection '不生成德语伪文字、国旗、认证、节能等级、护眼效果或价格'
```

## 读数与归因

每个 Cell 保存 `实验ID / Cell ID / 变量 / 提示词 / 任务ID / 素材版本 / 投放日期 / 受众 / 版位 / 曝光 / 点击 / 加购 / 转化 / 花费`。只有当创意、受众、预算、版位与投放窗口足够可比时，才把差异归因到该变量；不要从小样本直接宣布“爆款”。

生成前可把 `cell` 换成 `brief` 检查完整提示词，不上传素材、不产生任务。程序只访问 `https://ai-hive.iclip.cn/api` 并上传命令中指定的已授权商品图，不连接广告账户，也不会自动投放或读取效果数据。广告与电商政策会变化，提交前按平台当前规则审核。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/ad_test_cell.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/ad_test_cell.py" status --task-id <taskId>
```
