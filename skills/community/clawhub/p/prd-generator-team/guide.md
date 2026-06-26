# PRD生成器 Skill — 使用指南（团队版）

> **适用角色**：产品经理 / 高级PM / 助理PM / 产品总监  
> **版本**：V4.0 团队版 | **更新**：2026-03-09

---

## 0. 前置配置（首次使用需完成）

### iWiki 发布功能配置（可选）

本 Skill 已内置 iWiki MCP 客户端脚本，**无需额外安装 iwiki-doc Skill 或配置 MCP 连接**。

如需使用「发布到iWiki」功能，每位成员只需完成以下一次性配置：

1. 登录 [太湖个人令牌](https://tai.it.woa.com/user/pat)，创建 API Token（选择「iWiki官方MCP」权限）
2. 配置环境变量：
   ```bash
   echo 'export TAI_PAT_TOKEN="你的token"' >> ~/.bashrc && source ~/.bashrc
   ```
3. 验证：`echo $TAI_PAT_TOKEN`，非空即可

> 💡 不配置 token 不影响 PRD 生成和原型预览功能，仅影响 iWiki 发布。首次使用时 Skill 会自动检测环境并引导配置。

---

## 1. 快速开始（3分钟上手）

### 安装

```bash
# 方式A：从 Knot 平台下载安装（推荐）
# 下载 prd-generator-team.zip → 解压到 ~/.codebuddy/skills/

# 方式B：团队共享目录
cp -r /shared/skills/prd-generator-team ~/.codebuddy/skills/

# 激活：CodeBuddy → 设置 → Skills管理 → 导入本地Skill → 选择目录 → 安装
# 验证：Chat中输入 PRD生成 你好  → 正常响应即成功 ✅
```

> 安装后目录结构应为：
> ```
> prd-generator-team/
> ├── SKILL.md
> ├── guide.md
> ├── scripts/
> │   ├── connect_mcp.py         ← iWiki MCP 客户端（内置）
> │   ├── gen_flowmap.py         ← 页面流程图生成器（V3.6新增）
> │   └── publish_to_iwiki.py    ← iWiki 一键发布脚本（V3.5新增）
> └── templates/
>     ├── prd-template.md
>     └── prototype-style.css
> ```

### 初始化知识库（推荐）

```bash
mkdir -p {WORKSPACE}/.codebuddy/docs/biz-knowledge/{prd,business-rules,meeting-notes}
# 将已有PRD/业务文档拷贝到对应目录，知识库越丰富生成质量越高
```

### 30秒极速体验

```
PRD生成 做一个签到打卡小程序，用户每天签到获积分兑礼品，目标是提升日活
```

等待确认单 → 回复"确认" → 等待生成 → 完成！

---

## 2. 五种指令

| 指令 | 适用场景 | 示例 |
|------|----------|------|
| `PRD生成 {描述}` | 新项目/有明确想法 | `PRD生成 做一个答题小游戏，微信小程序` |
| `PRD生成 --draft {描述}` | 复杂项目先确认方向 | `PRD生成 --draft 企业CRM系统` |
| `PRD生成 --module {模块} {描述}` | 只需某个模块 | `PRD生成 --module 积分系统 答题获积分` |
| `PRD生成 基于 {文件}` | 会议纪要/已有文档 | `PRD生成 基于 /docs/meeting/纪要.md 生成PRD` |
| `PRD修改 {项目} {指令}` | 修改已有PRD | `PRD修改 quiz-game 补充积分过期规则` |
| `改PRD` / `修改PRD` / `调整PRD` / `更新PRD` | 自然语言修改（V3.9新增） | `改PRD quiz-game 积分上限改为5000` |

**选择建议**：新项目→`PRD生成` | 复杂项目→`--draft`先确认 | 开完会→引用纪要 | 微调→`PRD修改` 或直接说 `改PRD`/`修改PRD`

---

## 3. 完整流程示例

### 示例1：从一句话到完整PRD（最常用）

**① 输入需求**
```
你：PRD生成 做一个答题闯关小游戏，微信小程序，
    用户通过答题获取积分兑换优惠券，
    目标是提升用户活跃度和商业化转化。
```

**② AI输出确认单**（直接输出为 Markdown 文本，非代码块）

📋 需求理解确认单（第1轮）

1️⃣ 产品：✅ 答题闯关小游戏 / 微信小程序

2️⃣ 背景：✅ 提升用户活跃度和商业化转化

3️⃣ 目标用户：✅ 18-35岁移动端用户...

4️⃣ 核心功能范围：✅ P0: 答题闯关 / 积分系统...

5️⃣ 业务规则：✅ ...

6️⃣ 成功指标：✅ 日活提升20%...

7️⃣ 业务上下文：✅ 全新项目

8️⃣ 优先级建议：✅ V1.0 核心闭环

💡 **对的不用管，不对的告诉我。回复"确认"开始生成。**

**③ 确认并等待生成（~70秒）**
```
你：确认

PRD Skill：🚀 生成中...
├── ✅ Step 1/6 需求确认完成
├── ✅ Step 2/6 知识库检索（条件触发）
├── ✅ Step 3/6 PRD内容生成 → CHECKPOINT通过
├── ✅ Step 4/6 HTML原型生成 + 截图回填PRD → CHECKPOINT通过
├── ✅ Step 5/6 质量自检完成（34条规则）
└── ✅ Step 6/6 iWiki发布（按需）

✅ 生成完成！
📁 quiz-challenge-prd.md + prototype/
📊 质量评分：92/100（优秀）
```

**④ 发布到iWiki**
```
你：上传到iWiki，父页面ID：4017400280

PRD Skill：
├── ✅ Step 6 CHECKPOINT通过（zip内容合规）
└── ✅ 已发布到iWiki！
📄 页面：https://iwiki.woa.com/p/{page_id}
```

**⑤ 需要修改？**
```
你：PRD修改 quiz-challenge 补充积分上限规则

PRD Skill：已更新模块 + 同步更新原型。是否重新上传iWiki？
```

---

## 4. V3.1 新特性

### 4.1 三道防线质量保障体系

V3.1 最核心的升级是引入了**三道防线**，确保任何人使用 Skill 都能产出一致质量的文档：

| 防线 | 机制 | 解决的问题 |
|------|------|-----------|
| **第一道：模板即规范** | 模板中预置截图占位符 `SCREENSHOT_PLACEHOLDER`，AI指引改为 `AI_INSTRUCTION` 注释 | 截图遗漏、标题含模板标注 |
| **第二道：步骤内嵌CHECKPOINT** | Step 3/4/6 各有强制检查点，全部通过才能进入下一步 | 步骤间遗漏、执行偏差 |
| **第三道：增强QA检查（34条）** | 新增S-006~S-011共6条Error级检查项，与规则一一对齐 | QA漏检、虚假高分 |

### 4.2 时序图 + 流程图双视图

2.2 核心业务流程图现在要求同时包含：
- **sequenceDiagram**：展示多角色调用链（用户/前端/后端/外部系统）
- **flowchart**：展示用户端到端业务路径

### 4.3 截图嵌入对应模块 + 禁止文本线框图

页面截图不再集中放到附录，而是嵌入到每个模块的"页面交互说明"中，紧跟在"关联原型"之后。

**V3.2 新增硬规则**：页面交互说明中**禁止使用文本线框图/ASCII art**，页面展示必须且只能使用Demo页面截图（Step 5自动回填）。模板中已删除文本线框图模板，CHECKPOINT和QA规则均会检查是否有线框图残留。

### 4.4 iWiki一键发布

生成完成后可直接上传到iWiki，支持：
- **首次发布**：指定父页面ID创建新页面
- **更新发布**：cover=true覆盖已有页面
- **图片自动打包**：md+screenshots自动打包为zip上传，iWiki中图片正常显示
- **打包前CHECKPOINT**：自动检查zip内容合规性

### 4.5 图片两步走策略（实战验证 2026-03-03）

| 改进项 | V2 | V3.1 |
|--------|----|----|
| 图片嵌入方式 | `📎` 占位符，手动上传 | Markdown `![](images/xx.png)` 语法，截图自动回填到对应模块 |
| 尺寸控制 | 无 | 导入iWiki后通过API替换为 `<img width="375">` 控制显示 |
| iWiki兼容 | base64崩溃 | 相对路径+zip打包+markdown语法，完美兼容 |
| 打包检查 | 无 | Step 6 CHECKPOINT强制检查zip内容 |

### 4.6 页面流程图（V3.6 升级为标准脚本）

V3.6 将流程图生成从「AI 临时编写 PIL 脚本」升级为**标准脚本 `scripts/gen_flowmap.py`**：
- AI 只需创建 `flowmap-config.json` 配置文件（描述节点和连线）
- 调用标准脚本一键生成，**消除每次生成时临时脚本不一致的问题**
- 生成速度提升（省去 AI 构思+编写脚本的 token 开销）

流程图特性不变：
- 实际页面截图缩略图（宽度240px，等比缩放）
- 6种颜色箭头 + 5层分层布局
- 中文字体：NotoSansCJK
- 箭头走外围通道，不穿过页面截图区域
- **3.0章节仅使用截图版流程图**

---

## 5. 产出文件说明

### PRD文档（{项目名}-prd.md）

| 章节 | 核心内容 | 读者 |
|------|----------|------|
| 项目背景 | 市场背景、用户画像、目标指标 | 全团队 |
| 产品概述 | 定位、业务时序图+流程图（Mermaid）、功能架构 | 全团队 |
| 功能说明 | **每模块含4必填+2按需子章节+截图**：功能描述+业务规则+数据字段+异常处理+[页面交互含截图]+[埋点] | 开发/设计/测试 |
| 非功能需求 | 性能、安全、兼容性 | 技术团队 |

### HTML交互原型（prototype/）

| 文件 | 说明 |
|------|------|
| `index.html` | 原型入口/导航页 |
| `pages/*.html` | 各功能页面原型（支持跳转+点击交互） |
| `screenshots/` | 自动截图 + 页面流程图 |
| `assets/style.css` | 标准CSS变量体系 |

**原型特点**：📱 适配目标平台（移动端375px/PC端1440px/响应式） | 🔗 页面间可跳转 | 👆 点击/弹窗/状态切换 | 🎨 统一设计变量

**预览方式**：
- 💻 **本地预览**：右键 `prototype/index.html` → 在浏览器中打开
- 🔧 **本地服务**：使用 server.py 启动的服务，访问 `http://localhost:{PORT}/prd-preview/{项目名}/prototype/index.html`

> ⚠️ 如需配置在线预览服务，请参考团队部署文档设置HTTP静态文件服务器。

---

## 6. 最佳实践

### 输入技巧

| ❌ 避免 | ✅ 推荐 | 原因 |
|---------|---------|------|
| "做个APP" | "微信小程序，答题获积分兑优惠券，提升公众号活跃" | 含类型+功能+目标 |
| "签到系统" | "H5签到页，每日签到获积分，连续7天翻倍，嵌入现有APP" | 含载体+规则+约束 |

### 确认单审核重点

1. **功能范围（第4项）**：P0/P1/不做的边界
2. **业务规则（第5项）**：关键数值是否合理
3. **成功指标（第6项）**：指标和目标值

### iWiki发布技巧

V3.5 新增 `publish_to_iwiki.py` 一键发布脚本，将 zip打包+检查+上传+尺寸调整 封装为一条命令，**彻底消除手动遗漏导致的图片不显示问题**。

| 场景 | 做法 |
|------|------|
| 首次发布 | 告诉AI父页面ID，自动调用 `publish_to_iwiki.py` 一键完成 |
| 更新已有 | 告诉AI页面ID，`--cover` 覆盖 |
| 不知道页面ID | 告诉AI iWiki空间名，帮你查找 |
| 图片不显示 | V3.5已自动处理（脚本强制zip打包+markdown语法） |
| 图片太大 | 脚本自动执行差异化尺寸调整（C端截图width=375，B端截图width=100%，流程图保持原宽） |
| 文档过大 | 压缩截图或减少截图数量 |
| 仅补救尺寸 | `--doc-id` 参数可单独对已上传文档调整尺寸 |

> 生成完成后AI会自动提示iWiki发布选项，无需记忆命令。脚本内置完整 CHECKPOINT，打包前自动检查合规性。

---

## 7. 质量保障机制

### CHECKPOINT检查点

V3.1 在关键步骤之间设置了强制检查点，防止执行偏差：

| 检查点 | 位置 | 核心检查项 |
|--------|------|-----------|
| Step 3 CHECKPOINT | PRD内容生成完成后 | 无模板标注残留、无AI指引注释、截图占位符就位 |
| Step 4 CHECKPOINT | 截图回填完成后 | 所有占位符已替换、每个模块有截图、无HTML img标签、时序图+流程图存在 |
| Step 6 CHECKPOINT | zip打包前 | zip内容合规（无img标签/base64/占位符残留）、图片引用与文件一一对应 |

### QA检查规则（34条）

V3.2 新增S-011 Error级检查项，确保：
- 截图嵌入到对应模块（非集中附录）
- page-flow-map.png嵌入3.0章节
- 标题不含模板标注
- 无AI注释残留
- 源文件无HTML img标签
- **无文本线框图/ASCII art残留**

---

## 8. 文件位置

```
PRD输出：{WORKSPACE}/.codebuddy/docs/prd/{项目名}/
知识库：{WORKSPACE}/.codebuddy/docs/biz-knowledge/
  ├── prd/             ← PRD自动归档
  ├── business-rules/
  ├── meeting-notes/
  └── data-models/
```

---

## 9. FAQ

**Q1：V4.0相比V3.9有什么改进？**
核心改进（4大问题修复，10项P0+1项P1）：① **Step合并提速**：原7步流程压缩为6步（Step3框架+Step4填充合并为"PRD内容生成"一步到位），首次输出时间从~20min降至~10min ② **Step2条件触发**：知识库检索改为条件触发（仅迭代项目/有参考文档时执行），全新项目跳过可节省~1分钟 ③ **CHECKPOINT精简**：Step3 CHECKPOINT从8项精简为3项核心门禁，其余移至Step4 CHECKPOINT ④ **PC端截图5层修复**：flowmap-config.json新增viewport字段、screenshot.py新增--viewport-width参数+per-page自动视口、确认单增加混合平台选项、HTML原型增加desktop-frame模板 ⑤ **M5 iWiki引导加固**：M5变更摘要新增📤独立板块，完成锚点从4板块升为5板块（📋📁📊📤🔗），防止修改后遗漏发布引导 ⑥ **质检文件取消**：质检不再生成qa-report.md文件，改为终端直接输出评分 ⑦ **耗时公式优化**：从`3min+页面数×2min`调整为`2min+页面数×1.2min`。

**Q1b：V3.9相比V3.8有什么改进？**
核心改进（P0+P1共20项修复）：① **截图命令修正**：截图服务从裸HTTP服务器改为server.py（修复/prd-preview/路由404问题） ② **端口动态化**：不再硬编码8888/8080，自动检测可用端口 ③ **路径变量化**：全文引入{WORKSPACE}/{SKILL_DIR}/{PRD_DIR}变量，消除/data/workspace/硬编码 ④ **多视口支持**：原型不再强制375px，新增PC端1440px和响应式选项 ⑤ **必填裁剪**：6项必填改为4必填+2按需，API/服务类型自动跳过页面交互和埋点 ⑥ **QA按类型裁剪**：API类型跳过HTML原型检查项 ⑦ **进度反馈**：每个Step输出进度提示 ⑧ **SKILL瘦身**：合并重复规则，精简冗余内容。

**Q1b：V3.6相比V3.5.2有什么改进？**
核心改进（2项优化）：① **流程图标准化**：新增 `scripts/gen_flowmap.py` 标准脚本，AI 不再每次临时编写 PIL 脚本，而是创建 `flowmap-config.json` 配置后调用标准脚本一键生成，消除脚本不一致和叠加问题，生成速度提升 3-5 秒 ② **确认单格式优化**：确认单不再用代码块包裹，改为直接 Markdown 文本输出，每个序号项之间强制空行，解决渲染后挤在一起的可读性问题。

**Q1b：V3.5.2相比V3.5.1有什么改进？**
核心改进（13项优化）：① 截图自动同步到images/，本地PRD预览图片不再断裂 ② CHECKPOINT配套失败修复命令，AI失败时精准修复 ③ 核心约束速览提到文档开头，AI遵循率提升 ④ 规则条数统一为34条 ⑤ screenshot.py参数化（--port/--prefix） ⑥ 截图前置条件说明 ⑦ publish_to_iwiki.py网络重试 ⑧ parent_id条件必填 ⑨ 评分公式统一 ⑩ Step 0增加截图工具检测 ⑪ getSpacePageTree调用说明 ⑫ S-004单模块豁免 ⑬ 模板占位符说明。

**Q1b：V3.5.1相比V3.5有什么改进？**
核心改进：三重防线防止AI凭记忆跳过 `publish_to_iwiki.py`。① 触发词识别表顶部增加iWiki发布映射，用户说"发布/iWiki/上传"直接路由到Step 7 ② Step 7顶部硬编码唯一允许的命令模板，AI只需填变量 ③ Step 6完成输出中写死完整发布命令，无需回忆Step 7。

**Q1b：V3.5相比V3.4有什么改进？**
核心改进：新增 `publish_to_iwiki.py` 一键发布脚本，将 Step 7 的 zip打包+CHECKPOINT检查+上传+图片尺寸调整+二次验证 封装为一条命令，彻底解决了 AI 执行时跳过 zip 打包步骤直接上传 .md 文件导致 iWiki 图片不显示的问题。支持 `--dry-run`（仅检查）、`--cover`（覆盖）、`--doc-id`（仅调尺寸）等模式。

**Q2：V3.3相比V3.2有什么改进？**
核心改进：① 禁止文本线框图/ASCII art，页面交互说明必须使用Demo截图 ② 新增S-011 Error级QA检查（线框图残留检测） ③ Step 4/5 CHECKPOINT新增线框图检查项。

**Q2：iWiki上传后图片不显示？**
V3.1已有打包前CHECKPOINT自动检查。关键：zip打包时图片必须用Markdown `![描述](images/xx.png)` 语法（禁止HTML img标签），iWiki zip导入只识别markdown图片语法关联附件。严禁base64和外部URL。

**Q3：怎么更新已发布的iWiki页面？**
`PRD修改` 后告诉AI重新上传，使用cover=true覆盖已有页面。

**Q4：截图太大怎么办？**
两步走策略：保持原始截图上传（保证清晰度），导入iWiki后 `publish_to_iwiki.py` **自动执行**差异化尺寸调整：C端页面截图 → `<img width="375">`，B端PC端截图 → `<img width="100%">`（V1.2升级自动识别），流程图保持原始宽度。B端页面通过 flowmap-config.json 的 viewport=1440 和 alt 关键词（admin/dashboard等）自动识别。

**Q5：怎么分享给团队？**
```
"XXX项目PRD已完成：
 📄 PRD：.codebuddy/docs/prd/{项目名}/{项目名}-prd.md
 🌐 原型：打开 prototype/index.html 体验
 📄 iWiki：https://iwiki.woa.com/p/{page_id}
 📊 评分：92分"
```

**Q6：怎么配置在线预览？**
使用 `python3 prd_preview_server.py --port {端口}` 启动PRD预览专用服务，然后通过 `http://{你的IP}:{端口}/prd-preview/` 访问。该服务为轻量级独立服务，仅提供PRD预览功能，不包含周报工具的API和日志。如需团队共享，建议配置Nginx或其他HTTP服务器。

**Q7：CHECKPOINT是什么？什么时候触发？**
CHECKPOINT是V3.1新增的步骤内嵌检查点，在Step 3/4/6自动执行。它通过grep命令验证PRD文件内容是否符合规范（如无模板标注、截图已嵌入、无img标签等），全部通过才能进入下一步。不可跳过。

---

## 10. 故障排查

| 问题 | 解决 |
|------|------|
| PRD生成无响应 | 检查 设置→Skills管理 是否已安装 |
| 找不到文件 | 检查 `{WORKSPACE}/.codebuddy/docs/prd/` |
| 原型打不开 | 用绝对路径打开index.html，或启动本地HTTP服务 |
| iWiki上传失败 | 检查MCP token有效性、网络连通性、zip文件大小 |
| iWiki图片不显示 | 确认使用zip打包上传，图片路径为 `images/` 相对路径 |
| 评分很低 | 确认单阶段补充更多信息 |
| Mermaid图不显示 | 使用支持Mermaid的预览器 |
| CHECKPOINT不通过 | 查看具体失败项，AI会自动修复后重新验证 |

---

> 📮 反馈：企微联系cmlliazhang
