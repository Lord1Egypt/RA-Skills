# notice-monitor

[![ClawHub Skill](https://img.shields.io/badge/clawhub-skill-blue)](https://clawhub.com/skills/notice-monitor)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.com/skills/notice-monitor)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

## 📋 简介

**通用网站公告监控工具** - 帮助你自动监控任意政府公告网、采购网、招标网的最新动态。

- ✅ 支持任意网站（只需配置 URL）
- ✅ 自定义关键词过滤
- ✅ 多层级/多分类支持（省/市/县等）
- ✅ 自动去重，不重复推送
- ✅ 定时任务，自动执行
- ✅ 多通知渠道（DingTalk/微信/邮件/Webhook）

---

## 🚀 快速开始

### 1. 安装技能

```bash
clawhub install notice-monitor
```

### 2. 创建配置文件

```bash
cp ~/.openclaw/skills/notice-monitor/configs/default.yaml \
   ~/.openclaw/workspace/notice-monitor-config.yaml
```

### 3. 编辑配置

编辑 `~/.openclaw/workspace/notice-monitor-config.yaml`：

```yaml
tasks:
  - name: 黑龙江教育采购
    url: https://hljcg.hlj.gov.cn/maincms-web/procurementNotice
    levels:
      - name: 省级
        selector: "省级"
      - name: 市级
        selector: "市级"
    keywords:
      - 教育
      - 学校
      - 学院
      - 大学
      - 培训
    schedule: "0 8 * * *"
    notify:
      type: dingtalk
      target: "你的 DingTalk 用户 ID"
```

### 4. 运行

```bash
# 手动执行一次
openclaw skill run notice-monitor --config ~/.openclaw/workspace/notice-monitor-config.yaml

# 启用定时任务
openclaw skill cron notice-monitor enable
```

---

## 📖 详细文档

查看完整文档：[SKILL.md](SKILL.md)

### 配置参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `name` | 任务名称 | ✅ |
| `url` | 公告列表页 URL | ✅ |
| `levels` | 层级配置（省/市/县） | ❌ |
| `keywords` | 过滤关键词 | ✅ |
| `schedule` | Cron 表达式 | ❌ |
| `notify` | 通知配置 | ✅ |

### 示例配置

#### 教育采购监控
```yaml
tasks:
  - name: 黑龙江教育采购
    url: https://hljcg.hlj.gov.cn/maincms-web/procurementNotice
    keywords: [教育，学校，学院，大学，培训]
    schedule: "0 8 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

#### 医疗招标监控
```yaml
tasks:
  - name: 北京医疗招标
    url: https://bphc.beijing.gov.cn/notice
    keywords: [医院，医疗，药品，器械]
    schedule: "0 9 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

#### IT 项目监控
```yaml
tasks:
  - name: 上海 IT 采购
    url: https://zfcg.sh.gov.cn/notice
    keywords: [软件，系统，信息化，网络，数据]
    schedule: "0 10 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

---

## 📊 输出示例

```
📢 黑龙江教育采购 日报
📅 2026/3/20

【省级】14 条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ 哈尔滨医科大学设备更新项目招标公告
   📍 黑龙江省省本级 | 🕐 2026-03-19

【市级】5 条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ 七台河职业学院实训室竞争性磋商公告
   📍 七台河市本级 | 🕐 2026-03-19

✅ 今日新增：19 条 | 累计：156 条
```

---

## 🔧 高级用法

### 多任务并行
```yaml
tasks:
  - name: 教育采购
    url: ...
    keywords: [教育，学校]
    
  - name: 医疗招标
    url: ...
    keywords: [医院，医疗]
    
  - name: IT 项目
    url: ...
    keywords: [软件，系统]
```

### Webhook 通知
```yaml
notify:
  type: webhook
  url: https://your-server.com/api/notify
  method: POST
  headers:
    Authorization: Bearer xxx
```

### 自定义报告模板
```yaml
template: |
  📢 {{taskName}} 日报
  📅 {{date}}
  
  {{#each levels}}
  【{{name}}】{{count}}条
  {{#each items}}
  {{index}}️⃣ {{title}}
     📍 {{area}} | 🕐 {{date}}
  {{/each}}
  {{/each}}
  
  ✅ 今日新增：{{total}}条
```

---

## 🐛 故障排查

### 查看日志
```bash
tail -f ~/.openclaw/workspace/state/notice-monitor.log
```

### 测试运行
```bash
openclaw skill run notice-monitor --config ~/.openclaw/workspace/notice-monitor-config.yaml --dry-run
```

### 清除缓存
```bash
rm ~/.openclaw/workspace/state/pushed-ids-*.json
```

---

## 📝 版本历史

### v1.0.0 (2026-03-20)
- ✅ 初始版本发布
- ✅ 支持多任务配置
- ✅ 关键词过滤
- ✅ 自动去重机制
- ✅ DingTalk 通知集成

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 问题反馈：https://clawhub.com/skills/notice-monitor/issues
- 功能建议：https://clawhub.com/skills/notice-monitor/discussions

---

## 📄 License

MIT License

---

**作者**: 营销总监  
**ClawHub**: https://clawhub.com/skills/notice-monitor
