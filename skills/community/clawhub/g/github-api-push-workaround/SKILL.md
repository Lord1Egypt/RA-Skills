---
name: github-api-push-workaround
description: "git 推 GitHub/Gitee/AtomGit 的根因化排查与推送模板：401=凭据问题（helper 链残留死旧 PAT）、超时/挂死=通道问题（代理掐 git 传输，须 no_proxy 直连）、大面积 401=取值前缀坑（--raw 取裸值）。含直连推送模板（令牌走环境变量）、Git Data API 兜底（blob→tree→commit→ref）、Gitee 私有转公开、AtomGit 后端 gitcode 等实测坑。当用户说'推 GitHub'、'git push 失败/401/超时'、'发布仓库到远端'、'令牌失效了'时使用。"
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.2.1
agent_created: true
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch
category: 开发效率
platforms: [windows, macos, linux]
tags: [github, git-push, 代理, 凭据, 排查, 发布, gitee, atomgit]
description_zh: "git 推 GitHub/Gitee/AtomGit 的根因化排查与推送模板：401=凭据问题（helper 链残留死旧 PAT）、超时/挂死=通道问题（代理掐 git 传输，须 no_proxy 直连）、大面积 401=取值前缀坑（--raw 取裸值）。含直连推送模板（令牌走环境变量）、Git Data API 兜底（blob→tree→commit→ref）、Gitee 私有转公开、AtomGit 后端 gitcode 等实测坑。当用户说'推 GitHub'、'git push 失败/401/超时'、'发布仓库到远端'、'令牌失效了'时使用。"
description_en: "Root-cause troubleshooting and push templates for git remotes (GitHub/Gitee/AtomGit): 401 means credentials, timeout means channel, with no_proxy and API-fallback patterns."
classification:
  internal: ["cross-domain utility (pending categorization)"]
  skillhub: ["productivity"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
slug: github-api-push-workaround
read_when:
  - git push 报 401（令牌失效/凭据残留）要根因排查
  - git 推送超时/挂死，疑似代理掐了 git 传输要 no_proxy 直连
  - 大面积 401 要查取值前缀坑（--raw 取裸值）
  - 要用 Git Data API 兜底（blob→tree→commit→ref）推复杂对象
ai_protocol: true

---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
When the user reports `git push` failing with 401 (expired token / leftover credentials), request timeouts or network hangs — for root-cause troubleshooting. When publishing repositories to GitHub / Gitee / AtomGit, pushing to a remote, or flipping a private repo to public. When a wave of 401s points to the value-prefix pitfall (`--raw`), or when using env-var token direct-push. When the Git Data API fallback (blob→tree→commit→ref) is needed for complex object pushes.

### Usage
This is a document-style skill with no external script; the user triggers it by keywords in natural language and gets the matching troubleshooting guide and code templates. The system identifies the target platform, the auth-token source and the network config, then generates direct-push commands or API-call logic for the user to run. Main parameters: repo URL, auth method (PAT / GitHub Token), whether no_proxy direct mode is on, and the error-log summary — used to pick the specific Gitee-to-public or AtomGit backend rule.

### Workflow
1. Collect the user's error (401, timeout); decide whether it is an auth problem or a blocked-channel root cause.
2. Pick the push plan by platform: prefer env-var token direct push; on batch errors, check the `--raw` value logic.
3. Build the push environment: set no_proxy to bypass the proxy that cuts git transport; enable private-to-public or backend adaptation for Gitee/AtomGit.
4. Emit concrete commands or code snippets (including the Git Data API flow) for the user to run.
5. Verify push status and summarize; record unknown anomalies to the doc knowledge base for later improvement.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.2.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
当用户反馈 git push 报错 401（令牌失效/凭据残留）、请求超时或网络挂死时，用于根因排查。
当涉及 GitHub、Gitee/AtomGit 等平台的仓库发布、推送到远端或私有转公开操作需求时。
当检测到大面积 401 错误需排查取值前缀坑（--raw），或使用环境变量直连推送令牌方案时。
当需要执行 Git Data API 兜底流程（blob→tree→commit→ref）处理复杂对象推送时。

### 用法
本技能无需调用外部脚本，为文档型技能，用户通过自然语言触发关键词自动获取对应排查指南与代码模板。系统需识别目标平台类型、认证令牌来源及网络环境配置参数，直接生成包含直连推送命令或 API 调用逻辑的文本内容供用户参考执行。
主要参数包括：仓库地址/URL、认证方式（PAT/GitHub Token）、是否启用 no_proxy 直连模式以及错误日志摘要，用于匹配具体的 Gitee 转公开或 AtomGit 特殊处理规则。

### 流程
1. 收集用户报错信息（如 401、超时），判断是授权问题还是通道阻塞根因。
2. 根据目标平台选择推送方案：优先使用环境变量取令牌直连，若遇批量错误则检查 --raw 取值逻辑。
3. 构造推送执行环境：配置 no_proxy 规避代理拦截，针对 Gitee/AtomGit 启用私有转公开或后端适配转换。
4. 生成并展示具体命令或代码片段（含 Git Data API 流程），指导用户手动执行。
5. 验证推送状态并总结排查结果，若遇未知异常则记录至文档知识库供后续优化。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.2.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
