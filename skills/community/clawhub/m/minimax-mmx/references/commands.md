# MMX-CLI 详细命令参考

## 完整帮助
```bash
mmx --help                    # 全局帮助
mmx <resource> --help         # 各模块帮助
```

## auth - 鉴权管理
```bash
mmx auth login [--method oauth|api-key] [--api-key <key>]
mmx auth status              # 查看当前鉴权状态和配额
mmx auth refresh             # 刷新 OAuth token
mmx auth logout              # 登出
```

## text - 文本对话
```bash
mmx text chat --prompt <text> [--model <model>] [--stream]
```

## speech - 语音合成
```bash
mmx speech synthesize --text <text> --voice <voice-id> --out <file>
mmx speech voices            # 列出可用声音
```

常用声音：
- `中文主播` - 标准中文女声
- `中文客服` - 中文客服风格
- `英文主播` - 标准英文女声

## image - 图片生成
```bash
mmx image generate \
  --prompt <text> \
  [--aspect-ratio 1:1|16:9|9:16|3:4|4:3] \
  [--n <count>] \
  [--subject-ref type=character,image=<path>] \
  [--out-dir <dir>] \
  [--out-prefix <prefix>]
```

示例：
```bash
# 单张图片
mmx image generate --prompt "未来城市天际线" --out-dir ./images --quiet

# 多张图片
mmx image generate --prompt "产品展示图" --n 4 --out-dir ./products --quiet

# 角色一致性
mmx image generate --prompt "穿西装的男人" --subject-ref type=character,image=ref.png --quiet
```

## video - 视频生成
```bash
# 生成视频
mmx video generate \
  --prompt <text> \
  [--model MiniMax-Hailuo-2.3-Fast-6s-768p|MiniMax-Hailuo-2.3-6s-768p] \
  [--duration 6] \
  [--out <file>] \
  [--async]

# 查询异步任务
mmx video task get <task-id>

# 下载视频
mmx video download <task-id> [--out <file>]
```

## music - 音乐生成
```bash
mmx music generate \
  --prompt <text> \
  [--lyrics <text>] \
  [--instrumental] \
  [--out <file>]
```

## vision - 图片理解
```bash
mmx vision describe \
  --image <path|url> \
  [--detail low|high]
```

## search - 网络搜索
```bash
mmx search query \
  --query <text> \
  [--limit <count>]
```

## quota - 配额查询
```bash
mmx quota show
```

输出示例：
```
| MiniMax-M*          102 / 4,500  [................]   2% |
| speech-hd           0 / 19,000  [................]   0% |
| music-2.5           1 / 7        [██..............]  14% |
| image-01            0 / 200      [................]   0% |
```

## config - 配置管理
```bash
mmx config show                    # 显示当前配置
mmx config set <key> <value>      # 设置配置项
mmx config export-schema           # 导出配置 schema
```

## update - 更新
```bash
mmx update                         # 检查并更新到新版本
```
