# SKILL.md - 金十快讯技能

## 功能

获取金十金融快讯，支持以下命令：

- `jin10` - 获取最近快讯（从本地缓存读取，秒开）
- `细说N` - 查看第N条详情
- `展开说说N` - 深度分析（港股/恒生科技/腾讯/阿里影响）

## 架构

### 后台抓取（jin10_fetcher.py）
- 守护进程模式运行
- 每2-10分钟随机间隔抓取快讯
- 数据源：jin10.com 主页 + 详情页
- 缓存路径：`/tmp/jin10_cache/YYYYMMDD-HH.json`
- 自动清理超过24小时的旧缓存

### 前端读取（jin10_push.py）
- 直接从本地缓存读取，无需网络请求
- 支持 detail/deep 命令做深度分析

### 分析模块（jin10_analysis.py）
- 深度分析港股、恒生科技、腾讯(00700)、阿里(09988)影响
- 风险等级评估
- 相关个股推荐

## 使用方法

```bash
# 手动抓取一次数据
python3 /root/.openclaw/workspace/scripts/jin10_fetcher.py once

# 启动后台守护进程
python3 /root/.openclaw/workspace/scripts/jin10_fetcher.py daemon

# 读取快讯
python3 /root/.openclaw/workspace/scripts/jin10_push.py recent

# 查看详情
python3 /root/.openclaw/workspace/scripts/jin10_push.py detail 3

# 深度分析
python3 /root/.openclaw/workspace/scripts/jin10_push.py deep 3
```

## 性能

- 脚本执行：< 0.01秒（本地缓存读取）
- 响应速度：秒开

## 依赖

- Python 3
- requests
- concurrent.futures (标准库)

## x-token

用于金十网站访问：参考 TOOLS.md
