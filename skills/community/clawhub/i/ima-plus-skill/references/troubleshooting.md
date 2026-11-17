# Troubleshooting — 实测沉淀的错误码对照与避坑指南

> **按需读取**：仅在 API 调用出错（`code≠0`、`-100`、`-200`、异常现象）时查阅本节对照定位。
> 标注 `code=xxx` 为后端业务错误（stdout JSON 的 `code` 字段）；`退出码` 为脚本进程退出码。

## 一、知识库接口坑对照

| 接口 / 场景 | 试错现象 | 正确做法 |
| --- | --- | --- |
| `create_folder` | 手敲 `folder_name` → `code=51` 参数非法 | 字段名是 **`name`**（`--name` / 请求体 `name`） |
| `search_knowledge_base_in_square`（广场发现） | 误用 `query` → `code=51` | 参数是 **`question`**（且必填非空），脚本用 `--question` |
| `set_knowledge_top`（置顶） | ① 对单个**文件**置顶 → `code=220001 invalid media_id`；② `--media-id` 空时脚本误判成布尔 → `code=1 cannot unmarshal bool` | ① **仅支持文件夹**（`folder_...`，media_type=99）；② `is_top` 是布尔；③ `--media-id` 必须传真实 id |
| `export_media` / `export_media_for_ima_sandbox` | `code=220030 无权限访问该接口` | **key 权限问题，非脚本缺陷**：导出接口需 API key 开通导出权限；个人在 agent-interface 申请的 key 默认未开通，需用 ima app 内 copilot 环境变量中的凭证（已开通）。凭证获取见主 SKILL.md「Credential Check」 |
| `update_knowledge_base_permission` | 有**真实副作用**（影响该库所有成员） | 正式库改权限前**必须向用户确认** |
| `join_knowledge` | 会**真实加入**公开库（副作用） | 调用前确认用户确实要加入；加入后需用户到 IMA 客户端退出 |
| `get_media_info` 读取原文 | 订阅库（普通成员）返回 `code=220030 没有权限` | 仅**个人库（创建者）**能读文件/笔记原文；订阅库只能看列表，引导用户去客户端 |
| `get_knowledge_list` 的 `folder_id` | 把 `knowledge_base_id` 当 `folder_id` 传入 → 返回根目录而非目标文件夹 | 根目录**省略** `folder_id`；子目录 ID 必须 `folder_xxxx` 开头；看到 `current_path` = 走对路径 |
| `media_type` 枚举 | 曾误以为 `media_type=11` 是微信文章（其实是**笔记**），`6` 才是微信文章 | 速记：`1=PDF` `2=网页URL` `4=PPT` `5=Excel` `6=微信文章` `11=笔记` `16=网页视频` `20=HTML` `21=EPUB` `99=文件夹`；拿不准先搜样例 |
| `search_*` 返回空 | `info_list:[]` 不一定是真没内容 | 换关键词 / 换接口（`get_knowledge_list` 翻文件夹）；别一次空就放弃 |
| `check_repeated_names` 重名判定 | 刚上传完短时间内查同名可能 `is_repeated=false`（索引延迟） | 别仅凭一次查询认定无重名 |
| `create_folder` 接口选择 | 早期误用 `add_knowledge`+`media_type=99` 建文件夹失败 | 正确接口是 `create_folder`（实测可成功，返回 `data.media_id` 即 `folder_id`） |
| 删除类操作 | 试图删除文件/文件夹/知识库/标签 | **IMA OpenAPI 不支持任何实体删除**，测试留痕需用户到 IMA 客户端手动清理 |
| `tag_delete` / `tag_rename` | 删除标签移除其与所有文件关联（**不可逆**）；`tag_rename` 新名已存在时自动合并两组标签 | 调用前确认 |
| 写操作角色 | 普通成员调建库/改名/置顶/标签/权限 → `code=220030` | 需角色为创建者/协作成员/管理员 |
| 批量导出 / 打包 | 订阅库不可下载；HTML(20) 个人库也 `220030`；大文件（如 103MB 无后缀音频）需按 media_type 补后缀；同名文件会覆盖 | 仅个人库（创建者）可导出；并发 ≤8，单文件失败跳过不中断；订阅库引导客户端。完整 SOP 见下文「六、批量导出打包 SOP」 |
| `search_knowledge_base` 返回结构 | 按 `knowledge_base_list`/`id`/`name` 解析永远匹配不到 | 返回字段是 `info_list` / `kb_id` / `kb_name`；空 `query` 返回账号**全部**知识库（含订阅） |
| 文件夹上传 | —— | 用 `--folder <folder_id>`，支持任意层级嵌套；文件夹的 `media_id` 即其 `folder_id`；`move_knowledge` 仅支持文件，**不支持移动文件夹** |
| 订阅库权限墙 | 订阅库 134 条内容但 `get_media_info` 返回 `220030 没有权限通过skill获取订阅知识库的文件` | 个人库（创建者）全权限；订阅库（普通成员）只能看列表/元信息，引导用户去客户端，别反复重试 |
| `kb_id` 是 Base64 URL 安全变体 | 含 `=`、`+`、`_`，shell 极易丢字符 | 写进变量 + 双引号包住（`"$KB_ID"`）；PowerShell 别用反引号包值（反引号是转义符）；传入前先 `echo` 核对一次 |
| 写/查重类接口（`check_repeated_names` 等） | `code=222001 知识库已删除` | 目标知识库已在客户端被删除（索引残留：`get_knowledge_base` / `get_knowledge_list` 仍可能查到，但写操作全部拒绝）。换用现存库或重建；路径缓存会自动失效重查（`222001`/`已删除` 已纳入自愈判定） |

