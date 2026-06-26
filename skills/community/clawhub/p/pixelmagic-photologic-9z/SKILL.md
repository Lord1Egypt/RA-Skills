---
name: image-editor
description: "专业图像后期处理工具。支持多种修图风格（末日大片、日系清新、复古胶片等），自动检测并安装 ImageMagick，支持 RAW/JPG/PNG 等多种格式，提供批量处理和自定义预设功能。Use when: (1)用户需要修图/调色/加滤镜, (2)处理 RAW 格式照片, (3)批量处理图片, (4)创建自定义修图预设"
---

# 专业图像后期处理工具

## 功能特性

- ✅ 自动检测并安装 ImageMagick
- ✅ 多种修图风格预设
- ✅ 支持 RAW/JPG/PNG/TIFF 等格式
- ✅ 批量处理支持
- ✅ 自定义预设保存
- ✅ 中间文件隔离管理

## 修图风格预设

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| `apocalyptic` | 低饱和、青橙色调、暗角、颗粒 | 末日、科幻、电影感 |
| `japanese` | 高明度、低对比、偏青绿 | 日系清新、日常记录 |
| `vintage` | 暖色调、褪色感、柔焦 | 复古、怀旧 |
| `bw-high` | 黑白、高对比 | 纪实、艺术 |
| `custom` | 用户自定义参数 | 个性化需求 |

## 使用方法

### 单张处理

```python
from scripts.editor import ImageEditor

editor = ImageEditor()
result = editor.process(
    input_path="photo.dng",
    style="apocalyptic",
    output_name="my_photo"
)
```

### 批量处理

```python
editor.batch_process(
    input_dir="./photos",
    style="japanese",
    output_dir="./output"
)
```

### 自定义预设

```python
# 创建自定义预设
editor.create_preset(
    name="my_style",
    params={
        "brightness_contrast": "-10x30",
        "modulate": "100,70",
        "tint": "#3a5a4a",
        "gamma": 0.95,
        "sharpen": "0x1.2",
        "noise": 0.3,
        "vignette": True
    }
)
```

## 工作流程（迭代式分步修图法）

### 核心原则

- 必须采用迭代式分步修图法，确保每一步效果达标后再进行下一步，最终从原始图一次性生成无压缩损失的最终图像。
- 除非风格指定偏向高对比，否则不要增加对比度指令。
- 除非风格偏向，否则尽可能保证图像明暗的顺滑过渡，保留高光和暗部细节。
- 多模态模型在检验中间和最终图像时，要注意有没有因为过度拉参数导致的颜色断层，杂色，色斑色块等不正常现象。

### 详细步骤

#### 1. 初始化
- 检测 ImageMagick，未安装则提示安装
- 分析原始图片（分辨率、格式、色彩空间）
- **根据原始图片文件名创建独立工作目录**（避免不同图片的文件混淆，如果有重名就加-001,-002...这样的后缀）：
  ```
  workspace/image-editor-work/
  ├── {filename}/         # 以原始图片文件名命名的目录
  │   ├── temp/           # 中间处理文件
  │   │   ├── step01.jpg
  │   │   ├── step02.jpg
  │   │   └── params/     # 每步成功参数记录
  │   │       ├── step01_params.txt
  │   │       ├── step02_params.txt
  │   │       └── ...
  │   └── final/          # 最终输出
  │       └── xxx_final.jpg
  ├── {filename2}/        # 另一张图片的独立目录
  └── ...
  ```
- **示例**：处理 `IMG_20260329_111232.dng` 时，创建 `image-editor-work/IMG_20260329_111232/` 目录

#### 2. 迭代式分步修图（关键流程）

**核心原则：保留原图动态范围和色深**

对于所有图片（不论是RAW还是其他格式图片），**每步都必须从原始文件开始处理**，叠加之前已验证的参数，避免中间JPG丢失动态范围和色深。

**Step A - 生成中间JPG（仅用于验证，不参与修图流程）**

**核心原则：始终从原始文件开始**

每步处理都**从原始文件开始**，带上之前所有已验证的参数 + 当前步骤新参数，生成中间JPG仅用于多模态验证。

- 命令格式示例：
  ```bash
  # Step 1: 从原始图开始（不降低亮度，避免暗部死黑）
  magick original.dng -brightness-contrast 0x15 -quality 100 step01.jpg

  # Step 2: 仍从原始图开始，叠加Step1参数 + 新参数
  magick original.dng -brightness-contrast 0x15 -modulate 105,65 -quality 100 step02.jpg

  # Step 3: 继续从原始图开始，叠加Step1+Step2参数 + 新参数
  magick original.dng -brightness-contrast 0x15 -modulate 105,65 -fill "#3a5a6a" -tint 20 -quality 100 step03.jpg
  ```

