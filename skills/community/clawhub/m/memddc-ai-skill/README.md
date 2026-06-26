# memddc-ai-skill

> [English Version](README_EN.md)

## 一句话理解

MemDDC = 给代码做体检（初始化）→ 记录病历（快照）→ AI 医生快速诊断

## 核心能力

| 能力 | 说明 |
|------|------|
| **项目扫描** | 首次使用自动扫描全量代码，生成项目文档 |
| **三级索引** | metadata/index/context 结构，快速定位文件 |
| **关联映射** | entity→mapper→service→controller→view，按 ID 查表 |
| **DDD约束** | 修改必须符合领域模型和业务契约 |
| **VCS分析** | 自动分析 Git 提交规律，了解团队协作模式 |
| **Token节省** | 实测复杂业务修改节省 53% Token 消耗 |

## 触发关键词

```
MemDDC, 加载记忆约束修改, 按DDD契约迭代更新, memddc-init, memddc-update, memddc-sync
```

## 工作流程

### 1. 初始化 (memddc-init)

扫描项目 → 生成文档 → 构建 mem-snapshot.json（三级索引 + 关联映射）

### 2. 代码修改

读取 mem-snapshot.json → 查询 index 定位文件 → 按 DDD 约束修改 → 同步文档

### 3. 增量同步 (memddc-sync)

git diff → 分析变更范围 → 精准更新受影响文档 → 更新快照

## mem-snapshot.json 结构

```json
{
  "metadata": { "name": "RuoYi-Vue", "version": "1.0", "tech": "Java+Spring Boot" },
  "index": {
    "entities": { "SysDept": { "path": ".../SysDept.java", "module": "system" } },
    "relations": {
      "SysDept": {
        "entity": ".../SysDept.java",
        "mapper": ".../SysDeptMapper.xml",
        "service": ".../SysDeptServiceImpl.java",
        "controller": ".../SysDeptController.java",
        "views": [".../dept/index.vue"]
      }
    }
  },
  "context": {
    "patterns": ["treeBuild", "pagination", "crudApi"],
    "codeStyle": { "returnType": "AjaxResult", "annotation": "@RestController" }
  }
}
```

## 实战效果

RuoYi-Vue 前后端分离项目实测：

| 场景 | 使用MemDDC | 不使用 | 节省 |
|------|-----------|--------|------|
| 项目说明生成 | ~49,000 token | ~77,000 token | **36%** |
| 业务功能修改 | ~18,000 token | ~38,000 token | **53%** |
| 对话轮数 | 4轮 | 6-10轮 | **60%** |

## 目录结构

```
project/
├── .memddc/
│   ├── mem-snapshot.json       # 三级索引快照
│   ├── vcs-log-analysis.md    # VCS日志分析
│   ├── file-tree-analysis.md  # 文件结构分析
│   └── docs/                  # 项目文档
│       ├── architecture.md
│       ├── ddd-model.md
│       └── api.md
└── [项目源码]
```

## 在线体验

想了解 v1.0.2 版本的完整初始化效果？查看示例项目 [example/RuoYi-Vue](example/RuoYi-Vue/.memddc/)：

| 文件 | 说明 |
|------|------|
| [mem-snapshot.json](example/RuoYi-Vue/.memddc/mem-snapshot.json) | 完整的三级索引快照（25KB，含13个实体、15个Controller） |
| [config.json](example/RuoYi-Vue/.memddc/config.json) | 团队共享配置 |
| [ddd-model.md](example/RuoYi-Vue/.memddc/ddd-model.md) | DDD领域模型（5个限界上下文） |
| [init-report-20260402.md](example/RuoYi-Vue/.memddc/docs/init-report-20260402.md) | 初始化报告（Token消耗分析、流程详解） |
| [vcs-log-analysis.md](example/RuoYi-Vue/.memddc/vcs-log-analysis.md) | Git提交规律分析 |
| [docs/](example/RuoYi-Vue/.memddc/docs/) | 自动生成的项目文档（含架构图、业务文档、API文档等） |

> **示例项目说明**：RuoYi-Vue 是基于 SpringBoot+Vue 的前后端分离快速开发平台，包含 220 个 Java 文件、65 个 Vue 文件、22 个 XML Mapper，通过 MemDDC 初始化后生成完整项目知识库。

## 适用场景

- **团队协作**: 统一文档，新成员快速上手
- **复杂架构**: DDD 约束，避免野蛮修改
- **遗留系统**: 完整文档辅助重构
- **长期维护**: 记录决策历史，理解设计意图

## 技术栈支持

| 语言/框架 | 文档生成 | DDD建模 | 记忆压缩 |
|-----------|---------|---------|----------|
| Java/Spring | ✅ | ✅ | ✅ |
| Python/Django | ✅ | ✅ | ✅ |
| Go/Gin | ✅ | ✅ | ✅ |
| Vue/React | ✅ | ⚠️ | ✅ |

## 版本

- **v1.0.2** (当前): 三级索引 + 关联映射 + VCS分析
- **v1.0.1**: 团队协作 + 智能触发

## 链接

- GitHub: <https://github.com/qihao123/memddc-ai-skill>
- Email: <qihoo2017@gmail.com>
