---
name: migu-trip-agent
display_name: "🎒 咪咕旅游 - 智能行程规划"
description: 咪咕旅游智能规划助手。当用户说"去XX旅游"、"制定行程"、"规划旅游"、"景点推荐"、"自由行攻略"、"几天行程怎么安排"时自动调用。支持行程定制、行程调整、酒店景点美食推荐、简约行程、详细行程、路书生成等场景。运行时会通过用户本人在本地配置的登录凭证，访问第三方服务 gulangyu.migudm.cn 的 WebSocket/HTTPS 接口获取行程数据；脚本始终校验 TLS 证书，不会向用户索取或在输出/日志中回显 Token。
metadata:
  openclaw:
    emoji: "🎒"
    priority: 80
    intents:
      - trip_plan
      - travel_plan
      - itinerary
      - 旅游规划
      - 行程安排
      - 景点推荐
      - 简约行程
      - 详细行程
      - 路书生成
---

# 咪咕旅游智能行程规划

## 安全与网络行为说明

- 本 skill 通过 **WebSocket 与 HTTPS** 访问第三方服务 `gulangyu.migudm.cn` 获取行程数据，属于联网操作，不是纯离线生成。
- 鉴权使用**用户本人**的咪咕旅游登录 JWT。Agent **不得**向用户索取 Token 明文，也**不得**在回复或日志中回显 Token；Token 由用户本人在本地配置（详见「认证与 Token 配置」）。
- 脚本**始终启用 TLS 证书校验**，不提供关闭校验的选项；若出现证书错误，应排查本机证书/网络，而不是绕过校验。

## 核心功能

本 skill 提供以下核心功能：

1. **简约行程** - 快速生成行程概览，包含每日主题和关键景点
2. **详细行程** - 完整的日程规划，包含具体时间安排、交通、景点详情
3. **路书生成** - 生成可分享的完整旅行手册，包含美食推荐、住宿建议、注意事项
4. **行程调整** - 支持修改行程中的任意部分（景点、美食、住宿、交通）
5. **景点/酒店/美食推荐** - 根据用户偏好推荐目的地相关资源

## 何时使用

当用户提出以下需求时使用本 skill：

- 旅游行程规划：如"帮我规划去成都的旅游""规划北京三日游"
- 路线安排：如"从重庆去成都玩 3 天怎么安排"
- 行程调整：如"第二天不去公园""预算控制在 2000"
- 景点、酒店、美食推荐：如"成都有什么适合亲子的景点"
- 简约行程查询：如"给我一个简约行程""行程概览"
- 详细行程查询：如"详细行程是什么""每天具体怎么安排"
- 路书生成：如"生成路书""给我一份详细的旅行手册"
- 线上 `plan_multi` 返回 `summary_plan` 异常，需要 skill 侧兼容 fallback

## 输出格式说明

### 简约行程 (Summary Plan)

返回结构化的行程概览：

```json
{
  "summaryPlan": {
    "title": "重庆3日游",
    "days": 3,
    "theme": "山城探秘·美食之旅",
    "highlights": ["洪崖洞夜景", "武隆天坑", "火锅美食"],
    "daily_overview": [
      { "day": 1, "theme": "市区漫游", "key_spots": ["解放碑", "洪崖洞", "长江索道"] },
      { "day": 2, "theme": "武隆探秘", "key_spots": ["天生三桥", "龙水峡地缝"] },
      { "day": 3, "theme": "文艺打卡", "key_spots": ["磁器口", "李子坝", "南山一棵树"] }
    ],
    "budget": "2000-3000元/人",
    "best_season": "春秋季"
  }
}
```

### 详细行程 (Detailed Itinerary)

返回每日详细安排：

