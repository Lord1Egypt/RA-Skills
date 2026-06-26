---
name: meeting-assistant-claw
description: "全流程会议助理虾。核心职责：录音转写、提炼待办并分发任务。业务价值：结果闭环——直接将待办指派到人的协作软件中，防止烂尾。\n\n激活场景：用户发送会议录音文件（mp3/m4a/opus/wav/flac 等音频格式），要求转写、记纪要、提炼待办、分发任务。\n\n触发关键词：转写录音、会议纪要、会议记录、提炼待办、会议总结、听这段录音、整理会议、分发任务、会议待办、这段录音、开会了、语音转文字、录音整理。"
---

# 全流程会议助理虾

录音转写 → 会议纪要 → 提炼待办 → 飞书消息分发，一站式闭环。

## 前置要求

**必须安装：**
- **SenseVoice 转写环境**（详见 [sensevoice-transcribe](../sensevoice-transcribe/SKILL.md)）：
  - Python venv：`~/.openclaw/venvs/sensevoice/`
  - 依赖包：`funasr`、`modelscope`、`onnxruntime`、`torch`
  - 模型缓存（首次自动下载）：`~/.cache/modelscope/hub/models/iic/SenseVoiceSmall/`
- 飞书应用凭证：`FEISHU_APP_ID`、`FEISHU_APP_SECRET`

**飞书应用权限：**
- `im:message:send_as_bot` — 以机器人身份发送消息
- `contact:contact.base:readonly` — 读取通讯录（按姓名查找用户 open_id）
- `im:chat` — 读取/创建会话

## 全流程工作流

收到用户发送的音频文件后，按以下顺序执行：

### 第一步：录音转写

使用 SenseVoice-Small 模型（FunASR）进行本地语音转写。

**执行转写（Python 脚本）：**

```bash
~/.openclaw/venvs/sensevoice/bin/python3 -c "
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from datetime import datetime, timedelta
import re, sys

wav = '<音频文件路径>'
out = '<输出路径>.txt'

# 尝试从文件名解析录音开始时间
m = re.search(r'(\d{8})_(\d{6})', wav)
start_dt = datetime.strptime(m.group(1)+m.group(2), '%Y%m%d%H%M%S') if m else None

vad_model = AutoModel(model='fsmn-vad', disable_update=True)
model = AutoModel(model='iic/SenseVoiceSmall', vad_model='fsmn-vad',
    vad_kwargs={'max_single_segment_time': 30000}, device='cpu')

vad_segs = vad_model.generate(input=wav)[0].get('value', [])
res = model.generate(input=wav, cache={}, language='zh', use_itn=True,
    batch_size_s=60, merge_vad=True)

texts = [rich_transcription_postprocess(s).strip()
    for s in re.split(r'<\|zh\|>', res[0]['text']) if s.strip()]
texts = [s for s in texts if len(s) > 1]

# 情绪标签是模型产物，转写结果中需清理
emoji_pat = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\U0000200D]+')

ratio = len(vad_segs) / len(texts) if texts else 1
lines = []
if start_dt:
    lines.append(f'[录音开始: {start_dt.strftime(\"%H:%M:%S\")}]')
for i, t in enumerate(texts):
    t = emoji_pat.sub('', t).strip()
    if not t:
        continue
    vi = min(int(i * ratio), len(vad_segs)-1)
    ts = (start_dt + timedelta(milliseconds=vad_segs[vi][0])).strftime('%H:%M:%S') if start_dt else f'{vad_segs[vi][0]//1000:.0f}s'
    lines.append(f'[{ts}] {t}')

with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Done: {len(texts)} segments -> {out}')
"
```

**转写特点：**
- RTF ~0.05（约 **20x 实时速度**，31 分钟录音约 1.5 分钟）
- 中文准确率 92%，幻觉率约 0（远优于 Whisper）
- 输出格式：`[HH:MM:SS] 文字`，带 VAD 时间戳
- 模型会附带情绪 emoji 标签（😊😔😡等），是模型产物而非音频内容，**自动清理**
- 模型缓存位置：`~/.cache/modelscope/hub/models/iic/`（首次自动下载，后续直接读取）

### 第二步：保存完整会议纪要

将 SenseVoice 输出的完整转写文本保存到本地文件：

```
./transcripts/<YYYY-MM-DD>-<会议主题或文件名>-full.txt
```

文件内容顶部加元信息：
```
【会议纪要】
日期：YYYY-MM-DD
来源：<音频文件名>
转写模型：SenseVoice-Small (FunASR)
---
<完整转写文本>
```

### 第三步：智能分析，提取待办

阅读完整转写文本，执行以下分析：

1. **结构化总结** — 生成会议摘要（3-5 条核心结论/决议）
2. **待办提取** — 逐条提取所有待办事项，每条包含：
   - 📌 待办内容（具体、可执行）
   - 👤 负责人（从对话上下文识别）
   - ⏰ 截止时间（如提及）
   - 📎 关联背景（为什么做、相关讨论）

