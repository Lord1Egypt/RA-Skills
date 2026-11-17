# SkillHub / Cursor Skills Marketplace 提交清单

> 适用版本：`heyihub-skill@1.2.0`（package.json + SKILL.md frontmatter 已同步到 1.2.0）
> 维护者：在 Claude Code / 浏览器里手动粘贴下列字段到对应 Marketplace 提交表单

---

## 一、通用元数据（两个 Marketplace 共用）

| 字段 | 值 |
|---|---|
| Skill name | `heyi-paid-api` |
| Display name | 小红书 API｜抖音、B站、快手社媒数据接口 |
| Slug | `heyi-paid-api` |
| Version | `1.2.0` |
| Summary（短） | 小红书 API、抖音 API、B站 API、快手 API 的付费 HTTP 数据接口，支持笔记/视频搜索、详情、评论、用户作品和积分计费。 |
| Description（长） | Use when a user wants an AI agent to call Heyi's Xiaohongshu, Douyin, Kuaishou, or Bilibili HTTP APIs with a Bearer API Key, including endpoint discovery, point billing, balance checks, pagination, batching, error handling, retries, or usage reconciliation. |
| Homepage | `https://api.01011.top` |
| Tags | 小红书API, 小红书数据接口, XHS API, 抖音API, B站API, 哔哩哔哩API, 快手API, 社媒数据接口, 内容搜索, 笔记详情, 评论接口, 用户作品 |
| License | MIT |
| Author | heyi |

## 二、触发词（14 个，frontmatter 已有）

```
小红书 API
XHS API
抖音 API
Douyin API
B站 API
哔哩哔哩 API
Bilibili API
快手 API
Kuaishou API
heyi paid api
笔记搜索
视频解析
内容数据接口
社媒 API
```

## 三、仓库信息

| 字段 | 值（推荐） |
|---|---|
| 主仓库（GitHub） | `https://github.com/heyi-byte/heyihub-skill` |
| 镜像仓库（GitCode） | `https://gitcode.com/heyi-byte/heyihub-skill` |
| SKILL.md 路径（仓库内） | `docs/skills/heyi-paid-api/SKILL.md` |
| npm 包 | `heyihub-skill` |
| MCP 包（关联） | `heyihub-api-mcp@0.2.0` |

## 四、输入契约（frontmatter `inputs`）

| 字段 | 必填 | 默认 | secret | 说明 |
|---|---|---|---|---|
| `api_key` | ✅ | `HEYI_API_KEY` 环境变量 | ✅ | Bearer API Key |
| `base_url` | ❌ | `https://bot.01011.top` | — | API Base URL |
| `query_or_body` | ✅ | — | — | 按接口 schema 决定放 query 还是 JSON body |

## 五、输出契约（frontmatter `outputs`）

| 字段 | 说明 |
|---|---|
| `api_response` | HTTP JSON 响应（`code` / `msg` / `data`） |
| `bill_summary` | 调用是否计费的判定（按 HTTP 200 + 业务 code 200/2000/缺失） |
| `call_record_ref` | 服务端积分流水条目指针，用于事后对账 |

## 六、依赖与运行环境

- `curl` 或任意 HTTP 客户端
- Node.js >= 14（仅 `check` / `snapshot` 命令需要）
- 有效 API Key（注册赠送 50 点；填邀请码双方各 +10）

---

## 七、Anthropic SkillHub 提交步骤

1. 打开 https://www.anthropic.com/skillhub 或登录 https://claude.ai 后在 SkillHub 页面找提交入口
2. 选择 "Submit a Skill"
3. 填写：
   - **Name**：`heyi-paid-api`
   - **Repository URL**：`https://github.com/heyi-byte/heyihub-skill`（或 GitCode 镜像）
   - **SKILL.md path**：`docs/skills/heyi-paid-api/SKILL.md`
   - **Version**：`1.2.0`
4. 上传或粘贴 SKILL.md 文件内容
5. 触发词 + tags 直接从文件 frontmatter 抽取，确认无误后提交
6. 等待 Anthropic 审核（通常 1-3 个工作日）

## 八、Cursor Skills Marketplace 提交步骤

1. 打开 https://cursor.com/marketplace 或对应提交入口
2. 选择 "Submit a Skill"
3. 填写同上：name / repository / SKILL.md path / version
4. **特别注意**：Cursor 会验证 Skill 在本机能正常加载——确保 `bin/install.js` 的 mavis 路由（本次修复）已生效，能装到 `~/.cursor/skills/heyi-paid-api/SKILL.md`
5. 本地自检：
   ```bash
   cd docs/skills/heyi-paid-api
   node bin/install.js install --agent cursor --dry-run
   ```
   应输出目标 `~/.cursor/skills/heyi-paid-api/SKILL.md` 在列表里
6. 提交后等待 Cursor 审核

## 九、提交后验证

- Anthropic SkillHub：登录 Claude.ai → SkillHub → 搜 `heyi-paid-api` → 应能在结果里看到
- Cursor Marketplace：打开 Cursor → Settings → Skills → 搜 `heyi-paid-api`

## 十、关联：MCP 包（已发）

- `heyihub-api-mcp@0.2.0` 已构建并通过 npm pack 验证（25.5 kB / 34 文件），含 69 个工具
- 当前 publish 被 npm auth 阻塞，需用户刷新 token 后再发：参见 TODO 状态

---

**注意**：两个 Marketplace 都是**人工审核**，不是 git push。提交后由用户复制粘贴上述字段，并等待平台审核。审核期间可在 Marketplace 后台查看进度。