- **JPG质量必须设为最高**：`-quality 100`
- **严禁使用 `-resize` 或 `-crop`**：除非用户明确要求改变尺寸，否则不得改变原始分辨率
- **注意**：ImageMagick 7+ 使用 `magick` 命令即可，不需要 `magick convert`

**重要**：中间JPG仅用于多模态模型验证效果，**绝不作为下一步的输入**。

**Step B - 多模态效果验证**
- 使用多模态模型查看生成的中间JPG
- 判断是否达到该步骤的修图目标
- **如果未达到目标**：
  - 分析原因，调整 magick 参数
  - **重新从原始文件开始**，带上之前所有已验证参数 + 调整后新参数
  - **循环此步骤直到达标**
- **如果达到目标**：
  - 将该步骤的**新增** magick 参数写入 `temp/params/stepXX_params.txt`
  - **继续从原始文件开始**处理下一步，带上所有已验证参数（包括刚记录的）

**关键记忆**：
- 每步都重新读取原始文件
- 参数是累积的：Step N = 原始图 + param1 + param2 + ... + paramN
- 中间JPG只看不用，下一步仍从原始图开始

#### 3. 循环执行
- 对下一个修图步骤重复"Step A → Step B"流程
- 每步达标后记录参数到对应的 `stepXX_params.txt`
- 直到所有修图步骤完成

#### 4. 生成最终图像（关键步骤）

**严禁使用最后一步的中间JPG作为最终输出**。

正确做法：
1. 读取原始图片
2. 依次读取每步记录的参数文件 `stepXX_params.txt`
3. **构建一条完整的 magick 命令链**，按修图步骤顺序拼接所有参数
4. 从原始图一次性生成最终图像：
   ```bash
   magick original.dng \
     -brightness-contrast 0x15 \
     -modulate 105,65 -fill "#2a5a6a" -tint 20 \
     -sharpen 0x1.2 \
     -attenuate 0.4 +noise gaussian \
     -size 4096x3072 radial-gradient:black-white -level 0%,50% -compose blend -define compose:args=25 -composite \
     -quality 100 final_xxx.jpg
   ```

**为什么这样做？**
- 中间JPG经过多次保存，存在JPEG压缩损失
- 从原始图一次性应用所有参数，避免层层压缩
- 最终图像画质最高

#### 5. 收尾与交付

**文件保存：**
- 将最终图像复制到 `final/` 目录
- 可选：清理中间文件或保留供复查
- 记录处理日志

**交付给用户：**

由于 `open_result_view` 工具在某些环境下可能无法直接展示图片预览，**必须同时提供以下信息**：

1. **最终文件路径**（必须提供）
   ```
   最终图像已保存至：C:\Users\z9z\WorkBuddy\Claw\image-editor-work\final\xxx_final.jpg
   ```

2. **尝试使用 open_result_view**（可选）
   ```python
   from tools import open_result_view
   open_result_view(target_file=final_path)
   ```

3. **直接展示图片**（如果环境支持）
   - 使用 `read_file` 读取图片文件，系统可能会自动渲染预览

**完整交付示例：**
```python
final_path = "C:\\Users\\z9z\\WorkBuddy\\Claw\\image-editor-work\\final\\xxx_final.jpg"

# 告知用户文件位置
print(f"修图完成！最终图像保存至：{final_path}")

#将图片发送给用户

# 尝试打开结果视图
try:
    open_result_view(target_file=final_path)
except:
    pass

# 尝试直接展示图片
try:
    read_file(filePath=final_path)
except:
    pass
```


**重要**：无论 `open_result_view` 是否成功显示，都必须明确告知用户文件的本地路径，确保用户能找到成品。

### 流程图示

**统一处理流程（所有格式）：**
```
原始图
   │
   ├──► Step 1 参数 ──► 生成中间JPG ──► [多模态检查] ──► 达标?
   │                                                    │
   │                                                   否 ──► 调整参数 ──► 重新从原始图生成
   │                                                    │
   │                                                   是 ──► 记录参数到 step01_params.txt
   │
   ├──► Step 1+2 参数 ──► 生成中间JPG ──► [多模态检查] ──► 达标?
   │                                                      │
   │                                                     否 ──► 调整参数 ──► 重新从原始图生成
   │                                                      │
   │                                                     是 ──► 记录参数到 step02_params.txt
   │
   ├──► Step 1+2+3 参数 ──► 生成中间JPG ──► [多模态检查] ──► 达标?
   │                                                        │
   │                                                       ...
   ▼
[最终生成] ──► 从原始图一次性应用所有参数 ──► 最终图像 (最高画质)
```

