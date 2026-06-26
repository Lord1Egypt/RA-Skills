# Skill — 扫描分析

## 职责

理解项目代码和目录结构，识别代码文件和资源文件，提取所有需要本地化的文本，并生成扫描报告和分析报告。

## 前置条件

- `i18n-config.json` 已存在于项目根目录，包含项目路径、源语言、`translateImages`、`mcpAvailable` 等信息
- 如果没有，先回到主控 SKILL.md 的阶段 0 收集信息
- **开始执行前，必须先读取 `i18n-config.json`**，获取 `translateImages` 和 `mcpAvailable` 的值，后续步骤会用到

## ⚠️ 完整性要求

**扫描必须完整覆盖所有文件，不允许遗漏。** 具体措施：
1. **优先使用 `scripts/scan-chinese.js` 脚本进行 AST 扫描**：该脚本支持全部文件格式（JS/TS/JSON/CSV/TSV/HTML/WXML/CSS/WXSS/Cocos/Unity/C#/XML/TXT），基于 AST 精确提取，自动跳过注释
2. 脚本扫描完成后，**必须使用 `search_content`（grep）进行独立交叉对比**：用正则搜索所有中文，与脚本结果取并集
3. 大文件（超过 5000 行）分段扫描，每段不超过 2000 行，确保拼接结果完整
4. 扫描完成后，统计 `entries` 数量，与文件中实际包含的中文文本进行交叉校验
5. 如果上下文窗口不够一次处理完，分批扫描不同的文件集合，最后合并结果

## 执行步骤

### 步骤 1：全局项目扫描

扫描整个项目目录，建立对项目的基本认识：

1. **列出目录结构**（排除 `node_modules/`、`.git/`、`i18n/`、`build/`、`dist/`、`temp/`、`library/`、`local/` 等非源码目录）
2. **识别游戏引擎**（识别后写入 `i18n-config.json` 的 `engine` 字段）：
   - **Cocos Creator（<3.6）** → `engine: "cocos-creator"`：检查 `assets/cc.config.json`、`settings/` 目录、`.fire`/`.scene` 文件；版本 <3.6 或项目未启用 L10N
   - **Cocos Creator（≥3.6 且使用 L10N）** → `engine: "cocos-l10n"`：检查 `localization-editor/` 目录存在，或版本 ≥3.6 且用户确认使用 L10N 方案
   - **LayaAir** → `engine: "laya"`：检查 `laya.init()` 调用、`LayaAir/` 目录、`laya.game.config.json`
   - **Egret 白鹭** → `engine: "egret"`：检查 `egretProperties.json`、`libs/eui/eui.d.ts`
   - **Unity** → `engine: "unity"`：检查 `Assets/` + `ProjectSettings/` 目录结构、`.unity` / `.prefab`（YAML 格式）/ `.cs` 文件
   - **原生微信小游戏** → `engine: "native"`：检查 `game.json`、`game.js`；不匹配以上任何引擎时的默认值
3. **分类文件**：
   - 代码文件：`.js`、`.ts`、`.jsx`、`.tsx`、`.json`、`.wxml`、`.html`、`.htm`、`.css`、`.wxss`、`.scss`、`.less`、`.scene`、`.prefab`、`.fire`、`.xml`
   - **数据文件**：`.csv`、`.tsv`、`.txt`（位于 `resources/`、`datas/`、`data/`、`config/` 等数据目录下的文本文件）
   - 图片资源文件（按后缀名全量匹配，不区分大小写）：`.png`、`.jpg`、`.jpeg`、`.gif`、`.webp`、`.bmp`、`.svg`、`.ico`、`.tiff`、`.tif`、`.pvr`、`.pkm`、`.astc`、`.ktx`、`.dds`、`.exr`、`.hdr`
   - 其他资源文件：`.mp3`、`.wav`、`.ogg`、`.mp4`、`.fnt`、`.ttf`、`.atlas`、`.plist`
   - 配置文件：`game.json`、`project.config.json`、`tsconfig.json`
   - Unity 资源：`.prefab`、`.asset`、`.mat`、`.unity`
   - C# 代码：`.cs`

### 步骤 2：脚本 AST 扫描（优先路径）

**⭐ 这是主要的扫描路径。** 使用 `scripts/scan-chinese.js` 对项目进行全量 AST 扫描，精确提取字符串字面量中的中文文本。

