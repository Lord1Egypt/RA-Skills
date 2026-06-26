# jisilu-cb-daily Skill

集思录可转债每日数据收集 Skill，支持抓取基本数据、强赎倒计时、下修倒计时。

## 目录结构

```
jisilu-cb-daily/
├── SKILL.md                          # Skill 核心定义文件
├── scripts/
│   └── collect_jisilu_cb.py          # Python 数据抓取脚本
├── references/
│   └── cookie.json                   # Cookie 存储文件（首次运行自动生成）
└── output/                           # 数据输出目录
    └── jisilu_cb_YYYY-MM-DD.csv
```

## 安装方法

### 本地 OpenClaw / Kimi Code CLI

```bash
# 解压到 Skill 目录
unzip jisilu-cb-daily.zip -d ~/.config/agents/skills/

# 安装依赖
pip install requests pandas

# 首次运行（会提示输入 Cookie）
cd ~/.config/agents/skills/jisilu-cb-daily
python scripts/collect_jisilu_cb.py
```

### 云端 Kimi Claw

目前云端 Kimi Claw 主要通过 **ClawHub** 安装官方/社区 Skill。自定义 Skill 建议：
1. 先在本地 OpenClaw 调试验证
2. 通过对话方式让 Kimi Claw 按 SKILL.md 内容执行（见下方"替代方案"）

## 使用方法

### 方式1：命令行直接运行（本地）

```bash
python scripts/collect_jisilu_cb.py
```

首次运行会提示输入 `kbzw__user_login` Cookie，后续自动读取。

### 方式2：通过 Kimi Claw / OpenClaw 调用

在对话中发送：
```
使用 jisilu-cb-daily skill 抓取今日可转债数据
```

### 方式3：定时任务（本地）

```bash
# crontab -e
# 每天 15:30 执行
30 15 * * * cd ~/.config/agents/skills/jisilu-cb-daily && python scripts/collect_jisilu_cb.py >> output/cron.log 2>&1
```

## 获取 Cookie 方法

1. 用 Chrome/Edge 打开 https://www.jisilu.cn/ 并登录账号
2. 按 F12 打开开发者工具
3. 切换到 Application（应用）→ Cookies → https://www.jisilu.cn
4. 找到 `kbzw__user_login`，复制其 Value
5. 粘贴给 Skill 或写入 `references/cookie.json`

## 数据源

- 基本数据：https://www.jisilu.cn/web/data/cb/list
- 强赎数据：https://www.jisilu.cn/web/data/cb/redeem
- 下修数据：https://www.jisilu.cn/web/data/cb/adjust

## 注意事项

- Cookie 需要集思录登录状态，部分数据可能需要会员权限
- 建议每日 15:00 收盘后执行，此时数据最完整
- 如遇接口变更，可能需要更新脚本中的字段解析逻辑
