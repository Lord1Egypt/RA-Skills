# ProFind Skill

> OpenClaw 技能封装：macOS 专业文件搜索工具 ProFind 的 AppleScript + URL Scheme + Shell 自动化接口。

[![Platform](https://img.shields.io/badge/platform-macOS%2010.14%2B-blue)](https://apps.apple.com/app/id1559203395)
[![ProFind Version](https://img.shields.io/badge/ProFind-1.0%2B-green)](https://apps.apple.com/app/id1559203395)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

---

## 功能总览

| 功能 | 说明 | 调用方式 |
|------|------|---------|
| `find_files` | 文件名搜索（Spotlight 毫秒级） | URL Scheme |
| `find_content` | 内容/元数据搜索 | URL Scheme |
| `find_advanced` | 高级组合搜索（大小/日期/类型） | URL Scheme |
| `run_script` | 脚本钩子批量操作 | AppleScript |
| `open_search_window` | 打开搜索窗口（可预填查询词） | AppleScript |
| `query_api` | Media Server HTTP API（UPnP SOAP） | HTTP + SOAP |

---

## 快速开始

### 前置要求

```bash
# 1. 安装 ProFind（macOS 10.14+）
open "https://apps.apple.com/app/id1559203395"

# 2. 授予完全磁盘访问权限
#    系统偏好设置 → 隐私与安全性 → 完全磁盘访问 → 勾选 ProFind
```

### 基本搜索

```bash
# 搜索文件
osascript -e 'tell application "ProFind" to open location "profind:search?name=report&kind=PDF"'

# 搜索近一个月修改的 PDF
osascript -e 'tell application "ProFind" to open location "profind:search?name=report&kind=PDF&date=modified:~month"'

# 搜索大于 10MB 的视频
osascript -e 'tell application "ProFind" to open location "profind:search?name=*&kind=movie&size=larger:10MB"'
```

---

## 项目结构

```
profind-skill/
├── README.md
├── SKILL.md                          # 技能主文档（OpenClaw Skill 格式）
├── LICENSE
├── .github/
│   └── workflows/
│       └── validate.yml              # CI 验证脚本（搜索 + 脚本钩子）
├── docs/
│   ├── API-REFERENCE.md              # API 详细参考
│   ├── URL-SCHEME.md                # URL Scheme 参数速查
│   └── SAMPLE-SCRIPTS.md            # 自定义脚本示例
├── scripts/
│   ├── install.sh                    # 一键安装脚本（安装 ProFind + 配置权限）
│   └── profind-cli.sh               # 命令行封装工具
└── sample-scripts/
    ├── custom/                      # 自定义脚本示例
    │   ├── BatchRename.sh           # 批量重命名
    │   └── SendFilePathsViaMail.scpt  # 发送文件路径邮件
    └── README.md                    # 脚本使用说明
```

---

## 六大功能详解

### 1. find_files — 文件名搜索

基于 Spotlight 索引，毫秒级返回。

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=report.pdf&path=~/Documents"
end tell
EOF
```

### 2. find_content — 内容/元数据搜索

支持按内容、作者、UTI、元数据搜索。

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    -- 按标签搜索
    open location "profind:search?name=doc&label=red"
    -- 按大小搜索
    open location "profind:search?name=*&size=larger:1GB"
end tell
EOF
```

### 3. find_advanced — 高级组合搜索

多条件组合搜索。

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=*.swift&path=/Users/Admin/Projects&exclude:/Users/Admin/Projects/node_modules&date=modified:~month"
end tell
EOF
```

### 4. run_script — 脚本钩子

内置 9 个脚本钩子，支持自定义扩展。

```bash
# 调用内置 DuckDuckGo 搜索
osascript -e 'tell application "ProFind" to open location "profind:search?name=keyword&script=duckduckgo"'
```

### 5. open_search_window — 打开搜索窗口

```bash
osascript -e 'tell application "ProFind" to activate'
```

### 6. query_api — Media Server HTTP API

UPnP SOAP 协议，运行于端口 54812。

```bash
# 获取搜索能力
curl -s --max-time 10 -X POST "http://localhost:54812/ContentDirectory/control" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#GetSearchCapabilities"'
```

> ⚠️ Media Server 展示的是 ProFind UI 中的最近搜索结果，不是独立索引。
> 需要先在 ProFind 中执行搜索，再通过 SOAP 查询。

---

## 开发说明

### 本地测试

```bash
# 验证 ProFind 是否安装
[ -d "/Applications/ProFind.app" ] && echo "已安装" || echo "未安装"

# 验证 URL Scheme
osascript -e 'tell application "ProFind" to open location "profind:search?name=test"'

# 验证 Media Server
curl -s --max-time 3 -o /dev/null -w "%{http_code}" "http://localhost:54812/"
```

### 安装到 OpenClaw

```bash
# 将 SKILL.md 复制到 OpenClaw 技能目录
cp SKILL.md ~/Library/Application\ Support/QClaw/openclaw/config/skills/profind-skill/
```

---

## 贡献

欢迎提交 Issue 和 Pull Request！  
.问题反馈：441457345@qq.com  
.技能来源：nanobot@Qclaw  

## 许可证

[MIT License](LICENSE)
