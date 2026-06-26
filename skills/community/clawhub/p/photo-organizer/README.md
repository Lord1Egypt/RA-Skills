# Photo Organizer - 照片批量整理工具

一个简单但强大的照片批量整理工具，帮助你快速整理成千上万张照片！

## 功能特性
- ✅ 读取照片 EXIF 信息（拍摄时间、GPS 地点等）
- ✅ 按时间自动分类（年/月文件夹结构）
- ✅ 按地点自动分类（如果有 GPS 信息）
- ✅ 批量打标签（计划中）
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装

### 方法一：通过 clawhub 安装
```bash
clawhub install photo-organizer
```

### 方法二：作为 Python 脚本运行
```bash
# 克隆或下载项目
git clone <repo-url>
cd photo-organizer

# 安装依赖（如果需要）
pip install Pillow
```

## 依赖
- Python 3.6+
- Pillow（可选，用于读取 EXIF 信息）

## 快速开始

### 1. 按时间整理照片
```bash
python3 photo_organizer.py organize ./photos --by date --output ./organized
```

这会将你的照片按照拍摄时间整理到这样的文件夹结构中：
```
organized/
├── 2026/
│   ├── 03/
│   │   ├── photo1.jpg
│   │   └── photo2.jpg
│   └── 04/
└── 2025/
```

### 2. 按地点整理照片（需要 GPS 信息）
```bash
python3 photo_organizer.py organize ./photos --by location --output ./organized
```

如果你的照片有 GPS 信息，会按照地点整理（当前版本按年份+地点文件夹）。

### 3. 预览模式（不实际执行，先看效果）
```bash
python3 photo_organizer.py organize ./photos --by date --preview
```

这会显示整理方案，但不会实际移动文件。确认没问题后再去掉 --preview 参数执行。

### 4. 撤销操作
如果你整理错了，可以随时撤销：
```bash
python3 photo_organizer.py undo ./organized
```

## 详细使用说明

### organize 命令参数
- `directory`：（必需）照片所在的目录
- `--by`：整理方式，可选 `date`（按时间，默认）或 `location`（按地点）
- `--output`：输出目录，默认在输入目录下创建 `organized` 文件夹
- `--preview`：预览模式，只显示方案不实际执行

### 关于 EXIF 信息
- 工具会优先读取照片的 EXIF 信息中的拍摄时间
- 如果没有 EXIF 信息，会使用文件的修改时间
- GPS 功能需要照片中有 GPS 信息

### 安全性
- 工具默认使用复制而非移动，原照片不会被删除
- 执行前会自动保存备份
- 支持一键撤销操作
- 建议先用 --preview 预览效果

## 示例场景

### 场景 1：整理手机照片
```bash
# 将手机 DCIM 文件夹里的照片按时间整理
python3 photo_organizer.py organize ./DCIM --by date --output ./my-photos
```

### 场景 2：旅行照片整理
```bash
# 将旅行照片按地点整理（如果有 GPS）
python3 photo_organizer.py organize ./trip-photos --by location --output ./trip-by-place
```

### 场景 3：先预览，再执行
```bash
# 第一步：预览
python3 photo_organizer.py organize ./photos --by date --preview

# 第二步：确认没问题后执行
python3 photo_organizer.py organize ./photos --by date --output ./organized
```

## 配置文件（计划中）
未来版本将支持配置文件 `~/.photo-organizer.json`：
```json
{
  "output_dir": "./organized",
  "folder_structure": "{year}/{month}",
  "auto_tag": true,
  "backup_original": true
}
```

## 故障排除

### 问题：找不到 Pillow 库
**解决方法**：
```bash
pip install Pillow
```

### 问题：照片没有按正确时间整理
**原因**：照片可能没有 EXIF 信息
**解决方法**：工具会使用文件修改时间作为备选

### 问题：撤销失败
**原因**：备份文件可能被删除或修改
**解决方法**：确保在同一目录下执行，且备份文件未被删除

## 开发计划
- [ ] 按地点整理的完整功能（GPS 坐标转地点名称）
- [ ] 标签功能
- [ ] 人脸识别和分类
- [ ] 智能事件分组
- [ ] GUI 界面

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License

---

**Photo Organizer** - 让照片整理变得简单！📸
