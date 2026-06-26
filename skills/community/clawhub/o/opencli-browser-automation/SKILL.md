---
name: opencli-browser-automation
description: 基于 opencli + Chrome/Chromium Browser Bridge 的轻量化浏览器自动化技能。实现无需付费API即可操控浏览器，支持502条命令覆盖79个网站，支持知乎热榜、豆包聊天、B站等平台的自动化操作。当用户需要自动化浏览器操作、抓取网页数据、操控AI聊天机器人、执行连续对话任务时使用本技能。
---

# opencli 浏览器自动化技能方案

> 基于 opencli + Chrome/Chromium Browser Bridge，实现轻量化浏览器自动化
>
> **实战验证：2026-04-06 成功测试知乎、豆包连续对话！**

## 一、适用范围

- 公开可访问的网页（无需登录）
- 已登录态的网站（需先在浏览器中登录）
- GitHub、知乎、B站、豆包、小红书等各类网站
- 支持 502 条命令，覆盖 79 个网站和 7 个外部 CLI 工具
- AI 驱动：自动探索网站、生成命令、录制操作
- ✅ **已验证可用**：知乎热榜、B站排行、豆包聊天连续对话

## 二、前置条件

### 2.1 浏览器要求

用户需拥有以下任一浏览器（Edge/Chrome Beta/Chrome Dev 均可）：
- Edge（基于 Chromium，与扩展完全兼容）
- Chrome Beta（推荐，opencli 官方测试环境）
- Chrome Dev

### 2.2 扩展安装步骤

1. 下载扩展包：`opencli-extension.zip`（已备份至 `D:\BaiduSyncdisk\Workbuddy\backup\`）
2. 解压到任意目录
3. 打开浏览器 `edge://extensions/` 或 `chrome://extensions/`
4. 开启右上角「开发者模式」
5. 点击「加载解压缩的扩展」，选择解压后的文件夹

### 2.3 验证扩展连接状态

```powershell
opencli doctor
```

输出应显示：
```
Extension: connected ✅
```

⚠️ **重要**：Chrome Beta 必须保持运行，扩展才能连接。关闭浏览器后需重新打开才能恢复。

## 三、核心命令速查

### 基础操作（opencli operate）

| 命令 | 用途 |
|------|------|
| `opencli doctor` | 检查扩展连接状态 |
| `opencli daemon status` | 查看守护进程状态（PID/端口/内存） |
| `opencli operate open <URL>` | 打开网页 |
| `opencli operate state` | 获取页面可交互元素列表 |
| `opencli operate click <index>` | 点击元素（按索引） |
| `opencli operate type <index> <text>` | 输入文字 |
| `opencli operate screenshot [path]` | 截图 |
| `opencli operate eval <js>` | 执行 JavaScript |
| `opencli operate wait [秒数]` | 等待页面加载 |
| `opencli operate scroll [px]` | 滚动页面 |

### AI 驱动的高级命令

| 命令 | 用途 |
|------|------|
| `opencli explore <url>` | 探索网站，自动发现可用接口、API、存储结构 |
| `opencli generate <url>` | 一键：探索→合成→注册，直接生成新命令 |
| `opencli cascade <url>` | 策略级联：自动找最简单的可用策略 |
| `opencli record <url>` | 录制浏览器操作，生成 YAML 命令候选 |
| `opencli validate <target>` | 验证命令定义是否正确 |
| `opencli verify <target>` | 验证+冒烟测试 |
| `opencli plugin` | 管理插件 |

### 常用平台命令示例

