# GitLab 智能项目洞察助手

自动拉取私有 GitLab 指定仓库的多维度数据（Commits / MRs / Issues / Pipelines），生成智能摘要并推送到飞书群机器人。

## 核心功能

| 功能 | 说明 |
|------|------|
| 多维度数据抓取 | Commits + MRs + Issues + Pipelines 全方位监控 |
| 智能摘要 | 按功能模块聚类（✨新功能/🐛Bug修复/🛠重构/📄文档） |
| 管理洞察 | 识别阻塞 MR、检测失败 Pipeline |
| 风险预警 | 敏感文件变更检测 |
| 多样化输出 | 支持 concise / detailed / executive 三种风格 |

## 快速开始

### 1. 配置

复制示例配置文件并填写：

```bash
cp config.example.json config.json
```

编辑 `config.json`，填写以下字段：

| 字段 | 说明 |
|------|------|
| `gitlab_url` | 私有 GitLab 地址，如 `https://gitlab.yourcompany.com` |
| `gitlab_token` | Personal Access Token，需要 `read_api` 权限。在 GitLab → 头像 → Preferences → Access Tokens 中创建 |
| `repositories` | 要监控的仓库列表，格式为 `"命名空间/仓库名"`，例如 `"team/backend"` |
| `feishu_webhooks` | 飞书群机器人 Webhook 地址列表（可配多个群） |
| `timezone_offset` | 时区偏移，默认 `8`（北京时间） |

### 2. 手动运行

```bash
python gitlab_report.py
```

### 3. 输出风格选择

```bash
# 极简模式 - 一句话概括
python gitlab_report.py --style concise

# 详细模式（默认）- 按功能模块聚类
python gitlab_report.py --style detailed

# 管理层汇报模式 - 执行摘要
python gitlab_report.py --style executive
```

### 4. 预览模式（不推送）

```bash
python gitlab_report.py --preview --style detailed
```

## 输出示例

### Detailed 模式

```
📅 [project-name] 每日进度报告 (2026-03-19)
==================================================
🚀 核心进展
  ✨ 新功能 (3项): 新增用户登录接口、添加支付回调处理、支持二维码生成
  🐛 Bug 修复 (2项): 修复 token 过期问题、解决列表分页异常
  🛠️ 重构与优化 (1项): 优化数据库查询性能

⚠️ 风险与阻塞
  ✓ 无阻塞 MR
  ✓ 无失败 Pipeline

📊 统计洞察
  代码提交: 15 次 | 活跃成员: 5 人
  MR: 3 开放, 2 已合并
  Pipeline: 10 成功, 0 失败
  活跃度评级: Med
```

### Executive 模式

```
📋 [执行摘要] project-name - 2026-03-19
─────────────────────────────────────────────────
✅ 今日产出: 15 次代码提交, 5 位成员活跃
📈 活跃度: Med | 风险等级: 🟢 低

📌 产出分布:
  • ✨ 新功能: 3
  • 🐛 Bug 修复: 2
  • 🛠️ 重构与优化: 1

✓ 无阻塞事项
✓ 构建正常

🏆 今日之星: 张三 (8 次提交)
```

## 配置 Webhook 自动推送

### 方式一：WorkBuddy 自动化（推荐）

WorkBuddy 已为你配置好每天 18:00 自动执行的定时任务。修改配置后会自动生效。

### 方式二：GitLab Webhook 触发

在 GitLab 项目中配置 Webhook，实现特定事件自动触发报告：

1. 进入 GitLab 项目 → Settings → Webhooks
2. 添加新的 Webhook：
   - **URL**: 部署服务器的接收地址（如 `https://your-server.com/webhook`）
   - **Trigger**: 选择 `push` 或自定义事件
3. 创建接收脚本处理推送

示例接收脚本（Python Flask）：

```python
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # 验证 GitLab token（可选）
    token = request.headers.get('X-Gitlab-Token')
    if token != 'YOUR_SECRET_TOKEN':
        return 'Unauthorized', 401
    
    # 拉取最新代码
    subprocess.run(['git', 'pull'])
    
    # 生成并推送报告
    subprocess.run(['python', 'gitlab_report.py', '--style', 'detailed'])
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 方式三：系统定时任务（Linux Cron）

```bash
# 每天 18:00 执行
0 18 * * * /usr/bin/python3 /path/to/gitlab_report.py --style detailed >> /var/log/gitlab_report.log 2>&1
```

### 方式四：GitLab CI/CD 触发

在项目中添加 `.gitlab-ci.yml`：

```yaml
daily-report:
  only:
    - schedules
  schedule:
    - cron: '0 10 * * *'  # 每天 10:00 UTC
  script:
    - python gitlab_report.py --style detailed
  tags:
    - docker
  image: python:3.11
```

## 常见问题

**Q: 提示找不到仓库？**  
A: 检查 `repositories` 中的路径格式是否为 `命名空间/仓库名`，且 Token 有该仓库的读取权限。

**Q: 飞书收不到消息？**  
A: 确认 Webhook 地址完整，飞书机器人未被禁用，网络可访问 open.feishu.cn。

**Q: 如何只看某个人？**  
A: 报告已按成员分组显示，可直接查看特定成员的内容。

**Q: API 请求超时？**  
A: 代码已内置重试机制，检查 GitLab 服务器负载或网络状况。

## 技术细节

- **并发请求**: 使用 ThreadPoolExecutor 并行抓取 Commits/MRs/Pipelines/Issues
- **时间处理**: 自动计算 24 小时前的时间戳用于数据过滤
- **关联分析**: 从 Commit Message 提取 Issue 引用（如 #123）
- **阻塞检测**: 识别超过 24 小时未合并且无评审的 MR
