---
name: claude-config-generator
description: 为项目生成完整的 .claude 配置体系。通过问答引导生成 CLAUDE.md、settings.json、rules 等配置文件，并可从 ClawHub 安装 skills。
license: MIT
metadata:
  author: local
  version: "5.0"
---

为当前项目生成完善的 `.claude` 配置体系。

---

## 阶段 1：扫描项目

静默执行，无需交互：

1. 用 Glob 扫描目录结构（排除 `node_modules`、`.git`、`__pycache__`、`dist`、`build`）
2. 识别包管理器文件（`package.json` / `pyproject.toml` / `go.mod` / `pom.xml` / `Cargo.toml`）
3. 从包管理器中提取可用脚本/任务命令
4. 推断主要语言和项目类型
5. 读取已有的 `CLAUDE.md`（如存在）
6. 读取 `.claude/settings.json`（如存在）

---

## 阶段 2：安全敏感文件配置

用 **AskUserQuestion**（单选）询问：
- 是，配置安全敏感文件屏蔽
- 跳过

**若用户选择跳过** → 直接进入阶段 3。

**若用户选择是：**

根据阶段 1 扫描到的**目录结构和文件名**（不读取文件内容），自动推荐可能的敏感文件/目录。

推荐规则（按文件名/路径模式匹配，命中则加入推荐列表）：

| 模式 | 说明 |
|------|------|
| `.env` / `.env.*` | 环境变量文件 |
| `**/secrets/**` | secrets 目录 |
| `**/*.pem` / `**/*.key` / `**/*.jks` / `**/*.p12` | 证书与私钥 |
| `**/resources/application*.yml` / `**/resources/application*.yaml` / `**/resources/application*.properties` | Java/Spring 配置文件（可能含数据库密码、密钥等） |
| `**/resources/bootstrap*.yml` / `**/resources/bootstrap*.properties` | Spring Cloud 引导配置 |
| `**/application-prod.*` / `**/application-production.*` | 生产配置文件 |
| `**/terraform/*.tfvars` | Terraform 变量 |
| `**/k8s/prod/**` | 生产 K8s 配置 |
| `**/docker-compose.prod.*` | 生产 Docker 配置 |

将命中的路径整理为推荐列表，用 **AskUserQuestion**（多选）展示：

- 每个命中项作为一个选项，格式：`{路径模式}` — `{说明}`
- 最后一项：不屏蔽任何文件

> 若项目中未命中任何模式，仍展示常见选项（`.env`、secrets、证书）供用户选择。
> 若同时包含「不屏蔽任何文件」和其他项，忽略前者。

---

## 阶段 3：生成配置文件

### 3.1 创建目录骨架

先用 **Glob** 检查 `.claude/` 目录以及子目录是否已存在。若已存在完整结构（agents、commands、rules、skills 子目录均在），告知用户「目录骨架已存在，跳过创建」。否则仅创建缺失的目录：

```bash
mkdir -p .claude/agents .claude/commands .claude/rules .claude/skills
```

### 3.2 处理 CLAUDE.md

- 若已存在：不做任何修改，告知用户已跳过
- 若不存在：用 **AskUserQuestion** 询问「项目根目录缺少 CLAUDE.md，是否通过 `/init` 生成？」（是 / 否）
  - 用户确认后：使用 **Skill** 工具在前台执行 `/init`（`skill: "init"`），等待完成后再继续后续步骤
  - 用户拒绝则跳过

### 3.3 生成其余文件

已存在的文件跳过，`settings.json` 做深合并。

| 文件 | 内容 |
|------|------|
| `.claude/settings.json` | 根据包管理器填充 `permissions.allow`、根据用户选择填充 `permissions.deny`（敏感路径），其余字段留空骨架 |
| `.claude/settings.md` | settings.json 的字段说明 + 虚拟示例 |
| `.claude/README.md` | .claude 目录结构说明（各子目录用途、文件格式、settings.json 字段速查） |
| `.claude/rules/coding-standards.md` | 根据语言生成基础编码规范 |

生成完成后，展示目录结构预览，标注各文件状态（✓ 新建 / ✓ 已合并 / ⊘ 已跳过）。

---

## 阶段 4：Skills Hub

> 为项目添加 skills

### 步骤 1：本地 skills

