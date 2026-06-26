# jisilu-cb-daily Skill

集思录可转债每日数据收集 Skill，基于 webapi 接口，以 adjust 下修全量数据为主表合并强赎和基础字段。

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

## 使用方法

### 方式1：命令行直接运行（本地）

```bash
python scripts/collect_jisilu_cb.py
```

首次运行会提示输入 `kbzw__user_login + kbzw__Session` Cookie，后续自动读取。

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
4. 分别找到 `kbzw__user_login` 和 `kbzw__Session`，复制各自的 Value
5. 依次粘贴给 Skill，或写入 `references/cookie.json`

## 数据源

- 基本数据：`https://www.jisilu.cn/webapi/cb/list/`
- 强赎数据：`https://www.jisilu.cn/webapi/cb/redeem/`
- 下修数据：`https://www.jisilu.cn/webapi/cb/adjust/`

## 数据合并逻辑

1. **主表**：`adjust` 接口（约340条全量数据）
2. **LEFT JOIN**：`redeem` 强赎字段（仅部分转债有强赎数据）
3. **LEFT JOIN**：`list` 基础字段（价格、溢价率等）

## 注意事项

- 接口地址末尾必须带斜杠 `/`
- webapi 返回的是平铺数组 `data`，不是 `rows->cell` 嵌套结构
- Cookie 需要集思录登录状态，部分数据可能需要会员权限
- 建议每日 15:00 收盘后执行，此时数据最完整
