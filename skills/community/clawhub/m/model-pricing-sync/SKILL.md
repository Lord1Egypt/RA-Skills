---
name: model-pricing-sync
description: 抓取模型厂商与代码工具价格页面，读取 Markdown 后补 JSON 提取文件，并同步到飞书普通电子表格。需要收集模型价格、补全价格 JSON、追踪价格变化或推送 Lark Sheets 时使用。
---
# model-pricing-sync

按下面流程执行。

路径约定：本文所有路径都相对于本 skill 目录。执行前先定位 `skills/model-pricing-sync/`，下文用 `<skill_dir>` 表示。`<run_dir>` 表示本次运行生成的目录名，通常为 `YYYYMMDD`。

新增来源约定：如果用户要求新增某厂商的 API 或订阅跟踪，先搜索并确认官方价格页，再把来源和目标条目补到 `<skill_dir>/config/` 下对应 CSV。

## 1. 采集

运行：

```bash
python <skill_dir>/scripts/sync_pricing.py --mode collect
```

作用：

- 抓取网页来源并保存为 `<skill_dir>/artifacts/<run_dir>/collected/pages/*.md`
- 初始化或合并 `<skill_dir>/artifacts/<run_dir>/extracted/api_pricing.json`
- 初始化或合并 `<skill_dir>/artifacts/<run_dir>/extracted/subscription_plans.json`
- 更新 `<skill_dir>/artifacts/latest_run.json`
- 后续步骤都默认处理 `<skill_dir>/artifacts/latest_run.json` 指向的这个 `run_dir`

只想跑部分来源时，可传 `--vendors anthropic,google`。

采集异常只看：

- `<skill_dir>/artifacts/<run_dir>/collected/collect_issues.csv`

如果有记录，先根据 `source_url` 和 `message` 判断原因：

- 临时网络、超时、正文异常、反爬验证：先只对对应 vendor 重新运行采集，例如 `--vendors openai`
- 来源配置需要调整：更新 `<skill_dir>/config/vendors.csv`，再只对对应 vendor 重新运行采集

## 2. 更新目标并生成待填 JSON

只处理当前 `run_dir`：

- `<skill_dir>/artifacts/<run_dir>/collected/pages/*.md`

先根据本次采集的 Markdown 更新目标表，再生成待填 JSON。目标表是跟踪对象身份的唯一来源；页面 URL 只在 `<skill_dir>/config/vendors.csv` 维护：

- API 目标表：`<skill_dir>/config/target_api_models.csv`
- 订阅目标表：`<skill_dir>/config/target_subscription_plans.csv`

目标表更新规则：

- 先整体查看两个目标表，确认当前跟踪范围，再逐个阅读 `<skill_dir>/artifacts/<run_dir>/collected/pages/*.md`，若 Markdown 正文异常、抽取错位或信息明显不全，可按 `vendor_key + region + track_type` 到 `<skill_dir>/config/vendors.csv` 找对应 `source_url`，并直接打开网页作为依据。
- 如果 Markdown 里出现目标表没有的新旗舰、新主力、新版本数字更新模型，或正式新套餐，必须先把对应记录加入目标表
- 新增目标默认 `required=true`、`is_active=true`，除非页面明确只是临时预告、不可购买或不计划跟踪
- 新目标只选当前官方价格表主推项
- 已有套餐新增月付、年付、促销价等计费周期时，在后续同一套餐对象的 `prices[]` 里补价格
- 读 Markdown 后确认目标已下线、官方移除或不再跟踪时，把目标表对应记录改为 `is_active=false`

目标表确认无误后再运行：

```bash
python <skill_dir>/scripts/sync_pricing.py --mode prepare
```

`prepare` 会按目标表更新当前 run 的两个待填写文件：

- `<skill_dir>/artifacts/<run_dir>/extracted/api_pricing.json`
- `<skill_dir>/artifacts/<run_dir>/extracted/subscription_plans.json`

它只追加缺失的模型 / 套餐对象，不覆盖已经填写的 `prices[]`。

## 3. 填写 JSON

打开并填写当前 run 的两个文件：

