# 验收标准

本 Skill 达到以下条件即视为合格：

## 结构验收

- [x] `huawei-cloud-cci-query/` 目录存在，含 `SKILL.md` + `references/` + `scripts/` + `templates/`
- [x] `SKILL.md` 含 frontmatter（name/version/description/triggers/tags/tools）
- [x] frontmatter `name` 与目录名一致（`huawei-cloud-cci-query`）
- [x] `name` 符合命名规范 `huawei-cloud-{product}-{function}`
- [x] `references/iam-policies.md` 存在
- [x] `references/cli-installation-guide.md` 存在
- [x] `templates/test-vars.json` 存在
- [x] `scripts/cci_query.py` 存在且可执行

## 内容验收

- [x] SKILL.md 说明 CCI 实例查询触发场景与使用流程
- [x] 覆盖 hcloud CCI 只读查询命令（listNamespaces、listCoreV1NamespacedPod、readCoreV1NamespacedPod 等）
- [x] 命令名经过真实 `hcloud CCI --help` 验证（非 `ListInstances`/`ShowInstance`）
- [x] 含安全硬约束段落
- [x] 含 KooCLI Command Format Standard 段落
- [x] 含参数确认表

## 功能验收

- [x] `python3 scripts/cci_query.py --help` 正常输出用法
- [x] `python3 scripts/cci_query.py capability-list` 列出全部子命令
- [x] 真实 API 调用返回合法 JSON（`listNamespaces` 返回 `NamespaceList`）
- [x] AK/SK 缺失时退出码 3
- [x] 必填参数缺失时友好报错（退出码 2）
- [x] 403 时提示 CCI 服务授权委托（非静默崩溃）

## 安全验收

- [x] 无硬编码 AK/SK/Token
- [x] 不含任何虚构返回或降级分支，仅真实 API 调用
- [x] 所有 hcloud 调用有 30s 超时
- [x] 凭据动态扫描环境变量（不依赖固定变量名）
- [x] 无硬编码 IP 地址

## 文档验收

- [x] references/cci-cli-reference.md 含全部只读命令参数说明
- [x] references/iam-policies.md 含最小权限策略
- [x] README.md 更新目录结构说明
- [x] 文档清晰可执行，团队成员可据此查询 CCI 实例
