# 剪单短剧 Skill

剪单 AI 营销短剧创作平台官方 Agent Skill，用于指导 Codex、OpenClaw、TRAE 等智能体通过 `jd-drama` CLI 安全调用剪单短剧能力。

## 当前状态

- Skill 版本：`1.0.0-beta.6`
- CLI 包：`@flyengine/jd-drama-cli`
- 服务地址：[jiandan.flyengine.cn](https://jiandan.flyengine.cn/)
- 发布阶段：公开测试

公测版连接正式环境，会读取真实项目并使用真实创点。所有写操作都应先用 `--dry-run` 预览，再由用户明确同意后使用 `--confirm`。

## 支持能力

- 查询短剧项目、品牌和素材库。
- 根据创意或上传剧本创建短剧项目。
- 读取、替换、AI 校验、版本查询和恢复正式剧本分集。
- 对上传、AI 生成和二创剧本执行系统资产提取与深度解析，支持编辑和重新生成已有解析资产。
- 生成、查询、优化和修改分镜，支持 Seedance 2.5 拆分配置。
- 生成视频、检查任务进度，并将本地视频关联到分镜。
- 诊断失败任务并生成恢复建议。

## 安装 CLI

```bash
npm install -g @flyengine/jd-drama-cli@beta
jd-drama --version
```

## 安装 Skill

### Codex

```bash
jd-drama --json skill install --target codex --scope user --dry-run
jd-drama --json skill install --target codex --scope user --confirm
```

### OpenClaw

```bash
jd-drama --json skill install --target openclaw --scope user --dry-run
jd-drama --json skill install --target openclaw --scope user --confirm
```

### TRAE

在目标项目目录中执行：

```bash
jd-drama --json skill install --target trae --scope project --project-dir . --dry-run
jd-drama --json skill install --target trae --scope project --project-dir . --confirm
```

### WorkBuddy

在目标项目目录中执行诊断，并按返回提示同步 WorkBuddy harness：

```bash
jd-drama --json skill doctor --target workbuddy
```

也可以使用目标智能体提供的 GitHub Skill 安装能力，直接从本仓库安装根目录下的 `SKILL.md`。

## 网页授权

```bash
jd-drama auth login
jd-drama --json release-check
```

授权在剪单网页完成。不要向智能体提供剪单密码、手工复制的 Token、授权码或本地配置文件。

本机多个智能体通常共用一次网页授权。先检查 `jd-drama --json doctor`，仅在 `auth.browserAuthorization.needsLogin` 为 true 时登录。不要自动退出再登录：退出会撤销所有工具共用的授权。文件、钥匙串权限或网络异常应先按诊断处理后重试。缺少品牌与素材库权限时只需重新完成一次网页批准，无需先退出。

## 快速验证

```bash
jd-drama --json projects list --limit 10
jd-drama --json brands list --limit 10
jd-drama --json materials folders
jd-drama --json ai-script options
```

只预览创建计划，不写入数据：

```bash
jd-drama --json ai-script create \
  --idea "一支突出产品卖点的都市反转营销短剧" \
  --episode-count 1 \
  --name "CLI公测项目" \
  --generate \
  --dry-run
```

## 安全边界

- 智能体调用统一使用 `--json`。
- 写操作先用 `--dry-run`，确认后再使用 `--confirm`。
- 不通过原始接口绕过 CLI 的安全限制。
- 不泄露密码、授权码、本地配置文件或 Token。
- 不在重要的正式项目上测试删除和批量修改。
- 品牌只能在第一次创建项目时关联。
- 资产必须通过系统提取和解析生成，不得手工创建或绕过 CLI 调用接口。提取成功后才能深度解析，解析成功后再生成资产图片。深度解析可能消耗创点。
- 请同步升级本机所有 CLI/MCP 客户端；旧客户端的手工创建拦截需在配套后端部署后才生效。

完整智能体工作流见 [SKILL.md](./SKILL.md)。

## 使用许可

本仓库中的 Skill 文件按 [MIT-0 许可证](./LICENSE)发布。该许可证不适用于剪单服务、API、CLI 实现、商标、用户账号、额度或生成内容，具体边界见 [NOTICE](./NOTICE)。
