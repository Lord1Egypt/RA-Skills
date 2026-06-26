## v14.0.1 (2026-05-16) — 每周数据焕新版

### 📊 数据更新
- 更新 basic 数据至 2026-05-14（latest trading day）
- 更新 finance / closing 数据同步
- 同步最新 pre_market.py 代码与 config.json

---

## v14.0.0 (2026-05-09) — 每周数据焕新版

### 📊 数据更新
- 更新 basic 数据至 2026-05-08（latest trading day）
- 更新 closing 数据至 2026-05-08
- 同步最新 pre_market.py 代码（v12.5.1 内部版）
- 同步 config.json 配置

---

## v13.2.0 (2026-04-19) — 安全加固+体验修复版

### 🐛 Bug 修复
- Eastmoney API 空值修复: resp.get('data') or {} 避免 NoneType.get() 报错
- *ST 股票过滤: 从 Tushare 补充 name 列 + 全局 _NAME_MAP，不再漏网
- 价格数据 null 修复: 周末/节假日 fallback 到最近 daily_basic 缓存
- 价格兜底查找: 市值筛选后的 price_map 找不到时，从原始缓存二次查找

### 📦 交付优化
- 新增 CHANGELOG.md: 详细记录每次更新内容
- 新增 LICENSE (MIT): 符合开源规范
- 新增 .gitignore: 排除 __pycache__/cache_data 等非交付文件
- 清理交付物: 移除数据质量审查报告.md、__pycache__、cache_data/

### 🔧 架构改进
- 订单号三重防护: 时间戳 + 微秒 + UUID
- find_latest_order 按文件名排序，不再误读旧订单
- 订阅过期优先使用 finishTime 计算
- API 重试机制: 3 次重试 + 指数退避 + 超时增至 5s
- RSI 改用 Wilder's EMA 标准算法

# CHANGELOG

## v13.1.0 (2026-04-19) — 安全加固版

### 🔐 安全修复
- 移除 CLAWTIP_SM4_KEY 硬编码默认值，强制要求环境变量配置
- payTo 收款地址改为 Base64 编码存储，防肉眼提取
- 移除 `LIBU_MOCK_PAYMENT` / `LIBU_ENV` 开发模式后门
- 移除沙箱 TEST_SUCCESS 凭证在生产环境的放行逻辑
- 移除 `status="paid"` 无凭证的兼容模式绕过漏洞
- 添加凭证交叉验证：orderNo/payTo/amount 三重校验，防止凭证复用
- 添加月度订阅 30 天过期检查，优先使用 finishTime 计算

### 🛡️ 支付流程加固
- 订单号生成加入微秒级时间戳，防止并发冲突
- `_find_latest_order()` 改为按文件名（订单号）排序，避免误读旧订单
- 订阅过期 fallback 逻辑增强：finishTime → created_at → 放行

### 📈 算法优化
- RSI 指标改用 Wilder's EMA 标准算法（原为简单移动平均 SMA）
- 财务评分归一化：原始增速百分比 cap=100，防止 finance 权重碾压 technical
- API 请求增加自动重试机制（3 次，指数退避），超时从 3s 增至 5s

### 📦 体验改进
- config.json 财务阈值改为小数格式（0.30=30%），与 Tushare 返回值一致
- manifest.json config_schema 填充字段定义和默认值说明
- SKILL.md 文档修正"0 配置"宣传，明确标注必需环境变量
- 新增 .gitignore、LICENSE（MIT）、CHANGELOG.md
- 清理 `__pycache__/`、内部审查报告等非交付文件

---

## v13.0.0 (2026-04-18) — 支付集成版
- 集成 ClawTip 微支付（单次 ¥0.8 / 包月 ¥9.9）
- encrypted_data 采用 SM4-ECB + PKCS7 加密
- 支持双 SKU 选择

## v12.9.0 (2026-04-17)
- 沙箱支付全流程验证通过
- 修复订单路径 indicator 计算错误

## v12.5.1 (2026-04-16)
- 增加环境依赖检查与全局异常捕获
- 新增本地免费技术指标计算（MACD/RSI）
- 增加数据保质期检查
