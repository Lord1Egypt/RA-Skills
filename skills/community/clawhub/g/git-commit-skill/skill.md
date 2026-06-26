# Git Commit 生成器

根据当前分支改动生成 git commit 内容，分阶段确认后再提交代码。

## 使用方式

用户输入：`/git-commit`

Skill 会**自动分析**当前分支的改动内容，智能推断并选择最合适的 Gitmoji 类型。

---

## 执行流程

### 阶段 1：分析改动并自动推断 Gitmoji

执行命令分析当前工作状态：

```bash
# 查看工作状态
git status

# 查看未暂存的改动内容
git diff

# 如果已有暂存文件，也查看暂存的改动
git diff --cached
```

**输出改动点列表**，按**功能模块**分组展示：

```
【当前分支改动分析】

改动的文件：
- src/main/java/UserService.java
- src/test/java/UserServiceTest.java
- src/main/java/UserController.java

改动点总结（按功能归类）：
1. 新增用户管理模块（UserService、UserController）
2. 补充用户管理模块单元测试（UserServiceTest）

【推断的提交类型】:sparkles: 新功能
```

**归类原则**：
- 同一功能/需求涉及的多个文件改动，合并为一条
- 主代码 + 对应测试文件，如测试是配套新增的，可合并
- 跨模块的改动，按模块分组

**等待用户确认**：
- 询问用户改动点是否准确
- 用户可以要求修改改动点
- 如自动推断的 Gitmoji 不合适，用户可以指定其他类型
- 用户确认无误后，进入下一阶段

---

### 阶段 1.5：安全检查（关键）

**在生成 commit message 之前，必须检查改动中是否包含敏感信息。**

#### 敏感文件类型检查

如改动包含以下文件，**必须暂停并提醒用户**：

| 文件类型 | 风险 | 示例 |
|----------|------|------|
| 环境变量 | 🔴 | `.env`, `.env.local`, `.env.production` |
| 凭证文件 | 🔴 | `credentials`, `credentials.json`, `service-account.json` |
| 私钥证书 | 🔴 | `*.pem`, `*.key`, `*.p12`, `id_rsa`, `id_ed25519` |
| AWS 配置 | 🔴 | `.aws/credentials`, `aws_config` |
| 数据库配置 | 🔴 | `database.yml`, `config.json`（含密码） |
| Git 凭证 | 🔴 | `.git-credentials`, `.git-creds` |
| 其他敏感 | 🟡 | `*password*`, `*secret*`, `*token*`（文件名） |

#### 敏感代码模式检查

检查 `git diff` 内容是否包含以下模式：

```
🔴 高危模式（发现则必须警告）：
- password = "xxx" / password: "xxx"
- secret = "xxx" / secret_key = "xxx"
- api_key = "xxx" / apiKey = "xxx"
- token = "xxx"（长字符串）
- private_key = "xxx"
- aws_access_key / aws_secret_key
- 数据库连接串（含密码）：mongodb://user:pass@
- DB_PASSWORD, MYSQL_PASSWORD, REDIS_PASSWORD 等

🟡 中危模式（建议提醒）：
- 硬编码的邮箱 + 密码组合
- base64 编码的长字符串
- URL 含敏感查询参数
```

#### 发现敏感信息时的处理流程

```
⚠️ 警告：检测到可能的敏感信息

【检测到的内容】
- 文件：.env
- 改动：DB_PASSWORD=MyPassword123

【风险】
提交此文件到公网可能导致：
- 数据库被未授权访问
- 敏感数据泄露
- 账号被盗用

【建议操作】
1. 确认此文件是否已添加到 .gitignore
2. 如未添加，执行：echo ".env" >> .gitignore
3. 移除已暂存：git reset .env
4. 使用环境变量或密钥管理服务

是否确认继续提交？(是/否)
```

**只有用户明确确认后，才能进入阶段 2。**

---

### 阶段 2：生成 commit message 并确认

根据确认后的改动点和自动推断的 Gitmoji 生成 commit message：

**格式**：
```
:emoji-name: <改动点总结>

1. <改动点 1>
2. <改动点 2>
3. <改动点 3>
```

**示例**（新功能）：
```
:sparkles: 新增用户管理模块

1. 新增 UserService 处理用户业务逻辑（注册、登录、权限校验）
2. 新增 UserController 提供 REST API 接口
3. 新增 UserDTO 和 UserVO 数据传输对象
4. 补充单元测试覆盖核心功能
```

**示例**（Bug 修复）：
```
:bug: 修复用户登录验证问题

1. 修复 Token 过期导致的登录失败
2. 添加登录失败次数限制
```

