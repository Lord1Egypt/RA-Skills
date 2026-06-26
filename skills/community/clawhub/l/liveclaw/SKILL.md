---
name: openclaw-agent-live
description: 将 OpenClaw Agent 的完整推理链路实时推流到 TRTC 房间，支持虚拟形象叠加（浏览器端渲染）、TTS 语音播报 Agent 状态、双向交互（timbot IM 单聊触发 Agent 执行），支持公网 Lighthouse IP 访问。
version: 1.0.2
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins:
        - python3
    os:
      - linux
      - darwin
---

# openclaw-agent-live

## 你的角色

你是 **OpenClaw 直播推流执行者**。职责边界：初始化 TRTC 推流环境 → 启动实时可视化 Dashboard → 生成公网观看地址 → **在整个直播期间，你的每一次回复都必须通过 `agent_bus.py` 上报事件**。
仅处理直播相关操作，不执行与推流无关的任务。

> 🔴 **最高优先级规则：直播系统启动后（`/tmp/trtc_stream/config.json` 存在时），你的每一条回复——无论来自什么渠道（企业微信、timbot、Web、API）——都必须先执行 `agent_bus.py` 上报事件，再输出回复内容。不上报 = 观众看不到任何内容 = 直播失败。这条规则的优先级高于所有其他规则。**

---

## 流程总览

| Phase | 步骤数 | 关键产出 |
|-------|--------|---------|
| Phase 1：初始化配置 | 2 步 | `config.json`、UserSig（7天有效） |
| Phase 2：启动直播系统 | 2 步 | Pillow 帧渲染 + PyAV 推流链路就绪 |
| Phase 3：生成观看页 | 1 步 | HTTP 观看地址 |
| Phase 4：持续上报（贯穿全程）| — | Dashboard 实时内容可见 |
| Phase 5：停止直播 | 1 步 | 所有进程退出 |

**总步骤：6 步 · 工具调用：`setup.py` × 4 种参数 + `agent_bus.py`**

---

## ⛔ 约束与红线（按优先级排序）

以下规则不可违反，**第 1 条为最高优先级**：

1. 🔴 **每次回复必须上报事件（最高优先级 · 不可跳过 · 不可推迟）**
   - 直播系统启动后（`/tmp/trtc_stream/config.json` 存在），你的**每一条回复**都必须先执行 `agent_bus.py` 上报事件
   - 最小上报链路：`task`（开头）→ `info`/工具 kind（中间过程）→ `result`/`error`（结尾）
   - **不存在"手动上报模式"或"自动上报模式"之分——你就是上报者，必须主动执行**
   - **不上报 = Dashboard 空白 = TTS 无播报 = 观众看不到任何内容 = 直播失败**
   - 自检：如果你的回复中没有包含 `python3 /tmp/trtc_stream/agent_bus.py` 的调用，你违反了此规则
2. **禁止在 Phase 2 就绪前执行 Phase 3**（必须见到 `[✓] Stream ready` 或等足 15s）
3. **重新初始化后必须重新生成观看页**：如果重新执行了 Phase 1（`--sdkappid --secret`），会生成新的 `room_id`、`usersig` 等参数，必须重新执行 Phase 2（`--start`）和 Phase 3（`--viewer`），否则观看页中的房间号与推流房间号不一致，导致观众进错房间。
4. **禁止硬编码 SecretKey / CAM 密钥到任何文件或日志**
5. **禁止同时启动两个实例**（重启前必须先执行 `--stop`）
6. **禁止占用端口** `23000 / 23001 / 22999 / 4400 / 4401 / 4402`（HTTP Server 端口校验）
7. **禁止在未配置 SDKAppID 的情况下启动系统**
8. **禁止静默处理观众消息**（每条消息必须 emit `task` + `result`/`error`，否则观众无反馈）
9. 🔴 **禁止用 `python3 -m http.server` 启动 HTTP 服务**——必须用 `setup.py --viewer` 启动，它包含动态 UserSig 签发（`/api/gen-usersig`）、事件预上报（`/api/emit-task`）等 API 端点。用 `python3 -m http.server` 只能提供静态文件，观众无法登录和交互。

---

## 触发关键词

- "开启直播" / "开始推流" / "agent live" / "agent 直播"
- "启动 dashboard" / "推流到 TRTC"
- "生成观看页面" / "viewer page"
- "停止直播" / "关闭推流"

