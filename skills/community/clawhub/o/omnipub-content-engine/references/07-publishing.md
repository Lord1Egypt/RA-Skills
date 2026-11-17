# 阶段7 · 双平台发布

目标：公众号（草稿箱预览确认）+ 头条（发布）双平台落地，记录完整发布日志。

## 7.1 公众号发布

1. 终稿确认：**终稿必须按微信渲染器白名单来写，或者在推送前用 v9 清洗管线过滤**（见下文）。不要直接推网页设计稿（flex/grid/class/渐变/阴影/圆角/em）。
2. 推送到公众号草稿箱：

   - ⚠️ **教训（2026-08-14 实测）**：用 wenyan-cli 推 Markdown 会被 lapis 等内置主题重新渲染，设计稿的卡片化版式全部丢失。**不要用 wenyan 推设计稿类文章**。
   - ✅✅✅ **最终定稿（2026-08-15 实测）**：**通道不是 draft/add API 的问题，而是微信渲染器有硬 CSS 白名单**。
     - **关键取证**：2026-08-10 那篇 1:1 成功的心理机构 v9，用的也是 `/cgi-bin/draft/add` 直推。它和我这次的通道完全相同。
     - **真因**：v9 脚本在推送前对 HTML 做了一套「CSS 白名单清洗」（`UNSAFE_PROPS`），把 `border-radius`、`box-shadow`、`linear-gradient`/`background-image`、`letter-spacing`、`em`、`opacity`、`text-shadow`、`flex/grid` 等属性**全部剥掉或替换**后，才调 draft/add。微信存储时不报错（所以 draft/get 回读 0 差异），但**渲染器遇到这些属性直接忽略**——这就是「存储无损但显示不一致」的本质。
     - **本次错误链**：v2/v3 保留了 62 处 border-radius、17 处 box-shadow、10 处 gradient、21 处 letter-spacing → 本地浏览器全渲染，微信端全忽略 → 用户看到差异；v4 急着想复刻 v9，但只模仿了「纯平」外观、没使用它的清洗管线，结构和间距写得粗糙 → 更乱。
     - **正确做法（v6 定稿结构，已验证）**：
       - 若有网页设计稿：先用 `premailer` 内联 CSS → 去掉 `<style>`/class → 用 v9 白名单过滤（或复用 `outputs/make_v5_whitelist.py`）→ **再套用 v9 卡片式结构**（封面横幅 + 章节白卡片 + 卡片头 h2）→ 本地浏览器预览 = 微信端效果 → 用 draft/add 推送。
       - 若直接写原生稿：避开 `border-radius`、`box-shadow`、`linear-gradient`、`letter-spacing`、`em`、`rgba`、`opacity`、`text-shadow`、`flex/grid`、class、`<style>` 块。可用 `background-color` 色块、`border` 线条、`border-left` 彩条、`display:inline-block` 编号、`border-collapse:separate` 表格来组织层次。
       - **封面紫横幅**（v9 已验证）：`background-color:#534AB7;color:#fff;padding:48px 24px 40px;text-align:center`，标题用 h1，副标题用浅色 `#E0D9FF`
       - **章节白卡片**：`<div style="background-color:#FFF;margin-bottom:24px">` + 卡片头 `<div style="padding:18px 20px;border-bottom:1px solid #E0E0EB"><h2 style="font-size:19px;color:#534AB7">...` + 内容区 `<div style="padding:22px 20px">`
       - 章节编号可用 `<span style="display:inline-block;width:30px;height:30px;line-height:30px;text-align:center;background-color:#639922;color:#fff;font-size:14px;font-weight:800;vertical-align:middle">01</span>`（方块即可，不要 border-radius/渐变）
       - 数据卡/对比卡用 `<table style="width:100%;border-collapse:separate;border-spacing:4px">` + `<td style="background-color:#F0F0FF;padding:16px;text-align:center;vertical-align:top">`
       - 引用框用 `border-left:4px solid #534AB7;background-color:#F3F0FF;padding:14px 18px;margin:14px 0`
       - 正文 p 用 `font-size:15px;line-height:1.8;color:#333`（不要用 letter-spacing）
       - **图片不要重复标题**：如果信息图本身已包含标题文字，正文里不要再写一遍标题，只保留数据来源说明即可
     - **参考模板**：`outputs/公众号-native-v6.html`（2026-08-15 GEO 文卡片式终版，套用 v9 已验证结构，回读 227 标签 0 差异，border-radius/box-shadow/gradient/letter-spacing/opacity 全部为 0）
     - **清洗脚本**：`outputs/make_v5_whitelist.py`（可复制复用，核心规则来自 `2026-08-10-21-27-09/2026-08-10_心理机构赛道/push_to_wechat_v9.py`）
   - 🔍 **样式不一致诊断流程（先诊断再动手）**：
     1. 用 `draft/get` 回读远端草稿，与本地 HTML 逐标签比对 style 属性，先确认存储是否一致。
     2. **若存储一致但视觉不同**：不是通道问题，是微信渲染器白名单限制。把本地 HTML 用 v9 白名单清洗后，本地浏览器预览就会等于微信端效果。
     3. **若存储不一致**：检查 `Content-Type: application/json; charset=utf-8` 请求头是否缺失（会导致乱码/属性丢失）。
   - ⚠️ 若终稿已按网页标准写完（flex/grid/class/渐变/阴影），用 `scripts/wechat_compat.py` 转 table 版只能救急，且**仍有 border-radius/shadow/gradient 被忽略**，视觉上不可能 1:1。
   - 推送脚本 `wechat_publish_design.py`：draft/add 接口直接建草稿（content=清洗后的 HTML、thumb_media_id=封面、author、digest），创建成功后 draft/delete 删旧草稿；凭证存于 `C:/Users/miko/AppData/Roaming/wenyan-md/credential.json`
   - ⚠️⚠️ **编码坑（2026-08-14 实测踩过）**：
     - `draft/add` 请求**必须显式带 `headers={"Content-Type": "application/json; charset=utf-8"}`**。`requests` 的 `data` 传 bytes 时不会自动设置 Content-Type，微信服务器按错误编码解析 → 整篇（标题+正文）存储为乱码，后台显示 `ä½ çæ£è...`。
     - `draft/get` 响应 `Content-Type: text/plain` 无 charset，`requests.json()` 会按 ISO-8859-1 解码 → **即使存储正常也会显示假乱码**。验证时必须用 `resp.content.decode('utf-8')` 再 `json.loads`，不要用 `resp.json()` 判断中文。
     - 微信会把 `<img src>` 转成 `<img data-src>`（懒加载）、URL 加 `/640` 尺寸参数，属正常处理，后台预览图片仍正常显示。
   - 备选：`wewrite` 全流程（含封面图生成）、`md2wechat`
