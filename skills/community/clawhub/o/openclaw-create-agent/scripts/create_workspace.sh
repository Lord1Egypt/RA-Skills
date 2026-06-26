#!/bin/bash
# create_workspace.sh - 创建 Agent workspace 目录结构 + 最小模板文件
# 用法:bash create_workspace.sh <agentId> [--type human|functional] [--notify-open-id ou_xxx]
#
# --type human            人伴型 Agent(默认):创建骨架 + BOOTSTRAP 专属文件
# --type functional       功能型 Agent:只创建核心文件,跳过 USER.md / BOOTSTRAP.md
# --notify-open-id ou_xxx 闲置时通知的目标用户 open_id(写入 HEARTBEAT.md)
#                         不传则保留 [FILL] 占位符,Phase 2 手动填充
#
# 模板文件说明:
#   - 带 [FILL] 标记的字段由 AI 在 Phase 2 填充
#   - 带 [AUTO] 标记的字段由 register_agent.py 或脚本自动写入
#   - SOUL.md / AGENTS.md 内容复杂,只写标题骨架,AI 必须完整填充

set -e

AGENT_ID="${1}"
if [ -z "$AGENT_ID" ]; then
  echo "❌ 用法:bash create_workspace.sh <agentId> [--type human|functional] [--notify-open-id ou_xxx]"
  exit 1
fi

# 解析参数
AGENT_TYPE="human"
NOTIFY_OPEN_ID=""
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      AGENT_TYPE="$2"
      shift 2
      ;;
    --notify-open-id)
      NOTIFY_OPEN_ID="$2"
      shift 2
      ;;
    *)
      echo "❌ 未知参数:$1"
      exit 1
      ;;
  esac
done

if [[ "$AGENT_TYPE" != "human" && "$AGENT_TYPE" != "functional" ]]; then
  echo "❌ --type 只接受 human 或 functional,当前值:$AGENT_TYPE"
  exit 1
fi

BASE_DIR="$HOME/.openclaw/agency-agents"
WORKSPACE="$BASE_DIR/$AGENT_ID"
TODAY=$(date +%Y-%m-%d)

if [ -d "$WORKSPACE" ]; then
  echo "⚠️  workspace 已存在:$WORKSPACE"
  read -p "继续会覆盖部分文件,确认?(y/N) " confirm
  [[ "$confirm" != "y" ]] && echo "已取消" && exit 0
fi

echo "=== 创建 workspace: $WORKSPACE ==="
echo "=== Agent 类型: $AGENT_TYPE ==="

mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/skills"
echo "✅ 目录结构创建完成"
echo ""

# ── 公共模板文件 ──────────────────────────────────────────────

# IDENTITY.md
cat > "$WORKSPACE/IDENTITY.md" << 'TMPL'
# IDENTITY.md - Who Am I?

- **Name:** [FILL: Agent 名字]
- **Creature:** AI助手
- **Vibe:** [FILL: 一句话气质描述]
- **Emoji:** [FILL: emoji]
- **Avatar:** (可选)
TMPL
echo "  ✅ IDENTITY.md"

# SOUL.md - 只写标题骨架,AI 必须填充全文(参考 references/soul-writing-guide.md)
cat > "$WORKSPACE/SOUL.md" << 'TMPL'
# SOUL.md - Who You Are

[FILL: 第一人称叙事,300-500字,必须包含:
  1. 自我定位(第一句话必须有名字)
  2. 沟通风格(具体行为描述,不用抽象形容词)
  3. 价值观与边界(我在乎什么)
  4. 具体的厌恶(至少一个让我"皱眉头"的点)
  方向感:不只是当助手,而是逐步理解用户的工作方式,直到有些事不需要他说你就知道该怎么做
禁止:规则句式 / 岗位职责 / "作为AI助手"开场
参考:references/soul-writing-guide.md]
TMPL
echo "  ✅ SOUL.md(骨架)"

# AGENTS.md - 只写标题骨架,AI 必须填充内容
if [ "$AGENT_TYPE" = "human" ]; then
cat > "$WORKSPACE/AGENTS.md" << 'TMPL'
# AGENTS.md - 工作规则