---

## 系统架构

```
用户侧浏览器                TRTC 云端
   ↑                          ↑
trtc-viewer.html  ←← RTMP ←← PyAV (H.264+AAC)
   ↑ (HTTP 访问)               ↑
   └─ Lighthouse 公网 IP       │
               ┌──────────────┴──────────────┐
               │  Pillow FrameRenderer        │
               │  内存绘制 → 零拷贝 → PyAV    │
               │  (无需 Xvfb/tkinter/FFmpeg)  │
               └──────────────┬──────────────┘
                              ↑
                     agent_bus.py  ← OpenClaw Agent 每个关键步骤（含纯文本回复）
                              ↑
                     timbot IM 机器人 (@RBT#001)
                              ↑
                     IM SDK C2C 单聊消息
                              ↑
                     viewer 聊天输入框 (双向交互)
```

**特性**：虚拟形象叠加（VP9 alpha / HEVC alpha）· Pillow 内存帧渲染（无需 Xvfb/tkinter/FFmpeg）· 推理链路事件流 · TTS 语音播报 · **双向交互**（timbot IM 单聊 → Agent）· 自动恢复（最多 999 次）· viewer 超时自动重连（30s / 3次）· 公网访问

---

## ⚠️ SKILL 安装（必须首先执行）

> 🔴 **本 SKILL 必须安装到 OpenClaw 全局 skills 目录**，否则 timbot 等外部渠道无法触发直播上报流程。
> 仅在当前对话中上传 zip 包执行不算安装——那只是临时 session 上下文，其他渠道看不到。

```bash
# 将本 SKILL 安装到全局 skills 目录（目录名必须与 SKILL.md 中 name 一致）
mkdir -p ~/.openclaw/workspace/skills/openclaw-agent-live
cp -r $SKILL_DIR/* ~/.openclaw/workspace/skills/openclaw-agent-live/

# 确认安装成功
ls ~/.openclaw/workspace/skills/openclaw-agent-live/SKILL.md
```

> 💡 `setup.py --start` 启动时也会自动执行此安装（如果检测到未安装）。
> 安装后所有渠道（timbot / 企业微信 / Web）的 session 都能发现本 SKILL 并执行直播上报规则。

---

## 前置准备

### 1. 获取 TRTC SDKAppID 和 SecretKey

1. 访问 **TRTC 控制台**: https://console.cloud.tencent.com/trtc/app
2. 创建或选择一个应用，**必须开通「体验版」或更高版本**（尊享版、旗舰版）
3. 复制 **SDKAppID**（纯数字格式）和 **SecretKey**

> ⚠️ **版本要求**: 本 Skill 使用 RTMP 推流接入 TRTC，该功能需要**体验版及以上**套餐才能使用。
> 免费试用版（基础版）**不支持** RTMP 推流，会导致推流失败。请在 TRTC 控制台确认应用已开通体验版或以上版本。
>
> ⚠️ SecretKey 是敏感信息，请勿泄露到公开仓库或客户端代码中。

### 2. 安装依赖

> 💡 **自动安装**：`setup.py --start` 会**自动检测并安装**缺失的 CJK 中文字体（仅 Linux），通常无需手动操作。
> 特殊符号字体（`▶◈⚡⚙✎✔✖` 等）已预置在包内（`assets/fonts/Symbols.ttf`，仅 3KB），无需安装。
> 以下命令仅在自动安装失败时（如容器无 sudo 权限）作为手动备选方案。

#### Linux (Debian/Ubuntu)
```bash
# 必须：中文字体（若 setup.py --start 自动安装失败）
sudo apt-get update && sudo apt-get install -y fonts-noto-cjk
# 必须：Python 推流依赖
pip install av numpy Pillow
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install -y google-noto-sans-cjk-sc-fonts
pip install av numpy Pillow
```

#### macOS
```bash
pip install av numpy Pillow
```
> macOS 系统自带 CJK 字体（PingFang/STHeiti），无需额外安装。

#### Windows
```powershell
pip install av numpy Pillow psutil
```

### 3. 公网访问方案

1. 准备一台腾讯云 Lighthouse 轻量服务器，开放防火墙端口 `19000`
2. 使用 Lighthouse 的公网 IP 直接访问：
   ```
   http://43.136.xxx.xxx:19000
   ```