| 平台 | 命令示例 | 说明 |
|------|----------|------|
| 知乎 | `opencli zhihu hot` | 知乎热榜（✅已验证） |
| B站 | `opencli bilibili ranking` | B站热门视频（✅已验证） |
| Hacker News | `opencli hn top` 或 `opencli hackernews top` | HN 热帖（✅已验证） |
| V2EX | `opencli v2ex hot` | V2EX 热门话题 |
| 36氪 | `opencli 36kr hot` | 36氪热榜 |
| 新浪财经 | `opencli stock <代码>` | A股/港股/美股行情 |
| YouTube | `opencli youtube search <关键词>` | YouTube 搜索 |
| 豆包/元宝 | `opencli yuanbao ask "问题"` | 腾讯元宝对话 |
| 携程 | `opencli ctrip search <目的地>` | 携程搜索 |
| 虎扑 | `opencli tihu detail <帖子ID>` | 虎扑帖子详情 |
| 小红书 | `opencli xhs user <用户ID>` | 小红书用户笔记（需cookie） |

## 四、豆包聊天操作流程（✅实战验证）

豆包是字节跳动旗下的 AI 助手，支持连续对话、代码编写、图片生成等。

### 4.1 操作步骤

```powershell
# 1. 先确认扩展连接
opencli doctor

# 2. 打开豆包
opencli operate open "https://www.doubao.com"

# 3. 等待页面加载
Start-Sleep -Seconds 3

# 4. 查看页面状态（找到输入框索引）
opencli operate state

# 5. 定位输入框（注意：豆包的输入框每次状态查询会变ID）
# 方法A：用 state 返回的索引，如 [162] 或 [214] 等
opencli operate type <索引> "你好，请介绍一下你自己"

# 方法B：用 JS 定位（更可靠）
opencli operate eval "document.querySelector('[data-testid=chat_input_input]')?.focus()"

# 6. 发送消息（用 JS 模拟 Enter 键，最可靠）
opencli operate eval "document.querySelector('[data-testid=chat_input_input]')?.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}))"

# 7. 等待回复（豆包通常 3-5 秒回复）
Start-Sleep -Seconds 5

# 8. 获取回复内容
opencli operate eval "document.body.innerText"

# 9. 截图查看实际效果
opencli operate screenshot "C:\path\to\doubao_result.png"
```

### 4.2 连续对话技巧

```powershell
# 每条消息发送后，输入框元素ID会变化，需要重新定位
# 流程：state → 找输入框索引 → type → eval发送

# 示例：连续对话3次
# 第1轮
opencli operate state | Select-String "chat_input"
# 假设输出：[162]<textarea ... />
opencli operate type 162 "请帮我写一首诗"
opencli operate eval "..." # 发送

# 第2轮（输入框ID变成其他数字）
opencli operate state | Select-String "chat_input"
# 假设输出：[214]<textarea ... />
opencli operate type 214 "这首诗很美！是即兴创作的吗？"
opencli operate eval "..." # 发送
```

### 4.3 豆包可用功能

| 功能 | 状态 | 示例 |
|------|------|------|
| 自我介绍 | ✅ 已验证 | "你好，请介绍一下你自己" |
| 文字创作 | ✅ 已验证 | "写一首关于春天的七言绝句" |
| 连续对话 | ✅ 已验证 | 能记住前面的对话内容 |
| 代码编写 | ✅ 已验证 | "用Python写一个计算天数的函数" |
| 图片生成 | ⚠️ 可用 | "请帮我画一幅春天的风景画" |

### 4.4 豆包操作注意事项

1. **输入框定位**：豆包的输入框选择器是 `[data-testid=chat_input_input]`
2. **发送方式**：用 JS 模拟 Enter 键比直接用 `opencli operate click` 更可靠
3. **等待时间**：文字回复 3-5 秒，代码回复 2-3 秒，图片生成可能需要 10-20 秒
4. **上下文保持**：连续对话正常，会记住之前的内容
5. **URL变化**：开始对话后 URL 会变成类似 `/chat/38420299164573698` 这样的对话ID

## 五、知乎操作流程（✅实战验证）

### 5.1 无需登录的操作

```powershell
# 1. 打开热榜
opencli operate open "https://www.zhihu.com/hot"

# 2. 直接获取热榜数据（无需登录）
opencli zhihu hot
```

