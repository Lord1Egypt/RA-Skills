<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-11 -->

# OPC智脑 - 故障排查指南

## IDE路径速查

| IDE | Skills路径 | 配置文件 |
|-----|----------|---------|
| 码道IDE | `.codeartsdoer/skills/` | `.codeartsdoer/agents/opc-zhinao.json` |
| CodeBuddy | `.codebuddy/skills/` | `.codebuddy/skills-registry.json` |
| Cursor | `skills/` | `.cursorrules` |
| VSCode | `skills/` | `.github/copilot-instructions.md` |
| 其他 | `skills/` | `AGENTS.md` |

---

## 快速诊断流程

```
遇到问题 → 检查安装(文件是否存在) → 检查IDE识别(重启IDE) → 检查触发词 → 检查配置格式 → 仍未解决→提交Issue
```

一键检查（码道IDE示例，其他IDE替换路径）：

```bash
echo "=== OPC智脑诊断 ==="
ls -lh AGENTS.md                                          # AGENTS.md存在
file AGENTS.md                                            # 编码应为UTF-8
ls -la .codeartsdoer/agents/opc-zhinao.json               # 配置文件存在
ls -d .codeartsdoer/skills/*/ | wc -l                     # Skills数量=8
echo "=== 诊断完成 ==="
```

---

## 安装问题

### 权限不足

```bash
sudo bash install-prompt.sh /path/to/project
# 或
chmod -R 755 /path/to/project
```

### 路径不存在

```bash
mkdir -p /path/to/project && bash install-prompt.sh /path/to/project
```

### 文件冲突

安装脚本会提示是否覆盖。如需保留旧文件：`mv AGENTS.md AGENTS.md.backup` 后重新安装。

### 网络问题

```bash
# 检查网络
ping gitee.com
# 手动下载：https://gitee.com/zx_allen_li/opc_skills/repository/archive/main.zip
unzip opc_skills-main.zip && cd opc_skills-main
bash install-prompt.sh /path/to/project
```

### 依赖缺失（git未安装）

```bash
# macOS
brew install git
# Ubuntu
sudo apt-get install git
```

---

## 使用问题

### Skills无法触发

1. 确认安装成功（Skills数量=8）
2. 使用正确触发关键词：

| Skill | 触发关键词 |
|-------|----------|
| Skill1 | 创业Idea、想法、点子、可行性、需求验证 |
| Skill2 | MVP、产品设计、功能裁剪、交付成本、首单 |
| Skill3 | 注册公司、个体户、合规、财税、经营范围 |
| Skill4 | 获客、种子用户、冷启动、定价、付费验证 |
| Skill5 | 规模化、增长引擎、自动化、品牌、复购 |

3. 重启IDE

### 输出格式异常

重新安装：`bash install-prompt.sh .`。如AGENTS.md损坏，从仓库重新下载。

### 阶段判定错误

提供完整的6项核心信息（行业赛道、是否有Idea、是否有产品、是否注册公司、是否有付费用户、个人背景），使用量化数据。

### 响应慢

检查网络延迟（`ping api.openai.com`），关闭不必要插件，分步骤提问。

---

## 配置问题

### 自定义Skill不生效

1. 重启IDE 2. 检查SKILL.md格式（需含YAML frontmatter） 3. 检查文件权限（644）

### 触发关键词不生效

编辑`AGENTS.md`的"九、Skills 触发规则"表格，修改后重启IDE。验证：`grep "关键词" AGENTS.md`

### 路径配置错误

对照上方"IDE路径速查"表，修正文件位置。示例：`mv skills .codeartsdoer/skills`

---

## 兼容性问题

### IDE版本不兼容

升级IDE到最新版。如仍不支持Skills，使用通用Prompt模式：`bash install-prompt.sh /path/to/project`

### Windows系统

使用Git Bash或WSL执行脚本：`bash install-prompt.sh /c/path/to/project`

### 中文乱码

```bash
file AGENTS.md                    # 检查编码，应为UTF-8
iconv -f GBK -t UTF-8 AGENTS.md > AGENTS-utf8.md && mv AGENTS-utf8.md AGENTS.md
export LANG=en_US.UTF-8           # macOS/Linux设置编码
```

---

## 获取帮助

- 仓库：https://gitee.com/zx_allen_li/opc_skills.git
- Issue：https://gitee.com/zx_allen_li/opc_skills/issues
- 作者：李屹镒（公众号：科技新潮。视频号：小李君与AI）

提交Issue时请附：操作系统、IDE及版本、OPC智脑版本、复现步骤、期望vs实际结果。

---

**最后更新**：2026-06-11
