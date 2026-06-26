# 如何使用 Hotel Manager Skill 进行统一调价

本示例展示如何通过脚本一次性调整所有 OTA 平台的五一节假日价格。

## 场景
由于“五一”劳动节即将来临，酒店决定将所有房型的基础价格提高 200 元。

## 步骤

### 1. 确认配置文件
确保 `resources/ota_config.json` 中已填入正确的 API Key。

### 2. 执行调价脚本
在终端中运行以下命令：

```bash
# 假设房型 ID 为 "deluxe_king"，日期为 "2024-05-01"，基准价为 800
node scripts/price_manager.js
```

> 注意：生产环境下，您应通过命令行参数或外部调用传递具体数值。

### 3. 查看输出日志
您将看到类似以下内容的日志：
```text
--- Starting Unified Price Update for deluxe_king on 2024-05-01 (Base: 800) ---
[携程] Updating price for deluxe_king on 2024-05-01 to 810...
[美团] Updating price for deluxe_king on 2024-05-01 to 800...
[飞猪] Updating price for deluxe_king on 2024-05-01 to 795...
--- Unified Update Finished ---
```

## 自动接单设置
若要开启自动同步订单至内部 PMS，请运行：
```bash
node scripts/order_sync.js
```
该服务会每隔 5 分钟轮询一次新订单。
