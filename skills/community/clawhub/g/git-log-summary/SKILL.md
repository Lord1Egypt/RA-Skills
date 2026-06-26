---
name: git-log-summary
description: 生成Markdown格式的Git提交记录摘要报告。使用场景：当用户需要按照Markdown格式输出git仓库的详细统计信息时使用此技能。输出内容包括：项目信息、分支信息、提交统计、作者统计、最近提交记录、分支信息和提交类型统计等，全部以标准Markdown格式呈现。
license: MIT
author: 夕阳下的池塘
version: 1.0.0
---

# Git Log Summary Skill (Markdown格式)

此技能用于生成Markdown格式的Git提交记录摘要报告，适合文档化、分享和在线阅读。

## 快速开始

### 基本用法

生成当前git仓库的Markdown格式提交记录摘要：

```bash
./scripts/generate_git_summary.sh
```

### 输出格式示例

```markdown
# 项目名 Git提交记录摘要

## 报告信息
- **生成时间**: 2026-03-25 20:03:35
- **仓库路径**: `/path/to/repository`
- **仓库基本信息**:
  - **Git版本**: 2.39.5
  - **仓库创建时间**: 2026-03-05
  - **最后提交时间**: 2026-03-25

## 分支信息
### 当前分支
`master`

### 远程仓库
- origin https://example.com/repo.git (fetch)
- origin https://example.com/repo.git (push)

## 提交统计
### 总提交数
**总提交数**: 30

### 按作者统计
| 作者 | 提交次数 | 占比 |
|------|----------|------|
| user1 | 21 | 70.00% |
| user2 | 7 | 23.33% |

## 最近提交记录
显示最近 20 条提交记录：

| Commit Hash | 作者 | 提交时间 | 提交日志 |
|-------------|------|----------|----------|
| abc123 | user1 | 3 hours ago | feat: 新增功能 |
| def456 | user2 | 5 hours ago | fix: 修复问题 |

## 所有分支
### 本地分支
- master
- feature-branch

### 远程分支
- origin/HEAD
- origin/master

## 提交类型统计
基于最近1000条提交信息的类型分析：

| 类型 | 数量 | 占比 | 说明 |
|------|------|------|------|
| feat | 27 | 90.0% | 新功能 |
| fix | 2 | 6.7% | Bug修复 |

---
*报告生成完成*
```

## 脚本功能

### 主要脚本

`scripts/generate_git_summary.sh` - Markdown格式脚本，生成完整的git提交记录摘要

#### 功能特性

1. **项目信息提取**：
   - 自动获取项目名称（从git remote或目录名）
   - 获取仓库路径和基本信息
   - 记录生成时间

2. **分支信息**：
   - 当前分支
   - 远程仓库信息
   - 所有分支列表

3. **提交统计**：
   - 总提交数
   - 按作者统计提交次数和占比（Markdown表格格式）
   - 提交类型统计（feat, fix, merge等）

4. **详细提交记录**：
   - 最近提交的详细记录（Markdown表格格式）
   - 格式化输出：Commit Hash | 作者 | 提交时间 | 提交日志

5. **提交类型分析**：
   - 自动分析提交信息中的类型前缀
   - 统计各类提交的数量和占比
   - 提供类型说明

### 使用示例

```bash
# 生成默认报告（自动保存为 项目名-git-log-年月日-时分秒.md）
./scripts/generate_git_summary.sh

# 指定输出文件
./scripts/generate_git_summary.sh -o custom-report.md

# 限制最近提交数量
./scripts/generate_git_summary.sh -n 20

# 包含所有分支的统计
./scripts/generate_git_summary.sh -a

# 组合使用
./scripts/generate_git_summary.sh -n 15 -a
```

### 自动文件名格式

当不指定`-o`参数时，脚本会自动生成文件名：
```
项目名-git-log-年月日-时分秒.md
```

示例：
```
long-shop-git-log-20260325-203045.md
```

文件名组成：
- **项目名**: 从git remote或目录名自动提取
- **git-log**: 固定标识
- **年月日**: 报告生成日期（如20260325）
- **时分秒**: 报告生成时间（如203045）

## 远程仓库分析

### 远程分析脚本

`scripts/generate_git_summary_remote.sh` - 专门用于分析远程Git仓库

#### 功能特性
1. **自动克隆**: 自动克隆远程仓库到临时目录
2. **保留报告**: 生成报告后保留报告文件
3. **可选保留**: 可选择保留或删除克隆的仓库
4. **完整分析**: 包含所有本地分析功能

### 远程仓库使用示例

```bash
# 分析远程仓库（自动生成报告文件）
./scripts/generate_git_summary_remote.sh -u https://gitee.com/forever_1236/long-shop.git

# 指定输出文件
./scripts/generate_git_summary_remote.sh -u https://gitee.com/user/repo.git -o my-report.md

# 保留克隆的仓库目录
./scripts/generate_git_summary_remote.sh -u https://github.com/user/repo.git -k

# 组合使用
./scripts/generate_git_summary_remote.sh -u https://gitee.com/user/repo.git -n 30 -a -o report.md
```

## 脚本参数

### 本地分析脚本 (`generate_git_summary.sh`)
- `-o, --output <file>`: 指定输出文件（默认自动生成：项目名-git-log-年月日-时分秒.md）
- `-n, --num-commits <number>`: 指定显示的最近提交数量（默认20）
- `-a, --all-branches`: 包含所有分支的统计（默认只统计当前分支）
- `-h, --help`: 显示帮助信息

### 远程分析脚本 (`generate_git_summary_remote.sh`)
- `-u, --url <url>`: 远程Git仓库URL（必需）
- `-o, --output <file>`: 指定输出文件（默认自动生成）
- `-n, --num-commits <number>`: 指定显示的最近提交数量（默认20）
- `-a, --all-branches`: 包含所有分支的统计（默认只统计当前分支）
- `-k, --keep-clone`: 保留克隆的仓库目录（默认不保留）
- `-h, --help`: 显示帮助信息

## 提交类型识别

脚本会自动识别以下提交类型：
- `feat`: 新功能
- `fix`: Bug修复
- `merge`: 合并分支
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动
- `perf`: 性能优化
- `ci`: CI/CD相关
- `build`: 构建系统
- `revert`: 回退提交

## 注意事项

1. **确保在git仓库中**: 脚本必须在git仓库目录下运行
2. **git版本**: 需要git 1.8.0或更高版本
3. **权限**: 需要读取git配置和提交历史的权限
4. **大型仓库**: 对于大型仓库，统计所有提交可能需要较长时间

## 故障排除

### 常见问题

1. **"错误：当前目录不是git仓库"**:
   - 确保当前目录是git仓库
   - 运行 `git init` 初始化新仓库

2. **统计不准确**:
   - 运行 `git fetch --all` 更新远程分支信息
   - 使用 `-a` 参数包含所有分支统计

3. **提交类型识别错误**:
   - 检查提交信息是否符合约定格式（如 "feat: 添加新功能"）
   - 调整脚本中的类型匹配规则

### 性能优化

对于大型仓库：
- 使用 `-n` 参数限制最近提交数量
- 避免使用 `-a` 参数除非必要
- 考虑使用 `git log --since` 限制时间范围
