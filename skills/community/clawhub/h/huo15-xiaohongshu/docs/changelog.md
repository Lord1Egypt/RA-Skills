# 火一五小红书创作伙伴 — 版本历史

## v3.10.0（2026-05-01）— 哲学持续力 + 浏览器加固

> 调研 2026 年小红书 JA3/JA4 TLS 指纹、navigator.webdriver/cdc_ 检测、HTTP/2 settings 检测后，
> 对 v3.9 的浏览器桥接做 5 道新闸门加固；同时把哲学层延伸到「能量与持续力」和「身份认同符号系统」。

### 哲学侧（写得久，不只是写得对）

- **第六层：创作能量与持续力**（[creative_philosophy.md](../data/creative_philosophy.md)）
  - 6.1 写不出 ≠ 技法问题（能量低 > 状态僵 > 才是技法问题）
  - 6.2 没有灵感的产出策略（高峰储粮 + 中等补改 + 低谷续写）
  - 6.3 发出去的最后 10%（克服删除冲动：24h 缓冲 / 量级降级 / 关掉自我编辑）
  - 6.4 低谷-高峰循环：把它当作正常生理（3 个允许 + 输入处方）
  - 6.5 耗尽信号 3 级（早期/中期/晚期对应停损动作）
  - 6.6 续命的 3 个长期工具（创作日记 / 同行者 / 不为发布的写作）
- **第二层 2.4：身份认同符号系统** — Allen 第二课「卖身份认同」≠ 抽象
  - 5 类符号：物 / 地 / 行 / 时 / 语言节奏
  - 自检：抽象形容词 vs 具体符号
  - 红线：1-2 个真实细节 > 5 个炫耀符号；伪装 = 反向身份认同
- **philosophy.py 新命令**：`--layer 6` / `--energy` / `--identity`

### 防封号侧（v3.9 6 道 → v3.10 11 道闸门）

- **新 `health` 命令**（[browser_bridge.py](../scripts/browser_bridge.py)）：一次性透明化所有暴露面
  - CDP 连接 / 登录态 / 熔断状态 / 配额 / 节奏
  - 浏览器指纹自检：`webdriver` / `cdc_*` 标记 / `plugins.length` / `Canvas` / `chrome.runtime` / `hardwareConcurrency` / UA
  - 把检测点透明化让用户判断暴露程度（而不是黑盒声称"安全"）
- **新 `quota` 命令**：日配额可视化（进度条 + 状态分级）
- **日配额 100 次硬闸门**：对齐 SKILL.md 红线第 5 条；超限自动拒绝；按日期分文件 `~/.xiaohongshu/.daily_quota_<date>`
- **指数退避**：连续 3 次空响应 → 延迟翻倍（上限 30s），软风控信号自动降速
- **晨间缓冲 6:00-7:00**：拟人节奏，刚醒不刷热门；只允许 status/health/quota/stop
- SKILL.md 浏览器章节重写：列出 11 道闸门细节（不再笼统说"6 层"）

### 调研依据

公网搜到 2026 风控对抗共识：
- TLS 指纹（JA3/JA4）—— `requests` 被一眼识别 → 我们走真实 Chrome 完全规避
- `navigator.webdriver` —— 不传 `--enable-automation` 默认 false ✅
- `cdc_*` 标记 —— Selenium/ChromeDriver 注入，CDP 直连不会 ✅
- HTTP/2 settings frames —— Chrome 原生 ✅
- 行为序列分析 —— 拟人延迟 + 退避 + 缓冲应对

### 不做的（避免堆样子）

- ❌ 不引入 `curl_cffi` / `playwright-stealth` 等第三方反检测库（真实 Chrome 已经是顶配）
- ❌ 不动 SKILL.md description（CSO 合规已到位，v3.7.1 改过）
- ❌ 不引入新 `child_process` 调用（CLAUDE.md §6.2）
- ❌ 不复制龙虾原生功能

---

## v3.9.0（2026-05-01）— 浏览器桥接 + CDP 安全浏览

> 调研 2026 年小红书风控体系（JSVMP/x-s 2.0/TLS 指纹/行为序列分析）后，
> 确定 CDP 连接真实 Chrome 是最安全方案。实现 browser_bridge.py 并做反检测加固。