#### 2a-前置. 检查并安装脚本依赖（⚠️ 必须在执行脚本前完成）

脚本依赖（esprima、@babel/parser 等）安装在 `scripts/node_modules/` 目录中。**执行脚本前必须确认依赖已安装**，否则脚本将报错退出。

**检查方式**：检查 `scripts/node_modules/` 目录是否存在。

```bash
# 获取 scripts 目录的路径（即 scan-chinese.js 所在目录）
SCRIPTS_DIR="<skill所在目录>/scripts"

# 检查 node_modules 是否存在
if [ ! -d "$SCRIPTS_DIR/node_modules" ]; then
  echo "📦 脚本依赖未安装，正在安装..."
  cd "$SCRIPTS_DIR" && npm install
  echo "✅ 依赖安装完成"
else
  echo "✅ 脚本依赖已就绪"
fi
```

**关键说明**：
- 依赖声明在 `scripts/package.json` 中，包含：esprima、@babel/parser、@babel/traverse、@typescript-eslint/typescript-estree、json-source-map、papaparse、yaml
- 依赖安装到 `scripts/node_modules/`，**不是**用户项目的 `node_modules/`
- 脚本通过 `__dirname`（脚本自身路径）查找 `node_modules`，因此无论从哪个目录执行脚本，都能正确找到依赖
- 如果 `npm install` 因网络问题失败，至少需要安装核心依赖：`npm install esprima @babel/parser @babel/traverse`
- **此步骤只需在首次使用时执行一次**，后续执行脚本无需重复安装

#### 2a. 执行脚本扫描

```bash
node scripts/scan-chinese.js \
  --project <projectRoot> \
  --scan-paths <扫描目录,逗号分隔> \
  --exclude node_modules,.git,build,dist,temp,library,local,i18n \
  --engine <cocos|unity|laya|egret|native> \
  --output <projectRoot>/i18n/ast_scan_result.json \
  --verbose
```

参数说明：
- `--project`：项目根目录
- `--scan-paths`：扫描的子目录（默认 `.`，即整个项目）
- `--exclude`：排除的目录名
- `--engine`：游戏引擎类型（影响 Cocos/Unity 场景文件的解析方式）
- `--output`：输出文件路径
- `--verbose`：详细输出每个文件的扫描结果（同时会打印依赖加载状态）

#### 2b. 脚本支持的文件格式与解析策略

| 文件类型 | 扩展名 | 解析方式 | 说明 |
|---------|--------|---------|------|
| JavaScript | `.js`, `.jsx` | esprima AST → @babel/parser 容错降级 | 双引擎策略，确保最大兼容性 |
| TypeScript | `.ts`, `.tsx` | @typescript-eslint/typescript-estree → @babel/parser 降级 | 支持 TS 特有语法 |
| JSON | `.json` | json-source-map 精确定位 → JSON.parse 降级 | 含 Cocos 序列化资源深度扫描 |
| CSV/TSV | `.csv`, `.tsv` | 逐行逐单元格解析 | 自动识别表头行，精确单元格定位 |
| HTML/WXML | `.html`, `.htm`, `.wxml` | 正则匹配标签文本和属性值 | 扫描 `placeholder`、`title`、`alt` 等属性 |
| CSS/WXSS | `.css`, `.wxss`, `.scss`, `.less` | 正则提取 `content` 属性、`font-family` 中文字体 | 仅提取需要翻译的 CSS 值 |
| Cocos 场景 | `.prefab`, `.fire`, `.scene` | JSON 解析 + cc.Label/RichText 提取 | Cocos Creator 场景/预制体 |
| Unity | `.prefab`, `.asset`, `.mat`, `.unity` | YAML 解析 + m_Text 字段提取 | Unity 序列化资源 |
| C# | `.cs` | 正则匹配字符串字面量 | 支持插值字符串 `$""`、逐字字符串 `@""` |
| XML | `.xml` | 正则匹配标签文本和属性值 | 通用 XML 扫描 |
| 纯文本 | `.txt` | 逐行扫描 | 每行含中文即收录 |

#### 2c. 脚本 AST 扫描的优势