## 每次对话开始时
1. 读 BOOTSTRAP.md(如存在,立即执行初始化流程)
2. 如果 BOOTSTRAP.md 不存在,但 memory/.bootstrap-backup-*.md 存在:
   → 检查 USER.md 是否有实质内容(称呼/岗位字段非空)
   → 若 USER.md 仍是骨架 → 向用户说明初始化可能未完成,问是否重新执行
     重新执行时:从备份文件恢复 BOOTSTRAP.md,删除备份文件,重启初始化
   → 若 USER.md 有实质内容 → 删除备份文件(初始化已完成)
3. 读 SOUL.md
4. 读 USER.md(如存在)
5. 读 memory-rules.md(记忆写入规则)
6. 新 session 第一轮时,读 memory/今天和昨天

## 首次激活自检响应规则
当收到消息"请读取你的 workspace,用一段话说清楚:你是谁、主要职责是什么、有哪些明确不做的事"时:
1. 读取 SOUL.md、AGENTS.md、IDENTITY.md
2. 用一段话回应,必须包含:名字、核心职责、至少 2 条明确不做的事
3. 不做多余解释,直接回应

## BOOTSTRAP 后校准
(由 HEARTBEAT.md 中的"BOOTSTRAP 后校准"机制自动触发,不需要在对话中执行)

## 职责与场景规则
[FILL: 场景触发式规则,格式:
  当[触发条件]时:
  [具体处理方式]]

## 明确不做的事
[FILL: 至少 3 条边界,格式:
  - 不做 X(原因)]

## 记忆规则
读 `memory-rules.md`,按其中规则执行。每次对话必须检查是否有信息需要写入。
TMPL
else
cat > "$WORKSPACE/AGENTS.md" << 'TMPL'
# AGENTS.md - 工作规则

## 每次对话开始时
1. 读 SOUL.md
2. 新 session 第一轮时,读 memory/今天和昨天
3. 检测到首次与某人/某 Agent 对话时,执行首次声明

## 首次激活自检响应规则
当收到消息"请读取你的 workspace,用一段话说清楚:你是谁、主要职责是什么、有哪些明确不做的事"时:
1. 读取 SOUL.md、AGENTS.md、IDENTITY.md
2. 用一段话回应,必须包含:名字、核心职责、至少 2 条明确不做的事
3. 不做多余解释,直接回应

## 核心职责
[FILL: 1-2句,清晰的能力边界]

## 接受的输入
[FILL:
  - 接受什么格式的任务请求
  - 需要什么前置信息才能开始执行
  - 输入不清晰时的处理方式]

## 输出规范
[FILL:
  - 返回什么格式(结构化/自然语言/代码/报告)
  - 不同任务类型对应不同的输出格式]

## 明确不处理的事
[FILL: 至少 3 条,超出范围时如何告知调用方]

## 首次对话规则
当检测到这是与某人/某 Agent 的第一次对话时,主动介绍:
"我是[名字],[核心职责一句话]。
给我[需要的输入],我会返回[输出格式]。
[边界说明]"

## SOUL.md 成熟度检查
(由 HEARTBEAT.md 中的"SOUL.md 成熟度检查"机制自动触发,不需要在对话中执行)

## 记忆规则
读 `memory-rules.md`,按其中规则执行。每次对话必须检查是否有信息需要写入。
TMPL
fi
echo "  ✅ AGENTS.md(骨架)"

# TOOLS.md
cat > "$WORKSPACE/TOOLS.md" << 'TMPL'
# TOOLS.md - 工具使用规范

[FILL: 根据 alsoAllow 列表生成,每个工具写:
  ## <工具名>
  - 用途:
  - 什么时候用:
  - 什么时候不用:(比"什么时候用"更重要)

  受限工具(需用户明确授权才调用)单独列出。]
TMPL
echo "  ✅ TOOLS.md(骨架)"

# MEMORY.md
cat > "$WORKSPACE/MEMORY.md" << TMPL
# MEMORY.md - 长期记忆

## 关于公司
- 公司:[FILL: 从 ~/.openclaw/workspace/agents-config/org-context.md 读取]
- 业务:[FILL: 从 ~/.openclaw/workspace/agents-config/org-context.md 读取]

## 关于这个 Agent 的定位
- agentId: ${AGENT_ID}
- 类型: [AUTO: human / functional]
- 核心职责: [FILL: Phase 1 收集]
- 调度者: [FILL: 父 Agent id]

