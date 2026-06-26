---
name: inkroam-bijian-writing
version: 1.1.0
description: 笔尖写作专家：三要素收集 → 调用笔尖AI生成文章 → 输出可发布内容。Use when user asks to 用笔尖写文章 / 生成公众号文章 / 写一篇文章.
---

# 笔尖写作专家 Skill

三要素驱动的 AI 写作工具，调用笔尖AI平台生成高质量文章。

**职责边界：** 本 Skill 只负责**写作**（三要素收集 → 生成 → 输出），不负责发布。发布请使用 `inkroam-publisher`。

## 配置

### 笔尖 API Token

在工作区创建配置文件 `<workspace>/.bijian_config`（或 `$OPENCLAW_WORKSPACE/.bijian_config`）：

```bash
export BIJIAN_API_TOKEN='你的token'
export BIJIAN_TOKEN_HEADER='X-API-KEY'
export BIJIAN_TOKEN_PREFIX=''
export BIJIAN_BASE_URL='https://bj.aizmjx.com/api'
```

Token 获取地址：https://sso.aizmjx.com/home/apikey

**配置检查：**
```bash
# 按优先级查找配置文件
CONFIG_FILE="${OPENCLAW_WORKSPACE}/.bijian_config"
[ -f "$CONFIG_FILE" ] || CONFIG_FILE="$HOME/.openclaw/workspace/.bijian_config"
[ -f "$CONFIG_FILE" ] && source "$CONFIG_FILE" && echo "✅ 配置已加载" || echo "❌ 请创建 .bijian_config"
```

⚠️ **不要向用户询问 token，直接从配置文件读取。**

## 工作流

### Step 1：查询写作空间

```bash
source "$CONFIG_FILE" && python3 scripts/bijian_api.py spaces
```

- 1个空间 → 自动选择
- 多个空间 → 列出让用户选择
- 用户输入 `-切换空间` → 重新查询

### Step 2：收集三要素

**必须收集完整三要素才能生成。**

```
请提供文章三要素：

1️⃣ 主题（必填）
   例：花了3万养了一只金融虾（OpenClaw），到底值不值

2️⃣ 观点要点（必填）
   你最想表达的3-5条核心观点
   例：金融虾难在信任建立；值不值看系统可控性；五层架构设计思路

3️⃣ 参考素材（重要！）
   相关链接、操作步骤、安装命令、使用案例、数据来源等
   例：完整安装教程 + 对话案例 + 效果数据
```

**收集策略：**
- 只给主题 → 追问观点要点（至少3条）
- 没有素材 → **不留空**，AI 按文章类型主动补充（见下方策略）

**⚠️ 素材质量直接决定笔尖输出质量。素材越具体，文章越有干货。**

### 素材增强策略（按文章类型分场景）

AI 先判断文章类型，再主动补充对应素材：

| 类型 | 重点补充 |
|------|---------|
| 📐 教程/干货/工具 | 安装命令、使用案例、效果数据、技术架构、资源链接 |
| 🔥 热点/时事 | 事件时间线、多方观点、数据支撑、信息来源 |
| 💛 情感/故事/IP | 真实细节、情感锚点、人物画像、共鸣场景、金句 |
| ⚔️ 军事/历史/知识 | 事实数据、权威来源、对比分析、独特视角 |
| 🛒 种草/测评/变现 | 亲身体验、价格对比、效果证据、避坑提醒 |

### Step 3：调用笔尖生成

```bash
source "$CONFIG_FILE" && python3 scripts/bijian_api.py generate \
  --space-id ${SPACE_ID} \
  --topic-theme "${TOPIC_THEME}" \
  --viewpoints "${VIEWPOINTS}" \
  --reference-content "${REFERENCE_CONTENT}" \
  --user-require "${USER_REQUIRE}" \
  --is-need-picture false
```

### Step 4：轮询状态

```bash
source "$CONFIG_FILE" && python3 scripts/bijian_api.py task --article-id ${ARTICLE_ID}
```

状态码：`1`=生成中 `2`=成功 `3`=失败。每 3-5 秒查一次，最多 10 次。

### Step 5：获取文章

```bash
source "$CONFIG_FILE" && python3 scripts/bijian_api.py article --article-id ${ARTICLE_ID}
```

**展示给用户：**
```
✅ 文章生成成功！

标题：xxx
字数：1402字
封面图：已生成

[预览前200字]

下一步：
- 输入"发布" → 调用 inkroam-publisher 发布
- 输入"预览" → 查看完整文章
- 输入"重新生成" → 修改三要素重新生成
```

## 错误处理

| 错误 | 处理 |
|------|------|
| 令牌无效（401） | 提示重新获取：https://sso.aizmjx.com/home/apikey |
| 空间不存在 | 提示创建空间：https://bj.aizmjx.com/space |
| 生成失败 | 提示重新组织三要素，不盲目重试 |

## 依赖

- Python 3.7+
- 笔尖 API 脚本：`scripts/bijian_api.py`（已内置）

## 变更日志

- **v1.1.0** (2026-03-10)：配置路径说明优化；统一版本号。
- **v1.0.0** (2026-03-10)：首次发布。三要素收集、笔尖API对接、素材增强策略（5种文章类型）。发布功能拆分至 inkroam-publisher。