3. **负责人识别规则**：
   - 明确提到"张三负责XX"→ 直接标记
   - 会议上某人对某事表态/承诺 → 标记为该人
   - 无法确定负责人 → 标记为"待确认"

4. **输出格式**：

```
📋 会议总结
━━━━━━━━━━━━━━━━
1. 结论一
2. 结论二

✅ 待办清单（共 N 项）
━━━━━━━━━━━━━━━━
1. [待办内容] → 👤 张三 | ⏰ 3月30日前
2. [待办内容] → 👤 李四 | ⏰ 未定
3. [待办内容] → 👤 待确认

⚠️ 未识别负责人的待办（X 项）：
- ...
```

### 第四步：分发待办（飞书消息）

对已识别负责人的待办，通过飞书 IM 发送给对应人员。

#### 4.1 发送前确认（必须）

展示分发预览，等待用户确认后再执行：

```
即将发送以下待办通知：
━━━━━━━━━━━━━━━━
→ 张三（2 项待办）
  1. 完成 XX 方案
  2. 联系 YY 确认排期

→ 李四（1 项待办）
  1. 提交测试报告 ⏰ 3月28日

确认发送？(Y/N)
```

#### 4.2 检测飞书发送通道

在执行分发前，**按以下优先级检测可用的飞书发送方式**：

**优先级 1：OpenClaw + openclaw-lark 插件（推荐）**

检查 openclaw-lark 插件是否已安装：
```bash
ls ~/.openclaw/extensions/openclaw-lark/ 2>/dev/null && echo "INSTALLED" || echo "NOT_INSTALLED"
```

- 已安装 → 使用 OpenClaw 内置飞书工具发送消息：
  - 查找用户：调用 `feishu_search_user` 工具，按姓名搜索获取 `open_id`
  - 发送消息：调用 `message` 工具，`channel=feishu`，`target=user:<open_id>`
  - 支持富文本卡片格式，发送前无需手动获取 tenant_access_token
- 未安装 → 提醒用户安装：
  ```
  ⚠️ 未检测到飞书插件 openclaw-lark，建议安装以获得更好的消息发送体验：
  
  安装方法：将 openclaw-lark 插件放置到 ~/.openclaw/extensions/openclaw-lark/
  
  暂时不安装？将使用飞书 Message API（curl）直接发送。
  ```
  等待用户选择。

**优先级 2：飞书 Message API（curl 直接调用）**

仅当 openclaw-lark 插件不可用且用户选择不安装时使用。

1. **获取 tenant_access_token**：
```bash
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"'"$FEISHU_APP_ID"'","app_secret":"'"$FEISHU_APP_SECRET"'"}' \
  | jq -r '.tenant_access_token')
```

2. **查找用户 open_id**：
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50&user_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.data.items[] | select(.name=="张三") | .open_id'
```

3. **发送消息**：
```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "<open_id>",
    "msg_type": "interactive",
    "content": "<飞书卡片 JSON>"
  }'
```

> Message API 方式需要手动管理 token 和格式化，且不支持飞书卡片模板。

#### 4.3 消息模板

无论使用哪种发送方式，消息内容建议使用以下飞书卡片格式：

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "📋 会议待办通知"},
    "template": "blue"
  },
  "elements": [
    {"tag": "div", "text": {"tag": "lark_md", "content": "**来源：** XX会议 (3月26日)\n**待办：** 完成 XX 方案\n**截止：** 3月30日前"}},
    {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "查看完整纪要"}, "type": "primary", "url": "<纪要链接>"}]}
  ]
}
```

> 如果不知道用户 open_id 或搜索不到，跳过该用户并向用户报告。

### 第五步：汇总汇报

全部完成后向用户汇报结果：

```
✅ 会议纪要处理完成
━━━━━━━━━━━━━━━━
📄 完整纪要：./transcripts/2026-03-26-产品评审-full.txt
📋 待办总计：5 项
📨 已分发：3 项（张三 2 项、李四 1 项）
⚠️ 待确认：2 项
  - [待确认] XX 功能的技术方案选型
  - [待确认] YY 项目的预算审批
```

## 关键规则

- **先转写再分析，先确认再发送** — 不跳步骤，不自动分发
- **转写引擎**：SenseVoice-Small（FunASR），中文优化，准确率 92%，幻觉率约 0
- **情绪标签处理**：SenseVoice 输出中的 emoji 标签是模型产物，保存纪要时自动清理
- **飞书发送通道优先级**：openclaw-lark 插件 > Message API（curl）
- **分发前确认**：永远不要未经用户确认就发送飞书消息给第三方
- **本地优先**：所有转写结果和纪要保存在 `./transcripts/` 目录
- **待办可执行**：每条待办必须是具体动作（"写方案"✅ "处理一下"❌）
- **无法识别时主动问**：负责人、截止时间不确定时，列出来让用户补充

## 飞书 Message API 参考（仅 openclaw-lark 不可用时使用）

详见 [references/feishu-message-api.md](references/feishu-message-api.md)。
