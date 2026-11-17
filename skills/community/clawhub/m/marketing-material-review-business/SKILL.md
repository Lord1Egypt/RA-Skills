---
name: marketing-material-review-business
description: 营销版面审核技能（对外版）- 从广告审核法务视角，对营销素材进行合规性审核。支持图片审核、风险点标注、修改建议。触发词：这个版面、详情页、主图、KT板、直播间文案、素材、文档帮我审核一下。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧾",
        "requires": { "bins": ["python3", "curl"], "env": ["BAIDU_API_KEY", "BAIDU_SECRET_KEY"] },
        "primaryEnv": "BAIDU_API_KEY",
      },
  }
---

# 营销版面审核技能（业务版）

> **版本**：v1.1.10（2026-08-02 改造）
> **更新日期**：2026-08-01
> **说明**：本版本基于公开法规与行业通用合规要点构建，适用于食品、乳制品、保健品等行业的营销素材合规审核参考。
> **v1.1 变更**：
> - 剥离内部合规指引与产品引证清单（references/ 从 22 个精简为 20 个）
> - 新增 `scripts/` 目录：标注图生成脚本 + 百度 OCR 含位置识别
> - 工具配置全部走环境变量，不内置任何 key
> - **v1.1.1 OCR 策略收敛**：只保留百度 OCR，降低安装成本和排障成本；外部 risks 已带 bbox 时跳过 OCR
> - **v1.1.2 Agent 协议收敛**：不在脚本中调用 OpenClaw/MiniMax 等平台 API；改为宿主 Agent 读取 payload 并输出统一 JSON
> - **v1.1.3 OpenClaw 运行优化**：声明百度 OCR 环境依赖，补充宿主输出目录约束，并避免 presentation 模式因缺少 key 标记误筛成 0 风险
> - **v1.1.4 运行入口优化**：新增 `scripts/run_review.py`，自动选择 skill 内 `.venv`、加载常见 env 文件、自检百度 OCR，再运行完整审核
> - **v1.1.5 防误用优化**：`self_check.py` 和 `auto_review.py` 被系统 `python3` 直接运行时，会自动切换到 skill 内 `.venv`
> - **v1.1.6 Agent 扩展审核升级**：新增 `--prepare-agent-review` 和 `*_agent_prompt.md`，强制宿主 Agent 基于 OCR 全文新增规则漏检风险；扩充食品/乳品常见风险规则
> - **v1.1.7 SkillHub 发布优化**：`scripts/run_review.py` 首次运行会在缺少依赖时自动创建 `.venv` 并安装 `requirements.txt`
> - **v1.1.8 发布环境加固**：依赖安装优先使用 CPython；skill 目录不可写时自动降级到用户缓存或临时目录
> - **v1.1.9 依赖引导修复**：已有虚拟环境但依赖不完整时自动补装，不再误判为可用环境
> - **v1.1.10 尺寸自适应优化**：按长图/横图/普通图自适应缩放、右栏宽高、字体和卡片排布；短图风险较多时自动增高画布

---

## 概述

从**资深广告审核法务**的专业角度，对营销版面素材进行全面的合规性审核。

### 核心能力

1. **图片审核** - 识别图片中的文字、图案、宣称是否符合广告法
2. **风险点标注** - 在原图上直接标注风险位置和说明
3. **修改建议** - 提供具体的修改方案
4. **长图审核** - 支持电商详情页、产品banner等纵向长图

### 标注图目标效果

标注图应优先做成“长图批注版”：

- 左侧保留原营销素材，按比例缩放，不裁切主体内容
- 风险点在原图对应位置用红/橙/绿框标出，并加编号圆点
- 右侧生成整高审核栏，按风险点在原图中的纵向位置排列卡片
- 每张卡片包含：编号、风险词/标题、风险等级、依据、判定理由、修改建议
- 长图默认输出约 1080px 宽，便于飞书/微信/浏览器查看
- 已有 `risks.json` 且包含 bbox 时，直接画框，不再重复调用 OCR

### 审核视角

采用**甲方（品牌方）视角**，重点保护品牌形象和合规安全：