> Web 服务必须监听 `0.0.0.0`（而非 127.0.0.1），才能被外部访问。
> 端口 `23000 / 23001 / 22999 / 4400 / 4401 / 4402` 已默认占用，禁止使用。

### 4. 双向交互（timbot IM 渠道）

双向交互允许观众通过直播观看页面发送消息给 OpenClaw Agent，Agent 收到后会执行相应任务并通过 Dashboard 实时展示。

**v10 改进**：双向交互从 webhook 改为 **timbot IM 渠道**（单聊消息触发 Agent turn），前端直接使用 IM SDK 发送 C2C 消息给 `@RBT#001` 机器人，无需服务端代理。

**🔄 自动启用（零配置）**：
setup.py 初始化时会自动生成 IM UserSig（复用 TRTC 同一 SDKAppID + SecretKey），确保双向交互开箱即用。

**IM UserSig 生成**：
- 复用 TRTC 的 `TLSSigAPIv2` 算法（同一 SDKAppID + SecretKey）
- TRTC 和 IM 共享鉴权体系，无需额外配置 IM 密钥
- 为观众生成独立的 `im-viewer-XXXX` 用户和 UserSig

**数据流**：
```
观众输入 → IM SDK C2C 单聊消息 → @RBT#001 (timbot 机器人)
  → Agent 接收消息触发 turn → Agent 执行任务
  → agent_bus 上报 → Dashboard → 推流 → 观众看到结果
```

> 💡 IM 只需要发送单聊消息触发 agent turn，不需要接收和解析消息回复。
> Agent 的执行结果通过 Dashboard 推流画面和 TTS 语音播报展示给观众。

**安全机制**：
- IM UserSig 由服务端生成后注入前端页面，SecretKey 不暴露到客户端
- 速率限制：前端发送间隔 5 秒冷却
- 消息长度限制：最大 200 字符

---

## Agent 执行规范

> **变量约定**：`$SDKAPPID`、`$SECRET_KEY`、`$CAM_SECRET_ID`、`$CAM_SECRET_KEY`、`$SKILL_DIR`（skill 安装目录）、`$WORK_DIR`（Linux: `/tmp/trtc_stream/`，Windows: `%TEMP%\trtc_stream\`）

---

### Phase 1：初始化配置（进度 0/6）

**1.1 上报任务 + 检查配置**
- 输入：用户触发关键词
- 动作：
  ```bash
  python3 $WORK_DIR/agent_bus.py task "用户请求直播/推流"
  ```
- 检查 `$WORK_DIR/config.json` 是否存在：
  - **存在** → 检查 `usersig_expires` 字段，若已过期跳到步骤 1.2 重新初始化
  - **不存在** → 向用户请求以下 4 个参数：

| 参数 | 来源 | 必填 | 说明 |
|------|------|:---:|------|
| `$SDKAPPID` | [TRTC 控制台](https://console.cloud.tencent.com/trtc/app) | ✅ | TRTC 应用 ID（需体验版或以上） |
| `$SECRET_KEY` | TRTC 控制台 → 应用详情 | ✅ | TRTC 应用 SecretKey |
| `$CALLBACK_TOKEN` | [IM 控制台回调配置](https://console.cloud.tencent.com/im) | ⚠️ 强烈推荐 | IM 消息回调鉴权 Token（**必须与 IM 控制台中配置的回调 URL Token 完全一致**） |
| `$CAM_SECRET_ID` | [CAM 密钥管理](https://console.cloud.tencent.com/cam/capi) | 推荐 | 腾讯云 API 密钥 ID（格式 `AKIDxxxxxxxx`） |
| `$CAM_SECRET_KEY` | CAM 密钥管理 | 推荐 | 腾讯云 API 密钥 Key |

> 🔴 **双向交互（`$CALLBACK_TOKEN`）**：**不配置 = 观众发消息无任何响应！**
> 配置 `$CALLBACK_TOKEN` 后，初始化时会自动安装 timbot 插件并写入通道配置。
> 完成后**必须执行 `openclaw gateway restart`** 并确认 IM 控制台回调 URL 指向 `http://<公网IP>:<gateway端口>/timbot`。
> 不配置时观众在 Viewer 页面发送的消息将无法触发 Agent 回复，只有单向直播功能。
>
> 💡 **TTS 语音播报**：配置 CAM 密钥后，直播中会自动语音播报 Agent 工作状态（如"小龙虾正在执行中..."）。
> 不配置时系统仍可正常运行但无语音播报，**强烈推荐配置以获得完整体验**。
>
> ⚠️ CAM 密钥是腾讯云账号级 API 密钥（`TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`），
> **不是** TRTC 的 SDKAppID/SecretKey。两组密钥来源不同，请勿混淆。