### 5.2 需要登录的操作

```powershell
# 1. 人工在浏览器中完成登录
# 2. 之后可以直接操作
opencli operate open "https://www.zhihu.com/search?type=question&q=关键词"
Start-Sleep -Seconds 3

# 3. 滚动查看内容
opencli operate eval "window.scrollBy(0, 500)"
Start-Sleep -Seconds 2

# 4. 提取搜索结果
opencli operate eval "JSON.stringify([...document.querySelectorAll('h2, .ContentItem-title')].map(el=>el.innerText).filter(t=>t.trim()).slice(0,20))"
```

### 5.3 知乎注意事项

1. **登录后完全可用**：热榜、搜索都能正常工作
2. **操作节奏**：适当加 `wait`，模拟真人操作节奏
3. **触发验证**：知乎有反AI检测，大规模操作可能触发验证

## 六、高级技巧

### 6.1 截图调试

```powershell
# 关键步骤后截图确认
opencli operate screenshot "C:\path\to\debug1.png"

# 对比操作前后
opencli operate screenshot "C:\path\to\before.png"
# 执行操作...
opencli operate screenshot "C:\path\to\after.png"
```

### 6.2 用 JS 获取结构化数据

```powershell
# 获取页面所有图片链接
opencli operate eval "JSON.stringify([...document.querySelectorAll('img')].map(img=>({src:img.src,alt:img.alt})))"

# 获取对话内容（豆包等聊天页面）
opencli operate eval "document.body.innerText"

# 检查元素是否存在
opencli operate eval "document.querySelector('[data-testid=chat_input_input]') !== null"
```

### 6.3 页面滚动

```powershell
# 滚动到指定位置
opencli operate eval "window.scrollTo(0, 500)"
opencli operate eval "window.scrollTo(0, document.body.scrollHeight)"

# 滚动查看完整内容
opencli operate eval "window.scrollBy(0, 500)"
```

### 6.4 等待页面加载

```powershell
# 固定等待
Start-Sleep -Seconds 3

# 循环等待直到页面加载完成
opencli operate state | Select-String "loading"
```

## 七、标准使用流程

### 7.1 日常使用流程

```
1. 确认扩展已加载
   → opencli doctor

2. 导航到目标网页
   → opencli operate open "https://example.com"

3. 获取页面元素
   → opencli operate state

4. 根据索引操作（点击/输入/滚动）
   → opencli operate click 5
   → opencli operate type 3 "搜索内容"

5. 截图确认结果
   → opencli operate screenshot
```

### 7.2 探索新网站（AI驱动）

```
1. 探索网站结构
   → opencli explore "https://target-site.com"

2. 合成新命令
   → opencli synthesize <target>

3. 注册命令
   → opencli register <name>

4. 一键完成以上三步
   → opencli generate "https://target-site.com"
```

### 7.3 需登录网站的流程

```
1. 人工在浏览器中完成登录
2. 在浏览器中手动完成验证（如果有）
3. 之后自动化操作会复用登录态
4. 如再次触发验证，重新人工完成
```

## 八、注意事项

### 8.1 反 AI 检测网站

| 网站 | 验证情况 | 解决方案 | 验证日期 |
|------|----------|----------|----------|
| GitHub | ✅ 无需验证 | 直接可用 | - |
| 36氪 | ✅ 无需验证 | 直接可用 | - |
| Hacker News | ✅ 无需验证 | 直接可用 | 2026-04-06 |
| B站 | ✅ 无需验证 | 直接可用 | 2026-04-06 |
| **知乎** | ✅ **登录后完全可用** | 人工登录一次即可 | 2026-04-06 |
| **豆包** | ✅ **登录后完全可用** | 人工登录后连续对话正常 | 2026-04-06 |
| 微信 | ⚠️ 需扫码 | 需人工辅助 | - |
| 豆包图片生成 | ⚠️ 可能跳转 | 豆包说"我将为你绘制" | 2026-04-06 |