```json
{
  "detailedPlan": {
    "days": [
      {
        "day": 1,
        "date": "2026/06/10",
        "theme": "市区漫游",
        "schedule": [
          { "time": "09:00", "activity": "抵达重庆", "type": "交通" },
          { "time": "10:00", "activity": "解放碑商圈", "type": "景点", "duration": "2h", "tips": "美女聚集地，购物天堂" },
          { "time": "12:00", "activity": "八一好吃街午餐", "type": "美食", "duration": "1h", "recommend": "酸辣粉、小面" },
          { "time": "14:00", "activity": "长江索道", "type": "景点", "duration": "1h", "tips": "北站→南站，俯瞰两江" },
          { "time": "16:00", "activity": "洪崖洞", "type": "景点", "duration": "2h", "tips": "宫崎骏千与千寻取景地" },
          { "time": "19:00", "activity": "千厮门大桥夜景", "type": "景点", "duration": "1h", "tips": "最佳拍照位置" },
          { "time": "20:00", "activity": "老火锅晚餐", "type": "美食", "duration": "1.5h", "recommend": "老灶火锅" }
        ],
        "meals": { "breakfast": "自理", "lunch": "八一好吃街", "dinner": "老火锅" },
        "accommodation": "解放碑附近酒店"
      }
    ]
  }
}
```

### 路书生成 (Travel Guide)

生成完整的旅行手册：

```json
{
  "travelGuide": {
    "title": "重庆3日游完整路书",
    "overview": {
      "destination": "重庆",
      "days": 3,
      "best_season": "春秋季",
      "budget": "2000-3000元/人",
      "highlights": ["8D魔幻夜景", "正宗火锅", "武隆天坑"]
    },
    "preparation": {
      "best_time": "3-5月、9-11月",
      "weather": "春秋宜人，夏季炎热多雨",
      "clothing": "舒适运动鞋（山城步道多）、轻薄外套",
      "items": ["防晒霜", "雨伞", "充电宝", "肠胃药"]
    },
    "daily_guide": [
      {
        "day": 1,
        "title": "山城初体验",
        "route": "解放碑 → 八一好吃街 → 长江索道 → 洪崖洞 → 千厮门大桥",
        "highlights": [
          { "spot": "解放碑", "time": "2h", "intro": "重庆地标，美女美食聚集地" },
          { "spot": "长江索道", "time": "1h", "intro": "空中横跨长江，20元体验山城交通" }
        ],
        "food": [
          { "meal": "午餐", "place": "八一好吃街", "recommend": "酸辣粉、豌杂小面" },
          { "meal": "晚餐", "place": "洪崖洞附近", "recommend": "老火锅" }
        ],
        "tips": ["轻轨1号线直达解放碑", "索道建议南站上北站下", "洪崖洞19:00后夜景最美"]
      }
    ],
    "practical_info": {
      "transport": {
        "external": ["江北机场", "重庆北站", "重庆西站"],
        "internal": "轻轨/地铁最方便，支付宝扫码乘车"
      },
      "accommodation": {
        "areas": ["解放碑", "观音桥", "南滨路"],
        "recommend": "解放碑附近最方便"
      },
      "emergency": {
        "police": "110",
        "medical": "120",
        "tourism_hotline": "12301"
      }
    }
  }
}
```

## 展示格式规范（必须严格遵循）

**为保证不同大模型输出稳定性，Agent 必须按以下固定格式渲染行程，禁止自行发挥总结。**

### 1. 简约行程展示格式

**必须使用以下结构，严格按顺序渲染：**

```
## [行程标题] 🎯

| 天数 | 主题 | 城市 | 推荐景点 | 推荐美食 | 住宿 |
|------|------|------|----------|----------|------|
| DayX | [主题] | [城市] | [景点1]、[景点2] | [美食] | [酒店] |
| ... | ... | ... | ... | ... | ... |

📅 **行程时间**：YYYY/MM/DD - YYYY/MM/DD（共X天X晚）
💰 **预算参考**：[预算范围](如有）

💡 **如需调整，可以这样告诉我：**
- 「第一天住豪华酒店」
- 「最后一天吃肯德基」

---

这是简约行程。需要我继续为您生成每天的详细时间安排、交通与游玩细节吗？
```

**展示顺序（不可打乱）：** 先表格与时间/预算 → **必须**输出「如需调整」两条示例 → **必须**输出详细行程追问句。

**字段来源（必须从 summaryPlan 中提取）：**
- `行程标题`：从 `行程概览表[*].所在城市` 拼接，如 "成都+重庆4日游"
- `天数`：从 `行程总结.天数`
- `主题`：从 `行程概览表[*].行程主题`
- `城市`：从 `行程概览表[*].所在城市`
- `推荐景点`：从 `行程概览表[*].推荐景点[*].名称`，取前2个用"、"连接
- `推荐美食`：从 `行程概览表[*].推荐美食`
- `住宿`：从 `行程概览表[*].住宿推荐`
- `行程时间`：从 `行程总结.出发日期` 和 `行程总结.返回日期`
- `预算参考`：从 `行程总结.最高预算` 或 `行程总结.最低预算`

