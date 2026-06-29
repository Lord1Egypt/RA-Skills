# Global Auto Translator - 跨境电商外贸智能翻译引擎

> 专为跨境电商、外贸出海打造的智能翻译引擎。支持 50+ 语言精准互译，内置外贸行业专属术语库。不仅能精准翻译网页文本，更能完美处理带表格、排版的复杂 PDF/Word 文档，告别生硬机翻味，让跨国沟通零障碍。

## 版本

| 版本 | 价格 | 功能 |
|------|------|------|
| **免费版** | 🆓 免费 | MyMemory 翻译、剪贴板监控、外贸术语库 |
| **Premium** | 💰 付费 | DeepL Pro 高精度翻译、批量文档、无速率限制 |

## 功能特性

| 特性 | 免费版 | Premium |
|------|--------|---------|
| 翻译引擎 | MyMemory（免费） | DeepL Pro（高精度） |
| 剪贴板智能监控 | ✅ | ✅ |
| 外贸专属词库 | ✅ 50+ 术语 | ✅ |
| 50+ 语种支持 | ✅ | ✅ |
| 多引擎降级 | ✅ | ✅ |
| 文档翻译（PDF/Word） | 基础版 | 批量处理 |
| 速率限制 | 有 | 无 |
| 技术支持 | 社区 | 优先 |

## 安装

```bash
bash ~/.openclaw/workspace/skills/global-auto-translator/setup.sh
```

## 使用

### 1. 剪贴板智能翻译（后台守护进程）

```bash
# 启动守护进程
python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py start

# 查看状态
python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py status

# 停止
python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py stop
```

启动后，你在浏览器、微信、飞书、邮箱等任何工具中**复制外语文字**，系统会自动检测并弹窗询问是否需要翻译。

### 2. 文档翻译（PDF / Word）

```bash
# 翻译 PDF（输出为 TXT，保留分页）
python3 ~/.openclaw/workspace/skills/global-auto-translator/doc-translate.py 文件.pdf

# 翻译 Word（输出为 DOCX，保留格式）
python3 ~/.openclaw/workspace/skills/global-auto-translator/doc-translate.py 文件.docx

# 指定目标语言
python3 ~/.openclaw/workspace/skills/global-auto-translator/doc-translate.py 文件.docx --to en

# 指定输出路径
python3 ~/.openclaw/workspace/skills/global-auto-translator/doc-translate.py 文件.pdf -o /path/output.txt
```

### 3. 手动翻译

```bash
echo "Some text" | python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py translate
```

### 4. 激活 Premium（可选）

```bash
# 查看当前状态
python3 ~/.openclaw/workspace/skills/global-auto-translator/activate.py --status

# 激活 Premium（需要激活码）
python3 ~/.openclaw/workspace/skills/global-auto-translator/activate.py --key YOUR_KEY

# 购买激活码：联系 @guo123dong
```

## 配置

编辑 `~/.openclaw/global-auto-translator/config.json`：

```json
{
  "target_language": "zh",
  "poll_interval": 2,
  "min_text_length": 3,
  "translation_service": "mymemory",
  "sound_alert": true,
  "copy_to_clipboard": true,
  "excluded_apps": [],
  "trade_terms_enabled": true,
  "preserve_formatting": true,
  "prompt_cooldown": 30,
  "premium_enabled": false,
  "deepl_api_key": ""
}
```

### Premium 配置

购买 Premium 后，在 `config.json` 中添加：

```json
{
  "premium_enabled": true,
  "translation_service": "deepl",
  "deepl_api_key": "你的DeepL Pro API Key"
}
```

> 💡 **如何获取 DeepL Pro API Key？**
> 1. 访问 https://www.deepl.com/pro-api
> 2. 注册并订阅 API 套餐
> 3. 在 API 设置页面获取你的 Key

## 外贸术语库

编辑 `~/.openclaw/global-auto-translator/custom-terms.json` 添加/修改术语：

```json
{
  "trade_terms": {
    "FBA": "Fulfillment by Amazon（亚马逊物流）",
    "MOQ": "Minimum Order Quantity（最小起订量）",
    "FOB": "Free On Board（船上交货价/离岸价）",
    "Listing": "产品详情页/商品页面",
    "Conversion Rate": "转化率"
  }
}
```

### 已内置术语（50+条）

**贸易术语**: FOB, CIF, EXW, DDP, DAP  
**物流**: FBA, FBM, Freight Forwarder, Customs Clearance, BL  
**订单**: MOQ, Sample Order, Bulk Order, Lead Time  
**支付**: T/T, L/C, PayPal, Western Union, Chargeback  
**电商**: ASIN, SKU, Buy Box, Listing, Variation, Review, Feedback  
**广告**: PPC, ACOS, ROI, Conversion Rate, Click-through Rate, Impressions  
**单据**: PI, CI, PL, CO  
**其他**: OEM, ODM, ETA, ETD, Return Rate, Refund

## 翻译效果示例

```
原文: Please send us a quote for 500 units with FOB pricing. Our MOQ requirement is 100 pieces per order.
译文: 请向我们发送包含FOB定价的500个单位的报价。我们的MOQ要求是每个订单100件。

--- 外贸术语对照 ---
  MOQ: Minimum Order Quantity（最小起订量）
  FOB: Free On Board（船上交货价/离岸价）
```

## 文件结构

```
~/.openclaw/workspace/skills/global-auto-translator/
├── SKILL.md              ← 使用说明
├── translate-daemon.py   ← 守护进程（剪贴板监控 + 弹窗翻译）
├── doc-translate.py      ← 文档翻译器（PDF/Word）
├── activate.py           ← Premium 激活工具
└── setup.sh              ← 一键安装脚本

~/.openclaw/global-auto-translator/
├── config.json           ← 个性化配置
├── custom-terms.json     ← 外贸术语库
├── license.json          ← Premium 许可证（激活后生成）
├── daemon.log            ← 运行日志
├── state.json            ← 运行时状态
└── daemon.pid            ← 进程ID
```

## 购买 Premium

### 价格：¥29.90 终身使用

### 支付方式

1. 扫码支付 ¥29.90（支付宝或微信）
2. 付款后备注 **AutoTranslator**
3. 添加微信 **NewWave_CN** 发送付款截图
4. 5分钟内收到激活码
5. 运行激活: `python3 activate.py --key YOUR_KEY`

### 或通过命令行查看支付二维码

```bash
python3 activate.py --buy
```

## 许可证

- 免费版: MIT License
- Premium: 商业许可证（需购买）
