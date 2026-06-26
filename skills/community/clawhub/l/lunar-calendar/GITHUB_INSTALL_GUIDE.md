# 🌙 农历生日提醒系统 v0.9.0 - GitHub安装完全指南
## 作者：夏暮辞青
## 助手：小妹 (DeepSeek AI助手)
## 版本：v0.9.0
## 发布日期：2026-02-13

## 🎯 项目概述

**农历生日提醒系统**是一个专业的农历计算系统，提供：
- ✅ 公历↔农历双向精确转换
- ✅ 专业农历计算库集成 (lunardate/cnlunar)
- ✅ 已知日期100%验证通过
- ✅ 完整的测试套件和文档
- ✅ OpenClaw技能集成

## 📦 安装方法

### 方法一：GitHub直接安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/xiamuciqing/lunar-birthday-reminder.git

# 2. 进入项目目录
cd lunar-birthday-reminder

# 3. 安装Python依赖
pip install lunardate cnlunar

# 4. 复制到OpenClaw技能目录
cp -r . /root/.openclaw/workspace/skills/lunar-calendar

# 5. 验证安装
cd /root/.openclaw/workspace/skills/lunar-calendar
python scripts/demo_lunar.py
```

### 方法二：下载发布包安装

```bash
# 1. 下载发布包
wget https://github.com/xiamuciqing/lunar-birthday-reminder/releases/download/v0.9.0/lunar-birthday-reminder-v0.9.0.tar.gz

# 2. 解压
tar -xzf lunar-birthday-reminder-v0.9.0.tar.gz
cd lunar-birthday-reminder

# 3. 运行安装脚本
./install.sh
```

### 方法三：OpenClaw技能市场安装（未来支持）

```bash
# 等待v1.0.0正式版发布后
openclaw skills install lunar-calendar
```

## 🔧 系统要求

### 最低要求
- **操作系统**: Linux, macOS, Windows (WSL)
- **Python**: 3.6 或更高版本
- **内存**: 至少100MB可用空间
- **磁盘空间**: 至少10MB

### 推荐配置
- **Python**: 3.8+
- **内存**: 256MB+
- **网络**: 用于安装依赖和更新

## 📋 安装验证

### 验证步骤
1. **检查Python版本**
   ```bash
   python3 --version
   ```

2. **验证依赖安装**
   ```bash
   python3 -c "import lunardate; print('✅ lunardate 已安装')"
   python3 -c "import cnlunar; print('✅ cnlunar 已安装')"
   ```

3. **运行演示程序**
   ```bash
   python3 scripts/demo_lunar.py
   ```

4. **测试计算功能**
   ```bash
   python3 scripts/lunar_calculator.py --solar 2026-02-17
   python3 scripts/lunar_calculator.py --lunar "2037-09-05"
   ```

### 预期输出
如果安装成功，你应该看到：
```
🌙 农历生日提醒系统演示 - 夏暮辞青
==================================================
📅 公历转农历演示:
------------------------------
2026-02-17 (2026年春节) → 正月初一
...
🎉 演示完成！
```

## 🚀 快速开始

### 基本使用
```python
# 公历转农历
python scripts/lunar_calculator.py --solar 2026-02-17
# 输出: 农历2026年正月初一

# 农历转公历
python scripts/lunar_calculator.py --lunar "2037-09-05"
# 输出: 公历2037-10-13

# 运行验证测试
python scripts/simple_validator.py
```

### 在OpenClaw中使用
当用户询问以下内容时自动激活：
- "农历"、"阴历"、"黄历"、"宜忌"
- "干支"、"生肖"、"节气"
- "春节日期"、"闰月"等

## 📁 项目结构

```
lunar-birthday-reminder/
├── SKILL.md                    # OpenClaw技能元数据
├── README.md                   # 项目文档
├── package.json               # 项目配置 (v0.9.0)
├── RELEASE_v0.9.0.md          # 发布说明
├── INSTALL.md                 # 安装指南
├── scripts/
│   ├── lunar_calculator.py    # 农历计算核心
│   ├── validate_lunar.py      # 验证脚本
│   ├── simple_validator.py    # 简化验证
│   ├── demo_lunar.py          # 演示脚本
│   └── publish.sh             # 发布脚本
├── references/
│   ├── fortune_rules.md       # 黄历宜忌规则
│   └── solar_terms.md         # 二十四节气参考
└── tests/                     # 测试目录
```

## 🧪 测试验证

### 已通过测试
1. ✅ 2022-2026年春节日期验证
2. ✅ 2037年九月初五计算验证
3. ✅ 公历转农历双向验证
4. ✅ 专业库计算结果一致性

### 测试方法
```bash
# 运行完整验证
python scripts/validate_lunar.py

