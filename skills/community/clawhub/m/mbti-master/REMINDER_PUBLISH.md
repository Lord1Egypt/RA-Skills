# ClawHub发布提醒 - MBTI Master

**创建时间：** 2026-03-03
**发布时间：** 2026-03-17（14天后）
**Skill名称：** mbti-master
**版本：** 1.0.0
**GitHub：** https://github.com/shven273-design/mbti-master

## 待执行任务

### 1. 验证GitHub账号年龄
- [ ] 确认账号已注册满14天
- [ ] 确认可以正常登录ClawHub

### 2. 发布到ClawHub
```bash
# 登录ClawHub
clawhub login --token clh_Blbq6yXG9H9z1HtoogcuAePHMtO9irQfH7uVBGo3w_4

# 验证登录
clawhub whoami

# 进入项目目录
cd /workspace/projects/workspace/skills/mbti-master

# 发布skill
clawhub publish . --version 1.0.0

# 验证发布
clawhub search mbti
```

### 3. 发布后检查
- [ ] 可以在ClawHub搜索到mbti-master
- [ ] 可以正常安装
- [ ] 功能正常

## 备用方案

如果Token过期，需要：
1. 访问 https://clawhub.com
2. 登录后生成新Token
3. 使用新Token登录CLI

## 联系信息

- 作者：ShenJian
- GitHub：shven273-design
- 邮箱：shven273@gmail.com