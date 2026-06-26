# pixiv-skill

Pixiv 自动化技能（Cookie 鉴权模式）。

## 目录结构

- `SKILL.md`：给 AI 的技能说明与执行流程
- `scripts/pixiv.py`：主入口（推荐）
- `scripts/latest_rank.py`：轻量榜单抓取脚本
- `scripts/get_rank.py`：旧兼容脚本
- `config.example.yaml`：配置模板

## 配置

复制配置并填写 Cookie：

```bash
cp config.example.yaml config.yaml
```

最小示例：

```yaml
pixiv:
  cookie: "PHPSESSID=你的值;"
  proxy: ""
  download_dir: "./downloads"
  r: false
  auto_download: false
```

## 常用命令

```bash
python3 scripts/pixiv.py status
python3 scripts/pixiv.py rank --type day --lookback 2
python3 scripts/pixiv.py search --keyword "初音ミク"
python3 scripts/pixiv.py cache
python3 scripts/pixiv.py download --id 12345678
```

## 说明

- 默认先缓存元信息，不自动下载图片
- 图片直链可能被防盗链拦截，建议下载后再发送