## 二、笔记接口坑

| 场景 | 试错现象 | 正确做法 |
| --- | --- | --- |
| 写入 UTF-8 编码 | PowerShell 5.1 下乱码内容写入笔记 → **永久乱码不可恢复** | 写 `import_doc`/`append_doc` 前**强制校验**所有字符串字段为合法 UTF-8（详见主 SKILL.md「Detailed UTF-8 Encoding Rules」） |
| `update_note` 编辑块 | 对 `editable=false` 的块（图片/录音/附件/链接卡片/AI 生成块）下发 EDIT/DELETE → `code=210039` | 这类块只能作为 APPEND 锚点 |
| 模糊指令 | 用户说「有什么经验吗」可能指「笔记里有没有相关经验记录」 | 先反问确认意图（搜已有笔记 vs 其他含义） |

## 三、权限与凭证

- **凭证获取**：两种来源任选其一——① ima app 的 copilot 对话索要环境变量 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY` 的凭证（已开通导出，推荐）；② https://ima.qq.com/agent-interface 申请 key（普通功能可用，导出类接口可能 220030）。完整指令见主 SKILL.md「Credential Check」。
- **凭证单一来源（V1.0.8+）**：强制从环境变量 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY` 读取，**无任何文件配置与自动降级**（不再读 config.json / ~/.config/ima/）。ima.copilot 环境已自动注入；自建环境需主动 export 到 ~/.bashrc 或 ~/.zshrc。缺凭证 → 脚本退出码 `-100`。
- **220030 三种常见情况**：① 导出接口 key 未开通权限；② 订阅库（普通成员）读原文；③ 普通成员执行写操作（建库/改名/置顶/标签/权限）。
- **凭证安全**：凭证只发送到 `ima.qq.com`；**切勿打包进公开分发的 zip**；失效/报 220030 时重新走「一步获取凭证」更新。

## 四、平台与环境

- **PowerShell 5.1**：`Invoke-RestMethod` 静默将请求 Body 从 UTF-8 转系统 ANSI（中文 Windows 为 GBK）→ 必须用 UTF-8 字节数组模式（见主 SKILL.md「PowerShell 5.1 Environment Detection」）。PowerShell 7+ 默认 UTF-8。
- **Windows cmd**：每条命令前先 `chcp 65001 >nul` 防中文参数乱码；`node` 不在 PATH 时用完整路径。
- **cursor 分页**：首次 `cursor: ""`（空串），**不是** `null` 也不是 `"0"`（部分接口 `null` → `code:-100`；`"0"` 被当字符串跳过第一页）；用返回 `next_cursor` 翻页，`is_end=true` 停止。例外：`list_notebook` 首页传 `"0"`。`search_knowledge_base_in_square` 无 `is_end`，以 `next_cursor` 为空终止。
- **Linux / macOS**：默认 UTF-8，直接跑。

## 五、调用习惯

