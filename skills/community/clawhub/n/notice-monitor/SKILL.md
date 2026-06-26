# notice-monitor - 通用公告监控技能

## 📋 技能描述

**通用网站公告监控工具** - 支持任意政府公告/采购/招标网站的自动化监控

- 监控任意 URL 的公告列表页
- 自定义关键词过滤
- 多层级/多分类支持
- 自动去重 + 定时推送
- 支持 DingTalk/微信/邮件通知

---

## 🚀 快速开始

### 安装
```bash
clawhub install notice-monitor
```

### 配置
创建配置文件 `~/.openclaw/workspace/notice-monitor-config.yaml`：

```yaml
# 监控任务配置
tasks:
  - name: 黑龙江教育采购
    url: https://hljcg.hlj.gov.cn/maincms-web/procurementNotice
    levels:
      - name: 省级
        selector: "省级"
      - name: 市级
        selector: "市级"
      - name: 县区级
        selector: "县 (区)"
    keywords:
      - 教育
      - 学校
      - 学院
      - 大学
      - 培训
      - 教学
    schedule: "0 8 * * *"  # 每天早 8 点
    notify:
      type: dingtalk
      target: "01254349410626385789"

  - name: 北京医疗招标
    url: https://bphc.beijing.gov.cn/notice
    keywords:
      - 医院
      - 医疗
      - 药品
      - 器械
    schedule: "0 9 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

### 运行
```bash
# 手动执行一次
openclaw skill run notice-monitor --config ~/.openclaw/workspace/notice-monitor-config.yaml

# 启用定时任务
openclaw skill cron notice-monitor enable
```

---

## ⚙️ 配置参数说明

### 任务配置 (tasks)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 任务名称 |
| `url` | string | ✅ | 公告列表页 URL |
| `levels` | array | ❌ | 层级配置（省/市/县等） |
| `keywords` | array | ✅ | 过滤关键词列表 |
| `schedule` | string | ❌ | Cron 表达式，定时执行 |
| `notify` | object | ✅ | 通知配置 |

### 层级配置 (levels)

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 层级显示名称 |
| `selector` | string | 页面选择器（文本/XPath/CSS） |

### 通知配置 (notify)

| 参数 | 类型 | 说明 |
|------|------|------|
| `type` | string | 通知类型：`dingtalk` / `wechat` / `email` |
| `target` | string | 接收目标（用户 ID/群 ID/邮箱） |

---

## 📁 示例配置

### 示例 1：黑龙江省教育采购（当前配置）
```yaml
tasks:
  - name: 黑龙江教育采购
    url: https://hljcg.hlj.gov.cn/maincms-web/procurementNotice
    levels:
      - name: 省级
        selector: "省级"
      - name: 市级
        selector: "市级"
      - name: 县区级
        selector: "县 (区)"
    keywords:
      - 教育
      - 学校
      - 学院
      - 大学
      - 中学
      - 小学
      - 幼儿园
      - 培训
      - 教学
      - 科研
      - 实验室
      - 医院
    schedule: "0 8 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

### 示例 2：北京市医疗设备招标
```yaml
tasks:
  - name: 北京医疗招标
    url: https://bphc.beijing.gov.cn/notice
    keywords:
      - 医院
      - 医疗
      - 药品
      - 器械
      - 卫生
      - 诊所
    schedule: "0 9 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

### 示例 3：上海市 IT 项目采购
```yaml
tasks:
  - name: 上海 IT 采购
    url: https://zfcg.sh.gov.cn/notice
    keywords:
      - 软件
      - 系统
      - 信息化
      - 网络
      - 数据
      - 云平台
    schedule: "0 10 * * *"
    notify:
      type: dingtalk
      target: "01254349410626385789"
```

---

## 🔧 高级用法

### 多任务并行
```yaml
tasks:
  - name: 教育采购
    url: https://hljcg.hlj.gov.cn/...
    keywords: [教育，学校，学院]
    
  - name: 医疗招标
    url: https://bphc.beijing.gov.cn/...
    keywords: [医院，医疗，药品]
    
  - name: IT 项目
    url: https://zfcg.sh.gov.cn/...
    keywords: [软件，系统，信息化]
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

###  webhook 通知
```yaml
notify:
  type: webhook
  url: https://your-server.com/api/notify
  method: POST
  headers:
    Authorization: Bearer xxx
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

【县区级】0 条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 今日新增：19 条 | 累计：156 条
```

---

## 🐛 故障排查

### 查看日志
```bash
tail -f ~/.openclaw/workspace/state/notice-monitor.log
```

### 测试配置
```bash
openclaw skill run notice-monitor --config ~/.openclaw/workspace/notice-monitor-config.yaml --dry-run
```

### 清除缓存
```bash
rm ~/.openclaw/workspace/state/pushed-ids-*.json
```

---

## 📝 版本历史

- **v1.0.0** (2026-03-20) - 初始版本
  - 支持单/多任务监控
  - 关键词过滤
  - 自动去重
  - DingTalk 通知

---

## 📄 License

MIT License

---

**作者**: 营销总监  
**仓库**: https://clawhub.com/skills/notice-monitor
