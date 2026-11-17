# md-out-of-chat

**把 Markdown 从聊天里拿出来，变成人能直接看的东西。**

AI 助手活在聊天里（微信、飞书、Slack、Discord……），最爱写 `.md`。但这些 app 都不好好渲染 `.md`：代码错位、表格对不齐、链接像死的。

这个小工具 = 桥：
- **`.md` → 手机能直接看的本地 HTML**
- **`.md` → 一张能直接转发的手机长图 PNG**（v1.8.0）
- 代码块带语言标签 + 一键复制
- 表格自适应（手机横屏不爆）
- 默认本地运行，公开链接必须用户明确请求

## 触发条件

只在用户明确提到 skill 名字，或清楚表达"把这份 md 转成手机可看的 HTML"时才激活。不要仅凭 "转一下" 这种模糊短语触发。

## 为什么用

- 你在 IM 跟 AI 聊，AI 给你写了一份 `.md`
- 你想看 = **手机打不开 / 看不清**
- = **用 md-out-of-chat 转换** → 生成手机可看的版本

## 怎么用

告诉你的 AI 助手："**用 md-out-of-chat 转换这份 md**" 或 "**把这份 md 转成手机能看的 HTML**"。

skill 默认输出本地 HTML；长图 PNG 用 `--long-image` 或「出长图」触发；公开链接只在用户明确要求、明确确认且有部署工具时生成。

| 场景 | 输出 |
|------|------|
| 没有特别说明 | 本地 HTML |
| 明确说"出长图 / 手机长图 / 转成长图" | 长图 PNG（750px @2x）+ 兜底长图版 HTML |
| 明确说"公开链接/URL"、确认部署且有部署工具 | web 链接 |

### 长图导出（v1.8.0）

聊完的东西想直接转给朋友？一张长图比一段文本好用：微信里发图即读、排版不散、相册能存。

```bash
python3 md2share.py note.md --long-image           # 长图 PNG + 兜底 HTML
python3 md2share.py note.md --long-image=640       # 自定义宽度（480–1600）
python3 md2share.py ~/notes --since=today --long-image   # 批量长图
```

- **零安装**：用本机已有的 Chrome / Chromium / Edge 无头截图（只找、绝不下载安装）；没有浏览器就只出长图版 HTML，自己在浏览器里整页截图也行
- **为图重排**：固定 750px 宽、字号加大、表格和代码改为折行（图片里滚动区等于被裁掉）、目录/主题切换/复制按钮全部隐藏（截图里是死的假 UI）、外链把网址印在文字后面（图片里的链接点不动）
- **出图前隐私自检**：自动扫手机号 / 身份证 / 邮箱 / 疑似密钥 / 长卡号，只报类别和数量（不打印原文，日志本身不泄露）；命中时提醒你确认再转发
- **无水印**：页脚只有文档标题和生成时间，没有 logo、没有来源标记
- 超过 20000px 的超长文档会被截断，建议拆分后分段出图

### 批量导出（v1.6.0）

离开电脑，想一次把**今天做的东西**全变成手机能看的？指定一个文件夹就行：

> "用 md-out-of-chat 导出今天，文件夹 `~/notes`"
> "用 md-out-of-chat 导出本周 `~/projects/diary`"

```bash
python3 md2share.py ~/notes                # 该目录下所有 .md（只扫一层）
python3 md2share.py ~/notes --since=today  # 只转今天改过的
python3 md2share.py ~/notes --since=week   # 本周（周一 00:00 起）／7d ／2026-09-20
python3 md2share.py ~/notes ~/readable     # 输出集中到另一个目录
```

- **无状态**：时间过滤直接读文件自身修改时间，不生成索引/清单/跟踪文件
- **只扫一层**：不递归子目录；**源 `.md` 严格只读**，只新增/覆盖 `.html`
- **手动触发**：本 skill 不注册定时任务；"每天自动跑"属于宿主平台自动化，由你自己配
- **必须你指定文件夹**：不会自己猜目录

## 安装

这是标准 skill，**把文件夹放到 agent 的 skills 目录**就行：

| Agent | Skills 目录 |
|-------|------------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| 其他 | 任意 agent 监听的 skills/ 目录 |

```
cp -r md-out-of-chat ~/.claude/skills/
```

agent 会自动识别。

## 文件说明

- `SKILL.md` — 英文 spec（agent 读这个）
- `SKILL.zh.md` — 中文 spec（你读这个）
- `md2share.py` — 核心脚本：md → 本地 HTML / 长图 PNG（单文件 或 单层目录批量）
- `build_and_deploy.sh` — 本地构建辅助（只生成 dist/，不上传）
- `demo.md` — 测试用的小例子
- `README.md` — GitHub 首页展示用

## 隐私

- **默认本地跑** — 核心脚本只生成 `.html` / `.png` 文件，**数据不出你电脑**
- 长图模式的截图用**一次性 user-data-dir** 跑无头浏览器，只加载本地生成的文件（`file://`），跑完即删，**绝不碰你已登录的 Chrome 配置**
- 隐私自检只报「类别 + 数量」，不打印命中的原文
- 公开链接**只在用户明确要求、明确确认、且 assistant 有可信部署工具时**才生成；`build_and_deploy.sh` 默认不跑
- 本地图片（`![alt](./image.png)`）只有和 `.md` 同目录或其子目录下的才会内嵌为 base64；**绝对路径和 `../` 遍历一律不内嵌**；内嵌前按文件头（magic bytes）校验真实类型，且每个内嵌路径都打到 stderr 供审计
- 远程图片不会自动下载，只会渲染成链接占位
- **无任何统计上报**

## License

MIT
