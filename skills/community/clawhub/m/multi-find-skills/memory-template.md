# Multi-Find-Skills 记忆模板

> 本文件是 `memory-template.md` 的参考格式，实际运行时会读写 `~/.openclaw/skills/multi-find-skills/memory.md`

创建 `~/.openclaw/skills/multi-find-skills/memory.md`（如果不存在）：

```markdown
# Multi-Find-Skills Memory

## Status
status: ongoing
last: YYYY-MM-DD
sources: both
integration: proactive

## Preferences
<!-- 用户明确声明的质量偏好 -->
<!-- 示例：偏好活跃维护的、接受实验性的、喜欢轻量级的 -->

## Source Policy
<!-- 默认搜索来源：both / clawhub / skills.sh / lobehub -->
<!-- 示例：both -->

## Liked
<!-- 用户明确表扬过的技能及原因 -->
<!-- 格式：source:identifier — "表扬原因" -->
<!-- 示例：clawhub:pdf — "解析准确" -->
<!--      skills.sh:vercel-labs/agent-skills@frontend-design — "UI方案很好" -->

## Passed
<!-- 用户明确拒绝过的技能及原因 -->
<!-- 格式：source:identifier — "拒绝原因" -->

## Domains
<!-- 用户工作的领域（帮助缩小搜索范围）-->
<!-- 示例：前端、飞书集成、游戏开发 -->

---
*Updated: YYYY-MM-DD*
```

## Status 说明

| 值 | 含义 |
|---|---|
| `ongoing` | 仍在学习偏好 |
| `established` | 偏好数据已足够 |

## 记忆规则

### 要记录
- 用户明确说的来源偏好（"两个都搜"、"只用 ClawHub"）
- 用户明确说的质量偏好（"要活跃维护的"、"可以接受实验性的"）
- 用户明确表扬或拒绝的技能及原因

### 不要记录
- 静默安装（无评论 = 无数据）
- 从行为模式推断的偏好
- 用户没有明确说过的任何内容

## 使用方式

多技能匹配时：
1. **检查来源模式** — 按 `both` / `clawhub` / `skills.sh` / `lobehub` 搜索
2. **检查 Passed** — 排除相似的
3. **检查 Liked** — 倾向相似特质的
4. **应用 Preferences** — 据此过滤

## 维护

保持 50 行以内。超过时：
- 归档旧的 Liked/Passed 条目
- 保留最新的 Preferences