---

### 2. 详细行程展示格式

**必须按以下顺序输出：总览 → 每日详情 → 出行准备 → 伴手礼**

#### 2.1 行程总览

```
## 📋 行程总览

🎯 **目的地**：[目的地]
📅 **时间建议**：X天X晚
👥 **适合人群**：[人群]
🔑 **关键词**：[关键词1]、[关键词2]、...
🔥 **热门景点**：X个
🍜 **热门美食**：X个
```

**字段来源（必须从 detailedPlan.简介 中提取）：**
- `目的地`：从 `目的地`
- `时间建议`：从 `时间建议`
- `适合人群`：从 `适合人群`
- `关键词`：从 `关键词`（数组用"、"连接）
- `热门景点个数`：从 `景点数量`
- `热门美食个数`：从 `美食数量`

#### 2.2 每日详细行程

**每天必须包含：景点详情、美食详情、酒店详情**

```
### 🏙️ Day X（日期 周X）- 城市：主题

#### 🎫 景点详情
| 景点 | 评分 | 景区级别 | 营业时间 | 简介 | 游玩贴士 |
|------|------|----------|----------|------|----------|
| [名称] | ⭐X.X | AAAA景区 | HH:MM-HH:MM | [简介] | [tips] |
| ... | ... | ... | ... | ... | ... |

#### 🍜 美食详情
| 餐次 | 餐厅 | 推荐菜 | 人均 |
|------|------|--------|------|
| 早餐 | [餐厅] | [推荐菜] | XX元 |
| 午餐 | [餐厅] | [推荐菜] | XX元 |
| 晚餐 | [餐厅] | [推荐菜] | XX元 |

#### 🏨 酒店详情
| 酒店 | 星级 | 地址 | 特色 |
|------|------|------|------|
| [名称] | ⭐⭐⭐⭐ | [地址] | [特色] |

#### ⏰ 详细时间表
| 时间 | 活动 | 类型 | 备注 |
|------|------|------|------|
| HH:MM | [活动] | 交通/景点/美食 | [备注] |
| ... | ... | ... | ... |
```

**字段来源说明：**
- 景点详情：从 `schedule` 中 type=景点 的项目，提取 name、评分（ rating 或 score）、景区级别（level 或 景区级别）、营业时间（营业时间或 open_time）、简介（intro 或 简介）、游玩贴士（tips 或 游玩贴士）
- 美食详情：从 `meals` 和 `schedule` 中 type=美食 的项目
- 酒店详情：从 `accommodation`
- 时间表：从 `schedule[*].time`、`.activity`、`.type`、`.tips`

#### 2.3 出行准备清单

**只输出接口字段 `detailedPlan.出行准备清单`，原样展示，禁止改写、禁止归类、禁止补充。**

```
## 🎒 出行准备清单

[将 detailedPlan.出行准备清单 数组中的每一项各占一行，原文输出，保留接口中的 ✅ 等符号]
```

示例（接口返回为字符串数组时）：

```
## 🎒 出行准备清单

- ✅ 证件：身份证、银行卡、少量现金、有效优惠证件（如学生证、老年证）。
- ✅ 穿搭：……
- ✅ 装备：……
- ✅ 药品：……
```

**禁止：**
- 不要输出「注意事项」小节（接口无此字段，Agent 不得自行添加）
- 不要拆成「必备物品 / 衣物建议 / 注意事项」等自编分类
- 不要用 checkbox `[ ]` 替换接口里的 `✅` 文案

**字段来源：** `detailedPlan.出行准备清单`（`string[]`，逐条原样）

#### 2.4 伴手礼推荐

```
## 🎁 伴手礼推荐

| 城市 | 特产 | 推荐购买地 | 参考价格 |
|------|------|------------|----------|
| 成都 | 郫县豆瓣酱 | 超市/景区特产店 | 20-50元 |
| 成都 | 竹叶青茶 | 茶厂/商场 | 100-300元 |
| 重庆 | 火锅底料 | 超市/磁器口 | 20-80元 |
| 重庆 | 江津米花糖 | 商场/特产店 | 15-30元 |
```

