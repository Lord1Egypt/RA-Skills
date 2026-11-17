---
name: kb-sync
description: |
  知识库同步助手。在本地笔记目录与云端知识库（IMA / 腾讯乐享 / 通用 API）之间做增量同步，支持双向 diff、冲突检测、变更预览。当用户需要"把我的笔记同步到知识库""更新云端文档""本地和云端对一下"时调用。
agent_created: true
visibility: "public"
---

# 知识库同步助手

帮用户把本地积累的 Markdown 笔记增量同步到云端知识库，或在两端做一致性比对。核心：**先 diff 预览，再同步；冲突不静默覆盖**。

## 适用场景
- 本地笔记 → IMA/乐享知识库批量上传
- 云端知识库变更 → 拉回本地归档
- 定期双向对账，防止两端漂移

## 同步策略
- **增量**：基于内容哈希/修改时间，只传变更文件。
- **幂等**：相同内容不重复上传。
- **冲突**：本地与云端均变更 → 标记冲突，人工确认，不自动覆盖。
- **预览优先**：`--dry-run` 先列出将要新增/更新/删除。

## 标准工作流
### 1. 本地 diff 预览（无外部依赖，先验证逻辑）
使用 `scripts/kb_sync.py` 在本地"源目录 ↔ 已同步清单"之间做增量计算：
```bash
python scripts/kb_sync.py diff --src "C:/Users/小江/.workbuddy/skills" --manifest "C:/Users/小江/.workbuddy/kb_manifest.json" --dry-run
```
输出：待新增/更新/删除的文件清单（基于内容哈希）。

### 2. 对接云端
- **IMA**：调用 IMA OpenAPI（`ima-skills` 技能）逐条创建/更新知识条目。
- **乐享**：`lexiang` MCP 连接器做文档/知识库同步。
- **通用 REST**：用 `api-caller` 技能的 `api_call.py` 调对方 upsert 接口。

### 3. 执行并落盘 manifest
确认预览无误后去掉 `--dry-run` 执行，并把最新哈希写入 manifest，供下次增量。

## 质量门禁
- [ ] 是否先 `--dry-run` 预览（避免误删/误覆盖）
- [ ] 冲突是否被单独标记而非自动解决
- [ ] 云端写入是否走授权 token（环境变量注入）

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "知识库同步" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某云端接口反复失败 → 记录，reflect 建议切换同步后端
- 用户常用某知识库 → `prefer` 记录默认目标

## 安全边界
- 同步范围严格限定用户指定目录，不触碰桌面/下载等个人区
- 不把含密钥的笔记上传（先经 `static-deploy` 的敏感文件检查思路）
