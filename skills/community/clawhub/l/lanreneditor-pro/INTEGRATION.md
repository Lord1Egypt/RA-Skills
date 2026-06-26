# AI 平台集成指南

> 支持接入：扣子 Coze、Dify、FastGPT、OpenClaw、QClaw、WorkBuddy 等任意支持 HTTP 工具的 AI 平台

---

## 快速开始

### 1. 准备工作

| 项目 | 说明 |
|------|------|
| 平台地址 | `https://open.tyzxwl.cn` |
| API Key | 在「个人中心 → API Key」生成 |
| 公众号 | 至少授权 1 个微信公众号 |

### 2. 核心接口

```text
Base URL: https://open.tyzxwl.cn
Header: X-API-Key: wemd_xxxxxxxxxxxx
```

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/skill/templates` | GET | 获取模板列表（含用户自定义模板） |
| `/api/skill/templates/categories` | GET | 获取模板分类列表 |
| `/api/skill/accounts` | GET | 获取公众号列表 |
| `/api/skill/publish` | POST | 创建发布任务 |
| `/api/skill/publish/status` | GET | 查询发布状态 |
| `/api/skill/quota` | GET | 查询发布额度和公众号绑定情况 |

---

## 平台接入方式

### 扣子 Coze

1. 新建 Bot → 添加 HTTP 工具
2. 配置 4 个接口，统一添加 `X-API-Key` Header
3. 给 Bot 添加系统提示词（见下方）

### Dify / FastGPT

1. 添加自定义工具或 HTTP 请求节点
2. 配置 6 个接口
3. 在工作流中串联：获取模板 → 选模板 → 获取公众号 → 选公众号 → 发布 → 查询状态

### OpenClaw / QClaw / WorkBuddy

直接导入 `openclaw-skill` 目录或 ZIP 包，填入配置：

```yaml
apiBaseUrl: https://open.tyzxwl.cn
apiKey: wemd_xxxxxxxxxxxx
```

---

## 系统提示词（必读）

将以下内容添加到你的 Bot 系统提示词：

```text
你是微信公众号排版发布助手。工作流程：

1. 获取或生成文章内容
2. 调用 templates 接口获取模板列表
   - 只使用 isUserTemplate: true 的用户自定义模板
   - 如果 userTemplatesCount = 0，停止流程，引导用户创建模板：
     * 模板设计器：https://open.tyzxwl.cn/website/template-designer.html
     * Fork 官方模板：https://open.tyzxwl.cn/website/template-market.html
     * 个人中心管理：https://open.tyzxwl.cn/profile.html?tab=templates
3. 调用 accounts 接口获取公众号列表，让用户选择公众号
4. 确认后调用 publish 接口发布
5. 轮询 status 接口直到完成

额外能力：
- 用户可以随时使用 quota 接口查询剩余发布额度
- 用户可以要求预览排版效果

重要规则：
- 禁止使用系统内置模板（isUserTemplate: false）
- 用户没有自定义模板时必须引导创建，不能继续发布
- 必须让用户确认模板和公众号选择，不要自动跳过
```

---

## 发布接口参数

```json
POST /api/skill/publish
{
  "content": "# 文章标题\n\n正文内容...",
  "title": "文章标题",
  "templateId": "default",
  "accountId": "wx_appid（可选，默认第一个公众号）",
  "author": "作者名（可选，默认使用公众号名称）",
  "digest": "摘要（可选）",
  "coverImage": "封面图URL（可选）",
  "contentSourceUrl": "阅读原文链接（可选）",
  "autoGenerateCover": true
}
```

> `autoGenerateCover` 默认为 `true`，封面图采用 5 层兜底策略：用户指定 → AI 生成 → 文章首图 → 默认封面 → 占位图。

---

## 测试命令

```bash
# 测试模板接口
curl -H "X-API-Key: 你的KEY" https://open.tyzxwl.cn/api/skill/templates

# 测试模板分类
curl -H "X-API-Key: 你的KEY" https://open.tyzxwl.cn/api/skill/templates/categories

# 测试公众号接口
curl -H "X-API-Key: 你的KEY" https://open.tyzxwl.cn/api/skill/accounts

# 测试额度查询
curl -H "X-API-Key: 你的KEY" https://open.tyzxwl.cn/api/skill/quota

# 测试发布
curl -X POST -H "X-API-Key: 你的KEY" -H "Content-Type: application/json" \
  -d '{"content":"# 测试\n\n内容","templateId":"default","title":"测试文章"}' \
  https://open.tyzxwl.cn/api/skill/publish
```

---

## 常见问题

**Q: 发布失败说封面图裁剪问题？**  
A: 确保封面图是 2.35:1 比例（900x383），或设置 `autoGenerateCover: true` 让系统自动处理。

**Q: 为什么没有让我选模板/公众号？**  
A: 检查系统提示词是否明确要求必须确认选择。

**Q: 接口返回 401 错误？**  
A: 检查 API Key 是否正确，是否已过期。

**Q: 接口返回 429 错误？**  
A: 请求频率超限（默认 100 次/小时），请降低调用频率。

**Q: 模板列表中看不到我的自定义模板？**  
A: 确保 API Key 对应的用户已在 Web 端创建了自定义模板。Skill 模板接口会自动合并用户模板和内置模板。