**字段来源（必须从 detailedPlan 中提取）：**
- 景点详情：从 `schedule` 中 type=景点 的项目，提取 name、评分、景区级别、营业时间、简介、游玩贴士（tips）
- 美食详情：从 `meals` 和 `schedule` 中 type=美食 的项目
- 酒店详情：从 `accommodation`
- 时间表：从 `schedule[*].time`、`.activity`、`.type`、`.tips`

---

### 3. 路书展示格式

**直接输出图片链接，禁止生成文字描述：**

```
🖼️ **旅行路书**：[点击查看](图片URL)
```

---

### 4. 通用规则

- **禁止**在渲染时自行添加模型总结（如"这一天主要安排是..."）
- **禁止**省略或合并字段，必须完整展示所有必填字段
- **禁止**改变表格列顺序或格式
- 如某字段为空，输出"自理"或"待定"，不能留空
- 表情符号和 Emoji 按上述格式使用，不可自行增减
- **简约行程**：表格展示结束后，**必须**附带「第一天住豪华酒店」「最后一天吃肯德基」式微调引导，再追问是否生成详细行程
- **详细行程**：`出行准备清单` 仅原样输出接口数组；**不得**出现「注意事项」或自编清单分类

---

## OpenClaw 使用原则

OpenClaw 里不要用交互终端模式 `-i`。OpenClaw exec 没法稳定回答脚本里的 readline 表单提示。

正确流程是三段式逐步生成，不能一开始就问用户要生成哪一种：

1. Agent 在对话里只收集必填行程信息。
2. 必填信息齐全后，立即写入 `plan_form.json`，设置 `plan_type: "summary"`，单轮执行 `--trip-plan-direct --plan-form-file` 生成**简约行程**。
3. 展示简约行程后，只引导用户是否生成**详细行程**。
4. 用户确认需要详细行程后，**不要**再跑 WebSocket；用 `scripts/create_detail.mjs` + 当前 `session-file` 调 HTTP 接口生成。
5. 展示详细行程后，再引导用户是否需要**生成路书**。
6. 用户确认需要路书后，执行 `scripts/get_roadbook.mjs` 生成路书。

除非用户一开始明确说“只要详细行程”或“直接生成路书”，否则默认都从简约行程开始。

## 前置检查：Token 配置状态

**【关键逻辑】在任何行程规划之前，Agent 必须先检查 Token 是否已配置：**

1. **检查 Token 文件是否存在**：
   - Windows: `C:\Users\ll\.openclaw\workspace\skills\migu-trip-agent\secrets\plan_multi_token.txt`
   - Linux/Mac: `~/.openclaw/workspace/skills/migu-trip-agent/secrets/plan_multi_token.txt`

2. **Token 不存在时的处理**：
   - **禁止**尝试调用脚本生成行程
   - **禁止**自行手写或编造行程内容
   - **必须**读取「📌 用户配置 Token 指引模板」章节，原文返回给用户（模板会指引用户本人在本地配置，不要在对话里索取 Token）
   - 示例：读取 SKILL.md 中该模板章节后，原样返回给用户

3. **Token 存在但可能过期**：
   - 先执行 `--check-token --probe-auth` 预检
   - 如果 probe 失败，根据错误类型提示用户（见「认证与 Token 配置」章节）

---

## 需要向用户收集的信息

必填，缺一项就继续追问，不要执行脚本：

- 目的地：例如 `重庆市`
- 日期：开始日期和返回日期，格式 `YYYY/MM/DD`
- 人数：例如 `2成人、0儿童`

选填，用户没说可以留空：

- 出发地
- 预算
- 交通方式

推荐追问话术：

```text
为了生成简约行程，请先告诉我：目的地、出行日期（出发/返回，YYYY/MM/DD）、人数（几大几小）。
如有也可以补充：出发地、预算、交通方式；没有可以不说。
```

必填信息收集完整后，不再追问“生成简约/详细/路书哪一种”，直接生成简约行程。

## plan_form.json

最小可用示例：

