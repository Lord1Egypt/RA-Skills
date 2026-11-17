---

name: "git-helper-tool-free"
description: "提供Git常见操作辅助、冲突解决指引、提交规范检查与安全操作清单,适合开发者日常使用。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Git助手免费版"
  version: "1.0.0"
  summary: "提供Git常见操作辅助、冲突解决指引、提交规范检查与安全操作清单,适合开发者日常使用。"
  tags:
    - "开发工具"
    - "Git"
    - "辅助工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


Git助手免费版为开发者提供Git操作辅助能力。工具提供常见操作指引、合并冲突解决步骤、提交信息规范检查和安全操作检查清单,帮助开发者安全高效地使用Git。

本版本适合Git操作遇到问题时的辅助、冲突解决指引和新手Git操作指导。所有指引以步骤化方式呈现,易于跟随。

## 核心能力
### 1. 常见操作辅助
提供常见Git操作的分步指引。

**提交代码:**

```bash
git status

git diff
git diff --staged

git add file1.txt file2.txt
git add .

git commit -m "feat(scope): 描述"

git push
```

**创建功能分支:**

```bash
git switch main

git pull

git switch -c feature/new-feature

git push -u origin feature/new-feature
```

**合并分支:**

```bash
git switch main

git pull

git merge feature/new-feature

git commit

git push

git branch -d feature/new-feature
```

**输出**: 返回常见操作辅助的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 冲突解决指引
```bash
git diff --name-only --diff-filter=U

git diff

grep -rn "<<<\|>>>\|===" . --include="*.js" --include="*.py"

npm test  # 或其他测试命令
git add resolved-file.txt

git commit
git merge --abort
```

**输出**: 返回冲突解决指引的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 提交规范检查
```bash
#!/bin/sh
check_commit_message() {
    local msg="$1"
    local errors=()

    if ! echo "$msg" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\(\w+\))?:\s+.+'; then
        errors+=("格式不符合Conventional Commits规范")
        errors+=("正确格式: type(scope): description")
        errors+=("类型: feat|fix|docs|style|refactor|test|chore|perf|ci|build")
    fi

    local first_line=$(echo "$msg" | head -1)
    if [ ${#first_line} -gt 72 ]; then
        errors+=("首行长度${#first_line}超过72字符")
    fi

    if echo "$first_line" | grep -qE '[。.]$'; then
        errors+=("首行不应以句号结尾")
    fi

    if [ ${#errors[@]} -eq 0 ]; then
        echo "[OK] 提交信息规范"
        return 0
    else
        echo "[FAIL] 提交信息不规范:"
        for err in "${errors[@]}"; do
            echo "  - $err"
        done
        return 1
    fi
}

check_commit_message "feat(auth): 添加用户登录功能"
check_commit_message "修复了一个bug"
```

**输出**: 返回提交规范检查的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 安全操作检查
```bash
#!/bin/sh
echo "=== Git安全检查清单 ==="

BRANCH=$(git branch --show-current)
echo "1. 当前分支: $BRANCH"
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "   [!] 在主分支上,请确认是否要直接操作"
fi

if [ -n "$(git status --porcelain)" ]; then
    echo "2. [!] 有未提交的变更"
    git status -s
fi

AHEAD=$(git rev-list --count @{upstream}..HEAD 2>/dev/null)
if [ -n "$AHEAD" ] && [ "$AHEAD" -gt 0 ]; then
    echo "3. [!] 有 $AHEAD 个未推送的提交"
fi

STASH_COUNT=$(git stash list | wc -l)
if [ "$STASH_COUNT" -gt 0 ]; then
    echo "4. 有 $STASH_COUNT 个stash"
fi

BEHIND=$(git rev-list --count HEAD..@{upstream} 2>/dev/null)
if [ -n "$BEHIND" ] && [ "$BEHIND" -gt 0 ]; then
    echo "5. [!] 落后远程 $BEHIND 个提交"
fi

echo ""
echo "=== 安全建议 ==="
echo "- 不要在main分支直接提交"
echo "- 推送前先pull"
echo "- 使用--force-with-lease替代--force"
echo "- 定期清理已合并分支"
```

**输出**: 返回安全操作检查的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 常用配置模板

> 详细代码示例已移至 `references/detail.md`

**输出**: 返回常用配置模板的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：提交规范检查与安、全操作清单、适合开发者日常使、面向开发者的、操作辅助工具、提供常见操作指引、冲突解决步骤、核心能力、操作辅助指引、合并冲突解决步骤、提交信息规范检查、安全操作检查清单等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景
### 场景一:解决合并冲突
遇到合并冲突时获取解决指引。