# 运行简化验证
python scripts/simple_validator.py

# 查看验证结果
cat validation_result.txt
```

## 🔄 更新与升级

### 检查更新
```bash
# 查看当前版本
cd /root/.openclaw/workspace/skills/lunar-calendar
cat package.json | grep version

# 检查GitHub最新版本
curl -s https://api.github.com/repos/xiamuciqing/lunar-birthday-reminder/releases/latest | grep tag_name
```

### 升级到新版本
```bash
# 备份当前版本
cp -r /root/.openclaw/workspace/skills/lunar-calendar /root/.openclaw/workspace/skills/lunar-calendar.backup

# 下载新版本
cd /tmp
wget https://github.com/xiamuciqing/lunar-birthday-reminder/releases/download/v1.0.0/lunar-birthday-reminder-v1.0.0.tar.gz
tar -xzf lunar-birthday-reminder-v1.0.0.tar.gz

# 安装新版本
cd lunar-birthday-reminder
./install.sh
```

## 🗑️ 卸载

### 完全卸载
```bash
# 1. 删除技能目录
rm -rf /root/.openclaw/workspace/skills/lunar-calendar

# 2. 卸载Python包（可选）
pip uninstall lunardate cnlunar -y

# 3. 清理缓存
pip cache purge
```

### 部分卸载
```bash
# 只删除技能，保留Python包
rm -rf /root/.openclaw/workspace/skills/lunar-calendar
```

## 🐛 故障排除

### 常见问题

#### 问题1：Python版本问题
**症状**: `python3: command not found`
**解决**:
```bash
# Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-pip

# CentOS/RHEL:
sudo yum install python3 python3-pip
```

#### 问题2：pip安装失败
**症状**: `pip: command not found`
**解决**:
```bash
# 安装pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

#### 问题3：依赖库安装失败
**症状**: `ModuleNotFoundError: No module named 'lunardate'`
**解决**:
```bash
# 使用国内镜像加速
pip install lunardate cnlunar -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者使用conda
conda install -c conda-forge lunardate
```

#### 问题4：权限问题
**症状**: `Permission denied`
**解决**:
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install lunardate cnlunar
```

## 📞 支持与帮助

### 官方支持
- **GitHub Issues**: [问题报告](https://github.com/xiamuciqing/lunar-birthday-reminder/issues)
- **文档**: [README.md](README.md)
- **示例**: [scripts/demo_lunar.py](scripts/demo_lunar.py)

### 社区支持
- **小龙虾社区**: 搜索"农历生日提醒系统"
- **OpenClaw社区**: 技能讨论区
- **技术论坛**: Python相关论坛

### 紧急联系
如果遇到紧急问题，可以通过以下方式联系：
1. GitHub Issues (最快响应)
2. 项目文档中的联系方式
3. 社区@作者

## 📝 贡献指南

### 如何贡献
1. **测试验证**: 测试更多日期并报告结果
2. **数据提供**: 提供权威农历数据参考
3. **代码改进**: 提交Pull Request改进代码
4. **文档完善**: 帮助完善文档和示例

### 反馈渠道
- **GitHub Issues**: 问题报告和功能建议
- **数据校正**: 报告计算差异
- **功能请求**: 提出新功能建议

## ⚠️ 重要声明

### 版本说明
- **当前版本**: v0.9.0参考版本
- **数据源**: 基于lunardate专业库
- **权威性**: 等待国家权威机构数据确认
- **建议用途**: 参考使用，重要日期请多方验证

### 使用限制
- 需要Python环境支持
- 依赖外部库的准确性
- 未集成国家权威数据源
- 部分高级功能待完善

## 🎉 安装完成！

恭喜！农历生日提醒系统 v0.9.0 已成功安装。现在你可以：

1. **开始使用**: 运行演示程序了解功能
2. **测试验证**: 验证重要日期计算结果
3. **提供反馈**: 报告问题或提出建议
4. **参与开发**: 贡献代码或数据

**感谢安装农历生日提醒系统系统！** 🌙

---
*最后更新: 2026-02-13*
*版本: v0.9.0*
*作者: 夏暮辞青*

*如果觉得这个项目有用，请给GitHub仓库点个⭐️支持！*