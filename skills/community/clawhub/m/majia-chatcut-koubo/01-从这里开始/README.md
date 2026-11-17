# 从这里开始

这个目录是给维护者看的，不要求先懂代码。

## 我现在想做什么

| 你的目的 | 去哪里 | 怎么维护 |
| --- | --- | --- |
| 记录一次真实剪辑里新踩的坑 | [实操迭代与踩坑](../03-实操迭代与踩坑/README.md) | 先追加案例，再在迭代记录里写这次采用了什么 |
| 查字幕、转场、双画面、人脸取景怎么做 | [剪辑方法手册](../02-剪辑方法手册/README.md) | 找对应主题；只有跨案例验证过的经验才写进这里 |
| 看项目为什么这样设计、下一步做什么 | [项目设计与路线图](../04-项目设计与路线图/README.md) | 维护路线图、架构、迁移说明和规则吸收记录 |
| 修改主题颜色或版式坐标 | `assets/` | 这是半人工、半程序区，修改后必须运行全量验证 |
| 修改机器必须遵守的硬规则 | `rules/` | 同时补 schema、正反 fixture 和测试，不直接手改一句就结束 |
| 修改安装后 Agent 的总行为 | `SKILL.md` | 先读实操案例；修改后检查所有链接和版本面 |
| 修改一句话入口或主流程 | `agents/`、`workflows/`、`src/orchestration/` | 同步入口路由、状态、风险、样片、恢复和交付测试 |
| 修改稳剪/快剪/长片/录屏默认值 | `profiles/` | 默认只能保持或收紧安全边界，并更新匿名正反例 |
| 修改跨会话状态和报告 | `schemas/runtime/`、`templates/runtime/` | 同步 Schema、模板、CLI、故障场景和兼容检查 |
| 发布一批正式更新 | `CHANGELOG.md`、`package.json` | 经验积累不等于发版；达到一批后再统一升级版本 |

## 四个中文维护区

1. `01-从这里开始/`：人类入口和维护地图。
2. `02-剪辑方法手册/`：已经相对稳定、下次可以直接复用的方法。
3. `03-实操迭代与踩坑/`：真实案例、失败路径、ChatCut 产品问题和迭代回执。
4. `04-项目设计与路线图/`：架构、路线图、迁移说明和规则吸收记录。

## 英文目录是什么

这些目录主要给程序、测试和安装工具使用。平时阅读仓库时可以先忽略：

| 目录 | 用途 | 普通维护是否常改 |
| --- | --- | --- |
| `src/` | 核心程序实现 | 否 |
| `scripts/` | 校验和命令行工具 | 否 |
| `schemas/` | JSON 数据合同 | 否 |
| `fixtures/` | 测试用匿名样例 | 否 |
| `tests/` | 自动化回归测试 | 否 |
| `templates/` | 给用户复制的模板 | 偶尔 |
| `agents/` | 安装后的默认一句话入口 | 偶尔 |
| `workflows/` | 稳剪、快剪、专业增强和恢复说明 | 偶尔 |
| `profiles/` | 四套可复现剪辑默认方案 | 谨慎 |
| `assets/` | 版式、主题和视觉资产 | 按需 |
| `rules/` | 机器硬规则 | 谨慎 |

## 最常用的维护流程

```text
真实任务出现问题
  ↓
写入 03-实操迭代与踩坑
  ↓
在不同任务中重复验证
  ↓
晋升到 02-剪辑方法手册
  ↓
可以机器判定时，再进入 rules + fixtures + tests
  ↓
积累到一批后统一发正式版本
```

原则只有一句：案例先积累，方法后晋升，硬规则最后机器化。

## V1.7 主流程改动后的最小检查

```bash
npm run validate:runtime-contracts
npm run test:orchestration
npm run test:risk-policy
npm run test:run-state
npm run test:starter-prompts
npm run smoke:one-click:fake
npm run validate:docs-routing
npm run verify
```

真实 ChatCut 验证结果单独写入 `reports/live-canary-v1.7.0.json`。匿名模拟通过不能把真实状态从 `UNVERIFIED` 改为通过。

官方适配维护先读 [环境与文字修改](../workflows/session-and-text-safety.md) 和 [本轮来源与设计](../04-项目设计与路线图/2026-09-30官方更新与v1.7设计.md)，运行 `npm run test:compatibility` 与 `npm run check:official`。
