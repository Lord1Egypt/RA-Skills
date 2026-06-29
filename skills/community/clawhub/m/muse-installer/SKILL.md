---
name: "muse-installer"
description: "Muse一键安装+Onboarding。v1.0.3：DNA页签+进化记录+聊天反馈。Agent全自动装环境→启动后台→引导使用→3问题采集DNA→分析创作平台前十内容→同步Dashboard。"
category: product
---

# 🌀 Muse Installer — 一键安装 + Onboarding（含对话Agent）

> 给 Agent 这个 skill，它全自动帮你装好 Muse，然后像私人管家一样引导你完成 Onboarding。
> 全程你不需要打开终端，只需要回答三个问题。
> v1.0.3 新增：DNA 左栏页签 + 进化记录 + 聊天反馈 👍👎。控制面板和落地页 Hero 都内置对话 Agent。

---

## 🎯 Agent 执行流程（严格按顺序）

---

### Phase 0: 环境自检

Agent 先自查：

```bash
python3 --version && echo PY_OK || echo PY_MISSING
git --version && echo GIT_OK || echo GIT_MISSING
pip3 --version && echo PIP_OK || echo PIP_MISSING
```

**如果缺什么** → 告诉用户缺什么、怎么装（Mac: `brew install`，Win: 给官网链接），不要中断流程——缺 Python 时给安装指引，装好后用户说"继续"就接着走。

---

### Phase 1: 拉代码 + 装依赖

```bash
mkdir -p ~/.muse && cd ~/.muse
if [ -d "muse-catch" ]; then
  cd muse-catch && git pull origin main
else
  git clone https://github.com/KevPH2026/muse-catch.git && cd muse-catch
fi
pip3 install flask 2>&1 | tail -3
```

---

### Phase 2: 启动后台服务

```bash
cd ~/.muse/muse-catch
# 杀掉旧进程（如果有）
pkill -f "python3 server.py" 2>/dev/null
sleep 1
# 后台启动
nohup python3 server.py > /tmp/muse-server.log 2>&1 &
sleep 3
# 验证
curl -s http://localhost:5200/api/stats && echo "✅ Muse API 运行中" || echo "❌ 启动失败，查看 /tmp/muse-server.log"
```

---

### Phase 3: 告诉用户安装完成 + 发插件

> 🌀 **Muse 安装完成！**
>
> 🌐 **控制面板**：http://localhost:5200/app
> 💬 **Muse AI 对话**：右下角蓝色按钮打开聊天 Agent，或直接在落地页 http://localhost:5200/ 右侧体验
> 🧬 **DNA 页签**：左侧栏点击"🧬 DNA"查看完整创作 DNA 画像 + 进化记录
> 📝 **进化记录**：在聊天中点击 👍👎 给 AI 回复反馈，系统自动记录并进化
>
> 🧩 **浏览器插件**：`~/.muse/muse-catch/extension/`
> Chrome → `chrome://extensions` → 开启「开发者模式」→「加载已解压的扩展程序」→ 选上面的文件夹。

**不用等用户确认插件装没装**。直接进入 Phase 4。

---

### Phase 4: 使用方式介绍

Agent 向用户发送以下介绍：

> 现在你有四种方式捕获灵感：
>
> **① 浏览器插件（主力）**
> - 看到好内容 → 点插件图标 → 一键捕获
> - 刷 Twitter/X 时点收藏 → 自动导入灵感池
> - 粘贴微信公众号文章链接 → 自动抓取保存
> - 快捷键 `Ctrl+Shift+M` 直接捕获
>
> **② 直接跟我说**
> - 「记一下：XXX」
> - 「捕获：XXX」
> - 发一条链接 +「存起来」
>
> **③ Telegram Bot（可选）**
> - 转发消息给 Bot → 自动入库
> - 要配置就说「帮我配 Telegram Bot」
>
> 所有灵感 AI 自动提炼标题、摘要、关键词、情绪。

说完这些后，**立即进入 Phase 5 Onboarding**。

---

### Phase 5: Onboarding — 采集用户 DNA