```json
{
  "destinations": ["重庆市"],
  "cities": ["重庆市"],
  "people": 2,
  "people_type": "2成人、0儿童",
  "start_date": "2026/06/10",
  "return_date": "2026/06/12",
  "days": 3,
  "city_days": {},
  "plan_type": "summary"
}
```

`plan_type` 可选值：
- `summary` - 简约行程，必填信息齐全后默认使用
- `detailed` - **不要**用于 WebSocket；详细行程请用 `scripts/create_detail.mjs`
- `guide` - 路书，不走 `plan_multi`，确认后调用 `scripts/get_roadbook.mjs`

不要使用 `all` 作为默认值，避免一次性生成全部内容。

带选填项示例：

```json
{
  "departure": "成都市",
  "departure_city": "成都市",
  "destinations": ["重庆市"],
  "cities": ["重庆市"],
  "people": 2,
  "people_type": "2成人、0儿童",
  "min_budget": "",
  "max_budget": "3000",
  "travel_mode": "高铁",
  "start_date": "2026/06/10",
  "return_date": "2026/06/12",
  "days": 3,
  "city_days": {},
  "plan_type": "summary"
}
```

`days` 按开始日期和返回日期自然日计算，包含首尾两天。

## 分阶段生成话术

**重要：所有展示必须严格遵循「展示格式规范」章节的规定格式，不允许 agent 自行发挥。**

### 阶段 1：简约行程

当目的地、日期、人数齐全时，直接执行脚本生成简约行程。

**展示格式**：严格按「简约行程展示格式」渲染（见上一章节），其中已包含：

1. 行程表格与时间/预算  
2. **必须**展示的微调引导（固定示例，勿删改）：
   - 「第一天住豪华酒店」
   - 「最后一天吃肯德基」
3. 详细行程追问句：「这是简约行程。需要我继续为您生成每天的详细时间安排、交通与游玩细节吗？」

**禁止**只展示表格而不输出微调引导；**禁止**在简约行程阶段输出「注意事项」或路书引导。

### 阶段 2：详细行程

只有当用户确认“需要/继续/生成详细行程”时，执行（**专用 HTTP 接口，不是 plan_multi WebSocket**）：

```bash
node scripts/create_detail.mjs \
  --token-file "$HOME/.openclaw/workspace/skills/migu-trip-agent/secrets/plan_multi_token.txt" \
  --session-file "$HOME/.openclaw/workspace/plan_multi_session.txt" \
  --json
```

- URL：`POST https://gulangyu.migudm.cn/trip-agent-api/api/plan/create_detail`
- Body：`{"session_id":"<上一步 session-file 中的 UUID>"}`
- 成功时 JSON 含 `detailedPlan`（结构含 `简介`、`每日行程` 等）
- 前置条件：该 `session_id` 已在服务端有 **简约行程 summary_plan**（阶段 1 完成后自动入库）

**禁止**把 `plan_form.plan_type` 设为 `detailed` 再跑 `--trip-plan-direct`（会失败或只返回 summary_plan）。

**展示格式**：严格按「详细行程展示格式」渲染（见上一章节）。其中 **2.3 出行准备清单** 必须原样输出 `detailedPlan.出行准备清单`，**不要**输出「注意事项」。

展示详细行程末尾必须追问（必须使用以下固定话术）：

```text
详细行程已生成。需要我继续为您生成可分享的路书吗？
```

### 阶段 3：路书

只有当用户看完详细行程并确认需要路书时，才执行 `scripts/get_roadbook.mjs`。

路书接口请求体**只有** `session_id`（与线上一致）：

```json
{
  "session_id": "82f9c807-2a0d-4a59-ab5a-5ea67ee7986d"
}
```

- URL：`POST https://gulangyu.migudm.cn/trip-agent-api/road/book/pic/make`
- Header：`Authorization: Bearer <JWT>`
- 若返回 `{"code":-1,"msg":"fail"}`：说明该 `session_id` 下**还没有详细行程**（不是参数名写错）。须先调详细行程接口，再生成路书。

**推荐命令**（脚本会先 `create_detail`，再 `pic/make`）：

```bash
node scripts/get_roadbook.mjs \
  --token-file "$HOME/.openclaw/workspace/skills/migu-trip-agent/secrets/plan_multi_token.txt" \
  --session-file "$HOME/.openclaw/workspace/plan_multi_session.txt" \
  --verbose
```

