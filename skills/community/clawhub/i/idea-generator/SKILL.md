---
name: idea-generator
description: 创意工作台启动器。当用户说「启动创意工作台」「打开工作台」「开启工作台」时激活。负责启动工作台服务并返回访问链接，创意生成由用户在工作台网页中操作。
---

# Idea Generator - 创意工作台启动器

## 激活后执行以下步骤

### 第 1 步：检查服务是否已在运行

```bash
curl -s http://localhost:50000/ > /dev/null 2>&1 && echo "RUNNING" || echo "STOPPED"
```

### 第 2 步：如果未运行，自动启动

输出 `STOPPED` 时执行：

```bash
for SKILL_DIR in \
  "$HOME/openclaw/workspace/skills/idea-generator" \
  "$HOME/.openclaw/skills/idea-generator"
do
  [ -f "$SKILL_DIR/scripts/server.py" ] && break
done
cd "$SKILL_DIR/scripts" && nohup python3 server.py > server.log 2>&1 &
sleep 2
```

输出 `RUNNING` 时跳过此步。

### 第 3 步：回复用户

```
🎨 创意工作台已启动！

请在浏览器打开：http://localhost:50000/live-dashboard.html

在工作台中输入创意主题和需求，点击「开始生成」即可。
```

**到此结束，不执行任何创意生成流程。**

---

## 创意生成流程（由工作台触发，非对话触发）

工作台网页点击「开始生成」后，会通过 cron 任务唤醒 AI 执行创意生成。AI 收到唤醒后：

### 第 1 步：状态门控（必须最先执行）

```bash
curl -s http://localhost:50000/state.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
status = d.get('status', 'idle')
if status == 'running':
    print('GO')
    print('主题:', d.get('topic', ''))
    print('需求:', d.get('demand', ''))
    print('轮数:', d.get('rounds_count', 3))
else:
    print('ABORT:', status)
"
```

- 输出以 `GO` 开头 → 读取主题/需求/轮数，进入创意生成
- 输出以 `ABORT` 开头 → **立即终止，回复「任务已取消」，不做任何操作**

> 🔴 状态不是 `running` 就必须停止，这是硬性约束。

### 第 2 步：读参考文件

| 文件 | 内容 | 路径 |
|------|------|------|
| 创意生成标准 | 冲击波创意专家人设、核心心法、风格参考、输出格式 | `references/creative-standards.md` |
| 评分标准详解 | 四维评分体系、维度说明、分级反馈策略、评分示例 | `references/scoring-guide.md` |

### 第 3 步：核心流程（N 轮迭代）

**严格按 `rounds_count` 执行轮数（默认 3）。每轮必经以下步骤，轮次间承接递进。**

```
第N轮：
  [1] 分析需求（读取上一轮反馈，首轮无，规划搜索词条，搜索词条不要过泛，要注意聚焦某个洞察或优秀案例。其次读取上一轮反馈后，不能钻牛角尖，而是发散思维进行创作，不要只限制于某个方向死钻）
  [2] 网络搜索（百度 + B站，必须真实调用，搜索词条不要过泛，要注意聚焦某个洞察或优秀案例）
  [3] 生成创意（5个，去重）
  [4] 筛选评分（≥90分入围）
  [5] 记录反馈（沉淀至下一轮）
```

---

## 搜索规则

### ⛔ 绝对禁止伪造

所有搜索发现必须来自工具的实际返回内容，禁止凭空捏造任何趋势、数据或用户观点。

### 搜索方案（优先方案A）

**方案A：browser（推荐）**

每个平台的完整流程：
1. `browser(action=open, url=搜索URL)` → 记录返回的 `targetId`
2. `exec sleep 2` → 等待加载
3. `browser(action=snapshot, targetId=<targetId>)` → 提取真实内容
4. `POST /log/search` → 记录搜索结果
5. `browser(action=close, targetId=<targetId>)` → **立即关闭**，不保留

> 🔴 **每次搜索用完立即关闭标签页**，不复用，不积累。每轮搜索 2 个平台 = 打开 2 个、关闭 2 个。

**方案B：web_fetch（browser 不可用时）**

```
web_fetch(url=搜索URL, maxChars=2000) → 提取内容 → POST /log/search
```

### 搜索平台

| 平台 | URL |
|------|-----|
| 百度 | `https://www.baidu.com/s?wd={关键词}` |
| B站 | `https://search.bilibili.com/all?keyword={关键词}` |

### 搜索记录格式

```json
{
  "round": 0,
  "kw": "搜索关键词",
  "findings": "搜索发现（≥30字，来自真实返回内容）",
  "platform": "平台名"
}
```

---

## 创意输出格式

```json
{
  "发现": "创意基于的消费者洞察、社会现象、数据或趋势（≤50字）",
  "创意": "一句话核心创意（≤11字），简洁有力易记",
  "创意描述": "不超过三句话：如何执行、为何有效、解决什么营销问题"
}
```