- **精确字符串字面量提取**：AST 解析器能准确区分代码字符串和注释、import 路径等
- **自动跳过注释**：不会将 `// 修复XXX` 注释中的中文误识为需要翻译的文本
- **精确行列定位**：每个条目都有精确的 `loc.start.line`、`loc.start.column` 和 `range`
- **模板字符串完整提取**：`` `恭喜 ${name} 获得 ${reward}` `` 会提取完整模板并记录变量
- **拼接字符串识别**：`name + "达到" + lv + "级"` 会识别为 `concatenation` 类型
- **CSV/TSV 数据精确定位**：每个单元格都有精确的行列偏移和 range
- **双引擎容错**：esprima 解析失败时自动降级到 @babel/parser（支持 JSX/可选链/类属性等现代语法）

#### 2d. 脚本扫描结果格式

脚本输出的 JSON 格式与 `scan_report.json` 兼容：

```json
{
  "version": "1.0",
  "projectPath": "<项目根目录>",
  "sourceLanguage": "zh-CN",
  "scanTime": "...",
  "scanMethod": "ast_scan",
  "summary": {
    "totalTextEntries": 256,
    "totalMediaEntries": 50,
    "byType": { "text": 200, "template": 30, "concatenation": 26 },
    "byFileType": { ".js": 120, ".ts": 80, ".json": 20, ".csv": 36 }
  },
  "entries": [ /* TextEntry 数组 */ ],
  "mediaEntries": [ /* 媒体文件数组 */ ]
}
```

每个 TextEntry 包含：
- `key`：MD5 唯一标识
- `value`：中文文本内容
- `filePath`：相对文件路径
- `type`：`text` / `template` / `concatenation`
- `line`、`column`：行号列号（1-based）
- `loc`：精确位置 `{ start: { line, column }, end: { line, column } }`
- `range`：`[startOffset, endOffset]`
- `variables`：变量列表
- `context`：上下文（如 `csv_data:name`、`html_text`、`css_content`、`cocos_label` 等）

### 步骤 2-补充：AI 手动扫描（仅脚本无法覆盖时使用）

如果脚本执行失败（如依赖缺失）或某些特殊文件格式脚本不支持，AI 需要手动扫描这些文件。手动扫描规则如下：

#### 2a. JS/TS 文件中的文本

使用以下策略提取文本：

**纯字符串**：匹配引号内包含中文字符的文本
```javascript
// 匹配以下形式：
"开始游戏"          // 双引号字符串
'开始游戏'          // 单引号字符串
`开始游戏`          // 模板字符串（无变量）
```

提取规则：
- 使用正则 `/(['"\`])([^'"\`]*[\u4e00-\u9fff]+[^'"\`]*)\1/g` 匹配包含中文的字符串
- 记录精确的行号、列号和字符范围（range 必须精确到字符级别）
- 生成 key（使用 MD5 hash）
- **range 精确记录**：`range[0]` 是字符串（含引号）在文件中的起始偏移，`range[1]` 是结束偏移

**模板字符串**：包含 `${...}` 变量的模板字符串
```javascript
`恭喜 ${name} 获得 ${reward}`
```

提取规则：
- 匹配包含中文的模板字符串
- 提取变量名列表
- type 设为 `template`

**拼接字符串（重要）**：变量和字符串通过 `+` 拼接
```javascript
name + "达到" + lv + "级"
"你的" + itemName + "已经升到" + level + "级了"
```

提取规则：
- 识别包含中文字符串的拼接表达式
- **完整记录整个拼接表达式**（包括变量部分）
- 提取其中所有中文文本片段
- 提取变量名列表
- type 设为 `concatenation`
- 设置 `originalExpression` 为完整表达式
- 设置 `extractedTexts` 为提取的中文文本数组
- **range 精确记录整个拼接表达式的起止位置**

**需要跳过的内容**：
- 注释中的文本（`//` 和 `/* */`）
- `console.log()` / `console.warn()` / `console.error()` 中的纯调试文本
- import/require 路径
- 正则表达式中的文本
- 已经有 i18n 包装的文本（如 `i18n.t("key")`）

#### 2b. JSON 文件中的文本

```json
{
  "name": "开始",
  "description": "这是一个按钮"
}
```

提取规则：
- 遍历 JSON 值，提取包含中文的字符串值
- 记录 JSON 路径（如 `name`、`items[0].label`）
- 跳过键名，只提取值
- 跳过 URL、文件路径等非文本内容

#### 2c. Scene/Prefab 文件（Cocos Creator）

Cocos Creator 的 `.scene` 和 `.prefab` 文件是 JSON 格式，其中的 `cc.Label` 组件包含需要翻译的文本。

提取规则：
- 查找 `__type__: "cc.Label"` 或 `_string` 字段
- 提取其中包含中文的文本

