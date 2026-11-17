---

name: plug-enterprise-security-suite
slug: plug-enterprise-security-suite
displayName: "企业安全开发套件"
version: 1.1.0
summary: "认证/调试/反检测/密钥管理4合1,覆盖安全开发全生命周期"
license: Proprietary
description: |-
  |- 功能涵盖: plug, enterprise,。Use when 用户需要plug-enterprise-security-suite相关功能时使用。不适用于超出本技能能力范围的复杂需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。提供结构化输出和错误处理机制。
  覆盖企业级安全开发全场景的技能组合包，从认证架构到密钥管理，从调试排障到浏览器反检测，一站式解决安全开发难题。
  目标用户: 企业安全团队、全栈开发者、DevSecOps工程师、SaaS产品团队
  定价方案: 月付￥499/月 | 年...
tools:
  - read
  - exec
  - write
tags:
  - 企业安全
  - 认证授权
  - 调试排障
  - 浏览器自动化
  - 密钥管理
  - DevSecOps
  - OAuth
  - RBAC

---

> **核心功能**: 本技能提供中文交互、化工作流场景等能力。
## 异常处理指南
### 问题1: Better Auth认证系统登录返回500错误
**现象**: 用户登录时返回500 Internal Server Error
**原因**: BETTER_AUTH_SECRET未配置或数据库连接失败
**解决**:
1. 检查 `BETTER_AUTH_SECRET` 环境变量是否配置（会话签名密钥）
2. 确认数据库连接字符串正确，数据库服务在线
3. 检查auth-schema.sql是否已执行，数据库表结构是否完整
4. 使用key-vault-manager查看密钥存储状态，确认密钥未过期
5. 查看Node.js应用日志，确认Better Auth初始化无报错
### 问题2: 调试医生定位到的根因在并发代码中
**现象**: Bug仅在并发场景下出现，单线程测试无法复现
**原因**: 竞态条件或死锁，需要并发调试技术
**解决**:
1. 调试医生切换到并发调试模式：Thread Sanitizer/线程转储/锁图分析
2. 使用条件等待策略：记录触发频率与条件，增加日志等待下次触发
3. 生成线程转储（jstack/Node.js --inspect），分析锁竞争情况
4. 使用git bisect定位引入并发Bug的提交
5. 修复后使用验证闭环：回归测试（先验证失败→修复后通过）+ 完整测试套件
### 问题3: 浏览器自动化频繁被封号
**现象**: 多账号浏览器自动化操作后，账号被平台封禁
**原因**: 浏览器指纹未隔离或操作频率过高，被平台检测到自动化行为
**解决**:
1. 确认每个账号使用独立的浏览器配置目录（profile_dir参数）
2. 确认每个账号使用独立的Cookie存储（会话隔离）
3. 增加操作间隔频率控制（模拟真人操作节奏）
4. 敏感操作走独立WebSocket直连CDP，执行反检测JS
5. 使用CDP探针验证反检测有效性
6. 先访问首页建立Session再执行搜索（Cookie预热）
### 问题4: 密钥保险箱审计日志查询缓慢
**现象**: 查询审计日志响应时间超过5秒
**原因**: 审计日志数据量大，未建立索引或未分区
**解决**:
1. 确认审计日志表已建立时间戳索引
2. 按月分区审计日志表，减少单次查询数据量
3. 定期归档180天前的审计日志到冷存储
4. 使用key-vault-manager的合规报告功能，按时间段生成摘要
### 问题5: OAuth登录回调URL不匹配
**现象**: Google OAuth登录回调时报redirect_uri_mismatch错误
**原因**: OAuth Provider配置的回调URL与应用实际URL不一致
**解决**:
1. 确认Google Cloud Console中配置的Authorized redirect URIs
2. 确认应用环境变量GOOGLE_REDIRECT_URI与配置一致
3. 开发环境使用localhost回调，生产环境使用域名回调
4. 国内环境替换为微信/支付宝/飞书/钉钉OAuth Provider
5. 使用Better Auth的genericOAuth插件配置自定义Provider
## 功能适用范围
### 认证架构限制
- **Better Auth框架限制**: 部分高级功能（如OIDC Provider模式）仍在迭代，企业SSO(SAML)配置复杂需IdP端配合
- **WebAuthn兼容性**: Passkey/WebAuthn在旧浏览器（IE、部分安卓WebView）不支持，需提供降级方案
- **安全测试边界**: 本技能提供架构设计与配置模板，不替代完整的安全渗透测试
- **性能依赖LLM**: 复杂权限策略可能需要人工审查，性能取决于底层LLM能力
### 调试医生限制
- **不适用于**: 代码审查与静态分析（请使用lint工具）、自动化测试编写（请使用测试框架）、部署与发布管理（请使用CI/CD工具）、安全漏洞挖掘（请使用安全测试工具）、代码重构与性能优化（聚焦Bug修复）
- **间歇性Bug**: 无法保证100%复现间歇性故障，需增加监控等待触发
- **多语言覆盖**: 支持Python/JS/Go/Java/Rust主流语言，小众语言可能需要适配
### 浏览器助手限制
- **合规要求**: 仅用于合法合规场景（自动化测试/RPA流程/合规多账号管理），禁止用于爬虫滥用、刷量、欺诈
- **Chrome版本**: 需要Chrome/Chromium浏览器，不支持Firefox/Safari
- **反检测边界**: 反检测方案无法保证100%不被检测，平台检测技术持续升级
- **资源消耗**: 多账号并行时内存消耗较大，建议单实例管理不超过20个账号
### 密钥管理限制
- **本地存储**: 密钥存储在本地文件系统，不支持云端同步（安全考虑）
- **团队共享**: 需要所有成员安装key-vault-manager，加密分发需手动确认
- **轮换窗口**: 密钥轮换期间需双密钥兼容，轮换窗口内旧密钥仍有效
### 不适用场景
- 网络层安全（防火墙、WAF配置，属基础设施范畴）
- 数据库加密设计（属数据层安全）
- 代码漏洞扫描（属SAST/DAST工具职责）
- 物理安全与办公网络安全
- 监控告警系统搭建（请使用Prometheus/Grafana）
- 实时性要求<100ms的场景
- 需要完全离线运行的场景（LLM由Agent内置但部分API需网络）
## 疑问解答
### Q1: Better Auth与NextAuth/Auth.js有何区别？
A: Better Auth提供更完整的开箱即用功能（2FA、组织管理、Passkey内置），TypeScript优先，数据库Schema透明可控；NextAuth更轻量，社区生态成熟。企业级场景优先Better Auth。
### Q2: 调试医生的4阶段调试法适用于所有Bug吗？
A: 适用于复杂Bug、生产事故、间歇性故障、性能问题、并发问题。不适用于简单语法错误和UI样式微调（直接修改即可）。回归Bug可使用git bisect快速定位引入提交。
### Q3: 反检测浏览器助手合规吗？
A: 本工具仅用于合法合规的浏览器自动化场景（自动化测试/RPA流程/合规多账号管理）。使用者需遵守各平台服务条款和当地法律法规，禁止用于爬虫滥用、刷量、欺诈等违规行为。
### Q4: 密钥保险箱支持云端同步吗？
A: 不支持。出于安全考虑，密钥存储在本地文件系统，不支持云端同步。团队共享通过加密分发实现，需所有成员安装key-vault-manager。
### Q5: 国内环境如何替代Google OAuth？
A: 接入微信开放平台（扫码登录）、支付宝开放平台、飞书登录、钉钉登录。Better Auth支持自定义OAuth Provider，使用genericOAuth插件配置。
## 安全
### API Key零暴露原则
- 所有密钥（BETTER_AUTH_SECRET/OAuth Secret/JWT Secret/SMTP密码）通过环境变量注入
- Skill内零硬编码，所有密钥通过key-vault-manager统一管理
- 密码哈希强制：使用argon2（推荐）或bcrypt，禁止明文/MD5/SHA1存储
- 令牌安全：Access Token短有效期 + Refresh Token轮换 + httpOnly Cookie存储
- 密钥轮换：建议每90天轮换BETTER_AUTH_SECRET，提供轮换期间双密钥兼容
- 审计日志：记录登录、权限变更、组织操作、密钥操作等敏感行为，保留180天
### 认证安全防护
- **OWASP Top 10**: 注入防护 + XSS(CSP) + CSRF(SameSite+Token) + 速率限制
- **防暴力破解**: 登录尝试5次/15分钟 + 账号锁定 + IP封禁
- **会话安全**: 登录后重新生成会话ID（防会话固定攻击）
- **账号枚举防护**: 统一响应消息"若账号存在，邮件已发送"
- **密码重置安全**: 令牌时效性（15分钟）+ 一次性使用 + IP绑定
### 国内适配性
- OAuth Provider: 微信/支付宝/飞书/钉钉（替代Google/GitHub）
- 短信服务: 阿里云短信/腾讯云短信（替代Twilio）
- 邮件服务: 阿里云邮件推送/腾讯企业邮（替代SendGrid）
- 身份认证服务: 阿里云IDaaS/腾讯云身份管家（替代Auth0）
- 数据库: 达梦/人大金仓/TDSQL（替代MySQL/数据库）
- 浏览器: 360/搜狗浏览器（基于Chromium，兼容CDP协议）
===
## 技术创新
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
|:--------|:--------|:--------|:--------|:--------|
| 认证授权体系设计 | 2天/次 | 1小时/次 | 1.5天/次 | 10% |
| Bug根因分析 | 1周/次 | 2小时/次 | 6.5天/次 | 15% |
| 浏览器自动化测试 | 3天/次 | 1天/次 | 2天/次 | 5% |
| 密钥管理 | 1天/次 | 30分钟/次 | 0.5天/次 | 5% |
| 安全审计 | 1周/次 | 1天/次 | 6天/次 | 10% |
### 差异化对比
| 对比维度 | 本Plug | 手动操作 | Python脚本 | 专业软件 |
|:--------|:--------|:--------|:--------|:--------|
| 功能集成 | 一站式解决方案 | 分散操作 | 部分功能 | 功能全面但操作复杂 |
| 用户界面 | 优化用户体验 | 繁琐操作 | 界面简单 | 界面复杂 |
| 学习曲线 | 简单易学 | 需要培训 | 需要编程基础 | 需要专业知识 |
| 成本效益 | 高性价比 | 高成本 | 中等成本 | 高成本 |
| 支持与维护 | 专业支持 | 无支持 | 社区支持 | 专业支持 |
### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
|:----|:----|:----|:----|:----|
| 认证授权复杂 | 设计和维护认证授权体系复杂，易出错 | 安全风险 | 提供认证安全架构师技能，简化设计流程 | 降低错误率20% |
| Bug定位困难 | Bug定位耗时，影响开发效率 | 项目进度 | 提供调试医生技能，快速定位问题 | 提高开发效率30% |
| 密钥管理不安全 | 密钥管理不当，导致数据泄露 | 数据安全 | 提供密钥保险箱技能，增强密钥安全性 | 提高数据安全性50% |
===
## 代码示例
### 基础用法
```bash
# 安装和初始化
skill install plug-enterprise-security-suite
# 基本调用示例
skill execute plug-enterprise-security-suite --input "示例输入"
```
### 高级用法
```python
# Python API调用示例
import requests
# 配置API端点
api_url = "http://localhost:8080/api/skills/plug-enterprise-security-suite"
headers = {"Authorization": "Bearer YOUR_API_KEY"}
# 执行技能
response = requests.post(api_url, json={
    "input": "示例输入数据",
    "options": {"mode": "advanced"}
})
result = response.json()
print(result)
```
### 命令行批处理
```bash
# 批量处理多个输入
for file in *.csv; do
  skill execute plug-enterprise-security-suite --input "$file" --output "result_$file"
done
```
# 企业安全开发套件
> 认证架构、科学调试、浏览器反检测、密钥管理四大能力协同，覆盖企业安全开发全生命周期
## 能力清单
本Plug将企业安全开发拆解为4个独立又互补的能力域：认证安全架构师负责认证授权体系设计，调试医生负责Bug根因分析，反检测浏览器助手负责浏览器自动化稳定性，密钥保险箱负责敏感凭证安全管理。4个技能形成从架构设计到运行时调试到密钥保护的完整安全闭环。
### 包含技能
| 技能 | slug | 领域 | 核心能力 | 质量分 |
|:-----|:-----|:-----|:-----|:-----|
| 认证安全架构师 | `auth-security-architect` | Security | Better Auth + OAuth/2FA/SSO + RBAC/ABAC + OWASP Top 10防护 | 4.8/5.0 |
| 调试医生 | `debug-doctor` | Automation | 4阶段科学调试法 + 二分查找 + 并发/性能调试 + 验证闭环 | 4.9/5.0 |
| 反检测浏览器助手 | `stealth-browser-assistant` | Automation | DOM蒸馏三树定位 + Tab崩溃3秒自愈 + 指纹隔离 + 反检测混合方案 | 4.9/5.0 |
| 密钥保险箱(专业版) | `key-vault-manager` | Automation | 多保险箱管理 + 审计日志 + 密钥轮换 + 团队共享 + 本地API代理 | 4.7/5.0 |
### 技能间协同关系
```
auth-security-architect (认证架构) ──设计安全体系──> 应用开发
         │                                            │
    生成密钥/凭证                                      │
         │                                            │
         v                                            v
key-vault-manager (密钥管理) <──存储/轮换/审计──> debug-doctor (调试排障)
         │                                            │
    管理API Key                                定位生产Bug根因
         │                                            │
         v                                            v
stealth-browser-assistant (浏览器自动化) <──自动化测试/验证──┘
```
- **auth-security-architect** 设计认证授权体系，生成OAuth Client Secret、JWT Secret等凭证
- **key-vault-manager** 安全存储auth-security-architect生成的所有凭证，支持轮换和审计
- **debug-doctor** 在安全系统运行时使用4阶段科学调试法定位Bug根因
- **stealth-browser-assistant** 为安全系统的E2E自动化测试提供反检测浏览器能力
## 使用时机
| 触发场景 | 触发关键词/意图 | 调用技能 |
|:---------|:----------------|:---------|
| 设计认证授权系统 | "认证"、"授权"、"OAuth"、"2FA"、"SSO"、"登录"、"RBAC"、"权限" | auth-security-architect |
| 排查复杂Bug或生产事故 | "调试"、"Bug"、"根因"、"事故排查"、"复现"、"二分查找" | debug-doctor |
| 浏览器自动化被封/元素定位失败 | "浏览器自动化"、"反检测"、"指纹"、"封号"、"元素定位"、"CDP" | stealth-browser-assistant |
| 管理API密钥或证书 | "密钥管理"、"API Key"、"密钥轮换"、"审计日志"、"密钥保险箱" | key-vault-manager |
| 企业安全开发全流程 | "安全开发"、"DevSecOps"、"安全架构" | 4技能协同 |
## 适用范围
### 场景1 SaaS产品认证系统从零搭建
SaaS产品团队需要从零设计认证授权系统，支持邮箱密码、社交登录、2FA和企业SSO。
- **Step 1**: 调用 auth-security-architect，描述需求"支持邮箱密码+Google OAuth+TOTP 2FA，技术栈Next.js+better-auth+数据库"
- **Step 2**: 技能输出 auth.ts 配置 + auth-schema.sql 数据库表结构 + LoginForm.tsx + TwoFactorSetup.tsx
- **Step 3**: 调用 key-vault-manager，将生成的 BETTER_AUTH_SECRET、GOOGLE_CLIENT_SECRET 等密钥存入保险箱
- **Step 4**: 配置密钥轮换策略（90天轮换BETTER_AUTH_SECRET）和审计日志
### 场景2 生产事故根因排查
DevSecOps工程师遇到生产环境间歇性认证失败，传统调试方法无法定位根因。
- **Step 1**: 调用 debug-doctor，传入Bug现象"间歇性登录失败，约5%请求返回401"+ 日志 + 复现条件
- **Step 2**: 技能执行4阶段调试法：复现（记录触发频率与条件）→ 定位（二分查找+日志增强）→ 缩减（最小复现用例）→ 修复（最小化修改+验证闭环）
- **Step 3**: 定位根因后（如Refresh Token轮换竞态条件），输出修复方案和回归测试
- **Step 4**: 调用 key-vault-manager 审计日志，确认是否涉及密钥轮换导致的问题
### 场景3 多账号浏览器自动化安全测试
安全团队需要对SaaS产品进行多账号浏览器自动化测试，但遇到账号被封和元素定位失效问题。
- **Step 1**: 调用 stealth-browser-assistant，配置多账号指纹隔离（每个账号独立浏览器配置目录+独立Cookie存储）
- **Step 2**: 使用DOM蒸馏三树智能定位（无障碍角色→文本匹配→JS事件监听器→坐标点击）解决SPA前端更新导致元素失效
- **Step 3**: Tab崩溃时3秒内自动重建浏览器上下文，恢复崩溃前URL与Cookie
- **Step 4**: 敏感操作走独立WebSocket直连CDP，CDP探针验证反检测有效性
## 使用说明
### 快速开始
1. 确认Agent已加载本Plug的SKILL.md及4个成员技能的SKILL.md
2. 在Agent环境变量中配置 `LLM_API_KEY`（必需）和其他安全相关密钥
3. 确认Agent支持 exec 工具（命令行执行能力）
4. 认证架构师需要 Node.js 18+ 环境运行 Better Auth
5. 在Agent对话中描述安全需求，Plug将根据触发条件自动选择对应技能
### 安全开发工作流
#
### Step 1: 认证架构设计（auth-security-architect）
- **输入**: 应用类型（B2C SaaS/B2B企业应用/内部系统）+ 认证方式需求 + 技术栈
- **处理**: 基于Better Auth官方优选实践设计认证体系
  - 认证方式：邮箱密码 + OAuth + Magic Link + Passkey + 企业SSO(SAML/OIDC)
  - 会话策略：JWT无状态 / 数据库会话 / 混合模式
  - 权限模型：RBAC（角色-权限映射）+ ABAC（属性-权限映射）+ 多组织隔离
  - 2FA：TOTP + 短信验证码 + 邮箱验证码 + WebAuthn/Passkey + 备份码
  - OWASP Top 10防护：注入防护 + XSS(CSP) + CSRF(SameSite+Token) + 速率限制