### 新增
- **browser_bridge.py**：通过 Chrome CDP 安全浏览小红书
  - `start` — 启动 CDP Chrome + 打开 XHS（扫码一次长期登录）
  - `explore` — 获取探索页实时推荐笔记
  - `search <关键词>` — 搜索笔记
  - `note <url>` — 打开单篇笔记，提取标题/正文/话题/互动
  - `analyze <url>` — 对标拆解 + Allen 6 维自动诊断
  - `status` / `stop` — 连接状态检查 / 关闭
- **反检测加固（6 层硬编码保护）**：
  1. 拟人随机延迟（2~10 秒）
  2. 熔断机制（遇 403/461/captcha/滑块 → 30 分钟禁用）
  3. 夜间休眠（0:00-6:00 禁止操作）
  4. 会话操作上限（30 次）
  5. 模拟自然滚动后提取内容
  6. 只发 Runtime.evaluate，不发 Runtime.enable/Console.enable
- **assistant.py 集成**：`assistant.py browser <action>`
- **SKILL.md 新增「浏览器桥接」章节**
- **KB 沉淀**：`~/knowledge/huo15/2026-05-01-xhs-browser-bridge-cdp-anti-crawl.md`

### 坑 & 教训

1. Chrome 136+ 不允许默认 Profile 开 CDP 端口 → `--user-data-dir` 必传独立目录
2. CDP WebSocket 需要 `--remote-allow-origins=*`
3. 沙箱阻止 localhost:9222 → 所有 CDP 操作需 `dangerouslyDisableSandbox`
4. screencapture 在非 GUI 环境不可用 → JS 提取内容代替
5. 二维码 base64 内联图片 → decode 后通过 `open` 在 Preview 显示
6. websocket-client 需 pip 安装

---

## v3.8.0（2026-05-01）— 创作热身 + 实战对照 + 工具决策指南

> 补齐「动笔前怎么进入状态」和「哲学怎么落地」两个关键缺口。

### 新增
- **warmup.py**：三步创作热身仪式（切换感官 → 找到情绪 → 对齐哲学）
  - `--quick`：只看一个画面+情绪问题，直接动笔
  - `--freewrite`：场景 → 60 秒自由书写，附带开头句降低空白页焦虑
  - 14 个情绪触发器问题（从真实生活经验中提取，不是冷知识）
  - 集成进 assistant.py 主入口
- **creative_philosophy.md 新增「第〇层：创作热身」**：进入状态的三步法 + 卡住时的自救
- **creative_philosophy.md 新增「实战对照」章节**：一篇防晒霜笔记从攻略型到范本型的完整 4 轮转变
  - 原始稿 → 心象定义读者 → AB 点重定义 → 五法改写 → Jarvis 陷阱检查
  - 含 8 维 before/after 对照表
- **SKILL.md 新增「我现在该用哪个工具？」**：按 8 种用户状态路由到对应工具
- **scene_library.md 新增「情绪锚点速查」**：8 大类目 × 情绪锚点 × 写作建议

### 设计决策

v3.7 把哲学框架搭好了，但用户打开技能后有两个实际问题没解决：
1. 「我知道这些道理，但打开编辑器大脑一片空白」→ 热身仪式解决
2. 「哲学讲得很好，但我不知道我写的到底对不对」→ before/after 实例解决

热身的设计哲学：不是加更多理论，是帮用户**切换大脑模式**——从分析切到感受。
自由书写的 60 秒规则（不停、不改、不判断）来自创造性写作的经典方法论。

---

## v3.7.1（2026-05-01）— CSO 合规 + 红线 + 借口预防

> 用 superpowers:writing-skills 方法论审视后的改进。

### 改进
- **SKILL.md description 重写**：从 workflow 总结改为 CSO 合规的触发条件描述
  - 之前：250+ 字的功能列表（违反 "Description = When to Use, NOT What the Skill Does"）
  - 现在：纯触发条件 + 搜索关键词，不含任何 workflow 描述
- **新增「红线」章节**：8 条 STOP 信号，每条对应一个已知失败模式（跳过哲学检查/不查功课/不跑教练等）
- **新增「常见错误」章节**：8 组错误 vs 正确对照（开头/引导/口吻/结尾/功课/节气/金句/比喻）
- **creative_philosophy.md 新增「常见借口」章节**：7 条借口 vs 现实对照，预防自我合理化

### 方法论

