# 知识工作习惯追踪器

> 专为知识工作者设计的隐私优先、离线第一的习惯与事件记录系统

## 核心特性

- **单习惯专注**：一次只养一个习惯，减少注意力切换
- **隐私优先**：所有数据默认保存在浏览器本地，无自动上传
- **多平台支持**：Web浏览器版 + Electron桌面版 + Android覆盖层
- **事件沉淀**：手动/计时记录形成可追溯证据链
- **节点候选**：重复动作自动聚合，为知识共建准备素材

## 快速安装

```bash
# 通过ClawHub安装
clawhub install knowledge-habit-tracker

# 或手动安装
cd skills/knowledge-habit-tracker
./install.sh
```

## 使用方法

### Web浏览器版
```bash
./start-web.sh
# 打开 http://127.0.0.1:3000
```

### Electron桌面版（带悬浮窗）
```bash
./start-desktop.sh
# 主窗口 + 全局置顶计时窗
```

### 命令行工具
```bash
./habit-cli.sh start-web      # 启动Web版
./habit-cli.sh start-desktop  # 启动桌面版
./habit-cli.sh status         # 检查服务状态
./habit-cli.sh backup         # 查看备份说明
```

## 设计哲学

1. **离线第一**：默认所有操作在浏览器沙箱中完成
2. **数据主权**：用户完全控制数据导出/导入
3. **认知友好**：单习惯设计减少决策疲劳
4. **知识转化**：从个人习惯到集体知识的自然路径

## 与知识共建平台集成

本系统为 [Dragon Palace Knowledge Hub](https://github.com/puppetcat-fire/dragon-palace-knowledge-hub) 提供：

- **节点候选**：习惯事件聚合为可教程化的知识节点
- **点亮事件**：标准化的事件格式对接知识图谱
- **材料挂载**：习惯中使用的工具、方法可作为节点材料

## 隐私保证

- ✅ 所有习惯数据保存在浏览器localStorage
- ✅ 无自动数据上传或同步
- ✅ 反馈日志仅在主动启动服务时写入本地磁盘
- ✅ 支持完全的数据导出/导入（JSON格式）
- ✅ 默认只监听本地地址(127.0.0.1)

## 技术支持

- **文档**：详细功能说明请查看 [SKILL.md](SKILL.md)
- **源代码**：完整项目位于 `../knowledge-habit-tracker/`
- **问题反馈**：[GitHub Issues](https://github.com/puppetcat-fire/openclaw-skills/issues)

## 许可证

MIT License © 2026 柏然