**核心要点：**
- 每步都从**原始文件**开始
- 参数累积：Step N = 原始图 + param1 + param2 + ... + paramN
- 中间JPG**仅用于验证**，绝不参与下一步处理

## 目录结构

```
workspace/
└── image-editor-work/
    ├── {filename1}/        # 图片1的独立工作目录
    │   ├── temp/
    │   │   ├── step01.jpg
    │   │   ├── step02.jpg
    │   │   └── params/
    │   │       ├── step01_params.txt
    │   │       └── step02_params.txt
    │   └── final/
    │       └── {filename1}_final.jpg
    ├── {filename2}/        # 图片2的独立工作目录
    │   ├── temp/
    │   │   ├── step01.jpg
    │   │   └── params/
    │   │       └── step01_params.txt
    │   └── final/
    │       └── {filename2}_final.jpg
    └── ...
```

**命名规范：**
- 工作目录名：`{原始文件名（不含扩展名）}`
- 中间文件：`step{NN}.jpg`
- 参数文件：`step{NN}_params.txt`
- 最终文件：`{原始文件名}_final.jpg`

## 注意事项

- 处理 RAW 格式需要 ImageMagick 支持 RAW 解码
- 大分辨率图片处理耗时较长
- 建议先处理预览图确认效果

## 修图步骤判定标准（给Agent的指引）

### 多模态检查要点

查看中间JPG时，需关注：

| 步骤类型 | 检查要点 | 达标标准 |
|---------|---------|---------|
| **对比度调整** | 高光/阴影细节、整体通透感 | 暗部有细节、亮部不过曝、画面有层次感 |
| **色调调整** | 色温、饱和度、色彩倾向 | 符合目标风格（如青橙色调的青蓝阴影+暖黄高光） |
| **暗角** | 四角压暗程度、过渡自然度 | 四角**适度**压暗、边缘到中心过渡平滑、不突兀 |
| **暗部保护** | 阴影区域是否死黑、有无细节 | 暗部不发死黑，能分辨出纹理和层次；若整体偏暗导致难以判断，需主动提亮检查暗部 |
| **锐化** | 边缘清晰度、噪点控制 | 主体边缘清晰、无明显锯齿或噪点增加 |
| **颗粒** | 颗粒均匀度、自然感 | 胶片质感自然、不破坏细节、颗粒分布均匀 |
| **破坏性修图** | 过度拉参数导致的颜色断层，杂色，色斑色块等 | 颜色自然过度，没有断层，没有非额外添加颗粒效果的噪点，没有杂色和色斑色块 |

### 参数调整策略

- **效果不足**：增加参数强度（如对比度从15提升到25）
- **效果过度**：降低参数强度（如暗角从80%降低到60%）
- **色彩偏差**：调整色相或更换色调填充色
- **暗部过黑**：
  - 优先去掉 `-brightness-contrast` 中的负亮度值（如 `-5x20` 改为 `0x20`）
  - 避免使用 `gamma < 1.0`（如 `gamma 0.9/0.95`），改用 `modulate` 或 `level` 控制影调
  - 降低暗角强度（`compose:args` 从 60 降到 30-40）
  - 如暗部实在看不清，可临时生成一张 `+modulate 150` 的版本辅助检查细节
- **局部问题**：考虑是否需要分区域处理

### 重要提醒

1. **质量优先**：所有中间JPG必须使用 `-quality 100`
2. **保留原始**：严禁覆盖或修改原始图片
3. **参数记录**：每步达标后**立即**写入参数文件，防止丢失
4. **始终从原始图开始**：每步处理都从原始文件出发，叠加之前所有已验证参数
5. **中间JPG仅用于验证**：绝不使用中间JPG作为下一步的输入
6. **最终生成**：从原始图一次性应用所有参数生成最终图像
7. **暗部保护（避免过黑）**：
   - **严禁用 `-brightness-contrast` 的负亮度值压暗**（如 `-5x20`、`-10x40`）。如需暗调，用 `modulate`（如 `95`）或后期 `level` 实现，避免线性偏移杀死暗部。
   - **慎用 `gamma < 1.0`**（如 `0.9`、`0.95`），gamma 压缩会吞掉暗部层次。
   - **暗角用 `blend` 替代 `multiply`**：`multiply` 会让整张图（不仅是四角）被渐变灰色压暗；改用 `-compose blend -define compose:args=强度`，建议强度 30-50。