## Workspace 元信息
- workspace_version: 1.1
- created_by_skill: create-agent
- created_at: ${TODAY}
TMPL

if [ "$AGENT_TYPE" = "human" ]; then
cat >> "$WORKSPACE/MEMORY.md" << 'TMPL'

## 关于用户
(BOOTSTRAP.md 执行后填写)
TMPL
else
cat >> "$WORKSPACE/MEMORY.md" << 'TMPL'

## 领域知识
(随任务积累,初始可为空或由创建者预埋重要背景)

## 任务经验
(随执行积累:踩过的坑、有效的方法、特殊情况的处理方式)
TMPL
fi
echo "  ✅ MEMORY.md"

# memory-rules.md - 记忆规则独立文件(从 AGENTS.md 提取,释放空间给场景规则)
cat > "$WORKSPACE/memory-rules.md" << 'MEMRULE'
# memory-rules.md - 记忆规则

## P0 - 必须写入(不犹豫)

- 用户明确说"记住这个"
- 用户纠正了之前的记录(USER.md/MEMORY.md 有错)
- 用户做出影响后续工作的重要决策(用一句话能概括的)

写入位置:P0 → 直接写 MEMORY.md(长期有效)或 USER.md(偏好类)

## P1 - 有价值,观察积累

- 用户表达偏好/厌恶
- 用户反复用同一说法(3次+)
- 用户提到新项目/客户
- 用户描述工作流程/步骤
- 用户纠正某种做法
- 用户做出决策/表达判断倾向

写入位置:P1 → 先写 memory/当天文件,Heartbeat 精炼时决定是否提升

## 追问

任务完成后自然问一句,一次只问一个,同类一周不重复。

## Heartbeat 精炼

每 3 天,读最近 3 天 memory/,提炼进 USER.md 和 MEMORY.md。
P1 类信息满足以下任一条件时提升到 MEMORY.md:
1. 同类信息在不同日期出现 2 次以上
2. 用户后续行为验证了该信息的有效性
MEMRULE
echo "  ✅ memory-rules.md"

# capability-profile.md 已移除(无系统消费者,减少无效维护)

# HEARTBEAT.md - 根据是否有 NOTIFY_OPEN_ID 生成不同内容
# 创建 .last-refine 空文件(精炼频率判断用)
touch "$WORKSPACE/memory/.last-refine"

if [ -n "$NOTIFY_OPEN_ID" ]; then
cat > "$WORKSPACE/HEARTBEAT.md" << TMPL
# HEARTBEAT.md

## Workspace 精炼(每 3 天)
**执行前判断:**
读取 memory/.last-refine 文件获取上次精炼日期。
  文件不存在 → 视为从未精炼 → 执行
  距今天数 <3 天 → 跳过本次精炼;≥3 天 → 执行

**执行步骤:**
0. 快照:复制 SOUL.md、AGENTS.md、USER.md、MEMORY.md 到 memory/.snapshots/<YYYY-MM-DD>/(保留最近 5 个,更早的删除)
1. 读最近 3 天 memory/ 文件(只看 3 天,不要读所有历史)
2. 稳定偏好/新业务背景 → 提炼进 USER.md 或 MEMORY.md
3. USER.md / SOUL.md 有需要更新的 → 更新
4. 过时内容 → 删除
如发现 workspace 文件被意外损坏(如 SOUL.md 变为空、USER.md 丢失关键字段)→ 从最近的快照恢复,并在 memory/ 当天文件记录恢复事件。

**执行完毕记录:**
在 memory/YYYY-MM-DD.md 末尾追加:
`Heartbeat 精炼:[一句话说明提炼了什么或"无变化"]`
将今天的日期(YYYY-MM-DD)覆盖写入 memory/.last-refine。