应用 superpowers:writing-skills 的 4 个核心原则：
1. **CSO**：description 只写触发条件，不总结 workflow（避免 Claude 读 description 后跳过正文）
2. **Red Flags**：让 Claude 能自检——出现这些信号 = 停，重来
3. **Rationalization Prevention**：针对已知借口预先写反例
4. **Common Mistakes**：错误/正确对照表，快速定位问题

---

## v3.7.0（2026-05-01）— 五层创作哲学入库

> 综合 Allen 三课五技法 + 东东枪 99 篇 + 算法实践，提炼为统一的创作决策框架。
> 这是本技能从「工具集合」到「创作助手」的关键一步 — 有了灵魂。

### 新增
- **创作哲学**：`data/creative_philosophy.md` — 五层决策框架（原点→支点→手艺→陷阱→系统）
  - 第一层「创作原点」：心象定义读者 / 站文案里感受 / 场景共鸣铁律
  - 第二层「创作支点」：AB 点 / 核心体验 / 先做功课
  - 第三层「创作手艺」：留白法则 / 五法 / 三大句式 / 洞察 / 创意碰撞 / 动词用法
  - 第四层「创作陷阱」：Jarvis 五维 / AI 腔四类 / 算法红线
  - 第五层「创作系统」：渐进式教练 / 多切面法则 / 功夫积累 / 场景库维护
  - 决策速查「写一篇笔记的 8 个问题」
- **philosophy.py CLI**：动笔前 30 秒速查
  - 默认：8 问 + 四句心法
  - `--checklist`：纯文本清单，可粘贴到草稿顶部
  - `--mantra`：只看四句心法
  - `--layer 1~5`：深入某一层
- **案例库扩至 9 个**（从 4 个真实案例）：
  - `allen_shangban.md` — 上班是不合理的超自然现象（金句法）
  - `allen_shuhui.md` — 薯你会买（造词三层结构）
  - `allen_jinxing.md` — 人生尽兴指南六切面（多切面法则）
  - `allen_chunfen.md` — 春分·什么也不赶（节气减法）
  - `allen_zhouwen.md` — 周三存档（栏目化设计）

### 改进
- **AI 腔黑名单增强**：新增 20+ 模式 + 新增「Jarvis 攻略型句式」类别（6 条）
- **SKILL.md 重构**：创作哲学成为技能核心章节，前置到能力表之前
- **CLAUDE.md 更新**：新增长目录结构 + 维护原则 + philosophy.py
- **case_library/README.md 更新**：完整案例索引表（9 案例 + 5 模板）

### 设计决策

这次更新的根本问题是：v3.0~v3.6 积累了大量方法论文档（Allen、东东枪、算法），
但它们分散在多个文件中，缺乏一个统一的「决策框架」让创作者在动笔前快速对齐。
五层哲学解决了这个问题 — 它是所有技法的「操作系统」，不是又加了一层理论。

---

## v3.6.1（2026-04-30）— 算法指南 + 数据资产扩充

> 基于 Web 研究补充 2025-2026 小红书算法最新趋势。

### 新增
- **算法指南**：data/algorithm_guide.md — 包含 CES 最新公式（关注×8/评论×4/转发×4/收藏×1/点赞×1）、NoteLLM 模型、冷启动机制、互动质量 2026 更新、内容质量要素（原创率 35%）、30+ 条创作策略建议
- **SKILL.md 引用**：description 更新 + 数据资产列表新增 algorithm_guide.md

## v3.6.0（2026-04-30）— Allen 旺旺教学入库 + 先做功课红线

> 旺旺雪米饼批改训练（2026-04-29）的全部经验入库。

### 新增
- **先做功课工作流**：SKILL.md 新增「先做功课（Allen 红线）」规则 — 写产品/品牌前必须先查官方定位
- **Allen 60分文案五法**：SKILL.md 新增 5 条可操作技法（感受代配料/场景代功能/情绪代产品/过程代成分/比喻代描述）
- **态度 vs 成分框架**：SKILL.md 新增品牌定位认知框架
- **旺旺雪米饼案例**：data/case_library/wangwang_xuemi.md + data/allen_method.md 案例17入库
- **Allen 文案心法第 8 条**：「在写一个产品之前，先去做功课——深度了解品牌官方定位之后再开始创意」

### 改进
- **allen_method.md** 新增旺旺教学完整章节（品牌信息/失败分析/五法自检/先做功课流程）
- **实战水位表** 待修炼新增「先做功课的习惯」

## v3.5.0（2026-04-29）— 东东枪深化 + 创作力底座扩充

