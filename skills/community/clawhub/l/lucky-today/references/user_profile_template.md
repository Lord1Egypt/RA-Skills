# User Profile Template

仅为字段模板。**不保存任何真实个人信息**,所有值都是占位。

第一次用户明确说"记住我的生日 / 帮我建档 / 保存档案"时,可写入 `{baseDir}/user_profile.json`(见底部 JSON 结构)。

## 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `profileVersion` | string | 模板版本,固定 `"1.0.0"` |
| `userId` | string | 用户标识(渠道侧 chat_id / handle / 用户输入的代号) |
| `name` | string | 显示用名字,可以是昵称,可空 |
| `gender` | enum | `"male" / "female" / "other" / null` — 仅影响话题建议侧重,可空 |
| `birth.date` | string | `YYYY-MM-DD`,必填 |
| `birth.time` | string | `HH:mm` 或 `null` — 没有就不写,不要默认 12:00 |
| `birth.place` | string | 城市级地名或 `null` |
| `birth.lunar` | string | 农历 `YYYY-MM-DD` 或 `null`,可选 |
| `language` | enum | `"zh" / "en"` — 默认推送语言,可空 |
| `chartRaw` | string | 用户粘贴的命盘文本原文,可空(无星盘也能用) |
| `preferences.pushChannel` | string | `"telegram" / "feishu" / "slack" / "discord"` 或 `null` |
| `preferences.pushTo` | string | 渠道 ID(chat_id / channel_id 等)。**敏感字段,不要在普通会话回显。** |
| `preferences.morningTime` | string | `HH:mm`,默认 `"07:00"` |
| `preferences.eveningTime` | string | `HH:mm`,默认 `"21:00"` |
| `preferences.focus` | array | 用户关心的话题,如 `["事业", "财运"]` 或英文 |
| `partner.name` | string | 双人合盘对方名字,可空 |
| `partner.birthDate` | string | 对方生日,可空 |
| `createdAt` | string | ISO 时间 |
| `updatedAt` | string | ISO 时间 |

## JSON 结构(占位)

```json
{
  "profileVersion": "1.0.0",
  "userId": "<待填写>",
  "name": "<待填写或空>",
  "gender": null,
  "birth": {
    "date": "<YYYY-MM-DD,必填>",
    "time": null,
    "place": null,
    "lunar": null
  },
  "language": "zh",
  "chartRaw": null,
  "preferences": {
    "pushChannel": null,
    "pushTo": null,
    "morningTime": "07:00",
    "eveningTime": "21:00",
    "focus": []
  },
  "partner": {
    "name": null,
    "birthDate": null
  },
  "createdAt": "<YYYY-MM-DDTHH:mm:ss+08:00>",
  "updatedAt": "<YYYY-MM-DDTHH:mm:ss+08:00>"
}
```

## 写入规则

1. **必须明确同意才写**:用户说"记住""保存""帮我建档""下次别再问"等触发后才写入。其他情况只在内存里用。
2. **写入位置**:`{baseDir}/user_profile.json`(skill 根目录)。不要写到 `{baseDir}/data/` 或 `~/.openclaw/` 其他位置。
3. **写入前**:先 `read` 是否已存在;若存在,**先告知用户"已检测到现有档案,是否覆盖?"**,得到确认才覆盖。
4. **失败回退**:写不进去(环境只读)就告知"当前环境无法持久化档案,本会话临时使用"。
5. **更新**:任何字段变化都更新 `updatedAt`。
6. **删除**:用户说"删除档案""清除档案""不要记我"立刻删除 `user_profile.json`,并确认已删除。
7. **导出**:用户说"导出档案",直接 echo JSON 内容(可粘贴备份用)。

## 隐私约束

- **绝不**将 `pushTo`(渠道 ID)在普通输出里显示给用户(那是 chat_id / channel_id,不应该出现在运势文本里)
- **绝不**在向第三方渠道推送时附上 JSON 内容
- **绝不**把 `partner.birthDate` 反复回显给用户(对方生日是次密敏感)
- 用户档案文件被 `.clawhubignore` 和 `.gitignore` 排除,不会被打包/提交

## 与 yunshi 的区别

`yunshi` 使用 `data/profiles/<userId>.json`(支持完整八字 / 紫微 / 家庭成员 / 多用户)。

`lucky-today` 使用 `user_profile.json`(单文件,字段极简,仅服务"今日运势"场景)。

如用户同时安装两个 skill,**不要尝试同步两边的档案**,各自独立。
