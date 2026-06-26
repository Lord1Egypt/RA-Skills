---
name: ip
description: 聚合数据IP归属地查询V3.0，支持IPv4查询国家/省份/城市/运营商
metadata:
  openclaw:
    emoji: 🌍
    requires:
      bins: [python3]
      env: [JUHE_API_KEY]
    primaryEnv: JUHE_API_KEY
---

# IP 归属地查询（OpenClaw 技能）

基于聚合数据官方 IP 查询 V3.0 接口，支持 IPv4 地址快速查询归属地信息。

## 功能说明
- 查询 IPv4 地址的国家、省份、城市、运营商信息
- 数据格式标准化，可直接被 OpenClaw 解析使用

## 环境变量配置
在运行前必须配置 API 密钥：

# Windows（PowerShell）
$env:JUHE_API_KEY="你的聚合数据API Key"

# Linux / macOS
export JUHE_API_KEY="你的聚合数据API Key"

## 使用说明
1. 确保已安装依赖：pip install requests
2. 配置好环境变量 JUHE_API_KEY
3. 在终端中直接运行查询命令

## 调用命令
python3 skills/ip/ip.py 114.114.114.114

## 返回示例
{
  "error_code": 0,
  "reason": "success",
  "result": {
    "ip": "114.114.114.114",
    "country": "中国",
    "province": "北京",
    "city": "北京",
    "sp": "联通"
  }
}

## 错误说明
- JUHE_API_KEY not set：未配置环境变量
- invalid json：参数格式错误
- request failed：网络请求异常