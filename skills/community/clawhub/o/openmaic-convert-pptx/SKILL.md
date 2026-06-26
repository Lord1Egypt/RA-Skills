# OpenMAIC-convert-pptx

**OpenMAIC课程PPT转换工具**

## 描述

一个用于将OpenMAIC课程json文件转换成PPT文件的工具，支持包含演讲者讲稿。支持通过命令行参数指定OpenMAIC安装路径，灵活适应不同的安装环境。

## 使用场景

当用户需要：
- 从OpenMAIC课程导出PPT文件
- 获取包含演讲者讲稿的完整演示文稿
- 将OpenMAIC生成的课程转换为可分享的PPT格式
- 需要离线使用OpenMAIC课程内容

## 前置条件

1. **OpenMAIC已安装**：确保OpenMAIC已正确安装
2. **课程存在**：目标课程必须在OpenMAIC的`data/classrooms/{课程ID}`目录中
3. **Node.js环境**：需要Node.js运行环境

## 快速开始

### 基本用法

当用户提到"OpenMAIC PPT导出"、"导出OpenMAIC课程PPT"、"下载OpenMAIC PPT"等时，使用此技能。

### 快速命令
```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/OpenMAIC-convert-pptx

# 2. 导出课程（脚本会自动查找OpenMAIC路径）
node export_ppt.js <课程ID>

# 3. 查看生成的PPT文件
ls ~/.openclaw/workspace/*.pptx

# 4. 清理测试文件（可选）
rm -f ~/.openclaw/workspace/*.pptx
```

**注意**：脚本会自动查找OpenMAIC安装位置，无需手动指定路径。如果OpenMAIC安装在非标准位置，可以使用`--openmaic-path`参数手动指定。

## 使用方法

### 参数说明

技能支持以下参数：
- **课程ID**：课程的唯一标识符（如 `LLFqDUArdk`）
- **课程标题**：课程的标题（如 "什么是 MCP 协议？"）
- **OpenMAIC路径**：OpenMAIC的安装路径（通过 `--openmaic-path` 参数指定，可选）
- **包含讲稿**：是否在PPT备注中包含演讲者讲稿（默认：是，可通过 `--no-notes` 禁用）

### 智能路径查找

脚本会自动查找OpenMAIC安装位置，查找顺序：
1. **环境变量**：`OPENCLAW_HOME` 环境变量指定的路径 + `/workspace/OpenMAIC`
2. **用户主目录**：`~/.openclaw/workspace/OpenMAIC`（最常见的位置）
3. **当前目录**：从当前目录向上查找OpenMAIC文件夹
4. **OpenClaw工作空间**：查找`.openclaw/workspace/OpenMAIC`目录
5. **默认路径**：`/path/to/your/OpenMAIC`（回退）

**注意**：脚本会优先查找用户主目录下的`.openclaw/workspace/OpenMAIC`，这是OpenMAIC的标准安装位置。

### 操作流程

1. **确认需求**：询问用户要导出的课程ID。如果用户没有提供课程ID，则需要询问
2. **智能路径查找**：脚本会自动查找OpenMAIC安装位置，无需用户手动指定
3. **查找课程文件**：在找到的OpenMAIC路径下的`data/classrooms/{课程ID}`目录中寻找课程json文件
4. **验证课程**：检查课程文件是否存在
5. **生成PPT**：运行导出脚本生成PPT文件
6. **文件位置**：生成的PPT文件会自动保存到 `~/.openclaw/workspace/` 目录
7. **发送文件**：从workspace目录将生成的PPT文件发送给用户
8. **清理临时文件**：发送完成后删除workspace中的临时副本，保持工作空间整洁

**注意**：如果智能路径查找失败，可以手动使用`--openmaic-path`参数指定OpenMAIC路径。

## 文件结构

```
openMAIC-export-ppt/
├── SKILL.md              # 技能说明文档
├── export_ppt.js         # 主导出脚本
└── README.md             # 使用说明
```

## 技术实现

### 核心功能

1. **课程数据解析**：读取OpenMAIC课程JSON文件
2. **幻灯片提取**：提取所有幻灯片场景和元素
3. **讲稿收集**：收集所有`speech`类型的讲稿内容
4. **PPT生成**：使用`pptxgenjs`库生成PPT文件
5. **样式转换**：将OpenMAIC样式转换为PPT样式

### 支持的OpenMAIC元素

- **文本元素**：支持HTML格式的文本，提取纯文本和样式
- **形状元素**：支持矩形、圆形等基本形状
- **线条元素**：支持简单线条
- **背景设置**：支持主题背景色
- **讲稿内容**：支持`speech`类型的讲稿

### 样式转换

- **颜色转换**：支持HEX、RGB、RGBA格式
- **字体大小**：保持相对比例
- **对齐方式**：支持左对齐、居中、右对齐
- **文本样式**：支持粗体、斜体

## 命令行使用方法

### 基本语法
```bash
node export_ppt.js <课程ID或标题> [--openmaic-path <路径>] [--no-notes]
```