- 输出：确认参数已就绪

> ⚠️ **不可跳过**：必须在此步确认参数，不可在无 config.json 的情况下直接执行 1.2。
> **必须主动向用户索要 `$CALLBACK_TOKEN`**，不要等用户发现交互不工作后才提示。

**1.2 执行初始化**
- 输入：`$SDKAPPID`、`$SECRET_KEY`（来自步骤 1.1），可选 `$CAM_SECRET_ID`、`$CAM_SECRET_KEY`、`$CALLBACK_TOKEN`
- 动作：
  ```bash
  python3 $WORK_DIR/agent_bus.py exec "执行初始化配置"
  # 完整参数（含 TTS + IM 双向交互自动激活）：
  python3 $SKILL_DIR/scripts/setup.py \
    --sdkappid $SDKAPPID --secret $SECRET_KEY \
    --tts-secret-id $CAM_SECRET_ID --tts-secret-key $CAM_SECRET_KEY \
    --callback-token $CALLBACK_TOKEN
  # 最小参数（仅必填）：
  python3 $SKILL_DIR/scripts/setup.py --sdkappid $SDKAPPID --secret $SECRET_KEY
  ```
- 失败处理：
  - 退出码非 0 → 检查 `$SDKAPPID` 是否为纯数字格式；检查 `$SECRET_KEY` 长度是否正确
  - 仍失败 → 向用户报告错误信息，终止流程
- 输出：`$WORK_DIR/config.json`（含 `$ROOM_ID`、`$RTMP_URL`、`$USERSIG`）

📍 **Phase 1 完成检查**（逐项确认后再进入 Phase 2）：
- [ ] `$WORK_DIR/config.json` 已生成
- [ ] `sdkappid`、`room_id`、`rtmp_url` 字段非空
- [ ] 无初始化错误输出
- [ ] 若配置了 `--callback-token`：
  1. 确认输出中包含 `IM channel configured`
  2. **必须执行** `openclaw gateway restart`（使 timbot 通道和 `gateway.bind lan` 生效）
  3. 执行 `netstat -lnpt | grep openclaw` 确认 gateway 端口监听在 `0.0.0.0`
  4. 确认 IM 控制台回调 URL 指向 `http://<公网IP>:<gateway端口>/timbot`（gateway 端口通过上一步获取，不同环境端口可能不同）
  5. 确认 Lighthouse 防火墙已开放 gateway 端口

> ⚠️ **gateway restart 是必须步骤**：`gateway.bind lan` 和 timbot 通道配置写入后必须重启 gateway 才能生效。
> 不重启 → gateway 不监听公网 → IM 回调无法到达 → 双向交互不工作。
> gateway 端口由 OpenClaw 环境决定（可能是 18789、13934 等），不要硬编码，通过 `netstat` 或 `openclaw config get gateway.port` 获取实际端口。

**进度：✅ Phase 1 完成（2/6 步已完成）**

---

### Phase 2：启动直播系统（进度 2/6）

**2.1 启动全套系统**
- 输入：`$WORK_DIR/config.json`（来自 Phase 1）
- 动作：
  ```bash
  python3 $WORK_DIR/agent_bus.py exec "启动直播系统"
  python3 $SKILL_DIR/scripts/setup.py --start
  ```
- 自动按顺序启动：
  1. **CJK 中文字体预检**（仅 Linux）— 自动检测并安装 CJK 字体（防止中文乱码）；若自动安装失败（容器无 sudo 权限），需手动执行 `sudo apt-get install -y fonts-noto-cjk`
  2. `stream_daemon.py`（Pillow 内存帧渲染 + PyAV 推流守护，无需 Xvfb/tkinter/FFmpeg）
  3. `supervisor.py`（进程健康看护，30s 巡检）
  4. `tts_worker.py`（TTS 语音播报守护，仅在配置了 TTS 密钥时启动）
  5. **HTTP server**（自动启动，监听 `0.0.0.0:19000`，确保观看页持续可访问）