Agent 主动发起三个问题：

> 花 2 分钟做个 Onboarding，Muse 以后提炼灵感时自动关联你的赛道。
>
> **① 你对哪些领域/方向感兴趣？**
> 比如「AI + 教育」「跨境电商」「内容创作」——越具体越好。

等待用户回答。收到后：

> 收到。
>
> **② 你的职业是什么？**
> 比如「跨境营销 COO」「独立开发者」「产品经理」。

等待用户回答。收到后：

> 收到。
>
> **③ 你有内容创作平台吗？有的话把链接发给我。**
> Twitter/X、公众号、小红书、博客、播客都行。没有的话直接说「没有」。

等待用户回答。

---

### Phase 6: DNA 分析

**如果用户发了平台链接**（如 Twitter URL）：

1. **抓取前 10 条内容：**

   | 平台 | 抓取方式 |
   |------|---------|
   | Twitter/X | `opencli twitter user <用户名> --count 10` 或用 Chromium 打开主页截图+提取 |
   | 微信公众号 | 用户粘贴文章链接列表 |
   | 小红书 | `opencli xhs user <用户ID> --count 10` |
   | 博客/RSS | `web_fetch <URL>` |

2. **用 Agent 自身 LLM 分析内容，输出 DNA 结构：**

   ```
   【创作 DNA】
   - 赛道/领域: xxx
   - 内容风格: xxx
   - 核心话题: xxx, xxx, xxx
   - 受众画像: xxx
   - 差异化特征: xxx
   - 可深挖方向: xxx, xxx
   ```

3. **同步到控制面板：**

   ```bash
   curl -s -X POST http://localhost:5200/api/profile \
     -H 'Content-Type: application/json' \
     -d '{
       "profile": {
         "interests": "问题1回答",
         "occupation": "问题2回答",
         "platform": "问题3回答",
         "dna": {
           "niche": "赛道",
           "style": "风格",
           "topics": ["话题1","话题2"],
           "audience": "受众",
           "differentiator": "差异化",
           "deep_directions": ["方向1","方向2"]
         }
       }
     }'
   ```

**如果用户没发平台链接** → 跳过抓取，仅用三个问题的回答生成基础 DNA 并同步。

---

### Phase 7: Onboarding 完成

> 🌀 **Onboarding 完成！你的创作 DNA：**
>
> 🎯 **赛道**：xxx
> ✍️ **风格**：xxx
> 🔥 **核心话题**：xxx, xxx
> 👥 **受众**：xxx
>
> 已同步到控制面板 → http://localhost:5200/app（左栏 🧬 DNA 页签查看完整画像）
>
> 💡 **进化机制**：每次和 Muse AI 对话后点 👍👎 反馈，系统会记录你的偏好并持续进化。
>
> 开始第一条捕获：
> - 打开网页 → 点 Muse 插件图标
> - 或直接跟我说：「记一下：xxx」

---

### Bonus: Telegram Bot 配置

用户说「帮我配 Telegram Bot」时：

> 1. Telegram 找 @BotFather → `/newbot` → 起名 → 拿到 Token
> 2. 把 Token 发给我

收到 Token 后：

```bash
cd ~/.muse/muse-catch
export MUSE_BOT_KEY="<TOKEN>"
nohup python3 bot.py > /tmp/muse-bot.log 2>&1 &
sleep 2 && tail -3 /tmp/muse-bot.log
```

> 🤖 Bot 已启动！去 Telegram 给你的 Bot 发条消息试试。

---

## 🔧 故障速查

| 症状 | 命令 |
|------|------|
| API 拒绝连接 | `curl http://localhost:5200/api/stats` |
| 端口被占 | `lsof -i :5200` → 杀进程 |
| Server 崩溃 | `tail -50 /tmp/muse-server.log` |
| Bot 没反应 | `echo $MUSE_BOT_KEY` 确认已设 |

---

## 📋 激活口令

用户说「帮我装 Muse」，Agent 自动走 Phase 0→1→2→3→4→5→6→7。
