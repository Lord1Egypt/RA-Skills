# 联想示例库

> 记录典型任务的联想路径，供快速参照

---

## 壹启健康相关

### 新任务：H5页面改版
```
联想链: 壹启健康 → MEMORY_INDEX §项目 → yiqi-health-project.md
召回: 技术栈 / 部署路径 / 腾讯云配置
教训: UI改版必须先出设计稿 → 用户确认 → 再开发（见MEMORY.md 铁律）
```

### 新任务：腾讯云部署
```
联想链: 壹启健康 → 2026-04-29.md → 腾讯云部署流程
召回: 权限修复命令 / nginx配置 / systemd服务
教训: JAR chmod 644 + h5/admin chmod 755 + chown www-data
```

### 新任务：数据库问题
```
联想链: yiqi-health-project.md → 数据库设计文档
召回: SQLite路径 / JAR必须在项目根目录启动
```

### 新任务：管理后台开发
```
联想链: 2026-04-27.md → 管理后台需求整理
召回: Vue3 + Vite base /admin/ / 静态资源路径
```

---

## 彩色乐园相关

### 新任务：游戏逻辑修改
```
联想链: 彩色乐园 → colorful-park-project.md
召回: Vue 3 + Vite / Docker Compose / 前端构建命令
```

### 新任务：音频处理
```
联想链: 2026-04-20-bgm-cleanup-fix.md
召回: Mac say + ffmpeg后处理 / 67个.m4a文件 / 年轻妈妈音色
```

---

## TikTok / 短视频相关

### 新任务：短视频数据分析
```
联想链: TikTok → tiktok_report.py / tiktok_medical_tourism.py
召回: 工具路径 / 报告模板
```

### 新任务：入境医疗内容
```
联想链: 入境医疗 → inbound-medical-tourism-research.md
召回: 调研报告内容 / TikTok数据
```

---

## OpenClaw 系统相关

### 新任务：Skill安装/配置
```
联想链: clawhub / skills list → skill-creator
召回: 安装命令 / 验证流程
```

### 新任务：子Agent问题排查
```
联想链: SOUL.md → 多Agent架构
召回: Agent团队 / 故障接替规则
```

### 新任务：记忆系统异常
```
联想链: MEMORY_INDEX §OpenClaw配置 → DOCTRINE_SYSTEM.md
召回: 决策原则 / 记忆召回规范
```

---

## 踩坑相关

### 排查：文件权限问题
```
召回: .learnings/ERRORS.md
关键教训: chmod 644 / chmod 755 / chown www-data 三步缺一不可
```

### 排查：npm / brew 安装失败
```
召回: 2026-04-30 操作记录
教训: 国内网络直连npm不稳定，需代理
```

### 排查：Git仓库臃肿
```
召回: 2026-04-30 Git清理记录
命令: git gc --prune=now --aggressive
释放: 4.2GB → 342MB
```

---

## 通用模板

### 每次新任务的联想检查清单

- [ ] 查 MEMORY_INDEX.md 联想链
- [ ] memory_get 相关文件关键段落
- [ ] 检查 .learnings/ERRORS.md 是否有相关踩坑
- [ ] 检查 .learnings/LEARNINGS.md 是否有相关教训
- [ ] 判断：直接继续 / 补充记忆 / 更新索引