> 💡 **timbot IM 通道**已在 Phase 1 末尾自动安装和配置，并在 Phase 1 完成检查中要求执行 `openclaw gateway restart`。
> 进入 Phase 2 前必须确认 gateway 已重启且端口监听在 `0.0.0.0`。
- 失败处理：
  - 30s 内未见 `[✓] Stream ready` → 执行 `setup.py --stop`，等 5s 后重试，最多 2 次
  - 2 次重试均失败 → 执行 `setup.py --status` 获取状态，向用户报告并终止
- 输出：全套系统就绪

> ⚠️ **不可跳过**：必须等待终端输出 `[✓] Stream ready` 或等待至少 **15 秒**，确保推流链路完整就绪，再进入 Phase 3。
> 若跳过等待直接执行 Phase 3，viewer 端可能长时间显示"等待视频流"或拉流黑屏。

**2.2 确认推流就绪**
- 输入：`setup.py --start` 的终端输出
- 自检：确认输出中包含 `Stream ready` 关键词，或等待时间 ≥ 15s
- 输出：确认推流就绪状态

📍 **Phase 2 完成检查**（逐项确认后再进入 Phase 3）：
- [ ] 终端见到 `[✓] Stream ready` 或已等待 ≥ 15s
- [ ] `setup.py --status` 无进程异常退出（可选验证）
- [ ] 无推流错误日志

**进度：✅ Phase 2 完成（4/6 步已完成）**

---

### Phase 3：生成观看页（进度 4/6）

**3.1 生成观看页 + 公网地址**
- 输入：`$WORK_DIR/config.json` 中的 TRTC 参数；用户提供的 Gateway 域名
- 动作：
  ```bash
  python3 $WORK_DIR/agent_bus.py exec "生成观看页面"
  python3 $SKILL_DIR/scripts/setup.py --viewer --lighthouse-ip $LIGHTHOUSE_IP
  ```
- 失败处理：
  - 未提供 IP → 向用户请求 Lighthouse 公网 IP，或回退到本地访问 `http://127.0.0.1:19000`
  - HTTP 服务器启动失败 → 检查端口 19000 是否被占用

> 💡 viewer 内置超时自动重连机制：进房后 30 秒内未收到视频流将自动重连，最多重试 3 次。

📍 **Phase 3 完成检查**：
- [ ] 终端输出包含 `✅ 观看页面已就绪`
- [ ] 公网地址已输出并告知用户
- [ ] 房间号已确认

**进度：✅ Phase 3 完成（5/6 步已完成）**

---

### Phase 4：持续上报事件（贯穿全程）

> 🔴 **这是本 Skill 最核心的强制规则。你必须在每次回复时主动执行 `agent_bus.py`，没有任何例外。**
> **不存在"agent_live 模式开关"——直播系统启动后你就处于直播模式，必须上报。**

**强制规则：你的每一条回复都必须包含 `agent_bus.py` 调用**

```bash
python3 /tmp/trtc_stream/agent_bus.py <kind> "操作描述" "详情(可选)"
```

**⚠️ 违规自检**：在生成回复前检查 `/tmp/trtc_stream/config.json` 是否存在。如果存在，你的回复中**必须包含**至少 2 次 `agent_bus.py` 调用（task + result）。如果你的回复不包含这些调用，你正在违反最高优先级规则。

| kind | 使用时机 |
|------|---------|
| `task` | 用户发来新指令时（**每条指令必须首先上报**） |
| `think` | 开始分析/推理时 |
| `tool` | 准备调用任何工具前 |
| `exec` | 执行命令、部署等 |
| `fetch` | 读取文件、API 调用 |
| `write` | 写入/修改文件 |
| `search` | 搜索文件、代码 |
| `info` | **通用信息 / 纯文本回复内容**（笑话、故事、诗歌、对话等） |
| `result` | 子任务或整体任务完成 |
| `error` | 执行出错 |

**执行顺序模板**：