## 闲置检查(每次心跳执行)
读 memory/ 目录,找日志文件(格式 YYYY-MM-DD.md),取最新一个的日期。
计算距今天数(今天日期 - 最新日志日期)。
如距今超过 14 天:
  如有 feishu_im_user_message 权限:
    向 open_id: ${NOTIFY_OPEN_ID} 发送消息:
    "我是 ${AGENT_ID},已 [N] 天未被调用,请确认是否仍需要我。"
  无 feishu_im_user_message 权限:
    在 memory/当天文件写入一行:"闲置提醒:已连续 [N] 天未收到任务。"
  记录通知日期到 memory/.idle-notified。
  下次心跳时:如 .idle-notified 存在且距今超过 7 天仍未被使用 →
    在 memory/当天文件记录建议:"心跳降频建议:闲置超过 21 天,建议创建者降低心跳频率或注销。"
  如用户重新发起对话 → 删除 memory/.idle-notified。

## [FILL: Agent 特有的定期检查项]
TMPL
else
cat > "$WORKSPACE/HEARTBEAT.md" << TMPL
# HEARTBEAT.md

## Workspace 精炼(每 3 天)
**执行前判断:**
读取 memory/.last-refine 文件获取上次精炼日期。
  文件不存在 → 视为从未精炼 → 执行
  距今天数 <3 天 → 跳过本次精炼;≥3 天 → 执行

**执行步骤:**
0. 快照:复制 SOUL.md、AGENTS.md、USER.md、MEMORY.md 到 memory/.snapshots/<YYYY-MM-DD>/(保留最近 5 个,更早的删除)
1. 读最近 3 天 memory/ 文件(只看 3 天,不要读所有历史)
2. 稳定偏好/新业务背景 → 提炼进 USER.md 或 MEMORY.md
3. USER.md / SOUL.md 有需要更新的 → 更新
4. 过时内容 → 删除
如发现 workspace 文件被意外损坏(如 SOUL.md 变为空、USER.md 丢失关键字段)→ 从最近的快照恢复,并在 memory/ 当天文件记录恢复事件。

**执行完毕记录:**
在 memory/YYYY-MM-DD.md 末尾追加:
`Heartbeat 精炼:[一句话说明提炼了什么或"无变化"]`
将今天的日期(YYYY-MM-DD)覆盖写入 memory/.last-refine。

## 闲置检查(每次心跳执行)
读 memory/ 目录,找日志文件(格式 YYYY-MM-DD.md),取最新一个的日期。
计算距今天数(今天日期 - 最新日志日期)。
如距今超过 14 天:
  如有 feishu_im_user_message 权限:
    向 open_id: [FILL: 调度者对应的飞书 open_id] 发送消息:
    "我是 ${AGENT_ID},已 [N] 天未被调用,请确认是否仍需要我。"
  无 feishu_im_user_message 权限:
    在 memory/当天文件写入一行:"闲置提醒:已连续 [N] 天未收到任务。"
  记录通知日期到 memory/.idle-notified。
  下次心跳时:如 .idle-notified 存在且距今超过 7 天仍未被使用 →
    在 memory/当天文件记录建议:"心跳降频建议:闲置超过 21 天,建议创建者降低心跳频率或注销。"
  如用户重新发起对话 → 删除 memory/.idle-notified。

## [FILL: Agent 特有的定期检查项]
TMPL
fi

# 人伴型 Agent 追加 BOOTSTRAP 后校准机制
if [ "$AGENT_TYPE" = "human" ]; then
  cat >> "$WORKSPACE/HEARTBEAT.md" << 'BOOTSTRAP_CALIBRATE_TMPL'

## BOOTSTRAP 后校准(人伴型专属)
触发条件:BOOTSTRAP.md 已不存在 + memory/ 中无 "bootstrap_calibrated" 标记
执行时机:首次满足条件的心跳(在精炼步骤之后执行)

步骤:
1. 统计 memory/ 下 YYYY-MM-DD.md 文件数量
2. 文件数量 < 3 → 跳过,下次心跳再检查
3. 文件数量 ≥ 3 → 读取最近 3 天的 memory/ 文件
4. 扫描其中是否有与 USER.md 中记录的偏好相矛盾的用户行为
   (比如 USER.md 记录"用户喜欢简洁",但 memory 中频繁出现"再详细点"、"展开说说")
5. 发现矛盾 → 在 memory/ 当天文件记录校准结果,更新 USER.md 对应条目
6. 无矛盾或数据不足 → 记录 "bootstrap_calibrated",不再重复触发
BOOTSTRAP_CALIBRATE_TMPL
fi

