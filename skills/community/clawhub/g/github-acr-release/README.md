# GitHub + ACR 全周期发布管控

> 适用于任何语言（Python / Go / Rust / Node / Java…）的 Docker 化项目。

## 这个 Skill 能做什么

从"搭建发布流"到"发布后验证+下版本规划"，一条流水线管到底：

- **交互式配置**：问答式收集项目信息（版本管理、构建、ACR、服务器）
- **可持续性评分**：发布前检查项目健康度，列出缺失项和风险
- **版本一致性检测**：扫描所有版本号源，确保一致
- **标准发布流程**：13 步完整覆盖（流前→发布→流后）
- **热更新**：快速修复发布，跳过版本号变更
- **下版本规划**：发布完成后自动询问是否创建下一版本

## 适用场景

- GitHub + 阿里云 ACR 的 Docker 镜像发布
- 任何语言的容器化项目
- 需要版本管理 + CHANGELOG + 远程部署的项目
- 多人协作需要标准化发布流程的团队

## 核心概念

### 项目结构约定

```
{project-name}-v{X.Y.Z}/
├── {source}/                     ← 源码目录（可配置）
├── data/VERSIONS.json            ← 版本元数据（基石）
├── Dockerfile
├── docker-compose.yml
├── scripts/                      ← 工具脚本
└── .github/workflows/ci.yml
```

### VERSIONS.json 结构

```json
{
  "current": {
    "version": "X.Y.Z",
    "date": "YYYY-MM-DD",
    "notes": "描述",
    "data_version": 1,
    "digest": ""
  },
  "changelog": [
    {
      "version": "X.Y.Z",
      "date": "YYYY-MM-DD",
      "notes": "描述",
      "detail": {
        "sections": [
          { "type": "Added / 新增", "items": ["功能A"] },
          { "type": "Fixed / 修复", "items": [] }
        ]
      }
    }
  ]
}
```

## 使用方式

### 触发词

| 你说 | Skill 执行 |
|------|-----------|
| `新建发布流程` / `搭建发布流` | 交互式问询 → 生成配置 → 初始化骨架 |
| `检查` / `检查发布` | 仅流前检查（不发布） |
| `发布` / `发版` / `push` | 标准完整发布 |
| `热更新` / `hotfix` | 快速修复发布 |
| `下个版本` / `下版本` | 版本规划对话 |
| `检查项目` | 可持续性评分 + 缺失项报告 |

### 13 步发布流程

**阶段 A：发布流前**
- Step 0: 版本分支创建
- Step 1: 版本号一致性检查
- Step 2: 代码基线检查（按语言）
- Step 3: 可持续性评分
- Step 4: 预发布确认

**阶段 B：发布流**
- Step 5: 更新 VERSIONS.json
- Step 6: 编译前端（若有）
- Step 7: git commit + push
- Step 8: git tag + GitHub Actions 自动构建
- Step 9: 远程服务器部署（若有）

**阶段 C：发布流后**
- Step 10: 远端验证
- Step 11: 镜像 digest 同步
- Step 12: 环境清理
- Step 13: 收尾 + 下版本规划

## 可持续性评分

发布前自动检查项目健康度，评分项目包括：

| 类别 | 检查项 | 级别 |
|------|--------|------|
| 骨架 | Dockerfile、docker-compose、.gitignore | ⚠️ 建议 |
| 版本 | VERSIONS.json、版本号一致性、版本文件 | ❌ 必须 |
| 数据 | 配置备份、数据迁移、数据版本号 | ⚠️ 建议 |
| 运维 | 启动检查、一致性脚本、冒烟测试、验证脚本 | ⚠️ 建议 |
| 测试 | 模块测试、单元测试 | ⭐ 可选 |

## 脚本模板

Skill 可生成以下脚本到项目 `scripts/` 目录：

- `check_version_consistency.py` — 版本一致性检测
- `smoke_test.py` — API 冒烟测试
- `post_deploy_verify.py` — 发布后远程验证
- `full_release_check.py` — 一键综合检查

所有脚本模板变量从项目配置中自动替换。

## 版本管理规则

1. 新建版本 → 完整复制 data/（含 VERSIONS.json）
2. 只改 current.version + current.date
3. changelog 历史绝不动
4. 同版本多条记录合并为一条
5. 新版本条目先空着，等实际更新再填

## 常用命令

```bash
# 流前全检
python3 scripts/full_release_check.py

# 版本一致性检查
python3 scripts/check_version_consistency.py

# API 冒烟测试
python3 scripts/smoke_test.py --base-url http://localhost:PORT

# 发布后验证
python3 scripts/post_deploy_verify.py --target HOST --ssh
```

## 注意事项

- 敏感信息必须脱敏
- 版本号一致性必须检查
- 所有对外操作必须经用户确认
- 数据迁移走备份→验证→回滚机制