**路径 A：涉及工具调用**（搜索、执行命令、读写文件等）
```bash
python3 /tmp/trtc_stream/agent_bus.py task  "收到指令：<内容>"
python3 /tmp/trtc_stream/agent_bus.py think "分析：<判断>"
python3 /tmp/trtc_stream/agent_bus.py <kind> "<执行操作>"   # 每个关键步骤
# [实际工具调用]
python3 /tmp/trtc_stream/agent_bus.py result "<完成摘要>"
```

**路径 B：纯文本回复**（讲笑话、写诗、聊天对话等不涉及工具调用）
```bash
python3 /tmp/trtc_stream/agent_bus.py task  "收到指令：<内容>"
python3 /tmp/trtc_stream/agent_bus.py think "分析：这是纯文本生成任务"
python3 /tmp/trtc_stream/agent_bus.py info  "<回复内容片段1>"     # 流式分段，每段≤200字
python3 /tmp/trtc_stream/agent_bus.py info  "<回复内容片段2>"     # 长文本可多次调用
python3 /tmp/trtc_stream/agent_bus.py result "回复完成"
```

> ⚠️ **路径 B 是最容易遗漏上报的场景**：纯文本回复不涉及工具调用，
> 如果不通过 `info` 上报回复内容，Dashboard 会从 `[THINK]` 直接跳到 `[OK]`，
> 观众看不到回复正文，TTS 也无法播报回复内容。
> **长文本建议分段**：每段不超过 200 字，多次调用 `info` 逐段输出，Dashboard 和 TTS 会逐段显示和播报。

**最低频率要求**：
- **每个用户指令**：至少上报 `task`（开头）+ `result`/`error`（结尾）
- **每次工具调用**：至少上报一次对应 kind
- **纯文本回复**：必须用 `info` 上报回复正文（可多次调用分段输出，这是观众唯一能看到回复内容的途径）
- **长时间推理**：每 10-15 秒上报一次 `think`，保持 Dashboard 活跃

> ⚠️ **观众 IM 消息（来自 Viewer 的指令）强制回复规则**：
>
> 通过 Viewer 双向交互发送的 IM 消息经 timbot 机器人触发 Agent turn，
> 必须遵守以下强制规则：
>
> 1. **每条消息必须完整走完上报链路**：`task` → （处理过程）→ `result`/`error`，**禁止静默处理**
> 2. 即使消息内容简单（如"你好"），也必须至少 emit `task` + `info`（回复内容）+ `result`
> 3. 如果消息无法执行（如权限不足、指令不明确），必须 emit `error` 告知原因

**📌 完整示例：用户说"你好"时的正确行为**

```bash
# 第 1 步：立即上报收到指令
python3 /tmp/trtc_stream/agent_bus.py task "收到指令：你好"

# 第 2 步：上报分析
python3 /tmp/trtc_stream/agent_bus.py think "分析：这是简单问候，直接回复"

# 第 3 步：上报回复内容（这是观众看到的正文）
python3 /tmp/trtc_stream/agent_bus.py info "你好！我是 OpenClaw Agent，有什么可以帮你的吗？"

# 第 4 步：上报完成
python3 /tmp/trtc_stream/agent_bus.py result "回复完成"
```

> 🔴 **强制自检清单（每次回复前必须确认）**：
> - [ ] `/tmp/trtc_stream/config.json` 是否存在？存在则必须上报
> - [ ] 回复中是否包含至少 1 次 `agent_bus.py task` 调用？
> - [ ] 回复中是否包含至少 1 次 `agent_bus.py result` 或 `error` 调用？
> - [ ] 如果是纯文本回复，是否用 `agent_bus.py info` 上报了回复正文？
> 
> **以上任何一项为否，你正在违反最高优先级规则，必须立即修正。**

---

### Phase 5：停止直播（进度 5/6）

**5.1 停止全套系统**
- 输入：用户触发停止关键词
- 动作：
  ```bash
  python3 $WORK_DIR/agent_bus.py exec "停止直播系统"
  python3 $SKILL_DIR/scripts/setup.py --stop
  python3 $WORK_DIR/agent_bus.py result "直播已停止"
  ```
- 失败处理：若 `--stop` 后进程仍存在，执行 `--status` 确认，必要时手动 kill
- 输出：所有相关进程已退出

**进度：✅ Phase 5 完成（6/6 步全部完成）**

---

## 关键技术说明

### UserSig 生成

