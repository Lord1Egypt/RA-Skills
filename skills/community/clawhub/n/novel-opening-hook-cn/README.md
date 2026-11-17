# 小说开篇钩子改稿

![小说开篇钩子改稿](assets/promo-1600x900.png)

把中文小说开篇改成快节奏、悬念节奏、沉浸节奏三版，保留人物设定与核心事件。每版附原文定位和修改理由，最后推荐最适合读者的一版。直接将原文交给支持 Skill 的助手即可，无需浏览器或额外 API Key。

## 立即使用

把下面这段话连同开篇原文交给 Skill：

```text
请用小说开篇钩子改稿处理这段都市悬疑开头。必须保留：哥哥失踪三年后出现、无牌黑车、木匣、不要回家的警告。

林晚在雨里等了四十分钟，才等到那辆没有牌照的黑车。车门一开，失踪三年的哥哥坐在后排，怀里抱着她以为烧掉的木匣。

他没有叫她的名字，只把一把生锈的钥匙塞进她手里：‘别回家。’
```

你会得到：快节奏、悬念节奏、沉浸节奏三版改稿；每版都有可搜索定位的修改理由；最后附一版推荐稿。完整机器可读样例在 [fixtures/success-input.json](fixtures/success-input.json)。若只给题材而没有开篇原文，Skill 会明确提示资料缺失，见 [fixtures/failure-input.json](fixtures/failure-input.json)。

## 边界

只改用户提供的开篇范围，不生成整本小说、后续章节或大纲；不做六维审稿。不会为了制造钩子凭空增加死亡、反转、系统或身份设定。

## 安装与校验

复制或安装本目录后，无需配置 API Key。运行：

```bash
node scripts/self-test.mjs
```

## 许可证

本 Skill 提供原创开篇改稿指令与示例，采用 [MIT-0](LICENSE)。

## 安装

```bash
npx skills add xxjrq/novel-opening-hook-cn
```

也可以把本仓库目录复制到 Agent 的 Skills 目录，再用 `$novel-opening-hook-cn` 加上你的输入调用。
