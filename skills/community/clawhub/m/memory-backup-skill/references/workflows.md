# 工作流备份指南

## 工作流存放位置

所有工作流统一放在：

```
memory/workflows/<领域>-<名称>.md
```

不在根目录，不在 `docs/`，不在 `memory/projects/`。

## 为什么放在 memory/workflows/

- 备份脚本自动追踪 `memory/` 下所有文件，包括 `memory/workflows/`
- 跨渠道共享，所有会话都能读取
- 开新对话时说"从备份继续"，工作流一并恢复

## 新增工作流

在 `memory/workflows/` 下创建新文件，命名规范：

```
memory/workflows/<领域>-<名称>.md
```

示例：
- `memory/workflows/wechat-publish-workflow.md`
- `memory/workflows/cloudbase-deploy-workflow.md`
- `memory/workflows/feishu-doc-creation-workflow.md`

## 备份时自动清理旧版（重要）

**原则**：备份新工作流时，必须检查是否有同名旧版文件，一并清理。

常见旧版位置（需检查并删除）：
- `memory/wechat-publish-workflow.md` ← 旧位置，已迁移到 `memory/workflows/`
- `memory/<名称>-workflow.md` ← 旧位置
- `docs/<名称>-workflow.md` ← 旧位置
- `docs/<名称>.md` ← 可能是旧工作流

**清理操作**：
```bash
# 1. 确认新版位置
ls memory/workflows/<名称>-workflow.md

# 2. 检查旧位置是否有同名文件
ls memory/<名称>-workflow.md 2>/dev/null && echo "旧版存在，需删除"
ls docs/<名称>-workflow.md 2>/dev/null && echo "旧版存在，需删除"

# 3. 确认新版内容已包含旧版所有有价值信息后，删除旧版
rm memory/<名称>-workflow.md
rm docs/<名称>-workflow.md

# 4. 推送备份
bash scripts/memory-backup.sh
```

**判断标准**：
- 新旧版内容重复 → 删旧
- 旧版有新版没有的关键信息 → 先合并到新版，再删旧
- 不确定时 → 保留旧版，注明"已废弃，迁移到 memory/workflows/"

## 工作流文档结构建议

```markdown
# 工作流名称

## 适用场景
什么时候用这个工作流

## 前置准备
开始前需要什么（账号、工具、权限）

## 步骤
1. ...
2. ...

## 注意事项
容易踩的坑

## 相关记忆
关联的项目或配置
```

## 恢复流程

开新对话时，说：
> "从备份继续，我是自媒体创作者，用微信公众号工作流发文章"

龙虾读取 `memory/workflows/wechat-publish-workflow.md` 后即可按流程执行，无需重新解释。