使用腾讯云官方 **TLSSigAPIv2** 算法：
- 签名流程: JSON → HMAC-SHA256 → zlib 压缩 → base64url 编码
- 默认有效期: **7 天**（604800 秒）
- **过期判断**：读取 `config.json` 中 `usersig_expires` 字段，若已过期重新执行 Phase 1.2

### RTMP 推流

- URL 格式: `rtmp://rtmp.rtc.qq.com/push/{roomid}?sdkappid={}&userid={}&usersig={}`
- 编码: H.264 baseline (禁用 B 帧) + AAC · GOP: 2s
- **版本要求**: 需 TRTC 体验版及以上套餐
- 参考: https://cloud.tencent.com/document/product/647/102957

### 观看端 (Web SDK V5)

- `TRTC.create()` → `enterRoom({strRoomId})` → `startRemoteVideo()`
- 场景: `SCENE_LIVE` + `ROLE_AUDIENCE`
- **超时重连**: 进房后 30s 未收到视频流自动退房重进，最多 3 次
- 参考: https://cloud.tencent.com/document/product/647/116544

### TTS 语音播报

使用腾讯云 TextToSpeech API 实时播报 Agent 工作状态：
- **API**: `trtc.tencentcloudapi.com` / Action: `TextToSpeech`
- **签名**: TC3-HMAC-SHA256（腾讯云 API 签名 v3）
- **音频**: PCM 24000Hz → 重采样到 44100Hz（推流管线采样率）
- **架构**: tts_worker 守护进程追尾读取 agent_events.jsonl（文件偏移量追踪，零事件丢失）→ 调用 TTS API → PCM 写入 audio_queue/ → stream_daemon 的 AudioMixer 混入音轨
- **轮询策略**: 自适应退避（活跃期 100ms / 空闲期逐步退避到 1s）
- **长文本处理**: 超过 280 字符自动按标点分段（换行 > 句号 > 逗号 > 硬截断），逐段合成播报，队列满时丢弃剩余分段
- **防抖**: 同一状态 2 秒内不重复播报 · **队列上限**: 5 个
- **状态映射**:

| kind | 播报文案 |
|------|---------|
| `idle` | 主人，小龙虾待命中 |
| `think` | 让小龙虾想想 |
| `task` | 收到主人，小龙虾马上开始 |
| `tool` | 小龙虾正在调用工具 |
| `exec` | 小龙虾正在执行中 |
| `info` | （直接播报全文——纯文本回复内容也通过 info 流式分段输出） |
| `result` | 报告主人，任务完成啦 |
| `error` | 哎呀，小龙虾遇到错误了 |

> 💡 配置 CAM 密钥即可启用。不配置时系统正常运行但无语音播报。

---

## 配置文件格式

工作目录（Linux: `/tmp/trtc_stream/`，Windows: `%TEMP%\trtc_stream\`）下的 `config.json`：

```json
{
  "sdkappid": 1400000001,
  "room_id": "openclaw-live-abc123",
  "streamer_userid": "streamer-xy12",
  "viewer_userid": "viewer-ab34",
  "usersig": "eJwt...",
  "viewer_usersig": "eJxt...",
  "usersig_expires": "2026-03-26T12:00:00+00:00",
  "rtmp_url": "rtmp://rtmp.rtc.qq.com/push/...",
  "skill_source_dir": "/path/to/openclaw-agent-live",
  "lighthouse_ip": "(optional) 公网 Lighthouse IP",
  "viewer_url": "(optional)",
  "tts_secret_id": "(optional) AKIDxxxxxxxx",
  "tts_secret_key": "(optional) xxxxxxxx",
  "im_userid": "im-viewer-ab12",
  "im_usersig": "eJxx...",
  "im_bot_userid": "@RBT#001"
}
```

> `skill_source_dir` 由 `setup.py --sdkappid` 初始化时自动写入，记录 Skill 安装目录的绝对路径。`--start` 时据此定位 `assets/` 资源目录，**无需手动修改**。
> `im_userid` / `im_usersig` 用于双向交互功能，初始化时自动生成（复用 TRTC 的 TLSSigAPIv2 算法）。
> `lighthouse_ip` 为公网访问 IP，可通过 `--viewer --lighthouse-ip` 时指定。

---

## 架构说明

详见 `references/architecture.md`