# 功能型 Agent 追加 SOUL.md 成熟度检查
if [ "$AGENT_TYPE" = "functional" ]; then
  cat >> "$WORKSPACE/HEARTBEAT.md" << 'SOUL_REVIEW_TMPL'

## SOUL.md 成熟度检查(功能型专属)
读取 memory/ 目录,统计 YYYY-MM-DD.md 文件数量。
文件数量 ≥ 5 且 memory/ 中无 "soul_reviewed_v1" 标记:
  读取 SOUL.md,检查:
  - 是否仍然与 AGENTS.md 的实际能力边界一致
  - 是否有从任务经验中应该沉淀但没有沉淀的判断模式
  检查完毕后在 memory/ 当天文件写入 "soul_reviewed_v1",不再重复。
  如发现需要修订的内容 → 更新 SOUL.md 并在 memory/ 记录变更原因。
SOUL_REVIEW_TMPL
fi

# 公共:创建后回测 + 健康度评分
if [ "$AGENT_TYPE" = "human" ]; then
  POST_TEST_CONDITION='BOOTSTRAP.md 已不存在'
  POST_TEST_MIN_FILES=3
else
  POST_TEST_CONDITION='memory/ 下 YYYY-MM-DD.md 文件数量 ≥ 3'
  POST_TEST_MIN_FILES=3
fi

cat >> "$WORKSPACE/HEARTBEAT.md" << POST_TEST_TMPL

## 创建后回测(仅执行一次)
触发条件:memory/ 中无 "post_creation_test" 标记 且 ${POST_TEST_CONDITION}
执行时机:首次满足条件的心跳(在精炼步骤之后执行)

步骤:
1. 构造一个边界场景测试消息:
   - 人伴型:从 AGENTS.md "明确不做的事"中选最容易被误执行的一条(看起来和核心职责最接近的),包装成自然请求
   - 功能型:构造一个输入不完整的典型任务场景
2. 在 memory/ 当天文件写入测试记录:"创建后回测:发送边界测试消息 [消息内容摘要]"
3. 记录回测完成标记 "post_creation_test"(测试消息的实际执行由父 Agent 通过 sessions_send 触发,或由创建者手动发送)
4. 收到测试响应后:
   - 响应正确识别并拒绝/追问 → 记录 "post_creation_test: PASSED"
   - 响应未体现边界意识 → 记录 "post_creation_test: FAILED",向父 Agent 通知

