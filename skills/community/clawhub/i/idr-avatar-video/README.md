# 像衍数字人视频 Skill

An [Agent Skill](https://agentskills.io) for generating videos using [IDR](https://idr.ai) (idr) Digital Humans.

## Features

- 🎬 **Public Template Video**: 根据模板创建视频

```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 尝试第一个视频


```bash
# 列出公共数字人
python scripts/idr_video_client.py list_public_avatars

```

### 3. 设置Token

生成视频需要Token，请在官网注册获取 [neural-avatar.com/setting](https://www.neural-avatar.com):

```bash
export IDR_USER_TOKEN="your_token_here"
```

## 示例提示

如果你在agent平台使用它，尝试下面的提示词:

```
"列出公共数字人"
"使用一个专业的数字人生成一个欢迎视频"
```

## Documentation

- [SKILL.md](SKILL.md) - 完整的 skill 文档
- [references/](references/) - 参考API
  - [authentication.md](references/authentication.md) - 设置token
  - [avatars.md](references/avatars.md) - 选择数字人
  - [voices.md](references/voices.md) - 选择音色
  - [templates.md](references/templates.md) - 视频生成模板
  - [video-generation.md](references/video-generation.md) - 视频工作流

## API 参考

| Item | Value |
|------|-------|
| Base URL | `http://a1.neural-avatar.com:8004` |
| Auth | token via `Authorization` header |
| Token Source | [idr.ai](https://www.neural-avatar.com) |

## License

MIT - See [LICENSE](LICENSE) for details.
