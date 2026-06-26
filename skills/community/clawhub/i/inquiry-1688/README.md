# 1688 询盘 SKILL

向 1688 供应商发起询盘，自动获取供应商对商品问题的回复。提交后 20 分钟自动查询结果并推送通知。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

## ✨ 核心特性

- 💬 **自由文本询盘** - 支持任意商品问题（定制、起批量、规格等）
- ⏰ **自动查询结果** - 20 分钟后自动查询并推送通知
- 🔔 **钉钉推送** - 结果自动推送到钉钉，实时收到通知
- 🔄 **兜底机制** - 多层保障确保结果不丢失

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中配置：

```json5
{
  skills: {
    entries: {
      "inquiry-1688": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

密钥获取：访问 https://www.alphashop.cn/seller-center/apikey-management 申请。

## 🎯 使用方法

### 提交询盘

```bash
python3 scripts/inquiry.py submit "<商品链接或ID>" "<询盘问题>" [--quantity X] [--address "地址"]
```

### 查询结果

```bash
python3 scripts/inquiry.py query "<taskId>"
```

### 使用示例

在 Claude Code 中直接说：

```
"帮我问一下这个1688商品能不能定制logo"
"问下供应商起批量是多少"
```

## 📁 项目结构

```
inquiry-1688/
├── SKILL.md                    # SKILL 配置文件
├── README.md                   # 本文档
├── requirements.txt            # Python 依赖
└── scripts/
    └── inquiry.py              # 询盘主脚本
```

## 📝 注意事项

1. **等待时间** - 询盘提交后需等待约 20 分钟获取结果
2. **不要轮询** - 提交后由 cron 任务自动查询，无需手动反复查询
3. **AlphaShop 欠费** - 如返回欠费错误，需前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分

---

**最后更新**: 2026-03-19
