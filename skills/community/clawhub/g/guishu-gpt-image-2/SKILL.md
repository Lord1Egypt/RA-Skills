---
name: guishu-gpt-image-2
description: 使用贵数 Token 的 Images API 生成图片、参考图编辑、蒙版局部修改、批量素材和恢复已有图片下载。适用于用户明确选择贵数图片服务、guishu-gpt-image-2 或 OpenClaw 贵数生图工作流；不用于图片理解，也不替代用户指定的其他供应商。
---

# 贵数图片生成与编辑

使用包内 `scripts/generate.py`，Python 3.10+，只依赖标准库。`{baseDir}` 是 Agent 提供的 Skill 目录，不是给用户直接粘贴的终端路径；普通终端和 Windows 命令见 [接口与使用说明](references/gpt-image-2-api.md)。

默认模型保留 `gpt-image-2`，不会擅自切换用户模型。`--model` 可显式选择 `gpt-image-2.5-flare`、`gpt-image-2.5-sunburst` 或账户可用的其他 Images API 模型；不能把本地参数检查通过说成该账户已开通模型。

## 先选择操作

- **新图**：没有参考图时使用文生图。
- **改图/参考图**：先查看用户提供的图，使用 `--image`，不要仅把原图描述成文字再生成。多图分别说明用途，如“图一是产品，图二仅参考配色”。
- **局部修改**：使用 `--image` 加 `--mask`。蒙版透明区域表示修改区，作用于第一张图；主图和蒙版需同尺寸 PNG，蒙版需 Alpha 通道，各不超过 50 MiB。无蒙版可用自然语言编辑，但不能承诺像素级保留。
- **已经生成但取图失败**：用 `--resume` 取现有结果，绝不重新提交生图。没有保存响应时不能靠本 Skill 找回上游图片。

把用户要求整理为主体、用途、构图、文字、风格和必须保留的内容。非关键细节合理补全，不固定追问一套问卷。商品编辑须保留产品形状、数量、颜色和已有标识；不要凭空加价格、认证、性能或促销信息。需要精确中文文字时单独列出原文，生成后检查错字、漏字和布局。

## 凭据与数据

正式生成会将提示词、参考图/蒙版和 API Key 发往贵数接口，并可能收费。只发送本任务指定的素材，不搜集工作目录中的其他图片。

默认依次读取 `LLM_TOKEN_API_KEY`、`GUI_SHU_TOKEN_KEY`。**不再自动读取 `OPENAI_API_KEY`**。确实把贵数 Key 放在其他变量时，用 `--key-env VARIABLE_NAME` 明确选择；缺少 Key 时请用户在自己的环境中设置，不要求把 Key 粘贴到对话。

自定义 HTTPS endpoint 需显式选择凭据变量；不要把已有贵数 Key 自动发给陌生服务。生成 POST 不跟随重定向，不自动重试。旧 `--api-key` 保留兼容，但不要把真实 Key 放在命令行、日志或答案里。

默认不保存提示词/修订提示词，不将提示词拼进文件名；`--save-prompts` 才启用这些记录。恢复文件包含图片数据或临时签名 URL，仍是敏感产物，不可上传到公共仓库。macOS/Linux 创建的结果文件为仅当前用户可读写；Windows 请使用私人目录，不能将此说明理解为已设置 Windows ACL。

## 常用调用

```bash
# 免费的本地参数检查：无网络、无文件写入，也不读取 Key。
python3 "{baseDir}/scripts/generate.py" --prompt "蓝色音箱产品海报，简洁背景" --dry-run

# 文生图，结果目录必须为空。
python3 "{baseDir}/scripts/generate.py" \
  --prompt "蓝色音箱产品海报，简洁背景，柔和棚拍光，不添加虚构商标或价格" \
  --size 1024x1024 --quality high --n 1 --out-dir ./outputs/speaker

# 参考图编辑：每个 --image 指定一张本地图片。
python3 "{baseDir}/scripts/generate.py" \
  --image ./product.png \
  --prompt "只把背景换成暖灰色摄影棚，保留产品外形、颜色和商标，不增加文字" \
  --out-dir ./outputs/product-edit

# 蒙版编辑。
python3 "{baseDir}/scripts/generate.py" \
  --image ./product.png --mask ./mask.png \
  --prompt "将透明区域中的背景改成浅蓝色，保留产品" \
  --out-dir ./outputs/masked-edit

# 明确选择 Flare；auto 会按贵数现有路由省略 quality 参数。
python3 "{baseDir}/scripts/generate.py" \
  --model gpt-image-2.5-flare --quality auto \
  --prompt "极简咖啡店活动配图，无文字" --out-dir ./outputs/coffee

# 批量：UTF-8 文件每行一条提示词；每条单次提交，遇到异常停止余下请求。
python3 "{baseDir}/scripts/generate.py" \
  --prompt-file ./prompts.txt --n 1 --out-dir ./outputs/batch --json

# 只恢复已有结果，不需要 API Key，也不提交未开始的批量任务。
python3 "{baseDir}/scripts/generate.py" --resume ./outputs/batch --json
```

## 等待、失败与交付

生成默认 socket 超时 1200 秒，图片下载默认 120 秒，可分别调整。运行较慢时跟进**同一进程**，不要另开生图请求，也不要承诺固定 70–150 秒完成。

每次提交前记录 `submitting`；收到图片响应先存 `response-NNN.json`，每保存一张图更新 `state.json`。同次响应中的一张坏图不阻塞其他图片，失败原因记录在 `image_errors`。批量中途失败会保留已完成图片，余下提示词保持 `pending`。`--resume` 只重取已保存响应里的图片，并校验已有文件；不会执行 pending，也不会重发结果未知的请求。

- `generation_unknown` / `submitting`：请求可能已经受理。保留目录、时间和 request ID，先核对服务日志/用量；重新生成须得到用户确认。
- `download_failed`：先用 `--resume`。临时 URL 已过期、响应不完整或没有保存响应时，明确报告无法恢复，不能偷偷换成重生成。
- `partial`：返回数量与请求数量不同；交付已有图片并说明缺少/多出数量，不自动补单。
- HTTP 401/403/429：分别检查密钥、权限/服务限制、额度/限流；不自动换 Key、模型或服务地址。

退出码：`0` 全部完成或 dry-run 成功，`1` 部分完成/结果未知，`2` 参数或本地操作失败，`130` 用户中断。`--json` 的 stdout 是结果 JSON，进度写 stderr；先检查退出码和每项 status，不能仅凭存在输出目录宣布成功。

交付实际保存的图片和绝对路径；宿主支持时显示图片。查看产物，核对主体、指定文字、参考图保留要求、透明背景及尺寸是否符合用户要求。脚本的文件头检查不代替目视验收。`index.html` 是本地预览，`request.json` 是逐项状态摘要；不把它们当作网站发布或消息送达证明。
