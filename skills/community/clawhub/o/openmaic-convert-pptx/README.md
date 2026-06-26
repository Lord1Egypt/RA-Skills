# OpenMAIC PPT转换工具

一个用于将OpenMAIC课程json文件转换成PPT文件的工具，支持包含演讲者讲稿。脚本会自动查找OpenMAIC安装位置，无需手动指定路径。如果用户没有提供课程ID，则需要询问。

## 功能特性

- ✅ 从OpenMAIC课程JSON文件导出PPT
- ✅ 自动提取所有幻灯片元素
- ✅ 包含演讲者讲稿（可禁用）
- ✅ 保持原始样式和布局
- ✅ 支持通过课程ID或标题查找
- ✅ 自动清理临时文件

## 安装依赖

```bash
# 安装pptxgenjs
npm install pptxgenjs
```

或者如果已经在OpenMAIC项目中：

```bash
cd /path/to/your/OpenMAIC
npm install pptxgenjs
```

## 使用方法

### 命令行使用

```bash
# 通过课程ID导出（脚本会自动查找OpenMAIC路径）
node export_ppt.js LLFqDUArdk

# 通过课程标题导出
node export_ppt.js "什么是 MCP 协议？"

# 导出时不包含讲稿
node export_ppt.js LLFqDUArdk --no-notes

# 手动指定OpenMAIC路径（仅当智能查找失败时使用）
node export_ppt.js LLFqDUArdk --openmaic-path /path/to/your/OpenMAIC
```

### 在OpenClaw中使用

当用户要求导出OpenMAIC课程PPT时：

1. 确认要导出的课程ID或标题
2. 脚本会自动查找OpenMAIC安装位置
3. 运行导出脚本
4. 将生成的PPT文件发送给用户

**注意**：脚本会优先查找用户主目录下的`.openclaw/workspace/OpenMAIC`，这是OpenMAIC的标准安装位置。

## 文件结构

```
export_ppt.js          # 主导出脚本
```

## 输出示例

```
🚀 OpenMAIC课程PPT导出工具
==================================================
🔍 查找课程: "什么是 MCP 协议？"
📁 找到课程文件: /path/to/your/OpenMAIC/data/classrooms/LLFqDUArdk.json
📚 课程: 什么是 MCP 协议？
📋 ID: LLFqDUArdk
🎬 场景数量: 6
📊 幻灯片数量: 5
🗣️  讲稿数量: 36
📐 转换比例 - px转inch: 100, px转pt: 1.3888888888888888

📄 处理幻灯片 1: 什么是 MCP 协议？
  元素数量: 10
  添加讲稿: 6 条

📄 处理幻灯片 2: 核心概念与架构
  元素数量: 13
  添加讲稿: 8 条

📄 处理幻灯片 3: MCP 如何工作？
  元素数量: 18
  添加讲稿: 8 条

📄 处理幻灯片 4: 应用场景与优势
  元素数量: 11
  添加讲稿: 7 条

📄 处理幻灯片 5: 快速入门基础
  元素数量: 13
  添加讲稿: 7 条

💾 正在生成PPT文件: 什么是_MCP_协议？_1742112345678.pptx

🎉 导出完成！
==================================================
课程: 什么是 MCP 协议？
ID: LLFqDUArdk
幻灯片: 5 页
讲稿: 36 条
文件: /path/to/your/workspace/什么是_MCP_协议？_1742112345678.pptx
大小: 106.74 KB
```

## 支持的OpenMAIC元素

| 元素类型 | 支持情况 | 说明 |
|---------|---------|------|
| 文本元素 | ✅ | 支持HTML格式，提取纯文本和样式 |
| 形状元素 | ✅ | 支持矩形、圆形等基本形状 |
| 线条元素 | ✅ | 支持简单线条 |
| 背景设置 | ✅ | 支持主题背景色 |
| 讲稿内容 | ✅ | 支持`speech`类型的讲稿 |

## 样式转换

- **颜色**：HEX、RGB、RGBA → PPT颜色格式
- **字体大小**：保持相对比例
- **对齐方式**：左对齐、居中、右对齐
- **文本样式**：粗体、斜体

## 故障排除

### 常见问题

1. **课程文件不存在**
   ```
   ❌ 未找到课程: "课程名称"
   ```
   解决方案：检查课程ID或标题是否正确

2. **OpenMAIC目录不存在**
   ```
   ❌ OpenMAIC目录不存在: /path/to/OpenMAIC
   ```
   解决方案：脚本会自动查找OpenMAIC安装位置，如果找不到请使用`--openmaic-path`参数手动指定

3. **依赖缺失**
   ```
   Error: Cannot find module 'pptxgenjs'
   ```
   解决方案：确保OpenMAIC已正确安装，脚本会自动使用OpenMAIC项目中的`pptxgenjs`库

4. **智能路径查找失败**
   ```
   📁 使用的OpenMAIC路径: /path/to/OpenMAIC
   ```
   如果路径不正确，请使用`--openmaic-path`参数手动指定正确路径

### 调试模式

如需更多调试信息，可以修改脚本添加详细日志。

## 注意事项

1. **文件权限**：确保有读写权限
2. **大文件处理**：大型课程导出可能需要较长时间
3. **样式兼容性**：某些OpenMAIC样式可能无法完全转换
4. **临时文件**：导出完成后会自动清理

## 更新日志

### v1.1.0 (2026-03-17)
- **智能路径查找**：自动查找OpenMAIC安装位置，无需手动指定路径
- **查找顺序优化**：优先查找用户主目录下的`.openclaw/workspace/OpenMAIC`
- **环境变量支持**：支持`OPENCLAW_HOME`环境变量指定路径
- **路径查找增强**：支持从当前目录向上查找OpenMAIC文件夹

### v1.0.0 (2026-03-16)
- 初始版本发布
- 支持基本PPT导出功能
- 包含演讲者讲稿
- 支持样式转换

## 许可证

本项目采用 MIT 开源协议。详见 [LICENSE](LICENSE) 文件。

### MIT 许可证摘要

- ✅ 允许商业使用
- ✅ 允许修改
- ✅ 允许分发
- ✅ 允许私人使用
- ✅ 包含版权声明
- ✅ 包含许可证声明
- ❌ 无责任限制
- ❌ 无专利授权
- ❌ 无商标授权

**完整条款请查看 [LICENSE](LICENSE) 文件。**