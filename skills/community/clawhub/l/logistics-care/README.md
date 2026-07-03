# logistics-care — 电商物流延迟检测 & 安抚短信

为电商卖家提供「物流监控 → 延迟检测 → 安抚话术 → 短信发送」一站式服务。

## 功能

- **物流轨迹查询** — 支持60+快递公司（UAPI），自动识别快递公司
- **延迟风险检测** — 5条规则引擎：发货超时/运输停滞/派送异常/预计超时/无物流
- **AI安抚话术** — 按延迟类型自动生成专业安抚短信
- **短信发送** — 支持阿里云短信/腾讯云短信，默认 dry-run 安全预览
- **HTML报告** — 可视化展示检测结果和短信预览

## 快速开始

```bash
# 1. 配置UAPI API Key（免费注册 https://uapis.cn）
export UAPI_API_KEY="your_key"

# 2. 准备订单CSV（参考 assets/sample_orders.csv）
# 3. 验证订单数据
python scripts/order_processor.py --input orders.csv --validate

# 4. 物流检测 + 短信预览（dry-run，默认安全模式）
python scripts/order_processor.py --input orders.csv --preview

# 5. 确认后发送短信（需配置短信API）
python scripts/order_processor.py --input orders.csv --send --config sms_config.json

# 单号查询
python scripts/logistics_checker.py --single SF1234567890
```

## 延迟检测规则

| 规则 | 条件 | 级别 |
|------|------|------|
| 发货超时 | 下单>48h，物流待揽件 | 🔴 高 |
| 运输停滞 | 最后更新>24h，运输中 | 🟡 中 |
| 派送异常 | 退回/丢失/损坏 | 🔴 高 |
| 预计超时 | 超预计送达时间 | 🟡 中 |
| 无物流 | 单号无结果 | 🟢 低 |

## 技能结构

```
logistics-care/
├── SKILL.md                    # WorkBuddy技能定义
├── scripts/
│   ├── logistics_checker.py    # 物流查询+延迟检测
│   ├── sms_sender.py           # 话术生成+短信发送
│   └── order_processor.py      # 一站式集成
├── references/
│   └── api_config.md           # API配置参考
└── assets/
    ├── sample_orders.csv       # 示例订单
    └── sms_config_template.json # 短信配置模板
```

## 工作模式

| 模式 | 说明 |
|------|------|
| `dry-run` | 检测+预览短信，不发送（默认） |
| `send` | 检测+预览+确认后批量发送 |

## API依赖

- **物流查询**: [UAPI](https://uapis.cn) — 免费额度，40积分/次
- **短信发送**: [阿里云短信](https://www.aliyun.com/product/sms) / [腾讯云短信](https://cloud.tencent.com/product/sms)

详细配置见 `references/api_config.md`。

## License

MIT