> v3.5 选了 v3.4.1 末尾推荐的 **A+C** 组合：
> - **A. 东东枪深化** — AB 点贯穿创作全流程（drafts new 起 / coach-iterate 验 / weekly 看转化率）
> - **C. 创作力底座扩充** — 场景库 + 案例库 + 苏格拉底式学习

### A. 东东枪深化（AB 点全流程）

**1. drafts new 加可选 AB 点问询**
- `DraftMeta` 新加 4 字段：`ab_a_view` / `ab_a_feel` / `ab_b_view` / `ab_b_feel` + `ab_validated`
- 新建草稿时弹问 4 个问题（可跳过 / 命令行直传 / `--no-ab` 关掉）
- B 太抽象（< 5 字）时立刻提示"= 没有 B"

**2. drafts ab 子命令：查看 / 设置 / 验证**
- `drafts ab <id>` 查看当前 AB
- `drafts ab <id> --set` 重新设置
- `drafts ab <id> --validate` 让 LLM 看最新版判断 A→B 是否兑现，写回 meta

**3. coach-iterate 加第 7 维 ab_validation**
- 优先级最高：如果设了 AB 但 ab_validated 不是 True，**先 focus AB 点 3 轮**
- 给(what, why, how, example) 四件套：让用户假装 A 状态读者重读
- 6 维都过 7 + AB 验证通过 → 才算结业

**4. weekly_review 加 AB 转化率**
- 显示"X 个草稿设了 AB / Y 个已验证兑现 / 转化率 Z%"
- 长期看创作者"想清楚 vs 写到位"的能力变化

### C. 创作力底座扩充

**5. data/scene_library.md — 非节气日常画面库**
- 8 大类（家中 / 通勤 / 办公 / 季节 / 感官 / 关系 / 独处 / 消费）
- ~200 个**人人都有过**的具体画面（非冷知识）
- 解 Allen 痛点："AI 反复用同一批词（西瓜/蝉/冰棍）"

**6. scene_prompt.py — 每日场景词触发器**
- 每天抽 5 个画面，跨类目均衡
- 历史去重（用过的下次避开）
- `--category` 限定类目；`--history` 看用过哪些

**7. data/case_library/ 案例库（7 个案例文件）**
- `allen_lingqu.md` — 惊蛰·领取春日礼（动词意境）
- `jiaoxia_brand.md` — 蕉下品牌方法论
- `winter_01~05.md` — 冬日系列空模板（待用户填）
- 统一 schema：frontmatter + 原文 + 关键技法 + 苏格拉底问题 + 范本解读 + 你能学到的

**8. case_study.py — 单案例苏格拉底式学习**
- `list` / `study <id>` / `show <id>` / `related <keyword>` / `history`
- 苏格拉底模式：先你自己回答 N 个问题，再看老师答
- LLM 增强：对每个用户答案给个性化反馈
- 学习历史存 `~/.xiaohongshu/profile/case_studies.jsonl`

### assistant.py 新增子命令

`scene` / `case` 接进主入口（共 24 子命令）。

### E2E 验证

- scene_prompt 跨 5 类目抽 5 画面 ✓
- case_study list 7 案例分 3 来源 ✓
- drafts new 命令行直传 AB 点写进 meta ✓
- coach-iterate 自动 focus ab_validation 给 4 件套 ✓
- weekly_review 显示"AB 设定 1 / 验证 0 / 转化率 0%" ✓

---

## v3.4.0（2026-04-29）— 数据闭环 + 商业文案框架

> v3.4 解决两件事：
> 1. **数据闭环** — iter_sessions / practice / ab_tests / drafts 四个数据源之前没人看，现在都进了 weekly_review + annual_report
> 2. **商业文案底座** — Allen 2026-04-28 蕉下案例教学 + 东东枪《文案的基本修养》两套硬功夫沉淀进 data/ + 工具

### P0 — 数据闭环

**1. weekly_review 重写：整合 6 个数据源**
- 之前只看 posts.jsonl + snapshots.jsonl
- 现在加：iter_sessions（教练改稿轨迹）/ practice.jsonl / ab_tests.jsonl / drafts/ / feedback.jsonl
- 输出"成长曲线" — 6 维改进率 / 长期掉某维提示 / 改稿轨迹平均提升

**2. find.py — 跨数据全文搜索**
- 跨 drafts / baseline / posts / reviews / iter 5 个源
- 子串 / 正则 / 全词三种匹配
- 按"相关度 × 时间"排序