#### 2d. WXML/HTML 文件

```html
<text>开始游戏</text>
<view class="title">恭喜你，通关了！</view>
```

提取规则：
- 提取标签内的中文文本内容
- 提取包含中文的属性值（如 `placeholder="请输入"`）
- 跳过 CSS 类名、事件绑定等非文本属性

#### 2e. CSS/WXSS 文件

```css
.title::before {
  content: "第一关";
}
```

提取规则：
- 仅提取 `content` 属性中包含中文的文本
- 跳过其他属性

#### 2f. CSV/TSV 数据文件

小游戏常将配置数据放在 CSV 文件中（如角色表、关卡表、物品表等），这些文件中通常包含大量需要翻译的中文文本。

**典型 CSV 结构**（以 Cocos Creator 项目常见格式为例）：
```
角色名称,攻击类型,描述             ← 第1行：中文表头说明
string,number,string               ← 第2行：字段类型
name,type,desc                     ← 第3行：英文字段名
斧头兵,1,只会单体攻击的近战兵。    ← 第4行起：数据
标枪兵,4,只会单体攻击的远程兵。
```

**提取规则**：

1. **识别 CSV/TSV 文件**：
   - 后缀为 `.csv` 或 `.tsv` 的文件
   - 位于 `resources/`、`datas/`、`data/`、`config/` 等数据目录下的文本文件（可能没有后缀或后缀为 `.txt`）

2. **解析 CSV 结构**：
   - 按逗号（CSV）或制表符（TSV）分割
   - 识别表头行（通常前 1-3 行是表头/类型/字段名，数据从之后开始）
   - 判断依据：如果第 2 行全是类型关键字（`number`、`string`、`boolean`、`int`、`float`），则前 3 行为表头

3. **提取数据行中的中文**：
   - 遍历每一行数据的每一个单元格
   - 提取包含中文字符的单元格值
   - 跳过纯数字、纯英文、空值
   - 跳过看起来是 ID 或编码的字段（如 `804#1_804#2_804#3`）

4. **表头行的中文**：
   - 第 1 行的中文表头说明通常不需要翻译（它们是给开发者看的注释），但仍应记录在报告中，`context` 标注为 `csv_header`
   - 如果表头中的中文在游戏运行时会被读取使用（非常少见），需要翻译

5. **条目格式**：
   - `type` 设为 `text`
   - `filePath` 为 CSV 文件的相对路径
   - `loc.start.line` 为数据所在行号（0-indexed）
   - `loc.start.column` 为该单元格在行中的列索引
   - `context` 标注为 `csv_data`，并注明列名（如 `csv_data:name`、`csv_data:desc`）
   - `range` 标注该单元格值在文件中的精确字符偏移（如果 CSV 结构简单且可以精确计算）；如果无法精确计算，设为 `[0, 0]` 并确保 `loc` 准确
   - **⚠️ CSV 中相同中文可能出现多次**（如同一角色的不同等级重复出现），需要逐条记录每个出现位置，不可去重

6. **⚠️ 注意事项**：
   - CSV 文件可能使用 `\r\n`（Windows）或 `\n`（Unix）换行符，需要统一处理
   - 某些 CSV 字段可能被双引号包裹（`"含逗号,的值"`），需要正确解析
   - 数据文件通常被游戏代码在运行时读取和解析，翻译时需要保持 CSV 格式不变（只替换单元格内的中文文本）

### 步骤 3 & 4：图片处理（根据配置执行）

**⚠️ 在执行本步骤前，你必须已经读取了 `i18n-config.json` 并知道 `translateImages` 和 `mcpAvailable` 的值。如果还没有读取，现在立即读取。**

根据 `translateImages` 和 `mcpAvailable` 的组合值，选择对应的执行路径：

---

#### 路径 A：`translateImages` = `false`

不执行任何图片相关操作。报告中 `imageEntries` 为空数组，`totalImageEntries` 为 0。直接进入步骤 5。

---

#### 路径 B：`translateImages` = `true`，`mcpAvailable` = `false`

收集项目图片列表，但不执行 OCR：

