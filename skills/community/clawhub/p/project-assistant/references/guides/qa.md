# 问答文档管理指南

## 命令

| 命令 | 说明 |
|------|------|
| `/search-qa <关键词>` | 搜索历史问答 |
| `/list-qa [分类]` | 列出问答文档 |
| `/check-qa` | 检查文档是否过期 |
| `/delete-qa <id>` | 删除问答文档 |

## 执行命令

```bash
python3 {baseDir}/scripts/qa_doc_manager.py "$PROJECT_DIR" <command> [args]
```

## 文档分类

| 分类 | 说明 |
|------|------|
| `architecture` | 架构设计 |
| `build` | 构建配置 |
| `feature` | 功能实现 |
| `debug` | 问题调试 |
| `api` | 接口说明 |
| `module` | 模块说明 |
| `process` | 流程说明 |
| `other` | 其他 |

## 文档结构

```
项目目录/.claude/
├── index/qa_index.json    # 问答索引
└── docs/qa/               # 问答文档
    ├── architecture/
    ├── build/
    ├── feature/
    ├── debug/
    ├── api/
    ├── module/
    ├── process/
    └── other/
```

## 过期检测

自动检测两种过期情况：
1. **Git Commit 变化** - 代码有新提交
2. **文件哈希变化** - 相关文件被修改

## 示例

```bash
# 搜索 WiFi 相关问答
/search-qa WiFi

# 列出架构类问答
/list-qa architecture

# 检查文档过期
/check-qa
```