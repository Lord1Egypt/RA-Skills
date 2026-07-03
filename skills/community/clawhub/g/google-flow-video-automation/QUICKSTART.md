# Google Flow 自动化 - 快速入门

## 5分钟上手

### 步骤1：启动 Chrome（开启 CDP 调试）

**首次运行需要执行**（之后 Chrome 会记住设置）：

```bash
# 完全关闭所有 Chrome 窗口
pkill -9 "Google Chrome"

# 启动 Chrome 并开启远程调试（端口 9222）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" \
  "https://labs.google/fx/tools/flow" &
```

### 步骤2：手动登录（一次性）

在打开的 Chrome 窗口中：
1. 点击 **"Create with Google Flow"**
2. 登录你的 Google 账号（只需首次登录，之后 Cookie 保持）
3. 完成登录后，**保持 Chrome 开着**

### 步骤3：准备提示词文件

创建一个文本文件（例如 `prompts.txt`），每行一条提示词：

```
A joyful horse magically stepping out of a glowing screen into the viewer's hands, warm lighting, cinematic
A happy golden dog leaping out of a bright screen into the viewer's open hands, playful and magical, cinematic
A cat jumping out of a tablet screen, surprised expression, 4k
```

**提示词建议（英文效果更佳）**：
- 描述要具体（动作、表情、光线）
- 加上 `cinematic`、`4k`、`warm lighting` 等关键词
- 避免太复杂的场景（Google Flow 擅长简单主体+动作）

### 步骤4：运行自动化脚本

```bash
# 进入 Skill 目录
cd ~/.workbuddy/skills/google-flow-automation

# 生成单条视频
node google-flow-fast.js --prompt "A happy horse walking out of the screen" --output ./my-videos

# 批量生成（从文件读取）
node google-flow-fast.js --prompts prompts.txt --output ./my-videos

# 自定义参数（比例、时长）
node google-flow-fast.js \
  --prompts prompts.txt \
  --output ./my-videos \
  --ratio "16:9" \
  --duration "x2"
```

## 配置参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--prompts <file>` | 提示词文件（每行一条） | - |
| `--prompt <text>` | 单条提示词 | - |
| `--output <dir>` | 输出目录 | `./videos` |
| `--ratio` | 视频比例 | `16:9` |
| `--duration` | 时长（`x1`=5s, `x2`=10s, `x3`=15s, `x4`=20s） | `x2` |

## 优化建议（减少 Token 消耗）

### 1. 使用优化版脚本

`google-flow-fast.js` 比 `google-flow-automate.js` 更快，因为：
- ✅ 首次运行后会缓存成功的元素选择器
- ✅ 减少不必要的截图和快照
- ✅ 批量生成时复用页面状态

### 2. 避免频繁探索

首次运行后，selectors 会自动保存到 `selectors.json`。后续运行会直接使用缓存，速度提升 **3-5倍**。

### 3. 批量生成

一次运行生成多条视频，避免重复连接和登录：

```bash
# 在 prompts.txt 中放入所有提示词
node google-flow-fast.js --prompts prompts.txt --output ./videos
```

## 常见问题

### Q1: Chrome CDP 连接失败

**错误**：`Failed to connect to Chrome via CDP`

**解决**：
```bash
# 检查 Chrome 是否在运行
ps aux | grep "remote-debugging-port=9222"

# 检查端口是否可访问
curl http://127.0.0.1:9222/json/version

# 如果端口被占用，重启 Chrome
pkill -9 "Google Chrome"
# 然后重新执行步骤1
```

### Q2: 元素找不到（Selector 失效）

**错误**：`Failed to find element for action: createButton`

**解决**：
```bash
# 删除缓存的 selectors，让脚本重新探索
rm ~/.workbuddy/skills/google-flow-automation/selectors.json

# 重新运行脚本（会重新探索并缓存）
node google-flow-fast.js --prompts prompts.txt
```

### Q3: 视频生成太慢

**原因**：Google Flow 有队列机制，高峰期需要等待。

**解决**：
- 调整 `config.json` 中的 `maxWaitTime`（默认 10分钟）
- 避免在高峰期使用（美国时间白天）

### Q4: 下载失败

**原因**：视频 URL 是临时的，可能已过期。

**解决**：
- 脚本会自动点击下载按钮
- 检查 Chrome 的下载目录（默认 `~/Downloads`）
- 或者手动在 Google Flow 页面点击下载

## 高级用法

### 1. 自定义视频参数

编辑 `config.json`：

```json
{
  "defaultRatio": "16:9",
  "defaultDuration": "x2",
  "pollInterval": 5000,
  "maxWaitTime": 600000
}
```

### 2. 调试模式（开启截图）

```bash
# 编辑 config.json，设置：
{
  "screenshotOnError": true,
  "logLevel": "debug"
}
```

### 3. 并行生成（多个 Chrome 实例）

```bash
# 启动多个 Chrome（不同端口）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9223 \
  --user-data-dir=/tmp/chrome-profile-2 &

# 修改 config.json 中的 cdpPort，然后运行第二个实例
```

## 技术细节

### 为什么使用 Chrome CDP？

- ✅ **绕过 Google 登录检测**：使用真实 Chrome（非 Chromium）
- ✅ **复用登录状态**：Cookie 和 Session 自动保存
- ✅ **稳定可靠**：不会因为 Google 安全策略更新而失效

### 为什么不用 Selenium/Puppeteer？

- Playwright 的 `connectOverCDP` 更稳定
- `playwright-core` 比完整 Playwright 小 80%
- 支持多浏览器（Chromium/Firefox/WebKit）

### Token 消耗优化原理

1. **缓存 Selectors**：首次探索后保存，后续直接使用
2. **减少截图**：只在失败时截图，平时用 JS 执行结果判断
3. **批量操作**：一次连接，生成多条视频
4. **智能等待**：用 `waitForSelector` 代替轮询

## 文件结构

```
~/.workbuddy/skills/google-flow-automation/
├── SKILL.md                      # 详细文档
├── QUICKSTART.md                 # 本文件
├── google-flow-automate.js       # 完整版脚本（带详细日志）
├── google-flow-fast.js           # 优化版脚本（减少 Token 消耗）
├── config.json                    # 配置文件
├── selectors.json                 # Selector 缓存（自动生成）
└── examples/
    └── prompts-example.txt       # 示例提示词
```

## 下一步

- [ ] 加入代理支持
- [ ] 支持多个 Google 账号轮换
- [ ] 支持 Webhook 通知（生成完成后推送）
- [ ] 支持从 Google Drive 直接导出

---

**需要帮助？**  
在 WorkBuddy 中提问："如何使用 Google Flow 自动化 Skill？"