- 严格遵循《广告法》及相关法规
- 识别极限词、虚假宣传、违规宣称
- 保护品牌知识产权
- 防范投诉举报风险

---

## 使用方式

### 触发审核

在飞书发送图片并说：
- "版面审核"
- "素材审核"
- "图片审核"
- "营销合规"

AI 助手将自动识别并返回审核结果。

### 审核范围

**可以审核的内容：**
- 产品包装设计图（罐装/袋装/盒装）
- 电商详情页/产品长图/banner
- 海报、宣传页
- 直播间背景板/贴片
- 朋友圈/社群宣传图

**不审核的内容（内部说明，不影响对外使用）：**
- 设计稿印刷说明（面向印刷厂的工艺说明）
- 图层/版权声明等设计规范文件

---

## 审核标准（核心规则）

### 一、极限词与绝对化用语

**禁止使用：**
- 最佳、最优、第一、顶级、顶尖
- 极致、至尊、臻品、完美
- 史无前例、前所未有
- 销量第一、市场领导者（需权威证明）
- "全网最低价"、"地板价"
- 万里挑一、独一无二

**合规替代：**
| 禁用表述 | 合规替代 |
|---------|---------|
| 销量第一 | 销量领先（注明数据来源） |
| 顶级品质 | 品质卓越 / 匠心品质 |
| 地板价 | 限时优惠 / 心动价 |
| 全网最低价 | 会员专享价 / 限时特惠 |

### 二、功能与功效宣称

**规范要求：**
- 普通食品不得宣称保健功能
- 不得使用医疗术语
- 不得暗示疾病治疗效果

**敏感词汇：**
- 肠道、肠胃、润肠、通便
- 增强免疫力、抗疲劳、抗氧化
- 消炎、杀菌、降血压

**合规替代：**
| 禁用表述 | 合规替代 |
|---------|---------|
| 守护肠道 | 好喝美味 |
| 增强免疫力 | 营养丰富 |
| 补铁补血 | 含铁丰富 |

### 三、引证广告（2026-06-12《广告引证内容执法指南》重点）

**重要变化：** 在引证广告中使用"最高级""最佳"，或销量、销售额、市场占有率"第一"等用语进行宣传的，**不属于《广告绝对化用语执法指南》第六条规定的豁免情形**。

**引证广告合规要求：**
1. 须标明引证机构名称（如"数据来源：XXX机构"）
2. 须标明适用范围（全国/某省/某行业）
3. 须标明有效期限
4. "最高级""最佳"在引证广告中不豁免
5. 萝卜坑式引证=虚假广告（以极窄限定条件支撑"第一"宣称）

### 四、0蔗糖/0添加/无糖宣称

**常见违规：**
- 标注"0蔗糖"但配料含结晶果糖、麦芽糖等糖类
- "0添加"后仍有其他添加剂
- "无糖"产品含代糖却未标注

**要求：** "0蔗糖"≠"无糖"；须与配料表严格一致

### 五、营养标签合规（GB 28050-2025）

**钙含量声称标准：**
| 声称方式 | 含量要求 |
|---------|---------|
| 钙来源 / 含钙 | ≥120mg/100g（固体）|
| 高钙 / 富含钙 | ≥240mg/100g（固体）|

**营养成分作用声称用语：**
- 不得删改、添加和合并标准用语
- 使用作用声称前必须符合含量声称的要求
- 不得利用作用声称夸大产品功效

### 六、食品标签强制项（GB 7718-2025）

| 强制标示项 | 说明 |
|-----------|------|
| 产品名称 | 与执行标准一致，不得误导 |
| 配料表 | 所有原料须列明 |
| 生产日期+保质期到期日 | 须明示，不得仅写"见包装" |
| 储存条件 | 须具体（如"冷藏2-6℃"）|
| 生产者/委托方信息 | 须与SC编号主体一致 |
| 致敏物质提示 | 8类强制标示（麸质/甲壳类/鱼/蛋/花生/大豆/乳/坚果）|

### 七、SC食品生产许可证编号

**格式：** SC + 14位数字（共17位）

