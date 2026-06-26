# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## GENERAL (通用文字)
- `width`: 图像宽度（像素）
- `height`: 图像高度（像素）
- `angle`: 图像旋转角度（度）
- `text`: 文字识别结果（List<Object>）
  - `text`: 文字条内容
  - `text_class`: 文本类别标识，1是竖向文本，2是横向文本
  - `anglenet_class`: 角度分类标识
  - `x`: 文本块左上角X坐标
  - `y`: 文本块左上角Y坐标
  - `width`: 文本块宽度（像素）
  - `height`: 文本块高度（像素）
  - `pos`: 文本块四边形坐标（左上、右上、右下、左下），List<Array>
  - `confidences`: 文字条置信度
  - `chars`: 字符识别结果（List<Object>）
    - `pos`: 字符四点坐标，List<Array>
    - `text`: 识别的字符