- **输出**: auth.ts配置 + auth-schema.sql + API路由 + 登录表单 + 2FA设置组件
- **国内适配**: OAuth Provider优先微信/支付宝/飞书/钉钉，短信用阿里云/腾讯云
#
### Step 2: 密钥安全管理（key-vault-manager）
- **输入**: 密钥列表（BETTER_AUTH_SECRET/OAUTH secrets/SMTP密码等）+ 保险箱配置
- **处理**:
  - 多保险箱管理：按项目隔离密钥集合，权限隔离与切换
  - 密钥验证与脱敏：本地密钥安全操作，返回数据脱敏
  - 本地API代理：本地注入密钥发起请求，代理链路与重试策略
  - 审计日志：全量记录所有密钥操作历史
  - 密钥轮换：自动化密钥更新，定时轮换与到期提醒
  - 团队共享：加密分发密钥，端到端加密与权限控制
- **输出**: 密钥存储状态 + 审计日志 + 轮换计划 + 合规报告
#
### Step 3: 科学调试排障（debug-doctor）
- **输入**: Bug现象 + 代码环境 + 复现步骤 + 日志
- **处理**: 4阶段科学调试法
  - 复现：精确复现 + 可靠性评估 + 间歇性故障条件等待
  - 定位：二分查找（代码二分/模块二分/Git bisect/数据二分）+ 日志增强
  - 缩减：最小复现用例 + 根因确认
  - 修复：最小化修改 + 验证闭环 + 防御深度