**3. evolve 增强：从 iter_sessions 自动学**
- 之前只看 feedback reject 计数
- 现在也看 iter_sessions：同一维度 focus ≥ 5 次 / 改进率 < 30% → 标记 weak_dims
- 不直接禁用，只提示"长期掉这一维"，引导用户去 practice 加强
- RuleOverride 新加 weak_dims 字段

### P1 — 用户体验

**4. wizard.py — 五步上手向导**
- 主题 → 受众 → 风格 → 上传样本 → 选预设
- LLM 增强：用户随便答（"想写护肤""我是 30 多岁的"），Claude 自动抽 niche / persona
- 智能推荐 preset（按 niche / voice 推 allen / engineer / balanced）

### P2 — 长线仪式感

**5. annual_report.py — 月/季/年度创作年鉴**
- 月度时间轴（每月起草/发布/改稿/训练）
- 高光时刻（互动 Top 5 / 最长改稿 / 最大单篇进步）
- 风格变化对比（最早 vs 最近 baseline 的 6 维分）
- LLM 温度回顾（如开 LLM）

### 新增 — 商业文案框架（来自 Allen 2026-04-28）

**6. data/copywriting_frameworks.md** — 蕉下三式 + 东东枪《文案的基本修养》核心概念
- 蕉下三大句式：「不是…而是…」/ 修辞 / 「每一…」
- 东东枪：AB 点 / 核心体验 / 洞察 / 品牌固化偏好 / Idea 金字塔 / 创意碰撞法
- Allen 启示：写每篇笔记前 5 问 + 写完 3 自检

**7. frameworks.py CLI** 4 个子命令：
- `frameworks jiaoxia --topic X --value Y` 蕉下三式生成
- `frameworks ab --topic X` 东东枪 AB 点辅助（交互式）
- `frameworks key --product X` 核心体验追问 4 问
- `frameworks spark --key X --insight Y` 创意碰撞器（核心体验 × 洞察 = Idea）

### assistant.py 新增子命令

`wizard` / `find` / `annual` / `frameworks` 全部接进主入口。

### E2E 验证

- find 跨 drafts + baseline 命中"干皮" 2 处 ✓
- evolve 从 iter_sessions 自动检测出 resonance 改进率 20%，加进 weak_dims ✓
- weekly_review 输出 6 数据源整合 + 长期掉某维警告 ✓
- annual_report 高光时刻识别"最长改稿 5 轮" ✓
- frameworks jiaoxia 给"副业 / 活成自己"3 套句式各 4 条 ✓

---

## v3.3.0（2026-04-29）— 算法对齐 + 合规硬伤补齐

> 来源：ClawHub 同类技能（xhs-content-creator / social-creator）调研 +
> 实战合规缺口诊断。这次补的不是"美学"，是"硬知识" — 你 Allen 流打 90 分，
> 没标 #AI生成内容 也照样限流。

### P0 — 合规硬伤（必须修）

**1. #AI生成内容 必标检查（自 2026/01 起强制）**
- `compliance_check.py` 新增 `check_ai_label()`
- 默认开启，未标 → 高风险（必须改）
- 纯人工创作可加 `--no-ai-label-check` 跳过

**2. CES 算法分值落地（score_post 新加 ces_design 维度）**
- 关注(8) > 转发(4) ≈ 评论(4) > 点赞(1) ≈ 收藏(1)
- 检测 3 类引导：软关注 / 评论邀请 / 求点赞
- 全靠"求赞" → 扣 2 分 + 提示改成评论邀请（4 倍权重）

**3. 标题前 13 字关键词位置（score_title 新加）**
- 小红书搜索权重 40% 在标题前 13 字
- 关键词在前 +1 / 关键词在 13 字外 -1 + 提示挪前
- 通过 `RuleOverride.main_keyword` 配置（新增字段）

**4. 发布节奏硬限（publish_helper 新加 check_publish_cadence）**
- 单日 ≤ 2 篇、间隔 ≥ 2h
- 超限弹警告 + 询问是否继续
- 数据来源 `~/.xiaohongshu/posts.jsonl`

### P1 — 加分项

**5. 3:4 HTML 封面生成（cover_brief --html）**
- 5 套配色模板：minimal / tech / warm / dark / soft
- 自动按 brief 的版式 / 配色推荐模板
- F12 切换设备工具栏 → 直接截图
- 输出到 `~/.xiaohongshu/covers/<draft-id>/`