3. 用户打开草稿箱人工预览，确认：
   - 文末二维码/模板渲染正确
   - 图片无裂图、尺寸正确
   - 配色/排版符合所选主题（设计稿直推方案下应一致）
   - 无禁用词、无错别字
4. 确认后由用户手动点发布（公众号不允许第三方直接发布，且人工发布是风控安全线）

## 7.2 头条发布

用 `toutiao-publisher`（playwright-cli 方案，headed 模式自动登录创作者平台）：

1. 头条版标题（3 选 1，用户确认）
2. 封面：优先用阶段4生成的 900×600 封面图；AI 生成图需标注
3. 正文：头条版 markdown → 平台编辑器（注意空行、小标题、图片 alt）
4. 发布设置：首发声明、话题标签（1-3 个，选热度相关）、定时可选
5. 头条可直接由工具完成发布，但**发布后仍需用户后台复核**是否进入推荐池

## 7.3 发布日志（供阶段8复盘对照）

```
07-发布日志.md
平台 | 标题 | 链接 | 发布时间 | 选题评分卡得分(H/C/T/F/D) | 风格主题 | GEO评分 | 备注
公众号 | XXX | url | 2026-08-14 20:00 | 90 | healthcare | 通过 | 定时20:00
头条   | XXX | url | 2026-08-14 20:10 | 90 | healthcare | 通过 | 首发声明
```

**评分卡得分必须记录**——阶段8 复盘时用它判断「好选题是否被好执行辜负了」。

