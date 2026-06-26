# Map Address Query Skill

[English](#english) | [中文](#chinese)

---

<a id="english"></a>
## English

### Overview
A skill that provides map service address lookup and distance-query workflows. Currently supports Tencent Location Service (QQ Map).

It enables AI agents and users to:
- Convert a natural language address to geographic coordinates (Latitude/Longitude).
- Measure travel distance and duration between two locations.
- Calculate route distance matrices.

### Installation & Setup

1. **Download the CLI tool:**
   - **Mac/Linux**: Run `./scripts/qq_map_cli.sh`
   - **Windows**: Run `.\scripts\qq_map_cli.bat`

2. **Get an API Key:**
   - Visit [Tencent Location Service Console](https://lbs.qq.com/dev/console/application/mine).
   - Click "创建应用" (Create Application) and "添加key" (Add Key).
   - Copy the generated Key.

3. **Configure the Key globally:**
   - **Mac/Linux**: `./scripts/bin/qq-map-cli setup --config ~/.qq_map_cli_config.json --key "your-key" --force`
   - **Windows**: `.\scripts\bin\qq-map-cli.exe setup --config %USERPROFILE%\.qq_map_cli_config.json --key "your-key" --force`

### Usage

Once configured, the CLI can be used from any directory to query addresses:

```bash
# Geocode an address
./scripts/bin/qq-map-cli geocoder --config ~/.qq_map_cli_config.json --address "杭州大厦"

# Measure distance
./scripts/bin/qq-map-cli address-distance --config ~/.qq_map_cli_config.json --from-address "杭州西站" --to-address "杭州大厦" --mode driving
```

*(For raw JSON output, append `--json` to any command)*

### Troubleshooting

- **macOS SSL Error (`[SSL: CERTIFICATE_VERIFY_FAILED]`)**: 
  Prefix your command with `SSL_CERT_FILE=/etc/ssl/cert.pem` to use the macOS system certificates.

---

<a id="chinese"></a>
## 中文

### 简介
这是一个提供地图地址查询与距离测算工作流的技能插件。目前支持**腾讯位置服务（QQ地图）**。

它可以赋予 AI 代理或用户以下能力：
- 将自然语言地址转换为精确的地理坐标（经纬度）。
- 测量两个地点之间的实际物理距离与预估通行时间。
- 计算批量路线距离矩阵。

### 安装与配置

1. **自动下载依赖命令行工具：**
   - **Mac/Linux**: 运行 `./scripts/qq_map_cli.sh`
   - **Windows**: 运行 `.\scripts\qq_map_cli.bat`

2. **获取 API Key:**
   - 访问 [腾讯位置服务控制台](https://lbs.qq.com/dev/console/application/mine)。
   - 点击“创建应用”，然后“添加 Key”。
   - 复制生成的 Key 字符串。

3. **全局配置您的 Key：**
   - **Mac/Linux**: `./scripts/bin/qq-map-cli setup --config ~/.qq_map_cli_config.json --key "您的key" --force`
   - **Windows**: `.\scripts\bin\qq-map-cli.exe setup --config %USERPROFILE%\.qq_map_cli_config.json --key "您的key" --force`

### 使用方法

配置好全局密钥后，即可随时随地在终端发起查询：

```bash
# 查询具体地址坐标
./scripts/bin/qq-map-cli geocoder --config ~/.qq_map_cli_config.json --address "杭州大厦"

# 计算两地通行距离
./scripts/bin/qq-map-cli address-distance --config ~/.qq_map_cli_config.json --from-address "杭州西站" --to-address "杭州大厦" --mode driving
```

*(如果需要供程序对接的结构化 JSON 数据结果，可以在任何命令结尾加上 `--json`)*

### 常见问题 Troubleshooting

- **macOS 下出现 SSL 证书报错 (`[SSL: CERTIFICATE_VERIFY_FAILED]`)**: 
  这属于跨平台二进制文件的常见问题。在命令行开头加上 `SSL_CERT_FILE=/etc/ssl/cert.pem` 即可调用系统的根证书完成环境验证。例如：
  `SSL_CERT_FILE=/etc/ssl/cert.pem ./scripts/bin/qq-map-cli geocoder ...`
