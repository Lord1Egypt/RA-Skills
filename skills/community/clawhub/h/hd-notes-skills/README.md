# 话袋笔记 Skill

话袋笔记 Skill 是话袋面向通用 Agent 的笔记能力扩展，支持通过自然语言新建、更新和搜索个人笔记。它采用 `SKILL.md` + `references/` + `scripts/` 的标准 Skill 结构，可发布到 ClawHub、SkillHub 等 Skill 市场，也可被支持 Skill 目录的 Agent 环境安装使用。

## 核心能力

| 能力 | 说明 |
|------|------|
| 新建笔记 | 用一句话快速记录想法、会议结论、灵感和待整理内容 |
| 搜索笔记 | 用关键词找回之前记录的内容 |
| 更新笔记 | 基于搜索结果确认 `unique_id` 后，补充或修改已有笔记 |

## 安装

### 让 AI 助手安装（推荐）

在 AI 助手中输入以下指令即可安装：

**直接安装ClawHub地址：**
```text
请安装话袋笔记 Skill，地址：https://clawhub.ai/monkeydb/hd-notes-skills
```

**Claude Code / Cursor / Codex / OpenClaw / 其他通用 Agent：**
```text
请安装话袋笔记 Skill，地址：https://github.com/monkeyDB/hd-notes-skills
```

如果 ClawHub 不可用，也可以直接从 GitHub 安装：
```text
请安装话袋笔记 Skill，地址：https://raw.githubusercontent.com/monkeyDB/hd-notes-skills/main/SKILL.md
```

### 手动安装

将本仓库作为一个 Skill 目录放到你的 Agent 支持的 Skill 目录中。常见形式如下，实际路径以对应 Agent 文档为准：

```bash
git clone https://github.com/monkeyDB/hd-notes-skills.git
```

安装后，确保 Agent 能读取仓库根目录的 `SKILL.md`、`references/api.md` 和 `scripts/` 目录。

## 配置

1. 打开 [话袋开放平台](https://ihuadai.cn/desktop/openai)
2. 创建 API Key
3. 在 Agent 运行环境中配置环境变量：

```bash
export HUADAI_API_KEY=<你的API Key>
```

**Claude Code 用户** 也可以在 `~/.bashrc` 或 `~/.zshrc` 中设置：

```bash
echo 'export HUADAI_API_KEY=<你的API Key>' >> ~/.zshrc
source ~/.zshrc
```

调用 OpenAPI 时，Skill 会通过请求头传递：

```http
Authorization: <HUADAI_API_KEY>
```

> ⚠️ 不要在聊天中粘贴、展示或保存 API Key。

## 使用示例

### 记录想法

```text
记一下：以后可以试试每天早起 30 分钟看书，提高专注力。
```

### 记录会议结论

```text
帮我记一下今天的结论：
1. 本周先完成首页改版的基础功能
2. 登录问题优先修复，明天前给出方案
3. 下周一安排前后端联调
```

### 查找历史笔记

```text
帮我找一下之前记的「早起看书」相关内容。
```

### 更新笔记

```text
把刚才找到的早起看书那条补充一句：先从每周三天开始，不追求每天都做。
```

## API

Base URL：

```text
https://openapi.ihuadai.cn/open/api/v1
```

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/search` | 搜索笔记 |
| GET | `/block/:unique_id` | 获取笔记详情 |
| POST | `/block/upload-block` | 新建笔记 |
| POST | `/block/update-block` | 更新笔记 |

请求体、curl 示例和错误码见 [references/api.md](references/api.md)。

## 兼容平台

| 平台 | 状态 | 说明 |
|------|------|------|
| Claude Code | ✅ | 支持 SKILL.md 目录格式 |
| Cursor | ✅ | 支持 Skill 安装 |
| Codex (OpenAI) | ✅ | 通过 OpenClaw 兼容 |
| OpenClaw | ✅ | 原生支持，含 metadata.openclaw 配置 |
| 任意 Skill 目录 Agent | ✅ | 标准 SKILL.md + references/ + scripts/ 格式 |

## 安全边界

- API Key 只用于请求头 `Authorization`。
- 未配置 API Key 时，Skill 只引导用户到话袋开放平台创建并配置 API Key。
- 写操作必须以 API 返回 `code=200` 为准。
- 搜索为空时必须明确说明未找到，禁止编造结果。
- 更新笔记时，`unique_id` 必须来自搜索结果或用户明确提供。

## 相关链接

- [GitHub地址](https://github.com/monkeyDB/hd-notes-skills)
- [ClawHub商店地址](https://clawhub.ai/monkeydb/hd-notes-skills)
- [话袋开放平台](https://ihuadai.cn/desktop/openai)
- [话袋官网](https://ihuadai.cn)

## License

MIT-0
