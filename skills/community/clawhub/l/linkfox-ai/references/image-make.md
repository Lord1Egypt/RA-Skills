# AI 作图 / 视频 - 全部接口完整说明

本文档为 LinkFoxAI Skill 内置参考，涵盖开放平台 AI 作图/视频能力、完整参数与注意事项。

所有接口均为 **POST**，请求体 **Content-Type: application/json**，响应体 application/json。

---

## 一、通用作图流程

1. **可选**：调用「作图素材」获取预设素材地址（模特、场景等）。
2. **可选**：本地图片需先调用「图片上传」得到可访问 URL。
3. 调用具体作图接口，得到 **任务 ID**（`data.id`）。
4. 轮询「获取作图结果」直到 `data.status` 为 3(成功) 或 4(失败)，取 `data.resultList[].url` 得到结果图。
5. 结果图为**临时地址，有效期约 8 小时**；过期后调用「刷新结果图片地址」传入**图片 ID**（`resultList[].id`，非任务 ID）获取新 URL。

**注意事项：**
- 用户图片需外网可访问、链接稳定，建议使用国内图床（阿里云 OSS、腾讯云 COS 等）。
- 作图素材地址通过「作图素材」接口获得，用作预设资源。
- 本地图片上传支持 base64 编码，无需单独传 OSS。

---

## 二、通用响应结构

所有作图创建任务接口的响应结构一致：

| 参数 | 说明 | 类型 |
|------|------|------|
| traceId | 链路 ID | string |
| code | 状态码，200 为成功 | string |
| msg | 成功/错误描述 | string |
| msgKey | 错误码，code 非 200 时存在 | string |
| data.id | 任务 ID（用于轮询结果） | number |

响应示例：
```json
{"traceId":"f6e0fe4f360f78445c2c5d52f2414dea","code":"200","msg":"成功","data":{"id":123456}}
```

---

## 三、作图素材

**路径**：`/linkfox-ai/image/v2/material/list`

**注意**：此接口可用于连通性测试，无需上传图片。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| type | 类型：1=AI换模特-预设模特，2=模特图通用-预设场景，3=AI换模特固定脸-预设模特，4=模特图通用-场景素材，5=AI穿衣姿势-上下装素材，6=AI穿衣姿势-连体衣素材，7=AI穿戴-模特素材，8=手持商品-姿势素材，9=姿势裂变素材，10=套图-排版素材 | 是 | string |
| pageNum | 页数，默认 1 | 否 | number |
| pageSize | 单页条数，默认 10 | 否 | number |

响应 data 含 list（url/name/tagList）、total、hasMore。

```json
{"type":"1"}
```

---

## 四、图片上传

### 4.1 base64 上传

**路径**：`/linkfox-ai/image/v2/uploadByBase64`

**注意**：全局 QPS 100（不分 IP 不分用户）。适用于没有图片存储服务或无法外网访问的场景。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| fileName | 文件名（带扩展名），支持 jpeg/jpg/png/webp | 是 | string |
| base64 | 图片 base64 编码，文件不超过 10MB，最长边不超过 4096 | 是 | string |

响应 data 含 viewUrl（上传后图片访问地址）。

### 4.2 生成上传地址（OSS 直传）

**路径**：`/linkfox-ai/image/v1/generateUploadUrl`

**注意**：QPS 由阿里控制，并发能力高于 base64 方式。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| fileName | 文件名（主要取后缀） | 是 | string |

响应 data 含 viewUrl（上传成功后可用地址）、policy（url/signature/policy/key/OSSAccessKeyId，用于客户端直传 OSS）。

---

## 五、获取作图结果

**路径**：`/linkfox-ai/image/v2/make/info`

**注意**：需轮询此接口直到 status 变为 3（成功）或 4（失败）。建议轮询间隔 3-5 秒。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| id | 作图任务 ID | 是 | number |
| format | 结果格式，目前仅支持 jpg | 否 | string |

响应 data：

| 字段 | 说明 | 类型 |
|------|------|------|
| id | 作图任务 ID | number |
| status | 1=排队中 2=生成中 3=成功 4=失败 | integer |
| errorCode | 错误码 | string |
| errorMsg | 错误描述 | string |
| resultList | 结果图片数组 | array |
| resultList[].id | **图片 ID**（用于刷新地址） | number |
| resultList[].status | 0=生成中 1=成功 2=失败 | integer |
| resultList[].url | 高清图临时地址（有效期 8 小时） | string |
| resultList[].width | 宽 | integer |
| resultList[].height | 高 | integer |
| resultList[].format | 格式 | string |
| resultList[].size | 大小（字节） | integer |
| resultList[].extendField | 扩展参数（如 maskUrl、requestId 等） | object |

---

## 六、刷新结果图片地址

**路径**：`/linkfox-ai/image/v2/info`

**注意**：ID 是**图片 ID**（resultList[].id），不是作图任务 ID。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| id | 图片 ID | 是 | number |
| downloadFormat | 下载格式，如 jpg、png | 否 | string |

响应 data 含 url（新的图片访问地址）。

---

## 七、AI 换模特