## 7.4 发布节奏建议

- 公众号：周更 2-3 篇，固定时段（如 20:00-21:00 阅读高峰）
- 头条：与公众号同步或提前 1 天（头条时效性更强，热点稿优先头条）
- 同主题系列文：间隔不超过 7 天，保持知识簇连续（利于 GEO 和粉丝预期）

## 7.5 风控红线

- 不批量注册/批量发布（防判定营销号）
- 不诱导互动（「转发抽奖」「点赞过X更新」类属违规）
- 不搬运洗稿；原创声明按平台规则
- 文中商品/课程推荐不超过全文 10%，且如实描述

---

## 7.6 实战经验补充（2026-08-14 至 2026-08-21）

### 糖尿病 / 阿尔茨海默赛道推送实战

#### 公众号完整报告推送的特殊处理

1.2 万字 HTML 完整报告不能直接推，需要分步转换：

1. **HTML → Markdown 转换**：写 `convert_report_to_md.py` 解析 HTML 报告
   - Chart.js 图表 → matplotlib 重绘为静态 PNG（微信不支持 Chart.js 动态渲染）
   - `<0.1%` 裸尖括号必须转义为 `&lt;0.1%`
   - 清理重复 emoji（💡📌）
   - 九力标签提取错误修复
   - 表格 / 引用 / 时间线结构转换
2. **图片重传**：完整报告含 6-7 张图表，每次推送必须重新上传（mmbiz 旧链接失效）
3. **封面**：封面图大于等于 900×500，PNG 格式，否则报 40007

**已验证脚本**：`convert_report_to_md.py` + 6 张 matplotlib 静态图 → WeWrite CLI 推送成功。

#### 头条号图片上传的坑与修复

**问题**：批量上传 6 张图时，部分占位符显示"编辑 | 搜图"，图片未插入。

**根因**：
- 占位符顺序与文件映射不匹配（配图1→配图3→配图2 导致图片错位）
- ProseMirror 编辑器中占位符文本被拆分或隐藏
- 某些占位符段落根本不存在（HTML 转换时丢失）

**修复工具链**（已集成到 toutiao_publish.py v2）：
- `check_missing.js`：检测哪些 `pgc-img` 占位符未被替换
- `check_cover.js`：检查顶部封面图是否已设置
- `insert_fallback.js`：按关键词搜索标题/段落，将漏掉的图片插入到固定位置
- `batch_upload.js`：严格按正文中出现顺序匹配占位符，带 NOT-FOUND 日志

**关键教训**：
- 占位符必须按正文中出现顺序严格对应文件列表
- 标题长度 2-30 字（超出会被截断或拒绝）
- 必须先关闭 AI 助手弹窗再填标题（会遮挡输入框）
- 发布必须点两次：先"预览并发布"，再"确认发布"
- 长文（1万+字）可正常推送，无字数限制

#### 推送脚本 v2 更新说明

| 脚本 | 新增能力 |
|------|---------|
| `toutiao_publish.py` v2 | 生成完整脚本套件（inject + batch_upload + check_cover + check_missing + insert_fallback），Markdown 转 HTML 用 `markdown` 库，标题 30 字验证，图片按出现顺序严格映射 |
| `wechat_publish.py` v2 | 新增 `verify_draft`（draft/get 回读，必须用 `resp.content.decode('utf-8')`），`push_loop`（IP 白名单自动重试 30 次），`detect_mmbiz_images`（检测旧 mmbiz 链接），`republish_with_images`（删旧稿重建） |
| `cli.py` | 新增 `--verify`（推送后自动 draft/get 验证），`--force-upload`（强制重新上传所有图片，含 mmbiz 旧链接），`--retry`（IP 白名单自动重试） |

#### 效率提升建议

- 头条号推送耗时的主要环节：扫码登录（~2min）、图片批量上传（~2min/6张）、人工确认发布（~1min）
- 公众号推送耗时：IP 白名单获取（0-5min，用 `--retry` 可自动解决）、图片上传（~1min）、draft/add（~5s）
- 建议：推送前先用 `--verify` 跑一次，确认样式安全属性全为 0 再正式推送，避免反复修改浪费积分