### 8.2 避免触发验证的技巧

- **操作节奏模拟真人**：适当加 `wait`，每次操作间隔 1-2 秒
- **避免高频点击**：不要在 1 秒内连续点击多次
- **先观察页面加载完成再操作**：用 `opencli operate state` 确认页面加载完毕
- **使用 `opencli cascade`**：自动找最安全的策略
- **截图确认**：关键步骤后截图，确认页面状态

### 8.3 故障排查

| 问题 | 解决方案 |
|------|----------|
| Extension: not connected | 重启 Chrome Beta，确保扩展已启用 |
| 守护进程未运行 | 运行 `opencli daemon` 查看状态 |
| 操作无响应 | 先 `opencli operate state` 查看元素状态 |
| Chrome Beta 未运行 | 手动打开 Chrome Beta 浏览器 |
| 页面变空白/空 | 用 `opencli operate open` 重新导航到目标页面 |
| 输入框元素找不到 | 用 `state` 重新定位，元素ID每次会变 |
| 豆包发送后无回复 | 检查是否跳转了页面，等待更长时间 |
| URL 显示 about:blank | 扩展连接断开了，重新 `open` 目标页面 |

## 九、与 agent-browser 的对比

| 维度 | opencli | agent-browser |
|------|---------|---------------|
| 浏览器 | 复用用户已有 Chrome | 自带 Chromium（约 300MB） |
| 登录态 | 完全复用真实浏览器 | 独立 profile |
| 安装大小 | ~30KB（扩展）+ npm 包 | ~300MB |
| 命令数量 | 502 个（79 个网站） | 通用操作 |
| AI 探索 | ✅ 有（explore/generate） | ❌ 无 |
| **推荐场景** | **优先使用**，轻量简洁 | 备选方案 |

## 十、结论

**opencli 是首选工具**，理由：
1. 复用用户已有浏览器，不额外占用空间
2. 502 个现成命令，覆盖常用网站
3. AI 探索功能强大，支持一键生成新命令
4. 安装简单（npm + 扩展），不引入重复依赖
5. 登录态完全复用，避免重复认证

**agent-browser 作为备选**，当：
- opencli 无法连接用户浏览器时
- 需要独立浏览器环境时
- 需要特定 Chromium 版本时

---

## 十一、实战测试记录

| 日期 | 测试内容 | 结果 | 备注 |
|------|----------|------|------|
| 2026-04-06 | Hacker News 热帖 | ✅ 成功 | `opencli hackernews top` |
| 2026-04-06 | B站热门排行 | ✅ 成功 | `opencli bilibili ranking` |
| 2026-04-06 | 知乎热榜 | ✅ 成功 | 登录后 `opencli zhihu hot` |
| 2026-04-06 | 知乎搜索 | ✅ 成功 | `opencli operate open` + JS提取 |
| 2026-04-06 | 豆包自我介绍 | ✅ 成功 | 文字回复正常 |
| 2026-04-06 | 豆包写诗 | ✅ 成功 | "春日七言绝句"意境优美 |
| 2026-04-06 | 豆包连续对话 | ✅ 成功 | 能记住之前的对话内容 |
| 2026-04-06 | 豆包写Python代码 | ✅ 成功 | 完整代码+示例+注释 |
| 2026-04-06 | 豆包图片生成 | ⚠️ 可用 | 说"我将为你绘制"，可能跳转页面 |

---

## 十二、作者信息

**作者**：云爪 🐾

**联系邮箱**：3834522034@qq.com

**版本历史**：
- v1.2.0 (2026-04-06)：新增豆包/知乎操作流程、高级技巧、实战测试记录
- v1.1.0 (2026-04-06)：新增与 agent-browser 对比、故障排查
- v1.0.0 (2026-04-06)：初始版本
