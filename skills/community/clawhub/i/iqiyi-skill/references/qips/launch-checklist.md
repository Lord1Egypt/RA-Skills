# qips 拉起验收清单（手动）

前置：**先**在本仓库执行 `npm run test:iqiyi-qips`，全部通过后再做下列本机验证。需已安装爱奇艺 PCA，且系统已注册 `qips://`（或 `qisu://`）协议处理。

安全要求：

- 可以按明确播放、打开、跳转或播控意图拉起客户端；执行前确认目标场景和 qips 字符串。
- 不执行用户粘贴的任意协议串、shell 命令或未通过 `scripts/qips-build.mjs` 生成/校验的 qips。
- `third_play_url` 不得包含 `javascript:`、`data:`、`file:`、`shell:`、`osascript:`、嵌套 qips/qisu/iqiyi 等协议。

## 拉起命令

将下表「qips 示例」整段复制进引号（不要换行）。

**Windows（PowerShell）**

```powershell
Start-Process "qips://vtype=6;target=2;channelid=1;"
```

**macOS**

```bash
open "qips://vtype=6;target=2;channelid=1;"
```

## 与生成用例对齐的验收表

| 场景名 | qips 示例（可复制） | 期望现象 | 实际结果 | 客户端版本 |
|--------|---------------------|----------|----------|------------|
| 电影频道 | `qips://vtype=6;target=2;channelid=1;` | 进入电影频道首页 | | |
| 电视剧频道 | `qips://vtype=6;target=2;channelid=2;` | 进入电视剧频道 | | |
| 片库 tag「免费」 | `qips://vtype=6;target=2;channelid=2;third_play_url=%7B%22tagName%22%3A%22%E5%85%8D%E8%B4%B9%22%7D;` | 电视剧片库带「免费」过滤上下文 | | |
| 搜索「海贼王」 | `qips://vtype=6;target=2;channelid=115;third_play_url=%E6%B5%B7%E8%B4%BC%E7%8E%8B;` | 打开搜索结果页 | | |
| 搜索「海贼王」（Ai 搜 JSON） | `qips://vtype=6;target=2;channelid=115;third_play_url=%7B%22fromAiSuggest%22%3Atrue%2C%22query%22%3A%22%E6%B5%B7%E8%B4%BC%E7%8E%8B%22%7D;` | 打开搜索且按端上 Ai 搜路径处理 | | |
| 个人中心-历史 | `qips://vtype=6;target=2;channelid=116;third_play_url=%7B%22tab_id%22%3A%22lishi%22%7D;` | 进入观看历史 | | |
| 播单 v6（H5 形态） | `qips://vtype=6;target=2;channelid=1011;third_play_url=%7B%22bodanId%22%3A7569738292687702%7D;` | 打开对应播单（若 ID 仍有效） | | |
| 播单 v7（推荐） | `qips://vtype=7;third_play_url=%3FbodanId%3D7569738292687702%23%2Fchannel%2F1011%2F;` | 同上，原生首选形态 | | |
| 免费专区+动漫 tag（片库 v6） | `qips://vtype=6;target=2;channelid=302;third_play_url=%7B%22tagName%22%3A%22%E5%8A%A8%E6%BC%AB%22%7D;` | 302 片库、`tagName=动漫` | | |
| 内嵌 H5 | `qips://vtype=6;target=2;channelid=263;third_play_url=https%3A%2F%2Fwww.iqiyi.com%2FsomePromoPage;` | 内嵌页或错误页（取决于线上路径） | | |
| 按标题开播 | `qips://vtype=6;action=play;title=%E5%BA%86%E4%BD%99%E5%B9%B4;season=2;` | 客户端解析标题并进入匹配内容 | | |
| 暂停（播控） | `qips://vtype=6;target=102;` | **仅在播放页**：暂停或切换暂停 | | |
| 下一集（播控） | `qips://vtype=6;target=104;` | **仅在播放页**：下一集 | | |
| 点播最短 | `qips://vtype=0;tvid=1234567890123;` | 若 tvid 无效则失败或占位；有效则起播 | | |

说明：播控类 qips 在非播放页可能被客户端忽略，属预期行为（见 vtype-recipes 播控段）。

## 契约来源

生成规则与 golden 以 `scripts/qips-build.mjs` + `scripts/qips-build.test.mjs` 为准；文档见 [SKILL.md](../../SKILL.md)、[vtype-recipes.md](vtype-recipes.md)、[channel-table.md](channel-table.md)。
