<p align="center">
  <img alt="mu-humanizer-minesweeping" src="assets/default-banner.png" width="100%">
</p>

# ✍️ mu-humanizer-minesweeping · 写作AI味消除与禁忌扫雷仪

> 面向事实保真的写作 AI 味消除与书面风险扫描：让文字更自然，但不补造细节；发现表达风险，但不把敏感内容变成自动替换。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-humanizer-minesweeping/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill集合-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-humanizer-minesweeping)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-humanizer-minesweeping)](https://github.com/muippt/mu-humanizer-minesweeping/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-humanizer-minesweeping)](https://github.com/muippt/mu-humanizer-minesweeping/stargazers)

---

### 💡 使用场景示例

- 📣 **润色对外公告**：压缩空话、调整句式，同时保留数字、主体、范围与不确定性表达。
- 📊 **修改汇报材料**：识别模板化连接、重复表述和无信息收束，让结论更直接。
- 📢 **检查品牌与公共传播文案**：提示无依据绝对化、夸大承诺、身份标签化等表达风险。
- 🧯 **复核高敏感内容**：涉及法律案件、未成年人、民族宗教、主权或国际关系时，只提示人工复核。
- 🌐 **处理中英混排文本**：按句或段调用对应的表达模式库，并共享事实锚点。
- 🔒 **维护本地写作偏好**：将公司、团队与个人规则保留在本地，不进入公开仓库。

---

### ✨ 核心亮点

#### 🧭 证据守恒改写

改写只允许删除、压缩、重排或换句式，且只能使用原文已有信息。不会为了让文字“更像人”而补造数字、机构、人名、时间、案例、引语或因果关系。

#### 🔍 独立保真审计

改写完成后，审计阶段只读取原文、改写稿与锚点清单，独立核对实体、数字、时间、因果、极性、范围与限定词。发现漂移即回退原文。

#### 🛑 NO-OP 防护

仅改标点、空格、格式，或没有明确收益的同义替换，都会被判定为 `NO-OP`：不计为已处理，回退并列入未处理信号。

#### 🧩 四道编辑门

每处候选改写都要经过编辑资格、证据锚点、最小编辑和人类可复核四道门。输出包含逐处 diff、编辑收益、锚点来源和审计结果。

#### 💣 原创风险映射

书面禁忌扫雷采用原创的分级风险映射框架，参考公开写作建议但不转载、复刻或替代来源原文。高敏感命中一律 `review_only`，不提供定向替换。

#### 🔒 私有规则隔离

公司、团队和个人规则位于本地 `rules/` 目录，默认由 `.gitignore` 排除；公开版本不会携带任何组织或个人偏好。

---

### 📌 与同类工具对比

| 维度 | 🧭 本项目 | 常规润色 | 词库式替换 |
|---|---|---|---|
| 事实、数字与限定词 | 先抽取锚点，再独立审计 | 依赖执行者自查 | 通常不校验 |
| 无效改写 | 识别 `NO-OP` 并回退 | 可能被计入处理量 | 容易产生机械替换 |
| 高敏感表达 | 只提示人工复核 | 处理方式不固定 | 可能给出不合适替换 |
| 风险规则来源 | 原创映射，不转载来源文本 | 通常无规则说明 | 依赖词表 |
| 本地偏好 | 可选且与公开包隔离 | 不固定 | 不固定 |

---

### 🚀 工作流

| 工作流 | 适用场景 | 触发方式 |
|---|---|---|
| 完整编辑 | 需要润色、去 AI 味并完成扫雷 | 提供文本并要求“润色”“去 AI 味”或“改写” |
| 仅扫雷 | 不改写，只检查书面表达风险 | 明确要求“仅扫雷” |
| 私有规则管理 | 新增、查看、修改、停用或删除本地规则 | 使用明确的规则管理指令 |

完整编辑依次完成场景锚定、风格校准、证据守恒改写、独立含义保真审计和书面禁忌扫雷。短文本仍按规则出现次数判断，只在规则指定时不输出密度指标。

---

### ⚙️ 技术规格

| 项目 | 说明 |
|---|---|
| 类型 | 提示词与参考规则 Skill |
| 依赖 | 无 |
| 兼容环境 | 支持加载 `SKILL.md` 与本地参考规则的 AI Agent 环境 |
| 包体积 | 约 1.5 MB，含 README 横幅资源 |
| 文件结构 | `SKILL.md`、`references/`、本地 `rules/` 与公开文档 |
| 输入支持 | 自然语言文本，支持中文、英文与中英混排 |
| 输出格式 | 逐处 diff、编辑收益、锚点来源、审计结果和未处理信号 |
| 语言 | 中英文编辑；中文书面风险映射 |
| 版本 | 6.7.0 |
| 许可证 | MIT |

---

### 🛠️ 快速开始

**1. 安装** — 克隆到你的 Skill 目录

```bash
git clone https://github.com/muippt/mu-humanizer-minesweeping.git ~/.claude/skills/mu-humanizer-minesweeping
```

> 使用其他 Agent？将整个目录放到该工具约定的 Skill 加载位置即可；也可以在项目内使用 `.claude/skills/mu-humanizer-minesweeping`。

**2. 验证** — 重启或重新加载 Agent，确认它已被识别

```text
列出我当前可用的 Skills
```

**3. 使用** — 贴入一段文字，直接说明你要达到的效果

```text
请把下面这段公告润色得更自然，消除空话和模板化表达。
保留全部事实、数字、范围和限定词；高敏感表达只列为人工复核项。
```

也可以直接进入指定工作流：

```text
仅扫雷下面这段文字，不要改写正文。
```

```text
为我新增一条本地写作偏好规则，不要写入公开版本。
```

---

### 🔒 安全与隐私

- 作为本地提示词与参考规则 Skill 运行，不发起网络请求，也不收集遥测。
- 不包含凭据，不直接回写源文件。
- 私有规则仅保留在本地，默认排除出版本控制和公开发布包。
- 不判断文本作者身份，也不提供任何 AI 检测规避建议。

---

### ⭐ Star 趋势

这是首次公开发布，待仓库积累真实公开数据后再展示 Star 趋势图。

> 如果这个 Skill 对你有帮助，欢迎[点亮 GitHub Star](https://github.com/muippt/mu-humanizer-minesweeping/stargazers)，让更多写作者发现“事实优先”的编辑方式。

---

### 👤 作者简介

🎓 清华大学出版社签约作家 / 2026当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

---

### 📄 许可证与致谢

[MIT](LICENSE) © 2026 muippt

规则来源与参考说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。欢迎通过 [CONTRIBUTING.md](CONTRIBUTING.md) 和 GitHub Issues 提交贡献、修正建议与安全反馈。

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 issue。