**常见违规：**
- 使用旧QS编号（2018年已停用）
- SC编号类别与产品不符（如饮料用105乳制品编号）
- 冒用他人SC编号
- 委托加工未使用委托方SC编号

### 八、商品条码（GB 12904）

**核心原则：**
- 一物一码（不同规格/包装须独立GTIN）
- 厂商识别代码须在有效期内（2年）
- 委托加工须使用委托方厂商识别代码
- 条码符号等级≥C级

---

## 审核报告格式

### 风险等级说明

| 等级 | 标识 | 处理要求 | 典型情形 |
|------|------|---------|---------|
| 🔴 高风险 | 红色 | 必须改 | 绝对化用语、保健功能暗示、医疗功效宣称、科研机构背书、虚假数据 |
| 🟡 中风险 | 黄色 | 建议改 | 配方逻辑存疑、堆砌宣称、标注不规范、字体过小 |
| 🟢 低风险 | 绿色 | 注意合规 | 创意语过度表述、认证有效期需核 |

### 报告结构

```
## 版面审核报告

### 审核图片
- 文件名：xxx.png
- 审核时间：YYYY-MM-DD

### 风险等级分布
| 等级 | 数量 | 说明 |
|-----|------|------|
| 🔴 高风险 | N | 明确违规 |
| 🟡 中风险 | N | 建议修改 |
| 🟢 低风险 | N | 注意合规 |

### 风险详情

#### 🔴 风险点 1：[标题]
- **原文**：[逐字引用]
- **依据**：[法规条款]
- **判定**：[为什么违规]
- **改法**：[具体修改建议]

[继续列举...]

### 综合评价
[总结+后续操作建议]
```

---

## 知识库结构

```
references/
├── risk-rules.json             # 自动审核规则配置（关键词/等级/建议/模式）
├── compliance-rules.md         # 合规规则库（基于公开法规+案例）
├── forbidden-words.md          # 禁用词清单（100+词）
├── common-cases.md             # 常见审核案例
├── advertising-law.md           # 广告法核心条款
├── consumer-protection-law.md  # 消保法核心条款
├── promotion-regulations.md     # 促销行为管理规定
├── live-streaming-regulations.md # 直播法律法规
├── national-language-law.md     # 国家通用语言文字法（2026修订）
├── map-usage-rules.md          # 中国地图使用规范
├── barcode-compliance-rules.md # 商品条码合规规则
├── sc-food-production-license.md # SC食品生产许可证编号规范
├── food-category-standards.md  # 食品分类与执行标准对应表
├── gb-7718-2025-food-labeling.md # 预包装食品标签通则
├── gb-28050-2025-nutrition-labeling.md # 营养标签通则
├── gb-25190-2010-sterilized-milk.md # 灭菌乳标准
├── gb-19645-pasteurized-milk.md # 巴氏杀菌乳标准
├── gb-19301-2010-raw-milk.md  # 生乳标准
├── gb-24154-2015-sports-nutrition.md # 运动营养食品
├── gbt-32950-2016-fresh-agricultural-labels.md # 鲜活农产品标签标识
└── zhejiang-language-implementation.md # 浙江省语言文字实施办法
```

---

## 工具说明

### OCR / 脚本部署（可选）

业务版提供本地标注图生成脚本，OCR 统一使用百度 OCR 含位置接口，中文识别和坐标返回稳定。

**快速使用**：
```bash
# 方式 1：完整自动审核（推荐）
python3 scripts/run_review.py 图片.png

# 审核模式：balanced（日常默认）/ strict（全量初筛）/ presentation（业务交付重点版）
python3 scripts/run_review.py 图片.png --review-mode presentation --max-key-risks 14

# Agent 复核协议：manual 为本地兜底，只做规则直通，不等于完整智能审核
python3 scripts/run_review.py 图片.png --agent-mode manual

# 宿主 Agent 已输出 agent_risks.json 时，直接复用该结果画图和出报告
python3 scripts/run_review.py 图片.png --agent-risks-json agent_risks.json

# 复跑/调试：复用已有 OCR，避免重复消耗百度额度
python3 scripts/run_review.py 图片.png --ocr-json output/图片_ocr.json

# 长图 OCR：默认切片重叠 120px，降低切片边缘漏识别
python3 scripts/run_review.py 图片.png --slice-height 3200 --slice-overlap 120

# 方式 2：自动 OCR + 关键词匹配
python3 scripts/annotate_image.py 图片.png

# 方式 3：外部/人工审核结果 + 脚本画框
python3 scripts/annotate_image.py 图片.png 输出.png --risks risks.json
```

