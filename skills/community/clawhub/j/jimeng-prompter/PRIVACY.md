# Privacy Policy — 即梦 Prompt 大师 (Jimeng Prompter)

## 数据收集

本 Skill 在本地收集以下数据用于提升提示词质量：

| 数据类型 | 存储位置 | 用途 |
|----------|----------|------|
| 视觉风格偏好 | `references/evolution-memory.md` | 跨会话偏好追踪 |
| 色调/运镜偏好 | `references/evolution-memory.md` | 自动推荐 |
| 用户负面反馈 | `references/evolution-memory.md` | 避免重复踩坑 |

## 数据存储

- **所有数据仅存储在本地文件系统** — 不上传云端，不用于训练外部模型
- 进化记忆文件：`references/evolution-memory.md`
- 无数据库、无远程 API 调用

## 数据保留

- 默认保留期限：**90 天**
- 超过 90 天的记录建议手动清理

## 数据删除

用户可随时执行以下操作：

- 说「清除即梦偏好记录」→ 删除 `references/evolution-memory.md` 全部内容
- 说「这次不用记」→ 跳过本次进化记忆写入
- 手动删除 `references/evolution-memory.md` 文件

## 同意机制

- **进化记忆写入前征求同意** — 每次写入前系统会询问「记录这次偏好到本地吗？」
- 用户说"好"/"记住"/"嗯" → 写入
- 用户说"不用"/"这次不记" → 跳过
- 不会静默写入任何用户数据

## 联网行为

- 本 Skill **不发起任何外部网络请求**
- 不调用搜索 API、不访问外部服务、不上传任何数据

## 子代理数据

- 本 Skill 不使用 sub-agent（Director 和 Prompt Crafter 均由主 AI 直接执行）
- 不存在跨代理数据传递

## GDPR / 数据保护

- 本 Skill 符合数据最小化原则：仅收集提升提示词质量所必需的偏好数据
- 用户拥有完整的数据控制权：随时查看、修改、删除
- 不收集个人身份信息（姓名、邮箱、电话等）
- 不收集敏感内容原文（仅提取结构化的风格特征）
