# 在线购物优惠查询脚本说明

本目录包含支持优惠商品查询功能的核心脚本。

## 脚本列表

### 1. register.sh - 注册认证脚本

获取 API 访问凭证，支持本地缓存。

```bash
# 基本用法（首次注册，后续使用缓存）
./register.sh

# 强制重新注册
./register.sh --force

# 使用自定义用户名
./register.sh --username "ai_assistant_01"

# 清除本地缓存
./register.sh --clear-cache
```

> 默认将用户名注册到 `http://127.0.0.1:9090/user/register`，密码自动随机生成（可通过 `--password` 指定）。
> 如果未显式传入 `--username`，脚本会自动读取本机的设备 UUID（macOS 使用 IOPlatformUUID，Linux/WSL 优先 `/sys/class/dmi/id/product_uuid`，Windows 使用 `Get-CimInstance Win32_ComputerSystemProduct`）作为用户名；若无法获取则退回随机用户名。

**凭证缓存机制：**
- 首次调用会向服务端注册并获取凭证（UUID）
- 凭证自动保存到 `.credential_cache` 文件
- 后续调用优先使用缓存的凭证
- 默认设置 30 天过期时间，接近过期时自动刷新
- 缓存文件权限为 600（仅所有者可读写）

**返回格式：**
```json
{
  "status": "success",
  "credential": "46f7ff38-1984-4dd1-9ef6-727ae5d0c302",
  "username": "ai_shopper_1710058535_xxx",
  "user_id": "1",
  "expires_at": "2026-04-09T00:00:00Z",
  "api_endpoint": "http://127.0.0.1:9090",
  "cached_at": "2026-03-10T08:15:35Z",
  "device_uuid": "A1B2C3D4-E5F6-..."
}
```

### 2. search_products.sh - 商品查询脚本

根据关键词和条件查询商品信息。

```bash
./search_products.sh \
  --credential "uuid_xxx" \
  --keyword "商品关键词" \
  [--user_id "自定义 user_id"]
```

**参数说明：**
- `--credential`: 注册接口返回的 UUID（必填）
- `--keyword`: 搜索关键词（必填）
- `--user_id`: 自定义 user_id（可选，默认使用 credential）

**返回格式：**
```json
{
  "status": "success",
  "total": 150,
  "products": [
    {
      "item_id": "12345678",
      "title": "商品标题",
      "short_title": "短标题",
      "pict_url": "https://example.com/image.jpg",
      "reserve_price": "599.00",
      "zk_final_price": "299.00",
      "final_promotion_price": "279.00",
      "income_rate": "20",
      "commission_amount": "15.0",
      "shop_title": "店铺名称",
      "click_url": "https://example.com/deal",
      "small_images": ["https://example.com/image_small.jpg"],
      "promotion_tags": ["满减", "返券"]
    }
  ]
}

> ⚠️ `/coupon/search` 仅支持 `keyword` 与 `user_id` 参数，平台或价格筛选需由调用方在拿到结果后自行过滤。
```

### 3. generate_link.sh - 链接生成脚本

为指定商品生成优惠推广链接。

```bash
./generate_link.sh \
  --credential "uuid_xxx" \
  --product_id "12345678" \
  [--link_type "both"] \
  [--activity_id "act123"]
```

**参数说明：**
- `--credential`: 注册接口返回的 UUID（必填，作为 user_id）
- `--product_id`: 商品ID（必填）
- `--link_type`: 链接类型，可选 `url|code|both`（默认 `url`）
- `--activity_id`: 活动ID（可选）
- `--user_id`: 自定义 user_id（可选，默认使用 credential）

**返回格式：**
```json
{
  "status": "success",
  "product_id": "12345678",
  "link_type": "both",
  "url": "https://s.click.taobao.com/xxx",
  "code": "￥AbCd123￥",
  "expire_time": "2026-03-16T00:00:00Z"
}
```