用 **AskUserQuestion**（单选）询问：
- 是，从本地已有 skills 中选择
- 跳过

**若用户选择跳过** → 进入步骤 2。

**若用户选择是：**

1. 用 **Glob** 递归扫描以下路径下的所有 `SKILL.md`：
   - `~/.claude/skills/**/SKILL.md` — 用户自建 skills
   - `~/.claude/plugins/marketplaces/**/SKILL.md` — 市场安装的 skills（目录结构多样，必须用递归匹配）

   > 排除 `.gemini` 目录下的重复文件（与上层目录内容相同）

2. 读取每个 SKILL.md 的 frontmatter，提取 `name` 和 `description`，去重

3. 整理为表格展示。若总数超过 10 个，只展示前 10 个，并提示用户可输入 `more` 查看更多：

   ```
   本地可用 skills（共 N 个，显示前 10 个）：

   | # | 名称 | 描述 | 来源 |
   |---|------|------|------|
   | 1 | xxx  | xxx  | 自建 / 市场 |
   | ...
   | 10 | xxx | xxx | 自建 / 市场 |

   输入 "more" 查看更多。
   ```

   若总数不超过 10 个则全部展示。

4. 用 **AskUserQuestion** 询问：
   - 输入要添加的 skills 编号（Other 输入，多个用逗号分隔）
   - 查看更多（输入 `more`，继续展示下一批 10 个）
   - 不添加任何 skills

5. 用户选择后，将选中的 skills 目录复制到项目的 `.claude/skills/` 下（保持原目录结构）

---

### 步骤 2：ClawHub 在线安装

> 参考：`reference/clawhub.md`

用 **AskUserQuestion**（单选）询问：
- 是，从 ClawHub 搜索并安装更多 skills
- 跳过

**若用户选择跳过** → 直接进入阶段 5。

#### 前置检查

运行 `clawhub --version` 检查 CLI 是否已安装。若未安装，提示用户：

```
ClawHub CLI 未安装，是否现在安装？
执行：npm i -g clawhub
```

用 **AskUserQuestion** 确认后执行安装。若用户拒绝安装 CLI → 直接进入阶段 5。

### 推荐与搜索

1. 根据阶段 1 扫描到的**项目类型、语言、包管理器**，自动推荐 3~5 个搜索关键词（例如：Python 后端项目可推荐 `python`、`api`、`testing`、`security`、`devops`）

2. 对每个关键词执行 `clawhub search "{关键词}"`，汇总所有结果并去重

3. 整理为表格展示给用户：

   ```
   根据项目特征为你推荐以下 skills：

   | # | 名称 | 描述 |
   |---|------|------|
   | 1 | xxx  | xxx  |
   | ...
   ```

4. 用 **AskUserQuestion** 询问：
   - 输入要安装的 skills 编号（Other 输入，多个用逗号分隔）
   - 搜索更多 skills（通过 Other 输入自定义关键词）
   - 跳过，不安装任何 skills

5. 若用户选择安装：对每个选中的 skills 执行 `clawhub install {skill-name} --dir .claude/skills`

6. 若用户输入自定义关键词：执行 `clawhub search "{关键词}"`，展示结果，重复步骤 4

7. 安装完成后，询问是否继续搜索安装更多 skills，循环直到用户选择结束。

---

## 阶段 5：输出汇总

### 输出最终结果

1. **完整目录结构预览**：列出所有文件，标注状态（✓ 新建 / ✓ 已合并 / ⊘ 已跳过）
2. **已安装 skills 清单**：列出通过 ClawHub 安装的 skills 名称（若有）
3. **后续操作提示**：
   - 调整权限 → 编辑 `.claude/settings.json`
   - 新增规则 → 在 `.claude/rules/` 添加 `.md` 文件
   - 新增命令 → 在 `.claude/commands/` 添加 `.md` 文件
   - 浏览更多 skills → 访问 https://clawhub.ai/skills

---

## 防呆检查（全局约束）

写入任何文件之前必须遵守：

1. **CLAUDE.md**：已存在则不做任何修改，直接跳过
2. **settings.json**：已存在则读取后做 JSON 深合并，不直接覆盖
3. **其余文件**：已存在则跳过
4. **写入验证**：写入后用 Read 验证内容正确
5. **密钥禁令**：严禁在任何配置文件中写入 API Key、密码等密钥
