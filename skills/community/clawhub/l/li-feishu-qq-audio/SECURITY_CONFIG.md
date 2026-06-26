# 🔐 安全配置指南

## 1. 凭证管理

### 推荐：使用环境变量

```bash
# 在 ~/.bashrc 或 ~/.profile 中添加
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

**优点**：
- 不存储在文件中
- 不会意外提交到版本控制
- 每个用户独立配置

### 备选：使用 .env 文件

```bash
# 创建 .env 文件
cp .env.example .env
chmod 600 .env
nano .env  # 编辑填入真实凭证
```

**安全要求**：
- 权限必须是 600
- 不要提交到版本控制
- 定期轮换凭证

## 2. 模型下载安全

### 默认：使用镜像（推荐国内使用）

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### 可选：使用官方源

```bash
export HF_ENDPOINT=https://huggingface.co
```

### 可选：离线模型

如果担心网络供应链安全，可以：
1. 手动下载模型到本地目录
2. 设置 `FAST_WHISPER_MODEL_DIR` 指向本地目录

## 3. 多账户安全

### 风险说明

读取 `openclaw.json` 可能接触其他账户凭证。

### 安全做法

1. **优先使用环境变量**：
```bash
export OPENCLAW_ACCOUNT_ID=coder
```

2. **限制账户权限**：
   - 为不同用途创建不同的飞书应用
   - 最小化权限原则

3. **定期审计**：
   - 检查 openclaw.json 中的账户配置
   - 移除不使用的账户

## 4. 修复脚本安全

### fix-debug-leak.sh 风险

此脚本会修改 `/root/.openclaw/extensions/qqbot/` 扩展。

### 安全使用

1. **先备份**：
```bash
cp -r /root/.openclaw/extensions/qqbot /root/.openclaw/extensions/qqbot.backup
```

2. **测试环境验证**：
```bash
# 在测试环境先运行
./scripts/fix-debug-leak.sh --dry-run
```

3. **仅在需要时运行**：
```bash
# 确认需要修复调试信息泄露才运行
./scripts/fix-debug-leak.sh
```

## 5. 生产环境检查清单

### 安装前

- [ ] 审查所有脚本内容
- [ ] 确认凭证来源可靠
- [ ] 准备回滚方案

### 安装时

- [ ] 使用 `--dry-run` 测试（如果支持）
- [ ] 记录安装过程
- [ ] 验证依赖版本

### 安装后

- [ ] 检查日志输出
- [ ] 验证功能正常
- [ ] 监控资源使用

## 6. 应急响应

### 发现异常怎么办？

1. **立即停止**：
```bash
# 停止任何正在运行的脚本
pkill -f "feishu-tts"
pkill -f "fast-whisper"
```

2. **检查日志**：
```bash
tail -f /tmp/openclaw/*.log
```

3. **回滚更改**：
```bash
# 如果修改了扩展，恢复备份
cp -r /root/.openclaw/extensions/qqbot.backup /root/.openclaw/extensions/qqbot
```

4. **更新凭证**：
   - 重置 FEISHU_APP_SECRET
   - 检查账户异常

## 7. 定期维护

- [ ] 每周检查日志
- [ ] 每月更新依赖
- [ ] 季度审查配置
- [ ] 年度轮换凭证

## 8. 联系与支持

- 发现安全问题请联系作者
- 关注官方更新公告
- 参与社区安全讨论

---

**安全是每个人的责任。感谢您的关注！**