**路径**：`/linkfox-ai/image/v2/make/changeModel`

**注意**：与 AI 换模特 2.0 的差异——生成的模特脸部更随机，使用同一个头部图，生成的模特脸部有细微变化。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 模特原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |
| imageSegUrl | 模特原图保留区抠图结果 | 否 | string |
| modelHeadImageUrl | 模特头部图。格式：jpg/jpeg/png/webp，5M 以内，最小 512x512，最大 2048x2048。或调用作图素材(type=1) | 是 | string |
| sceneImgUrl | 场景参考图。格式：jpg/jpeg/png/webp，10M 以内，最小 768x768，最大 4096x4096。或调用作图素材(type=2 预设场景/type=4 场景素材)。建议使用场景素材，效果稳定 | 否 | string |
| sceneStrength | 场景相似度，值越大越相似，[0,1]，默认 0.7 | 否 | string |
| modelPrompt | 模特特征参数，多选用逗号拼接 | 否 | string |
| customPrompt | 自定义描述，最多 600 字符 | 否 | string |
| customNegPrompt | 画面中不需要的元素 | 否 | string |
| genOriRes | 是否生成原分辨率图，默认 false | 否 | boolean |
| realModel | 原图是否真人模特（false 为人台），默认 true | 否 | boolean |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

**模特特征参数字典：**

| 类型 | 可选值 |
|------|--------|
| 表情 | 微笑、大笑 |
| 姿势 | 坐着、躺着 |
| 体型 | 肥胖、微胖、苗条 |
| 角度 | 侧身、侧脸 |
| 其他 | 背面、光头 |

---

## 八、AI 换模特-2.0

**路径**：`/linkfox-ai/image/v2/make/changeModelFixed`

**注意**：与 AI 换模特的差异——生成的模特脸部更固定，使用同一个头部图，脸部变化很小。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 模特原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |
| imageSegUrl | 模特原图保留区抠图结果 | 否 | string |
| modelImageUrl | 模特头部图。或调用作图素材(type=3) | 是 | string |
| sceneImgUrl | 场景图。或调用作图素材(type=4) | 否 | string |
| sceneStrength | 场景相似度 [0,1]，默认 0.7 | 否 | string |
| genOriRes | 是否生成原分辨率图，默认 false | 否 | boolean |
| realModel | 原图是否真人模特，默认 true | 否 | boolean |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 九、模特换场景

**路径**：`/linkfox-ai/image/v2/make/modelChangeScene`

**注意**：sceneImgUrl 与 scenePrompt 二选一必填。建议使用场景素材（type=4），效果稳定。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 模特原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |
| imageSegUrl | 模特抠图结果 | 否 | string |
| sceneImgUrl | 场景图。或作图素材(type=2/4)。与 scenePrompt 二选一 | 条件 | string |
| scenePrompt | 场景描述。与 sceneImgUrl 二选一 | 条件 | string |
| sceneStrength | 场景相似度 [0,1]，默认 0.7 | 否 | string |
| genOriRes | 是否生成原分辨率图，默认 false | 否 | boolean |
| realModel | 原图是否真人模特，默认 true | 否 | boolean |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 十、AI 穿衣-上下装

**路径**：`/linkfox-ai/image/v2/make/fittingRoom`

**注意**：upperOriginUrl 与 downOriginUrl 至少填一项。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| upperOriginUrl | 上衣原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 4096x4096 | 与下衣二选一 | string |
| upperImageUrl | 上衣抠图结果 | 否 | string |
| downOriginUrl | 下装原图。同上衣格式要求 | 与上衣二选一 | string |
| downImageUrl | 下装抠图结果 | 否 | string |
| modelImageUrl | 模特姿势图。或作图素材(type=5) | 是 | string |
| modelMaskImageUrl | 模特穿戴区域图（黑白图，黑色为穿戴区域） | 否 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 十一、AI 穿衣-连体衣

**路径**：`/linkfox-ai/image/v2/make/fittingRoomSuit`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| suitOriginUrl | 连体衣原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 4096x4096 | 是 | string |
| suitImageUrl | 连体衣抠图结果 | 否 | string |
| modelImageUrl | 模特姿势图。或作图素材(type=6) | 是 | string |
| modelMaskImageUrl | 模特穿戴区域图（黑白图，黑色为穿戴区域） | 否 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 十二、AI 穿戴

**路径**：`/linkfox-ai/image/v2/make/intelligentWear`

**注意**：穿戴模特原图为自定义图片时，targetMaskUrl 必填。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 穿戴商品图。格式：jpg/jpeg/png/webp，尺寸 300x300~4096x4096，宽高比 0.4~2.5 | 是 | string |
| targetOriginUrl | 穿戴模特原图。自定义地址或作图素材(type=7) | 是 | string |
| targetMaskUrl | 穿戴区域图（黑白图，黑色为穿戴区域）。自定义模特图时必填 | 条件 | string |
| productCategory | 商品品类，见下表 | 否 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

**商品品类字典：**

