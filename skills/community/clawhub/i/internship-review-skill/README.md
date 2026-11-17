# 实习复盘 Skill（internship-review）

> 将零散的实习记忆转化为结构化的专业复盘文档。支持 **WorkBuddy 技能安装**和**任意 AI agent 粘贴即用**两种方式。

## 功能

- **模板生成**：根据用户背景自动生成定制的复盘模板（9 个板块）
- **逐段引导**：一对一引导用户填满每个板块，一次一个问题，不一次塞满
- **STAR+L 方法论**：S 场景 → T 任务 → A 行动 → R 结果 → **L 可复用的方法论**

## 使用方式

### 方式 A：WorkBuddy 技能安装

1. 下载本仓库
2. 将 `internship-review/` 文件夹放入 skills 目录：
   - 用户级：`~/.workbuddy/skills/`
   - 项目级：`.workbuddy/skills/`
3. 新开对话即可激活，触发词：

```
帮我复盘实习  写一份实习回顾  实习复盘  实习总结
```

### 方式 B：任意 AI agent 粘贴即用

1. 打开 [`internship-review-all-in-one.md`](./internship-review-all-in-one.md)
2. 复制全部内容，粘贴到以下任一位置：
   - **ChatGPT**：Custom GPT 的 Instructions / Projects 的 Project instructions
   - **Claude**：Projects 的 Project knowledge / 对话中直接粘贴
   - **Cursor / Windsurf**：`.cursor/rules/` 或 `.windsurfrules`
   - **其他 agent**：作为 System Prompt 或 Project Context
3. 对话中说"帮我复盘实习"即可启动

### 各平台差异

| 平台 | 文件加载 | 模板输出 |
|---|---|---|
| **WorkBuddy** | 自动按需加载 `references/` | 直接写入 Obsidian/本地文件 |
| **ChatGPT** | 粘贴 all-in-one 版到 Instructions | 手动复制模板到本地 |
| **Claude Projects** | 上传 all-in-one 到 Project knowledge | 直接写入文件系统 |
| **Cursor** | 放入 `.cursor/rules/` 自动加载 | 直接写入文件系统 |

## 结构

```
internship-review/
├── SKILL.md                            # WorkBuddy 技能主流程
├── internship-review-all-in-one.md     # 通用版：粘贴即用，适配所有 agent
├── README.md
├── LICENSE
└── references/
    ├── review-template.md              # 9 板块复盘模板
    └── review-methodology.md           # STAR+L 方法论 + 引导话术
```

## 复盘模板包含

| # | 板块 | 说明 |
|---|---|---|
| 0 | 基本信息 | 公司、岗位、周期 |
| 1 | 一句话总结 & 价值闭环 | 入职 vs 离职的能力对比 |
| 2 | 数据速览 | 硬数字先摆出来 |
| 3 | 项目复盘 ×2~3 | STAR+L 深度拆解 |
| 4 | 能力盘点 | 硬技能/软技能/认知升级 |
| 5 | 行业与组织观察 | 从公司层拔高到行业层 |
| 6 | 不足与改进 | 具体案例 + 可执行改进方式 |
| 7 | 未来 6 个月计划 | 可验证的行动清单 |
| 8 | 感谢与人脉 | 内推、背调资产 |
| 9 | 附录：作品集素材 | 脱敏后就是作品集原料 |

## 许可证

MIT