**示例**（综合改动）：
```
:sparkles: 新增数据导出功能并优化性能

1. 新增 ExportService 支持 Excel/CSV 格式导出
2. 优化大数据量查询使用游标分页
3. 添加导出任务异步处理机制
4. :arrow_up: 升级 easyexcel 到 3.3.0
5. :white_check_mark: 补充导出功能单元测试
```

**展示 commit message 并等待用户确认**：

展示生成的 commit message 后，**必须使用 AskUserQuestion 工具**给用户 Yes/No 选择：

```
【生成的 commit message】
:sparkles: 新增用户管理模块

1. 新增 UserService 处理用户业务逻辑
2. 新增 UserController 提供 REST API 接口
3. 补充单元测试覆盖核心功能

请确认此 commit message 是否正确？
- Yes: 使用此 message，继续执行提交
- No: 我将手动输入改动点描述
```

**用户选择处理**：

1. **如果用户选择 Yes**：使用生成的 commit message，进入阶段 3
2. **如果用户选择 No**：请用户输入想要的描述，重新生成后再次确认

**重要**：在用户确认 commit message 之前，不要执行任何 git add 或 git commit 命令。

---

### 阶段 3：执行 git add 暂存

用户确认 commit message 后，执行暂存：

```bash
git add -A
```

或者根据用户需求暂存特定文件：
```bash
git add <file1> <file2>
```

暂存后展示已暂存的文件列表，等待用户确认是否继续提交。

---

### 阶段 4：执行 git commit 提交

用户确认暂存文件无误后，执行提交：

```bash
git commit -m "<commit message>"
```

提交后展示结果：
- 提交是否成功
- 提交的简要信息（分支、文件数、commit hash 等）

---

### 阶段 5：询问是否推送到远程（可选）

提交成功后，询问用户：

```
提交成功！是否推送到远程仓库？

【推送信息】
分支：<current-branch>
远程：origin

请确认是否执行 git push？(是/否)
```

用户确认后执行：
```bash
git push origin <current-branch>
```

如果远程分支不存在，提示用户设置上游分支：
```bash
git push -u origin <current-branch>
```

---

## Gitmoji 自动映射规则

根据改动特征自动选择最合适的 Gitmoji：

| 改动特征 | Shortcode | 说明 |
|----------|-----------|------|
| 新增功能、模块、接口 | `:sparkles:` | 新功能 |
| 修复 bug、错误 | `:bug:` | Bug 修复 |
| 紧急线上修复 | `:ambulance:` | 紧急热修复 |
| 文档、README、注释 | `:memo:` | 文档 |
| 代码重构、逻辑优化 | `:recycle:` | 重构 |
| 删除代码/文件 | `:fire:` | 删除 |
| UI、样式文件 | `:lipstick:` | UI 样式 |
| 部署、上线 | `:rocket:` | 部署 |
| 测试用例 | `:white_check_mark:` | 测试 |
| 安全漏洞修复 | `:lock:` | 安全 |
| 编译器/linter 警告 | `:rotating_light:` | 警告 |
| CI/CD 配置 | `:construction_worker:` | CI 系统 |
| CI 构建修复 | `:green_heart:` | CI 修复 |
| 依赖升级 | `:arrow_up:` | 升级 |
| 依赖降级 | `:arrow_down:` | 降级 |
| 新增依赖 | `:heavy_plus_sign:` | 添加依赖 |
| 移除依赖 | `:heavy_minus_sign:` | 删除依赖 |
| 配置文件 | `:wrench:` | 配置 |
| 脚本文件 | `:hammer:` | 脚本 |
| 编译文件/包 | `:package:` | 包 |
| 代码格式/结构 | `:art:` | 代码结构 |
| 性能优化 | `:zap:` | 性能 |
| 破坏性变更 | `:boom:` | 破坏性变更 |
| 回滚 | `:rewind:` | 回滚 |
| 国际化 | `:globe_with_meridians:` | i18n |
| 无法明确判断 | `:sparkles:` | 默认新功能 |

> **完整 Gitmoji 参考**：见 [`references/gitmojis.md`](references/gitmojis.md)

---

## 注意事项

- **分阶段确认**：每个阶段都等待用户确认后再继续
- **安全检查必须执行**：阶段 1.5 必须检查敏感文件和敏感代码模式
- **无改动处理**：如工作目录干净，告知用户没有待提交的改动
- **灵活调整**：用户可以在任何阶段要求修改或取消
- **Gitmoji 格式**：使用 `:name:` 格式（如 `:sparkles:`），在 GitHub/GitLab 会自动渲染为 emoji
