# one-mail 版本历史

## v1.0.3 (2026-03-07)

### 修改
- 更新 SKILL.md 为中文描述
- 优化中文用户体验
- 统一文档语言为中文

### 改进
- 插件说明中文化
- 更清晰的功能描述
- 更友好的使用指南

---

## v1.0.2 (2026-03-07)

### 新增
- ✅ Outlook 附件支持（< 3MB 文件）
  - 实现 Microsoft Graph API fileAttachment
  - 自动 base64 编码
  - 文件大小验证和错误处理
  - 大文件（> 3MB）提示使用 OneDrive 分享

### 修改
- 更新文档反映 Outlook 附件支持
- 改进附件失败的错误消息
- 更新 README.md 和 SKILL.md

### 测试
- ✅ Outlook 附件发送测试通过
- ✅ 附件接收验证通过

---

## v1.0.1 (2026-03-07)

### 修复
- ✅ 网易邮箱 IMAP ID 支持
  - 添加自动发送 IMAP ID 命令
  - 符合网易邮箱客户端标识要求
  - 添加测试脚本 `test-163-imap.py`

### 文档
- 更新 README.md 添加 IMAP ID 说明
- 添加网易邮箱连接测试方法

---

## v1.0.0 (2026-03-07)

### 首次发布

**核心功能**
- ✅ 多账户管理（Gmail、Outlook、网易邮箱）
- ✅ 统一收发接口
- ✅ 跨账户搜索
- ✅ 附件支持（Gmail、网易邮箱）
- ✅ JSON 输出格式
- ✅ 安全凭证存储

**脚本**
- `setup.sh` - 初始化配置
- `fetch.sh` - 收取邮件
- `send.sh` - 发送邮件
- `accounts.sh` - 账户管理
- `stats.sh` - 邮件统计
- `test.sh` - 功能测试
- `demo.sh` - 功能演示
- `onemail` - CLI 主入口
- `install.sh` - 系统安装
- `uninstall.sh` - 系统卸载

**适配器**
- `lib/gmail.sh` - Gmail 适配器（基于 gog CLI）
- `lib/outlook.sh` - Outlook 适配器（Microsoft Graph API）
- `lib/163.sh` - 网易邮箱适配器（IMAP/SMTP）
- `lib/common.sh` - 公共函数库

**文档**
- `SKILL.md` - Skill 定义
- `README.md` - 详细文档
- `QUICKSTART.md` - 快速入门
- `EXAMPLES.md` - 使用示例
- `PROJECT.md` - 项目总结

**配置**
- `skill.json` - Skill 元数据
- `config.template.json` - 配置模板
- `credentials.template.json` - 凭证模板
- `Makefile` - 任务管理
- `.gitignore` - Git 忽略规则

**依赖**
- bash 4.0+
- jq
- curl
- openssl
- python3
- gog (可选)

---

## 未来计划

### v1.1.0
- [x] Outlook 附件支持 ✅ (已完成于 v1.0.2)
- [ ] 网易邮箱连接测试
- [ ] 邮件详情查看（view.sh）
- [ ] 邮件标记功能（mark.sh）
- [ ] HTML 邮件支持

### v1.2.0
- [ ] 支持 QQ 邮箱
- [ ] 支持 Hotmail
- [ ] 邮件模板功能
- [ ] 邮件规则和过滤器
- [ ] 邮件标签和分类
- [ ] Outlook 大文件附件（> 3MB，使用上传会话）

### v2.0.0
- [ ] Web UI 界面
- [ ] 邮件搜索优化
- [ ] 性能优化和缓存
- [ ] 多语言支持
- [ ] 插件系统

---

**作者**: Huang Baixun ([@huangbaixun](https://github.com/huangbaixun))  
**许可证**: MIT  
**仓库**: https://github.com/huangbaixun/one-mail
