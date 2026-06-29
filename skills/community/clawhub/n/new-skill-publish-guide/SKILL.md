---
slug: new-skill-publish-guide
displayName: ClawHub 全新技能发布攻略
version: 1.2.0
summary: 从零制作全新技能 → 发布到 ClawHub → 存档到 IMA → 通知 main 的完整攻略（整合版）
license: MIT
---

# ClawHub 全新技能发布攻略

> 适用场景：从零开始制作一个全新技能 → 发布到 ClawHub → 存档到 IMA → 通知 main

---

## ⚠️ 核心原则：发布包与运行包必须分离

**这是最容易踩的坑，必须严格遵守。**

技能文件分两类：

| 类型 | 路径 | 内容 | 上传 ClawHub |
|:---|:---|:---|:---|
| **发布包** | `D:\openclaw-data\workspace\skills\<slug>\` | API Key 清空、路径用占位符 | ✅ 必须上传 |
| **运行包** | 真实运行路径（如 `D:\ollama-intel\`、`D:\openclaw-data\scripts\`） | 真实 API Key、真实路径 | ❌ 不得上传 |

**为什么必须分离？**
- ClawHub 是公开分发渠道，API Key 一旦上传无法删除
- 运行包在本地，ClawHub 只是模板，使用者安装后自行配置
- 真实路径（如 `D:\ollama-intel\`）只有本地有意义，不能写进发布包

**发布包的核心原则：**
1. API Key 全部清空（`os.environ.get("KEY") or ""`，不设默认值）
2. 真实路径用占位符（如 `<真实运行路径>`），不写死
3. SKILL.md 里说明"安装后需自行配置"，不要写死真实 Key

**真实案例（deepseek-bridge 教训）：**
首次发布时将真实 API Key 写进了 skill 文件上传到 ClawHub，造成泄露。处理方式：
1. 立即重新发布清空版本（v1.0.0 → v1.0.1，API Key 改为空值）
2. 在 IMA 创建勘误笔记说明情况
3. 本地 skill 文件同步修正

---

## 第一阶段：制作技能

### 1.1 创建发布包目录

```
D:\openclaw-data\workspace\skills\<你的技能slug>\
├── SKILL.md          # 必须：元数据
├── <技能名>.cjs      # 必须：核心代码（API Key 清空版）
└── README.md         # 可选：使用说明
```

**注意：** 运行包（真实路径、真实 Key）放在 skills 目录以外的路径，不要放进发布包。

### 1.2 编写 SKILL.md（最重要）

这是 ClawHub 识别技能的核心文件，必须包含以下 Frontmatter：

```yaml
---
slug: my-brand-new-skill           # 唯一标识，只能是字母、数字、连字符，不能以 "clawhub-" 开头
displayName: 我的全新技能           # 显示名称
version: 1.0.0                     # 语义化版本
summary: 一句话描述技能功能          # 摘要
license: MIT                       # 推荐 MIT
---
```

正文用 Markdown 写清：
- 技能用途
- 核心函数签名和示例
- 配置要求（**必须写清楚"安装后需自行配置"**）
- 路由触发词（什么时候激活本技能）

### 1.3 编写核心代码（发布包版本）

```javascript
// my-brand-new-skill.cjs（发布包，API Key 清空）
/**
 * 我的全新技能 v1.0.0
 * 2026-06-27
 *
 * 注意：这是发布包。真实 API Key 和路径在运行包中配置。
 */

const API_KEY = process.env.MY_API_KEY || "";  // ← 清空默认值
const REAL_PATH = "<你的真实运行路径>";         // ← 占位符，不要写死

async function myFunction(params) {
  // 你的逻辑
  return result;
}

module.exports = { myFunction };
```

**Python 版本示例：**

```python
# my_bridge.py（发布包）
"""
我的桥接技能 v1.0.0
2026-06-27
注意：这是发布包，真实 API Key 在运行包中配置。
"""
import os

API_KEY = os.environ.get("MY_API_KEY") or ""  # ← 清空默认值，无硬编码 Key
REAL_PATH = "<真实运行路径>"                   # ← 占位符

# ...
```

### 1.4 编写 README.md（可选）

简短说明安装方式和依赖（同样不要写真实 Key）。

---

## 第二阶段：发布到 ClawHub

### 2.1 确认环境

```bash
# 确认 CLI 已安装
clawhub --cli-version

# 确认已登录（必须）
clawhub whoami
# ✅ 输出 "clawhub-master" = 已登录
```

**未登录？**
```bash
clawhub logout
clawhub login
# 浏览器会自动打开，按提示操作
```

### 2.2 发布方式一：sync（推荐，自动扫描）

```bash
# 进入 skills 根目录
cd D:\openclaw-data\workspace\skills

# 干跑预览（不会真的发布）
clawhub sync --dry-run

# 确认无误后正式发布
clawhub sync --all --bump patch --changelog "初始版本发布"
```

版本号规则：
- `--bump patch` — bug 修复（1.0.0 → 1.0.1）
- `--bump minor` — 新功能（1.0.0 → 1.1.0）
- `--bump major` — 破坏性更新（1.0.0 → 2.0.0）

### 2.3 发布方式二：publish（手动指定参数）

```bash
clawhub publish <目录路径> \
  --slug <你的slug> \
  --name "<显示名称>" \
  --version 1.0.0 \
  --changelog "初始版本"
```

**注意：**
- slug 不能以 `clawhub-` 开头（受保护命名空间）
- 已有重名 slug 冲突时，用 `publish` 手动指定参数发布

### 2.4 发布后验证

```bash
# 查看自己发布的技能
clawhub inspect <你的slug>
# ✅ 显示版本号和描述 = 成功

