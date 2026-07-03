# 围棋下一手推荐飞书图片机器人

## 围棋高参（飞书机器人）

你可以直接使用围棋高参飞书机器人，无需本地部署：

https://applink.feishu.cn/T97DbgVIGt1W

![围棋高参二维码](./weiqi-gaocan-qr.png)

## 使用流程

这是 Go Next Move skill 的可选飞书入口，不会替换或修改原有 CLI skill。

机器人使用飞书长连接模式：运行 KataGo 的机器主动连出到飞书，不需要公网 webhook 服务或公网隧道。推荐日常优先使用这种部署方式，发图和收结果都在飞书里完成，链路更短、响应更快。


1. 先发送一次设置消息，例如：

```text
设置 黑 中级
```

2. 之后直接发送棋盘照片。机器人会下载图片，调用现有的 `scripts/next_move.py --input image`，再回复推荐落点和结果图。

设置按会话保存在本地 JSON 文件中。私聊和不同群聊可以使用不同设置。只发送部分设置时会保留其他旧值；例如 `设置 白` 只会修改轮到白棋下。

## 命令

```text
设置 黑 中级
设置 白 高级
设置 白
设置 高级
设置 black beginner
当前设置
上报
帮助
```

支持的行棋方：

- `黑`, `黑棋`, `black`, `b`
- `白`, `白棋`, `white`, `w`

支持的推荐强度：

- `初级`, `beginner`
- `中级`, `intermediate`
- `高级`, `advanced`
- `特级`, `expert`

如果最近一次识别图或结果图有问题，发送 `上报`、`报错`、`识别错` 或 `反馈`。配置了 `FEISHU_FEEDBACK_DIR` 后，机器人会把当前会话最近一次成功分析的数据保存到该目录下，包含 `input.jpg`、`output.jpg` 和 `metadata.json`。

## 部署

安装依赖：

```bash
python3 -m pip install -r scripts/requirements.txt
python3 -m pip install -r integrations/feishu/requirements.txt
```

创建一个飞书应用，并启用机器人长连接模式。

需要开通的飞书权限：

- `im:message.p2p_msg:readonly`：接收发给机器人的私聊消息。
- `im:message.group_at_msg:readonly`：接收群聊中 @ 机器人的消息。
- `im:message.group_at_msg.include_bot:readonly`：接收包含机器人消息的群聊 @ 消息。
- `im:message`：读取消息事件所需的消息元数据和内容。
- `im:message:send_as_bot`：以机器人身份发送回复。
- `im:resource`：下载收到的图片，并上传输出的标注结果图。

修改权限或事件订阅后，需要发布新的应用版本，并在租户内升级或安装该版本；只改开发配置不会立即生效。

可以在飞书控制台导入下面的权限 JSON：

```json
{
  "scopes": {
    "tenant": [
      "im:message",
      "im:message.group_at_msg.include_bot:readonly",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": [
      "im:resource"
    ]
  }
}
```

需要订阅的事件：

- `im.message.receive_v1`：接收用户发来的消息。

运行：

```bash
cat > .env.feishu <<'EOF'
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
KATAGO_PATH=/path/to/katago
KATAGO_MODEL=/path/to/model.bin.gz
KATAGO_ANALYSIS_CONFIG=/path/to/analysis_example.cfg
KATAGO_SKILL_CONFIG=katago/analysis_skill.cfg
FEISHU_FEEDBACK_DIR=/path/to/local/feedback-data
EOF

python3 integrations/feishu/feishu_image_bot.py
```

### macOS launchd 性能设置

如果用 `launchd` 常驻运行飞书机器人，不要把 plist 的 `ProcessType`
设为 `Background`。macOS 会降低后台任务的 CPU/QoS，OpenCV 的棋盘候选
grid fitting 会明显变慢；实测同一张 1080x1920 棋盘图的识别时间可能从约
1 秒放大到约 6 秒。

建议使用 `Interactive`，或直接省略 `ProcessType`：

```xml
<key>ProcessType</key>
<string>Interactive</string>
```

重启后可以检查：

```bash
launchctl print gui/$(id -u)/com.wanghongbao.go-next-move.feishu-bot
```

输出里应看到 `spawn type = interactive`，而不是 `background`。

常用选项：

```bash
python3 integrations/feishu/feishu_image_bot.py \
  --visits 300 \
  --level intermediate \
  --side-to-move black \
  --feedback-dir /path/to/local/feedback-data \
  --settings-path ~/.go-next-move/feishu-settings.json
```

KataGo 相关参数会转发给 `scripts/next_move.py`：

```bash
--katago /path/to/katago
--model /path/to/model.bin.gz
--analysis-config /path/to/analysis.cfg
--skill-config katago/analysis_skill.cfg
```

`--katago` 默认依次读取 `KATAGO_PATH`、`KATAGO`，最后使用 `PATH` 中的 `katago`。`--model`、`--analysis-config` 和 `--skill-config` 分别默认读取 `KATAGO_MODEL`、`KATAGO_ANALYSIS_CONFIG` 和 `KATAGO_SKILL_CONFIG`。

`--feedback-dir` 默认读取 `FEISHU_FEEDBACK_DIR`；不配置时会关闭显式错误样本上报。

如果机器人能收到图片消息，但分析时报 `FileNotFoundError: ... 'katago'`，说明飞书长连接和消息收发已经正常，只是服务进程找不到 KataGo 可执行文件。请用绝对路径启动，或在启动前把 `KATAGO_PATH=/path/to/katago` 写入 `.env.feishu`。

## 注意事项

- 机器人使用现有 OpenCV 图片识别链路，不经过 LLM。
- 如果棋盘识别不准，请发送更清晰的照片。该集成保持原有“一张照片分析一步”的行为，暂不支持提子状态修正或多手 overlay。
- 群聊通常需要 @ 机器人，具体取决于飞书应用的事件和权限设置。机器人自身没有强制要求 @，因为图片消息通常不方便同时携带文本。
- 如果本地日志只有 WebSocket `ping`/`pong`，而飞书事件日志为空，请优先检查私聊权限 `im:message.p2p_msg:readonly` 和群聊 @ 权限 `im:message.group_at_msg:readonly`。这种现象通常表示飞书没有权限为应用生成消息事件，而不是 Python 进程异常。
