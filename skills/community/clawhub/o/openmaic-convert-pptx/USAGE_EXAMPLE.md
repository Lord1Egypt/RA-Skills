# OpenMAIC PPT转换技能使用示例

## 场景：用户要求导出OpenMAIC课程PPT

### 用户输入
"帮我导出OpenMAIC课程'什么是 MCP 协议？'的PPT"

### OpenClaw助理响应流程

1. **识别技能需求**
   - 用户提到"OpenMAIC课程"和"导出PPT"
   - 匹配到`openMAIC-export-ppt`技能

2. **确认课程信息**
   ```
   我来帮你导出OpenMAIC课程的PPT。
   
   请确认：
   1. 课程ID或标题："什么是 MCP 协议？"
   2. 是否需要包含演讲者讲稿？（默认包含）
   ```

3. **执行导出流程**
   ```javascript
   // 1. 检查OpenMAIC安装
   const OPENMAIC_PATH = '/path/to/your/OpenMAIC';
   // 2. 查找课程文件
   const courseFile = findCourseFile('什么是 MCP 协议？');
   // 3. 运行导出脚本
   const result = await exportCoursePPT(courseFile);
   ```

4. **发送结果**
   ```
   ✅ PPT导出完成！
   
   📊 导出详情：
   - 课程：什么是 MCP 协议？
   - ID：LLFqDUArdk
   - 幻灯片：5页
   - 讲稿：36条
   - 文件大小：106.7 KB
   
   这是生成的PPT文件，已包含完整的演讲者讲稿：
   ```
   [发送PPT文件]

5. **清理临时文件**
   ```bash
   rm -f 什么是_MCP_协议？_*.pptx
   ```

## 完整对话示例

**用户**：帮我导出OpenMAIC课程LLFqDUArdk的PPT

**助理**：我来帮你导出OpenMAIC课程的PPT。

请确认：
1. 课程ID：LLFqDUArdk
2. 是否需要包含演讲者讲稿？（默认包含）

**用户**：确认，包含讲稿

**助理**：🚀 开始导出OpenMAIC课程PPT...
```
📚 课程：什么是 MCP 协议？
📋 ID：LLFqDUArdk
🎬 场景数量：6
📊 幻灯片数量：5
🗣️  讲稿数量：36
📐 转换比例 - px转inch: 100, px转pt: 1.3888888888888888

📄 处理幻灯片 1: 什么是 MCP 协议？
  元素数量：10
  添加讲稿：6条

📄 处理幻灯片 2: 核心概念与架构
  元素数量：13
  添加讲稿：8条

📄 处理幻灯片 3: MCP 如何工作？
  元素数量：18
  添加讲稿：8条

📄 处理幻灯片 4: 应用场景与优势
  元素数量：11
  添加讲稿：7条

📄 处理幻灯片 5: 快速入门基础
  元素数量：13
  添加讲稿：7条

💾 正在生成PPT文件...
✅ PPT文件已生成
```

🎉 导出完成！

📊 导出详情：
- 课程：什么是 MCP 协议？
- ID：LLFqDUArdk
- 幻灯片：5页
- 讲稿：36条
- 文件大小：106.7 KB

这是生成的PPT文件，已包含完整的演讲者讲稿：
[发送PPT文件]

## 技能触发关键词

当用户输入包含以下关键词时，触发此技能：

- "OpenMAIC PPT导出"
- "导出OpenMAIC课程PPT"
- "下载OpenMAIC PPT"
- "OpenMAIC课程转PPT"
- "OpenMAIC导出演示文稿"

## 参数处理

### 课程标识
- 优先使用课程ID（如 `LLFqDUArdk`）
- 也支持课程标题（如 "什么是 MCP 协议？"）
- 自动搜索匹配的课程文件

### 讲稿选项
- 默认包含演讲者讲稿
- 可通过`--no-notes`参数禁用
- 用户可明确要求"不要讲稿"或"只要幻灯片"

## 错误处理示例

### 课程不存在
**用户**：导出课程"不存在的课程"的PPT

**助理**：❌ 未找到课程："不存在的课程"

请检查：
1. 课程ID或标题是否正确
2. OpenMAIC中是否有该课程
3. 课程文件是否在 `data/classrooms/` 目录中

### OpenMAIC未安装
**助理**：❌ OpenMAIC目录不存在

请先安装OpenMAIC：
1. 克隆OpenMAIC仓库
2. 安装依赖
3. 启动服务

### 依赖缺失
**助理**：❌ 缺少依赖：pptxgenjs

正在安装依赖...
```
npm install pptxgenjs
```
✅ 依赖安装完成，重新尝试导出

## 最佳实践

1. **确认需求**：始终先确认课程信息和讲稿需求
2. **进度反馈**：导出过程中提供进度反馈
3. **详细报告**：导出完成后提供详细统计信息
4. **文件清理**：发送文件后清理临时文件
5. **错误处理**：提供清晰的错误信息和解决方案

## 技能集成

此技能可与以下技能配合使用：

1. **openmaic技能**：OpenMAIC设置和课程创建
2. **powerpoint-pptx技能**：PPT文件进一步编辑
3. **feishu-file-sender技能**：将PPT发送到飞书