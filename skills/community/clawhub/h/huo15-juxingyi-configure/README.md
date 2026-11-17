# 聚星逸配置 · huo15-juxingyi-configure

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>一个 Key 调 50+ 顶级大模型</h3>
<h3>接口实时拉取 · 自动写入 · 零本地硬编码</h3>

</div>

<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

<div align="center">

![Version](https://img.shields.io/badge/version-1.3.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Node](https://img.shields.io/badge/node-%3E%3D18.0-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-published-ff6b6b)

</div>

---

## 这是什么

`huo15-juxingyi-configure` 是 OpenClaw 专用 skill,帮你快速接入聚星逸(Juxingyi)大模型聚合平台:

1. **接口实时拉取**:每次运行都从聚星逸 `/v1/models` 接口获取最新可用模型列表
2. **自动写入**:`~/.openclaw/openclaw.json` 的 `fireworks-hub` provider 段
3. **主模型取列表第一个**:配完后主动询问是否切换
4. **日常更新**:`--update` 保留当前主模型,只刷新模型列表(平台新增模型后日常刷新)
5. **灵活切换**:随时用 `--switch` 换主模型
6. **安全可靠**:写入前自动备份,支持环境变量引用存储密钥

> **模型列表完全来自接口,不维护任何本地硬编码清单**——平台新增模型无需更新本 skill。
> 接入文档:https://fireworks-simulator.huo15.com/docs.html

---

## 快速开始

### 安装

```bash
# 从 ClawHub 安装(推荐)
clawhub install huo15-juxingyi-configure --dir ~/.openclaw/workspace/skills

# 或从源码安装
git clone https://cnb.cool/huo15/ai/huo15-skills.git
cp -r huo15-skills/huo15-juxingyi-configure/ ~/.openclaw/workspace/skills/
```

### 使用

**1. 获取聚星逸 API Key**

打开 [聚星逸控制台](https://fireworks-simulator.huo15.com/app/) →「API 密钥」页,创建一个 `fsk-` 开头的密钥。

**2. 运行配置脚本**

```bash
cd ~/.openclaw/workspace/skills/huo15-juxingyi-configure
node scripts/configure.mjs <fsk-key>
```

脚本调 `/v1/models` 接口拉取最新模型列表,自动写入 `~/.openclaw/openclaw.json`,主模型取接口返回列表的第一个。

**3. 重启 OpenClaw**

```bash
openclaw restart
```

> 完整操作流程见 [用户手册 SOP](docs/user-guide.md)

---

## 脚本命令

| 命令 | 说明 |
|------|------|
| `node configure.mjs <fsk-key>` | 首次配置:拉取模型列表并写入(主模型取列表第一个) |
| `node configure.mjs <fsk-key> --list` | 只列出接口返回的模型(不写文件) |
| `node configure.mjs <fsk-key> --update` | **日常更新模型列表(保留当前主模型)** |
| `node configure.mjs <fsk-key> --env` | 首次配置时用环境变量引用存储密钥(更安全) |
| `node configure.mjs --switch <model-id>` | 切换主模型(支持前缀匹配) |
| `node configure.mjs --show` | 查看当前聚星逸配置 |
| `node configure.mjs --help` / `-h` | 显示帮助 |
| `node configure.mjs --version` / `-v` | 显示版本号 |
| `node configure.mjs --help` / `-h` | 显示帮助 |
| `node configure.mjs --version` / `-v` | 显示版本号 |

---

## 模型列表来源

**模型列表完全来自聚星逸 `/v1/models` 接口实时返回,本 skill 不维护任何本地模型清单。**

脚本处理逻辑:
1. 调 `GET /v1/models` 拿到平台当前所有可用模型
2. 跳过生图/视频模型(ID 含 `image`/`seedream`/`t2v`/`i2v`/`video`/`dall-e`/`happyhorse`)——不能用于文本对话
3. 剩余文本模型全部写入配置
4. 主模型取接口返回列表的第一个,其余作 fallbacks

> **关于模型参数**:接口 `/v1/models` 只返回 `id`/`owned_by`,不返回上下文窗口等参数。脚本除 `id`/`name` 外填保守默认值(`contextWindow`: 131072, `maxTokens`: 8192, `reasoning`: false)保证 OpenClaw 可用,可手动调整。

---

## 安全建议

- **默认**:API Key 明文写入 `openclaw.json`,最简单
- **更安全**:加 `--env` 用环境变量引用:
  ```bash
  node configure.mjs <fsk-key> --env
  export FIREWORKS_API_KEY=fsk-你的密钥
  ```

---

## 文件结构

```
huo15-juxingyi-configure/
├── SKILL.md                       # ClawHub 嵌入源(≤ 25KB)
├── _meta.json                     # ClawHub 元数据
├── README.md                      # 本文件
├── CLAUDE.md                      # 开发规范
├── LICENSE                        # MIT
├── .gitignore                     # skill 级忽略
├── scripts/
│   └── configure.mjs              # 零依赖配置脚本(Node 18+)
└── docs/
    ├── prd.md                     # 产品需求文档
    ├── user-guide.md              # 用户手册 SOP
    ├── dev-guide.md               # 开发者 SOP
    └── changelog.md               # 版本变更历史
```

---

## 与其他 skill 协作

| 场景 | 配套 skill |
|------|-----------|
| 查询 token 用量/费用 | [`huo15-yh-usage`](../huo15-yh-usage/)(凭 fsk- 查账单)|

---

## 文档

| 文档 | 说明 |
|------|------|
| [用户手册 SOP](docs/user-guide.md) | 面向终端用户的标准操作流程 |
| [开发者 SOP](docs/dev-guide.md) | 面向接手开发的架构内幕、运维流程、踩坑经验 |
| [PRD](docs/prd.md) | 产品需求文档 |
| [变更历史](docs/changelog.md) | 版本变更记录 |

---

## License

[MIT](LICENSE) — 自由商用 / 修改 / 再发布。需保留版权声明 `Copyright (c) 2026 青岛火一五信息科技有限公司`。

---

<div align="center">

**公司名称:** 青岛火一五信息科技有限公司

**联系邮箱:** postmaster@huo15.com | **QQ群:** 1093992108

---

**关注逸寻智库公众号,获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>