- **高级技术**: 条件等待(间歇性故障)、并发调试(Thread Sanitizer/线程转储/锁图)、性能调试(Flame Graph/py-spy/内存快照)
- **输出**: 4阶段调试报告 + 根因分析 + 修复方案 + 回归测试 + 防复发措施
- **多语言适配**: Python(pdb/cProfile)、JS(Chrome DevTools)、Go(pprof)、Java(jstack/jmap/MAT)、Rust(gdb)
#
### Step 4: 浏览器自动化安全测试（stealth-browser-assistant，可选）
- **输入**: action(locate_element/recover_tab/stealth_check/browser_lifecycle) + intent + url
- **处理**:
  - DOM蒸馏三树智能定位：CDP获取DOM树+Accessibility树+DOMSnapshot，降级链定位元素
  - Tab崩溃3秒自愈：监听page crash事件，3秒内重建浏览器上下文，恢复URL与Cookie
  - 指纹防护与多账号隔离：独立浏览器配置目录 + 独立Cookie存储 + 操作间隔频率控制
  - 反检测混合方案：日常操作走自动化API，敏感操作走WebSocket直连CDP
- **输出**: 元素句柄 + 定位方法 + 置信度 + 恢复状态 + 反检测结果
### 单技能调用
每个技能均可独立调用。认证架构师适合项目初期设计阶段，调试医生适合运行时排障阶段，浏览器助手适合自动化测试阶段，密钥管理贯穿全生命周期。
## 请求格式
```json
{
  "plug": "plug-enterprise-security-suite",
  "action": "execute_workflow | execute_single",
  "input": {
    "workflow": "full | auth_only | debug_only | stealth_only | vault_only",
    "auth_input": {
      "app_type": "B2C SaaS",
      "auth_methods": ["email_password", "google_oauth", "totp_2fa"],
      "tech_stack": "Next.js + better-auth + 数据库",
      "session_strategy": "database"
    },
    "debug_input": {
      "bug_description": "间歇性登录失败，约5%请求返回401",
      "environment": "production",
      "reproduction_steps": "随机出现，无法稳定复现",
      "logs": "..."
    },
    "stealth_input": {
      "action": "locate_element",
      "intent": "点击登录按钮",
      "url": "https://app.example.com/login",
      "fallback_selectors": ["#login-btn", "button[type=submit]"]
    },
    "vault_input": {
      "action": "store_key",
      "vault_id": "project_alpha",
      "key_name": "BETTER_AUTH_SECRET",
      "key_value": "***",
      "rotation_days": 90
    }
  },
  "options": {
    "format": "json",
    "verbose": true
  }
}
```
## 返回格式
```json
{
  "status": "success",
  "plug": "plug-enterprise-security-suite",
  "results": [
    {
      "step": 1,
      "skill": "auth-security-architect",
      "status": "completed",
      "output": {
        "files": ["auth.ts", "auth-schema.sql", "LoginForm.tsx", "TwoFactorSetup.tsx"],
        "auth_methods": ["email_password", "google_oauth", "totp"],
        "session_strategy": "database",
        "rate_limit": "10 requests/minute"
      }
    },
    {
      "step": 2,
      "skill": "key-vault-manager",
      "status": "completed",
      "output": {
        "vault_id": "project_alpha",
        "keys_stored": 5,
        "rotation_configured": true,
        "audit_log_enabled": true
      }
    }
  ],
  "metadata": {
    "total_steps": 2,
    "duration_ms": 8000,
    "timestamp": "2026-07-29T10:00:00Z"
  }
}
```
## 运行环境
### 运行环境
- **Agent平台**: Claude Code / Cursor / Codex / Gemini CLI / Windsurf 等支持SKILL.md的任意Agent
- **操作系统**: Windows / macOS / Linux
- **运行时**: 需要Agent支持 exec（命令行执行）能力
- **Node.js**: 18+（认证安全架构师运行Better Auth必需）
### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 | 国内替代方案 |
|:-------|:-----|:---------|:---------|:-------------|
| LLM API | API | 必需 | 任意LLM服务商，由Agent内置LLM提供 | 通义千问/文心一言/智谱GLM/DeepSeek/Kimi |
| better-auth | npm包 | 认证架构必需 | `npm install better-auth` | 无替代，Better Auth为开源框架 |
| 数据库 | 关系型数据库 | 认证架构必需 | MySQL/数据库/SQLite | 国产数据库: 达梦/人大金仓/TDSQL |
| Chrome/Chromium | 浏览器 | 浏览器助手必需 | Chrome浏览器 | 国产浏览器: 360/搜狗(基于Chromium) |
| OAuth Provider | API Key | 认证架构可选 | Google/GitHub Client ID/Secret | 微信/支付宝/飞书/钉钉开放平台 |
| 短信服务 | API Key | 认证架构可选 | Twilio短信2FA | 阿里云短信/腾讯云短信 |
| 邮件服务 | SMTP | 认证架构可选 | SendGrid邮件验证 | 阿里云邮件推送/腾讯企业邮 |
| JSON文件存储 | 文件系统 | 密钥管理必需 | exec工具创建vault目录 | 本地文件系统，无海外依赖 |
### API Key配置（零暴露原则）
- **LLM_API_KEY**: 必需（通常由Agent内置）- 架构设计/调试分析/浏览器定位
- **BETTER_AUTH_SECRET**: 认证架构必需 - 会话签名密钥，建议90天轮换
- **GOOGLE_CLIENT_ID/SECRET**: 认证架构可选 - Google OAuth登录
- **TWILIO_API_KEY**: 认证架构可选 - 短信2FA
- **SMTP配置**: 认证架构可选 - 邮箱验证/密码重置
- **配置方式**: 所有密钥通过环境变量注入，Skill内零硬编码
- **安全检查**: 所有密钥通过key-vault-manager管理，严禁在代码中硬编码
### 可用性分类
- **分类**: MD+EXEC
- **说明**: 纯Markdown技能定义，认证架构师需要Node.js+数据库环境，浏览器助手需要Chrome环境
- **开箱即用**: 密钥管理和调试医生可零配置直接使用（LLM由Agent内置），认证架构师和浏览器助手需额外环境
## 错误恢复流程
### 异常处理策略
## 核心特点
- **自动化执行**: 认证/调试/反检测/密钥管理4合1,覆盖安全开发全生命周期
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## 特色分析
| 对比维度 | 企业安全开发套件 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 认证/调试/反检测/密钥管理4合1,覆盖安全开发全生命周期 | 通用场景 | 通用场景 |