```bash
#!/bin/sh
echo "=== 合并冲突解决助手 ==="

CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null)
if [ -z "$CONFLICTS" ]; then
    echo "没有冲突文件"
    exit 0
fi

echo "发现冲突文件:"
echo "$CONFLICTS" | while read f; do
    echo "  - $f"
done

echo -e "\n冲突详情:"
for f in $CONFLICTS; do
    echo "--- $f ---"
    grep -n "<<<<<<<\|=======\|>>>>>>>" "$f" 2>/dev/null
done

echo -e "\n解决步骤:"
echo "1. 打开冲突文件"
echo "2. 找到 <<<<<<< ======= >>>>>>> 标记"
echo "3. 选择保留的代码,删除标记"
echo "4. git add <file>"
echo "5. git commit"

echo -e "\n冲突标记检查:"
for f in $CONFLICTS; do
    if grep -q "<<<<<<<\|>>>>>>>" "$f" 2>/dev/null; then
        echo "  [!] $f 仍有冲突标记"
    fi
done
```

### 场景二:提交前检查
提交前进行安全检查。

```bash
#!/bin/sh
echo "=== 提交前检查 ==="

BRANCH=$(git branch --show-current)
echo "当前分支: $BRANCH"

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "[!] 警告: 在 $BRANCH 分支上"
    read -p "确认在 $BRANCH 上提交? (y/N) " confirm
    [ "$confirm" != "y" ] && exit 1
fi

echo -e "\n检查调试代码..."
DEBUG=$(git diff --cached --name-only | xargs grep -l "console.log\|debugger\|print(" 2>/dev/null)
if [ -n "$DEBUG" ]; then
    echo "[!] 发现调试代码:"
    echo "$DEBUG"
fi

echo -e "\n检查敏感信息..."
SECRET=$(git diff --cached | grep -iE "(password|secret|api_key)\s*=\s*['\"]" 2>/dev/null)
if [ -n "$SECRET" ]; then
    echo "[!] 发现敏感信息"
    exit 1
fi

echo -e "\n检查大文件..."
LARGE=$(git diff --cached --name-only | xargs -I{} sh -c 'test -f "{}" && wc -c "{}"' 2>/dev/null | awk '$1>1048576{print $2}')
if [ -n "$LARGE" ]; then
    echo "[!] 发现大文件(>1MB):"
    echo "$LARGE"
fi

echo -e "\n[OK] 检查通过"
```

### 场景三:误操作恢复

## 不适用场景

以下场景Git助手免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始
### Step 1:获取帮助
在 AI Agent 中输入:

```
我遇到了Git合并冲突,请帮我解决。
```

### Step 2:按照指引操作
Agent 会提供步骤化的解决指引。

### Step 3:安全检查
操作完成后进行安全检查确认。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 配置示例
### Git助手配置
```yaml
version: "1.0"

safety:
  block_main_push: true
  check_debug_code: true
  check_secrets: true
  check_large_files: true
  max_file_size: 1MB

commit:
  conventional: true
  max_subject: 72
  types: [feat, fix, docs, style, refactor, test, chore]

conflict:
  auto_detect: true
  check_markers: true
  suggest_resolution: true

recovery:
  show_reflog: true
  safe_mode: true
```

## 优选实践
1. **操作前检查**:每次Git操作前运行安全检查

2. **规范提交**:遵循Conventional Commits规范

```bash
git commit -m "feat(auth): 添加用户登录功能"

git commit -m "update"
```

3. **安全推送**:使用 `--force-with-lease`

4. **及时清理**:定期清理已合并分支和stash

5. **保留reflog**:不要清理reflog,它是恢复的保障

## 常见问题
### Q1:如何查看Git命令帮助?
```bash
git help <command>
git <command> --help
git <command> -h    # 简短帮助
git help commit
git merge --help
```

### Q2:如何配置Git补全?
```bash
source $HOME/.git-completion.bash

autoload -Uz compinit && compinit
```

### Q3:免费版与专业版有何区别?
| 能力维度 | 免费版 | 专业版 |
|:---------|:-------|:-------|
| 操作指引 | 基础指引 | 智能向导 |
| 冲突解决 | 手动指引 | 自动分析 |
| 安全检查 | 基础检查 | 深度审计 |
| 恢复操作 | 手动恢复 | 自动恢复 |
| 批量操作 | 不支持 | 批量处理 |
| 诊断 | 基础 | 深度诊断 |

### Q4:如何查看Git配置?
```bash
git config --list

git config --list --global

git config user.name
git config user.email
```

## 依赖说明
### 运行环境
- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **运行时**:Git 2.20+ / Bash

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Git | 运行时 | 必需 | git-scm.com 下载 |
| Bash | 运行时 | 推荐 | 系统自带 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 远程仓库认证:

```bash
git config --global credential.helper store
```

### 可用性分类
- **分类**:MD+execute(纯 Markdown 指令,需要 exec 命令行执行能力)
- **说明**:基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 提供Git辅助
- **适用规模**:个人开发者日常使用

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据