**6. 话题 5 槽分级强制（score_hashtags 重写）**
- 大词 / 中词 / 长尾自动分类
- 全是大词 → 扣 2 分 + 建议改成 2 泛 + 2 垂 + 1 长尾
- 完全没大词 → 扣 1 分（失去基础流量池）
- 完全没长尾 → 扣 1 分（错过精准受众）

### P2 — 文档同步

**7. community_rules.md 新增"〇、最新硬性合规"章节**
- AI 标签 / 发布节奏 / CES 算法 / 标题前 13 字 4 大块
- 实战检查清单同步更新

### 关键洞察

ClawHub 上其他小红书技能都把"小红书技能"做成了**生成器**（输入主题 → 输出文案）。
我们差异化是**陪练系统**（输入主题 → 帮你练成可持续创作的人）。

但**合规和算法常识**这种"硬知识"对手做得更扎实，必须吸收。
v3.3 把"硬知识"补全 — 让 Allen 流的美学打分能跑在合规底座上。

---

## v3.2.0（2026-04-28）— 工作流闭环 + SKILL.md 瘦身

> 触发：发现 SKILL.md 超 ClawHub embedding 8192 token 上限（135% 已用），
> 后半部分内容（v3.0/v3.1 章节）被截断，搜索可发现性受损。

**结构调整：**
- SKILL.md 瘦身到 ≤ 5K 字符，留触发词 + 命令速查 + 核心定位
- 详细教程 / 典型场景 / Python API / 数据资产 / 错误对照 → `README.md`
- 完整版本历史 → `docs/changelog.md`（本文件）

**新增三个能力（解决真实工作流痛点）：**

### 1. `coach_iterate.py` — 渐进式教练

来源：Allen 给贾维斯的最终评价 *"看出问题 ≠ 写得出来"*。

`critique.py` 一次给所有 6 维反馈 = 信息过载，用户不知道先改哪。
`coach-iterate` 一次只 focus **当前最差的那一维**，给 (what, why, how, example)
四件套；用户改完跑同一命令 → 自动对比该维分数变化 → 升了给下一维 / 没升继续追问。

记录在 `~/.xiaohongshu/profile/iter_sessions/<draft-id>/` 形成"改稿轨迹"。

### 2. `drafts.py` — 草稿版本管理

之前草稿散在 /tmp/、~/Desktop/，改稿无追踪。

```bash
drafts new --topic "下班后副业"            # 创建 ~/.xiaohongshu/drafts/<id>/
drafts add <id> /path/to/content.md       # 加版本（v01, v02, v03...）
drafts list                                # 列所有草稿
drafts show <id>                           # 看最新版
drafts diff <id>                           # 对比 v_n vs v_{n-1} 的 6 维分变化
drafts promote <id>                        # 标记终稿，转给 publish_helper
```

### 3. `today.py` — 今日选题推荐

解决"打开技能不知道写什么"的空白页焦虑。
综合：
- **当前节气**（自动从 `data/seasonal_themes.md` 命中）
- **栏目化**（如果有 series 沉淀，提醒"周三存档"该更新了）
- **公式轮换**（最近一直用 T2，建议试试 T3 / T11）
- **风格档案**（按你的 niche / persona 定制）

输出 1~3 条选题 + 推荐理由 + 可执行的 `assistant.py write ...` 命令。

---

## v3.1.0（2026-04-27）— Jarvis 陷阱 + 对标拆解 + Prompt Caching

来源：Allen 2026-04-27 夜「重启尽兴」对照课 + Anthropic API 进阶能力调研
+ 主流小红书工具市场调研。

**新增第 6 个 Allen 美学维度「范本范」(jarvis_trap)：**
检测大多数 AI / 工程师写文案的 5 维系统性偏差 —
开头挖痛点 / 引导建议动作 / 我在说话 / 运营口吻 / 教做型结尾。
最核心：'教读者怎么做' vs '展示什么样的人已经在做'。

**新增 [reverse_engineer.py](../scripts/reverse_engineer.py)** — 对标爆款 URL 反向拆解：
公式 / 骨架 / 钩子 / Allen 6 维 / 关键词 / "why it works" / "你赛道怎么用"。
可一键 `--add-baseline` 进风格档案。