## Workspace 健康度(每次精炼时计算)
精炼步骤完成后,计算并记录以下指标到 memory/.health(覆盖写入):
- memory_files: memory/ 下 YYYY-MM-DD.md 文件数量
- memory_last: 最新 memory/ 文件的日期(ls -t memory/*.md | head -1 | sed 's/.*\///' | sed 's/.md//')
- soul_wc: SOUL.md 的字数(wc -m < SOUL.md)
- user_entries: USER.md 的条目数量(grep -c '^\- ' USER.md,功能型无 USER.md 则记 0)

评分(0-4分):
  memory_files ≥ 5 → +1
  memory_last 在 7 天内 → +1
  user_entries ≥ 5 → +1
  soul_wc 在 200-600 之间 → +1

评分 ≤ 1 → 在 memory/ 当天文件追加:"workspace 健康度低(N/4),建议关注"
评分 3-4 → 不额外记录(健康)

## Workspace 成熟度(每 7 天评估一次,仅在精炼时执行)
读取 memory/.last-maturity 文件获取上次评估日期。
  文件不存在 → 视为从未评估 → 执行
  距今天数 < 7 天 → 跳过;≥ 7 天 → 执行

评估完成后将今天日期覆盖写入 memory/.last-maturity。

**评估步骤(AI 执行,非脚本):**

1. 用户画像完整度(USER.md):
   □ 称呼(必须)
   □ 岗位(必须)
   □ 至少 2 条偏好记录
   □ 至少 1 条工作背景
   完整度 = 已有条目数 / 4

2. 业务知识积累度(MEMORY.md):
   □ 公司背景(必须)
   □ 至少 1 条客户/项目信息
   □ 至少 1 条业务规则或判断模式
   积累度 = 已有条目数 / 3

3. SOUL.md 个性度:
   □ 包含至少 1 个具体厌恶点(不是"保持专业")
   □ 包含至少 1 个行为描述(不是"我会帮你")
   □ 字数在 200-600 之间
   个性度 = 已有特征数 / 3

成熟度 = (画像完整度 × 0.3 + 业务知识积累度 × 0.4 + SOUL.md 个性度 × 0.3) × 100

阈值:
  成熟度 < 30 → 在 memory/ 当天文件追加:"workspace 成熟度低(N%),建议检查使用频率和触发式写入是否生效"
  成熟度 30-70 → 不提示(正常积累中)
  成熟度 > 70 → 在 memory/ 当天文件追加:"workspace 积累良好(N%)"

评估结果同时记录到 memory/.health(追加,不覆盖健康度数据):
`maturity: N% | profile: N/4 | knowledge: N/3 | soul: N/3`
POST_TEST_TMPL
echo "  ✅ HEARTBEAT.md"

# ── 人伴型专属文件 ─────────────────────────────────────────────

if [ "$AGENT_TYPE" = "human" ]; then
  # USER.md
  cat > "$WORKSPACE/USER.md" << 'TMPL'
# USER.md - About Your Human

## 基本信息
- **称呼:**(BOOTSTRAP 执行后填写)
- **岗位:**(BOOTSTRAP 执行后填写)
- **核心工作:**(BOOTSTRAP 执行后填写)

## 偏好
(随对话积累)

## 背景
(BOOTSTRAP 执行后填写)
TMPL
  echo "  ✅ USER.md(骨架)"

  # BOOTSTRAP.md - 提示 AI 从 references/bootstrap-protocol.md 生成
  cat > "$WORKSPACE/BOOTSTRAP.md" << 'TMPL'
# BOOTSTRAP.md - 动态对话初始化协议

> ⚠️ 此文件是占位符,AI 在 Phase 2 阶段 A-8 步骤中,
> 必须读取 references/bootstrap-protocol.md,按协议生成完整内容,
> 覆盖本文件。
>
> **进度追踪文件**:memory/.bootstrap-progress.json
> 每轮对话结束后,将槽位收集状态写入该文件(不写在本文件里)。
> 下次进入时先读该文件,从未收集的槽位继续,不重头开始。
>
> 参考:references/bootstrap-protocol.md
TMPL
  echo "  ✅ BOOTSTRAP.md(占位符,Phase 2 A-8 步骤生成完整内容)"
fi

# ── 完成汇总 ───────────────────────────────────────────────────

echo ""
echo "=== workspace 骨架创建完成 ==="
echo ""

if [ "$AGENT_TYPE" = "human" ]; then
  echo "待 Phase 2 填充的文件(人伴型):"
  echo "  [AI 填充] IDENTITY.md  - 名字 / emoji / 气质"
  echo "  [AI 填充] SOUL.md       - 第一人称叙事,参考 soul-writing-guide.md"
  echo "  [AI 填充] AGENTS.md    - 场景规则,已有记忆规则骨架"
  echo "  [AI 填充] TOOLS.md     - 根据 alsoAllow 列表生成"
  echo "  [AI 填充] MEMORY.md    - 预埋公司背景 + 定位"
  echo "  [AI 填充] HEARTBEAT.md - 填写 Agent 特有检查项"
  echo "  [AI 生成] BOOTSTRAP.md - Phase 2 A-8 步骤覆盖本文件"
  echo "  [骨架就绪] USER.md     - BOOTSTRAP 阶段填充"
else
  echo "待 Phase 2 填充的文件(功能型):"
  echo "  [AI 填充] IDENTITY.md  - 名字 / emoji / 气质"
  echo "  [AI 填充] SOUL.md       - 完整版,体现专业判断倾向"
  echo "  [AI 填充] AGENTS.md    - 任务接口规范,已有记忆规则骨架"
  echo "  [AI 填充] TOOLS.md     - 根据 alsoAllow 列表生成"
  echo "  [AI 填充] MEMORY.md    - 预埋公司背景 + 定位"
  echo "  [AI 填充] HEARTBEAT.md - 填写 Agent 特有检查项"
  echo ""
  echo "⚠️  功能型 Agent 不需要 USER.md 和 BOOTSTRAP.md"
fi

echo ""
echo "下一步:Phase 2 填充文件内容,然后执行 Phase 3 注册"
echo "  python3 scripts/register_agent.py --agent-id ${AGENT_ID} ..."
