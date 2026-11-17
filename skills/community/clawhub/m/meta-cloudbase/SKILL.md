---
name: meta-cloudbase
version: 1.0.0
description: |
  由 model-distillation 从教师技能 cloudbase 蒸馏并增强的超越型元技能。
  蒸馏其全栈开发部署体系(Web/小程序/移动/云函数/CloudRun/NoSQL·MySQL/鉴权/AI Agent)
  与"先识别场景→读对应源技能→再写码"的路由契约，叠加自验证、自我反思、super-agent
  编排与持续自进化闭环，并在常见失败根因(鉴权漏配/SDK边界误用)上做对抗验证，逐步超越教师。
agent_created: true
visibility: public
---
# meta-cloudbase（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **cloudbase** 蒸馏并增强生成。
> 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略「主动与其他大模型对话、蒸馏、逐步超越」）。

## 来源能力签名（教师 cloudbase）
- 规模：原始 SKILL.md 24869 字符、25 步显性工作流、1 个 learner.py。
- 定位：腾讯云开发（CloudBase）全栈开发部署工具包——建站/Web 应用/微信小程序/移动 App，含鉴权、数据库(NoSQL/MySQL)、云函数、CloudRun、存储、AI 能力、Agent、UI 指引。
- **前置硬依赖**：CloudBase MCP 必须配置（否则无法管理环境/部署/操作数据库）。
- **高优先级路由契约（核心方法论）**：先识别场景 → 读对应源技能 → 再写码/调 API。
  - Web 登录注册 → `auth-tool`→`auth-web`；微信小程序 → `miniprogram-development`→`auth-wechat`；
  - 云函数 → `cloud-functions`；CloudRun 后端 → `cloudrun-development`；AI Agent → `cloudbase-agent`；UI → `ui-design` 先出设计规范。
- **常见失败根因（经验）**：Web 鉴权失败多因跳过 provider 配置；Native 失败多因误读 Web SDK 路径；小程序失败多因把 `wx.cloud` 当 Web 鉴权/SDK 用。

## 蒸馏出的真实工作流（继承 + 强化）
1. **识别场景**：区分 Web / 微信小程序 / Native / 云函数 / CloudRun / AI Agent / UI。
2. **路由读源**：按路由契约先读对应源技能（stable 标识符路由，避免误读 Web SDK）。
3. **确认前置**：检查 CloudBase MCP 是否已配、鉴权 provider 状态与可发布密钥。
4. **开发交付**：UI 场景先出设计规范再写界面；鉴权场景先开 provider 再写前端。
5. **部署验证**：用 MCP 部署/发布，校验环境与函数/DB 操作可达。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 校验"路由是否正确(未误读 Web SDK) + 前置依赖齐备"；reliability<0.8 即回退补配。
2. **自我反思闭环**：每次交付后写入 `self-reflection-loop`，沉淀"哪类场景最常因漏配 provider 失败"，反哺路由前置检查。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程建站/上线任务编排。
4. **对抗验证蒸馏质量**：对路由契约做反例测试——故意给"小程序场景"却走 Web 鉴权路径，验证被纠正到 `auth-wechat`，防误路由。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(cloudbase) | 学生(meta-cloudbase) |
| --- | --- | --- |
| 工作流 | 25 步显性流程（全栈） | 同流程 + 自验证钩子 + 路由反例验证 |
| 失败防护 | 未显式标注 | 显式 limits + 对抗验证（防误路由/漏配） |
| 自进化 | 已有 learner.py | 强化注入，纳入 meta-evolver 闭环 |
| 集成 | 单点全栈工具 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成 CloudBase 全栈开发/部署/上线；本技能在教师能力之上叠加自验证、路由反例验证与反思，输出更可靠、可追溯、少踩坑。

## 已知限制（来自教师蒸馏 + 元进化补充）
- 教师依赖 CloudBase MCP 与 `references/` 下各源技能细节，蒸馏未内嵌这些通道，实跑需先配 MCP 并读对应源技能。
- 教师为开发部署工具，**不替代需求与架构设计**；spec/架构场景应配合 `spec-workflow` 先确认需求。
- 蒸馏不保证覆盖教师全部隐式知识（如完整 MCP 配置路径与各类 SDK 细节），深度使用需对照教师原技能核验。
