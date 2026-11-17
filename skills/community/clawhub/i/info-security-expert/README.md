# 龙.skill — 马金龙 AI 安全顾问（info-security-expert）

> 一个面向企业信息安全场景的 WorkBuddy 专家技能包（Skill / Expert）。

马金龙的数字化分身——15 年+ 信息安全实战经验，CISSP、CIW Security Analyst 持证，
《企业信息安全体系建设之道》作者，公众号「安全管理杂谈」主理人。
不整虚的，说人话，先动手再开口。

## 能干什么

覆盖企业信息安全的全生命周期咨询与落地指导：

- **安全体系建设**：从零搭建、成熟度评估、路线图规划（道法术器势框架）
- **等保合规**：等级保护 2.0 五步法、网安法 / 数据安全法 / 个保法 / SOX404
- **安全架构**：纵深防御、安全域划分、零信任、IAM / MFA / RBAC
- **攻防演练 / 护网**：红蓝对抗、钓鱼演练、护网准备与复盘
- **SDL / DevSecOps**：威胁建模、安全左移、流水线扫描集成
- **供应链安全 / 数据安全 / 云安全 / AI 安全 / 工控安全**
- **ISMS 制度文档**：五级文档体系（方针→制度→流程→规范→表单）编写
- **安全事件响应 / 应急取证 / 安全培训体系**

## 目录结构

```
info-security-expert/
├── SKILL.md                      # 技能入口与索引（必含）
├── references/                   # 详细知识库
│   ├── framework.md              # 道法术器势 + CIA + 四层架构
│   ├── knowledge-domains.md      # 知识领域详解
│   ├── methodology.md            # 咨询方法论（四步走）
│   ├── practical-wisdom.md       # 12 条实战经验
│   ├── style.md                  # 说话风格与做事原则
│   ├── isms-doc-system.md        # ISMS 文档编码体系
│   ├── system-security.md        # 系统/主机安全
│   ├── incident-response.md      # 事件响应
│   ├── vulnerability-management.md # 漏洞管理
│   ├── security-culture.md       # 安全文化
│   └── software-supply-chain.md  # 软件供应链安全
└── README.md
```

## 安装到 WorkBuddy

将本仓库克隆 / 下载后，放到 WorkBuddy 的技能目录：

- **用户级（推荐，全局可用）**：`~/.workbuddy/skills/info-security-expert/`
- **项目级（团队共享）**：`<项目>/.workbuddy/skills/info-security-expert/`

目录结构需保持 `SKILL.md` 在根、`references/` 在同级的形态。重启 WorkBuddy 后即可在对话中调用该专家。

## 使用边界

本技能只做**咨询、规划、评估、方法论传授**，不执行以下动作：

- 不做实际渗透测试（无书面授权即犯罪）
- 不对用户系统直接执行操作
- 不替用户做业务决策

## 许可

本仓库内容供个人学习与安全体系建设参考使用。转载或二次分发请保留出处，并注明作者「马金龙 / 安全管理杂谈」。
