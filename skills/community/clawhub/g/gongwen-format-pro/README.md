# 党政机关公文格式标准排版 v2.2.0

严格依据《党政机关公文格式》**GB/T 9704-2012**，把草稿变成能直接发的正式公文。

一个技能覆盖三件事：**文风净化 → 国标排版 → 合规质检**。

---

## 能干什么

### ① 排版 `scripts/gongwen_format.py`

Markdown / TXT / DOCX 草稿 → 国标合规 `.docx`。

覆盖全部版式要素：份号、密级和保密期限、紧急程度、发文机关标志（红头）、发文字号、签发人、红色分隔线、标题、主送机关、正文与四级标题、附件说明、附件正文另面编排、发文机关署名、成文日期、印章版式、附注、抄送机关、印发机关和印发日期、页码。

关键参数全部按国标落地：页边距上 37 / 下 35 / 左 28 / 右 26mm，版心 156×225mm，每页 22 行每行 28 字，正文 3 号仿宋、行距固定 28 磅、首行缩进 2 字，标题 2 号小标宋居中，一级黑体 / 二级楷体 / 三四级仿宋，版记 4 号仿宋，页码 4 号宋体加一字线、单页右空一字双页左空一字。

### ② 质检 `scripts/gongwen_check.py`

对任意 `.docx` 做 6 组 30+ 项扫描，输出高 / 中 / 低三级问题清单，每条都给出「实测值 / 期望值 / 整改建议 / 定位文字」。结论只有**合规**与**不通过**两种，不搞模糊评分。

### ③ 文风净化 `scripts/style_clean.py`

139 条规则，分两档：

- **直接替换**：网络用语、口语、AI 腔、常见错别字、半角标点、emoji、Markdown 残留
- **仅标记**：赋能／闭环／抓手、我觉得、尽快、有关部门、文种混用、发文字号方括号等——这些改了可能失真，交人决定

设计原则：宁可漏改，不可错改。

---

## 快速开始

```bash
pip install python-docx

# 看效果
python scripts/gongwen_format.py --demo

# 排一份红头通知
python scripts/gongwen_format.py --config gongwen_config.demo.json --output 通知.docx

# 检查合不合规
python scripts/gongwen_check.py --input 通知.docx --report 质检报告.md

# 净化一篇脏草稿
python scripts/style_clean.py --input draft.md --output clean.md --report 文风报告.md
```

完整工作流：

```bash
python scripts/style_clean.py   --input draft.md --output clean.md --report 文风报告.md --keep-markdown
python scripts/gongwen_format.py --config my.json --input clean.md --output 正式文件.docx
python scripts/gongwen_check.py --input 正式文件.docx --report 质检报告.md
```

---

## 关于字体

国标点名的「方正小标宋简体」「仿宋_GB2312」「楷体_GB2312」在多数机器上没有预装。脚本会**探测本机实际存在的字体文件**并自动回退（小标宋 → 华文中宋 → 宋体），运行时打印实际映射，例如：

```
字体映射：标题/机关标志=宋体｜正文=仿宋｜一级=黑体｜二级=楷体｜页码/版记=宋体
```

回退只影响本机预览观感，不影响文档结构合规。付印或送审前，在装有公文字库的机器上加 `--strict-font` 重新生成即可。

---

## 目录结构

```
gongwen-format-pro/
├── SKILL.md                      技能入口（三模式路由）
├── README.md                     本文件
├── manifest.yaml                 技能元数据
├── gongwen_config.demo.json      配置模板
├── scripts/
│   ├── gongwen_format.py         国标排版引擎
│   ├── gongwen_check.py          格式质检
│   └── style_clean.py            文风净化与校对
└── references/
    ├── gb9704-2012.md            国标参数速查
    ├── qc-checklist.md           质检项清单与阈值
    ├── style-guide.md            文风词表说明
    ├── cli-reference.md          完整参数手册
    └── faq.md                   常见问题（字体/质检/文件占用/层级/PDF 等）
```

---

## v2.0.0 相比旧版改了什么

由 1.0.0 与 1.4.0 两版合并升级而来。

