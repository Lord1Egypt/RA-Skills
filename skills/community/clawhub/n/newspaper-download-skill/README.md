# newspaper-download

报刊 PDF 下载工具 — 基于 [pick-read.vip](https://pick-read.vip) 接口，查询已收录的国际报刊更新，获取 PDF 下载链接。

## 功能

- **查看更新** — 查询今天/近期更新了哪些报纸、杂志
- **定位期次** — 按报纸名称和日期定位指定期次
- **获取下载链接** — 批量获取 PDF 下载链接

## 支持平台

本工具以 Skill 方式运行在以下 AI 平台：

| 平台 | 地址 |
|---|---|
| QClaw | https://qclaw.qq.com/ |
| WorkBuddy | https://copilot.tencent.com/work/ |
| OpenClaw | https://github.com/openclaw/openclaw |

## 快速开始

1. 下载本仓库（Code → Download ZIP）
2. 编辑 `config.json`，填入你的导入令牌：

```json
{
    "api_base": "https://pick-read.vip/api",
    "import_token": "imp-你的令牌填这里"
}
```

3. 在支持 Skills 的平台中安装本工具，即可直接使用

**导入令牌在哪里获取？** 登录 [pick-read.vip](https://pick-read.vip) → 账户页 → 导入令牌 → 生成令牌。

## 推荐提示词

```
查看今天更新了什么内容，并给出下载地址
查看金融时报是否更新，并给出下载地址
查看 2026-03-01 的更新内容并提供下载地址
```

## 命令行使用

```bash
# 查看今天更新
python3 scripts/get_data.py updates --no-save

# 查看最近 3 天更新
python3 scripts/get_data.py updates --days 3 --no-save

# 查询某一期信息 + 下载链接
python3 scripts/get_data.py issue-info "Financial Times" --issue-date 2026-03-27 --token imp-xxxx --no-save

# 今天所有新增期次的下载链接
python3 scripts/get_data.py download-links --token imp-xxxx --no-save
```

## 说明

- 查询接口不需要认证，任何人都可以查看更新
- 下载链接需要有效的 Import Token
- 无 token 时仍返回期次信息，但下载链接为空
- 本工具无第三方依赖，仅使用 Python 标准库