- `<skill_dir>/artifacts/<run_dir>/extracted/api_pricing.json`
- `<skill_dir>/artifacts/<run_dir>/extracted/subscription_plans.json`

填写依据：

- 只根据 `<skill_dir>/artifacts/<run_dir>/collected/pages/*.md` 里明确出现的信息填写
- 可参考上一轮已填写的 JSON，保持对象映射、`original_price_text` 写法、`notes` 风格和套餐/模型摘要的一致性
- 不得因为参考上一轮 JSON 而跳过本次 Markdown 核对，尤其是价格和模型
- 正常按 `pages/*.md` 填；只有当采集结果明显不可靠时，直接访问对应网页补齐
- 不猜测页面没有明确写出的价格、能力、周期或缓存费用
- 找不到就保持空数组、空字符串或不填，不要编造价格
- 保留 `source_url`、`original_price_text` 和必要 `notes`
- 不要改 `prepare` 已经预填的身份字段
- 如果填 JSON 期间又改了目标表，重新运行 `--mode prepare`

填写 `api_pricing.json`：

- 主要填写顶层 `notes` 和 `prices[]`
- `prices[]` 字段：`price_dimension`、`source_price_amount`、`currency`、`unit_basis`、`original_price_text`、`notes`
- API 价格统一采用基准价口径：官方公开按量付费、文本 token、标准在线推理价
- 不用免费层、试用额度、促销价、折扣价、预付包、资源包、专属实例、吞吐量包、批处理价或微调价，除非目标对象本身就是这些计费项
- 页面同时给原价、折扣价、优惠价时，优先取原价 / 标准价；如果页面只给当前成交价，在 `notes` 说明
- 页面按上下文长度、输入长度、输出长度分阶梯时，取页面顺序中的第一个基准阶梯，并把阶梯条件写进 `original_price_text`；`notes` 统一写 `基准阶梯价`
- 页面有文字、图片、音频、视频等多模态价格时，普通模型目标只取文字 token 价格；其他模态只在目标对象明确需要时填写
- 价格必须来自目标模型所在的同一标题、段落或表格块；相邻价格表不能借用。无法确认归属时保持 `prices[]` 为空，并在顶层 `notes` 写明疑点
- 每个目标模型按 `prices[]` 拆价格；常用维度是 `input`、`cached_input`、`output`
- 不适用缓存的厂商只填 `input`、`output`

填写 `subscription_plans.json`：

- 主要填写顶层 `features`、`plan_summary`、`notes` 和 `prices[]`
- `prices[]` 字段：`billing_cycle`、`source_price_amount`、`currency`、`unit_basis`、`seat_rule`、`original_price_text`、`notes`
- 月付、季付、年付、促销价等放在同一个套餐对象的多个 `prices[]` 里
- 套餐权益优先写入 `features[]`；如果需要人工整理摘要，再写 `plan_summary`

推荐词表：

- API `price_dimension`：`input`、`output`、`cached_input`、`cached_output`、`embedding`、`image`、`audio`、`other`
- API `unit_basis`：`per_1m_tokens`、`per_1k_tokens`、`per_image`、`per_minute`、`per_month`、`other`
- 订阅 `billing_cycle`：`monthly`、`quarterly`、`annual`、空
- 订阅 `unit_basis`：`per_month`、`per_user_month`、`per_year`、`per_user_year`、`per_quarter`、空
- `region`：优先用配置已有值，不自行发明新口径，除非页面明确出现且现有值无法表达

## 4. 构建与推送

运行：

```bash
python <skill_dir>/scripts/sync_pricing.py --mode build
```

`build` 会生成扁平 CSV，并把全量问题写到 `<skill_dir>/artifacts/<run_dir>/build_issues.csv`。

如果 `build_issues.csv` 里有能补齐的信息，修正后重新运行 `--mode build`。如果剩余问题是当前材料无法补齐的来源失败、页面未写价格或目标暂时缺价，保留 issue，继续推送。

推送：

```bash
python <skill_dir>/scripts/sync_pricing.py --mode push
```

`push` 同步最近一次 `build` 生成的数据。