1. **按后缀名全量匹配**所有图片文件，支持的后缀包括：`.png`、`.jpg`、`.jpeg`、`.gif`、`.webp`、`.bmp`、`.svg`、`.ico`、`.tiff`、`.tif`、`.pvr`、`.pkm`、`.astc`、`.ktx`、`.dds`、`.exr`、`.hdr`
   - **⚠️ 不做任何内容初筛**，只要后缀匹配就纳入列表，避免遗漏含文字的图片
   - 匹配时后缀名不区分大小写（如 `.PNG`、`.Jpg` 都应匹配）
2. **仅排除**以下路径：
   - `node_modules/`、`.git/`、`build/`、`dist/`、`temp/`、`library/`、`local/` 等非源码目录
   - `i18n/assets/` 目录（翻译产物）
   - `i18n/backups/` 目录（备份文件）
3. 对于每张图片，记录文件路径和文件大小
4. 所有图片加入 `imageEntries`，`ocrText` 设为 `null`，`ocrStatus` 设为 `"pending"`

然后进入步骤 5。

---

#### 路径 C：`translateImages` = `true`，`mcpAvailable` = `true`

**这是完整路径。收集全部图片 → 全量上传 OCR → 根据 OCR 结果筛选出含中文的图片。**

**C-1. 收集项目中所有图片**：
1. **按后缀名全量匹配**所有图片文件，支持的后缀包括：`.png`、`.jpg`、`.jpeg`、`.gif`、`.webp`、`.bmp`、`.svg`、`.ico`、`.tiff`、`.tif`、`.pvr`、`.pkm`、`.astc`、`.ktx`、`.dds`、`.exr`、`.hdr`
   - **⚠️ 不做任何内容初筛（如文件大小、图片尺寸等）**，只要后缀匹配就纳入列表，避免遗漏含文字的图片
   - 匹配时后缀名不区分大小写（如 `.PNG`、`.Jpg` 都应匹配）
2. **仅排除**以下路径：
   - `node_modules/`、`.git/`、`build/`、`dist/`、`temp/`、`library/`、`local/` 等非源码目录
   - `i18n/assets/` 目录（翻译产物）
   - `i18n/backups/` 目录（备份文件）
3. 将所有符合条件的图片路径写入 `i18n/image_list.txt`（每行一个相对路径）
4. 记录图片总数

**C-2. MCP 上传全部图片**：

**⛔ 严禁 AI 自行创建 zip、读取图片二进制、调用 MCP 分片上传接口（UploadScanFilesInitMcp/PartMcp/CompleteMcp）。必须且只能使用以下脚本命令完成上传：**

1. 执行以下命令上传图片：
   ```
   node scripts/upload-images.js --project <projectRoot> --images-file i18n/image_list.txt
   ```
   脚本会自动完成 zip 打包、MCP 配置读取、分片上传全流程。
2. 从命令输出的最后几行中查找 `__FILE_ID__=<id>`，提取 `file_id`（整数）
3. **如果上传失败**：将所有图片标记为 `ocrStatus: "failed"`，进入步骤 5

**C-3. 执行 OCR（全量）**：
1. 调用 MCP 工具 `StartImageOcrMcp`，传入参数 `{ "file_id": <file_id> }`
2. 调用 MCP 工具 `GetImageOcrProgressMcp`，传入 `{ "file_id": <file_id> }` 轮询进度
   - 返回 `status=1`（运行中）：等待 5 秒后再次调用
   - 返回 `status=2`（成功）：进入下一步
   - 返回 `status=3`（失败）：标记全部为 `ocrStatus: "failed"`，进入步骤 5
3. OCR 成功后，调用 MCP 工具 `GetImageOcrResultMcp`，传入 `{ "file_id": <file_id> }`
4. 获取返回的 `ocr_items` 数组

**C-4. 筛选含中文的图片，生成 imageEntries**：

**关键变化**：不是把所有图片都放入 `imageEntries`，而是只把 OCR 识别出含中文文本的图片放入。

1. 遍历 `ocr_items`，将每个 `text` 按 `locations` 中的图片路径分配
2. `locations` 中的路径需要去掉上传脚本添加的前缀（如 `files/`），还原为项目相对路径
3. **筛选条件**：只有 `text` 中包含中文字符（匹配 `/[\u4e00-\u9fff]/`）的条目才纳入 `imageEntries`
4. 同一张图片出现在多个 `ocr_items` 中时，将所有中文文本用 `\n` 连接合并
5. 生成 `imageEntries`，每个条目：
   - `ocrText`：OCR 识别出的中文文本
   - `ocrStatus`：`"recognized"`
6. **不含中文的图片不进入 `imageEntries`**（它们不需要翻译）

