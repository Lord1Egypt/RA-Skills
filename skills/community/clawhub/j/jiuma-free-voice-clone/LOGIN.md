# 九马AI授权登录

用于获取和管理九马AI服务的API访问密钥。通过扫码登录方式获取API密钥，使其他九马AI技能能够正常使用。

## 核心功能

1. **获取登录二维码**：生成九马AI平台的登录二维码和登录链接
2. **检查登录状态**：获得二维码和登录链接之后，定时每分钟验证登录状态并获取API密钥
3. **API密钥管理**：自动保存获取的API密钥到本地文件系统
4. **无缝集成**：与其他九马AI技能（文生图、数字人、语音克隆等）无缝集成

## 安装依赖

```bash
# 安装必要的Python依赖
pip install requests
```

## 使用方法

### 命令行使用

```bash
# 1. 获取登录二维码和访问令牌
python3 jiuma_auth_login.py --login

# 2. 检查登录状态并获取API密钥
python3 jiuma_auth_login.py --check --access_token "<your_access_token>"
```

### 完整登录流程示例

```bash
# 第一步：获取登录信息
python3 jiuma_auth_login.py --login
# 输出示例：
# {
#   "status": "success",
#   "message": "获取登录通行证成功",
#   "data": {
#     "login_qrcode": "https://cache.jiuma.com/static/uploads/20260331/69cb63596b230.png",
#     "login_url": "https://console.jiuma.com/user/login?rand_string=69cb63585b3db",
#     "access_token": "abc123xyz456"
#   }
# }

# 第二步：用手机扫描二维码或访问登录链接完成登录
# 第三步：添加每分钟定时任务，验证登录状态并获取API密钥，或用户告知完成登录主动触发
python3 jiuma_auth_login.py --check --access_token "abc123xyz456"
# 输出示例：
# {
#   "status": "success",
#   "message": "登录成功，已保存api_key，可以继续使用九马AI工具",
#   "data": {}
# }
```

### 在OpenClaw中使用

```bash
# 获取登录信息
exec python3 /path/to/jiuma_auth_login.py --login

# 检查登录状态
exec python3 /path/to/jiuma_auth_login.py --check --access_token "your_token_here"
```

```bash
# 1. 先获取API密钥
python3 jiuma_auth_login.py --login
# 然后用返回的access_token检查登录状态
python3 jiuma_auth_login.py --check --access_token "your_token"

# 2. 之后就可以使用其他九马AI技能
# 如：文生图技能
python3 jiuma_free_image_gen/agent.py --submit --text "图片描述"

# 数字人生成技能
python3 jiuma_free_meta_human/generate_video.py --action create --text "视频内容"
```

## 错误处理

| 错误类型 | 描述 | 解决方案 |
|---------|------|---------|
| 网络超时 | 请求API超时 | 检查网络连接，重试操作 |
| API返回错误 | API返回非200状态码 | 查看具体错误信息，联系九马AI支持 |
| 登录状态无效 | access_token无效或已过期 | 重新获取登录二维码 |
| 文件权限错误 | 无法保存API密钥 | 检查文件系统权限 |

## 注意事项

1. **登录时效**：登录二维码和access_token通常有有效期限制，建议尽快完成登录
2. **网络要求**：需要能够访问九马AI API服务器（api.jiuma.com）
3. **兼容性**：此技能需要Python 3.6+和requests库