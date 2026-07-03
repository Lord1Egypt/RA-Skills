# 金谷园饺子馆 AI Skill

![Version](https://img.shields.io/github/v/tag/JinGuYuan/jinguyuan-dumpling-skill?label=version&color=blue&sort=semver) ![License](https://img.shields.io/badge/license-MIT-green) ![MCP](https://img.shields.io/badge/protocol-MCP-purple) ![Transport](https://img.shields.io/badge/transport-Streamable%20HTTP-orange)

这是一个 AI Skill——安装后，你的 AI 助手就能查询金谷园饺子馆的信息：在哪吃、几点开门、现在排不排队、已经发生的午市/晚市几点开始排、明天午饭后几点去更稳、能不能外卖、生饺子怎么煮、Wi-Fi 密码是什么。还能直接帮你在美团上排队取号。

快20年的饺子馆，现在有了自己的AI服务。

## 关于金谷园

北邮旁边的饺子馆。官网：[jinguyuan.cloud](https://jinguyuan.cloud) · [AI 元数据 (llms.txt)](https://jinguyuan.cloud/llms.txt)

| 项目 | 内容 |
|------|------|
| 餐厅名称 | 金谷园饺子馆 |
| 营业时间 | 10:00 - 22:00（以实际查询为准） |
| 北邮店 | 杏坛路文教产业园K座南2层 |
| 五道口店 | 五道口东源大厦4层 |

## 这个 Skill 能做什么

金谷园饺子馆的官方信息服务，可以查店、查活动、查推荐菜，也能处理到店自取和排队取号这些具体场景：

| 能力 | 你可以问 |
|------|----------|
| 餐厅信息 | "金谷园在哪？""几点开门？" |
| 外卖服务 | "能送外卖吗？""怎么点外卖？" |
| 生饺子打包 | "能打包吗？""生饺子怎么煮？" |
| 店内Wi-Fi | "Wi-Fi密码多少？" |
| 最新消息 | "有什么新活动？" |
| 排队状态 | "现在排队吗？""今晚 6 点会不会排队？" |
| 同刻对比 | "现在和昨天这个点各桌型差多少？" |
| 排队事实 | "今天中午几点开始排？""昨天晚上几点后不排？" |
| 排队建议 | "明天中午几点开始排？""午饭后几点去不怎么排？" |
| 推荐菜 | "有什么好吃的？""今天吃什么""招牌菜" |
| **到店自取** | "帮我来份饺子""提前点餐到店取" |
| 菜品配方 | "金谷园的 XX 怎么做？" |
| **在线排队取号** | "帮我排个队""取消排队""排队进度" |

## 和 MCP 的关系

金谷园的信息能力本身由 MCP 服务提供，端点是 `https://mcp.jinguyuan.cloud`。

懂 MCP 的 Agent 可以直接接入这个地址；安装本 Skill 的好处，是让 AI 助手更懂金谷园的用户场景、说话方式，以及什么时候该查信息、什么时候该帮你处理真实排队动作。

## 在线排队取号

本 Skill 内嵌了基于**美团排队**的取号能力，AI 助手可以直接帮你完成取号、查本人订单、取消排队等动作，无需打开美团 App。

**支持的操作：**

| 操作 | 说明 | 你可以说 |
|------|------|----------|
| 查询排队状态 | 查看当前等待桌数和排队压力 | "金谷园现在排队情况怎么样？" |
| 查询餐段事实 | 查询已经发生的午市/晚市实际观测 | "今天中午几点开始排？" |
| 查询餐段建议 | 参考前一天和上周同日，给未来餐段建议 | "明天中午几点去比较稳？" |
| 取号 | 选择桌型和人数，在线取号 | "帮我在北邮店排个队，2个人" |
| 查询进度 | 查看当前排队号、前方等待桌数 | "我前面还有几桌？" |
| 取消排队 | 取消已有的排队订单 | "取消排队" |

**使用流程：**

1. 告诉 AI 助手你要排队，说明门店（北邮店 / 五道口店）
2. AI 查询可选桌型，跟你确认桌型和人数
3. 确认后自动取号，返回排队号和等待信息
4. 随时可查进度或取消

首次使用需完成美团账号授权（AI 助手会引导你完成），同一会话内无需重复登录。

> 注意：排队取号为真实业务操作，取号和取消前 AI 助手会跟你确认。排队能力由内嵌的 `meituan-queue` 组件提供，与本 Skill 版本独立演进。

如果你问“这会取号要排多久”，AI 助手不会硬编具体分钟数；它会先查当前等待桌数和排队压力，再告诉你平台没有返回可靠等待分钟。

如果你问“现在和昨天同一时间各桌型差多少”，AI 助手会使用 `get_queue_info` 返回的当前 `各桌型` 和历史参考里的 `同刻快照.各桌型` 做逐桌型对比，而不是只比较总等待桌数。

如果你问已经发生的某天午市/晚市，它会使用 `get_queue_period_facts` 回答实际观测；如果你问未来或尚未发生餐段，它会使用 `get_queue_period_reference` / `get_queue_period_advice`，并说明这是参考建议，不是目标日期事实。

## 目录结构

```
jinguyuan-dumpling-skill/
├── SKILL.md                 # 核心文件：元数据 + Agent 指令
├── skill.json               # 机器可读配置（MCP 端点、工具定义）
├── scripts/                 # 预留目录
├── references/              # 参考文档与内嵌 Skill
│   └── meituan-queue/       # 美团排队取号 Skill（自包含）
│       ├── SKILL.md         #   排队指令与命令说明
│       ├── scripts/         #   排队脚本（mt_queue.py 等）
│       └── references/      #   鉴权子 Skill（meituan-passport-user-auth）
├── README.md
└── LICENSE
```

## 安装

### 最简单的方式：告诉你的 AI 助手

直接拷贝下面这句话发给你的 AI 助手：

> 帮我安装金谷园饺子馆 Skill，仓库地址：https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill

Agent 会自动克隆仓库并安装到对应的 Skill 目录。

### 其他安装方式

**手动克隆到 Skill 目录：**

将本仓库克隆到你项目下的 Skill 目录，不同 IDE 对应的路径：

| IDE | Skill 目录 |
|-----|-------------|
| Qoder | `.qoder/skills/jinguyuan-dumpling-skill/` |
| Cursor | `.cursor/skills/jinguyuan-dumpling-skill/` |
| Trae | `.trae/skills/jinguyuan-dumpling-skill/` |
| Windsurf | `.windsurf/skills/jinguyuan-dumpling-skill/` |
| Claude Code | `.claude/skills/jinguyuan-dumpling-skill/` |
| 通用 | `.agents/skills/jinguyuan-dumpling-skill/` |

```bash
# 示例：安装到 Qoder
git clone https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill.git \
  .qoder/skills/jinguyuan-dumpling-skill
```

只要目录下有 `SKILL.md`，Agent 下次启动就会自动加载这个 Skill。

## 发布平台

- GitHub：https://github.com/JinGuYuan/jinguyuan-dumpling-skill
- Gitee：https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill

## 给 Agent 的接入信息

| 项目 | 说明 |
|------|------|
| MCP 端点 | https://mcp.jinguyuan.cloud |
| Skill 配置 | [`skill.json`](./skill.json) |
| 工具清单 | 以 MCP `tools/list` 返回为准 |

## 版本

版本号见顶部徽章，以 [`skill.json`](./skill.json) 为准。

> 说明：本 Skill 版本与内嵌排队组件（meituan-queue）版本独立演进，互不影响。

## License

[MIT](LICENSE)
