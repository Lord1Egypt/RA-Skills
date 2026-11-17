# iOS 快捷指令生成器

说一句「我想要个能……的快捷指令」，产出一个能直接导入 iPhone 的 `.shortcut` 文件。
不用 Mac、不用 Xcode、不用 iCloud。

```bash
./bin/sc setup                            # 装依赖，体检
./bin/sc init --cn "我的快捷指令CA"        # 建本机 CA（一次）
./bin/sc build 配方.json                  # → out/X-signed.shortcut
```

最后那个文件发到手机上，点开就弹「导入到快捷指令」。

---

## 为什么需要它

iOS 15 之后，**未签名的快捷指令会被直接拒绝导入**，提示「无法验证」。
苹果官方的签名通道只有一条：macOS + 快捷指令 App + iCloud。

这个技能用自建 CA 在 Linux 上完成同一件事：生成 → 自签 → 交付。
代价是手机要装一次这个 CA 的根证书。这是 iOS 的机制，任何第三方工具都绕不过。

---

## 平台支持

| 平台 | 生成配方 | 签名（出可导入文件） |
|---|---|---|
| Linux x86-64（glibc） | ✅ | ✅ |
| Linux arm64 | ✅ | ❌ 签名器无 ARM 版 |
| macOS | ✅ | ❌ 签名器是 Linux ELF |
| Windows | ✅（WSL2 的 Linux 侧） | 同 Linux x86-64 |
| Alpine / musl | ✅ | ❌ 缺 glibc |

签名器 `bin/shortcut-sign` 是预编译的 Linux x86-64 二进制，换平台就跑不动。
`sc doctor` 会提前说清楚，不会等你签完才发现。

**只想验配方、人在别的平台**：加 `--no-sign`，产物未签名，本机验证结构够用，
但手机不会接受导入。

---

## 上手

### 1. 建证书

三个入口，看手里有什么：

```bash
./bin/sc adopt "https://www.icloud.com/shortcuts/xxxx"   # 有分享链接，自动取名字
./bin/sc adopt 某个.shortcut                              # 有文件
./bin/sc init --cn "我的快捷指令CA"                        # 都没有，自己起名
```

`adopt` 会先把样本里的证书链解出来，和本机证书**逐字节比对**：

| 情况 | 结果 |
|---|---|
| 样本里的 CA 就是本机这套（字节一致） | 什么都不用做，手机早就信任了 |
| 样本是另一套证书 | 提示二选一：继续用本机的，或 `--force` 按样本名字重建 |
| 未签名 / 苹果官方签名 | 按名字新建一套，手机装一次新证书 |

> **为什么不能直接拿样本里的证书签名**：`.shortcut` 里嵌的只有证书（公钥），
> **私钥永远不在文件里**。签名必须用私钥，所以只有本机存着配套私钥时才成立。

产物在 `certs/`：

```
ca.crt / ca.key              CA 证书与私钥
sign.crt / sign.key          签名证书与私钥
key.bin                      X9.63 裸私钥（97 字节）
auth.plist                   证书链，签名时用
ca.mobileconfig              发到手机上装的那个
```

**`certs/` 不能外传。** 私钥给了别人，别人就能以你的名义签发任何东西。

不想让私钥待在技能目录里（压缩分享技能包时容易连 `ca.key` 一起发出去）：
`SC_CERT_DIR=~/.shortcut-ca ./bin/sc init`，之后每条命令都带同一个变量。

### 2. 写配方

```json
{
  "name": "PillReminder",
  "color": "Orange",
  "steps": [
    { "do": "notify", "WFNotificationActionTitle": "该吃药了",
      "WFNotificationActionBody": "早饭后一片" },
    { "do": "note.append", "entity": "健康记录", "text": "服药打卡 {now}" }
  ]
}
```

`name` 只能 ASCII。`color` 可选 Red / Orange / Yellow / Green / Teal / Blue / Violet / Purple / Pink / Gray。

可用的东西：

- **26 个动作**：`./bin/sc catalog` 全列出来，含每个参数的含义
- **7 个变量**：`{clipboard}` `{now}` `{input}` `{prev}` `{battery}` `{location}` `{repeat_item}`
- **控制流**：`if` / `repeat` / `repeat_each` / `menu`
- **条件**：12 种，中英文写法都行

参数键写错会当场报错并列出合法键，不会等你导进手机才发现动作是空的。

### 3. 生成

```bash
./bin/sc build 配方.json -o out/名字.shortcut
```

出两个文件：`out/名字.shortcut`（未签名）和 `out/名字-signed.shortcut`（发这个）。
生成时做三道校验：动作数 > 0、控制流开闭配对、签名前后动作数一致。

### 4. 装到手机

第一次要装根证书，之后不用再装：

1. 把 `certs/ca.mobileconfig` 发到 iPhone，**用 Safari 打开**
2. 设置 → 通用 → VPN与设备管理 → 安装
3. 设置 → 通用 → 关于本机 → **证书信任设置** → 对这个 CA 开「完全信任」

⚠ 第 3 步不做，导入时照样报「无法验证」。

然后把 `-signed.shortcut` 发过去，在「文件」App 里点开 → 分享 → 快捷指令。

### 5. 让它自己跑

生成的是「做什么」，「什么时候做」要在手机上设：

快捷指令 App → 底部「自动化」→ 右上「+」→ 特定时间（或到达某地 / 连上某个 Wi-Fi）
→ 选刚导入的快捷指令 → **关掉「运行前询问」** → 完成。

「运行前询问」不关，每次都会弹确认，等于没自动化。

---

## 命令

| 命令 | 作用 |
|---|---|
| `sc setup` | 检查并安装依赖 |
| `sc doctor` | 环境 + 证书体检 |
| `sc init [--cn 名字]` | 生成本机 CA 与签名证书 |
| `sc adopt 链接或文件 [--dry-run] [--force] [--cn 名字]` | 从已有快捷指令取 CA 名并建证书 |
| `sc catalog [--group 组] [--grep 词] [--json]` | 列可用动作 |
| `sc build 配方.json [-o 路径] [--no-sign] [--json]` | 配方 → .shortcut |
| `sc verify X.shortcut` | 校验已签名文件 |

---

## 它不做什么

- **不负责定时**。产出的快捷指令要自己放进「自动化」里设触发条件。
- **不负责远程下发**。想让服务器给手机派任务（入队 → 唤醒 → 拉取 → 回执），
  那是自动化编排的事，本技能到此为止。
- **不是官方签名**。自签依赖 iOS 对用户根证书的信任，苹果大版本升级有可能收紧。
- **不碰你的数据**。除了 `adopt` 去 iCloud 拉取你给的那条分享链接，全程不联网。

---

## 常见问题

**证书能不能大家共用一套？**
不能。手机装根证书是「无条件信任」级别，共用等于把签发权交出去。每人自己生成。

**手机能不能不装证书？**
不能。这是 iOS 的导入校验，任何第三方工具都绕不过，苹果自己也得走签名。

**换了台电脑要重来吗？**
要重新生成证书，手机也得重装——新机器上的私钥是新的。想避免就备份 `certs/`。

**导入后名字变问号？**
快捷指令名或文件名带了非 ASCII 字符。全改英文重新生成。

**怎么卸载？**
手机：设置 → 通用 → VPN与设备管理 → 删掉描述文件。电脑：删 `certs/` 目录。

---

## 许可

MIT，见 `LICENSE`。随包分发的第三方组件见 `THIRD-PARTY-NOTICES.md`。

自签用途请自行评估合规性：装根证书会扩大设备信任面，公司或他人设备不要装。