## 错误处理

所有脚本在出错时返回统一格式：

```json
{
  "status": "error",
  "error_code": "ERROR_CODE",
  "message": "错误描述信息"
}
```

**常见错误码：**
- `AUTH_FAILED`: 认证失败
- `INVALID_CREDENTIAL`: 凭证无效或过期
- `INVALID_PARAMS`: 参数错误
- `PRODUCT_NOT_FOUND`: 商品不存在
- `NETWORK_ERROR`: 网络错误
- `RATE_LIMIT`: 请求频率超限
- `UNKNOWN_ERROR`: 未知错误

## 使用示例

### 完整流程示例

```bash
# 1. 获取凭证（首次会注册，后续使用缓存）
CREDENTIAL=$(./register.sh | jq -r '.credential')

# 2. 查询商品
PRODUCTS=$(./search_products.sh \
  --credential "$CREDENTIAL" \
  --keyword "无线耳机")

# 3. 提取第一个商品ID
PRODUCT_ID=$(echo "$PRODUCTS" | jq -r '.products[0].item_id')

# 4. 生成推广链接
LINK=$(./generate_link.sh \
  --credential "$CREDENTIAL" \
  --product_id "$PRODUCT_ID" \
  --link_type "both")

# 5. 输出链接
echo "$LINK" | jq -r '.short_link'
```

### 凭证管理示例

```bash
# 查看当前缓存的凭证
if [ -f .credential_cache ]; then
  cat .credential_cache | jq .
else
  echo "没有缓存的凭证"
fi

# 强制刷新凭证
./register.sh --force

# 清除缓存（下次会重新注册）
./register.sh --clear-cache
```

## 配置说明

### 环境变量

可以通过环境变量配置默认值：

```bash
export SHOPPING_API_ENDPOINT="http://127.0.0.1:9090"
export SHOPPING_API_TIMEOUT=30
export SHOPPING_DEFAULT_PLATFORM="taobao"
```

### 配置文件

可以创建 `config.json` 文件：

```json
{
  "api_endpoint": "https://api.example.com",
  "timeout": 30,
  "default_platform": "taobao",
  "cache_enabled": true,
  "cache_ttl": 300
}
```

## 注意事项

1. **凭证管理**
   - 凭证会自动缓存到本地，无需每次注册
   - 缓存文件 `.credential_cache` 不应提交到版本控制
   - 建议在 `.gitignore` 中添加 `.credential_cache`
   - 凭证过期会自动重新注册

2. **请求频率**
   - 遵守 API 调用频率限制
   - 建议添加请求间隔
   - 使用缓存减少重复请求

3. **错误重试**
   - 网络错误可以重试 2-3 次
   - 凭证过期会自动刷新
   - 参数错误不应重试

4. **数据验证**
   - 检查返回的 status 字段
   - 验证必要字段是否存在
   - 处理空结果的情况

5. **安全性**
   - 缓存文件权限为 600
   - 不要在日志中暴露完整凭证
   - 定期清理过期的缓存文件

## 开发指南

### 添加新脚本

1. 创建脚本文件并添加执行权限
2. 遵循统一的参数格式
3. 返回标准的 JSON 格式
4. 添加错误处理
5. 更新本 README

### 测试脚本

```bash
# 运行测试
./test_scripts.sh

# 测试单个脚本
./test_scripts.sh register
./test_scripts.sh search
./test_scripts.sh generate
```

## 故障排查

### 常见问题

1. **脚本无法执行**
   ```bash
   chmod +x *.sh
   ```

2. **jq 命令不存在**
   ```bash
   # macOS
   brew install jq
   
   # Linux
   apt-get install jq
   ```

3. **网络连接失败**
   - 检查网络连接
   - 验证 API 端点是否正确
   - 检查防火墙设置

## 更新日志

- 2026-03-09: 初始版本，包含基础的注册、查询和链接生成功能