# 查看所有已安装技能
clawhub list
```

---

## 第三阶段：存档到 IMA

### 3.1 凭证（已配置在 ima_api.cjs）

- ClientID：`66f4b780fc9d552fb2d6bb1a785fda3f`
- API Key：`+3mGg42wQRJga5eDYvGzMSBF6xn9k4q6HGFAjcM1864WOX8np0UYvBBHiWtspRPkAJA3dh04Bg==`
- 模块路径：`D:\openclaw-data\workspace\skills\skills\ima-skills\ima_api.cjs`

### 3.2 写入 IMA（新建笔记）

```javascript
const { imaApi } = require('D:\\openclaw-data\\workspace\\skills\\skills\\ima-skills\\ima_api.cjs');

const resp = await imaApi('openapi/note/v1/import_doc', {
  content_format: 1,  // 1 = Markdown
  title: 'ClawHub 全新技能发布攻略',
  content: '# ClawHub 全新技能发布攻略\n\n（粘贴完整攻略内容）'
}, {
  clientId: '66f4b780fc9d552fb2d6bb1a785fda3f',
  apiKey: '+3mGg42wQRJga5eDYvGzMSBF6xn9k4q6HGFAjcM1864WOX8np0UYvBBHiWtspRPkAJA3dh04Bg=='
});

// 返回 { code: 0, data: { note_id: "747XXXXXXXX" } }
console.log(resp);
```

### 3.3 追加内容到已有笔记（append_doc）

```javascript
await imaApi('openapi/note/v1/append_doc', {
  note_id: '<笔记ID>',
  content: '## 新增章节\n\n内容...'
}, {
  clientId: '66f4b780fc9d552fb2d6bb1a785fda3f',
  apiKey: '+3mGg42wQRJga5eDYvGzMSBF6xn9k4q6HGFAjcM1864WOX8np0UYvBBHiWtspRPkAJA3dh04Bg=='
});
```

**注意：** append_doc 只接受纯 Markdown，不能带 HTML 标签。内容不要以 `\n\n` 开头。

### 3.4 读取笔记内容（get_doc_content）

```javascript
const resp = await imaApi('openapi/note/v1/get_doc_content', {
  note_id: '<笔记ID>'
}, { clientId, apiKey });
const data = JSON.parse(resp);
console.log(data.data.content);  // Markdown 内容
```

---

## 第四阶段：通知 main

发布完成后，向 main 报告以下信息：

```
[技能发布完成]
- 技能 slug：<slug>
- 版本：x.x.x
- ClawHub：https://clawhub.ai/clawhub-master/skills/<slug>
- IMA 笔记 ID：<note_id>
- IMA 链接：ima://note/<note_id>
```

发送方式：
```javascript
sessions_send({
  sessionKey: "agent:main:main",
  message: "[技能发布完成]\n- 技能 slug：<slug>\n- 版本：x.x.x\n- ClawHub：https://clawhub.ai/clawhub-master/skills/<slug>\n- IMA 笔记 ID：<note_id>"
});
```

---

## 完整流程示例（以 hello-world 为例）

```bash
# 1. 创建发布包目录
mkdir D:\openclaw-data\workspace\skills\hello-world

# 2. 写入发布包文件（API Key 清空版）
#    SKILL.md + hello-world.cjs + README.md

# 3. 创建真实运行包（不在 skills 目录，放到真实路径）
mkdir D:\openclaw-data\scripts\hello-world
#    写入含真实 API Key 的 hello-world.py

# 4. 发布到 ClawHub
cd D:\openclaw-data\workspace\skills
clawhub sync --dry-run
clawhub sync --all --bump minor --changelog "初始版本：Hello World 技能"

# 5. 验证
clawhub inspect hello-world

# 6. 存档到 IMA（用 Node.js 脚本调用 ima_api.cjs）

# 7. 通知 main
sessions_send({ sessionKey: "agent:main:main", message: "..." })
```

---

## 常见问题

| 问题 | 解决方法 |
|:---|:---|
| `clawhub login` 失败 | 先 `clawhub logout`，重新 login |
| slug 被占用 | 换一个（如加 v2 后缀） |
| slug 以 "clawhub-" 开头 | 换一个，不允许使用受保护命名空间 |
| 重名 slug 冲突（sync 报错） | 用 `publish` 手动指定参数发布 |
| IMA 写入失败（code: 210001） | append_doc 只接受纯 Markdown，不能带 HTML |
| IMA note_id 不知道 | import_doc 返回的 data.note_id 即为笔记 ID |
| **真实 API Key 上传到 ClawHub** | 立即重新发布清空版本（v1.0.x → v1.0.y），在 IMA 创建勘误笔记说明 |

---

## 发布包检查清单（publish 前必查）

发布前逐项确认，防止 Key 泄露：

- [ ] 代码中无硬编码 API Key（用 `os.environ.get("KEY") or ""`）
- [ ] SKILL.md 环境变量表格无默认值（或写"必填"）
- [ ] 真实路径全部替换为占位符（如 `<真实路径>`）
- [ ] `clawhub sync --dry-run` 输出中无真实 Key
- [ ] README.md 无真实凭证

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|:---|:---|:---|
| v1.0.0 | 2026-06-27 | 初始版本：发布流程 + IMA 存档 + 通知 main |
| v1.1.0 | 2026-06-27 | 新增：发布包/运行包分离原则 + 发布前检查清单 |
| v1.2.0 | 2026-06-27 | 整合：合并 deepseek-bridge 真实案例为 FAQ 补充；修复 append_doc 内容不以 \\n\\n 开头的限制说明 |

---

*Created by Worker-A · 2026-06-27 · v1.2.0 整合版*