**C-5. 保存含中文图片列表**：

将筛选出的含中文图片路径单独保存到 `i18n/chinese_image_list.txt`（每行一个相对路径），供阶段 3（执行翻译）使用。

**示例**：
```
项目共 50 张图片，全部上传 OCR

OCR 返回:
  ocr_items[0]: text="开始游戏", locations=["files/assets/img/btn_start.png"]
  ocr_items[1]: text="Settings", locations=["files/assets/img/btn_setting.png"]  ← 无中文，排除
  ocr_items[2]: text="设置", locations=["files/assets/img/btn_config.png"]

筛选后 imageEntries（仅含中文的）:
  - filePath="assets/img/btn_start.png", ocrText="开始游戏", ocrStatus="recognized"
  - filePath="assets/img/btn_config.png", ocrText="设置", ocrStatus="recognized"

chinese_image_list.txt:
  assets/img/btn_start.png
  assets/img/btn_config.png
```

完成 C-4 后进入步骤 5。

---

### 步骤 5：生成报告

**⚠️ 生成报告前，先确认以下检查点：**
- 如果 `translateImages` = `true` 且 `mcpAvailable` = `true`：确认已经执行了路径 C 的全部步骤（C-1 到 C-4），`imageEntries` 中的 `ocrStatus` 不应全部为 `"pending"`
- 如果上述检查不通过，**回到步骤 3 & 4 执行缺失的步骤**

#### 生成 scan_report.json

将步骤 2（AST 脚本扫描）和步骤 3-4（图片处理）的结果汇总为扫描报告，格式参见 `references/scan-report-schema.md`。

**基于脚本扫描结果生成**：
- 读取 `i18n/ast_scan_result.json`（步骤 2a 脚本输出），其中 `entries` 数组已包含全部文本条目（带精确 key、loc、range）
- 将脚本输出的条目直接作为 `scan_report.json` 的 `entries` 基础
- 补充步骤 7（grep 交叉对比）发现的遗漏条目
- 合并图片条目（`imageEntries`）

要点：
- 每个条目必须有唯一的 `key`（使用 `filePath + line + column + value` 的 MD5）
- 拼接字符串的 `value` 保存完整的拼接表达式
- 所有路径使用相对于项目根目录的相对路径
- **range 必须精确**：这是替换阶段的核心依据，错误的 range 会导致替换失败或代码损坏
- **图片条目**（`imageEntries`）：每张图片必须包含 `ocrText` 和 `ocrStatus` 字段，反映 OCR 的实际结果：
  - OCR 识别到文本 → `ocrText` 为文本内容，`ocrStatus` 为 `"recognized"`
  - OCR 执行但未识别到文本 → `ocrText` 为 `null`，`ocrStatus` 为 `"empty"`
  - OCR 失败 → `ocrText` 为 `null`，`ocrStatus` 为 `"failed"`
  - 未执行 OCR → `ocrText` 为 `null`，`ocrStatus` 为 `"pending"`

#### 生成 analysis_report.json

基于扫描过程中的观察，生成分析报告：

1. **引擎信息**：识别到的引擎类型和版本
2. **项目结构**：源码目录、资源目录、配置文件
3. **i18n 就绪度**：
   - 是否已有 i18n 框架
   - 硬编码文本数量
   - 模板字符串数量
   - 拼接字符串数量
   - 包含文字的图片数量
4. **模块分组**：将文件按功能模块分组（UI、战斗、教程、设置等）
5. **建议**：基于分析结果给出本地化建议

### 步骤 6：自检

**⚠️ 报告写入磁盘后，必须执行以下自检。任何一项不通过都必须修正后重新写入报告。**

**6a. 读取已写入的 `scan_report.json`，逐项验证：**

| 检查项 | 验证方法 | 不通过时的修正 |
|--------|----------|----------------|
| **文本条目完整性** | `entries` 数组不为空（除非项目确实没有中文文本） | 回到步骤 2 重新扫描 |
| **文本条目字段** | 每个 entry 都有 `key`、`value`、`filePath`、`type`、`loc`、`range` | 补全缺失字段 |
| **图片条目存在性**（路径 B/C） | `translateImages=true` 时，`imageEntries` 数组不为空（除非项目确实没有图片） | 回到步径 3 & 4 重新执行 |
| **OCR 结果写入**（路径 C） | `translateImages=true` 且 `mcpAvailable=true` 时，`imageEntries` 中至少有部分条目的 `ocrStatus` 为 `"recognized"` 或 `"empty"`（不应全部为 `"pending"`） | 回到路径 C 的 C-4 步骤，将 OCR 结果合并写入 |
| **OCR 文本内容**（路径 C） | 对 `ocrStatus="recognized"` 的条目，`ocrText` 不为 `null` 且不为空字符串 | 重新从 OCR 结果中提取并写入 |
| **统计数据一致** | `summary.totalTextEntries` == `entries.length`；`summary.totalImageEntries` == `imageEntries.length` | 修正 summary 统计 |

