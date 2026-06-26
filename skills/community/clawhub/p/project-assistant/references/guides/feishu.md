# 飞书文档集成指南

## 协作原则

**只读 + 建议，不直接修改文档**

```
分析项目 → 生成建议 → 用户确认 → 飞书 Skill 执行
```

## 命令

| 命令 | 说明 |
|------|------|
| `/feishu-report` | 生成更新建议报告 |
| `/feishu-status` | 检查文档同步状态 |
| `/feishu-suggest <file> <type>` | 生成单个文件文档建议 |

## 执行命令

```bash
python3 {baseDir}/scripts/feishu_doc_manager.py "$PROJECT_DIR" <command> [args]
```

## 配置项

```bash
/set-config feishu.doc_token "doccnxxx"
/set-config feishu.folder_token "fldcnxxx"
/set-config feishu.wiki_token "wikcnxxx"
/set-config feishu.doc_url "https://xxx.feishu.cn/docx/xxx"
```

## 更新优先级

| 优先级 | 说明 | 示例 |
|--------|------|------|
| 🔴 高 | API 变更 | 接口参数变化 |
| 🟡 中 | 模块变更 | 功能修改 |
| 🟢 低 | 文档更新 | README 修改 |

## 变更类型

| 类型 | 说明 |
|------|------|
| `api_added` | 新增 API |
| `api_modified` | API 变更 |
| `module_added` | 新增模块 |

## 协作流程

1. 获取文档：`feishu_doc_fetch`
2. 生成建议：`/feishu-report`
3. 用户确认
4. 执行更新：`feishu_doc_update append`
5. 创建任务：`feishu_task_task create`