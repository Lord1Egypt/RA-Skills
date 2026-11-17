# 用户手册(SOP)· 聚星逸配置

> 面向终端用户的标准操作流程。跟着走,3 分钟完成聚星逸接入 OpenClaw。

---

## 一、前置条件

| 项 | 要求 |
|----|------|
| OpenClaw | 已安装并初始化(`~/.openclaw/openclaw.json` 存在) |
| Node.js | 18.0 或更高(终端运行 `node -v` 确认) |
| 聚星逸账号 | 已注册,有 `fsk-` 开头的 API Key |
| Skill | 已安装 `huo15-juxingyi-configure` |

### 没有聚星逸账号?

1. 打开 [聚星逸控制台](https://fireworks-simulator.huo15.com/app/)
2. 用手机号 + 验证码注册
3. 新用户注册即赠体验额度
4. 进入「API 密钥」页,点击新建,生成 `fsk-` 开头的密钥(**明文仅展示一次,请妥善保存**)

---

## 二、安装 Skill

### 方式 A:从 ClawHub 安装(推荐)

```bash
clawhub install huo15-juxingyi-configure --dir ~/.openclaw/workspace/skills
```

### 方式 B:从源码安装

```bash
git clone https://cnb.cool/huo15/ai/huo15-skills.git
cp -r huo15-skills/huo15-juxingyi-configure/ ~/.openclaw/workspace/skills/
```

---

## 三、标准配置流程

### Step 1 · 进入 skill 目录

```bash
cd ~/.openclaw/workspace/skills/huo15-juxingyi-configure
```

### Step 2 · 运行配置脚本

```bash
node scripts/configure.mjs fsk-你的密钥
```

**脚本做了什么**:
1. 调用聚星逸 `/v1/models` 接口获取最新模型列表(完全来自接口,无本地清单)
2. 跳过生图/视频模型
3. 写入 `~/.openclaw/openclaw.json`
4. 主模型取接口返回列表的第一个
5. 自动备份原配置

**成功输出示例**:
```
✅ 聚星逸配置完成!
   备份: ~/.openclaw/openclaw.json.bak.2026-07-19T00-00-00-000Z
   模型数: 30 个文本对话模型
   主模型: fireworks-hub/DeepSeek-V4-Flash
   备选链: 29 个模型
   密钥存储: 直接写入(明文)

   主模型 & 备选链:
   ★ fireworks-hub/DeepSeek-V4-Flash
     fireworks-hub/DeepSeek-V4-Pro
     ...

重启 OpenClaw 后生效。
```

> **关于模型参数**:接口只返回模型 `id`,不返回上下文窗口等。脚本填保守默认值(`contextWindow`: 131072, `maxTokens`: 8192, `reasoning`: false)保证可用,可手动调整。

### Step 3 · 询问是否切换主模型

配置完成后,**AI 会主动问你**是否切换到其他模型(因为主模型是自动取的列表第一个)。

**如果你想切换**:
```
回复模型名即可,如 "DeepSeek-V4-Pro" 或 "claude-opus-4-8"
```

或直接运行:
```bash
node scripts/configure.mjs --switch DeepSeek-V4-Pro
```

**如果你想知道有哪些模型可选**:
```bash
node scripts/configure.mjs fsk-你的密钥 --list
```

输出示例:
```
🛰️  聚星逸 · 可用模型(来自 /v1/models 接口)
   共 40 个,其中 30 个文本对话模型

文本对话模型(将写入配置):
  DeepSeek-V4-Flash                 Deepseek V4 Flash (聚星逸) ★ 默认主模型
  DeepSeek-V4-Pro                   Deepseek V4 Pro (聚星逸)
  GPT-5.5                           Gpt 5.5 (聚星逸)
  ...

生图/视频模型(跳过,不配文本对话): 10 个
  Seedream-Image
  ...
```

### Step 4 · 重启 OpenClaw

```bash
openclaw restart
```

重启后,OpenClaw 会使用聚星逸的模型进行对话。

---

## 四、日常操作

### 查看当前配置

```bash
node scripts/configure.mjs --show
```

输出示例:
```
🛰️  聚星逸当前配置
   Provider: fireworks-hub
   Base URL: https://fireworks-simulator-api.huo15.com/v1
   API 类型: openai-completions
   密钥方式: 直接密钥 (fsk-Gho…)
   文本模型: 30 个
   主模型:   fireworks-hub/DeepSeek-V4-Flash
   备选链:
     fireworks-hub/DeepSeek-V4-Pro
     ...

   已配模型:
   ★  DeepSeek-V4-Flash                 Deepseek V4 Flash (聚星逸)
      DeepSeek-V4-Pro                   Deepseek V4 Pro (聚星逸)
      ...
```

### 切换主模型

```bash
node scripts/configure.mjs --switch claude-opus-4-8
```

输出示例:
```
✅ 主模型已切换
   备份: ~/.openclaw/openclaw.json.bak.2026-07-19T...
   旧主: fireworks-hub/DeepSeek-V4-Flash
   新主: fireworks-hub/claude-opus-4-8
   备选: 29 个模型

重启 OpenClaw 后生效。
```

### 重新配置(平台新增了模型)

**日常更新推荐用 `--update`(保留当前主模型)**:

```bash
node scripts/configure.mjs fsk-你的密钥 --update
```

`--update` 与重新配置(不加 `--update`)的区别:
- `--update`:**保留当前主模型**(若仍在平台列表),只刷新模型列表,报告新增/移除
- 不加 `--update`:主模型重置为列表第一个(适合从头重新配置)

`--update` 输出示例:
```
✅ 聚星逸模型列表已更新!
   备份: ~/.openclaw/openclaw.json.bak.2026-07-19T...
   模型数: 18 → 20 个文本对话模型
   ✨ 新增 2 个:
     + NewModel-X1
     + NewModel-X2
   主模型保留: fireworks-hub/DeepSeek-V4-Flash
   备选链: 19 个模型

重启 OpenClaw 后生效。
```

**想从头重新配置**(不保留主模型):

```bash
node scripts/configure.mjs fsk-你的密钥
```

> 重新配置不会丢失其他 provider 的设置,只更新 `fireworks-hub` 段。

---

## 五、安全选项

### 默认:密钥明文存储

最简单的方式,密钥直接写在 `openclaw.json` 中。

### 推荐:环境变量引用

```bash
# 配置时加 --env
node scripts/configure.mjs fsk-你的密钥 --env

# 然后设置环境变量(加到 ~/.zshrc 或 ~/.bashrc)
export FIREWORKS_API_KEY=fsk-你的密钥

# 重启 OpenClaw 前确保环境变量已加载
source ~/.zshrc
```

配置文件中只存:
```json
"apiKey": {
  "source": "env",
  "provider": "default",
  "id": "FIREWORKS_API_KEY"
}
```

---

## 六、模型选择建议

配置完成后,可根据用途切换主模型(用 `--switch`):

| 场景 | 推荐方向 |
|------|---------|
| 日常编程、快速问答 | DeepSeek 系列、Qwen 系列 |
| 复杂代码生成、架构设计 | GPT 系列、Claude Opus 系列 |
| 深度分析、数学推理 | DeepSeek-R1 等推理模型 |
| 长文档处理 | Gemini 系列(长上下文) |
| Claude 系列偏好 | claude-opus / claude-sonnet |
| 国产模型偏好 | Qwen / GLM / DeepSeek |

> 完整可用模型以 `--list` 调接口实时返回为准,平台会不断新增。

---

## 七、常见问题

### Q1:配置后 OpenClaw 报错 "model not found"

**原因**:未重启 OpenClaw。

**解决**:
```bash
openclaw restart
```

### Q2:API 返回 401

**原因**:密钥无效或已过期。

**解决**:
1. 去 [聚星逸控制台](https://fireworks-simulator.huo15.com/app/) →「API 密钥」确认密钥状态
2. 重新运行配置脚本

### Q3:用了 `--env` 但 OpenClaw 报 "API key not found"

**原因**:环境变量未设置或未加载。

**解决**:
```bash
# 检查环境变量
echo $FIREWORKS_API_KEY

# 如果为空,设置它
export FIREWORKS_API_KEY=fsk-你的密钥
source ~/.zshrc  # 或 ~/.bashrc

# 然后重启 OpenClaw
openclaw restart
```

### Q4:想恢复配置前的状态

**解决**:找到备份文件,恢复即可:
```bash
ls ~/.openclaw/openclaw.json.bak.*
# 选最近的
cp ~/.openclaw/openclaw.json.bak.2026-07-19T00-00-00-000Z ~/.openclaw/openclaw.json
openclaw restart
```

### Q5:平台新增了模型,怎么更新配置?

**解决**:用 `--update` 日常更新(保留当前主模型):
```bash
node scripts/configure.mjs fsk-你的密钥 --update
```

脚本会调接口拿最新列表,报告新增/移除的模型,保留你当前选的主模型。无需更新 skill 本身。

如果想从头重新配置(不保留主模型),直接运行:
```bash
node scripts/configure.mjs fsk-你的密钥
```

### Q6:主模型不是我想要的

**原因**:主模型自动取接口返回列表的第一个,可能不是你偏好的。

**解决**:配置完成后 AI 会主动询问是否切换,回复模型名即可。或随时运行:
```bash
node scripts/configure.mjs --switch 你想要的模型名
```

---

## 八、命令速查卡

```bash
# ── 配置 ──
node scripts/configure.mjs <fsk-key>           # 首次配置(主模型取列表第一个)
node scripts/configure.mjs <fsk-key> --env     # 配置(密钥用环境变量)

# ── 日常更新 ──
node scripts/configure.mjs <fsk-key> --update  # 更新模型列表(保留当前主模型)

# ── 查看 ──
node scripts/configure.mjs --show              # 查看当前配置
node scripts/configure.mjs <fsk-key> --list    # 列出接口返回的模型

# ── 切换 ──
node scripts/configure.mjs --switch <model-id> # 切换主模型
```

---

## 九、获取帮助

| 渠道 | 信息 |
|------|------|
| 聚星逸控制台 | https://fireworks-simulator.huo15.com/app/ |
| 接入文档 | https://fireworks-simulator.huo15.com/docs.html |
| 辉火管家 AI | 网站右下角悬浮按钮,7×24 在线答疑 |
| QQ 群 | 1093992108 |
| 邮箱 | postmaster@huo15.com |
| 电话 | 185 5489 8815 |
| 公众号 | 逸寻智库(扫码关注) |

---

**青岛火一五信息科技有限公司**