| 值 | 说明 |
|------|------|
| footwear | 鞋靴 |
| luggage | 箱包 |
| eyewear | 眼镜 |
| necklace | 项链 |
| hat | 帽子 |
| earring | 耳环 |
| ring | 戒指 |
| wristband | 手环手链 |
| watch | 手表 |
| headwear | 头饰 |
| belt | 皮带 |
| other | 其他 |

---

## 十三、商品替换

**路径**：`/linkfox-ai/image/v2/make/shopReplace`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 商品原图。格式：jpg/jpeg/png/webp，20M 以内，最小 384x384，最大 8192x8192 | 是 | string |
| sourceImageUrl | 原图的抠图结果 | 否 | string |
| targetOriginUrl | 替换的目标原图 | 是 | string |
| targetImageUrl | 目标原图抠图结果 | 否 | string |
| denoiseStrength | 生成图变化程度，[0,1]，默认 0.5，越大变化越高 | 否 | string |
| imageOutputWidth | 输出宽度，最长边不超过 4096，最短边不低于 32 | 否 | number |
| imageOutputHeight | 输出高度，同上。不传或只传一个时与原图尺寸一致 | 否 | number |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 十四、场景裂变

**路径**：`/linkfox-ai/image/v2/make/sceneFission`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |
| segImageUrl | 保留区域图 | 否 | string |
| strength | 相似度 [0.1,1]，默认 0.5，越大越相似，浮点数小数点后一位 | 否 | string |
| prompt | 强化内容描述，不传则自动提取，最长 600 字符 | 否 | string |
| imageOutputWidth | 输出宽度，最长不超过 2048，最短不低于 32 | 否 | number |
| imageOutputHeight | 输出高度，同上。不传时最长边固定 1024，最短边按原图比例调整 | 否 | number |
| provider | 模式：SCENE_FISSION_REALISTIC=写实（默认），SCENE_FISSION_SIMPLE=简约，SCENE_FISSION_INTELLIGENT=智能 | 否 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 十五、场景图生成（AI 绘图）

**路径**：`/linkfox-ai/image/v2/make/aiDraw`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| prompt | 生图描述 | 是 | string |
| imageUrl | 参考图 | 否 | string |
| style | 生图风格，可选：场景素材/人物素材/古韵国风/传神素描/赛博朋克/像素插画/静谧水墨/动漫线稿/新海诚/宫崎骏/CG/黑白插画/复古日漫/Q版人物/写实油画/C4D剪纸/灵韵水彩/清新日漫 | 否 | string |
| scale | 宽高比，默认 1:1，可选 1:1/16:9/9:16 | 否 | string |
| outputNum | 输出张数 [1,4]，默认 4 | 否 | number |

---

## 十六、相似图裂变

**路径**：`/linkfox-ai/image/v2/make/imageToImage`

**注意**：自定义尺寸（width+height）与 scale 二选一。宽高只传一个时取原图对应值。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 参考图。格式：jpg/png/webp，10M 以内，最大 4096x4096 | 是 | string |
| prompt | 生图描述，不填则自动提取，最多 600 字符 | 否 | string |
| weight | 相似度 [0,2]，默认 2 | 否 | integer |
| width | 自定义宽度，最小 384，最大 4096 | 否 | integer |
| height | 自定义高度，最小 384，最大 4096 | 否 | integer |
| scale | 宽高比字符串（如 16:9），与自定义尺寸二选一 | 否 | string |
| outputNum | 输出张数 [1,4]，默认 4 | 否 | number |

---

## 十七、自动抠图

**路径**：`/linkfox-ai/image/v2/make/cutout`

**注意**：clothClass 仅在 subType=9（服饰）时生效，可多选以逗号分割，多选会合并抠图结果。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |
| subType | 抠图类型：1=通用，2=人像，3=商品，9=服饰，12=头发，13=人脸 | 是 | integer |
| clothClass | 服饰抠图分类（subType=9 时生效），可多选逗号分割：tops/coat/skirt/pants/bag/shoes/hat | 否 | string |

---

## 十八、精细抠图-创建任务

**路径**：`/linkfox-ai/v2/process/result/interactCutout/create`

**注意**：pointList 中 x/y 为归一化坐标（0~1），isSelect 1=选中 0=不选中。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图 | 是 | string |
| scoreUrl | 概率图（迭代时传入上一次返回的 scoreUrl） | 否 | string |
| featureUrl | 全局分割图（同上） | 否 | string |
| pointList | 点位操作列表 | 是 | array |
| pointList[].x | 与左边缘距离 / 图片宽度，0~1 | 是 | number |
| pointList[].y | 与上边缘距离 / 图片高度，0~1 | 是 | number |
| pointList[].isSelect | 0=不选中，1=选中 | 是 | integer |

---

## 十九、精细抠图-获取结果

**路径**：`/linkfox-ai/v2/process/result/interactCutout/info`

**注意**：status 1=已创建 2=执行中 3=成功 4=失败。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| id | 精细抠图任务 ID | 是 | string |

响应 data：id、status、result（maskUrl/scoreUrl/imageUrl/featureUrl）。

---

## 二十、图片高清放大

**路径**：`/linkfox-ai/image/v2/make/superResolution`

