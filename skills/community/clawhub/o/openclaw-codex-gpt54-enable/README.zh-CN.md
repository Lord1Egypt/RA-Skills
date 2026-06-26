# OpenClaw Codex GPT-5.4 启用技能

这是一个可复用的 OpenClaw 技能，用来沉淀一套**低风险、可回滚、可验证**的流程：在**不重编译 OpenClaw** 的前提下，通过配置层补丁启用 `openai-codex/gpt-5.4`。

## 仓库内容

- `SKILL.md`：真正的 OpenClaw 技能文件
- `README.md`：英文说明
- `README.zh-CN.md`：中文说明
- `LICENSE`：MIT 许可证

## 为什么要做这个技能

实际使用中，经常会碰到这种情况：

- `openai/gpt-5.4` 已经能在 OpenClaw 里看到
- 但 `openai-codex/gpt-5.4` 还没有放开
- 或者显示 `not allowed`
- 或者本地配置里压根没注册这条模型路由

这个技能把一次真实实战经验，整理成可复用 SOP：

1. 先确认当前模型支持情况
2. 不碰安装目录，优先改 `~/.openclaw/openclaw.json`
3. 新增 `openai-codex` provider
4. 补上 `gpt-5.4` 模型定义
5. 补上别名和 fallback
6. 用 `openclaw models list` 做静态校验
7. 用 `session_status` 做真实调用校验

## 核心思路

优先采用**配置层补丁**，而不是直接修改 Homebrew 安装目录里的打包 JS：

- 风险更低
- 回滚更简单
- 验证速度更快
- 更适合先跑通、再沉淀

## 适用场景

当你满足下面条件时，这个技能就很好用：

- `openai/gpt-5.4` 已经存在
- `openai-codex/gpt-5.4` 不存在或不可用
- 你想要一套可重复执行的启用流程
- 你不想上来就改安装包或重编译

## 快速流程

```bash
# 1）查看当前模型
openclaw models list --plain | grep 'gpt-5.4'

# 2）备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)

# 3）修改 ~/.openclaw/openclaw.json
#    - 新增 models.providers.openai-codex
#    - 新增 gpt-5.4 模型
#    - 新增 GPT54Codex 别名
#    - 新增 fallback: openai-codex/gpt-5.4

# 4）校验注册结果
openclaw models list --plain | grep 'openai-codex/gpt-5.4'
```

然后在 OpenClaw 会话里进一步验证：

```text
session_status(model='openai-codex/gpt-5.4')
```

## 这个仓库适合谁

- OpenClaw 深度用户
- 想测试新模型路由的人
- 想把“踩坑经验”沉淀成技能资产的人

## 注意事项

不同版本的 OpenClaw，`openclaw.json` 字段可能略有不同。请把示例配置**合并**进你当前的真实结构里，不要盲目整文件覆盖。

## 许可证

MIT
