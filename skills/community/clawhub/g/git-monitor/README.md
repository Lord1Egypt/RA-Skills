# Git 项目监控技能

自动监控 Git 项目更新（支持 GitHub、GitLab、Gitee 等所有 Git 平台），拉取最新代码并生成变更摘要。

## ⚡ 1分钟快速开始

```bash
# 1. 安装
clawhub install git-monitor

# 2. 告诉我监控什么
# 直接说：监控 GitHub 项目 anthropics/skills

# 3. 开启自动推送（可选）
# 直接说：设置定时检查，每6小时一次
```

然后就完事了！🎉

---

## 📖 完整功能

### 添加监控
```
监控 GitHub 项目 anthropics/skills
监控 https://gitee.com/mindspore/mindspore
监控 GitLab 项目 gitlab-org/gitlab
```

### 查看列表
```
查看监控列表
```

### 手动检查
```
检查所有更新
```

### 删除监控
```
删除监控 anthropics/skills
```

### 定时任务
```
设置定时检查，每1小时/6小时/1天一次
关闭定时检查
```

---

## ⚙️ 飞书通知

- **在 OpenClaw 中使用** → 自动推送，无需配置 ✅
- **其他情况** → 配置环境变量即可：
  ```bash
  export FEISHU_APP_ID="xxx"
  export FEISHU_APP_SECRET="xxx"
  export FEISHU_CHAT_ID="xxx"
  ```

获取飞书配置：https://open.feishu.cn/