- **模糊查询直接调 API，别过度读 SKILL.md**：「看看有啥」→ 立刻 `search_knowledge_base(query="")`；「XX 库里有什么」→ `get_knowledge_list(knowledge_base_id=...)`。浅读即可，调用优先。
- **模糊指令先反问**：指代歧义（「经验/技巧/记录/保存/添加」多重解释）→ **0.5 秒反问一句 > 翻 5-8 次 API**。未确认意图前不要调 API。
- **内部 ID 不外露**：面向用户只展示知识库名称、文件标题、文件夹名；`kb_id`/`media_id`/`folder_id` 自己调用用。
- **长结果做摘要 + 给下一步**：结果 > 10 条分主题归类，结尾引导「想深入哪条？」
- **文件上传优先用一键脚本**：`upload_to_kb.cjs` 封装 5 步流程（preflight → 重名 → create_media → COS → add_knowledge），支持 `--path "知识库名/文件夹"`（首选，自动解析）/`--kb-name`/`--cancel-if-dup`，避免手工拼 JSON 出错。

## 六、批量导出打包 SOP（2026-07-22 实测）

1. `list_all_files.cjs --json --path "我的知识库"` 拿全量文件清单（路径 + media_id + media_type）。
2. 对每个文件 `get_media_info` 拿 `url_info.url` + `headers`，URL 后拼 `response-content-type=application/octet-stream&response-content-disposition=attachment` 强制下载。
3. 按 `path` 保持目录结构落盘；**同名文件会覆盖**（如「项目报告v1.0」出现在两个文件夹）→ 加 media_id 短后缀防重。
4. 实测可下载：个人库 TXT(13)/Markdown(7)/MP3录音(15)/PDF 等；**HTML(20) 即使个人库也 220030**（类型受限）；订阅库任意类型 220030。
5. 规模与健壮性：订阅库可能万级条目（如鸿蒙 14661 条）且无法下载；大文件（103MB 无后缀音频）按 media_type 补 `.mp3` 等后缀；批量下载并发 ≤8，单文件失败跳过不中断。
6. 结论：「全部打包」API 层面只能覆盖个人库（创建者）；订阅库引导用户到 IMA 客户端手动导出或申请导出权限。

## 七、实测结论（2026-07-21 全功能实测）
- 在「测试知识库1」实测 **25 项 KB 功能 + 6 项 notes 功能**，仅 `export_media` 因后端权限未开通失败，其余全部通过。
- 脚本为**单一跨平台 Node.js 实现**（纯 `node:` 内置模块、Node 18+）：Windows / Linux / macOS 命令本身完全一致，差异只在 shell 包装与中文编码；老 cmd（GBK）下 emoji 日志乱码但功能不受影响。
- **IMA OpenAPI 不支持删除任何实体**：文件/文件夹/知识库/标签均不可删，测试留痕需用户到客户端手动清理。

## 八、路径解析缓存（V1.0.8+）

自然语言路径（`--path "知识库名/文件夹/子夹"`）的解析结果按「知识库 → 文件夹 → 子文件夹」**树状缓存**，避免重复查 API。

- **缓存位置**：环境变量 `IMA_RESOLVE_CACHE` 指定（ima.copilot 默认 `/sandbox/workspace/.ima_cache/resolve_cache.json`，workspace 持久、平台不重置）；**非 ima.copilot 环境未设置 → 加载即报错**「未设置缓存位置环境变量 IMA_RESOLVE_CACHE」，与凭证同等强制。
- **缓存内容**：只有「名字 → kb_id / folder_id」映射，**不含凭证**。
- **失效自愈**：操作 API 报「目标不存在」（`220001` / invalid / 不存在 / 未找到 类）→ 自动失效该路径缓存 → 全 API 重查 → 重试一次；重查任一层找不到 → 报「在「X」下未找到「Y」」整体失败。权限（220030）/ 限流（200001）类错误**不触发**自愈。
- **手动清缓存**：删除缓存文件即可，下次解析自动重建；知识库/文件夹被删除或改名后首次操作会走自愈恢复。
- **常见坑**：
  - 缓存文件损坏 / 格式不对 → 自动按空缓存重建，不影响使用
  - 首次操作报「未找到」且路径确实存在 → 多为缓存键不匹配（省略库名/模糊名），会保守全清重查，属正常流程
  - `ima_skill_create` 注册报 `is a directory` → skill 目录里有嵌套软链或同名子目录，先 `find <skill_dir> -type l` 检查并删除后重新注册
