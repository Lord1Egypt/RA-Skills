---
name: ohyesai-music
description: Generate custom music tracks (vocal or instrumental) via OhYesAI asynchronously.
homepage: https://dev.ohyesai.com
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["curl", "grep", "sleep"],"env":["OHEYSAI_API_KEY"]}}}
---

# Music Skill

通过调用 OhYesAI API，直接在 Clawdbot 中生成自定义风格的歌曲（支持纯音乐或带人声）。
*注意：音乐生成耗时较长，本技能采用“提交任务 -> 轮询查询状态 -> 下载文件”的异步工作流。*


## Setup

1. 首次安装/使用时，请前往获取 API Key: [https://ohyesai.com](https://ohyesai.com?from=https://clawhub.ai)
2. 设置你的环境变量:
   ```bash
   export OHEYSAI_API_KEY="your-api-key"
   ```

## Usage

使用此技能生成音乐时，必须与用户进行多轮对话以收集必要参数。完成生成、下载后，必须**将真实音频文件交付给用户**。

### 参数说明
在调用 API 前，请确认以下参数：
- `prompt` (必填)：用户提示词/歌曲的画面与情感描述，需与用户沟通获取。
- `styles` (必填)：歌曲风格（如“流行”、“动漫”、“摇滚”等），需与用户沟通获取。
- `instrumental` (必填)：布尔值。`true` 代表纯音乐（无歌词/无人声），`false` 代表有歌词的音乐，需与用户沟通获取。
- `title`：歌曲标题。**无需向用户询问**，请根据其他参数自动推理生成一个合适的歌名。

### 1. 提交任务 (Submit Task)
收集完参数后，使用 `curl` 调用 submit 接口提交任务：
```bash
curl -s --location --request POST "https://ohyesai.com/ohyesai-next/api/vio/skill/music-submit?apikey=$OHEYSAI_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "晚安",
    "prompt": "晚安风格的宁静歌曲",
    "styles": "动漫",
    "instrumental": true
}'
```
**返回值**：该接口会返回一个 `taskId`（任务ID），请务必将其提取并保存，用于后续查询。

### 2. 查询任务状态 (Query Status)
使用获取到的 `taskId` 通过 GET 请求不断轮询查询任务状态：
```bash
curl -s --location --request GET "https://ohyesai.com/ohyesai-next/api/vio/skill/music-query?apikey=$OHEYSAI_API_KEY&taskId=你的taskId"
```
**接口返回值有以下 3 种状态**：
1. `**音乐生成状态**: 进行中` -> 任务还在排队或生成中，**你需要 sleep 一段时间（如 10 秒）后继续重试**。
2. `**音乐生成状态**: 已完成` -> 任务完成，状态文本后会附加包含 MP3 音频链接的 Markdown 文本。
3. `**任务不存在**` -> 任务生成失败或 ID 错误，应终止轮询并告知用户。

### 3. 下载与交付 (Download and Deliver)
当状态变为**已完成**时，返回值示例：
```md
**音乐生成状态**: 已完成
[晚安_1](https://ohyesainext-test.tos-cn-beijing.volces.com/mv%2F202603%2F66d82e777e2544a89a6c3aedc9f60c93.mp3?...)
[晚安_2](https://ohyesainext-test.tos-cn-beijing.volces.com/mv%2F202603%2F66d82e777e2544a89a6c3ae706362o75.mp3?...)
```

**必须严格执行以下交付操作**：
1. 从上述返回值中提取出 `.mp3` 文件的 URL。
2. 使用 `curl -o "文件名.mp3" "音频URL"` 命令将音频文件下载到当前工作目录。
3. **⚠️ 致命注意（推送文件）：** 下载完成后，**绝对不能仅仅回复纯文本！** 你必须输出可供用户点击的本地文件链接，例如 `[点击下载 晚安_1.mp3](./晚安_1.mp3)` 或者调用系统内置的发文件工具将本地 MP3 推送给用户。

## Examples

这里提供了一个标准的 Bash 自动化脚本，它整合了**提交、轮询、提取、下载**的全流程，你（大语言模型）可以直接修改参数并执行此脚本来完成整个任务：

```bash
# 1. 提交任务并获取 Task ID
TASK_ID=$(curl -s --location --request POST "https://ohyesai.com/ohyesai-next/api/vio/skill/music-submit?apikey=$OHEYSAI_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "安眠曲",
    "prompt": "安静助眠的轻音乐",
    "styles": "动漫",
    "instrumental": true
}')

# 简单清理可能存在的引号或换行符
TASK_ID=$(echo "$TASK_ID" | tr -d '"' | tr -d '\n' | tr -d '\r')
echo "Task Submitted! Task ID: $TASK_ID"
echo "开始轮询等待音乐生成..."

# 2. 轮询状态
while true; do
    RESULT=$(curl -s --location --request GET "https://ohyesai.com/ohyesai-next/api/vio/skill/music-query?apikey=$OHEYSAI_API_KEY&taskId=$TASK_ID")
    
    if echo "$RESULT" | grep -q "已完成"; then
        echo "音乐生成已完成！"
        # 3. 提取 MP3 URL（正则提取 http...mp3... 括号内的内容）
        MP3_URL=$(echo "$RESULT" | grep -o 'http[^)]*' | head -n 1)
        
        if [ -n "$MP3_URL" ]; then
            echo "正在下载音频..."
            curl -s -o "安眠曲_1.mp3" "$MP3_URL"
            echo "下载成功！文件已保存为 ./安眠曲_1.mp3"
        else
            echo "未能提取到有效的音频 URL"
        fi
        break
    elif echo "$RESULT" | grep -q "任务不存在"; then
        echo "查询失败：任务不存在或已失效。"
        break
    else
        echo "生成中，等待 20 秒后重试..."
        sleep 20
    fi
done
```

### 完整工作流说明
1. 询问用户获取 `prompt`, `styles`, `instrumental`。
2. 自动生成 `title`，代入上述示例脚本并执行。
3. 脚本执行完毕并显示“下载成功”后，向用户回复：**"您的音乐已生成完毕，请点击此处收听/下载：[安眠曲_1.mp3](./安眠曲_1.mp3)"** (或者调用系统发文件的内置能力)。

### 联系客服
![联系客服](https://ohyesainext-public.tos-cn-beijing.volces.com/openclawCstomerServiceQr.jpeg)
![联系客服](https://ohyesainext-public.tos-cn-beijing.volces.com/customerServiceQrCode.jpeg)
