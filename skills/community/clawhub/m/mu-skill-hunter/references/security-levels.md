# 安全风险分级说明

## 风险等级定义

| 等级 | 触发条件 | 结论 | 木老师操作 |
|------|---------|------|----------|
| 🟢 LOW | 无任何 Flag | ✅ 可安装 | 确认安装命令即可 |
| 🟡 MEDIUM | 仅有 Yellow Flags | ⚠️ 需确认 | 人工核实 Yellow Flag 描述后决定 |
| 🔴 HIGH | 1~2 条 Hard Reject | ❌ 建议拒绝 | 小木上报，等木老师明确指令 |
| ⛔ EXTREME | 3+ 条 Hard Reject | ❌ 拒绝 | 直接拒绝，清理暂存区 |

## Hard Reject 规则（R1~R10 + AI1~AI2）

来源：mu-lobster-guard Red Flags 完整规则集

| ID | 规则名 | 触发模式 | 风险 |
|----|--------|---------|------|
| R1 | 外部 URL 请求 | curl/wget 到非白名单域名 | 数据外泄 |
| R2 | base64 解码执行 | base64 -d / atob() | 隐藏 payload |
| R3 | eval/exec 动态执行 | eval() / exec() | 远程代码执行 |
| R4 | 读取系统凭证路径 | ~/.ssh / ~/.aws / /etc/shadow | 凭证窃取 |
| R5 | 访问 Agent 私密文件 | MEMORY.md / SOUL.md / agent-config.json | 隐私泄露 |
| R6 | 混淆/超长单行代码 | 单行 >500 字符 | 隐藏恶意逻辑 |
| R7 | 裸 IP 网络请求 | http://x.x.x.x | 绕过域名审查 |
| R8 | 提权操作 | sudo / chmod 777 / chown root | 提权攻击 |
| R9 | 凭证外发 | token/key/secret + curl/fetch | 凭证泄露 |
| R10 | 未声明包安装 | pip/npm/apt install 未在文档说明 | 供应链投毒 |
| AI1 | Prompt Injection | "ignore previous instructions" 等 | 隐藏指令攻击 |
| AI2 | 挖矿特征 | xmrig / stratum+tcp / coinhive | 恶意占用算力 |

## Yellow Flag 规则（Y1~Y4）

| ID | 规则名 | 说明 | 判断方式 |
|----|--------|------|---------|
| Y1 | 写入 Agent 持久化目录 | 合法 Skill 可能需要，但需确认写入范围 | 检查写入路径是否在 Skill 自己的子目录 |
| Y2 | 已知外部网络请求 | 确认目标域名是否为 Skill 声明的依赖 | 对照 SKILL.md 描述确认 |
| Y3 | 环境变量修改 | 确认是否影响其他工具 | 查看改了哪个变量名 |
| Y4 | 后台进程/子进程 | 确认是否有终止条件 | 查看是否有超时/退出机制 |

## 白名单域名（R1 豁免）

以下域名为正常 Skill 依赖，不触发 R1：
- `github.com` / `api.github.com` / `raw.githubusercontent.com`
- `clawhub.ai`
- `skillhub.cn` / `skillhub-1388575217.cos.ap-guangzhou.myqcloud.com`（SkillHub 腾讯云 COS）
- `skills.sh`
- `npmjs.com` / `pypi.org`

## 原则

> **宁可误拒，不可误放。**
> 不确定时一律上报木老师，不自行放行。