### 参数说明
- `<课程ID或标题>`：课程的ID或完整标题（必填）
- `--openmaic-path <路径>`：指定OpenMAIC安装路径（可选，默认：`/path/to/your/OpenMAIC`）
- `--no-notes`：不包含演讲者讲稿（可选，默认包含讲稿）

### 使用样例

#### 样例1：智能路径查找（推荐）
```bash
# 脚本会自动查找OpenMAIC安装位置
node export_ppt.js LLFqDUArdk

# 使用课程标题导出
node export_ppt.js "什么是 MCP 协议？"
```

#### 样例2：指定OpenMAIC路径导出课程（仅当智能查找失败时使用）
```bash
# 手动指定OpenMAIC路径
node export_ppt.js LLFqDUArdk --openmaic-path ~/.openclaw/workspace/OpenMAIC

# 导出课程标题为"什么是 MCP 协议？"的PPT
node export_ppt.js "什么是 MCP 协议？" --openmaic-path ~/.openclaw/workspace/OpenMAIC
```

#### 样例3：不包含讲稿导出
```bash
# 智能查找路径，不包含讲稿
node export_ppt.js LLFqDUArdk --no-notes

# 指定路径，不包含讲稿
node export_ppt.js LLFqDUArdk --openmaic-path ~/.openclaw/workspace/OpenMAIC --no-notes
```

**注意**：在大多数情况下，使用样例1的智能路径查找即可，无需手动指定路径。

## 示例

### 示例1：通过课程ID导出

用户："导出OpenMAIC课程LLFqDUArdk的PPT"

步骤：
1. 确认课程ID：`LLFqDUArdk`
2. 确认OpenMAIC路径：`~/.openclaw/workspace/OpenMAIC`
3. 运行导出脚本：`node export_ppt.js LLFqDUArdk --openmaic-path ~/.openclaw/workspace/OpenMAIC`
4. 发送生成的PPT文件

### 示例2：通过课程标题导出

用户："导出'什么是 MCP 协议？'这个课程的PPT"

步骤：
1. 搜索匹配的课程文件
2. 获取课程ID：`LLFqDUArdk`
3. 确认OpenMAIC路径
4. 运行导出脚本
5. 发送生成的PPT文件

## 故障排除

### 常见问题

1. **课程文件不存在**
   - 检查课程ID是否正确
   - 确认OpenMAIC安装路径是否正确
   - 使用`--openmaic-path`参数指定正确的路径

2. **PPT生成失败**
   - 检查Node.js环境
   - 确认`pptxgenjs`库已安装
   - 确认OpenMAIC路径正确

3. **路径错误**
   - 错误信息：`Cannot find module '/path/to/your/OpenMAIC/packages/pptxgenjs/dist/pptxgen.cjs.js'`
   - 解决方法：脚本会自动查找OpenMAIC路径，如果找不到请使用`--openmaic-path`参数手动指定

4. **智能路径查找失败**
   - 脚本会显示：`使用的OpenMAIC路径: ...`
   - 如果路径不正确，会显示警告信息
   - 使用`--openmaic-path`参数手动指定正确路径
   - **常见原因**：OpenMAIC安装在非标准位置，或环境变量设置不正确

5. **样式不正确**
   - 检查样式转换逻辑
   - 调整转换比例

### 调试信息

导出脚本会输出以下信息：
- 课程名称和场景数量
- 幻灯片数量和讲稿统计
- 转换比例和元素处理情况
- 文件生成路径和大小

## 更新日志

### v1.1.0 (2026-03-17)
- **智能路径查找**：自动查找OpenMAIC安装位置，无需手动指定路径
- **查找顺序优化**：优先查找用户主目录下的`.openclaw/workspace/OpenMAIC`
- **环境变量支持**：支持`OPENCLAW_HOME`环境变量指定路径
- **路径查找增强**：支持从当前目录向上查找OpenMAIC文件夹

### v1.0.0 (2026-03-16)
- 初始版本
- 支持从OpenMAIC课程导出PPT
- 包含演讲者讲稿
- 支持基本样式转换

## 注意事项

1. **文件权限**：确保有读写权限
2. **临时文件**：导出完成后会自动清理临时文件
3. **大文件处理**：对于大型课程，导出可能需要较长时间
4. **样式兼容性**：某些OpenMAIC样式可能无法完全转换到PPT
5. **文件保存位置**：生成的PPT文件会自动保存到 `~/.openclaw/workspace/` 目录中，而不是技能文件夹内。这是为了：
   - 避免污染技能目录
   - 方便用户查找和管理文件
   - 符合OpenClaw的工作空间规范
   - 支持后续的文件发送和分享操作

## 相关技能

- [openmaic](./openmaic/)：OpenMAIC设置和使用指南
- [powerpoint-pptx](./powerpoint-pptx/)：PPTX文件处理技能

## 许可证

本项目采用 MIT 开源协议。详见 [LICENSE](LICENSE) 文件。