**6b. 读取已写入的 `analysis_report.json`，验证：**
- `i18nReadiness` 中的各项统计数字与 scan_report 一致
- 如果走了路径 C，`imageWithTextCount` 应等于 `imageEntries` 中 `ocrStatus="recognized"` 的数量

**6c. 输出自检结果**（仅内部使用，不需要展示给用户）：
- 全部通过 → 进入步骤 7
- 有不通过项 → 按上表修正后重新写入报告，再次执行 6a/6b

### 步骤 7：grep 交叉对比扫描

**⚠️ 这是扫描阶段的关键步骤，不可跳过。AST 扫描虽然精确，但可能在以下场景遗漏中文：**
- AST 解析器不支持的文件格式（如非标准配置文件）
- AST 解析失败的文件（语法错误的 JS/TS 文件）
- 被引擎特殊处理的序列化格式
- 动态生成的字符串（如通过 `String.fromCharCode` 等方式）
- 嵌套在复杂表达式中的中文

**使用 grep 进行独立全量搜索，与步骤 2 的 AST 扫描结果进行交叉对比。**

#### 7a. 使用 `search_content` 搜索所有中文

使用 `search_content`（grep）工具，在项目源码目录中搜索所有包含中文字符的文件：

```
搜索正则: [\u4e00-\u9fff]
搜索范围: 项目根目录（排除 node_modules、.git、i18n、build、dist、temp、library、local）
```

**具体执行方式**（按文件类型分批搜索，提高效率）：

1. **代码文件**：`search_content`，glob 为 `*.{js,ts,jsx,tsx}`，pattern 为 `[\u4e00-\u9fff]`
2. **JSON 文件**：`search_content`，glob 为 `*.json`（排除 `.meta` 文件），pattern 为 `[\u4e00-\u9fff]`
3. **数据文件**：`search_content`，glob 为 `*.{csv,tsv,txt}`，pattern 为 `[\u4e00-\u9fff]`
4. **标记语言**：`search_content`，glob 为 `*.{wxml,html,htm,xml}`，pattern 为 `[\u4e00-\u9fff]`
5. **样式文件**：`search_content`，glob 为 `*.{css,wxss,scss,less}`，pattern 为 `[\u4e00-\u9fff]`
6. **场景文件**：`search_content`，glob 为 `*.{scene,prefab,fire}`，pattern 为 `[\u4e00-\u9fff]`

#### 7b. 与 AST 扫描结果交叉对比

将 grep 搜索结果与 `ast_scan_result.json`（或已生成的 `scan_report.json`）中已有的 `entries` 进行对比：

1. **对于每个 grep 发现的含中文的文件和行**：
   - 检查该 `filePath` + `line` 是否已存在于 AST 扫描结果的 `entries` 中
   - 如果已存在 → 跳过（已覆盖）✅
   - 如果不存在 → 这是一个**潜在遗漏**，需要进一步分析 ⚠️

2. **对潜在遗漏条目进行分类判断**：

| 类型 | 判断条件 | 处理方式 |
|------|---------|---------|
| **注释中的中文** | 行以 `//` 开头，或位于 `/* */` 块注释中 | 跳过（不需要翻译） |
| **console.log 调试文本** | `console.log/warn/error(...)` 中的文本 | 跳过（通常不需要翻译，除非面向用户） |
| **import/require 路径** | 出现在 `import` 或 `require()` 中 | 跳过 |
| **.meta 文件** | 文件名以 `.meta` 结尾 | 跳过 |
| **需要翻译的中文** | 不属于以上排除类型 | **补充到扫描报告中** |

3. **排除规则的优先级**：如果一行中同时包含注释中的中文和代码中的中文（如 `let msg = "格子不足"; // 格子不足提示`），AST 扫描已经精确提取了代码字符串，grep 发现的是同一行，应视为已覆盖。

