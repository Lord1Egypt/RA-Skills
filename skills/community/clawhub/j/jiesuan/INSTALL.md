# AI智能结算助手 Pro - 安装指南

## 📦 Skill包已准备就绪！

### 包含文件清单

✅ **SKILL.md** (12.46 KB) - 技能说明文档（OpenClaw必需）  
✅ **settlement_engine.py** (16.51 KB) - 核心结算引擎  
✅ **test_topic_rule.py** (4.01 KB) - 测试脚本  
✅ **README.md** (2.34 KB) - Skill包说明  
✅ **UPDATE_v1.1.0.md** (8.20 KB) - v1.1.0更新说明  
✅ **package.json** (1.19 KB) - 包信息文件  
✅ **INSTALL.md** (本文件) - 安装指南  

**总大小**: ~45 KB

---

## 🚀 安装方法

### 方法一：直接复制（推荐）

1. 复制整个 `ai-settlement-pro` 文件夹
2. 粘贴到OpenClaw技能目录：
   ```
   Windows: C:\Users\<用户名>\.openclaw\skills\
   Linux/Mac: ~/.openclaw/skills/
   ```

3. 最终路径应为：
   ```
   .openclaw/skills/ai-settlement-pro/
   ├── SKILL.md
   ├── settlement_engine.py
   ├── test_topic_rule.py
   ├── README.md
   ├── UPDATE_v1.1.0.md
   ├── package.json
   └── INSTALL.md
   ```

### 方法二：通过OpenClaw命令（如支持）

```bash
openclaw skill install ai-settlement-pro
```

### 方法三：从压缩包安装

如果提供了压缩包：

1. 解压 `ai-settlement-pro-v1.1.0.zip`
2. 将解压后的 `ai-settlement-pro` 文件夹移动到技能目录
3. 重启OpenClaw

---

## ✅ 验证安装

### 1. 检查技能是否加载

在OpenClaw中输入：
```
列出所有技能
```

应该能看到 **ai-settlement-pro 🏆**

### 2. 运行测试

```bash
cd ~/.openclaw/skills/ai-settlement-pro/
python test_topic_rule.py
```

如果所有测试通过，说明安装成功！

### 3. 试用技能

```
请帮我结算活动：总奖金1万元，播放量≥1万，携带话题#测试的作者瓜分
```

---

## 🔧 配置要求

### Python环境
- **Python版本**: >= 3.7
- **依赖库**: 无（仅使用标准库）

### 数据要求
- CSV或Excel文件
- 必须包含：作者ID、作者名称、视频标题
- 编码：UTF-8（推荐）

---

## 🆘 常见问题

### Q1: 技能无法加载？
**A**: 检查以下几点：
1. 文件夹名称是否为 `ai-settlement-pro`
2. SKILL.md 文件是否存在
3. 文件编码是否为 UTF-8

### Q2: 话题词识别不准确？
**A**: 确保：
1. CSV文件包含"视频标题"或"标题"字段
2. 话题词格式正确（以#开头）
3. 使用明确的逻辑关键词（且/或）

### Q3: 规则解析失败？
**A**: 检查：
1. 规则描述是否包含奖金金额
2. 条件表达式是否清晰（如"播放量≥3万"）
3. 参考SKILL.md中的示例格式

### Q4: 如何更新技能？
**A**: 
1. 备份当前版本（如有自定义修改）
2. 下载新版本
3. 覆盖原文件夹
4. 重启OpenClaw

---

## 📝 使用示例

### 示例1：简单瓜分
```
总奖金5万元，播放量≥5万的作者瓜分
```

### 示例2：带话题词（单个）
```
总奖金2万元，播放量≥3万，携带话题#金铲铲的作者瓜分
```

### 示例3：带话题词（且关系）
```
奖池3万元，播放量≥2万，同时携带话题#金铲铲和#攻略的作者瓜分
```

### 示例4：带话题词（或关系）
```
总奖金4万，作品≥3条，携带话题#英雄联盟或#云顶之弈的作者瓜分
```

---

## 🔄 卸载方法

如需卸载：

1. 删除技能文件夹：
   ```bash
   rm -rf ~/.openclaw/skills/ai-settlement-pro
   ```

2. 重启OpenClaw

---

## 📞 技术支持

- **文档**: 查看 SKILL.md 获取详细说明
- **更新日志**: 查看 UPDATE_v1.1.0.md
- **问题反馈**: 通过OpenClaw技能市场提交

---

## 📄 许可与版权

© 2026 AI智能结算助手Pro团队  
遵循OpenClaw技能开发规范

---

**安装完成后，开始使用吧！祝结算顺利！🎉**