若详细行程已在 H5/上一轮生成完成，可加 `--skip-create-detail` 只打路书接口。

`session_id` 必须来自**同一次**简约/详细行程规划写入的 `plan_multi_session.txt`，且与当前 token 同一登录用户；否则会 `400 没有查询到会话详情` 或 `code=-1 fail`。

**展示格式**：严格按「路书展示格式」渲染（见上一章节），直接输出图片链接。

## 输出处理

脚本加 `--json` 后，Agent 优先读取：

- `summaryPlan`：简约行程
- `detailedPlan`：详细行程
- `travelGuide`：路书
- `answer`：服务端自然语言回复
- `content`：可直接展示的文本
- `sessionId`：后续调整行程时复用

**⚠️ 重要：Agent 必须将上述 JSON 数据按「展示格式规范」章节的固定格式渲染给用户，禁止自行总结或改变表格结构。**

## 行程调整

用户要求调整已有行程时：

1. 读取上一次的 `plan_form.json`。
2. 只修改用户明确要求变更的字段。
3. 保留 `session-file`，继续同一会话。
4. 再次执行 `--trip-plan-direct --plan-form-file`。

常见调整：

- "第二天吃肯德基"：在 question 中保留调整意图
- "预算控制在 2000"：更新 `max_budget`
- "改成 4 天"：更新 `return_date` / `days`
- "只要简约行程"：设置 `plan_type: "summary"`
- "继续生成详细行程"：执行 `scripts/create_detail.mjs`（保留 `session-file`）
- "生成路书"：不要再调用 `plan_multi`，执行 `scripts/get_roadbook.mjs`

## 认证与 Token 配置

本 skill 需要调用咪咕旅游（第三方服务 `gulangyu.migudm.cn`）的 WebSocket / HTTPS 接口，接口鉴权使用**用户自己的**登录 JWT。

**安全边界（必须遵守）：**
- **不得**要求用户在对话中发送、粘贴或以任何形式提供 Token 明文；**不得**主动向用户索取 Token。
- **不得**把 Token 写入日志、聊天回复、代码或提交内容。
- Token 由**用户本人在本地**配置（环境变量或用户自己的凭据文件）。Agent 只读取脚本输出的“可用/过期”结论，不接触 Token 明文。

### 保存路径（固定）

- Windows：`C:\Users\ll\.openclaw\workspace\skills\migu-trip-agent\secrets\plan_multi_token.txt`
- Linux/Mac：`~/.openclaw/workspace/skills/migu-trip-agent/secrets/plan_multi_token.txt`

**禁止**用飞书/Markdown 手改文件（极易改坏 1 个字符导致 401）。请由**用户本人**在自己的终端里配置：

```powershell
# 建议由用户本人执行，不要把 Token 发到聊天里
cd C:\Users\ll\.openclaw\workspace\skills\migu-trip-agent
$env:PLAN_MULTI_TOKEN | node scripts\plan_multi_ws_client.mjs --save-token-stdin
```

⚠️ **注意**：无需提供手机号；Token 属于用户个人凭据，只保存在本机。

`--save-token-stdin` 写入后会自动 `--probe-auth` 校验，只输出 `probe: WebSocket auth OK` 等结论，**不会回显 Token**；**只有 probe OK 才能继续规划**。

### 执行前预检

```bash
node scripts/plan_multi_ws_client.mjs --check-token --probe-auth --token-diagnostics
```

- 退出码 `0` + `probe: WebSocket auth OK`：可用
- 退出码 `2`：未配置或 JWT 形态错误
- 退出码 `3`：**不要笼统说“token 过期”**，先看 stderr 的 `exp=... expired=false`：
  - `expired=false` 且 401 → **token 文件保存时被损坏**，请用户本人在本地重新配置（`--save-token-stdin`）覆盖
  - `expired=true` → JWT 真的过期，由用户本人重新登录 H5 获取新 token 并在本地更新

**Agent 禁止**根据猜测告诉用户“2024年2月过期”；必须以脚本输出的 `exp=` 和 `expired=` 为准。

### 用户如何获取自己的 Token（仅用户本人在本地操作）

