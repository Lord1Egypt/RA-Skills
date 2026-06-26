# KreadoAI Skill v1.1.0

KreadoAI 官方技能，支持数字人视频生成、文字转语音、即时形象克隆、视频字幕/水印去除。

## 环境要求

- Node.js 18+
- KreadoAI Pro 会员及 API Token

## 配置

1. 注册 [kreadoai.com](https://www.kreadoai.com/)
2. 升级为 Pro 会员
3. 获取 API Token：账号总览 -> API 设置
4. 配置方式：

```bash
export KREADO_API_TOKEN="your_api_token"
# 或者
node scripts/kreado.mjs account --configure
```

## 使用方法

```bash
node scripts/kreado.mjs <子命令> [选项]
```

| 命令 | 说明 |
| --- | --- |
| `account` | 账号信息、配置凭证 |
| `avatar` | 数字人形象管理 |
| `video` | 视频生成 |
| `clone` | 即时形象克隆 |
| `tts` | 文字转语音 |
| `subtitle` | 字幕/水印去除 |

运行 `node scripts/kreado.mjs <子命令> --help` 查看详细用法。