| 项 | 旧版问题 | v2.0.0 |
|---|---|---|
| 版记字号 | 1.4.0 误用 3 号 | 修正为 4 号仿宋 |
| 页码 | 1.4.0 默认首页不编页码（不合国标）；1.0.0 居中不分奇偶 | 默认全篇编码，单页右空一字、双页左空一字，`--no-first-page-num` 降为可选 |
| 字体 | 字体名在 Windows 上失配，显示为默认字体 | 字体回退链探测本机字体文件，打印实际映射 |
| 层级识别 | 1.0.0 无智能识别 | 合入 1.4.0 的 Markdown + 序号双通道识别 |
| 配置方式 | 两版各执一端 | JSON 配置与 CLI 参数并存，命令行优先 |
| 质检 | 无 | 新增，30+ 项三级报告 |
| 文风 | 无 | 新增，139 条规则双档处理 |

---

## v2.2.0 新增（SkillSpector 安全整改）

针对 NVIDIA SkillSpector 扫描发现的 9 项风险点逐项加固，未改变任何排版/质检/文风能力：

| 发现类别 | 风险 | 整改 |
|---|---|---|
| MCP Tool Poisoning（High） | 旧版通过调用外部办公软件进程导出 PDF | **彻底移除** PDF 导出与相关参数、外部办公软件依赖；导出需求由 Word/WPS 另存为完成 |
| Context-Inappropriate Capability | 同上，外部二进制攻击面 | 同上，脚本不再 spawn 任何外部进程 |
| Intent-Code Divergence | docstring 称「不做语义改写」却做替换 | 改为准确表述：做「表层规范化」（固定可审计规则表），不改动实质性内容，可能失真的只标记 |
| Vague Triggers ×3 | 触发词含「排版」「生成正式文件」「转成Word」等泛词 | 触发词收窄到公文专属场景；路由表与兜底表同步收窄 |
| Natural-Language Policy ×2 | 「必须使用此技能」强制语气、强制统一文风 | 改为「当用户明确要求时使用 / 适用场景需用户主动提出」；文风净化为 opt-in，实质性内容不改写 |
| Vague Triggers（兜底） | 判不准自动跑 C→A→B 全链路 | 改为先问用户确认意图，不自行跑全链路 |
| MCP Least Privilege | 能力与权限未声明 | manifest `capabilities` 显式声明（读用户文件/执行本地脚本/只读字体列表），并说明纯本地、用户主动、不读其他目录 |

PDF **文本层输入**（pypdf，本地、无外部二进制）予以保留，但已在 description 与 manifest 中**显式声明**为受支持的输入格式，消除「未披露的能力扩展」问题。

---

## v2.1.0 新增

在 v2.0.0 之上，回应实际使用中的体验与安全诉求：

| 项 | 说明 |
|---|---|
| 自然语言交互层 | SKILL.md 新增「交互铁律」「模糊输入兜底」「必须拒绝的请求」；交付用模拟执行反馈模板，无执行能力时给出 Markdown 红头预览 |
| FLAG 批量确认话术 | 文风净化发现 FLAG 项时给出「替换 / 保留」二选一话术，把决定权交回用户 |
| 自动备份 | 三脚本写文件前自动把原稿备份为 `.bak-时间戳`，防覆盖丢失 |
| 友好错误 | 文件被占用 / 无权限 / 编码错误给出可操作提示与解决方案，不再抛裸栈 |
| PDF 文本输入 | `gongwen_format.py` 与 `style_clean.py` 支持读取 `.pdf` 文本层（pypdf，需 `pip install pypdf`） |
| 内容逻辑校验 | 质检新增可机械验证的日期合法性（无效月/日）与「成文日期早于发文字号年份」检查，列为低级别 |
| 本地处理声明 | 明确纯本地运行、不联网、不上传文件，详见 FAQ |
| FAQ 文档 | 新增 `references/faq.md`，覆盖字体缺失、质检不通过、文件占用、层级错乱、PDF 等高频问题 |

---

## 边界

只管**格式与文风**，不代拟内容、不判断行文关系是否恰当、不核实事实与数据。印章默认只留位置。

**本地处理声明**：本技能为纯本地运行，不发起任何联网请求、不调用外部 API、不上传文件；所有排版、质检、净化均在用户本机完成，仅处理用户主动提供的文件，可完全离线使用。国标条款以正式发布文本为准；与本单位现行发文格式规定冲突时，以单位规定为准。

---

## 反馈与联系

使用问题、误报反馈、实务建议，欢迎通过项目仓库提交 Issue。

署名：一线评标专家&ChesaraM
