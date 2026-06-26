# 话袋笔记 Skill

---

## ✨ 核心能力（MVP）

| 能力 | 说明 |
|------|------|
| **✏️ 新建笔记** | 用一句话快速记录你的想法、会议内容或灵感 |
| **🔍 更新笔记** | 对已有笔记进行补充或修改，让内容始终保持最新 |
| **📄 搜索笔记** | 输入关键词，快速找到你记录过的内容 |

---
💡 使用场景
✏️ 随手记录（想到就记）
不需要整理格式，直接说就可以。
💬 记录一个想法

👤 记一下：以后可以试试每天早起30分钟看书，提高专注力
🤖 好的，已经帮你记下来了。


💬 会议快速记录

👤 帮我记一下今天的结论：
1）本周先完成首页改版的基础功能
2）登录问题优先修复，明天前给出方案
3）下周一安排联调，涉及前后端一起参与
🤖 已帮你记录好了，后面可以随时查看或补充。


🔍 要用时找（随时召回）
不用翻记录，直接问。
💬 查找历史笔记

👤 帮我找一下之前记的“早起看书”的想法
🤖 找到了几条相关内容，已经按时间帮你整理好了。


🚀 快速上手
你只需要记住两件事：


📝 想记录 → 直接说“记一下…”


🔎 想查找 → 直接说“帮我找…”


剩下的交给我来处理。

✅ 当前支持能力（MVP）

- 新建笔记
- 更新笔记
- 关键词搜索笔记


🌱 小提示

不需要结构化输入，像聊天一样说就行

内容越具体，后面越容易找回来

可以把它当作你的「第二大脑」

---

## 安装


### 方式一：通过 ClawHub/SkillHub（腾讯）/SkillHub（中国）  安装（推荐）

```bash
clawhub install huadai-notes-skills
SkillHub install huadai-notes-skills
SkillHub install huadai-notes-skills
```

### 方式二：让 AI 助手安装

> 帮我安装话袋笔记 Skill，地址是 https://github.com/HuadaiNotes/hd_notes_skills/blob/main/SKILL.md

### 方式三：手动安装

```bash
mkdir -p ~/.openclaw/workspace/skills/huadai-notes-skill
cd ~/.openclaw/workspace/skills/huadai-notes-skill
curl -sL https://github.com/HuadaiNotes/hd_notes_skills/blob/main/SKILL.md -o SKILL.md
curl -sL https://github.com/HuadaiNotes/hd_notes_skills/blob/main/SKILL.md -o package.json
```


## 配置（重要）

### 自动配置（默认）

安装后首次使用时，若检测到缺少配置，AI 会自动触发 OAuth Device Flow（详见 [OAuth 授权配置（话袋笔记）](references/oauth.md)）：

1. 你发起任意笔记相关操作（保存/搜索/打开）
2. AI 检测到未配置 `HUADAI_API_KEY` / `HUADAI_USER_UUID`
3. AI 生成授权链接（verification_uri）并提示你完成授权
4. 授权成功后自动写入 `HUADAI_API_KEY` 与 `HUADAI_USER_UUID`，继续执行你的请求

### 手动配置（可选）

在 `~/.openclaw/openclaw.json` 中注入（示例见 [配置（必须先完成）](references/config.md)、[OAuth 授权配置](references/oauth.md)）：

- `HUADAI_BASE_URL`: `https://openapi.ihuadai.cn/open/api/v1`
- `HUADAI_API_KEY`: OAuth 换取的 `api_key`
- `HUADAI_USER_UUID`: OAuth 返回的用户 `unique_id`（对应请求头 `USER-UUID`）
- `HUADAI_CLIENT_ID`: 可选覆盖；默认使用服务端预注册 `client_id`

此 Skill 需要在运行环境中提供以下环境变量（不要在聊天中粘贴任何密钥）：

- `HUADAI_BASE_URL`（必填）：话袋 OpenAPI 根地址（例如 `https://openapi.ihuadai.cn/open/api/v1`）
- `HUADAI_CLIENT_ID`（可选覆盖，仅 OAuth）：OAuth Device Flow 的应用标识（申请设备码/换取 API Key；流程见 [OAuth 授权配置](references/oauth.md)）
- `HUADAI_API_KEY`（必填）：业务 API 调用鉴权（请求头 `Authorization`）
- `HUADAI_USER_UUID`（强烈建议，群聊/多人场景必配）：用户唯一标识

## Base URL 与接口路径

- Base URL：`https://openapi.ihuadai.cn/open/api/v1`
- API 路径：以本仓库 **references** 为准（统一 `/open/api/v1/...`）；接口分册：[新建笔记（Upload）](references/upload.md)、[更新笔记（Update）](references/update.md)、[搜索笔记（Search）](references/search.md)、[API 详细参考](references/api-details.md)

## 安全说明

- 不在对话中索取、输出或回显任何 `HUADAI_API_KEY`
- 所有读写都必须通过 API 获取结果，禁止编造“已保存/已找到”
- 开启 `HUADAI_USER_UUID` 时，非 user 的请求必须拒绝并提示原因

---

## 📜 相关链接

- [话袋官网](https://ihuadai.cn/)
- [ClawHub](https://clawhub.ai/----/ihuadai.cn)
- [SkillHub腾讯](https://skillhub.tencent.com/-----/ihuadai.cn)
- [SkillHub中国](https://www.skill-cn.com//-----/ihuadai.cn)

---

## License

见 `LICENSE`。