**OpenClaw 宿主运行约束**：
- 优先运行 `python3 scripts/run_review.py 图片路径 ...`，不要直接调用系统 `python3 scripts/auto_review.py` 或 `python3 scripts/self_check.py`；该入口会自动选择 skill 内 `.venv`，并先执行自检
- 环境自检使用 `python3 scripts/run_review.py --self-check`；需要实际调用百度 OCR 时使用 `python3 scripts/run_review.py --self-check --live`
- 输出目录不要放在 skill 安装目录、`scripts/`、`references/` 或 `work-tests/` 下；`run_review.py` 默认输出到 `~/.openclaw/workspace/output/marketing-material-review/<时间戳>/`
- 如果百度 OCR 环境变量缺失，必须先报告配置问题，不要用少量人工 OCR 代替完整 OCR 后声称“完整审核”
- OpenClaw service 不一定继承用户 shell 里的环境变量；推荐开启 `env.shellEnv.enabled=true`，或把 `BAIDU_API_KEY` / `BAIDU_SECRET_KEY` 写入 `~/.openclaw/.env` 后重启/重载
- 宿主 Agent 输出 `agent_risks.json` 时，重点交付风险需设置 `key: true` 或 `level: high`，否则 `presentation` 模式会过滤掉
- 用户要求“完整审核/自动化审核/用 skill 审核”时，不要把 `manual-rule-pass-through` 当成最终智能审核结果；必须走下面“两段式 Agent 扩展流程”

默认情况下，`risks.json` 里的 `bbox` 必须是**输入原图坐标**。如果 bbox 已经是缩放后输出图的坐标，运行时加：
```bash
python3 scripts/annotate_image.py 图片.png 输出.png --risks risks.json --bbox-space display
```

**推荐工作流（完整 Agent 审核成品）**：
1. 先运行 `run_review.py --prepare-agent-review` 完成百度 OCR、规则初筛、`*_agent_payload.json` 和 `*_agent_prompt.md`
2. 宿主 Agent 必须读取 `*_agent_prompt.md` 和 `*_agent_payload.json`，基于 OCR 全文新增规则漏检风险，写出 `agent_risks.json`
3. 再运行 `run_review.py --ocr-json ... --agent-risks-json agent_risks.json` 生成最终完整版和重点版批注图
4. 日常使用默认 `--review-mode balanced`；法务全量初筛用 `--review-mode strict`；业务交付用 `--review-mode presentation`
5. 复跑调试时传入 `--ocr-json`，只重跑规则、Agent 协议和画框，不重复调用百度 OCR
6. 对复杂争议点，再由人工/法务复核 `*_agent_risks.json` 或 `*_risks.json`
7. 如需精修，修改 `risks.json` 后运行 `annotate_image.py` 重新生成批注图

自动审核规则维护在 `references/risk-rules.json`。修改关键词、风险等级、依据、建议、适用模式或是否进入重点版时，优先改该 JSON，不改 Python。

Agent 复核是**宿主协议**，不是脚本里的平台 API 调用。当前内置 `manual` 本地兜底，不调用外部模型，只把规则候选规范化为统一 Agent 输出。OpenClaw、MiniMax、Codex 或其他类似平台使用这个 skill 时，应由该平台当前 Agent 读取 `*_agent_payload.json` 和 `template/agent-review-prompt.md`，结合 `references/` 知识库判断、合并、排除和新增风险，再写出 `agent_risks.json`，最后用 `--agent-risks-json` 复用结果生成图和报告。