#### 7c. 补充遗漏条目

对于确认需要补充的遗漏条目：

1. **读取对应文件的具体内容**，理解中文出现的上下文
2. **精确定位**：确定该中文文本的精确行号、列号和 range
3. **生成新的 TextEntry**：按照 scan_report_schema.md 的格式生成条目
4. **追加到 `scan_report.json`** 的 `entries` 数组中
5. **更新统计**：`summary.totalTextEntries` 等

#### 7d. 输出交叉对比结果

```
🔍 交叉对比扫描完成：
   AST 扫描条目: X 条
   grep 发现含中文文件: Y 个
   grep 发现含中文行: Z 行
   已被 AST 覆盖: A 行
   注释/调试/排除: B 行
   新发现需补充: C 条
   更新后总计: X + C 条
```

如果有新发现条目（C > 0），重新执行步骤 6 的自检。

### 步骤 8：输出摘要并继续

将报告保存到 `{projectRoot}/i18n/` 目录，输出简短摘要。**本阶段到此结束，由 SKILL.md 控制后续流程。**

摘要格式：
```
📊 扫描完成！
   AST 脚本扫描: X 条（来自 scan-chinese.js）
   grep 交叉补充: Y 条
   总计: X + Y 条文本、M 张疑似含文字的图片。
```
（如果 `translateImages` 为 `false`，省略图片部分）

## 关键注意事项

1. **不要遗漏拼接字符串**：这是小游戏本地化中最容易出问题的地方。`scripts/scan-chinese.js` 已支持 `concatenation` 类型的完整识别，会将 `a + "中文" + b + "中文"` 识别为拼接表达式并提取变量。

2. **处理嵌套场景**：一个文件中可能同时存在纯文本、模板字符串和拼接字符串，`scan-chinese.js` 的 AST 遍历能全部处理。

3. **避免重复计数**：同一个文本在同一位置只计一次。如果在拼接表达式中已提取，不要再作为独立纯文本重复提取。`scan-chinese.js` 的 BinaryExpression 处理会检查父节点，避免嵌套重复。

4. **大文件处理**：`scan-chinese.js` 通过 AST 解析处理大文件，不受行数限制。但对于 AI 手动补充时，超过 5000 行的文件需分段处理。

5. **Scene 文件特殊处理**：Cocos Creator 的 scene 文件可能非常大（数万行 JSON），`scan-chinese.js` 会自动识别 `cc.Label` 和 `cc.RichText` 组件提取 `_string` 字段。

6. **range 和列号精确性**：range 和 `loc.start.column` 是替换阶段的核心依据。`scan-chinese.js` 输出的每个条目都包含精确的 range 和 loc。在记录 range 时，确保 `range[0]` 和 `range[1]` 是文件中的精确字符偏移量。**`loc.start.column` 必须指向字符串字面量的引号位置或字符串内容起始位置**（即中文文本在行中的精确列偏移），替换脚本 v3.4 会使用列号做精确切片匹配来区分注释和代码中的同名文本。如果无法确定精确 range，至少确保 `loc`（行号和列号）的准确性。

7. **CSV/TSV 数据文件不可遗漏**：`scan-chinese.js` 已内置 CSV/TSV 扫描支持，自动识别表头行结构，逐行逐单元格提取中文，输出带精确行列和 range 的结果。

8. **双路径交叉对比是必须步骤**：步骤 2 的 AST 脚本扫描（精确但可能遗漏非标准格式）和步骤 7 的 grep 独立扫描（全面但不区分注释/代码），两者取并集才能最大限度确保零遗漏。即使 AST 扫描结果看起来已经完整，也必须执行 grep 交叉对比步骤。

9. **脚本依赖安装（首次使用前必须执行）**：`scan-chinese.js` 的依赖声明在 `scripts/package.json` 中，需要在脚本目录下执行 `npm install` 安装到 `scripts/node_modules/`。脚本启动时会自动从以下路径搜索依赖（按优先级）：① `scripts/node_modules/`（脚本自身目录）→ ② skill 根目录的 `node_modules/` → ③ `--project` 指定的项目目录的 `node_modules/` → ④ Node.js 全局路径。**推荐做法是在 `scripts/` 目录下执行 `npm install`，一键安装全部依赖**，这是最可靠的方式。如果 `scripts/node_modules/` 不存在，脚本会在报错信息中提示正确的安装命令。