**注意**：放大后结果图最长边最大 8192。例如 3000x3000 放大 4 倍 → 8192x8192。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，最大 4096x4096 | 是 | string |
| magnification | 放大倍数 [1,4]（浮点数），只高清不放大传 1 | 是 | float |
| enhanceQuality | 是否高清化 | 否 | boolean |

---

## 二十一、智能扩图

**路径**：`/linkfox-ai/image/v2/make/expandImage`

**注意**：原图尺寸 300x300~4096x4096，宽高比 0.4~2.5。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp | 是 | string |
| width | 期望扩图后宽度 | 是 | number |
| height | 期望扩图后高度 | 是 | number |
| prompt | 提示词，最多 600 字符 | 否 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 二十二、图片翻译

**路径**：`/linkfox-ai/image/v3/make/imageTransl`

**注意**：原图最大 3000x3000，4M 以内。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，4M 以内，最小 385x385，最大 3000x3000 | 是 | string |
| translationPlatform | 翻译源：deepl / chatgpt | 是 | string |
| sourceLanguage | 源语种代码 | 是 | string |
| targetLanguage | 目标语种代码 | 是 | string |

**源语种代码：** CHS(中文)、ENG(英文)、CHT(繁体中文)、ESP(西班牙语)、JPN(日语)、KOR(韩语)、PT(葡萄牙语)、ROM(罗马尼亚语)、RUS(俄语)、VIN(越南语)、DEU(德语)

**目标语种代码：** AR(阿拉伯语)、BG(保加利亚语)、BN(孟加拉语)、CHS(中文)、CHT(繁体中文)、CKB(中库尔德语)、CSY(捷克语)、DA(丹麦语)、DEU(德语)、EL(希腊语)、ENG(英语)、ESP(西班牙语)、ET(爱沙尼亚语)、FA(波斯语)、FI(芬兰语)、FIL(菲律宾语)、FRA(法语)、GU(古吉拉特语)、HE(希伯来语)、HI(印地语)、HR(克罗地亚语)、HUN(匈牙利语)、ID(印尼语)、ITA(意大利语)、JPN(日语)、JW(爪哇语)、KOR(韩语)、LO(老挝语)、LT(立陶宛语)、LV(拉脱维亚语)、MR(马拉地语)、MS(马来语)、MY(缅甸语)、NLD(荷兰语)、NO(挪威语)、PLK(波兰语)、PT(葡萄牙语)、PTB(葡萄牙语)、ROM(罗马尼亚语)、RUS(俄语)、SK(斯洛伐克语)、SL(斯洛文尼亚语)、SV(瑞典语)、SW(斯瓦希里语)、TA(泰米尔语)、TE(泰卢固语)、TG(塔吉克语)、TH(泰语)、TL(他加禄语)、TRK(土耳其语)、UK(乌克兰语)、UR(乌尔都语)、VIN(越南语)

---

## 二十三、手部修复

**路径**：`/linkfox-ai/image/v2/make/handRepair`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，尺寸 300x300~4096x4096，宽高比 0.4~2.5 | 是 | string |
| personType | 人物类型：0=女孩，1=男孩，2=成年女性，3=成年男性 | 是 | number |
| maskUrl | 修复区域（黑白图，白色为修复区域） | 否 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 二十四、局部重绘

**路径**：`/linkfox-ai/image/v2/make/areaRepair`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，尺寸 300x300~4096x4096，宽高比 0.4~2.5 | 是 | string |
| prompt | 提示词，最多 600 字符 | 是 | string |
| maskUrl | 重绘区域图（黑白图，白色为重绘区域） | 是 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 二十五、印花提取

**路径**：`/linkfox-ai/image/v2/make/printExtract`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |

---

## 二十六、消除笔

**路径**：`/linkfox-ai/image/v2/make/interactErase`

**注意**：原图尺寸 300x300~4096x4096，宽高比 0.4~2.5。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。格式：jpg/jpeg/png/webp | 是 | string |
| maskImageUrl | 消除区域图（黑白图，白色为消除区域） | 是 | string |

---

## 二十七、手持商品

**路径**：`/linkfox-ai/image/v2/make/handHeld`

**注意**：手持姿势图为自定义图片时 targetMaskUrl 必填。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 手持商品图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |
| targetOriginUrl | 手持姿势图。自定义地址或作图素材(type=8) | 是 | string |
| targetMaskUrl | 手持区域图（黑白图，尺寸与姿势图一致）。自定义姿势图时必填 | 条件 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | number |

---

## 二十八、饰品文字

**路径**：`/linkfox-ai/image/v2/make/linkedWord`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| fontname | 字体名称（见下方列表） | 是 | string |
| fontSize | 输出字体大小 | 是 | integer |
| left | 左边加环，默认 false | 否 | boolean |
| right | 右边加环，默认 false | 否 | boolean |
| prompt | 饰品文字内容 | 是 | string |

**可选字体：** Caitlyn、ItaliannoRob、Alison、ALSScript、WhiteAngelica、Milkshake、ScriptMTBold、PassionsConflictROB、Sacramento、Cervanttis、Notera 2 PERSONAL USE ONLY、UyghurMerdane、OldEnglishText、Halimun、AlexBrush、Scriptina、CounselorScript、EliannaBoldItalic、AutumnChant、MagnoliaScript

