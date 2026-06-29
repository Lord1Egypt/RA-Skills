# 大模型Token成本节约 · WorkBuddy Skill

> 本技能是对开源项目 [headroom](https://github.com/chopratejas/headroom)（by **chopratejas**，MIT License）的 WorkBuddy Skill 封装。所有核心压缩能力来自 headroom 项目，本仓库仅提供封装层和使用说明。

"大模型 Token 成本节约工具。在请求到达大模型之前自动压缩 prompt 和上下文，减少 60-95% 的 token 消耗，直接降低 API 成本。支持 Claude/OpenAI/Gemini 等主流模型，提供代理模式、CLI 包装、Python SDK 和 MCP Server 四种接入方式。"

## 特性

- 请参考 SKILL.md 中的详细说明

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「大模型Token成本节约」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/workbuddy-llm-token-compressor.git \
  ~/.workbuddy/skills/llm-token-compressor
```

### 环境依赖

请参考 SKILL.md 中的环境要求章节

## 使用

```bash
python3 scripts/pipeline.py <参数>
```

详细参数请参考 SKILL.md

## 输出

请参考 SKILL.md

## 项目结构

```
.gitignore
LICENSE
SKILL.md
assets
references
references/api_reference.md
references/headroom_api.md
scripts
```

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」|
| 💬 公众号 | 微信搜「桂皮AI实战」|
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) — AI工具 · 创作 · 产品 · 流量 · 变现 |
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意）|

## License

MIT License — 详见 [LICENSE](./LICENSE)

原项目 headroom 版权归 chopratejas 所有，本封装遵循相同的 MIT 协议。
