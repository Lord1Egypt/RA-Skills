---
name: img2-generate-only
version: 3.0.0
description: 独立单图 IMG2 生图 Skill。必须显式提供接口地址和密钥，调用 OpenAI 兼容图片接口生成单张图片并本地落盘。
metadata:
  openclaw:
    emoji: "🖼️"
requires:
  bins:
    - python3
---

# IMG2 Generate Only Skill

## 定位

这是一个**纯单图生图 Skill**。

它只做一件事：

```text
prompt → 调用 IMG2 / gpt-image-2 → 本地落盘 → 返回结构化结果
```

它**不依赖任何历史本地配置**，也**不包含你们之前环境里的私有 provider 配置**。

使用时必须由用户或工作流**显式提供入参**。

它不负责：
- 飞书发送
- 云盘上传
- 批量并发
- 文章排版
- 公众号推送

---

## 执行脚本

```bash
python3 /home/ye/.openclaw/workspace/scripts/img2_generate_only.py
```

---

## 绝对必填参数

下面这些参数必须由用户显式提供：

### 1）`prompt`
最终图片提示词。

### 2）`base_url`
图片接口基础地址。

例如：

```text
https://your-api.example.com/v1
```

脚本会自动请求：

```text
{base_url}/images/generations
```

### 3）`api_key`
接口密钥。

例如：

```text
sk-xxxx
```

### 4）`model`
图片模型名称。

当前标准推荐：

```text
gpt-image-2
```

### 5）`size`
图片尺寸。

例如：

```text
1024x1024
```

### 6）`task_name`
任务名，用于输出文件命名。

### 7）`timeout_ms`
单张图最长等待时间，单位毫秒。

推荐：

```text
300000
```

---

## 可选参数

### 8）`output_dir`
图片输出目录。

默认：

```text
/tmp/generated-images
```

### 9）`response_format`
返回格式。

默认推荐：

```text
b64_json
```

### 10）`n`
生成数量。

当前这个 Skill 只支持单图，必须为：

```text
1
```

### 11）`return_base64`
是否在结果中返回 base64。

默认：

```text
false
```

一般不建议开启，返回 `image_path` 更稳。

---

## 标准输入 JSON

```json
{
  "prompt": "一只毛茸茸的橘猫坐在窗边，真实摄影风格，阳光柔和，无文字，无水印",
  "base_url": "https://your-api.example.com/v1",
  "api_key": "sk-xxxx",
  "model": "gpt-image-2",
  "size": "1024x1024",
  "task_name": "orange-cat-window",
  "timeout_ms": 300000,
  "output_dir": "/tmp/generated-images",
  "response_format": "b64_json",
  "n": 1,
  "return_base64": false
}
```

---

## 命令行调用示例

### JSON 方式

```bash
python3 /home/ye/.openclaw/workspace/scripts/img2_generate_only.py '{
  "prompt": "一只毛茸茸的橘猫坐在窗边，真实摄影风格，阳光柔和，无文字，无水印",
  "base_url": "https://your-api.example.com/v1",
  "api_key": "sk-xxxx",
  "model": "gpt-image-2",
  "size": "1024x1024",
  "task_name": "orange-cat-window",
  "timeout_ms": 300000,
  "output_dir": "/tmp/generated-images",
  "response_format": "b64_json",
  "n": 1,
  "return_base64": false
}'
```

### CLI 参数方式

```bash
python3 /home/ye/.openclaw/workspace/scripts/img2_generate_only.py \
  --prompt "一只毛茸茸的橘猫坐在窗边，真实摄影风格，阳光柔和，无文字，无水印" \
  --base_url "https://your-api.example.com/v1" \
  --api_key "sk-xxxx" \
  --model gpt-image-2 \
  --size 1024x1024 \
  --task_name orange-cat-window \
  --timeout_ms 300000 \
  --output_dir /tmp/generated-images
```

---

## 成功输出

```json
{
  "ok": true,
  "stage": "done",
  "image_path": "/tmp/generated-images/orange-cat-window-20260508-094000.png",
  "bytes": 1544093,
  "base_url": "https://your-api.example.com/v1",
  "model": "gpt-image-2",
  "size": "1024x1024"
}
```

如果 `return_base64=true`，还会额外返回：

```json
{
  "b64": "..."
}
```

---

## 失败输出

失败时返回结构化 JSON：

```json
{
  "ok": false,
  "stage": "request",
  "http_status": 502,
  "upstream_error_type": "upstream_error",
  "upstream_error_message": "Upstream request failed",
  "error": "脱敏后的错误信息",
  "diagnosis": {
    "category": "upstream_failure",
    "human_reason": "图片模型上游服务失败或临时不可用；不是本地脚本问题。",
    "retryable": true
  }
}
```

---

## 失败诊断字段

工作流建议读取：

- `ok`
- `stage`
- `http_status`
- `upstream_error_type`
- `upstream_error_message`
- `diagnosis.category`
- `diagnosis.human_reason`
- `diagnosis.retryable`

---

## 这个 Skill 的边界

这个 Skill 只负责**单张图生成**。

如果用户需要：
- 多张图批量生成
- 受控并发
- 队列监控
- state.json / batch_result.json

那应该使用单独的批量调度器，而不是把这些逻辑塞进这个单图 Skill 里。

---

## 一句话定义

**这是一个纯独立单图 IMG2 生图节点：用户必须显式提供 `prompt + base_url + api_key + model + size + task_name + timeout_ms`，脚本返回本地图片路径和结构化状态。**