---

## 二十九、商品精修

**路径**：`/linkfox-ai/image/v2/make/productRepair`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 商品原图。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 8192x8192 | 是 | string |

---

## 三十、图片获取描述词-创建任务

**路径**：`/linkfox-ai/v2/process/result/imageToPrompt/create`

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| type | 应用类型：5=相似图裂变，13=场景裂变，69=穿衣套图卖点分析，71=商品套图卖点分析 | 是 | string |
| imageUrlList | 图片地址列表（只有套图卖点分析支持多张） | 是 | List\<string\> |
| keyword | 关键字。场景裂变时有效；套图卖点分析时可传入商品信息 | 否 | string |
| provider | 套图模式提取类型：API_PRE_POINT=卖点分析（默认），API_LAYOUT_DESC=排版描述 | 否 | string |

---

## 三十一、图片获取描述词-获取结果

**路径**：`/linkfox-ai/v2/process/result/imageToPrompt/info`

**注意**：status 1=已创建 2=执行中 3=成功 4=失败。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| id | 任务 ID | 是 | string |

响应 data：id、status、result.content（描述词文本）。

---

## 三十二、智能修图

**路径（新版本优先）**：`/linkfox-ai/image/v2/make/imageEditV2`

**版本说明**：
- 自 **2026/03/13** 起，统一使用 `imageEditV2`。
- 旧版 `imageEdit` 视为**废弃接口**，仅用于历史兼容，不建议继续接入。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图。支持 jpg/jpeg/png/webp；尺寸 300x300 ~ 4096x4096；宽高比 0.4 ~ 2.5 | 是 | string |
| prompt | 提示词 | 是 | string |
| provider | 模型：BANANA / BANANA_2 / BANANA_PRO / WAN2_7 / SEEDREAM5 / GPT_2_IMAGE / AIDRAW_EDIT | 是 | string |
| outputNum | 输出张数 [1,4]，默认 1 | 否 | integer |
| resolution | 分辨率：1K / 2K / 4K。BANANA_PRO / GPT_2_IMAGE 默认 2K，其余默认 1K。WAN2_7 / AIDRAW_EDIT 不支持 4K / SEEDREAM5 不支持 1K、4K | 否 | string |
| aspectRatio | 可选：1:1、3:4、4:3、4:5、5:4、16:9、9:16、2:3、3:2、21:9（SEEDREAM5 不支持 4:5 / 5:4） | 否 | string |
| supplyType | 供应模式：eco（经济）/ stable（稳定，默认）。仅 BANANA 系列生效 | 否 | string |
| needOptimize | 是否提示词优化：true/false | 否 | boolean |
| template | 提示词模板名称（单图模板，见下方可选值说明。模板中的 provider、needOptimize 优先级更高） | 否 | string |
| quality | 输出品质：low / medium / high，仅 GPT_2_IMAGE 生效，默认 medium | 否 | string |

**template 可选值（单图）：**

`白底图`、`商品主图精修`、`生成场景`、`海报制作`、`加人或物`、`换动物`、`服装平铺`、`3D服装`、`人台换模特`、`卡通插画`、`改身材`、`更换风格`、`移除元素`、`文字消除`、`去除水印`、`添加水印`

---

## 三十三、智能修图-多图

**路径（新版本优先）**：`/linkfox-ai/image/v2/make/multiImageFusionV2`

**版本说明**：
- 自 **2026/03/13** 起，统一使用 `multiImageFusionV2`。
- 旧版 `multiImageFusion` 视为**废弃接口**，仅用于历史兼容，不建议继续接入。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageList | 图片列表。支持 jpg/jpeg/png/webp（10M 以内），最小 800x800，最大 4096x4096。最多12张 | 是 | array[string] |
| provider | 模型：BANANA / BANANA_2 / BANANA_PRO / WAN2_7 / SEEDREAM5 / GPT_2_IMAGE / AIDRAW_EDIT | 是 | string |
| prompt | 强化内容描述（100 字以内） | 否 | string |
| outputNum | 输出张数，默认 1 | 否 | integer |
| resolution | 分辨率：1K / 2K / 4K。BANANA_PRO / GPT_2_IMAGE 默认 2K，其余默认 1K。WAN2_7 / AIDRAW_EDIT 不支持 4K / SEEDREAM5 不支持 1K、4K | 否 | string |
| aspectRatio | 可选：1:1、3:4、4:3、4:5、5:4、16:9、9:16、2:3、3:2、21:9（SEEDREAM5 不支持 4:5 / 5:4） | 否 | string |
| supplyType | 供应模式：eco（经济）/ stable（稳定，默认）。仅 BANANA 系列生效 | 否 | string |
| needOptimize | 是否提示词优化：true/false。仅 BANANA_PRO 支持 | 否 | boolean |
| template | 提示词模板名称（多图模板，见下方可选值说明。模板中的 provider、needOptimize 优先级更高） | 否 | string |
| quality | 输出品质：low / medium / high，仅 GPT_2_IMAGE 生效，默认 medium | 否 | string |

