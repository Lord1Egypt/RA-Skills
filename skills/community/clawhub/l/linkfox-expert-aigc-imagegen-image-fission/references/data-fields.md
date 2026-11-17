# 图片裂变 - 数据字段汇总

## 步骤 1：参数校验与模型确认

| 方向 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 输入 | images | list[image] | 用户上传的图片列表 |
| 输入 | model | string | 用户选择的模型标识 |
| 输入 | quality | string | 图片质量参数（仅 GPT_2_IMAGE） |
| 输出 | model | string | 透传的模型标识（不校验枚举，默认 GPT_2_IMAGE） |
| 输出 | quality | string | 透传的质量参数（仅 GPT_2_IMAGE） |

## 步骤 2：图片预处理与队列生成

| 方向 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 输入 | images | list[image] | 原始图片列表 |
| 输出 | processing_queue | list[image] | 待裂变的图片队列 |

## 步骤 3：组装 Prompt

| 方向 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 输入 | similarity_threshold | int | 相似度上限百分比 |
| 输入 | user_prompt | string | 用户附加提示词 |
| 输出 | final_prompt | string | 拼接后的完整 prompt |

## 步骤 4：逐张裂变生图

| 方向 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 输入 | processing_queue | list[object] | 来自 S2 |
| 输入 | final_prompt | string | 来自 S3 |
| 输入 | model | string | 来自 S1（透传） |
| 输入 | quality | string | 来自 S1（透传） |
| 输入 | fission_count | int | 每张图裂变数量 |
| 输出 | fission_results | list[object] | 每项含 original_image、fission_images[] |

## 步骤 5：产出整理与落盘

| 方向 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 输入 | fission_results | list[object] | 来自 S4 |
| 输出 | media_files | list[path] | 落盘后的图片路径列表 |
| 输出 | mapping | list[object] | 原图→裂变图文件名映射 |
