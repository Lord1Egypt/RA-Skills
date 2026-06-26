# 小红书/视频号全流程自动化技能

> 社交媒体内容自动发布与运营工作流

---

## 📌 技能概述

**技能名称**: `social-media-automation`

**版本**: 1.0.0

**适用场景**:
- 小红书笔记自动发布
- 微信视频号自动发布
- 多账号矩阵管理
- 内容日历规划与执行

**核心能力**:
- ✅ 账号信息采集与配置
- ✅ 内容模板库建设
- ✅ 自动发布（API/浏览器自动化）
- ✅ 数据追踪与日报生成
- ✅ 合规风控管理

---

## 🎯 标准工作流

### Phase 1: 账号交接（30 分钟）

**信息采集表**:

| 平台 | 采集项 | 用途 |
|------|--------|------|
| **小红书** | 账号名称、类型、认证状态、粉丝量、笔记数、发布频率、内容类型、素材库、API 权限 | 判断技术路线 |
| **视频号** | 账号名称、类型、认证状态、粉丝量、视频数、直播情况、关联公众号、小店、API 权限 | 判断技术路线 |

**决策逻辑**:
```
账号类型判断
├── 企业号/专业号 + API 权限 → ✅ 官方 API（稳定、合规）
└── 个人号 / 无 API 权限 → ⚠️ 浏览器自动化（需维护）
```

**凭证管理**:
- 存储位置：`.credentials/social-media/`
- 加密方式：gpg 或 pass
- 禁止明文传输

---

### Phase 2: 内容策略（1 小时）

**目标人群定位**:
- □ 减脂人群  □ 增肌人群  □ 产后恢复  □ 中老年健身
- □ 办公室人群  □ 学生党  □ 其他

**内容选题库**:

| 类别 | 选题示例 | 优先级 |
|------|---------|--------|
| 减脂 | 7 天燃脂计划、HIIT 入门、饮食搭配 | P0 |
| 增肌 | 新手增肌指南、蛋白摄入、力量训练 | P0 |
| 居家 | 无器械训练、办公室拉伸、晨练 routine | P1 |
| 科普 | 健身误区、动作纠错、装备推荐 | P1 |
| 激励 | 前后对比、打卡挑战、粉丝故事 | P2 |

**发布节奏**:
| 平台 | 频率 | 时间段 |
|------|------|--------|
| 小红书 | 1-2 篇/天 | 7-8 点、20-21 点 |
| 视频号 | 1 篇/天 + 直播 2-3 场/周 | 12 点、20 点 |

**合规注意事项**:
- ⚠️ 避免医疗宣称（减脂≠治病）
- ⚠️ 动作安全提示必须到位
- ⚠️ 不夸大效果（如"7 天瘦 20 斤"）
- ⚠️ 前后对比图需真实

---

### Phase 3: 技术部署（2-4 小时）

#### 方案 A: 官方 API（推荐）

**小红书（蒲公英平台）**:
```python
# 配置
API_BASE = "https://api.xiaohongshu.com"
ACCESS_TOKEN = "xxx"

# 发布笔记
def publish_note(title, content, images):
    response = requests.post(
        f"{API_BASE}/note/publish",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={
            "title": title,
            "desc": content,
            "images": images
        }
    )
    return response.json()
```

**视频号**:
```python
# 配置
API_BASE = "https://api.weixin.qq.com"
ACCESS_TOKEN = "xxx"

# 发布视频
def publish_video(title, video_url, cover_url):
    response = requests.post(
        f"{API_BASE}/channel/post",
        params={"access_token": ACCESS_TOKEN},
        json={
            "title": title,
            "media_video_url": video_url,
            "cover_url": cover_url
        }
    )
    return response.json()
```

---

#### 方案 B: 浏览器自动化（备选）

**依赖**: Playwright + Cookie 维持登录

```python
from playwright.sync_api import sync_playwright

def publish_xiaohongshu(title, content, images):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 加载 Cookie 保持登录
        page.context.add_cookies(load_cookies())
        
        # 访问发布页
        page.goto("https://creator.xiaohongshu.com/publish")
        
        # 填写内容
        page.fill("textarea[placeholder='输入标题']", title)
        page.fill("div[contenteditable='true']", content)
        
        # 上传图片
        file_input = page.input("input[type='file']")
        file_input.set_input_files(images)
        
        # 发布
        page.click("button:has-text('发布')")
        
        browser.close()
```

---

### Phase 4: 数据追踪（自动化）