建议的宿主 Agent 两段式流程：
```bash
# 第一步：生成 OCR、规则候选、Agent 输入材料和本次专用 prompt
python3 scripts/run_review.py 图片.png --output-dir output --prepare-agent-review

# 第二步：宿主 Agent 按 output/*_agent_prompt.md 读取 output/*_agent_payload.json，
#        必须执行 keep/exclude/adjust/merge/add，写出 agent_risks.json

# 第三步：复用 OCR 和 Agent 输出重新生成最终图和报告
python3 scripts/run_review.py 图片.png --output-dir output --ocr-json output/图片_ocr.json --agent-risks-json agent_risks.json
```

Agent 输入输出：
- `*_agent_payload.json`：图片信息、OCR 全文、规则候选、规则库和知识库摘要
- `*_agent_prompt.md`：本次任务专用宿主 Agent 提示，包含 payload 路径、输出路径和强制扩展审核要求
- `*_agent_risks.json` / `agent_risks.json`：宿主 Agent 确认/排除/合并/新增后的风险清单
- `template/agent-review-prompt.md`：宿主 Agent 必须遵循的复核提示和 JSON 输出格式

`risks.json` 建议字段：
```json
[
  {
    "id": 1,
    "word": "品类领导者",
    "bbox": [230, 420, 690, 560],
    "level": "high",
    "basis": "《广告法》第九条",
    "reason": "使用领导者类绝对化表述，需有充分权威依据。",
    "suggestion": "删除或改为客观描述，并补充数据来源。"
  }
]
```

**OCR 方案**：

| 模式 | 接口 | 适用 |
|------|------|------|
| `accurate` | 百度高精度含位置版 | 默认推荐，适合包装图、详情页、营销图 |
| `general` | 百度标准含位置版 | 成本/速度优先时可切换 |

**完整依赖安装**：
```bash
# 必要
pip install -r requirements.txt

# 推荐首选：百度 OCR 高精度含位置版（需注册 https://ai.baidu.com 拿 key）
export BAIDU_API_KEY="你的API Key"
export BAIDU_SECRET_KEY="你的Secret Key"
# 可选：accurate=高精度含位置版（默认），general=标准含位置版
export BAIDU_OCR_MODE="accurate"

# 安装自检
python3 scripts/self_check.py
# 实际调用百度 OCR 验证 key 和网络
python3 scripts/self_check.py --live
# OpenClaw/宿主平台推荐入口：自动用 .venv、加载常见 env、自检并输出到稳定目录
python3 scripts/run_review.py 图片.png
# 推荐自检入口：同样自动用 .venv，避免系统 Python 缺 Pillow/OpenCV
python3 scripts/run_review.py --self-check

```

**OCR 调度顺序**：
```
百度 OCR（默认高精度含位置版，可切标准含位置版）
```

> **设计原则**：只保留一个稳定 OCR 入口，降低安装成本和排障成本。需要完全离线时，可传入已有 `risks.json` + bbox 直接画框。

> **安全说明**：脚本不内置任何 API key。所有凭证通过环境变量注入。未配置环境变量时，自动 OCR 会明确报错；如果外部 `risks.json` 已带 bbox，则无需 OCR 也能直接生成标注图。

详细使用说明、参数说明、常见问题见 `scripts/README.md`。

### 本地审核脚本（可选）

如需离线批量审核，优先使用 `scripts/run_review.py`；只有明确知道 Python 环境和 OCR key 已配置时，才直接使用 `scripts/auto_review.py`：
```bash
python3 scripts/auto_review.py /path/to/image.png --review-mode balanced
```
完整文档：详见 `scripts/README.md`。

---

## 使用前提

1. **知识库更新**：本规则库基于 2026-07 前的法规版本，部分新规（如 GB 7718-2025 实施日期 2027-03-16）请以最新法规为准
2. **具体场景判断**：本审核为通用规则，具体产品/行业的特殊规定（如保健食品、婴幼儿配方乳粉）须参照专项法规
3. **标注图说明**：OCR 工具不可用时，提供纯文字版风险报告，不影响审核质量

---

## 典型案例参考

详见 `references/common-cases.md`，包含 30+ 实际审核案例，覆盖：
- 乳制品宣传违规案例
- 极限词使用案例
- 功能宣称违规案例
- 引证广告违规案例
- 营养标签违规案例