用户如需在本地配置自己的登录 JWT，可在**自己的浏览器/电脑**上按以下步骤获取，并由用户本人通过环境变量或凭据文件提供给脚本：

1. 浏览器打开 [咪咕旅游 H5](https://gulangyu.migudm.cn/multi-city-trip-agent/) 并用手机号登录。
2. 按 F12 打开开发者工具 → 切换到 **Network** 标签。
3. 刷新页面。
4. 找到 WebSocket 请求（显示为 `WS`），从 **Headers** 的 `token=xxx` 复制整段 Token。
5. 或者找到 https 请求，从 **Headers** 的 `Authorization: Bearer xxx` 复制整段 Token。
6. 或在 **Application**（应用）标签 → **Local Storage** 中查找 `vue3_h5_template_user` 键里面的apiToken值。

**Token 特征**：一长串字符，以 `eyJ` 开头

**⚠️ 重要**：
- Token 属于**用户个人凭据**：请勿发送给任何人，**包括本 Agent**。本 skill 不会向用户索取 Token 明文，也不会在回复或日志里回显。
- 获取后请由用户本人写入本地配置；Token 有效期约7天，过期后由用户本人重新获取并更新。

---

## 📌 用户配置 Token 指引模板（必须原文引用）

**当 Token 不存在时，Agent 必须读取以下内容并原文返回给用户，禁止自行改写：**

> 您好！检测到本机还没有配置咪咕旅游的登录 Token，暂时无法为您生成行程。
>
> 出于安全考虑，**请不要把 Token 发到聊天里**，请由您本人在自己的终端配置（任选其一）：
>
> 1. 设置环境变量后重试（Windows）：`setx PLAN_MULTI_TOKEN "<你的JWT>"`，然后新开一个终端。
> 2. 或把 JWT 写入本地凭据文件（见「认证与 Token 配置」章节的自助配置命令）。
>
> 若您还没有 Token，可在**您自己的浏览器**里获取（方法见下）；配置好之后告诉我，我继续为您生成行程 ~
>
> ---
>
> 📱 **自行获取 Token 方法（请勿分享给他人）**：
>
> 1. 浏览器打开 [咪咕旅游 H5](https://gulangyu.migudm.cn/multi-city-trip-agent/) 并用手机号登录
> 2. 按 F12 打开开发者工具 → 切换到 **Network** 标签
> 3. 刷新页面
> 4. 找到 WebSocket 请求（显示为 `WS` 开头），从 **Headers** 的 `token=xxx` 复制整段 Token
> 5. 或者找到 https 请求，从 **Headers** 的 `Authorization: Bearer xxx` 复制整段 Token
> 6. 或在 **Application**（应用）标签 → **Local Storage** 中查找 `vue3_h5_template_user` 键里面的 `apiToken` 值
>
> ⚠️ Token 是一长串字符（以 `eyJ` 开头），属于您的个人凭据：**请勿发送给任何人（包括助手）**，只在您本机配置即可。


## 推荐执行命令

```bash
cd ~/.openclaw/workspace/skills/migu-trip-agent
node scripts/plan_multi_ws_client.mjs \
  --token-file "$HOME/.openclaw/workspace/skills/migu-trip-agent/secrets/plan_multi_token.txt" \
  --bearer \
  --trip-plan-direct \
  --plan-form-file "$HOME/.openclaw/workspace/plan_form.json" \
  --session-file "$HOME/.openclaw/workspace/plan_multi_session.txt" \
  --fallback-trip-plan \
  --json \
  --log-file "./ws-openclaw.jsonl"
```

Windows PowerShell：

```powershell
cd C:\Users\ll\.openclaw\workspace\skills\migu-trip-agent
node scripts\plan_multi_ws_client.mjs `
  --token-file "$env:USERPROFILE\.openclaw\workspace\skills\migu-trip-agent\secrets\plan_multi_token.txt" `
  --bearer `
  --trip-plan-direct `
  --plan-form-file "$env:USERPROFILE\.openclaw\workspace\plan_form.json" `
  --session-file "$env:USERPROFILE\.openclaw\workspace\plan_multi_session.txt" `
  --fallback-trip-plan `
  --json `
  --log-file ".\ws-openclaw.jsonl"
```

⚠️ **注意**：所有命令均**不需要**提供手机号，Token 本身已包含用户身份信息。