**日报模板**:
```markdown
## 📊 社交媒体日报 [YYYY-MM-DD]

### 发布情况
| 平台 | 计划 | 实际 | 状态 |
|------|------|------|------|
| 小红书 | 2 | 2 | ✅ |
| 视频号 | 1 | 1 | ✅ |

### 数据汇总
| 平台 | 阅读/播放 | 点赞 | 收藏 | 评论 | 涨粉 |
|------|----------|------|------|------|------|
| 小红书 | 12,345 | 234 | 89 | 12 | +5 |
| 视频号 | 8,901 | 156 | 34 | 8 | +3 |

### 爆款内容 TOP3
1. [标题] - 阅读量 XXXX
2. [标题] - 阅读量 XXXX
3. [标题] - 阅读量 XXXX

### 异常情况
- 无 / [具体描述]

### 优化建议
- [基于数据的改进建议]
```

**数据采集**:
- 小红书：蒲公英平台 API / 手动截图
- 视频号：视频号助手后台 / 自动化脚本

---

## 📁 文件结构

```
social-media-automation/
├── SKILL.md                 # 技能文档
├── config.py                # 配置管理
├── accounts.py              # 账号管理
├── content_templates.py     # 内容模板库
├── publisher.py             # 发布模块
├── data_tracker.py          # 数据追踪
├── daily_report.py          # 日报生成
└── .credentials/            # 凭证存储（加密）
    ├── xiaohongshu.json.gpg
    └── wechat.json.gpg
```

---

## 🔧 核心代码模块

### 1. 账号管理

```python
import json
from cryptography.fernet import Fernet

class AccountManager:
    def __init__(self, key_file='.credentials/key.key'):
        self.key = load_key(key_file)
        self.cipher = Fernet(self.key)
    
    def save_account(self, platform, account_info):
        encrypted = self.cipher.encrypt(
            json.dumps(account_info).encode()
        )
        with open(f'.credentials/{platform}.enc', 'wb') as f:
            f.write(encrypted)
    
    def load_account(self, platform):
        with open(f'.credentials/{platform}.enc', 'rb') as f:
            encrypted = f.read()
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())
```

---

### 2. 内容模板库

```python
CONTENT_TEMPLATES = {
    "减脂": {
        "title": "{天数}天燃脂计划 | {效果}",
        "content": """
💪 第{天数}天打卡！

🔥 今日训练：
{训练内容}

🥗 饮食建议：
{饮食内容}

💡 小贴士：
{注意事项}

#减脂 #健身 #{品牌}
""",
        "hashtags": ["减脂", "健身", "燃脂", "自律"]
    },
    "增肌": {
        "title": "新手增肌 | {部位}训练指南",
        "content": """
🏋️ 增肌必看！

💪 目标肌群：{部位}
📊 推荐动作：
{动作列表}

⚠️ 注意事项：
{注意事项}

#增肌 #力量训练 #健身
""",
        "hashtags": ["增肌", "力量训练", "健身"]
    }
}
```

---

### 3. 发布调度器

```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=7, minute=30)
def morning_publish():
    """早间发布"""
    content = generate_content("morning")
    publish_xiaohongshu(content)
    publish_wechat(content)
    log_publish_result("morning", True)

@scheduler.scheduled_job('cron', hour=20, minute=0)
def evening_publish():
    """晚间发布"""
    content = generate_content("evening")
    publish_xiaohongshu(content)
    log_publish_result("evening", True)

@scheduler.scheduled_job('cron', hour=22, minute=0)
def daily_report():
    """生成日报"""
    report = generate_daily_report()
    send_to_feishu(report)

if __name__ == '__main__':
    scheduler.start()
```

---

## ⚠️ 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| API 调用失败 | Token 过期 | 刷新 Access Token |
| 发布失败 | 内容违规 | 检查合规用词 |
| Cookie 失效 | 登录态过期 | 重新扫码登录 |
| 图片上传失败 | 格式/大小不符 | 转为 JPG，<10MB |
| 数据抓取异常 | 页面结构变更 | 更新选择器 |

---

## 📊 性能指标

| 指标 | 目标值 |
|------|--------|
| 发布成功率 | ≥98% |
| 数据延迟 | <5 分钟 |
| 日报准时率 | 100% |
| 内容合规率 | 100% |

---

## 🔄 自我迭代机制

### 每周回顾

**回顾内容**:
1. 发布成功率分析
2. 爆款内容特征提取
3. 用户反馈收集
4. 平台规则变更追踪

**迭代动作**:
- 优化内容模板
- 调整发布时间
- 更新合规词库
- 改进数据追踪

### 月度升级

- 新增内容类别
- 优化发布策略
- 集成新平台
- 技能文档版本升级

---

## 📝 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-03-25 | v1.0 | 初始版本，基于已交付项目沉淀 |

---

*技能文档版本：v1.0 | 最后更新：2026-03-25*
