# MGTV Skill 快速开始指南

## 🎬 功能概述

MGTV Skill 是一个芒果 TV 视频搜索与播放工具，使用芒果 TV 官方搜索 API，能够智能匹配最相关的视频并在系统浏览器中自动播放。

### 核心功能

- ✅ **官方 API 搜索**：使用芒果 TV 官方搜索接口 `mobileso.bz.mgtv.com`
- ✅ **智能匹配**：自动选择最相关的视频结果
- ✅ **优先播放**：智能识别有正片内容的结果
- ✅ **自动打开**：在系统默认浏览器中打开播放页面
- ✅ **支持多种内容**：综艺、电视剧、电影、动漫等

## 📦 安装

### 方法 1：手动安装（推荐）

Skill 已位于 `/Users/bilong/opencode/skills/mgtv`

```bash
# 验证安装
cd /Users/bilong/opencode/skills/mgtv
node scripts/search-mgtv.js --query "测试"
```

### 方法 2：使用 ClawHub

```bash
# 发布到 ClawHub
cd /Users/bilong/opencode/skills/mgtv
clawhub publish . --slug mgtv --name "MGTV" --version 1.0.0

# 在其他项目安装
clawhub install mgtv
```

## 🚀 快速使用

### 基本使用

```bash
# 搜索并播放
node scripts/search-mgtv.js --query "节目名称"

# 示例
node scripts/search-mgtv.js --query "乘风破浪的姐姐"
node scripts/search-mgtv.js --query "歌手 2024"
node scripts/search-mgtv.js --query "大侦探"
```

### 运行效果

```
============================================================
MGTV - 芒果 TV 视频搜索与播放
============================================================
搜索关键词：乘风破浪的姐姐
============================================================
正在搜索：乘风破浪的姐姐...

找到 9 个结果:
============================================================
1. 乘风破浪的姐姐 (节目)
   └─ 包含视频：2020-06-12 第 1 期（上）：30 位姐姐集结
2. 乘风破浪的姐姐 第二季 (类型 1)
3. 乘风破浪的姐姐 舞台完整版 (类型 1)
...
============================================================

✓ 选择：乘风破浪的姐姐
============================================================

正在打开浏览器：https://www.mgtv.com/b/338497/8337559.html?fpa=se
✓ 已在浏览器中打开

✓ 操作完成！
正在播放视频，享受观看！
```

## 📖 使用场景

### 场景 1：搜索综艺节目

```bash
# 搜索特定综艺
node scripts/search-mgtv.js --query "歌手"
node scripts-search-mgtv.js --query "明星大侦探"
node scripts/search-mgtv.js --query "你好星期六"

# 搜索特定年份
node scripts/search-mgtv.js --query "歌手 2024"
```

### 场景 2：搜索电视剧

```bash
node scripts/search-mgtv.js --query "繁花"
node scripts/search-mgtv.js --query "庆余年"
node scripts/search-mgtv.js --query "长相思"
```

### 场景 3：直接打开视频链接

```bash
# 已知道视频 URL
node scripts/search-mgtv.js --direct-url "https://www.mgtv.com/b/338497/8337559.html"
```

### 场景 4：在 OpenClaw 中使用

安装 skill 后，在 OpenClaw 中直接使用自然语言：

```
用户：我想看《乘风破浪的姐姐》
助手：正在搜索芒果 TV 的《乘风破浪的姐姐》...
     已找到相关视频，正在打开浏览器...
     ✓ 已在浏览器中打开第一集

用户：播放《歌手 2024》
助手：搜索《歌手 2024》...
     正在打开播放页面...

用户：帮我找一下何炅主持的综艺节目
助手：搜索何炅主持的综艺节目...
     找到《你好，星期六》，正在打开...
```

## ⚙️ 命令行参数

| 参数 | 说明 | 类型 | 示例 |
|------|------|------|------|
| `--query` | 搜索关键词 | 必填 | `"歌手 2024"` |
| `--direct-url` | 直接打开的 URL | 可选 | `"https://..."` |
| `--show-all` | 打开搜索页面（不自动选择） | 可选 | `--show-all` |

### 参数示例

```bash
# 基本搜索
node scripts/search-mgtv.js --query "大侦探"

# 打开搜索页面让用户手动选择
node scripts/search-mgtv.js --query "综艺" --show-all

# 直接打开指定视频
node scripts/search-mgtv.js --direct-url "https://www.mgtv.com/b/xxx/xxx.html"
```

## 🔧 技术细节

### 使用的 API

```
https://mobileso.bz.mgtv.com/pc/suggest/v1
```

**请求参数：**
- `q`: 搜索关键词
- `pc`: 返回结果数量（默认 10）
- `src`: 来源标识（mgtv）
- `did`: 设备 ID（随机生成）
- `_support`: 支持标识

**返回数据结构：**
```json
{
  "code": 200,
  "data": {
    "suggest": [
      {
        "title": "节目名称",
        "showTitle": "显示标题",
        "type": 1,
        "typeName": "节目",
        "url": "//www.mgtv.com/xxx.html",
        "videoList": [
          {
            "title": "视频标题",
            "url": "//www.mgtv.com/b/xxx/xxx.html"
          }
        ]
      }
    ]
  }
}
```

### 智能匹配逻辑

1. **优先级 1**：有 `videoList` 的结果（包含具体剧集）
2. **优先级 2**：有 `url` 字段的结果（节目主页）
3. **优先级 3**：打开搜索页面让用户选择

### 支持的操作系统

- **macOS**: 使用 `open` 命令
- **Windows**: 使用 `start` 命令
- **Linux**: 使用 `xdg-open` 命令

## 🧪 测试

```bash
# 运行完整测试套件
node scripts/test.js

# 测试不同类型的搜索
node scripts/search-mgtv.js --query "歌手"        # 综艺
node scripts/search-mgtv.js --query "繁花"        # 电视剧
node scripts/search-mgtv.js --query "乘风破浪"    # 有 videoList 的结果
```

## ⚠️ 注意事项

1. **网络连接**：需要能够访问芒果 TV 网站
2. **浏览器**：系统需要有默认浏览器
3. **VIP 内容**：部分视频需要芒果 TV 会员账号
4. **地区限制**：某些内容可能有地区限制

## 🐛 故障排除

### 问题 1：搜索结果为空

**原因**：关键词不明确或网络问题

**解决**：
- 使用更精确的节目名称
- 检查网络连接
- 尝试其他关键词

### 问题 2：浏览器无法打开

**原因**：系统命令缺失

**解决**：
- macOS: 确认 `open` 命令可用
- Windows: 使用命令提示符或 PowerShell
- Linux: 安装 `xdg-utils`

```bash
# Linux 安装
sudo apt-get install xdg-utils  # Debian/Ubuntu
sudo yum install xdg-utils      # CentOS/RHEL
```

### 问题 3：视频无法播放

**原因**：VIP 限制或地区限制

**解决**：
- 登录芒果 TV 账号
- 清除浏览器缓存
- 检查是否需要会员

## 📝 更新日志

### v1.0.0 (2024-04-10)

- ✅ 使用芒果 TV 官方搜索 API
- ✅ 智能匹配最相关的视频
- ✅ 支持直接打开视频链接
- ✅ 支持搜索页面展示
- ✅ 跨平台支持（macOS/Windows/Linux）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**免责声明**：本 Skill 仅供学习交流使用，请支持正版视频内容。
