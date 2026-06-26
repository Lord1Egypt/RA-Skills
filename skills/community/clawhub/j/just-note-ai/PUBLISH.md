# just-note 发布指南

**版本**: v0.2.0  
**发布时间**: 2026-03-26

---

## 一、发布前准备

### 1.1 检查清单

- [x] SKILL.md 完整
- [x] README.md 清晰
- [x] CLI 工具可执行
- [x] 测试通过
- [x] 文档齐全
- [ ] ClawHub 登录

### 1.2 发布信息

| 字段 | 值 |
|------|------|
| **Slug** | `just-note` |
| **Name** | 记一下 |
| **Version** | 0.2.0 |
| **Description** | 像发消息一样记录一切，AI 自动分类整理 |
| **Tags** | note, ai, knowledge, productivity |

---

## 二、发布步骤

### 方式 1: 使用 ClawHub CLI（推荐）

#### 步骤 1: 登录

```bash
npx clawhub@latest login
```

会打开浏览器，登录 ClawHub 账号。

#### 步骤 2: 发布

```bash
cd ~/openclaw/workspace/skills/just-note
npx clawhub@latest publish . \
  --slug just-note \
  --name "记一下" \
  --version 0.2.0 \
  --changelog "MVP 完成：记录/查询/统计/导出功能，AI 自动分类" \
  --tags "note,ai,knowledge,productivity"
```

#### 步骤 3: 验证

访问：https://clawhub.ai/skills/just-note

---

### 方式 2: 手动上传（备用）

1. 访问 https://clawhub.ai
2. 登录账号
3. 点击 "Publish Skill"
4. 上传 `just-note` 文件夹
5. 填写信息：
   - Slug: `just-note`
   - Name: `记一下`
   - Version: `0.2.0`
   - Description: `像发消息一样记录一切，AI 自动分类整理`
   - Tags: `note, ai, knowledge, productivity`
6. 提交发布

---

## 三、安装测试

发布后，测试安装：

```bash
# 安装
npx clawhub@latest install just-note

# 测试
just-note help
just-note write --type expense --amount 200 --tags "test" --content "测试安装"
just-note today
```

---

## 四、发布后检查

### 4.1 ClawHub 页面检查

访问：https://clawhub.ai/skills/just-note

检查项：
- [ ] 页面显示正常
- [ ] 版本正确（0.2.0）
- [ ] 描述清晰
- [ ] 标签正确
- [ ] 安装按钮可用

### 4.2 安装测试

```bash
# 新环境测试
npx clawhub@latest install just-note
just-note --version
```

### 4.3 文档检查

- [ ] README.md 显示正常
- [ ] 示例代码正确
- [ ] 使用说明清晰

---

## 五、推广建议

### 5.1 社区推广

1. **OpenClaw Discord** - 发布到 #skills 频道
2. **GitHub** - 创建 GitHub 仓库
3. **社交媒体** - Twitter/微博分享

### 5.2 文档完善

- [ ] 添加视频教程
- [ ] 补充更多使用场景
- [ ] 收集用户反馈

---

## 六、版本规划

### v0.3.0（下周）

- [ ] AI 消息集成
- [ ] 语义检索
- [ ] 智能关联

### v0.4.0（下月）

- [ ] Web 界面
- [ ] 多端同步
- [ ] 插件系统

### v1.0.0（未来）

- [ ] 稳定版
- [ ] 完整文档
- [ ] 用户案例

---

## 七、常见问题

### Q: 发布失败怎么办？

A: 检查：
1. 是否登录（`clawhub whoami`）
2. slug 是否重复
3. 版本号是否正确

### Q: 如何更新版本？

A: 修改 version，重新发布：
```bash
npx clawhub@latest publish . --slug just-note --version 0.3.0 --changelog "新增 AI 消息集成"
```

### Q: 如何删除已发布的 skill？

A: 
```bash
npx clawhub@latest delete just-note
```

---

## 八、发布命令速查

```bash
# 登录
npx clawhub@latest login

# 发布
npx clawhub@latest publish . --slug just-note --name "记一下" --version 0.2.0 --changelog "MVP 完成" --tags "note,ai,knowledge,productivity"

# 查看已发布
npx clawhub@latest inspect just-note

# 更新版本
npx clawhub@latest publish . --slug just-note --version 0.3.0 --changelog "新增功能"

# 删除
npx clawhub@latest delete just-note
```

---

## 九、发布状态

| 步骤 | 状态 | 说明 |
|------|------|------|
| 代码准备 | ✅ 完成 | 所有文件就绪 |
| 文档准备 | ✅ 完成 | README/SKILL.md 等 |
| 测试 | ✅ 完成 | 测试通过 |
| ClawHub 登录 | ⏳ 待完成 | 需要浏览器登录 |
| 发布 | ⏳ 待完成 | 等待登录 |
| 验证 | ⏳ 待完成 | 发布后验证 |

---

## 十、联系支持

如有问题：
- ClawHub 文档：https://clawhub.ai/docs
- OpenClaw Discord: https://discord.gg/clawd
- GitHub Issues: https://github.com/openclaw/clawhub/issues

---

**下一步**: 运行 `npx clawhub@latest login` 登录，然后发布。
