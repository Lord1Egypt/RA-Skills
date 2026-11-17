# OpenClaw NovelAI

[English README](README.md) | 简体中文

这是一个面向 NovelAI 小说创作和图片工作流的非官方 OpenClaw Skill。

本项目在 NovelAI 文字生成和上游 [NovelAI-Image-MCP](https://github.com/xinvxueyuan/NovelAI-Image-MCP) 之上增加工作流层，帮助 OpenClaw Agent 管理小说上下文、规划章节插图、选择图片操作、在高消耗操作前请求确认，并记录可复现的创作素材。

Skill 内部名称是 `openclaw-novelai`，ClawHub slug 是 `novelai-workflows`。

- GitHub：[techotaku39/openclaw-novelai](https://github.com/techotaku39/openclaw-novelai)
- ClawHub：[@techotaku39/novelai-workflows](https://clawhub.ai/techotaku39/skills/novelai-workflows)
- 从 ClawHub 安装：`openclaw skills install @techotaku39/novelai-workflows`

> 本项目与 OpenClaw 或 NovelAI 没有隶属、赞助或官方认可关系。

## 功能

- 从 `canon.md`、`memory.md`、`lorebook.md` 和 `style.md` 维护有长度限制的小说上下文。
- 支持大纲、续写、改写、审阅和总结工作流。
- 通过 OpenAI 兼容的模型提供商编排 NovelAI 文字模型。
- 将图片操作交给上游 NovelAI Image MCP Server 执行。
- 在当前服务器提供对应工具时，支持文生图、多角色提示、图生图、局部重绘、Vibe、Director、ControlNet 标注、标签建议以及账户/费用查询。
- 在不保存凭据的前提下记录模型、Prompt、Seed、尺寸、工具和输出路径。
- 包含脱敏的真实 API 能力测试套件和离线契约测试。

这个 Skill 是工作流编排指南，不是图片 API 的替代实现。真正调用 NovelAI 图片接口的是独立的 MCP Server。

## 文档

- [English README](README.md)
- [英文完整使用手册](docs/FULL-USER-MANUAL.md)
- [英文快速入门指南](docs/QUICK-START.md)
- [中文完整使用手册](docs/完整使用手册.md)
- [中文快速入门用法](docs/快速入门用法.md)
- [英文费用与额度说明](docs/COSTS-AND-QUOTAS.md) —— NovelAI Anlas、Opus 免费生图和 V5 使用额度。
- [中文费用与额度说明](docs/费用与额度说明.md)
- [英文零 Anlas 变体](variants/openclaw-novelai-free/README.md) —— 严格禁止付费图片操作的变体。
- [中文零 Anlas 变体](variants/openclaw-novelai-free/README.zh-CN.md)
- [英文 Opus 免费增强变体](variants/openclaw-novelai-opus-free/README.md) —— 放行实测为零 Anlas 的图生图、局部重绘和部分 Director 工具。
- [中文 Opus 免费增强变体](variants/openclaw-novelai-opus-free/README.zh-CN.md)
- [兼容性说明](COMPATIBILITY.md) —— 已脱敏的能力和限制摘要。

## 仓库结构

```text
SKILL.md
README.md
README.zh-CN.md
LICENSE
NOTICE.md
SECURITY.md
CONTRIBUTING.md
CHANGELOG.md
.clawhubignore
docs/
  COSTS-AND-QUOTAS.md
  FULL-USER-MANUAL.md
  QUICK-START.md
  费用与额度说明.md
  完整使用手册.md
  快速入门用法.md
variants/
  openclaw-novelai-free/
    SKILL.md
  openclaw-novelai-opus-free/
    SKILL.md
    README.md
    README.zh-CN.md
examples/
  openclaw.config.example.json5
scripts/
  project_state.py
  live_api_test.py
tests/
  test_project_state.py
  test_live_api_test.py
  test_skill_contract.py
```

`SKILL.md` 保留在仓库根目录，这样可以作为本地 Skill 或 Git 仓库 Skill 安装到 OpenClaw。

## 运行架构

参考配置使用：

- NovelAI 文字提供商：`https://text.novelai.net/oa`；
- 文字模型：`xialong-v1` 和 `glm-4-6`；
- 上游图片 MCP：`novelai-image-mcp==0.4.0`；
- 凭据来源：由主机管理的 `NOVELAI_TOKEN` 环境变量，或等效的 SecretRef。

请将凭据放在仓库、Prompt、日志、生成元数据和命令参数之外。不要把示例配置中的 `${NOVELAI_TOKEN}` 替换成真实值后提交。

配置关系见 [examples/openclaw.config.example.json5](examples/openclaw.config.example.json5)。请把它合并到已有的 OpenClaw 配置中，不要覆盖无关设置。

## 使用示例

```text
读取当前项目的 canon、memory、lorebook 和 style，为第三章提出三个走向；写正文前先等我确认。
```

```text
找出第三章的关键场景，拟定配图 Prompt，估算总消耗；在生成任何内容前先等我确认。
```

```text
用这张图片做图生图，保留脸部和构图，把背景改成雨夜街道，保留原图并将结果保存为新素材。
```

```text
使用这张图片和遮罩，只重绘右手，保持所有未遮罩区域不变，并记录生成参数。
```

## 安全行为

Skill 会要求 Agent：

- 不在聊天中索要或重复 NovelAI Token；
- 在使用特定模型或图片功能前检查当前可用的 MCP 工具；
- 在模糊或批量图片任务前展示模型、尺寸、步数、样本数和预计费用；
- 保留原图，把编辑结果写入独立文件；
- 在不包含凭据的前提下记录安全元数据；
- 操作失败时如实报告失败，不虚构输出结果。

启用第三方 Skill 和 MCP Server 前应先检查其内容。上游 MCP Server 是独立依赖，请单独阅读它的许可证和安全说明。

## 当前兼容性说明

随附的 API 测试套件于 2026-09-05 运行，验证了账户访问、Xialong 补全、GLM-4.6 流式聊天、V5/V4.5 图片生成、多角色提示、图生图、局部重绘、Vibe、标签建议、ControlNet 标注和 Director 工具。

- GLM-4.6 建议使用流式输出；非流式请求可能返回 HTTP 200，但文本为空。
- NovelAI 专用 `/ai/upscale` 路径在测试的两个图片主机上均返回 404。只有当前服务器确实返回图片时，才能认为 `upscale_image` 可用；较大尺寸图生图或本地放大器属于不同的替代操作。
- 目标 OpenClaw 主机仍需单独完成 MCP 握手和工具发现检查。

NovelAI 和 OpenClaw 可能独立更新。修改上游版本固定值前，应重新运行真实 smoke suite，并更新 `COMPATIBILITY.md`。

## 开发检查

离线测试套件不应需要 Token：

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts\project_state.py scripts\live_api_test.py tests\test_project_state.py tests\test_skill_contract.py tests\test_live_api_test.py
```

真实测试套件是主动执行的，并且只从进程环境读取 `NOVELAI_TOKEN`。不要把凭据粘贴进命令，也不要提交真实测试输出。

## 发布

推荐的分发方式：

1. 使用 GitHub 作为源码主仓库。
2. 为版本创建 Tag，并保持 `SKILL.md` frontmatter 中的名称稳定。
3. 将 Skill 发布或同步到 [ClawHub](https://clawhub.ai/)，slug 使用 `novelai-workflows`。
4. 不要把生成图片、账户报告、`.env` 文件、缓存和压缩包提交到公开仓库。

发布前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md) 和 [NOTICE.md](NOTICE.md)。

## 参考资料

- [OpenClaw Skills](https://docs.openclaw.ai/skills)
- [OpenClaw ClawHub 快速开始](https://docs.openclaw.ai/clawhub/quickstart)
- [NovelAI Image MCP](https://github.com/xinvxueyuan/NovelAI-Image-MCP)
- [NovelAI 图片模型](https://docs.novelai.net/en/image/models/)
- [NovelAI 文字模型](https://docs.novelai.net/en/text/models/)
- [NovelAI Persistent API Token](https://docs.novelai.net/en/text/usersettings/account/)