**新增 [llm_helper.py](../scripts/llm_helper.py)** — Anthropic SDK 统一封装：
- prompt caching（Allen 数据 5min TTL，命中后 0.1x 成本）
- streaming（critique --watch 实时反馈）
- JSON 模式（critique --rewrite 一键攻略型→范本型）
- tool use 接口预留

**新增 [cover_brief.py](../scripts/cover_brief.py)** — 封面文案 + 版式建议
（3 套方案，按赛道配色）。

**critique.py** 新增 `--rewrite`（LLM 改写）+ `--watch`（流式分析）。

**practice.py** 新增 `rewrite-jarvis` — 用 Allen 5 维差距训练改写思路。

---

## v3.0.0（2026-04-27）— Allen 流升级（哲学家视角）

来源：司志远（Allen）2026-04-23~27 三课 + 五技法 + 11 案例教学。

v2.5 给的是工程师视角（钩子/排版/合规），v3.0 加上 Allen 美学叠加。

**新增 5 个 Allen 美学维度（[xhs_aesthetic.py](../scripts/xhs_aesthetic.py)）：**
- breath 留白度
- ai_speak 去 AI 腔
- teach_vs_lead 带读者
- resonance 共鸣度
- invitation 邀请语

**新增 4 个 CLI：**
- `critique.py` — Allen 风格诊断
- `coin_word.py` — 造词工具（谐音/概念迁移/形式包装）
- `series_design.py` — 栏目化 + 5 级互动阶梯 + 12 月节奏
- `reader_simulate.py` — 6 种读者画像走全文

**新增 3 份数据资产：**
- `data/allen_method.md` — 三课五技法 + 11 案例 + 认知转变表
- `data/ai_speak_patterns.json` — AI 腔黑名单 80+ 条
- `data/seasonal_themes.md` — 24 节气 + 节日"已存在画面"清单

**新增风格预设（profile_init.py preset）：**
- `allen` — 工程 50% + Allen 50%（品牌/情感共鸣赛道）
- `engineer` — 纯工程（干货/教程/工具）
- `balanced` — 工程 70% + Allen 30%（默认）

`coach.py` 整合 Allen 维度，对低于 7 分的维度自动产出 (what, why, how, example)。

---

## v2.5.x（2026-04-27）— 从"工具堆"升级为"创作助手"

**三个跃迁：**

### 1. 从无记忆 → 有档案

新增 `~/.xiaohongshu/profile/`（用户私有，跨 skill 可共用）：
- `style.json` — 自动从 baseline 学习语调/长度/emoji/口头禅
- `rules.json` — 用户教过的助手记住
- `feedback.jsonl` — 用户对每条建议的反馈
- `baseline/` — 1~5 篇代表作样本

### 2. 从单点工具 → 对话入口

新增 `assistant.py` — 一个入口把所有能力串起来：
status / next / init / write / coach / publish / review / learn / evolve。

### 3. 从静态规则 → 学习演进

`learn` 教规则、`evolve` 自动演进、`feedback.jsonl` 跟踪。

**新增 9 个文件：**
xhs_profile / xhs_coach / profile_init / coach / brainstorm / weekly_review /
assistant / practice / ab_test。

---

## v2.0.x（2026-04-27）— 全流程创作能力大改版

新增 7 个 CLI：选题 / 创作 / 打分 / 合规 / 发布辅助 / 跟踪。
新增 6 份数据资产：标题公式 / 正文骨架 / emoji / 话题 / 社区规则 / 敏感词。

---

## v1.0.x（2026-04-23）— 抓取 + 分析能力首版

Cookie 抓取 + 离线分析（互动 / 关键词 / 时段 / 爆款特征）。
强节流 + 风控检测（460 / 461 / 403 / captcha / redirect-to-login）。

---

## 设计哲学

1. **个人号 / 小团队**为目标用户，不是 MCN 批量号工厂
2. **规则可解释** — 标题公式、骨架、打分项明文写在 data/，Claude 和你都能读
3. **不依赖大模型** — 所有脚本零 API 成本可跑；让 Claude 调用产物
4. **半自动 ≠ 全自动** — 发布按钮永远在人手里，账号才安全
5. **闭环优于单点** — 调研 / 写 / 发 / 复盘任何一环少了，都做不长
6. **协同创作不是 AI 替写** — 助手让你看见 AI 腔 / 教读者腔 / 攻略型陷阱，
   然后你自己重写。从 48 → 80 分的差距是真实的写作能力提升空间。
