# 项目截图使用指南

本目录用于存放项目截图和示例图片。

## 📷 推荐的截图类型

### 1. 产品界面截图
| 截图名称 | 内容 | 用途 |
|---------|------|------|
| `screenshot_workbuddy_main.png` | WorkBuddy 主界面 | README 展示 |
| `screenshot_skill_list.png` | Skills 列表（显示本技能） | 使用指南 |
| `screenshot_import_skill.png` | 导入 Skill 界面 | 安装教程 |

### 2. 操作步骤截图
| 截图名称 | 内容 | 用途 |
|---------|------|------|
| `screenshot_init.png` | 初始化知识库 | 使用指南 |
| `screenshot_folder_empty.png` | 空文件夹（待处理图片） | 使用指南 |
| `screenshot_folder_with_images.png` | 放入图片后的文件夹 | 使用指南 |
| `screenshot_processing.png` | AI 正在处理 | 使用指南 |
| `screenshot_complete.png` | 处理完成提示 | 使用指南 |

### 3. 文档效果截图
| 截图名称 | 内容 | 用途 |
|---------|------|------|
| `screenshot_word_doc.png` | Word 文档效果 | README 展示 |
| `screenshot_md_doc.png` | Markdown 文档效果 | README 展示 |
| `screenshot_folder_structure.png` | 目录结构 | 使用指南 |

### 4. 对比效果截图（用于推广）
| 截图名称 | 内容 | 用途 |
|---------|------|------|
| `screenshot_before.png` | 原始截图（处理前） | 推广素材 |
| `screenshot_after.png` | 整理后的文档（处理完） | 推广素材 |

---

## 📸 如何准备截图

### Windows 截图方法

#### 方法一：PrintScreen 键
1. 按 `PrtSc` 键（全屏截图）
2. 打开画图工具（Win + R → 输入 `mspaint`）
3. 粘贴（Ctrl + V）
4. 保存为 PNG 格式

#### 方法二：Win + Shift + S（推荐）
1. 按 `Win + Shift + S`
2. 选择截图区域
3. 截图自动复制到剪贴板
4. 粘贴到文件并保存

#### 方法三：使用 Snipaste（第三方工具）
- 下载：https://www.snipaste.com/
- 按 F1 截图，F3 贴图

---

## 📂 目录结构示例

```
assets/
└── screenshots/
    ├── 产品界面/
    │   ├── workbuddy_main.png
    │   ├── skill_list.png
    │   └── import_skill.png
    ├── 操作步骤/
    │   ├── init.png
    │   ├── folder_empty.png
    │   ├── folder_with_images.png
    │   ├── processing.png
    │   └── complete.png
    ├── 文档效果/
    │   ├── word_doc.png
    │   ├── md_doc.png
    │   └── folder_structure.png
    └── 对比效果/
        ├── before.png
        └── after.png
```

---

## 📝 在 README.md 中添加截图

准备好截图后，可以在 README.md 中添加以下部分：

```markdown
## 📸 效果展示

### 处理前（原始截图）
![处理前](assets/screenshots/对比效果/before.png)

### 处理完（生成的文档）
![处理完](assets/screenshots/对比效果/after.png)

### Word 文档效果
![Word 文档](assets/screenshots/文档效果/word_doc.png)

### Markdown 文档效果
![Markdown 文档](assets/screenshots/文档效果/md_doc.png)
```

---

## 🚀 快速开始

1. **准备截图**：按照上面的推荐清单拍摄
2. **放入目录**：将截图文件放入 `assets/screenshots/` 对应子目录
3. **提交到 Git**：
   ```bash
   git add assets/screenshots/
   git commit -m "docs: add project screenshots"
   git push origin master
   ```
4. **更新 README**：在 README.md 中添加截图展示部分

---

## 💡 提示

- ✅ 使用 PNG 格式（清晰度更高）
- ✅ 截图分辨率建议 1920x1080 或 1280x720
- ✅ 确保截图中的文字清晰可读
- ✅ 可以稍后补充，不影响项目正常使用

---

**祝你使用愉快！** 🎉
