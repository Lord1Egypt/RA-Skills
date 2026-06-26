# ClawHub 过审 Checklist

发布任何 OpenClaw 技能前，先逐项自查。目标不是“差不多”，而是**元数据、文档、实现三层完全一致**。

## 1. 元数据一致性

核对以下文件是否口径一致：

- `SKILL.md` frontmatter
- `package.json`
- `README.md`
- 实际脚本 / 代码

重点检查：

- `name`
- `description`
- `version`
- `homepage`
- `requires.bins`
- `requires.env`
- `primaryEnv`
- `clawhub.credentials`

## 2. 依赖声明

如果代码或文档里实际用到了这些东西，就必须声明：

- CLI 工具：如 `mcporter` / `git` / `gh` / `ffmpeg`
- 环境变量 / 凭证：如 `DINGTALK_MCP_DOCS_URL`
- 外部服务 URL / token

原则：**真实依赖了什么，就声明什么，不要少报。**

## 3. 凭证说明

如果 skill 需要 token / URL / key，必须写清：

- 凭证名字是什么
- 从哪获取
- 怎么配置
- 推荐存哪里
- 是否属于敏感信息

正文里最好明确：

- 推荐配置方式
- 备用配置方式
- 安全提醒

## 4. Instruction Scope 一致

文档里教用户做的事，不能超出代码真实边界。

重点排查：

- 文档是否让用户读 / 写某些本地文件
- 代码是否只允许 workspace 内路径
- 文档是否写了工作区外路径
- 文档是否暗示了代码并不支持的行为

原则：**文档、脚本、安全限制必须一致。**

## 5. 示例参数必须和真实实现一致

重点核对：

- 参数名大小写
- ID 格式
- URL 格式
- JSON 结构
- 返回值字段名

避免出现“README 看起来能用，复制后跑不通”。

## 6. 本地文件行为要明写

只要脚本会碰本地文件，就明确写清：

- 会读取什么文件
- 会输出什么文件
- 允许哪些扩展名
- 路径限制是什么
- 是否有限制大小
- 是否直接联网

## 7. 安装机制透明

如果需要外部工具：

- 写安装命令
- 写验证命令
- 不要偷偷依赖没声明的 CLI

## 8. 发布闭环

每次发布必须完整走完：

1. 更新版本号
2. 更新 `CHANGELOG.md`
3. `git add` / `commit`
4. `git push`
5. 创建 GitHub Release
6. 发布到 ClawHub
7. 同步到 `~/.openclaw/workspace/skills/<skill>/SKILL.md`

## 9. 测试最小集

至少覆盖：

- 路径安全
- 参数格式 / ID 格式
- 核心 happy path

如果改了安全逻辑，必须跑测试，不要只改文档。

## 10. 安全审查补充

重点新增这几类自查：

- description 不得包含机器本地目录路径（如 `~/Skills`、`~/.openclaw/workspace`）
- 不得推荐 TLS / 证书校验绕过命令（如 `NODE_TLS_REJECT_UNAUTHORIZED=0`）
- 不得把读取本地凭证文件内容作为常规排障步骤（如直接 `cat` token 文件）
- 对 agent 工作区或其他敏感目录的写操作，必须明确标注为受信任环境下的显式操作

## 11. 发版前最后一轮 grep

重点搜这些高风险词：

- `~/workspace`
- `~/Skills`
- `UUID v4`
- `NODE_TLS_REJECT_UNAUTHORIZED=0`
- `config.json`
- 旧版本号
- 未声明的 env 名
- 未声明的 CLI 名
- 旧参数名 / 旧接口名

## 三问自检

发版前最后问自己：

1. **我文档里写的，代码真能这么干吗？**
2. **我代码真实依赖的东西，元数据都声明了吗？**
3. **用户照 README 复制，真能跑通吗？**

只要其中一个答不上来，就先别发。