**template 可选值（多图）：**

`搭配融图`、`搭配上身`

---

## 三十四、商品套图

**路径（新版本优先）**：`/linkfox-ai/image/v2/make/productMarketMaterialV3`

**版本说明**：
- 自 **2026/03/13** 起，统一使用 `productMarketMaterialV3`。
- 旧版 `productMarketMaterialV2` 视为**废弃接口**，仅用于历史兼容，不建议继续接入。

**注意**：
- imageList 最多 5 张，最小 800x800，最大 4096x4096，10M 以内。
- 各类型数量（aPlusNum/aPlusProNum/sellerTypeNum/sceneTypeNum/closeUpTypeNum/closeUpWhiteTypeNum/whiteBgTypeNum）单项最大 **12**。
- aPlusStyles/pointStyles 传入时，数量需与目标生成数量一致。
- brandKey 为 JSON 对象，总长度不超过 1000 字符。
- 结果通过获取作图结果接口轮询，`resultList[].extendField.type` 标识图片类型，参见下方「参数→输出 type 映射」。

**参数→输出 type 映射：**

| 参数 | 生成内容 | `extendField.type` |
|------|----------|---------------------|
| aPlusNum | 普通 A+ 排版图 | APlusNormal |
| aPlusProNum | 高级 A+ 排版图 | APlusPro |
| aPlusHasPhone | 手机版 A+（基于高级 A+ 结果） | APlusHasPhone |
| sellerTypeNum | 卖点图 | sellPoint |
| sceneTypeNum | 场景图 | scene |
| closeUpTypeNum | 特写图 | closeUp |
| closeUpWhiteTypeNum | 白底特写图 | closeUpWhite |
| whiteBgTypeNum | 白底图 | whiteBg |

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageList | 商品图片列表（最多 5 张） | 是 | array[string] |
| sellerPoint | 商品卖点描述，最多 2500 字符（未开启自动提取卖点描述时校验必填） | 是 | string |
| provider | 模型：BANANA_PRO（Pro）/ BANANA_2（基础版 2 代）/ WAN2_7（万相2.7）/ GPT_2_IMAGE（GPT图片2）/ AIDRAW_EDIT（自研修图） | 是 | string |
| aPlusNum | 普通 A+ 数量，默认 0，最大 12 | 否 | integer |
| aPlusProNum | 高级 A+ 数量（Pro），默认 0，最大 12 | 否 | integer |
| aPlusHasPhone | 是否生成手机版 A+（基于高级 A+ 结果，数量与高级 A+ 一致），默认 false | 否 | boolean |
| aPlusAspectRatio | 自定义 A+ 宽高比（仅高级 A+ 场景使用），如 16:9/9:16/1:1 | 否 | string |
| aPlusStyles | A+ 排版列表，id（风格 id，通过作图素材接口获取）或 prompt（排版词，通过排版描述接口获取） | 否 | List |
| sellerTypeNum | 卖点图数量，默认 0，最大 12 | 否 | integer |
| isExtractPrePoint | 是否自动提取卖点：true 开启 false 关闭，默认 false | 否 | boolean |
| sceneTypeNum | 场景图数量，默认 0，最大 12 | 否 | integer |
| closeUpTypeNum | 特写图数量，默认 0，最大 12 | 否 | integer |
| closeUpWhiteTypeNum | 白底特写图数量，默认 0，最大 12 | 否 | integer |
| whiteBgTypeNum | 白底图数量，默认 0，最大 12 | 否 | integer |
| pointStyles | 卖点图排版列表（同 aPlusStyles 格式） | 否 | List |
| aspectRatio | 素材宽高比：1:1/3:2/2:3/4:3/3:4/4:5/5:4/16:9/9:16/21:9 | 否 | string |
| brandKey | 品牌基因 JSON：brandColor(#RRGGBB)/fontStyle/salesRegion/language/platform/customSettings | 否 | string |
| resolution | 输出分辨率：2K（默认）/4K；AIDRAW_EDIT 支持 1K / 2K | 否 | string |
| quality | 输出品质：low / medium / high，仅 GPT_2_IMAGE 生效，默认 medium | 否 | string |

---

## 三十五、服装套图

**路径（新版本优先）**：`/linkfox-ai/image/v2/make/wearCollectionV2`

**版本说明**：
- 自 **2026/03/13** 起，统一使用 `wearCollectionV2`。
- 旧版 `wearCollection` 视为**废弃接口**，仅用于历史兼容，不建议继续接入。

**注意**：
- imageList 最多 5 张，最小 384x384，最大 4096x4096，10M 以内。
- 各类型数量（aPlusNum/aPlusProNum/modelTypeNum/insTypeNum/sellerTypeNum/sizeTypeNum/whiteTypeNum）单项最大 **12**。
- sellerPoint 建议包含面料、卖点、目标人群、使用场景、尺码等信息，有助于提升结果质量。
- 结果通过获取作图结果接口轮询，`resultList[].extendField.type` 标识图片类型，参见下方「参数→输出 type 映射」。

**参数→输出 type 映射：**

| 参数 | 生成内容 | `extendField.type` |
|------|----------|---------------------|
| aPlusNum | 普通 A+ 排版图 | APlusNormal |
| aPlusProNum | 高级 A+ 排版图 | APlusPro |
| aPlusHasPhone | 手机版 A+（基于高级 A+ 结果） | APlusHasPhone |
| modelTypeNum | **模特+场景合成图**（非纯模特图） | **scene** |
| insTypeNum | 种草图 | ins |
| sellerTypeNum | 卖点图 | point |
| sizeTypeNum | 尺码图 | size |
| whiteTypeNum | 白底图 | white |

> **⚠️ 特别说明**：`modelTypeNum` 生成的是**模特穿上服装并置于场景中的合成图**，输出 type 为 `scene`，而非 `model`。命名虽含 "model"，但产出是模特+场景的完整合成结果。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageList | 商品图片列表（最多 5 张） | 是 | array[string] |
| sellerPoint | 商品卖点描述，最多 2500 字符（未开启自动提取卖点描述时校验必填） | 是 | string |
| provider | 模型：BANANA_PRO（Pro）/ BANANA_2（基础版 2 代）/ WAN2_7（万相2.7）/ GPT_2_IMAGE（GPT图片2） | 是 | string |
| aPlusNum | 普通 A+ 数量，默认 0，最大 12 | 否 | integer |
| aPlusProNum | 高级 A+ 数量，默认 0，最大 12 | 否 | integer |
| aPlusHasPhone | 是否生成手机版 A+（基于高级 A+ 结果，数量与高级 A+ 一致），默认 false | 否 | boolean |
| aPlusAspectRatio | A+ 宽高比，不填则自动选择；支持 16:9/9:16/1:1 | 否 | string |
| aPlusStyles | A+ 排版列表（id 或 prompt） | 否 | List |
| modelTypeNum | **模特+场景合成图**数量（输出 type=`scene`），默认 0，最大 12 | 否 | integer |
| ↳ modelImageUrl | 模特参考图，未设置时启动智能模式。**仅 modelTypeNum > 0 时生效** | 否 | string |
| ↳ sceneImageUrl | 场景参考图，未设置时启动智能模式。**仅 modelTypeNum > 0 时生效** | 否 | string |
| ↳ isExactScene | 场景裂变模式：true=遵循背景（默认），false=相似裂变。**仅 modelTypeNum > 0 时生效** | 否 | boolean |
| ↳ modelAndSceneInfo | 描述想要的场景内容和模特特征。**仅 modelTypeNum > 0 时生效** | 否 | string |
| insTypeNum | 种草图数量，默认 0，最大 12 | 否 | integer |
| sellerTypeNum | 卖点图数量，默认 0，最大 12 | 否 | integer |
| isExtractPrePoint | 是否自动提取卖点：true 开启 false 关闭，默认 false | 否 | boolean |
| pointStyles | 卖点图排版列表（同 aPlusStyles 格式） | 否 | List |
| sizeTypeNum | 尺码图数量，默认 0，最大 12 | 否 | integer |
| whiteTypeNum | 白底图数量，默认 0，最大 12 | 否 | integer |
| aspectRatio | 素材宽高比：1:1/3:2/2:3/4:3/3:4/4:5/5:4/16:9/9:16/21:9 | 否 | string |
| brandKey | 品牌基因 JSON（同商品套图） | 否 | string |
| resolution | 输出分辨率：2K（默认）/4K | 否 | string |
| quality | 输出品质：low / medium / high，仅 GPT_2_IMAGE 生效，默认 medium | 否 | string |

---

## 三十六、姿势裂变

**路径**：`/linkfox-ai/image/v2/make/modelPoseFission`

**注意**：postureUrl（素材 type=9）与 prompt 二选一。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 图片地址。格式：jpg/jpeg/png/webp，20M 以内，最小 385x385，最大 4096x4096 | 是 | string |
| prompt | 自定义姿势描述。与 postureUrl 二选一 | 否 | string |
| postureUrl | 姿势图片 URL。作图素材(type=9)或自定义。与 prompt 二选一 | 否 | string |
| outputNum | 输出数量 [1,4]，默认 1 | 否 | number |

---

## 三十七、带货口播

**路径**：`/linkfox-ai/image/v2/make/salesVideo`

**注意**：
- 该接口返回任务 ID（`taskId`），需继续轮询「获取作图结果」接口查询最终资源。
- `prompt` 建议包含商品卖点、目标人群、使用场景和行动指令，以提升口播质量。
- `imageList` 传入商品主图/细节图通常能提升视频一致性和转化表达。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| prompt | 口播脚本/提示词 | 是 | string |
| imageList | 参考图 URL 列表（建议 1~6 张） | 否 | array[string] |
| videoType | 模型类型：WAN / SEED（seed = seedance） | 是 | string |
| videoTime | 视频时长（秒）。WAN: 10/15秒；SEED: 5/10/15秒 | 否 | number |
| isPro | 是否开启高质量模式（SEED 专用，等同 resolution=720p） | 否 | boolean |
| aspectRatio | 视频比例：16:9 / 9:16 | 否 | string |
| resolution | 视频分辨率。仅SEED类型支持，可选值：480p/720p/1080p（默认480p）。传入时优先于 isPro | 否 | string |

---

## 三十八、图转视频

**路径**：`/linkfox-ai/image/v2/make/imageToVideo`

**注意**：
- 该接口返回任务 ID，需继续轮询「获取作图结果」接口查询最终视频地址。
- 不同模型支持的参数和时长不同，详见下方「各模型参数支持情况」。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| imageUrl | 原图地址。格式：jpg/jpeg/png/webp | 是 | string |
| videoType | 模型类型：KLING（可灵）/ V（电影/Veo）/ WAN（万相）/ SEED（Seedance/豆包）/ HAILUO（海螺） | 是 | string |
| videoTime | 视频时长（秒），不同类型支持的时长不同，见下方对照 | 是 | number |
| prompt | 视频提示词（2000 字以内） | 否 | string |
| promptOptimizer | 是否开启提示词优化：true/false，默认 false | 否 | boolean |
| isPro | 是否开启高质量/Pro 模式，默认 false（SEED 专用，等同 resolution=720p） | 否 | boolean |
| voice | 是否生成声音：true/false，默认 false | 否 | boolean |
| lastFrameImageUrl | 尾帧图地址（用于控制视频结束帧画面） | 否 | string |
| aspectRatio | 视频比例：16:9 / 9:16 | 否 | string |
| camera | 运镜参数：single（单镜头）/ multi（多镜头），仅WAN类型支持 | 否 | string |
| resolution | 视频分辨率。仅SEED类型支持，可选值：480p/720p/1080p（默认480p）。传入时优先于 isPro | 否 | string |

**各模型参数支持情况：**

| 参数 | KLING（可灵） | V（电影/Veo） | WAN（万相） | SEED（Seedance/豆包） | HAILUO（海螺） |
|------|:---:|:---:|:---:|:---:|:---:|
| videoTime（时长） | 5 / 10 秒 | 4 / 8 秒 | 10 / 15 秒 | 5 / 10 / 15 秒 | 6 / 10 秒 |
| prompt（提示词） | 支持 | 支持 | 支持 | 支持 | 支持 |
| promptOptimizer（提示词优化） | 支持 | 支持 | 支持 | 支持 | 支持 |
| isPro（Pro 模式） | 支持 | 支持 | - | 支持 | 支持 |
| voice（生成声音） | - | - | 支持 | 支持 | - |
| camera（运镜） | - | - | single / multi | - | - |
| lastFrameImageUrl（尾帧图） | 支持 | 支持 | 支持 | 不支持 | 不支持 |
| aspectRatio（视频比例） | 传入不生效 | 16:9 / 9:16，未传默认 9:16 | - | 16:9 / 9:16 | 传入不生效 |
| resolution（分辨率） | - | - | - | 480p / 720p / 1080p，默认 480p | - |

---

## 三十九、视频复刻

**路径**：`/linkfox-ai/image/v2/make/videoReclone`

**注意**：
- 该接口返回任务 ID，需继续轮询「获取作图结果」接口查询最终视频地址。
- `refVideoUrl` 必须为稳定可访问的公网 URL，异步分析阶段才访问，短期签名 URL 可能已过期。
- `refImageList` 中的图片在提交任务时**同步**下载，若图片无法访问，任务创建立即报错。
- `SEED_FAST` 不支持 `1080P` 分辨率，传入会报错。
- 视频复刻涉及多步 AI 分析，通常比图片任务耗时更长，建议轮询间隔 5~10 秒。

| 参数 | 说明 | 必填 | 类型 |
|------|------|------|------|
| refVideoUrl | 参考视频的公网 URL（需长期有效，避免使用短期签名 URL） | 是 | string |
| refImageList | 参考商品图 URL 列表，1~6 张可访问外网的图片 URL | 是 | array[string] |
| videoType | 模型类型：SEED / SEED_FAST | 是 | string |
| duration | 目标视频时长（秒），范围 5~15 的整数 | 是 | number |
| resolution | 视频分辨率，见下方对照表 | 是 | string |
| saleCountry | 销售国家（如 CN、US） | 是 | string |
| targetLanguage | 目标语言（如 zh、en） | 是 | string |
| ratio | 视频比例：16:9 / 9:16 / 1:1 / 3:4 / 4:3 / 21:9 | 否 | string |
| productInfo | 补充商品文字信息，用于辅助 AI 分析，最多 2500 字符 | 否 | string |

**各模型参数支持情况：**

| 参数 | SEED（Seedance/豆包） | SEED_FAST（Seedance 2.0 Fast） |
|------|:---:|:---:|
| duration（时长） | 5~15 秒整数 | 5~15 秒整数 |
| resolution（分辨率） | 480P / 720P / 1080P | 480P / 720P（不支持 1080P） |
| ratio（视频比例） | 16:9 / 9:16 / 1:1 / 3:4 / 4:3 / 21:9 | 16:9 / 9:16 / 1:1 / 3:4 / 4:3 / 21:9 |
| refImageList 上限 | 6 张 | 6 张 |
