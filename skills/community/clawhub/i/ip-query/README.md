# IP查询技能

一个用于查询当前公共IP地址的OpenClaw技能。

## 功能特性

- ✅ 查询当前公共IP地址
- ✅ 获取地理位置信息（城市、地区、国家）
- ✅ 获取网络信息（ISP、组织）
- ✅ 多种输出格式（简单、详细、JSON）
- ✅ 多API备用，提高可靠性
- ✅ 友好的中文界面

## 安装

将此技能目录复制到OpenClaw的技能目录中：

```bash
# 方法1: 使用clawhub（推荐）
clawhub install ip-query

# 方法2: 手动安装
cp -r ip-query ~/.openclaw/workspace/skills/
```

## 使用方法

### 在OpenClaw中
当您提到以下关键词时，技能会自动激活：
- "我的IP地址"
- "查询IP"
- "公网IP"
- "当前IP"
- "ip address"
- "my ip"

### 命令行使用
您也可以直接运行脚本：

```bash
# 简单模式（仅显示IP）
./scripts/ip_query.sh --simple

# 详细模式（显示所有信息）
./scripts/ip_query.sh --detail

# JSON格式输出
./scripts/ip_query.sh --json
```

## 示例

### 示例1：简单查询
```
用户：我的IP地址是多少？

技能：🌐 您的公共IP地址: 123.45.67.89
```

### 示例2：详细查询
```
用户：查询我的IP详细信息

技能：
🌐 您的公共IP地址: 123.45.67.89

📍 位置信息:
- 城市: 北京
- 地区: 北京市
- 国家: 中国
- 经纬度: 39.9042, 116.4074

🏢 网络信息:
- ISP: 中国电信
- 组织: China Telecom

🔒 隐私提示: 这是您的公网IP地址，请勿随意分享。
```

## 技术细节

### 使用的API
1. **主要API**: `https://api.ipify.org` - 获取简单IP
2. **详细信息API**: `https://ipinfo.io` - 获取地理位置和网络信息
3. **备用API**: 
   - `https://icanhazip.com`
   - `https://ifconfig.me/ip`
   - `https://ipecho.net/plain`

### 依赖
- `curl` - HTTP客户端
- `jq` (可选) - JSON解析器

## 隐私说明

- 此技能仅查询公共IP地址，不涉及私人网络信息
- 使用第三方API，数据可能被API提供商记录
- 建议仅在需要时查询IP信息

## 许可证

MIT License