> 详细创意心法和风格参考见 `references/creative-standards.md`

---

## 评分标准（概要）

**四维冲击波评分（满分 100）：**

| 维度 | 满分 |
|------|------|
| 冲击波特质（事件化/反套路/情感共鸣/可视化） | 40 |
| 话题传播力（可分享性/参与门槛/延展空间） | 25 |
| 营销效果（需求匹配/行动召唤/转化潜力） | 25 |
| 可执行性（资源投入/风险可控） | 10 |

**入围标准：总分 ≥ 90，且冲击波特质 ≥ 35**

> 详细评分规则和分级反馈策略见 `references/scoring-guide.md`

---

## 轮次承接规则

- **第 1 轮**：分析原始需求，搜索洞察，生成 5 个候选，评分筛选，记录反馈
- **第 N 轮**：在思考中明确写出「承接第 N-1 轮反馈：...」，用新关键词搜索，生成 5 个新候选（去重），评分筛选，记录反馈

**创意去重：**
- 与已有创意相似度 > 60% → 评分时降权
- 相似度 > 80% → 直接过滤，不进入评分

---

## API 端点（http://localhost:50000）

| 端点 | 作用 |
|------|------|
| `POST /init` | 初始化任务 |
| `POST /round/start` | 开始轮次（参数：`round`, `theme`） |
| `POST /log/thinking` | 记录思考（参数：`round`, `content`） |
| `POST /log/search` | 记录搜索发现 |
| `POST /idea/add` | 添加创意（参数：`round`, `ideas`） |
| `POST /idea/evaluate` | 评分筛选（参数：`round`, `evaluations`） |
| `POST /round/feedback` | 本轮反馈（参数：`round`, `content`） |
| `POST /done` | 完成任务 |

### 🔴 轮次编号规则（重要）

**round 参数从 0 开始：**
- 第 1 轮 → `round=0`
- 第 2 轮 → `round=1`
- 第 3 轮 → `round=2`

> 这是数组索引，不是人类习惯的编号。如果传错会导致过程从第二轮开始显示。

### API 调用示例（必须严格遵循）

#### 1. 开始轮次 `/round/start`
```json
{
  "round": 0,  // 第1轮用0，第2轮用1，第3轮用2
  "theme": "本轮主题"
}
```

#### 2. 记录思考 `/log/thinking`
```json
{
  "round": 0,
  "content": "本轮分析思路..."
}
```

#### 3. 记录搜索 `/log/search`
```json
{
  "round": 0,
  "kw": "搜索关键词",
  "findings": "搜索发现（≥30字）",
  "platform": "百度"
}
```

#### 4. 添加创意 `/idea/add`
```json
{
  "round": 0,
  "ideas": [
    {
      "发现": "洞察描述（≤50字）",
      "创意": "创意名称（≤11字）",
      "创意描述": "执行方式+有效性+解决的问题"
    },
    // ... 共5个创意
  ]
}
```

#### 5. 评分筛选 `/idea/evaluate`（🔴 最关键，必须包含完整评分）
```json
{
  "round": 0,
  "evaluations": [
    {
      "idx": 0,  // 创意索引（0-4）
      "total": 91,  // 总分（必须传此字段！）
      "dimensions": {  // 四维评分（可选但建议传）
        "冲击波特质": 38,
        "话题传播力": 23,
        "营销效果": 23,
        "可执行性": 7
      },
      "feedback": ""
    },
    // ... 每个创意都要评分
  ]
}
```

> 🔴 **评分必须传 `total` 字段！** 如果只传 `score` 或不传，会导致显示0分。

#### 6. 本轮反馈 `/round/feedback`
```json
{
  "round": 0,
  "content": "本轮总结：入围创意、淘汰原因、下轮方向..."
}
```

#### 7. 完成任务 `/done`
```json
{}  // 无参数
```

---

## 核心规则

1. **单会话完整执行** — 所有轮次在一次回复中连续完成，不分多次
2. **思考过程可视化** — 向用户展示完整思考、搜索发现、创意生成、评分理由
3. **搜索不可跳过** — 每轮必须先有真实数据支撑，再发想创意
4. **每步立即更新** — 完成一个步骤立即调用对应 API
5. **全量透明** — 每轮所有创意（含淘汰）完整展示，评估过程可见
6. **每步停止检查** — 每次调用任何 API 之前必须检查状态：
   ```bash
   curl -s http://localhost:50000/state.json | python3 -c \
     "import sys,json; d=json.load(sys.stdin); print('STOPPED') if d.get('status') != 'running' else print('OK')"
   ```
   输出 `STOPPED` → 立即调用 `POST /done`，停止所有操作，不进入本轮

   > 🔴 **这是最高优先级约束。不管处于哪个阶段，查到就停。**
